import numpy as np
import openseespy.opensees as ops

g = 9.81


def run_sdof(material, properties, record, dt, mass, damping=0.05):
    ops.wipe()
    ops.model('basic', '-ndm', 1, '-ndf', 1)
    ops.node(1, 0.)
    ops.node(2, 0.)
    ops.mass(2, mass)
    ops.fix(1, 1)

    ops.uniaxialMaterial(material, 1, *properties)
    ops.element("zeroLength", 1, 1, 2, "-mat",
                1, "-dir", 1, "-doRayleigh", 1)
    lam = ops.eigen("-fullGenLapack", 1)

    # Period
    _ = 2 * np.pi / np.sqrt(lam[0])

    omega = lam[0] ** 0.5
    ops.rayleigh(0.0, 0.0, 0.0, 2 * damping / omega)

    # Define ground motion
    acc = np.array(record[1]) * g
    t = record[0]
    dur = t[-1]

    # Define the analysis
    dt_analysis = 0.01
    ops.timeSeries('Path', 2, '-dt', dt, '-values', *acc)
    ops.pattern('UniformExcitation', 100, 1, '-accel', 2)
    ops.wipeAnalysis()
    ops.constraints('Plain')
    ops.numberer('Plain')
    ops.system('BandGeneral')
    ops.test('EnergyIncr', 1e-8, 10)
    ops.algorithm('ModifiedNewton')
    ops.integrator('Newmark', 0.5, 0.25)
    ops.analysis('Transient')

    # Run the analysis
    current_time = ops.getTime()
    curr_max_abs = 0.0

    ok = 0
    while current_time < dur and ok == 0:
        ok = ops.analyze(1, dt_analysis)
        if ok != 0:
            ok = ops.analyze(1, 0.5 * dt_analysis)
        if ok != 0:
            ok = ops.analyze(1, 0.25 * dt_analysis)
        if ok != 0:
            ops.algorithm('Broyden', 8)
            ok = ops.analyze(1, dt_analysis)
            ops.algorithm("ModifiedNewton")
        if ok != 0:
            ops.algorithm('Newton', '-initial')
            ok = ops.analyze(1, dt_analysis)
            ops.algorithm("ModifiedNewton")
        if ok != 0:
            ops.algorithm('NewtonLineSearch', 0.8)
            ok = ops.analyze(1, dt_analysis)
            ops.algorithm("ModifiedNewton")
        if ok != 0:
            ops.test('NormDispIncr', 1e-8 * 0.1, 10 * 50)
            ops.algorithm('Newton', '-initial')
            ok = ops.analyze(1, dt_analysis)
            ops.test('EnergyIncr', 1e-8, 10)
            ops.algorithm("ModifiedNewton")

        curr_disp = ops.nodeDisp(2)[0]

        if np.abs(curr_disp) > curr_max_abs:
            curr_max_abs = np.abs(curr_disp)

        current_time = ops.getTime()

    ops.wipe()

    return curr_max_abs
