import openseespy.opensees as ops


def add_joints() -> None:
    """Add components of joints to ops domain.
    """
    # -------------------------------------------------
    # Add stairs joints to ops domain
    # -------------------------------------------------
    # Joint grid ids (x, y, z): (1, 0, 0.5)
    ops.node(1010001, 6.1, 0.0, 1.35, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # Joint grid ids (x, y, z): (2, 0, 0.5)
    ops.node(1020001, 8.95, 0.0, 1.35, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # Joint grid ids (x, y, z): (1, 0, 1.5)
    ops.node(1010002, 6.1, 0.0, 4.05, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # Joint grid ids (x, y, z): (2, 0, 1.5)
    ops.node(1020002, 8.95, 0.0, 4.05, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # Joint grid ids (x, y, z): (1, 0, 2.5)
    ops.node(1010003, 6.1, 0.0, 6.75, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # Joint grid ids (x, y, z): (2, 0, 2.5)
    ops.node(1020003, 8.95, 0.0, 6.75, '-mass', 2.293728899082568, 2.293728899082568, 2.293728899082568, 0.0, 0.0, 0.0)

    # -------------------------------------------------
    # Add floor joints to ops domain
    # -------------------------------------------------
    # Joint grid ids (x, y, z): (0, 0, 1)
    ops.node(1, 0.0, 0.0, 2.7, '-mass', 5.378147122993725, 5.378147122993725, 5.378147122993725, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000001, 0.0, 0.0, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 131, 34.99761238, 0.0002, 34.99761238, 0.0132, 19.33714015, 0.027, -34.99761238, -0.0002, -34.99761238, -0.0132, -19.33714015, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 141, 62.27099378, 0.0002, 62.27099378, 0.0132, 33.1391536, 0.027, -62.27099378, -0.0002, -62.27099378, -0.0132, -33.1391536, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 130, 131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 140, 141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 150, 7916666.66666667)
    ops.section('Aggregator', 10000001, 150, 'P', 99999, 'Vy', 99999, 'Vz', 140, 'My', 130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000001, 1, 10000001, 10000001, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 0, 1)
    ops.node(10001, 6.1, 0.0, 2.7, '-mass', 5.67170400372767, 5.67170400372767, 5.67170400372767, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010001, 6.1, 0.0, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1000131, 42.94119656, 0.0002, 42.94119656, 0.0132, 24.22931068, 0.027, -42.94119656, -0.0002, -42.94119656, -0.0132, -24.22931068, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1000141, 92.85977235, 0.0002, 118.00041898, 0.009, 118.00041898, 0.02, -92.85977235, -0.0002, -118.00041898, -0.009, -118.00041898, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1000130, 1000131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1000140, 1000141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1000150, 7916666.66666667)
    ops.section('Aggregator', 10010001, 1000150, 'P', 99999, 'Vy', 99999, 'Vz', 1000140, 'My', 1000130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010001, 10001, 10010001, 10010001, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 0, 1)
    ops.node(20001, 8.95, 0.0, 2.7, '-mass', 5.671704003727672, 5.671704003727672, 5.671704003727672, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020001, 8.95, 0.0, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2000131, 42.94119656, 0.0002, 42.94119656, 0.0132, 24.22931068, 0.027, -42.94119656, -0.0002, -42.94119656, -0.0132, -24.22931068, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2000141, 92.85977235, 0.0002, 118.00041898, 0.009, 118.00041898, 0.02, -92.85977235, -0.0002, -118.00041898, -0.009, -118.00041898, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2000130, 2000131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2000140, 2000141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2000150, 7916666.66666667)
    ops.section('Aggregator', 10020001, 2000150, 'P', 99999, 'Vy', 99999, 'Vz', 2000140, 'My', 2000130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020001, 20001, 10020001, 10020001, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 0, 1)
    ops.node(30001, 15.05, 0.0, 2.7, '-mass', 5.3781471229937265, 5.3781471229937265, 5.3781471229937265, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030001, 15.05, 0.0, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3000131, 34.99761238, 0.0002, 34.99761238, 0.0132, 19.33714015, 0.027, -34.99761238, -0.0002, -34.99761238, -0.0132, -19.33714015, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3000141, 62.27099378, 0.0002, 62.27099378, 0.0132, 33.1391536, 0.027, -62.27099378, -0.0002, -62.27099378, -0.0132, -33.1391536, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3000130, 3000131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3000140, 3000141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3000150, 7916666.66666667)
    ops.section('Aggregator', 10030001, 3000150, 'P', 99999, 'Vy', 99999, 'Vz', 3000140, 'My', 3000130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030001, 30001, 10030001, 10030001, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 1, 1)
    ops.node(101, 0.0, 3.75, 2.7, '-mass', 9.257424521216807, 9.257424521216807, 9.257424521216807, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000101, 0.0, 3.75, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 10131, 84.46584748, 0.0002, 109.13365319, 0.009, 109.13365319, 0.02, -84.46584748, -0.0002, -109.13365319, -0.009, -109.13365319, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 10141, 124.71204572, 0.0002, 124.71204572, 0.0132, 67.40753984, 0.027, -124.71204572, -0.0002, -124.71204572, -0.0132, -67.40753984, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 10130, 10131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 10140, 10141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 10150, 13965000.0)
    ops.section('Aggregator', 10000101, 10150, 'P', 99999, 'Vy', 99999, 'Vz', 10140, 'My', 10130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000101, 101, 10000101, 10000101, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 1, 1)
    ops.node(10101, 6.1, 3.75, 2.7, '-mass', 12.503408261264935, 12.503408261264935, 12.503408261264935, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010101, 6.1, 3.75, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1010131, 73.951714, 0.0002, 93.65834584, 0.009, 93.65834584, 0.02, -73.951714, -0.0002, -93.65834584, -0.009, -93.65834584, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1010141, 131.95305832, 0.0002, 167.11587199, 0.009, 167.11587199, 0.02, -131.95305832, -0.0002, -167.11587199, -0.009, -167.11587199, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1010130, 1010131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1010140, 1010141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1010150, 10260000.0)
    ops.section('Aggregator', 10010101, 1010150, 'P', 99999, 'Vy', 99999, 'Vz', 1010140, 'My', 1010130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010101, 10101, 10010101, 10010101, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 1, 1)
    ops.node(20101, 8.95, 3.75, 2.7, '-mass', 12.503408261264937, 12.503408261264937, 12.503408261264937, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020101, 8.95, 3.75, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2010131, 73.951714, 0.0002, 93.65834584, 0.009, 93.65834584, 0.02, -73.951714, -0.0002, -93.65834584, -0.009, -93.65834584, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2010141, 131.95305832, 0.0002, 167.11587199, 0.009, 167.11587199, 0.02, -131.95305832, -0.0002, -167.11587199, -0.009, -167.11587199, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2010130, 2010131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2010140, 2010141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2010150, 10260000.0)
    ops.section('Aggregator', 10020101, 2010150, 'P', 99999, 'Vy', 99999, 'Vz', 2010140, 'My', 2010130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020101, 20101, 10020101, 10020101, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 1, 1)
    ops.node(30101, 15.05, 3.75, 2.7, '-mass', 9.257424521216809, 9.257424521216809, 9.257424521216809, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030101, 15.05, 3.75, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3010131, 84.46584748, 0.0002, 109.13365319, 0.009, 109.13365319, 0.02, -84.46584748, -0.0002, -109.13365319, -0.009, -109.13365319, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3010141, 124.71204572, 0.0002, 124.71204572, 0.0132, 67.40753984, 0.027, -124.71204572, -0.0002, -124.71204572, -0.0132, -67.40753984, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3010130, 3010131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3010140, 3010141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3010150, 13965000.0)
    ops.section('Aggregator', 10030101, 3010150, 'P', 99999, 'Vy', 99999, 'Vz', 3010140, 'My', 3010130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030101, 30101, 10030101, 10030101, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 2, 1)
    ops.node(201, 0.0, 7.5, 2.7, '-mass', 5.284874951739903, 5.284874951739903, 5.284874951739903, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000201, 0.0, 7.5, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 20131, 34.93290685, 0.0002, 34.93290685, 0.0132, 19.2930531, 0.027, -34.93290685, -0.0002, -34.93290685, -0.0132, -19.2930531, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 20141, 52.21277049, 0.0002, 52.21277049, 0.0132, 28.11377045, 0.027, -52.21277049, -0.0002, -52.21277049, -0.0132, -28.11377045, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 20130, 20131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 20140, 20141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 20150, 8906250.0)
    ops.section('Aggregator', 10000201, 20150, 'P', 99999, 'Vy', 99999, 'Vz', 20140, 'My', 20130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000201, 201, 10000201, 10000201, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 2, 1)
    ops.node(10201, 6.1, 7.5, 2.7, '-mass', 7.016424288118307, 7.016424288118307, 7.016424288118307, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010201, 6.1, 7.5, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1020131, 38.54591482, 0.0002, 38.54591482, 0.0132, 21.73359746, 0.027, -38.54591482, -0.0002, -38.54591482, -0.0132, -21.73359746, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1020141, 68.18443627, 0.0002, 86.68233402, 0.009, 86.68233402, 0.02, -68.18443627, -0.0002, -86.68233402, -0.009, -86.68233402, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1020130, 1020131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1020140, 1020141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1020150, 8906250.0)
    ops.section('Aggregator', 10010201, 1020150, 'P', 99999, 'Vy', 99999, 'Vz', 1020140, 'My', 1020130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010201, 10201, 10010201, 10010201, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 2, 1)
    ops.node(20201, 8.95, 7.5, 2.7, '-mass', 7.0164242881183085, 7.0164242881183085, 7.0164242881183085, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020201, 8.95, 7.5, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2020131, 38.54591482, 0.0002, 38.54591482, 0.0132, 21.73359746, 0.027, -38.54591482, -0.0002, -38.54591482, -0.0132, -21.73359746, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2020141, 68.18443627, 0.0002, 86.68233402, 0.009, 86.68233402, 0.02, -68.18443627, -0.0002, -86.68233402, -0.009, -86.68233402, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2020130, 2020131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2020140, 2020141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2020150, 8906250.0)
    ops.section('Aggregator', 10020201, 2020150, 'P', 99999, 'Vy', 99999, 'Vz', 2020140, 'My', 2020130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020201, 20201, 10020201, 10020201, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 2, 1)
    ops.node(30201, 15.05, 7.5, 2.7, '-mass', 5.284874951739904, 5.284874951739904, 5.284874951739904, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030201, 15.05, 7.5, 2.7) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3020131, 34.93290685, 0.0002, 34.93290685, 0.0132, 19.2930531, 0.027, -34.93290685, -0.0002, -34.93290685, -0.0132, -19.2930531, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3020141, 52.21277049, 0.0002, 52.21277049, 0.0132, 28.11377045, 0.027, -52.21277049, -0.0002, -52.21277049, -0.0132, -28.11377045, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3020130, 3020131, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3020140, 3020141, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3020150, 8906250.0)
    ops.section('Aggregator', 10030201, 3020150, 'P', 99999, 'Vy', 99999, 'Vz', 3020140, 'My', 3020130, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030201, 30201, 10030201, 10030201, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 0, 2)
    ops.node(2, 0.0, 0.0, 5.4, '-mass', 5.284874951739903, 5.284874951739903, 5.284874951739903, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000002, 0.0, 0.0, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 231, 31.06156905, 0.0002, 31.06156905, 0.0132, 16.62089293, 0.027, -31.06156905, -0.0002, -31.06156905, -0.0132, -16.62089293, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 241, 47.01360872, 0.0002, 47.01360872, 0.0132, 24.47605444, 0.027, -47.01360872, -0.0002, -47.01360872, -0.0132, -24.47605444, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 230, 231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 240, 241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 250, 8906250.0)
    ops.section('Aggregator', 10000002, 250, 'P', 99999, 'Vy', 99999, 'Vz', 240, 'My', 230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000002, 2, 10000002, 10000002, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 0, 2)
    ops.node(10002, 6.1, 0.0, 5.4, '-mass', 5.534853850822471, 5.534853850822471, 5.534853850822471, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010002, 6.1, 0.0, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1000231, 37.11091132, 0.0002, 37.11091132, 0.0132, 20.27699272, 0.027, -37.11091132, -0.0002, -37.11091132, -0.0132, -20.27699272, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1000241, 67.5865052, 0.0002, 87.53415043, 0.009, 87.53415043, 0.02, -67.5865052, -0.0002, -87.53415043, -0.009, -87.53415043, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1000230, 1000231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1000240, 1000241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1000250, 8906250.0)
    ops.section('Aggregator', 10010002, 1000250, 'P', 99999, 'Vy', 99999, 'Vz', 1000240, 'My', 1000230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010002, 10002, 10010002, 10010002, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 0, 2)
    ops.node(20002, 8.95, 0.0, 5.4, '-mass', 5.534853850822473, 5.534853850822473, 5.534853850822473, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020002, 8.95, 0.0, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2000231, 37.11091132, 0.0002, 37.11091132, 0.0132, 20.27699272, 0.027, -37.11091132, -0.0002, -37.11091132, -0.0132, -20.27699272, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2000241, 67.5865052, 0.0002, 87.53415043, 0.009, 87.53415043, 0.02, -67.5865052, -0.0002, -87.53415043, -0.009, -87.53415043, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2000230, 2000231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2000240, 2000241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2000250, 8906250.0)
    ops.section('Aggregator', 10020002, 2000250, 'P', 99999, 'Vy', 99999, 'Vz', 2000240, 'My', 2000230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020002, 20002, 10020002, 10020002, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 0, 2)
    ops.node(30002, 15.05, 0.0, 5.4, '-mass', 5.284874951739904, 5.284874951739904, 5.284874951739904, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030002, 15.05, 0.0, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3000231, 31.06156905, 0.0002, 31.06156905, 0.0132, 16.62089293, 0.027, -31.06156905, -0.0002, -31.06156905, -0.0132, -16.62089293, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3000241, 47.01360872, 0.0002, 47.01360872, 0.0132, 24.47605444, 0.027, -47.01360872, -0.0002, -47.01360872, -0.0132, -24.47605444, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3000230, 3000231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3000240, 3000241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3000250, 8906250.0)
    ops.section('Aggregator', 10030002, 3000250, 'P', 99999, 'Vy', 99999, 'Vz', 3000240, 'My', 3000230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030002, 30002, 10030002, 10030002, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 1, 2)
    ops.node(102, 0.0, 3.75, 5.4, '-mass', 9.257424521216807, 9.257424521216807, 9.257424521216807, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000102, 0.0, 3.75, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 10231, 74.91218136, 0.0002, 98.51367935, 0.009, 98.51367935, 0.02, -74.91218136, -0.0002, -98.51367935, -0.009, -98.51367935, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 10241, 112.45145345, 0.0002, 112.45145345, 0.0132, 58.82863148, 0.027, -112.45145345, -0.0002, -112.45145345, -0.0132, -58.82863148, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 10230, 10231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 10240, 10241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 10250, 13965000.0)
    ops.section('Aggregator', 10000102, 10250, 'P', 99999, 'Vy', 99999, 'Vz', 10240, 'My', 10230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000102, 102, 10000102, 10000102, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 1, 2)
    ops.node(10102, 6.1, 3.75, 5.4, '-mass', 12.503408261264935, 12.503408261264935, 12.503408261264935, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010102, 6.1, 3.75, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1010231, 64.57322172, 0.0002, 83.00813731, 0.009, 83.00813731, 0.02, -64.57322172, -0.0002, -83.00813731, -0.009, -83.00813731, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1010241, 115.21888582, 0.0002, 148.11255873, 0.009, 148.11255873, 0.02, -115.21888582, -0.0002, -148.11255873, -0.009, -148.11255873, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1010230, 1010231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1010240, 1010241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1010250, 10260000.0)
    ops.section('Aggregator', 10010102, 1010250, 'P', 99999, 'Vy', 99999, 'Vz', 1010240, 'My', 1010230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010102, 10102, 10010102, 10010102, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 1, 2)
    ops.node(20102, 8.95, 3.75, 5.4, '-mass', 12.503408261264937, 12.503408261264937, 12.503408261264937, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020102, 8.95, 3.75, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2010231, 64.57322172, 0.0002, 83.00813731, 0.009, 83.00813731, 0.02, -64.57322172, -0.0002, -83.00813731, -0.009, -83.00813731, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2010241, 115.21888582, 0.0002, 148.11255873, 0.009, 148.11255873, 0.02, -115.21888582, -0.0002, -148.11255873, -0.009, -148.11255873, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2010230, 2010231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2010240, 2010241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2010250, 10260000.0)
    ops.section('Aggregator', 10020102, 2010250, 'P', 99999, 'Vy', 99999, 'Vz', 2010240, 'My', 2010230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020102, 20102, 10020102, 10020102, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 1, 2)
    ops.node(30102, 15.05, 3.75, 5.4, '-mass', 9.257424521216809, 9.257424521216809, 9.257424521216809, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030102, 15.05, 3.75, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3010231, 74.91218136, 0.0002, 98.51367935, 0.009, 98.51367935, 0.02, -74.91218136, -0.0002, -98.51367935, -0.009, -98.51367935, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3010241, 112.45145345, 0.0002, 112.45145345, 0.0132, 58.82863148, 0.027, -112.45145345, -0.0002, -112.45145345, -0.0132, -58.82863148, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3010230, 3010231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3010240, 3010241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3010250, 13965000.0)
    ops.section('Aggregator', 10030102, 3010250, 'P', 99999, 'Vy', 99999, 'Vz', 3010240, 'My', 3010230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030102, 30102, 10030102, 10030102, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 2, 2)
    ops.node(202, 0.0, 7.5, 5.4, '-mass', 5.284874951739903, 5.284874951739903, 5.284874951739903, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000202, 0.0, 7.5, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 20231, 31.06156905, 0.0002, 31.06156905, 0.0132, 16.62089293, 0.027, -31.06156905, -0.0002, -31.06156905, -0.0132, -16.62089293, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 20241, 47.01360872, 0.0002, 47.01360872, 0.0132, 24.47605444, 0.027, -47.01360872, -0.0002, -47.01360872, -0.0132, -24.47605444, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 20230, 20231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 20240, 20241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 20250, 8906250.0)
    ops.section('Aggregator', 10000202, 20250, 'P', 99999, 'Vy', 99999, 'Vz', 20240, 'My', 20230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000202, 202, 10000202, 10000202, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 2, 2)
    ops.node(10202, 6.1, 7.5, 5.4, '-mass', 7.016424288118307, 7.016424288118307, 7.016424288118307, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010202, 6.1, 7.5, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1020231, 33.95449431, 0.0002, 33.95449431, 0.0132, 18.62439547, 0.027, -33.95449431, -0.0002, -33.95449431, -0.0132, -18.62439547, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1020241, 59.34849074, 0.0002, 76.69291117, 0.009, 76.69291117, 0.02, -59.34849074, -0.0002, -76.69291117, -0.009, -76.69291117, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 1020230, 1020231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1020240, 1020241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1020250, 8906250.0)
    ops.section('Aggregator', 10010202, 1020250, 'P', 99999, 'Vy', 99999, 'Vz', 1020240, 'My', 1020230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010202, 10202, 10010202, 10010202, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 2, 2)
    ops.node(20202, 8.95, 7.5, 5.4, '-mass', 7.0164242881183085, 7.0164242881183085, 7.0164242881183085, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020202, 8.95, 7.5, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2020231, 33.95449431, 0.0002, 33.95449431, 0.0132, 18.62439547, 0.027, -33.95449431, -0.0002, -33.95449431, -0.0132, -18.62439547, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2020241, 59.34849074, 0.0002, 76.69291117, 0.009, 76.69291117, 0.02, -59.34849074, -0.0002, -76.69291117, -0.009, -76.69291117, -0.02, 0.6, 0.2, 0.0, 0.01, 0.3)
    ops.uniaxialMaterial('MinMax', 2020230, 2020231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2020240, 2020241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2020250, 8906250.0)
    ops.section('Aggregator', 10020202, 2020250, 'P', 99999, 'Vy', 99999, 'Vz', 2020240, 'My', 2020230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020202, 20202, 10020202, 10020202, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 2, 2)
    ops.node(30202, 15.05, 7.5, 5.4, '-mass', 5.284874951739904, 5.284874951739904, 5.284874951739904, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030202, 15.05, 7.5, 5.4) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3020231, 31.06156905, 0.0002, 31.06156905, 0.0132, 16.62089293, 0.027, -31.06156905, -0.0002, -31.06156905, -0.0132, -16.62089293, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3020241, 47.01360872, 0.0002, 47.01360872, 0.0132, 24.47605444, 0.027, -47.01360872, -0.0002, -47.01360872, -0.0132, -24.47605444, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3020230, 3020231, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3020240, 3020241, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3020250, 8906250.0)
    ops.section('Aggregator', 10030202, 3020250, 'P', 99999, 'Vy', 99999, 'Vz', 3020240, 'My', 3020230, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030202, 30202, 10030202, 10030202, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 0, 3)
    ops.node(3, 0.0, 0.0, 8.1, '-mass', 3.834461496082411, 3.834461496082411, 3.834461496082411, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000003, 0.0, 0.0, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 331, 46.73307992, 0.0002, 46.73307992, 0.0132, 23.14845279, 0.027, -46.73307992, -0.0002, -46.73307992, -0.0132, -23.14845279, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 341, 70.17496816, 0.0002, 70.17496816, 0.0132, 33.80538016, 0.027, -70.17496816, -0.0002, -70.17496816, -0.0132, -33.80538016, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 330, 331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 340, 341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 350, 8906250.0)
    ops.section('Aggregator', 10000003, 350, 'P', 99999, 'Vy', 99999, 'Vz', 340, 'My', 330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000003, 3, 10000003, 10000003, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 0, 3)
    ops.node(10003, 6.1, 0.0, 8.1, '-mass', 4.010149569476906, 4.010149569476906, 4.010149569476906, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010003, 6.1, 0.0, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1000331, 47.03917366, 0.0002, 47.03917366, 0.0132, 23.38007853, 0.027, -47.03917366, -0.0002, -47.03917366, -0.0132, -23.38007853, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1000341, 70.56360741, 0.0002, 70.56360741, 0.0132, 34.10550789, 0.027, -70.56360741, -0.0002, -70.56360741, -0.0132, -34.10550789, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 1000330, 1000331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1000340, 1000341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1000350, 8906250.0)
    ops.section('Aggregator', 10010003, 1000350, 'P', 99999, 'Vy', 99999, 'Vz', 1000340, 'My', 1000330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010003, 10003, 10010003, 10010003, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 0, 3)
    ops.node(20003, 8.95, 0.0, 8.1, '-mass', 4.010149569476907, 4.010149569476907, 4.010149569476907, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020003, 8.95, 0.0, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2000331, 47.03917366, 0.0002, 47.03917366, 0.0132, 23.38007853, 0.027, -47.03917366, -0.0002, -47.03917366, -0.0132, -23.38007853, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2000341, 70.56360741, 0.0002, 70.56360741, 0.0132, 34.10550789, 0.027, -70.56360741, -0.0002, -70.56360741, -0.0132, -34.10550789, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 2000330, 2000331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2000340, 2000341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2000350, 8906250.0)
    ops.section('Aggregator', 10020003, 2000350, 'P', 99999, 'Vy', 99999, 'Vz', 2000340, 'My', 2000330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020003, 20003, 10020003, 10020003, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 0, 3)
    ops.node(30003, 15.05, 0.0, 8.1, '-mass', 3.8344614960824113, 3.8344614960824113, 3.8344614960824113, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030003, 15.05, 0.0, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3000331, 46.73307992, 0.0002, 46.73307992, 0.0132, 23.14845279, 0.027, -46.73307992, -0.0002, -46.73307992, -0.0132, -23.14845279, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3000341, 70.17496816, 0.0002, 70.17496816, 0.0132, 33.80538016, 0.027, -70.17496816, -0.0002, -70.17496816, -0.0132, -33.80538016, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3000330, 3000331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3000340, 3000341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3000350, 8906250.0)
    ops.section('Aggregator', 10030003, 3000350, 'P', 99999, 'Vy', 99999, 'Vz', 3000340, 'My', 3000330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030003, 30003, 10030003, 10030003, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 1, 3)
    ops.node(103, 0.0, 3.75, 8.1, '-mass', 7.306231860666349, 7.306231860666349, 7.306231860666349, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000103, 0.0, 3.75, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 10331, 81.89573345, 0.0002, 81.89573345, 0.0132, 41.53310889, 0.027, -81.89573345, -0.0002, -81.89573345, -0.0132, -41.53310889, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 10341, 140.3294107, 0.0002, 140.3294107, 0.0132, 68.89422706, 0.027, -140.3294107, -0.0002, -140.3294107, -0.0132, -68.89422706, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 10330, 10331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 10340, 10341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 10350, 15516666.66666667)
    ops.section('Aggregator', 10000103, 10350, 'P', 99999, 'Vy', 99999, 'Vz', 10340, 'My', 10330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000103, 103, 10000103, 10000103, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 1, 3)
    ops.node(10103, 6.1, 3.75, 8.1, '-mass', 10.649027527319983, 10.649027527319983, 10.649027527319983, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010103, 6.1, 3.75, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1010331, 70.99115881, 0.0002, 70.99115881, 0.0132, 37.46139689, 0.027, -70.99115881, -0.0002, -70.99115881, -0.0132, -37.46139689, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1010341, 121.42376599, 0.0002, 121.42376599, 0.0132, 61.77888895, 0.027, -121.42376599, -0.0002, -121.42376599, -0.0132, -61.77888895, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 1010330, 1010331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1010340, 1010341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1010350, 11400000.0)
    ops.section('Aggregator', 10010103, 1010350, 'P', 99999, 'Vy', 99999, 'Vz', 1010340, 'My', 1010330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010103, 10103, 10010103, 10010103, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 1, 3)
    ops.node(20103, 8.95, 3.75, 8.1, '-mass', 10.649027527319985, 10.649027527319985, 10.649027527319985, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020103, 8.95, 3.75, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2010331, 70.99115881, 0.0002, 70.99115881, 0.0132, 37.46139689, 0.027, -70.99115881, -0.0002, -70.99115881, -0.0132, -37.46139689, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2010341, 121.42376599, 0.0002, 121.42376599, 0.0132, 61.77888895, 0.027, -121.42376599, -0.0002, -121.42376599, -0.0132, -61.77888895, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 2010330, 2010331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2010340, 2010341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2010350, 11400000.0)
    ops.section('Aggregator', 10020103, 2010350, 'P', 99999, 'Vy', 99999, 'Vz', 2010340, 'My', 2010330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020103, 20103, 10020103, 10020103, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 1, 3)
    ops.node(30103, 15.05, 3.75, 8.1, '-mass', 7.306231860666351, 7.306231860666351, 7.306231860666351, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030103, 15.05, 3.75, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3010331, 81.89573345, 0.0002, 81.89573345, 0.0132, 41.53310889, 0.027, -81.89573345, -0.0002, -81.89573345, -0.0132, -41.53310889, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3010341, 140.3294107, 0.0002, 140.3294107, 0.0132, 68.89422706, 0.027, -140.3294107, -0.0002, -140.3294107, -0.0132, -68.89422706, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3010330, 3010331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3010340, 3010341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3010350, 15516666.66666667)
    ops.section('Aggregator', 10030103, 3010350, 'P', 99999, 'Vy', 99999, 'Vz', 3010340, 'My', 3010330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030103, 30103, 10030103, 10030103, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (0, 2, 3)
    ops.node(203, 0.0, 7.5, 8.1, '-mass', 3.834461496082411, 3.834461496082411, 3.834461496082411, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10000203, 0.0, 7.5, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 20331, 46.73307992, 0.0002, 46.73307992, 0.0132, 23.14845279, 0.027, -46.73307992, -0.0002, -46.73307992, -0.0132, -23.14845279, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 20341, 70.17496816, 0.0002, 70.17496816, 0.0132, 33.80538016, 0.027, -70.17496816, -0.0002, -70.17496816, -0.0132, -33.80538016, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 20330, 20331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 20340, 20341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 20350, 8906250.0)
    ops.section('Aggregator', 10000203, 20350, 'P', 99999, 'Vy', 99999, 'Vz', 20340, 'My', 20330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10000203, 203, 10000203, 10000203, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (1, 2, 3)
    ops.node(10203, 6.1, 7.5, 8.1, '-mass', 5.400938355396595, 5.400938355396595, 5.400938355396595, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10010203, 6.1, 7.5, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 1020331, 49.98735567, 0.0002, 49.98735567, 0.0132, 25.57111355, 0.027, -49.98735567, -0.0002, -49.98735567, -0.0132, -25.57111355, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 1020341, 74.32209718, 0.0002, 74.32209718, 0.0132, 36.95388747, 0.027, -74.32209718, -0.0002, -74.32209718, -0.0132, -36.95388747, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 1020330, 1020331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 1020340, 1020341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 1020350, 8906250.0)
    ops.section('Aggregator', 10010203, 1020350, 'P', 99999, 'Vy', 99999, 'Vz', 1020340, 'My', 1020330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10010203, 10203, 10010203, 10010203, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (2, 2, 3)
    ops.node(20203, 8.95, 7.5, 8.1, '-mass', 5.400938355396595, 5.400938355396595, 5.400938355396595, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10020203, 8.95, 7.5, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 2020331, 49.98735567, 0.0002, 49.98735567, 0.0132, 25.57111355, 0.027, -49.98735567, -0.0002, -49.98735567, -0.0132, -25.57111355, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 2020341, 74.32209718, 0.0002, 74.32209718, 0.0132, 36.95388747, 0.027, -74.32209718, -0.0002, -74.32209718, -0.0132, -36.95388747, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 2020330, 2020331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 2020340, 2020341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 2020350, 8906250.0)
    ops.section('Aggregator', 10020203, 2020350, 'P', 99999, 'Vy', 99999, 'Vz', 2020340, 'My', 2020330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10020203, 20203, 10020203, 10020203, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)

    # Joint grid ids (x, y, z): (3, 2, 3)
    ops.node(30203, 15.05, 7.5, 8.1, '-mass', 3.8344614960824113, 3.8344614960824113, 3.8344614960824113, 0.0, 0.0, 0.0)
    # Joint flexibility model: inelastic
    ops.node(10030203, 15.05, 7.5, 8.1) # Constrained floor node
    ops.uniaxialMaterial('Hysteretic', 3020331, 46.73307992, 0.0002, 46.73307992, 0.0132, 23.14845279, 0.027, -46.73307992, -0.0002, -46.73307992, -0.0132, -23.14845279, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('Hysteretic', 3020341, 70.17496816, 0.0002, 70.17496816, 0.0132, 33.80538016, 0.027, -70.17496816, -0.0002, -70.17496816, -0.0132, -33.80538016, -0.027, 0.6, 0.2, 0.0, 0.0, 0.3)
    ops.uniaxialMaterial('MinMax', 3020330, 3020331, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('MinMax', 3020340, 3020341, '-min', -0.1, '-max', 0.1)
    ops.uniaxialMaterial('Elastic', 3020350, 8906250.0)
    ops.section('Aggregator', 10030203, 3020350, 'P', 99999, 'Vy', 99999, 'Vz', 3020340, 'My', 3020330, 'Mz', 99999, 'T')
    ops.element('zeroLengthSection', 10030203, 30203, 10030203, 10030203, '-orient', 0, 0, 1, 0, 1, 0, '-doRayleigh', 0)
