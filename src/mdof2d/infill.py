"""
----------------------------------------------------------------
OpenSees procedures for modelling Clay Masonry Infill Walls
The original method was created in tcl by Gerard J. O'Reilly
The current Python method was adapted from tcl by Volkan Ozsarac
----------------------------------------------------------------
"""

import math
from .units import pi, mm, MPa
import openseespy.opensees as ops


def infill_model(
    eleTag, typ, nds, B, H, hb, hc, bc, tw,
    Ec, Ewh, Ewv, Gw, v, fwv, fwu, fws, sig_v,
    gt_inf=None, pflag=0
):
    """
    Creates a masonry Infill. Adapted from:
    https://github.com/gerardjoreilly/Numerical-Modelling-of-GLD-RC-Frames

    Parameters
    ----------
    eleTag : int
        label of panel
    typ : str
        type of infill model ('single' | 'double' | 'triple' | 'truss')
    nds : list[int]
        list of nodes [list TL TR BR BL]/[list TL TL TR TR BR BR BL BL]
        (i.e always start numbering from top left corner)
    B : float
        Bay width (centrelines) [mm]
    H : float
        Height (centrelines) [mm]
    hb : float
        Beam height [mm]
    hc : float
        Column height [mm]
    bc : float
        Column width [mm]
    tw : float
        Wall thickness [mm]
    Ec : float
        Concrete Elastic Modulus [MPa]
    Ewh : float
        Horizontal secant modulus [MPa]
    Ewv : float
        Vertical Secant Modulus [MPa]
    Gw : float
        Shear Modulus [MPa]
    v : float
        Poissons Ratio
    fwv : float
        Vertical compressive strength [MPa]
    fwu : float
        Sliding shear resistance of mortar joints [MPa]
    fws : float
        Shear resistance under diagonal compression [MPa]
    sig_v : float
        Vertical Compression due to gravity loading [MPa]
    GT_inf : int, optional
        geometric transformation tag for rigid beams
    pflag : int, optional
        put 1 to print info
    """
    # Helper to create Pinching4
    def proc_uniaxial_pinching(
        materialTag, pEnvelopeStress, nEnvelopeStress, pEnvelopeStrain,
        nEnvelopeStrain, rDisp, rForce, uForce, gammaK, gammaD, gammaF, gammaE,
        damage
    ):
        ops.uniaxialMaterial(
            'Pinching4', materialTag,
            pEnvelopeStress[0], pEnvelopeStrain[0],
            pEnvelopeStress[1], pEnvelopeStrain[1],
            pEnvelopeStress[2], pEnvelopeStrain[2],
            pEnvelopeStress[3], pEnvelopeStrain[3],
            nEnvelopeStress[0], nEnvelopeStrain[0],
            nEnvelopeStress[1], nEnvelopeStrain[1],
            nEnvelopeStress[2], nEnvelopeStrain[2],
            nEnvelopeStress[3], nEnvelopeStrain[3],
            rDisp[0], rForce[0], uForce[0],
            rDisp[1], rForce[1], uForce[1],
            gammaK[0], gammaK[1], gammaK[2], gammaK[3], gammaK[4],
            gammaD[0], gammaD[1], gammaD[2], gammaD[3], gammaD[4],
            gammaF[0], gammaF[1], gammaF[2], gammaF[3], gammaF[4],
            gammaE, damage
        )

    # --------------------------------------
    # CALCULATE SOME TERMS
    # --------------------------------------
    Ic = bc * (hc**3) / 12.0  # mm^4
    Bw = B - hc  # mm
    Hw = H - hb  # mm
    theta = math.atan(Hw / Bw)  # rad
    dw = math.sqrt(Bw * Bw + Hw * Hw)  # mm
    Ewtheta = 1.0 / (
        (math.cos(theta) ** 4) / Ewh
        + (math.sin(theta) ** 4) / Ewv
        + (math.cos(theta) ** 2) * (math.sin(theta) ** 2)
        * (1.0 / Gw - 2.0 * v / Ewv)
    )
    lambdaH = H * (
        (Ewtheta * tw * math.sin(2.0 * theta) / (4.0 * Ec * Ic * Hw)) ** 0.25
    )
    z = pi / 2.0 / lambdaH * H  # mm
    s = z / 3.0  # mm

    # --------------------------------------
    # DETERMINE WIDTH OF STRUT
    # --------------------------------------
    if lambdaH < 3.14:
        K1, K2 = 1.300, -0.178
    elif 3.14 < lambdaH < 7.85:
        K1, K2 = 0.707, 0.010
    else:
        K1, K2 = 0.470, 0.040

    bw = dw * (K1 / lambdaH + K2)  # mm
    Aw = (bw * tw * mm * mm)  # mm^2

    # --------------------------------------
    # DETERMINE CRITICAL STRESS IN EACH MODE
    # --------------------------------------
    # Compression in centre
    sigw1 = 1.16 * fwv * math.tan(theta) / (K1 + K2 * lambdaH)
    # Compression at corners
    sigw2 = (
        1.12
        * fwv
        * math.sin(theta)
        * math.cos(theta)
        / (K1 * (lambdaH**-0.12) + K2 * (lambdaH**0.88))
    )
    # Shear sliding
    sigw3 = (
        (fwu * (1.2 * math.sin(theta) + 0.45 * math.cos(theta)) + 0.3 * sig_v)
        * dw / bw
    )
    # Diagonal tension
    sigw4 = (0.6 * fws + 0.3 * sig_v) * dw / bw
    # Governing failure mechanism
    sigw = min(sigw1, sigw2, sigw3, sigw4)

    # --------------------------------------
    # DETERMINE HYSTERETIC RULE
    # --------------------------------------
    sigDS2 = sigw * MPa
    sigDS1 = 0.80 * sigDS2
    sigDS4 = 0.10 * sigDS2

    K1s = 0.8 * Gw * Bw * tw / Hw / 1e3  # (units per original script)
    Ftruss = sigDS1 * Aw
    FDS1 = Ftruss * math.cos(theta)
    delt = FDS1 / K1s if K1s != 0 else 0.0
    thetaDS1_calc = delt / Hw if Hw != 0 else 0.0
    if pflag == 10:
        print(f"Params: K1={K1s:.3f}  Ftruss={Ftruss:.3f} FDS1={FDS1:.3f} "
              f"del={delt:.6f} thetaDS1={thetaDS1_calc:.6f}")

    # Drift limits (Sassun et al. 2015)
    thetaDS1 = 0.0018
    thetaDS2 = 0.0046
    # thetaDS3 = 0.0105
    thetaDS4 = 0.0188

    def eps_from_theta(thetaDS):
        # 1 - sqrt( (1 + ((B/H - thetaDS)^2)) / (1 + (B/H)^2) )
        return 1.0 - (
            (1.0 + (B / H - thetaDS) ** 2) / (1.0 + (B / H) ** 2)) ** 0.5

    epsDS1 = eps_from_theta(thetaDS1)
    epsDS2 = eps_from_theta(thetaDS2)
    # epsDS3 = eps_from_theta(thetaDS3)
    epsDS4 = eps_from_theta(thetaDS4)

    # ----------------------------
    # MATERIAL DEFINITION
    # ----------------------------
    if typ == "truss":
        deltaDS1 = thetaDS1 * H / 2.0
        deltaDS2 = thetaDS2 * H / 2.0
        deltaDS4 = thetaDS4 * H / 2.0

        forceDS1 = sigDS1 * Aw
        forceDS2 = sigDS2 * Aw
        forceDS4 = sigDS4 * Aw

        pF = [forceDS1, forceDS2, forceDS4, forceDS4]
        nF = [-forceDS1, -forceDS2, -forceDS4, -forceDS4]
        pD = [deltaDS1, deltaDS2, deltaDS4, deltaDS4]
        nD = [-deltaDS1, -deltaDS2, -deltaDS4, -deltaDS4]
        rDisp = [0.8, 0.8]
        rForce = [0.1, 0.1]
        uForce = [0.0, 0.0]
        gammaK = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaD = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaF = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaE = 0.0
        dam = "energy"
        proc_uniaxial_pinching(
            int(f"9{eleTag}"), pF, nF, pD, nD, rDisp, rForce,
            uForce, gammaK, gammaD, gammaF, gammaE, dam
        )
        # Example elastic placeholder from Tcl (commented):
        # ops.uniaxialMaterial('Elastic', int(f"800{eleTag}"), 1e10)

    else:
        # stress & strain “envelopes”
        pF = [0.001, 0.002, 0.001, 0.001]
        nF = [-sigDS1, -sigDS2, -sigDS4, -sigDS4]
        pD = [epsDS1, epsDS2, epsDS4, epsDS4]
        nD = [-epsDS1, -epsDS2, -epsDS4, -epsDS4]
        rD = [0.8, 0.8]
        rF = [0.1, 0.1]
        uF = [0.0, 0.0]
        gK = [0.0, 0.0, 0.0, 0.0, 0.0]
        gD = [0.0, 0.0, 0.0, 0.0, 0.0]
        gF = [0.0, 0.0, 0.0, 0.0, 0.0]
        gE = 0.0
        dM = "energy"
        proc_uniaxial_pinching(
            int(f"8{eleTag}"), pF, nF, pD, nD, rD, rF, uF,
            gK, gD, gF, gE, dM
        )
        # # These terms are calibrated by Cavalieri et al. [2005]
        # # and listed in Landi et al. DBA chapter
        # pinchX = 0.8
        # pinchY = 0.1
        # damage1 = 0.0
        # damage2 = 0.0
        # beta0 = 0.5
        # ops.uniaxialMaterial(
        #     'Hysteretic', int(f"8{eleTag}"), pF[0], pD[0], pF[1], pD[1],
        #     pF[2], pD[2], nF[0], nD[0], nF[1], nD[1], nF[2], nD[2],
        #     pinchX, pinchY, damage1, damage2, beta0
        # )

    # --------------------------------------
    # CREATE ELEMENTS
    # --------------------------------------
    if typ == "single":
        nI, nJ, nK, nL = nds[0], nds[1], nds[2], nds[3]
        ops.element('truss', int(f"{eleTag}1"), nI, nK, Aw, int(f"8{eleTag}"),
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}2"), nL, nJ, Aw, int(f"8{eleTag}"),
                    '-doRayleigh', 1)

    if typ == "double":
        nI1, nI2, nJ1, nJ2, nK1, nK2, nL1, nL2 = nds
        # Node redefinitions were commented out in Tcl; kept that way here.

        ops.element('truss', int(f"{eleTag}1"), nI1, nK2, 0.5 * Aw,
                    int(f"8{eleTag}"), '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}2"), nI2, nK1, 0.5 * Aw,
                    int(f"8{eleTag}"), '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}3"), nL1, nJ2, 0.5 * Aw,
                    int(f"8{eleTag}"), '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}4"), nL2, nJ1, 0.5 * Aw,
                    int(f"8{eleTag}"), '-doRayleigh', 1)

        # Remove nodes and redefine positions of actual offsets
        # ops.remove('node', nI1); ops.remove('node', nJ2);
        # ops.remove('node', nK1); ops.remove('node', nL2)
        # x2,y2,z2 = ops.nodeCoord(nI2); ops.node(nI1, x2, y2, z2 - z/3*mm)
        # x1,y1,z1 = ops.nodeCoord(nJ1); ops.node(nJ2, x1, y1, z1 - z/3*mm)
        # x2,y2,z2 = ops.nodeCoord(nK2); ops.node(nK1, x2, y2, z2 + z/3*mm)
        # x1,y1,z1 = ops.nodeCoord(nL1); ops.node(nL2, x1, y1, z1 + z/3*mm)

    if typ == "triple":
        nI1, nI2, nI3, nJ1, nJ2, nJ3, nK1, nK2, nK3, nL1, nL2, nL3 = nds

        # def _repl(tag, x, y, z):
        #     ops.remove("node", tag)
        #     ops.node(tag, x, y, z)
        # b = B - (H - 0.5 * z) / math.tan(theta)
        # x, y, zv = ops.nodeCoord(nI2)
        # _repl(nI1, x, y, zv - z / 2 * mm)
        # _repl(nI3, x + b * mm, y, zv)
        # x, y, zv = ops.nodeCoord(nJ2)
        # _repl(nJ1, x - b * mm, y, zv)
        # _repl(nJ3, x, y, zv - z / 2 * mm)
        # x, y, zv = ops.nodeCoord(nK2)
        # _repl(nK1, x, y, zv + z / 2 * mm)
        # _repl(nK3, x - b * mm, y, zv)
        # x, y, zv = ops.nodeCoord(nL2)
        # _repl(nL1, x + b * mm, y, zv)
        # _repl(nL3, x, y, zv + z / 2 * mm)

        A_quarter = 0.25 * bw * tw * mm * mm
        A_half = 0.50 * bw * tw * mm * mm
        ops.element('truss', int(f"{eleTag}1"), nI1, nK3, A_quarter, eleTag,
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}2"), nI2, nK2, A_half, eleTag,
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}3"), nI3, nK1, A_quarter, eleTag,
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}4"), nL1, nJ3, A_quarter, eleTag,
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}5"), nL2, nJ2, A_half, eleTag,
                    '-doRayleigh', 1)
        ops.element('truss', int(f"{eleTag}6"), nL3, nJ1, A_quarter, eleTag,
                    '-doRayleigh', 1)

    if typ == "truss":
        # Rodrigues approach with Decanini and Sassun modification
        nI, nJ, nK, nL = nds[0], nds[1], nds[2], nds[3]

        rig = [0.5, 0.1, 1e10, 1e10, 0.1]  # Ar, Ir, Er, Gr, Jr
        Ar, Ir, Er, Gr, Jr = rig

        # Create the centre nodes
        cNodeU = int(f"30{eleTag}")
        cNodeL = int(f"40{eleTag}")

        nIX, nIY, nIZ = ops.nodeCoord(nI)

        print("# THIS ASSSUMES INFILL IS IN X DIRECTION ONLY")
        direc = 1
        if direc == 1:
            ops.node(cNodeU, nIX + 0.5 * B, nIY, nIZ - 0.5 * H,
                     '-mass', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            ops.node(cNodeL, nIX + 0.5 * B, nIY, nIZ - 0.5 * H,
                     '-mass', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        elif direc == 2:
            ops.node(cNodeU, nIX, nIY + 0.5 * B, nIZ - 0.5 * H,
                     '-mass', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            ops.node(cNodeL, nIX, nIY + 0.5 * B, nIZ - 0.5 * H,
                     '-mass', 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        # Rigid links (elasticBeamColumn as rigid beams)
        if gt_inf is None:
            raise ValueError(
                "gt_inf (geomTransf tag) must be provided for the rigid links."
            )

        # elasticBeamColumn: tag, iNode, jNode, A, E, G, J, Iy, Iz, transfTag
        ops.element('elasticBeamColumn', int(f"{eleTag}1"), nI, cNodeU, Ar, Er,
                    Gr, Jr, Ir, Ir, gt_inf)
        ops.element('elasticBeamColumn', int(f"{eleTag}2"), nJ, cNodeU, Ar, Er,
                    Gr, Jr, Ir, Ir, gt_inf)
        ops.element('elasticBeamColumn', int(f"{eleTag}3"), nK, cNodeL, Ar, Er,
                    Gr, Jr, Ir, Ir, gt_inf)
        ops.element('elasticBeamColumn', int(f"{eleTag}4"), nL, cNodeL, Ar, Er,
                    Gr, Jr, Ir, Ir, gt_inf)

        # # rigidlinks as truss with huge stiffness
        # ops.uniaxialMaterial('Elastic', int(f"800{eleTag}"), 1e10)
        # ops.element('truss', int(f"{eleTag}1"), nI, cNodeU, Ar,
        #             int(f"800{eleTag}"), '-doRayleigh', 1)
        # ops.element('truss', int(f"{eleTag}2"), nJ, cNodeU, Ar,
        #             int(f"800{eleTag}"), '-doRayleigh', 1)
        # ops.element('truss', int(f"{eleTag}3"), nK, cNodeL, Ar,
        #             int(f"800{eleTag}"), '-doRayleigh', 1)
        # ops.element('truss', int(f"{eleTag}4"), nL, cNodeL, Ar,
        #             int(f"800{eleTag}"), '-doRayleigh', 1)

        # Masonry element: zeroLength with Pinching material in 'direc'
        ops.element('zeroLength', int(f"{eleTag}0"), cNodeU, cNodeL, '-mat',
                    int(f"9{eleTag}"), '-dir', direc)

    # --------------------------------------
    # PRINT SOME OUTPUT
    # --------------------------------------
    if pflag > 0:
        if typ == "double":
            nI1, nI2, nJ1, nJ2, nK1, nK2, nL1, nL2 = nds
            print(f"Created Double-Strut Infill Wall {eleTag} between: "
                  f"{nI1}-{nK2}/{nI2}-{nK1} and {nL1}-{nJ2}/{nL2}-{nJ1}")
        if typ == "triple":
            nI1, nI2, nI3, nJ1, nJ2, nJ3, nK1, nK2, nK3, nL1, nL2, nL3 = nds
            print(f"Created Triple-Strut Infill Wall {eleTag} between: "
                  f"{nI1}-{nK3}/{nI2}-{nK2}/{nI3}-{nK1} and "
                  f"{nL1}-{nJ3}/{nL2}-{nJ2}/{nL3}-{nJ1}")
        if typ == "truss":
            nI, nJ, nK, nL = nds[0], nds[1], nds[2], nds[3]
            print(f"Created Truss Infill Wall {eleTag} between:"
                  f"{nI}-{nK} and {nL}-{nJ}")

    if pflag > 1:
        print(f"bw: {bw:.1f}mm dw: {dw:.1f}mm tw: {tw:.1f}mm z:{z:.1f}mm "
              f"s:{s:.1f}mm theta:{theta:.4f}rad")
        print(f"sigw: {sigw:.2f}MPa Ewtheta:{Ewtheta:.2f}MPa Aw:{Aw:.3f}m2")

    if pflag > 2:
        print(f"sigDS1: {sigDS1:.2f} sigDS2: {sigDS2:.2f} sigDS4: {sigDS4:.2f}"
              " (kPa)")

    if pflag > 3:
        print("Mechanism Parameters:")
        print(f"Compression in centre: {sigw1:.3f} MPa")
        print(f"Compression at corners: {sigw2:.3f} MPa")
        print(f"Shear sliding: {sigw3:.3f} MPa")
        print(f"Diagonal tension: {sigw4:.3f} MPa")
