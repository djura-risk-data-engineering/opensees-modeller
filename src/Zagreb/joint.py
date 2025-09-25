"""
----------------------------------------------------------------
OpenSees procedures for modelling RC Beam-Column Joints
The original method was created in tcl by Gerard J. O'Reilly
The current Python method was adapted from tcl by Volkan Ozsarac
----------------------------------------------------------------

The procedure also requires MPa units to be specified in the units file.

This script contains a number of functions that will create a beam-column
joint. This was developed for interior and exterior beam column joints which
possess no joint reinforcement and have smooth bars with end-hooks. The full
derivation of the the terms used in these models can be found in
O'Reilly [2016]. The joint basically consists of a central node pair that has
a rotational hinge defined based on the specified properties of the joint.
Rigid offsets illustrated in the joint model diagrams are intnded to be
incorporated with rigid end offsets in the element transformations definition
for modelling efficiency.

In summary, the type of information submitted to these procedures is geometry,
material properties, principal stress in the joint limit-states and hysteretic
properties.

One of the input options is the joint type that is required, which for now are
Exterior, Interior, Roof or Elastic. This distongiushes which expressions are
to be used for the moment capacity computation. In the case of elastic joints,
however, all of the inputs requested by the procedure aren't actually needed
for any computation. This is so the command is left the same and the joints
can be turned "on" or "off" relatively easily if doing some form of parameter
study.

References:
O’Reilly, G. J., Sullivan, T. J. [2019] “Modeling Techniques for the Seismic
Assessment of the Existing Italian RC Frame Structures,” Journal of Earthquake
Engineering, Vol. 23, No.8, pp. 1262-1296 DOI: 10.1080/13632469.2017.1360224.
"""

import math
import openseespy.opensees as ops
from .units import MPa


