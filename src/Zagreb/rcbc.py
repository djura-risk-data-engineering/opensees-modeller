"""
----------------------------------------------------------------
OpenSees procedures for modelling RC Beam Columns w/ smooth bars
The original method was created in tcl by Gerard J. O'Reilly
The current Python method was adapted from tcl by Volkan Ozsarac
----------------------------------------------------------------

This script contains two function that create a 3D beam column element with
lumped plasticity. The model has been developed for RC beam-column elements
that were constructed using poor concrete, poor shear reinforcement and smooth
bars before the introduction of seismic provisions in the 1970's in Italy.
The full explanation and calibration of all the parameters required here can
be found in O'Reilly [2016] in addition to any expressions needed to determine
the parameters outlined here.

In summary, the details that need to be submitted to the procedure are basic
parameters such as beam-column dimensions and material properties, along with
details about the reinforcement. Currently, the model accepts the input of
reinforcement content in terms of percentages, where three levels of
reinforcement are considered: Top level, middle level and bottom level. This
applies for both axes of bending, which are termed the local y and local y
axes. This means that the flexural capacity of the section can be specified as
being different in either direction. In addition to the flexural behaviour, an
uncoupled shear hinge has been aggregated into the element. This means that a
shear failure in the element can also be accounted for by introduction of such
an hinge. The parameters used to determine the shear behaviour are adopted
from Zimos et al. [2015] and outlined in O'Reilly [2016] also.

References:
O’Reilly, G. J., Sullivan, T. J. [2019] “Modeling Techniques for the Seismic
Assessment of the Existing Italian RC Frame Structures,” Journal of Earthquak
Engineering, Vol. 23, No.8, pp. 1262-1296 DOI: 10.1080/13632469.2017.1360224.

Zimos, D. K., Mergos, P. E., Kappos, A. J. [2015] “Shear Hysteresis Model
for Reinforced Concrete Elements Including the Post-Peak Range,” COMPDYN
2015 - 5th ECCOMAS Thematic Conference on Computational Methods in
Structural Dynamics and Earthquake Engineering, Crete Island, Greece.

Scott, M. H., Fenves, G. L. [2006] “Plastic Hinge Integration Methods
for Force-Based Beam-Column Elements,” Journal of Structural Engineering,
American Society of Civil Engineers, Vol. 132, No.2, pp. 244-252.
"""

import math
import openseespy.opensees as ops
from .units import MPa, mm


def proc_uniaxial_pinching(
    materialTag, pEnvelopeStress, nEnvelopeStress, pEnvelopeStrain,
    nEnvelopeStrain, rDisp, rForce, uForce, gammaK, gammaD, gammaF, gammaE,
    damage
):
    """Create a Pinching4 material"""
    ops.uniaxialMaterial(
        'Pinching4', materialTag,
        # + Envelope (pos)
        pEnvelopeStress[0], pEnvelopeStrain[0],
        pEnvelopeStress[1], pEnvelopeStrain[1],
        pEnvelopeStress[2], pEnvelopeStrain[2],
        pEnvelopeStress[3], pEnvelopeStrain[3],
        # - Envelope (neg)
        nEnvelopeStress[0], nEnvelopeStrain[0],
        nEnvelopeStress[1], nEnvelopeStrain[1],
        nEnvelopeStress[2], nEnvelopeStrain[2],
        nEnvelopeStress[3], nEnvelopeStrain[3],
        # reloading/unloading
        rDisp[0], rForce[0], uForce[0],
        rDisp[1], rForce[1], uForce[1],
        # degradation
        gammaK[0], gammaK[1], gammaK[2], gammaK[3], gammaK[4],
        gammaD[0], gammaD[1], gammaD[2], gammaD[3], gammaD[4],
        gammaF[0], gammaF[1], gammaF[2], gammaF[3], gammaF[4],
        gammaE, damage
    )


def moment_curvature(index, h, b, cv, dbL, dbV, fc, Ec, P, fyL, Es,
                     rho1, rho2, rho3, pflag=0):
    """
    Returns (Mp, Mn, cp, cn)
    - Iterative neutral axis search at yield curvature, both signs.
    """
    # Concrete/steel strains
    n_c = 0.8 + fc / 18.0                      # n term for concrete
    e_c = (fc / Ec) * (n_c / (n_c - 1.0))      # epsilon_c' for concrete
    e_s = fyL / Es                             # Steel yield strain

    # Yield Curvature (rad/m)
    phiY = 2.1 * fyL / Es / h

    # Depths to steel layers
    d1 = cv + dbV + dbL / 2.0                  # Top layer depth (m)
    d2 = h / 2.0                               # Middle layer depth (m)
    d3 = h - cv - dbV - dbL / 2.0              # Bottom layer depth (m)

    # Helper to run the NA iteration
    def solve(sign='pos'):
        c = h / 2.0
        count = 0
        err = 0.5
        # Iterate to balance axial force
        while err > 0.001 and count < 1000:
            if pflag >= 2:
                print(f"Iteration {count} c:{c:.6f}  Error: {err:.6f} kN")

            # Strains
            e_s1 = (c - d1) * phiY          # top steel
            e_s2 = (d2 - c) * phiY          # middle steel
            e_s3 = (d3 - c) * phiY          # bottom steel
            e_top = c * phiY                # top concrete strain

            # Steel stresses (elastic-perfectly plastic)
            f_s1 = e_s1 * Es if e_s1 < e_s else fyL
            f_s2 = e_s2 * Es if e_s2 < e_s else fyL
            f_s3 = e_s3 * Es if e_s3 < e_s else fyL

            # Steel forces (kN)
            if sign == 'pos':
                Fs1 = f_s1 * rho1 * b * d3 * 1000.0
                Fs3 = f_s3 * rho3 * b * d3 * 1000.0
            elif sign == 'neg':
                Fs1 = f_s1 * rho3 * b * d3 * 1000.0
                Fs3 = f_s3 * rho1 * b * d3 * 1000.0
            Fs2 = f_s2 * rho2 * b * d3 * 1000.0

            # Concrete forces (kN)
            ratio = e_top / e_c
            a1b1 = ratio - (ratio**2) / 3.0  # alpha1beta1 term
            b1 = (4.0 - ratio) / (6.0 - 2.0 * ratio)  # beta1
            Fc = a1b1 * c * fc * b * 1000.0  # Concrete block force (kN)

            # Section axial force equilibrium (tension +, compression)
            Psec = P + Fs2 + Fs3 - Fc - Fs1

            # Update c to drive Psec -> 0
            if Psec < 0:
                c -= 0.001
            elif Psec > 0:
                c += 0.001

            err = abs(Psec)
            if err < 5:
                break
            count += 1

        # Moment about section top
        moment = (
            P * (0.5 * h - c)
            + Fs1 * (c - d1)
            + Fs3 * (d3 - c)
            + Fs2 * (d2 - c)
            + Fc * c * (1.0 - b1 / 2.0)
        )
        return moment, c

    # Positive bending: as given steel ratios
    Mp, cp = solve('pos')

    # Negative bending: swap top/bottom steel ratios
    Mn, cn = solve('neg')

    if pflag >= 1:
        print(f"Myp{index}: {Mp:.6f} kNm")
        print(f"Myn{index}: {Mn:.6f} kNm")

    return Mp, Mn, cp, cn


