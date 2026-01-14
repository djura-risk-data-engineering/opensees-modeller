"""
--------------------------------------------------
3D Model of Calvi et al. [2002] 3 Storey RC Frame
--------------------------------------------------
The original model was created in tcl by Gerard J. O'Reilly
The current model in Python was adapted from tcl by Volkan Ozsarac
--------------------------------------------------

References:
Calvi, G. M., Magenes, G., Pampanin, S. [2002] “Experimental Test on a
Three Storey RC Frame Designed for Gravity Only,” 12th European
Conference on Earthquake Engineering, London, UK.

O’Reilly, G. J., Sullivan, T. J. [2019] “Modeling Techniques for the Seisimic
Assessment of the Existing Italian RC Frame Structures,” Journal of Earthquake
Engineering, Vol. 23, No.8, pp. 1262-1296 DOI: 10.1080/13632469.2017.1360224.
"""

import os
import openseespy.opensees as ops

from .units import mm, m
from .joint import joint_model
from .rcbc import rcbc_nonduct
from .infill import infill_model
from .analyses import do_modal, do_nspa


def build_model(infills=0, outsdir="", sf=1.5):
    # -------------------------------
    # Setup / output folder
    # -------------------------------
    ops.wipe()
    if outsdir:
        os.makedirs(outsdir, exist_ok=True)

    # -------------------------------
    # Model def: 3D, 6 dof/node
    # -------------------------------
    ops.model('basic', '-ndm', 3, '-ndf', 6)

    # -------------------------------
    # Basic model parameters
    # -------------------------------
    # Dimensions (See Calvi et al. [2002] for details)
    hc = sf * 200 * mm  # column section height (m)
    bc = sf * 200 * mm  # column section width  (m)
    hb = sf * 330 * mm  # beam section height   (m)
    bb = sf * 200 * mm  # beam section width    (m)
    sb = sf * 115 * mm  # beam stirrup spacing  (m)
    sc = sf * 135 * mm  # column stirrup spacing (m)
    cv = 20 * mm  # cover (m)
    H = sf * 2.0 * m  # floor height (m)
    # dbeam = 301 * mm  # Beam section depth
    # dcolumn = 172 * mm  # Column section depth
    dbL = sf * 10 * mm  # long. bar dia (m)
    dbV = sf * 4 * mm  # transverse bar dia (m)
    B1 = sf * 3.0 * m  # width of 1st bay (m)
    B2 = sf * 1.33 * m  # width of 2nd bay (m)
    B3 = sf * 2.33 * m  # width of 3rd bay (m)

    # Axial loads (kN)
    P111 = sf * 43.0  # joint (X1, Y1, Z1)
    P211 = sf * 61.8  # joint (X2, Y1, Z1)
    P311 = sf * 57.1  # joint (X3, Y1, Z1)
    P411 = sf * 38.3  # joint (X4, Y1, Z1)
    P112 = sf * 27.1  # joint (X1, Y1, Z2)
    P212 = sf * 38.9  # joint (X2, Y1, Z2)
    P312 = sf * 36.5  # joint (X3, Y1, Z2)
    P412 = sf * 24.8  # joint (X4, Y1, Z2)
    P113 = sf * 11.2  # joint (X1, Y1, Z3)
    P213 = sf * 15.9  # joint (X2, Y1, Z3)
    P313 = sf * 15.9  # joint (X3, Y1, Z3)
    P413 = sf * 11.2  # joint (X4, Y1, Z3)

    # Structural masses (tonnes)
    M111 = sf * 1.62  # joint (X1, Y1, Z1)
    M211 = sf * 2.34  # joint (X2, Y1, Z1)
    M311 = sf * 2.10  # joint (X3, Y1, Z1)
    M411 = sf * 1.38  # joint (X4, Y1, Z1)
    M112 = sf * 1.62  # joint (X1, Y1, Z2)
    M212 = sf * 2.34  # joint (X2, Y1, Z2)
    M312 = sf * 2.10  # joint (X3, Y1, Z2)
    M412 = sf * 1.38  # joint (X4, Y1, Z2)
    M113 = sf * 1.14  # joint (X1, Y1, Z3)
    M213 = sf * 1.62  # joint (X2, Y1, Z3)
    M313 = sf * 1.62  # joint (X3, Y1, Z3)
    M413 = sf * 1.14  # joint (X4, Y1, Z3)

    # Material Properties (See Calvi et al. [2002] for details)
    # compressive strength of concrete (in MPa)
    fcb1 = 13.28  # 1st floor beams
    fcb2 = 13.84  # 2nd floor beams
    fcb3 = 12.72  # 3rd floor beams
    fcc1 = 17.06  # 1st floor columns
    fcc2 = 13.19  # 2nd floor columns
    fcc3 = 13.47  # 3rd floor columns
    # Elastic modulus of concrete (in MPa)
    Ecb1 = 3320 * (fcb1**0.5) + 6900  # 1st floor beams
    Ecb2 = 3320 * (fcb2**0.5) + 6900  # 2nd floor beams
    Ecb3 = 3320 * (fcb3**0.5) + 6900  # 3rd floor beams
    Ecc1 = 3320 * (fcc1**0.5) + 6900  # 1st floor columns
    Ecc2 = 3320 * (fcc2**0.5) + 6900  # 2nd floor columns
    Ecc3 = 3320 * (fcc3**0.5) + 6900  # 3rd floor columns
    # Yield strength of steel (in MPa)
    fyL = 345.9  # longitudinal reinforcement bars
    fyV = 385.6  # transverse reinforcement bars
    # # Ultimate strength of steel (in MPa)
    # fuL = 458.6  # longitudinal reinforcement bars
    # fuV = 451.9  # transverse reinforcement bars
    # Elastic modulus of steel (in MPa)
    Es = 200e3

    # Reinforcement ratios (See Calvi et al. [2002] for details)
    # Column section
    rC_top = 0.0043836176561718   # top
    rC_web = 0.0                  # web
    rC_bot = 0.0043836176561718   # bottom
    rC_shr = 0.000930842267730309  # shear
    # Beam Section 1
    rB1_top = 0.00542912215581993  # top
    rB1_web = 0.0                  # web
    rB1_bot = 0.00542912215581993  # bottom
    rB1_shr = 0.00109272787950949  # shear
    # Beam Section 3
    rB3_top = 0.00730498482849603  # top
    rB3_web = 0.0                  # web
    rB3_bot = 0.00166971081794195  # bottom
    rB3_shr = 0.00109272787950949  # shear
    # Beam Section 5
    rB5_top = 0.00542656015831134  # top
    rB5_web = 0.0                  # web
    rB5_bot = 0.00354813548812665  # bottom
    rB5_shr = 0.00109272787950949  # shear

    # Joint Properties (See O'Reilly [2016] for experimental calibration)
    # Shear deformations for each limit state: cracking, peak, ultimate
    gamm_int = 2 * [0.0002, 0.0090, 0.0200]
    gamm_ext = 2 * [0.0002, 0.0132, 0.0270]
    # Shear strength coefficients for each LS: cracking, peak, ultimate
    kappa_int = 2 * [0.29, 0.42, 0.42]
    kappa_ext = 2 * [0.132, 0.132, 0.053]
    # Hysteretic parameters (pinchx, pinchy, damage1, damage2, beta)
    hyst_ext = [0.6, 0.2, 0.0, 0.0, 0.3]
    hyst_int = [0.6, 0.2, 0.0, 0.01, 0.3]

    # Other inputs for the joint_model method
    c_c1 = [fcc1, Ecc1, cv]
    c_c2 = [fcc2, Ecc2, cv]
    c_c3 = [fcc3, Ecc3, cv]
    brs = [dbL, dbV]  # bar diameters (dbL, dbV) in m
    col = [hc, bc]  # (hcX, hcY) in m
    bm = [hb, hb, bb, bb]  # (hbX, hbY, bbX, bbY) in m

    # -------------------------------
    # Base nodes
    # -------------------------------
    # node tag x y z ; masses set to zero
    base_nodes = {
        1110: (0.0, 0.0, 0.0),
        1210: (B1, 0.0, 0.0),
        1310: (B1 + B2, 0.0, 0.0),
        1410: (B1 + B2 + B3, 0.0, 0.0),
    }
    for tag, (x, y, z) in base_nodes.items():
        ops.node(tag, x, y, z)
        ops.mass(tag, 0, 0, 0, 0, 0, 0)

    # -------------------------------
    # Transformations (PDelta + joint offsets)
    # -------------------------------
    # Use P-Delta geometric transformations. Include rigid-end offsets to
    # account for the rigid zones of the beam-column joints.
    # These are incorporated here as opposed to inserting rigid members at
    # each joint for computational efficiency. Local z is in global Y
    GTb, GTc = 1, 2  # TransfTag for beams and columns
    ops.geomTransf('PDelta', GTb, 0, 1, 0,
                   '-jntOffset',  hc/2, 0.0, 0.0, -hc/2, 0.0, 0.0)
    ops.geomTransf('PDelta', GTc, 0, 1, 0,
                   '-jntOffset',  0.0, 0.0,  hb/2, 0.0, 0.0, -hb/2)

    # -------------------------------
    # Property output files
    # -------------------------------
    # Open a set of files so that the properties of the beams, columns and
    # joint elements creted using the provided procedures can be examined
    # later.
    if outsdir:
        pfile_jnts = open(os.path.join(outsdir, "Properties_joints.txt"), "w")
        pfile_bms = open(os.path.join(outsdir, "Properties_beams.txt"), "w")
        pfile_cols = open(os.path.join(outsdir, "Properties_columnn.txt"), "w")
    else:
        pfile_jnts = None
        pfile_bms = None
        pfile_cols = None

    # -------------------------------
    # Joints
    # -------------------------------
    # 1st floor
    joint_model("Exterior", 111, (0.00, 0.0, 1*H), M111, col, bm, c_c1, brs,
                P111, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)
    joint_model("Interior", 211, (B1, 0.0, 1*H), M211, col, bm, c_c1, brs,
                P211, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Interior", 311, (B1+B2, 0.0, 1*H), M311, col, bm, c_c1, brs,
                P311, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Exterior", 411, (B1+B2+B3, 0.0, 1*H), M411, col, bm, c_c1,
                brs, P411, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)
    # 2nd floor
    joint_model("Exterior", 112, (0.00, 0.0, 2*H), M112, col, bm, c_c2, brs,
                P112, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)
    joint_model("Interior", 212, (B1, 0.0, 2*H), M212, col, bm, c_c2, brs,
                P212, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Interior", 312, (B1+B2, 0.0, 2*H), M312, col, bm, c_c2, brs,
                P312, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Exterior", 412, (B1+B2+B3, 0.0, 2*H), M412, col, bm, c_c2,
                brs, P412, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)
    # 3rd floor
    joint_model("Exterior", 113, (0.00, 0.0, 3*H), M113, col, bm, c_c3, brs,
                P113, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)
    joint_model("Interior", 213, (B1, 0.0, 3*H), M213, col, bm, c_c3, brs,
                P213, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Interior", 313, (B1+B2, 0.0, 3*H), M313, col, bm, c_c3, brs,
                P313, H, kappa_int, gamm_int, hyst_int, pfile_jnts)
    joint_model("Exterior", 413, (B1+B2+B3, 0.0, 3*H), M413, col, bm, c_c3,
                brs, P413, H, kappa_ext, gamm_ext, hyst_ext, pfile_jnts)

    # -------------------------------
    # Beams (ST=0)
    # -------------------------------
    # 1st floor
    ST = 0
    rcbc_nonduct(
        ST, 5111, GTb, int("6111"), int("6211"), fyL, fyV, Es, fcb1, Ecb1, bb,
        hb, sb, cv, dbL, dbV, 0.0, B1/2, rB1_shr, rB1_top, rB1_web, rB1_bot,
        rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web,
        rB1_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5211, GTb, int("6211"), int("6311"), fyL, fyV, Es, fcb1, Ecb1, bb,
        hb, sb, cv, dbL, dbV, 0.0, B2/2, rB3_shr, rB3_top, rB3_web, rB3_bot,
        rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web,
        rB3_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5311, GTb, int("6311"), int("6411"), fyL, fyV, Es, fcb1, Ecb1, bb,
        hb, sb, cv, dbL, dbV, 0.0, B3/2, rB5_shr, rB5_top, rB5_web, rB5_bot,
        rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web,
        rB5_bot, pfile_bms
    )
    # 2nd floor
    rcbc_nonduct(
        ST, 5112, GTb, int("6112"), int("6212"), fyL, fyV, Es, fcb2, Ecb2, bb,
        hb, sb, cv, dbL, dbV, 0.0, B1/2, rB1_shr, rB1_top, rB1_web, rB1_bot,
        rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web,
        rB1_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5212, GTb, int("6212"), int("6312"), fyL, fyV, Es, fcb2, Ecb2, bb,
        hb, sb, cv, dbL, dbV, 0.0, B2/2, rB3_shr, rB3_top, rB3_web, rB3_bot,
        rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web,
        rB3_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5312, GTb, int("6312"), int("6412"), fyL, fyV, Es, fcb2, Ecb2, bb,
        hb, sb, cv, dbL, dbV, 0.0, B3/2, rB5_shr, rB5_top, rB5_web, rB5_bot,
        rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web,
        rB5_bot, pfile_bms
    )
    # 3rd floor
    rcbc_nonduct(
        ST, 5113, GTb, int("6113"), int("6213"), fyL, fyV, Es, fcb3, Ecb3, bb,
        hb, sb, cv, dbL, dbV, 0.0, B1/2, rB1_shr, rB1_top, rB1_web, rB1_bot,
        rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web, rB1_bot, rB1_top, rB1_web,
        rB1_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5213, GTb, int("6213"), int("6313"), fyL, fyV, Es, fcb3, Ecb3, bb,
        hb, sb, cv, dbL, dbV, 0.0, B2/2, rB3_shr, rB3_top, rB3_web, rB3_bot,
        rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web, rB3_bot, rB3_top, rB3_web,
        rB3_bot, pfile_bms
    )
    rcbc_nonduct(
        ST, 5313, GTb, int("6313"), int("6413"), fyL, fyV, Es, fcb3, Ecb3, bb,
        hb, sb, cv, dbL, dbV, 0.0, B3/2, rB5_shr, rB5_top, rB5_web, rB5_bot,
        rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web, rB5_bot, rB5_top, rB5_web,
        rB5_bot, pfile_bms
    )

    # -------------------------------
    # Columns (ST=1)
    # -------------------------------
    ST = 1
    # 1st floor
    rcbc_nonduct(
        ST, 7111, GTc, 1110, 1111, fyL, fyV, Es, fcc1, Ecc1, bc, hc, sc,
        cv, dbL, dbV, P111, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7211, GTc, 1210, 1211, fyL, fyV, Es, fcc1, Ecc1, bc, hc, sc,
        cv, dbL, dbV, P211, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7311, GTc, 1310, 1311, fyL, fyV, Es, fcc1, Ecc1, bc, hc, sc,
        cv, dbL, dbV, P311, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7411, GTc, 1410, 1411, fyL, fyV, Es, fcc1, Ecc1, bc, hc, sc,
        cv, dbL, dbV, P411, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    # 2nd floor
    rcbc_nonduct(
        ST, 7112, GTc, 1111, 1112, fyL, fyV, Es, fcc2, Ecc2, bc, hc, sc,
        cv, dbL, dbV, P112, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7212, GTc, 1211, 1212, fyL, fyV, Es, fcc2, Ecc2, bc, hc, sc,
        cv, dbL, dbV, P212, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7312, GTc, 1311, 1312, fyL, fyV, Es, fcc2, Ecc2, bc, hc, sc,
        cv, dbL, dbV, P312, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7412, GTc, 1411, 1412, fyL, fyV, Es, fcc2, Ecc2, bc, hc, sc,
        cv, dbL, dbV, P412, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    # 3rd floor
    rcbc_nonduct(
        ST, 7113, GTc, 1112, 1113, fyL, fyV, Es, fcc3, Ecc3, bc, hc, sc,
        cv, dbL, dbV, P113, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7213, GTc, 1212, 1213, fyL, fyV, Es, fcc3, Ecc3, bc, hc, sc,
        cv, dbL, dbV, P213, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7313, GTc, 1312, 1313, fyL, fyV, Es, fcc3, Ecc3, bc, hc, sc,
        cv, dbL, dbV, P313, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )
    rcbc_nonduct(
        ST, 7413, GTc, 1412, 1413, fyL, fyV, Es, fcc3, Ecc3, bc, hc, sc,
        cv, dbL, dbV, P413, H/2, rC_shr, rC_top, rC_web, rC_bot, rC_top,
        rC_web, rC_bot, rC_top, rC_web, rC_bot, rC_top, rC_web, rC_bot,
        pfile_cols
    )

    if infills > 0:
        # Infill properties (weak infill from Hak et al. 2012)
        fwv = 2.02  # Vertical compressive strength [MPa]
        fwu = 0.44  # Sliding shear resistance of mortar joints [MPa]
        fws = 0.55  # Shear resistance under diagonal compression [MPa]
        Ewh = 991.0  # Concrete Elastic Modulus [MPa]
        Ewv = 1873.0  # Horizontal secant modulus [MPa]
        Gw = 1089.0  # Shear Modulus [MPa]
        tw = 80.0  # Wall thickness [mm]
        sig_v = 0.0	 # Vertical Compression due to gravity loading [MPa]
        v = 0.2  # Poissons Ratio

        # 1st floor
        # infill_model(
        #     2111, 'single', [1111, 1211, 1210, 1110], B1/mm, H/mm,
        #     hb/mm, hc/mm, bc/mm, tw, Ecc1, Ewh, Ewv, Gw, v, fwv, fwu, fws,
        #     sig_v, gt_inf=None, pflag=0
        # )
        infill_model(
            2211, 'single', [1211, 1311, 1310, 1210], B2/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc1, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        # infill_model(
        #     2311, 'single', [1311, 1411, 1410, 1310], B3/mm, H/mm,
        #     hb/mm, hc/mm, bc/mm, tw, Ecc1, Ewh, Ewv, Gw, v, fwv, fwu, fws,
        #     sig_v, gt_inf=None, pflag=0
        # )
        # 2nd floor
        infill_model(
            2112, 'single', [1112, 1212, 1211, 1111], B1/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc2, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        infill_model(
            2212, 'single', [1212, 1312, 1311, 1211], B2/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc2, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        infill_model(
            2312, 'single', [1312, 1412, 1411, 1311], B3/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc2, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        # 3rd floor
        infill_model(
            2113, 'single', [1113, 1213, 1212, 1112], B1/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc3, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        infill_model(
            2213, 'single', [1213, 1313, 1312, 1212], B2/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc3, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )
        infill_model(
            2313, 'single', [1313, 1413, 1412, 1312], B3/mm, H/mm,
            hb/mm, hc/mm, bc/mm, tw, Ecc3, Ewh, Ewv, Gw, v, fwv, fwu, fws,
            sig_v, gt_inf=None, pflag=0
        )

    print("Elements created")

    # Close property files
    if outsdir:
        pfile_jnts.close()
        pfile_bms.close()
        pfile_cols.close()

    # -------------------------------
    # Boundary conditions
    # -------------------------------
    # Base supports
    for node in (1110, 1210, 1310, 1410):
        ops.fix(node, 1, 1, 1, 1, 1, 1)

    # OOP support at connections: fix Y only (dY)
    oop_nodes = [
        1111, 1211, 1311, 1411,
        1112, 1212, 1312, 1412,
        1113, 1213, 1313, 1413
    ]
    for node in oop_nodes:
        ops.fix(node, 0, 1, 0, 0, 0, 0)

    # -------------------------------
    # Print model to file
    # -------------------------------
    if outsdir:
        model_path = os.path.join(outsdir, "model.txt")
        try:
            os.remove(model_path)
        except FileNotFoundError:
            pass
        ops.printModel('-file', model_path)

    # -------------------------------
    # Gravity analysis
    # -------------------------------
    ops.timeSeries('Constant', 101)
    ops.pattern('Plain', 101, 101)
    #             node   x   y      z     rx  ry  rz
    ops.load(1111, 0.0, 0.0, -(P111-P112), 0.0, 0.0, 0.0)
    ops.load(1211, 0.0, 0.0, -(P211-P212), 0.0, 0.0, 0.0)
    ops.load(1311, 0.0, 0.0, -(P311-P312), 0.0, 0.0, 0.0)
    ops.load(1411, 0.0, 0.0, -(P411-P412), 0.0, 0.0, 0.0)

    ops.load(1112, 0.0, 0.0, -(P112-P113), 0.0, 0.0, 0.0)
    ops.load(1212, 0.0, 0.0, -(P212-P213), 0.0, 0.0, 0.0)
    ops.load(1312, 0.0, 0.0, -(P312-P313), 0.0, 0.0, 0.0)
    ops.load(1412, 0.0, 0.0, -(P412-P413), 0.0, 0.0, 0.0)

    ops.load(1113, 0.0, 0.0, -P113, 0.0, 0.0, 0.0)
    ops.load(1213, 0.0, 0.0, -P213, 0.0, 0.0, 0.0)
    ops.load(1313, 0.0, 0.0, -P313, 0.0, 0.0, 0.0)
    ops.load(1413, 0.0, 0.0, -P413, 0.0, 0.0, 0.0)

    ops.constraints('Penalty', 1e14, 1e14)
    ops.numberer('RCM')
    ops.system('UmfPack')
    ops.test('EnergyIncr', 1e-6, 100)
    ops.algorithm('Newton')
    ops.integrator('LoadControl', 0.01)
    ops.analysis('Static')
    ops.analyze(100)

    # keep gravity & reset time
    ops.loadConst('-time', 0.0)
    print("Gravity analysis completed")


def run_nspa(infills=0, outsdir="", sf=1.5):

    # --------------------------------------
    # BUILD MODEL
    # --------------------------------------
    build_model(infills, outsdir, sf)

    # -------------------------------
    # Lateral loading
    # -------------------------------
    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    denom = 0.45 + 0.90 + 1.0
    ops.load(1111, 0.45 / denom, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(1112, 0.90 / denom, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(1113, 1.00 / denom, 0.0, 0.0, 0.0, 0.0, 0.0)
    print("Lateral loading applied")
    # --------------------------------------
    # Define recorders
    # --------------------------------------
    # Nodes
    ops.recorder(
        "Node", "-file", f"{outsdir}/displacement.txt",
        "-node", 1111, 1112, 1113, "-dof", 1, "disp"
    )
    ops.recorder(
        "Node", "-file", f"{outsdir}/reaction.txt",
        "-node", 1110, 1210, 1310, 1410, "-dof", 1, "reaction"
    )
    # # Hinges
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/joint_forces.txt",
    #     "-ele", 9113, 9213, 9313, 9413,
    #             9112, 9212, 9312, 9412,
    #             9111, 9211, 9311, 9411,
    #     "force"
    # )
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/joint_deformations.txt",
    #     "-ele", 9113, 9213, 9313, 9413,
    #             9112, 9212, 9312, 9412,
    #             9111, 9211, 9311, 9411,
    #     "deformation"
    # )
    # # Beams
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/beam_section_forces.txt",
    #     "-ele", 5113, 5213, 5313,
    #             5112, 5212, 5312,
    #             5111, 5211, 5311,
    #     "section", "force"
    # )
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/beam_section_deformations.txt",
    #     "-ele", 5113, 5213, 5313,
    #             5112, 5212, 5312,
    #             5111, 5211, 5311,
    #     "section", "deformation"
    # )
    # # Columns
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/column_section_forces.txt",
    #     "-ele", 7113, 7213, 7313, 7413,
    #             7112, 7212, 7312, 7412,
    #             7111, 7211, 7311, 7411,
    #     "section", "force"
    # )
    # ops.recorder(
    #     "Element", "-file", f"{outsdir}/column_section_deformations.txt",
    #     "-ele", 7113, 7213, 7313, 7413,
    #             7112, 7212, 7312, 7412,
    #             7111, 7211, 7311, 7411,
    #     "section", "deformation"
    # )

    # --------------------------------------
    # NONLINEAR STATIC PUSHOVER ANALYSIS
    # --------------------------------------
    dref = 0.04      # reference displacement
    mu = 6          # multiple of dref
    ctrl_node = 1113  # control node
    disp_dir = 1      # displacement direction
    n_steps = 2000     # number of steps
    do_nspa(dref, mu, ctrl_node, disp_dir, n_steps)


def run_modal(infills=0, outsdir="", sf=1.5, num_modes=5):
    # --------------------------------------
    # BUILD MODEL
    # --------------------------------------
    build_model(infills, outsdir, sf)

    # --------------------------------------
    # MODAL ANALYSIS
    # --------------------------------------
    nodes = [1111, 1112, 1113]
    do_modal(num_modes, outsdir, nodes)