def joint_model(jtype, index, XYZ, M, col, bm, conc, bars, P, H, kappa, gamm,
                hyst, pfile=None, pflag=0):
    """
    Method to create RC Beam-Column Joint model in OpenSeesPy

    Args:
        jtype: "Exterior", "Interior", "Roof", or "Elastic"
        index: joint index (used in tag construction)
        XYZ: (X, Y, Z) in m
        M: mass at node (metric tonnes) -> applied to DOF 1,2
        col: (hcX, hcY) in m
        bm:  (hbX, hbY, bbX, bbY) in m
        conc: (fc, Ec, cv) with MPa & m
        bars: (dbL, dbV) in m
        P: axial load in kN
        H: interstorey height in m
        kappa: list/tuple of 6 kappas (+crack +peak +ult -crack -peak -ult)
        gamm: list/tuple of 6 rotations in rad (same order)
        hyst: list/tuple of 5 hysteretic params
        pfile: file-like object for logging
        pflag: print flag (0/1)
    """
    # --------------------------------------
    # Initial variables
    # --------------------------------------
    X, Y, Z = XYZ
    hcX, hcY = col
    Ac = hcX * hcY
    hbX, hbY, bbX, bbY = bm
    hb = max(hbX, hbY)  # pick larger
    fc, Ec, cv = conc
    dbL, dbV = bars

    # --------------------------------------
    # Nodes
    # --------------------------------------
    n1 = int(f"1{index}")
    n6 = int(f"6{index}")
    ops.node(n1, X, Y, Z)
    ops.node(n6, X, Y, Z)
    ops.mass(n1, M, M, 0.0, 0.0, 0.0, 0.0)  # set the masses

    # --------------------------------------
    # Axial material
    # --------------------------------------
    Kspr = 2.0 * Ec * MPa * Ac / hb  # kN/m
    rigM = int(f"1{index}")  # rigid mat
    axM = int(f"2{index}")  # elastic mat
    ops.uniaxialMaterial('Elastic', rigM, 1e15)
    ops.uniaxialMaterial('Elastic', axM, Kspr)

    # --------------------------------------
    # Connection width - Equation 2.48 (O'Reilly, 2016)
    # --------------------------------------
    # X direction
    if hcY >= bbX:
        bjX = hcY
    elif (bbX + 0.5 * hcX) < hcY:
        bjX = bbX + 0.5 * hcX
    else:
        bjX = hcY  # fall-through safeguard

    if hcY < bbX:
        bjX = bbX
    elif (hcY + 0.5 * hcX) < bbX:
        bjX = hcY + 0.5 * hcX

    # Y direction
    if hcX >= bbY:
        bjY = hcX
    elif (bbY + 0.5 * hcY) < hcX:
        bjY = bbY + 0.5 * hcY
    else:
        bjY = hcX  # safeguard

    if hcX < bbY:
        bjY = bbY
    elif (hcX + 0.5 * hcY) < bbY:
        bjY = hcX + 0.5 * hcY

    # --------------------------------------
    # Flexural materials
    # --------------------------------------
    pt = []
    MjX, MjY = [], []
    jX = 0.9 * (hbX - cv - dbV - dbL / 2.0)
    jY = 0.9 * (hbY - cv - dbV - dbL / 2.0)

    for ii in range(6):
        pti = kappa[ii] * math.sqrt(fc) * MPa  # Equation 2.34 (O'Reilly, 2016)
        pt.append(pti)

        if jtype == "Interior":  # Equation 2.55 (O'Reilly, 2016)
            Mx = pti * bjX * hcX * (H * jX / (H - jX)) * (
                1 + P / (bjX * hcX * pti))**0.5
            My = pti * bjY * hcY * (H * jY / (H - jY)) * (
                1 + P / (bjY * hcY * pti))**0.5

        elif jtype == "Exterior":  # Equation 2.33 (O'Reilly, 2016)
            termX = hbX / (2.0 * hcX)
            termY = hbY / (2.0 * hcY)
            Mx = pti * bjX * hcX * (H * jX / (H - jX)) * (termX + (
                termX ** 2 + 1.0 + P / (bjX * hcX * pti))**0.5)
            My = pti * bjY * hcY * (H * jY / (H - jY)) * (termY + (
                termY ** 2 + 1.0 + P / (bjY * hcY * pti))**0.5)

        elif jtype == "Roof":
            termX = hbX / (2.0 * hcX)
            termY = hbY / (2.0 * hcY)
            Mx = 2.0 * pti * bjX * hcX * jX * (termX + (
                termX ** 2 + 1.0 + P / (bjX * hcX * pti))**0.5)
            My = 2.0 * pti * bjY * hcY * jY * (termY + (
                termY ** 2 + 1.0 + P / (bjY * hcY * pti))**0.5)

        elif jtype == "Elastic":
            Mx = pti * bjX * hcX * (H * jX / (H - jX)) * (
                1.0 + P / (bjX * hcX * pti))**0.5
            My = pti * bjY * hcY * (H * jY / (H - jY)) * (
                1.0 + P / (bjY * hcY * pti))**0.5

        else:
            raise ValueError(f"Unknown jtype '{jtype}'")

        MjX.append(1.0 * Mx)
        MjY.append(1.0 * My)

    # Create flexural uniaxial materials
    flX_base = int(f"3{index}")
    flY_base = int(f"4{index}")

    if jtype != "Elastic":
        # Hysteretic (pos: 0,1,2) and (neg: 3,4,5)
        ops.uniaxialMaterial('Hysteretic',
                             flX_base,
                             1.0 * MjX[0],  gamm[0],
                             1.0 * MjX[1],  1.0 * gamm[1],
                             1.0 * MjX[2],  1.0 * gamm[2],
                             -1.0 * MjX[3], -1.0 * gamm[3],
                             -1.0 * MjX[4], -1.0 * gamm[4],
                             -1.0 * MjX[5], -1.0 * gamm[5],
                             hyst[0], hyst[1], hyst[2], hyst[3], hyst[4])

        ops.uniaxialMaterial('Hysteretic',
                             flY_base,
                             1.0 * MjY[0],  gamm[0],
                             1.0 * MjY[1],  1.0 * gamm[1],
                             1.0 * MjY[2],  1.0 * gamm[2],
                             -1.0 * MjY[3], -1.0 * gamm[3],
                             -1.0 * MjY[4], -1.0 * gamm[4],
                             -1.0 * MjY[5], -1.0 * gamm[5],
                             hyst[0], hyst[1], hyst[2], hyst[3], hyst[4])

    else:
        # Elastic equivalent stiffness from first point
        kx = MjX[0] / gamm[0]
        ky = MjY[0] / gamm[0]
        ops.uniaxialMaterial('Elastic', flX_base, kx)
        ops.uniaxialMaterial('Elastic', flY_base, ky)

    # --------------------------------------
    # MinMax limits on rotations
    # --------------------------------------
    gamm_max = 0.100  # Use a higher limit for now, needs to be updated later
    flXM = int(f"5{index}")
    flYM = int(f"6{index}")
    ops.uniaxialMaterial('MinMax', flXM, flX_base,
                         '-min', -gamm_max, '-max', gamm_max)
    ops.uniaxialMaterial('MinMax', flYM, flY_base,
                         '-min', -gamm_max, '-max', gamm_max)

    # --------------------------------------
    # ZeroLength elements
    # --------------------------------------
    ET = int(f"9{index}")
    ops.element('zeroLength', ET, n1, n6,
                '-mat', rigM, rigM, axM, flYM, flXM, rigM,
                '-dir', 1, 2, 3, 4, 5, 6, '-doRayleigh', 1)

    # --------------------------------------
    # Printouts
    # --------------------------------------
    if pflag == 1:
        print(f"Created connection at grid (XYZ): {index}")
        print(f"Coords: {X:.3f} {Y:.3f} {Z:.3f} m")
        print(f"Element: {int(f'17{index}')}")
        print(f"Mass: {M:.1f} tonnes")
        print(f"P: {P:.1f} kN")
        print(f"Concrete: fc: {fc:.1f}MPa Ec: {Ec:.1f}MPa")
        print(f"Joint: bjX: {bjX:.3f}m bjY: {bjY:.3f}m")
        print(f"Kspr: {Kspr:.1f} kN/m")
        print(f"MjX: {MjX[0]:.2f} {MjX[1]:.2f} {MjX[2]:.2f} {-MjX[3]:.2f} "
              f"{-MjX[4]:.2f} {-MjX[5]:.2f} kNm")
        print(f"MjY: {MjY[0]:.2f} {MjY[1]:.2f} {MjY[2]:.2f} {-MjY[3]:.2f} "
              f"{-MjY[4]:.2f} {-MjY[5]:.2f} kNm")
        print(f"gamma: {gamm[0]:.4f} {gamm[1]:.4f} {gamm[2]:.4f} rad")

    # File log (format mirrors Tcl order; note the original mixes X/Y lists)
    if pfile:
        print((
            f"Element {ET} "
            f"MjX:{MjY[0]:.2f} {MjY[1]:.2f} {MjY[2]:.2f} {-MjY[3]:.2f} "
            f"{-MjY[4]:.2f} {-MjY[5]:.2f} "
            f"MjY: {MjX[0]:.2f} {MjX[1]:.2f} {MjX[2]:.2f} {-MjX[3]:.2f} "
            f"{-MjX[4]:.2f} {-MjY[5]:.2f} "
            f"gamma: {gamm[0]:.4f} {gamm[1]:.4f} {gamm[2]:.4f}"
        ), file=pfile)

    # Optional: return some useful values
    return {
        "tags": {"n1": n1, "n6": n6, "ET": ET,
                 "rigM": rigM, "axM": axM, "flX": flX_base, "flY": flY_base,
                 "flX_mm": flXM, "flY_mm": flYM},
        "bj": {"X": bjX, "Y": bjY},
        "Kspr": Kspr,
        "MjX": MjX, "MjY": MjY,
        "gamm": gamm,
    }