def rcbc_nonduct(
    ST, ET, GT, iNode, jNode, fyL, fyV, Es, fc, Ec, b, h, s, cv, dbL, dbV, P,
    Ls, rho_shr,
    rho_top1zz, rho_mid1zz, rho_bot1zz,
    rho_top2zz, rho_mid2zz, rho_bot2zz,
    rho_top1yy, rho_mid1yy, rho_bot1yy,
    rho_top2yy, rho_mid2yy, rho_bot2yy,
    pfile, pflag=0
):
    """
    Creates flexural (Pinching4) hinges at both ends in Mz/My,
    optional shear springs at ends, an elastic cracked section for the
    interior, and a forceBeamColumn element with hinge integration.

    ST			Shear Hinge Tag (1 for shear hinge, 0 for none)
    ET			Element Tag
    GT			Geometric Transf Tag
    iNode		i Node
    jNode		j Node
    fyL 		Steel yield strength long. bars (MPa)
    fyV 		Steel yield strength shear. bars (MPa)
    Es 			Steel elastic modulus (MPa)
    fc			Concrete compressive strength (MPa)
    Ec			Concrete elastic modulus (MPa)
    b			Section width (m)
    h			Section height (m)
    s			Shear rft spacing
    cv			Cover (m)
    dbL			Long. bar diameter (m)
    dbV			Shear bar diameter (m)
    P			Axial force (kN) (+ Compression, - Tension)
    Ls			Shear span
    rho_shr		Ratio of shear rft =Ash/bs
    rho_top1zz	Ratio of top rft = Astop/bd (END 1 about zz axis)
    rho_mid1zz	Ratio of web rft =Asmid/bd (END 1 about zz axis)
    rho_bot1zz	Ratio of bottom rft = Asbot/bd (END 1 about zz axis)
    rho_top2zz	Ratio of top rft = Astop/bd (END 2 about zz axis)
    rho_mid2zz	Ratio of web rft =Asmid/bd (END 2 about zz axis)
    rho_bot2zz	Ratio of bottom rft = Asbot/bd (END 2 about zz axis)
    rho_top1yy	Ratio of top rft = Astop/bd (END 1 about yy axis)
    rho_mid1yy	Ratio of web rft =Asmid/bd (END 1 about yy axis)
    rho_bot1yy	Ratio of bottom rft = Asbot/bd (END 1 about yy axis)
    rho_top2yy	Ratio of top rft = Astop/bd (END 2 about yy axis)
    rho_mid2yy	Ratio of web rft =Asmid/bd (END 2 about yy axis)
    rho_bot2yy	Ratio of bottom rft = Asbot/bd (END 2 about yy axis)
    pflag		Print flag (optional - 1: details about hinge are printed)
    pfile		Print file -  prints the backbone properties to a specified file
    """

    # --------------------------------------
    # General section & material numbers
    # --------------------------------------

    # Normalized axial load ratio (dimensionless)
    nu = P / (b * h * fc * MPa)

    # Depths to steel layers for both axes (m)
    # bottom layer depth for bending about zz (i.e., My about local y)
    dyy = h - dbV - cv - dbL / 2.0
    # bottom layer depth for bending about yy (i.e., Mz about local z)
    dzz = b - dbV - cv - dbL / 2.0
    # top layer depth used in shear formulas
    d1 = dbV - cv - dbL / 2.0

    # Gross props
    Ag = b * h
    Izz = b * (h ** 3) / 12.0
    Iyy = h * (b ** 3) / 12.0

    EIzz = Ec * MPa * Izz    # kN.m2
    EIyy = Ec * MPa * Iyy    # kN.m2
    EA = Ec * MPa * Ag     # kN

    # Shear modulus (elastic part for interior)
    Gc = 0.4 * Ec * MPa
    # Kshear = Gc * Ag

    # Concrete/steel strain params (kept for completeness)
    # n_c = 0.8 + fc / 18.0
    # e_c = (fc / Ec) * (n_c / (n_c - 1.0))
    # e_s = fyL / Es

    # Torsion (thin-rectangle approximation)
    if h >= b:
        J = h * (b ** 3) * (0.333 - 0.21 * (h / b) * (1 - (b / h) ** 4) / 12.0)
    else:
        J = b * (h ** 3) * (0.333 - 0.21 * (b / h) * (1 - (h / b) ** 4) / 12.0)

    # --------------------------------------
    # Member length from current node coords
    # --------------------------------------
    x1, y1, z1 = ops.nodeCoord(iNode)
    x2, y2, z2 = ops.nodeCoord(jNode)
    L = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

    # --------------------------------------
    # Yield curvatures
    # --------------------------------------
    phiYzz = 2.1 * fyL / Es / h  # bend about zz (Mz)
    phiYyy = 2.1 * fyL / Es / b  # bend about yy (My)

    # --------------------------------------
    # Yield moments via your helper (four ends/axes)
    # --------------------------------------
    # zz axis (Mz): section dims (h,b)
    Myp1zz, Myn1zz, cp1zz, cn1zz = moment_curvature(
        '1zz', h, b, cv, dbL, dbV, fc, Ec, P, fyL, Es,
        rho_top1zz, rho_mid1zz, rho_bot1zz, pflag=0
    )
    Myp2zz, Myn2zz, cp2zz, cn2zz = moment_curvature(
        '2zz', h, b, cv, dbL, dbV, fc, Ec, P, fyL, Es,
        rho_top2zz, rho_mid2zz, rho_bot2zz, pflag=0
    )

    # yy axis (My): swap dims (b,h)
    Myp1yy, Myn1yy, cp1yy, cn1yy = moment_curvature(
        '1yy', b, h, cv, dbL, dbV, fc, Ec, P, fyL, Es,
        rho_top1yy, rho_mid1yy, rho_bot1yy, pflag=0
    )
    Myp2yy, Myn2yy, cp2yy, cn2yy = moment_curvature(
        '2yy', b, h, cv, dbL, dbV, fc, Ec, P, fyL, Es,
        rho_top2yy, rho_mid2yy, rho_bot2yy, pflag=0
    )

    # Initial cracked stiffnesses & cracked EI
    Kizz = Myp1zz / phiYzz
    Kiyy = Myp1yy / phiYyy
    EIrzz = Kizz / EIzz
    EIryy = Kiyy / EIyy
    EIzze = EIrzz * EIzz
    EIyye = EIryy * EIyy
    Izze = EIrzz * Izz
    Iyye = EIryy * Iyy

    # --------------------------------------
    # Capping moments
    # --------------------------------------
    Mcp1zz = 1.077 * Myp1zz
    Mcn1zz = 1.077 * Myn1zz
    Mcp2zz = 1.077 * Myp2zz
    Mcn2zz = 1.077 * Myn2zz
    Mcp1yy = 1.077 * Myp1yy
    Mcn1yy = 1.077 * Myn1yy
    Mcp2yy = 1.077 * Myp2yy
    Mcn2yy = 1.077 * Myn2yy

    # --------------------------------------
    # Ultimate moments
    # --------------------------------------
    Mup1zz = 0.8 * Mcp1zz
    Mun1zz = 0.8 * Mcn1zz
    Mup2zz = 0.8 * Mcp2zz
    Mun2zz = 0.8 * Mcn2zz
    Mup1yy = 0.8 * Mcp1yy
    Mun1yy = 0.8 * Mcn1yy
    Mup2yy = 0.8 * Mcp2yy
    Mun2yy = 0.8 * Mcn2yy

    # --------------------------------------
    # Plastic hinge length
    # --------------------------------------
    Lp = 0.08 * Ls + 0.022 * fyL * dbL

    # --------------------------------------
    # Ultimate curvatures
    # --------------------------------------
    mu_phi = 22.651 - 47.348 * nu
    if nu < 0.1:
        mu_phi = 22.651 - 47.348 * 0.1
    if nu > 0.25:
        mu_phi = 22.651 - 47.348 * 0.25
    if nu > 0.999 and pflag:
        print(
            f"WARNING: Element {ET} has an axial load ratio greater than 1.0!"
        )
    phiUzz = phiYzz * mu_phi
    phiUyy = phiYyy * mu_phi

    # --------------------------------------
    # Capping curvatures
    # --------------------------------------
    app = -0.1437 * nu - 0.0034
    if nu < 0.1:
        app = -0.1437 * 0.1 - 0.0034
    phiCzz = phiUzz + (0.2 * 1.077 * phiYzz) / app
    phiCyy = phiUyy + (0.2 * 1.077 * phiYyy) / app

    # --------------------------------------
    # Exhaustion (fracture) curvature limits
    # --------------------------------------
    # This is computed based on an ultimate strain of the rebar.
    # This is conservatively taken to be 0.08, based on p141 of
    # Priestley et al. [2007], and the corresponding curvature computed.

    # Only the reinforcement fracture is checked here as this is anticipated
    phi0zz = 0.08 / max(1e-12, (dzz - cp1zz))
    phi0yy = 0.08 / max(1e-12, (dyy - cp1yy))

    # --------------------------------------
    # Max capacity (residual) and corresponding curvatures
    # --------------------------------------
    # Take the residual as 10% of the capping moment (OpenSees doesnt like 0)
    Mmp1zz = 0.1 * Mcp1zz
    Mmp2zz = 0.1 * Mcp2zz
    Mmp1yy = 0.1 * Mcp1yy
    Mmp2yy = 0.1 * Mcp2yy
    Mmn1zz = 0.1 * Mcn1zz
    Mmn2zz = 0.1 * Mcn2zz
    Mmn1yy = 0.1 * Mcn1yy
    Mmn2yy = 0.1 * Mcn2yy

    phiMp1zz = phiCzz + (Mmp1zz - Mcp1zz) * phiYzz / (app * Myp1zz)
    phiMp2zz = phiCzz + (Mmp2zz - Mcp2zz) * phiYzz / (app * Myp2zz)
    phiMp1yy = phiCyy + (Mmp1yy - Mcp1yy) * phiYyy / (app * Myp1yy)
    phiMp2yy = phiCyy + (Mmp2yy - Mcp2yy) * phiYyy / (app * Myp2yy)

    phiMn1zz = phiCzz + (Mmn1zz - Mcn1zz) * phiYzz / (app * Myn1zz)
    phiMn2zz = phiCzz + (Mmn2zz - Mcn2zz) * phiYzz / (app * Myn2zz)
    phiMn1yy = phiCyy + (Mmn1yy - Mcn1yy) * phiYyy / (app * Myn1yy)
    phiMn2yy = phiCyy + (Mmn2yy - Mcn2yy) * phiYyy / (app * Myn2yy)

    # --------------------------------------
    # Shear backbone (optional ST>0)
    # --------------------------------------
    if ST > 0:
        # This is as per Zimos et al. [2015]
        # Elastic shear
        Gc = 0.42 * Ec  # Shear Modulus of Concrete (in MPa)
        GA0 = 0.8 * b * h * Gc * MPa  # (in kN)
        # Tensile Strength fo concrete from Collins and Mitchell (in kN/m2)
        ft = (math.sqrt(fc) / 3.0) * MPa

        # Cracking Shear as per Sezen & Moehle [2004] (in kN)
        V_cryy = ft * h / Ls * math.sqrt(1 + P / (ft * b * h)) * 0.8 * b * h
        V_crzz = ft * b / Ls * math.sqrt(1 + P / (ft * h * b)) * 0.8 * h * b
        gamm_cryy = V_cryy / GA0
        gamm_crzz = V_crzz / GA0

        # Cracked shear response terms
        # Shear Capacity from Priestley et al [1993] in kN
        # Assumption: k=0.29, theta=45deg
        V_cyy = (0.29 * math.sqrt(fc) * 0.8 * b * h * 1e3
                 + P * math.tan(h / (2.0 * Ls))
                 + rho_shr * b * fyV * MPa * (dyy - d1))
        V_czz = (0.29 * math.sqrt(fc) * 0.8 * h * b * 1e3
                 + P * math.tan(b / (2.0 * Ls))
                 + rho_shr * h * fyV * MPa * (dzz - d1))
        # Cracked Stiffness from Mergos and Kappos in kN/m
        # Assumption: theta=45deg
        GA1yy = (Es * MPa * b * (dyy - d1) * rho_shr) / (
            1 + 4 * Es / Ec * rho_shr)
        GA1zz = (Es * MPa * h * (dzz - d1) * rho_shr) / (
            1 + 4 * Es / Ec * rho_shr)
        # Cracking strain with correction factors from Mergos and Kappos
        paramV1yy = min(Ls / h, 2.5)
        paramV1zz = min(Ls / b, 2.5)
        gamm_pkyy = ((gamm_cryy + (V_cyy - V_cryy) / GA1yy) * (1 - 1.07 * nu)
                     * (5.37 - 1.59 * paramV1yy))
        gamm_pkzz = ((gamm_crzz + (V_czz - V_crzz) / GA1zz) * (1 - 1.07 * nu)
                     * (5.37 - 1.59 * paramV1zz))
        V_ccyy = 0.9 * V_cyy  # Opensees gets knarky with 0 stiffness
        V_cczz = 0.9 * V_czz  # Opensees gets knarky with 0 stiffness

        # Failure terms
        paramV2 = min(nu, 0.4)
        omega_k = rho_shr * fyV / fc
        paramV3 = min(omega_k, 0.08)
        gamm_u1yy = ((1 - 2.5 * paramV2) * (paramV1yy ** 2)
                     * (0.31 + 17.8 * paramV3) * gamm_pkyy)
        gamm_u1zz = ((1 - 2.5 * paramV2) * (paramV1zz ** 2)
                     * (0.31 + 17.8 * paramV3) * gamm_pkzz)
        if gamm_u1yy <= gamm_pkyy:
            gamm_uyy = gamm_pkyy
            V_ccyy = V_cyy
        else:
            gamm_uyy = gamm_u1yy

        if gamm_u1zz <= gamm_pkzz:
            gamm_uzz = gamm_pkzz
            V_cczz = V_czz
        else:
            gamm_uzz = gamm_u1zz

        # Descending branch
        nu_lyy = (P * 1e3 / (rho_top1zz + rho_bot1zz) / fyL
                  / (b / mm) / (dyy / mm))
        nu_lzz = (P * 1e3 / (rho_top1yy + rho_bot1yy) / fyL
                  / (h / mm) / (dzz / mm))
        tau_aveyy = V_cyy / b / dyy / 1e3
        tau_avezz = V_czz / h / dzz / 1e3

        A_confpcyy = (dyy - d1) * (b - 2 * (cv + dbV + dbL)) / b / h
        A_confpczz = (dzz - d1) * (h - 2 * (cv + dbV + dbL)) / h / b

        gamm_tppyy = (
            0.65 * (((rho_top1zz + rho_bot1zz) / A_confpcyy) ** 1.2)
            * math.sqrt(rho_shr * fyV / nu_lyy / (s / dyy)
                        / (tau_aveyy / math.sqrt(fc))))
        gamm_tppzz = (0.65 * (((rho_top1yy + rho_bot1yy) / A_confpczz) ** 1.2)
                      * math.sqrt(rho_shr * fyV / nu_lzz / (s / dzz)
                                  / (tau_avezz / math.sqrt(fc))))

        Sppyy = (7.36 + 0.28 * math.sqrt(nu + 0.02) / (rho_shr + 0.0011)
                 / (((rho_top1zz + rho_bot1zz) * fyL * dbL / A_confpcyy / dyy)
                    + 0.06))
        Sppzz = (7.36 + 0.28 * math.sqrt(nu + 0.02) / (rho_shr + 0.0011)
                 / (((rho_top1yy + rho_bot1yy) * fyL * dbL / A_confpczz / dzz)
                    + 0.06))

        gamm_myy = gamm_uyy + gamm_tppyy
        gamm_mzz = gamm_uzz + gamm_tppzz

        V_resyy = V_cyy * (1 - Sppyy * gamm_tppyy)
        V_reszz = V_czz * (1 - Sppzz * gamm_tppzz)

        if V_resyy <= 0:
            V_resyy = 0.1 * V_cyy
            gamm_tppyy = 1.0 / Sppyy
            gamm_myy = gamm_uyy + gamm_tppyy

        if V_reszz <= 0:
            V_reszz = 0.1 * V_czz
            gamm_tppzz = 1.0 / Sppzz
            gamm_mzz = gamm_uzz + gamm_tppzz

    # --------------------------------------
    # Console/file outputs (mirroring Tcl)
    # --------------------------------------
    if pflag == 1:
        print(f"Element {ET} between nodes {iNode} and {jNode}")
        print(f"Myp1zz: {Myp1zz:.1f} kNm Myp2zz: {Myp2zz:.1f} kNm "
              f"Myp1yy: {Myp1yy:.1f} kNm Myp2yy: {Myp2yy:.1f} kNm")
        print(f"Myn1zz: {Myn1zz:.1f} kNm Myn2zz: {Myn2zz:.1f} kNm "
              f"Myn1yy: {Myn1yy:.1f} kNm Myn2yy: {Myn2yy:.1f} kNm")
        print(f"Mcp1zz: {Mcp1zz:.1f} kNm Mcp2zz: {Mcp2zz:.1f} kNm "
              f"Mcp1yy: {Mcp1yy:.1f} kNm Mcp2yy: {Mcp2yy:.1f} kNm")
        print(f"Mcn1zz: {Mcn1zz:.1f} kNm Mcn2zz: {Mcn2zz:.1f} kNm "
              f"Mcn1yy: {Mcn1yy:.1f} kNm Mcn2yy: {Mcn2yy:.1f} kNm")
        print(f"Mup1zz: {Mup1zz:.1f} kNm Mup2zz: {Mup2zz:.1f} kNm "
              f"Mup1yy: {Mup1yy:.1f} kNm Mup2yy: {Mup2yy:.1f} kNm")
        print(f"Mun1zz: {Mun1zz:.1f} kNm Mun2zz: {Mun2zz:.1f} kNm "
              f"Mun1yy: {Mun1yy:.1f} kNm Mun2yy: {Mun2yy:.1f} kNm")
        print(f"Mup1zz: {Mmp1zz:.1f} kNm Mup2zz: {Mmp2zz:.1f} kNm "
              f"Mup1yy: {Mmp1yy:.1f} kNm Mup2yy: {Mmp2yy:.1f} kNm")
        print(f"Mun1zz: {Mmn1zz:.1f} kNm Mun2zz: {Mmn2zz:.1f} kNm "
              f"Mun1yy: {Mmn1yy:.1f} kNm Mun2yy: {Mmn2yy:.1f} kNm")
        print(f"phiYzz: {phiYzz:.4f} rad/m phiYyy: {phiYyy:.4f} rad/m")
        print(f"phiCzz: {phiCzz:.4f} rad/m phiCyy: {phiCyy:.4f} rad/m")
        print(f"phiUzz: {phiUzz:.4f} rad/m phiUyy: {phiUyy:.4f} rad/m")
        print(f"phi0zz: {phi0zz:.4f} rad/m phi0yy: {phi0yy:.4f} rad/m")
        print(f"phiMp1zz: {phiMp1zz:.4f} rad/m phiMp2zz: {phiMp2zz:.4f} rad/m "
              f"phiMp1yy: {phiMp1yy:.4f} rad/m phiMp2yy: {phiMp2yy:.4f} rad/m")
        print(f"phiMn1zz: {phiMn1zz:.4f} rad/m phiMn2zz: {phiMn2zz:.4f} rad/m "
              f"phiM1nyy: {phiMn1yy:.4f} rad/m phiMn2yy: {phiMn2yy:.4f} rad/m")
        print(f"phi0zz: {phi0zz:.4f} 1/m   phi0yy: {phi0yy:.4f} 1/m")
        print(f"Lp: {Lp:.3f}m   nu: {nu:.3f}   a_pp: {app:.3f}   L:{L:.3f}m")
        print(f"b: {b:.3f}m   h: {h:.3f}m")
        print(f"Izz: {Izz:.6f}m4   Iyy: {Iyy:.6f}m4")
        print(f"EA: {EA:.1f}kN   EIcr,zz/EIg {EIrzz:.3f}   "
              f"EIcr,yy/EIg {EIryy:.3f}")
        print(f"EIyy: {EIyy:.1f}kNm2   EIzz: {EIzz:.1f}kNm2")
        print(f"EIcryy: {EIyye:.1f}kNm2   EIcrzz: {EIzze:.1f}kNm2")
        if ST > 1:
            print(f"V_cryy:{V_cryy:.1f}kN V_ccyy:{V_ccyy:.1f}kN "
                  f"V_cyy:{V_cyy:.1f}kN V_resyy:{V_resyy:.1f}kN "
                  f"V_crzz:{V_crzz:.1f}kN V_cczz:{V_cczz:.1f}kN "
                  f"V_czz:{V_czz:.1f}kN V_reszz:{V_reszz:.1f}kN")
            print(f"gamm_cryy:{gamm_cryy:.4f} gamm_pkyy:{gamm_pkyy:.4f} "
                  f"gamm_uyy:{gamm_uyy:.4f} gamm_myy:{gamm_myy:.4f} "
                  f"gamm_crzz:{gamm_crzz:.4f} gamm_pkzz:{gamm_pkzz:.4f} "
                  f"gamm_uzz:{gamm_uzz:.4f} gamm_mzz:{gamm_mzz:.4f}")

    # File print (compact)
    if ST > 1 and pfile:
        print((
            f"Element {ET} between nodes {iNode} and {jNode} "
            f"Myp1zz: {Myp1zz:.1f} kNm Myp2zz: {Myp2zz:.1f} kNm "
            f"Myp1yy: {Myp1yy:.1f} kNm Myp2yy: {Myp2yy:.1f} kNm "
            f"Myn1zz: {Myn1zz:.1f} kNm Myn2zz: {Myn2zz:.1f} kNm "
            f"Myn1yy: {Myn1yy:.1f} kNm Myn2yy: {Myn2yy:.1f} kNm "
            f"Mcp1zz: {Mcp1zz:.1f} kNm Mcp2zz: {Mcp2zz:.1f} kNm "
            f"Mcp1yy: {Mcp1yy:.1f} kNm Mcp2yy: {Mcp2yy:.1f} kNm "
            f"Mcn1zz: {Mcn1zz:.1f} kNm Mcn2zz: {Mcn2zz:.1f} kNm "
            f"Mcn1yy: {Mcn1yy:.1f} kNm Mcn2yy: {Mcn2yy:.1f} kNm "
            f"Mup1zz: {Mup1zz:.1f} kNm Mup2zz: {Mup2zz:.1f} kNm "
            f"Mup1yy: {Mup1yy:.1f} kNm Mup2yy: {Mup2yy:.1f} kNm "
            f"Mun1zz: {Mun1zz:.1f} kNm Mun2zz: {Mun2zz:.1f} kNm "
            f"Mun1yy: {Mun1yy:.1f} kNm Mun2yy: {Mun2yy:.1f} kNm "
            f"Mup1zz: {Mmp1zz:.1f} kNm Mup2zz: {Mmp2zz:.1f} kNm "
            f"Mup1yy: {Mmp1yy:.1f} kNm Mup2yy: {Mmp2yy:.1f} kNm "
            f"Mun1zz: {Mmn1zz:.1f} kNm Mun2zz: {Mmn2zz:.1f} kNm "
            f"Mun1yy: {Mmn1yy:.1f} kNm Mun2yy: {Mmn2yy:.1f} kNm "
            f"phiYzz: {phiYzz:.4f} 1/m phiYyy: {phiYyy:.4f} 1/m "
            f"phiCzz: {phiCzz:.4f} 1/m phiCyy: {phiCyy:.4f} 1/m "
            f"phiUzz: {phiUzz:.4f} 1/m phiUyy: {phiUyy:.4f} 1/m "
            f"phiMp1zz: {phiMp1zz:.4f} 1/m phiMp2zz: {phiMp2zz:.4f} 1/m "
            f"phiMp1yy: {phiMp1yy:.4f} 1/m phiMp2yy: {phiMp2yy:.4f} 1/m "
            f"phiMn1zz: {phiMn1zz:.4f} 1/m phiMn2zz: {phiMn2zz:.4f} 1/m "
            f"phiM1nyy: {phiMn1yy:.4f} 1/m phiMn2yy: {phiMn2yy:.4f} 1/m "
            f"V_cryy:{V_cryy:.1f}kN V_ccyy:{V_ccyy:.1f}kN V_cyy:{V_cyy:.1f}kN "
            f"V_resyy:{V_resyy:.1f}kN "
            f"V_crzz:{V_crzz:.1f}kN V_cczz:{V_cczz:.1f}kN V_czz:{V_czz:.1f}kN "
            f"V_reszz:{V_reszz:.1f}kN "
            f"gamm_cryy:{gamm_cryy:.10f} gamm_pkyy:{gamm_pkyy:.10f} "
            f"gamm_uyy:{gamm_uyy:.10f} gamm_myy:{gamm_myy:.10f} "
            f"gamm_crzz:{gamm_crzz:.10f} gamm_pkzz:{gamm_pkzz:.10f} "
            f"gamm_uzz:{gamm_uzz:.10f} gamm_mzz:{gamm_mzz:.10f} "
            f"nu:{nu:.3f} EIcr,zz/EIg {EIrzz:.3f}   EIcr,yy/EIg {EIryy:.3f}"
        ), file=pfile)
    elif pfile:
        print((
            f"Element {ET} between nodes {iNode} and {jNode} "
            f"Myp1zz: {Myp1zz:.1f} kNm Myp2zz: {Myp2zz:.1f} kNm "
            f"Myp1yy: {Myp1yy:.1f} kNm Myp2yy: {Myp2yy:.1f} kNm "
            f"Myn1zz: {Myn1zz:.1f} kNm Myn2zz: {Myn2zz:.1f} kNm "
            f"Myn1yy: {Myn1yy:.1f} kNm Myn2yy: {Myn2yy:.1f} kNm "
            f"Mcp1zz: {Mcp1zz:.1f} kNm Mcp2zz: {Mcp2zz:.1f} kNm "
            f"Mcp1yy: {Mcp1yy:.1f} kNm Mcp2yy: {Mcp2yy:.1f} kNm "
            f"Mcn1zz: {Mcn1zz:.1f} kNm Mcn2zz: {Mcn2zz:.1f} kNm "
            f"Mcn1yy: {Mcn1yy:.1f} kNm Mcn2yy: {Mcn2yy:.1f} kNm "
            f"Mup1zz: {Mup1zz:.1f} kNm Mup2zz: {Mup2zz:.1f} kNm "
            f"Mup1yy: {Mup1yy:.1f} kNm Mup2yy: {Mup2yy:.1f} kNm "
            f"Mun1zz: {Mun1zz:.1f} kNm Mun2zz: {Mun2zz:.1f} kNm "
            f"Mun1yy: {Mun1yy:.1f} kNm Mun2yy: {Mun2yy:.1f} kNm "
            f"Mup1zz: {Mmp1zz:.1f} kNm Mup2zz: {Mmp2zz:.1f} kNm "
            f"Mup1yy: {Mmp1yy:.1f} kNm Mup2yy: {Mmp2yy:.1f} kNm "
            f"Mun1zz: {Mmn1zz:.1f} kNm Mun2zz: {Mmn2zz:.1f} kNm "
            f"Mun1yy: {Mmn1yy:.1f} kNm Mun2yy: {Mmn2yy:.1f} kNm "
            f"phiYzz: {phiYzz:.4f} 1/m phiYyy: {phiYyy:.4f} 1/m "
            f"phiCzz: {phiCzz:.4f} 1/m phiCyy: {phiCyy:.4f} 1/m "
            f"phiUzz: {phiUzz:.4f} 1/m phiUyy: {phiUyy:.4f} 1/m "
            f"phiMp1zz: {phiMp1zz:.4f} 1/m phiMp2zz: {phiMp2zz:.4f} 1/m "
            f"phiMp1yy: {phiMp1yy:.4f} 1/m phiMp2yy: {phiMp2yy:.4f} 1/m "
            f"phiMn1zz: {phiMn1zz:.4f} 1/m "
            f"phiMn2zz: {phiMn2zz:.4f} 1/m phiM1nyy: {phiMn1yy:.4f} 1/m "
            f"phiMn2yy: {phiMn2yy:.4f} 1/m  "
            f"nu:{nu:.3f} EIcr,zz/EIg {EIrzz:.3f}   EIcr,yy/EIg {EIryy:.3f}"
        ), file=pfile)

    # -----------------------------------------------
    # Flexural material models (Pinching4 + MinMax)
    # -----------------------------------------------
    # Moment envelopes (+/-) for both axes/ends
    pMom1zz = [Myp1zz, Mcp1zz, Mup1zz, Mmp1zz]
    pMom2zz = [Myp2zz, Mcp2zz, Mup2zz, Mmp2zz]
    nMom1zz = [-Myn1zz, -Mcn1zz, -Mun1zz, -Mmn1zz]
    nMom2zz = [-Myn2zz, -Mcn2zz, -Mun2zz, -Mmn2zz]
    pMom1yy = [Myp1yy, Mcp1yy, Mup1yy, Mmp1yy]
    pMom2yy = [Myp2yy, Mcp2yy, Mup2yy, Mmp2yy]
    nMom1yy = [-Myn1yy, -Mcn1yy, -Mun1yy, -Mmn1yy]
    nMom2yy = [-Myn2yy, -Mcn2yy, -Mun2yy, -Mmn2yy]

    # Curvature envelopes (+/-)
    pCurv1zz = [phiYzz, phiCzz, phiUzz, phiMp1zz]
    pCurv2zz = [phiYzz, phiCzz, phiUzz, phiMp2zz]
    nCurv1zz = [-phiYzz, -phiCzz, -phiUzz, -phiMn1zz]
    nCurv2zz = [-phiYzz, -phiCzz, -phiUzz, -phiMn2zz]
    pCurv1yy = [phiYyy, phiCyy, phiUyy, phiMp1yy]
    pCurv2yy = [phiYyy, phiCyy, phiUyy, phiMp2yy]
    nCurv1yy = [-phiYyy, -phiCyy, -phiUyy, -phiMn1yy]
    nCurv2yy = [-phiYyy, -phiCyy, -phiUyy, -phiMn2yy]

    # Pinching reloading/unloading params
    rDispM = [0.1, 0.1]
    rForceM = [0.3, 0.3]
    uForceM = [-0.8, -0.8]
    gammaKM = [0.0, 0.0, 0.0, 0.0, 0.0]
    gammaDM = [0.0, 0.0, 0.0, 0.0, 0.0]
    gammaFM = [0.0, 0.0, 0.0, 0.0, 0.0]
    gammaEM = 0.0
    damM = "energy"

    # Material tags
    ohingeMTag1zz = int(f"101{ET}")
    ohingeMTag2zz = int(f"102{ET}")
    ohingeMTag1yy = int(f"103{ET}")
    ohingeMTag2yy = int(f"104{ET}")

    # Create Pinching4 flexural materials
    proc_uniaxial_pinching(
        ohingeMTag1zz, pMom1zz, nMom1zz, pCurv1zz, nCurv1zz,
        rDispM, rForceM, uForceM, gammaKM, gammaDM, gammaFM, gammaEM, damM)
    proc_uniaxial_pinching(
        ohingeMTag2zz, pMom2zz, nMom2zz, pCurv2zz, nCurv2zz,
        rDispM, rForceM, uForceM, gammaKM, gammaDM, gammaFM, gammaEM, damM)
    proc_uniaxial_pinching(
        ohingeMTag1yy, pMom1yy, nMom1yy, pCurv1yy, nCurv1yy,
        rDispM, rForceM, uForceM, gammaKM, gammaDM, gammaFM, gammaEM, damM)
    proc_uniaxial_pinching(
        ohingeMTag2yy, pMom2yy, nMom2yy, pCurv2yy, nCurv2yy,
        rDispM, rForceM, uForceM, gammaKM, gammaDM, gammaFM, gammaEM, damM)

    # Wrap with MinMax curvature limits
    hingeMTag1zz = int(f"105{ET}")
    hingeMTag2zz = int(f"106{ET}")
    hingeMTag1yy = int(f"107{ET}")
    hingeMTag2yy = int(f"108{ET}")

    ops.uniaxialMaterial('MinMax', hingeMTag1zz, ohingeMTag1zz,
                         '-min', -phi0zz, '-max', phi0zz)
    ops.uniaxialMaterial('MinMax', hingeMTag2zz, ohingeMTag2zz,
                         '-min', -phi0zz, '-max', phi0zz)
    ops.uniaxialMaterial('MinMax', hingeMTag1yy, ohingeMTag1yy,
                         '-min', -phi0yy, '-max', phi0yy)
    ops.uniaxialMaterial('MinMax', hingeMTag2yy, ohingeMTag2yy,
                         '-min', -phi0yy, '-max', phi0yy)

    # -----------------------------------------------
    # Shear material model (optional)
    # -----------------------------------------------
    if ST > 0:
        # Positive/Negative envelope Moment
        pV1yy = [V_cryy, V_ccyy, V_cyy, V_resyy]
        pV1zz = [V_crzz, V_cczz, V_czz, V_reszz]
        nV1yy = [-V_cryy, -V_ccyy, -V_cyy, -V_resyy]
        nV1zz = [-V_crzz, -V_cczz, -V_czz, -V_reszz]
        # Positive/Negative envelope Curvature
        pShr1yy = [gamm_cryy, gamm_pkyy, gamm_uyy, gamm_myy]
        pShr1zz = [gamm_crzz, gamm_pkzz, gamm_uzz, gamm_mzz]
        nShr1yy = [-gamm_cryy, -gamm_pkyy, -gamm_uyy, -gamm_myy]
        nShr1zz = [-gamm_crzz, -gamm_pkzz, -gamm_uzz, -gamm_mzz]
        rDispV = [0.4, 0.4]
        rForceV = [0.2, 0.2]
        uForceV = [0.0, 0.0]
        gammaKV = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaDV = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaFV = [0.0, 0.0, 0.0, 0.0, 0.0]
        gammaEV = 0.0
        damV = "energy"
        # add the material to domain through the use of a procedure
        ohingeShTagyy = int(f"109{ET}")
        ohingeShTagzz = int(f"110{ET}")
        proc_uniaxial_pinching(
            ohingeShTagyy, pV1yy, nV1yy, pShr1yy, nShr1yy, rDispV, rForceV,
            uForceV, gammaKV, gammaDV, gammaFV, gammaEV, damV)
        proc_uniaxial_pinching(
            ohingeShTagzz, pV1zz, nV1zz, pShr1zz, nShr1zz, rDispV, rForceV,
            uForceV, gammaKV, gammaDV, gammaFV, gammaEV, damV)

        # Cut off at axial-failure shear strains
        hingeShTagyy = int(f"111{ET}")
        hingeShTagzz = int(f"112{ET}")
        ops.uniaxialMaterial('MinMax', hingeShTagyy, ohingeShTagyy,
                             '-min', -gamm_myy, '-max', gamm_myy)
        ops.uniaxialMaterial('MinMax', hingeShTagzz, ohingeShTagzz,
                             '-min', -gamm_mzz, '-max', gamm_mzz)

    # --------------------------------------
    # Sections and element creation
    # --------------------------------------
    ETag = int(f"112{ET}")  # Internal elastic section tag
    fTag1zz = int(f"113{ET}")  # Section tag Mz 1
    fTag2zz = int(f"114{ET}")  # Section tag Mz 2
    # fTag1yy = int(f"115{ET}")  # Section tag My 1
    # fTag2yy = int(f"116{ET}")  # Section tag My 2
    phTag1 = int(f"117{ET}")  # Create an aggregated section tag
    phTag2 = int(f"118{ET}")  # Create an aggregated section tag
    intTag = int(f"119{ET}")  # beam integration tag

    # Elastic interior with cracked properties
    ops.section('Elastic', ETag, Ec * MPa, Ag, Izze, Iyye, Gc, J)

    # Plastic hinge sections (uniaxial)
    ops.section('Uniaxial', fTag1zz, hingeMTag1zz, 'Mz')
    ops.section('Uniaxial', fTag2zz, hingeMTag2zz, 'Mz')

    # Aggregate My to Mz
    ops.section('Aggregator', phTag1, hingeMTag1yy, 'My', '-section', fTag1zz)
    ops.section('Aggregator', phTag2, hingeMTag2yy, 'My', '-section', fTag2zz)

    # Integration scheme (Scott & Fenves [2006] JStructE Paper)
    ops.beamIntegration('HingeRadau', intTag, phTag1, Lp, phTag2, Lp, ETag)

    if ST < 1:
        # No shear springs
        ops.element('forceBeamColumn', ET, iNode, jNode, GT, intTag,
                    '-iter', 100, 1e-12)

    elif ST == 1:
        # Shear springs at both ends via zeroLength elements + rigid links
        iX, iY, iZ = ops.nodeCoord(iNode)
        jX, jY, jZ = ops.nodeCoord(jNode)

        # Create two dummy nodes in their place
        iDummy = int(f"11{iNode}")
        jDummy = int(f"12{jNode}")
        ops.node(iDummy, iX, iY, iZ)
        ops.node(jDummy, jX, jY, jZ)

        # Create the rigid material
        rigM = int(f"100{ET}")
        ops.uniaxialMaterial('Elastic', rigM, 1e10)

        # zeroLength shear hinges (materials mapped to dof 1..6)
        ops.element('zeroLength', int(f"1{ET}"), iDummy, iNode,
                    '-mat', hingeShTagzz, hingeShTagyy, rigM, rigM, rigM, rigM,
                    '-dir', 1, 2, 3, 4, 5, 6, '-doRayleigh', 1)
        ops.element('zeroLength', int(f"2{ET}"), jDummy, jNode,
                    '-mat', hingeShTagzz, hingeShTagyy, rigM, rigM, rigM, rigM,
                    '-dir', 1, 2, 3, 4, 5, 6, '-doRayleigh', 1)

        # Main element between dummy nodes
        ops.element('forceBeamColumn', ET, iDummy, jDummy, GT, intTag,
                    '-iter', 100, 1e-12)

    # Return a summary dict if you want to inspect values programmatically
    return {
        "nu": nu, "Lp": Lp, "L": L,
        "phi": {"Yzz": phiYzz, "Yyy": phiYyy, "Czz": phiCzz, "Cyy": phiCyy,
                "Uzz": phiUzz, "Uyy": phiUyy, "0zz": phi0zz, "0yy": phi0yy,
                "Mp1zz": phiMp1zz, "Mp2zz": phiMp2zz,
                "Mp1yy": phiMp1yy, "Mp2yy": phiMp2yy,
                "Mn1zz": phiMn1zz, "Mn2zz": phiMn2zz,
                "Mn1yy": phiMn1yy, "Mn2yy": phiMn2yy},
        "M": {
            "yp1zz": Myp1zz, "yn1zz": Myn1zz, "yp2zz": Myp2zz, "yn2zz": Myn2zz,
            "yp1yy": Myp1yy, "yn1yy": Myn1yy, "yp2yy": Myp2yy, "yn2yy": Myn2yy,
            "cp1zz": Mcp1zz, "cn1zz": Mcn1zz, "cp2zz": Mcp2zz, "cn2zz": Mcn2zz,
            "up1zz": Mup1zz, "un1zz": Mun1zz, "up2zz": Mup2zz, "un2zz": Mun2zz,
        },
        "EI": {"EIzze": EIzze, "EIyye": EIyye, "EIrzz": EIrzz, "EIryy": EIryy},
        "I": {"Izze": Izze, "Iyye": Iyye}
    }
