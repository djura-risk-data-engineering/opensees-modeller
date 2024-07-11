
import openseespy.opensees as ops


def build(Fvect, Dvect, mass, damage):
    # Clear any preexisting model
    ops.wipe()

    # Create ModelBuilder (with two-dimensions and 3 DOF/node)
    ops.model('basic', '-ndm', 2, '-ndf', 3)

    # Define two nodes at the same location
    ops.node(1, 0, 0)
    ops.node(2, 0, 0)

    # Assign mass to the 2nd node
    ops.mass(2, mass, mass, 0)

    # Impose the fixations
    ops.fix(1, 1, 1, 1)
    ops.fix(2, 0, 0, 1)

    # Create the positive and negative envelopes
    positiveEnvelope = []
    negativeEnvelope = []

    for F, disp in zip(Fvect, Dvect):
        positiveEnvelope.extend([F, disp])
        negativeEnvelope.extend([-F, -disp])

    materialTag = 99

    if damage:
        ops.uniaxialMaterial('HystereticSM', materialTag, '-posEnv', *
                             positiveEnvelope, '-negEnv', *negativeEnvelope, '-damage', 0.1, 0.1)
    else:
        ops.uniaxialMaterial('HystereticSM', materialTag, '-posEnv',
                             *positiveEnvelope, '-negEnv', *negativeEnvelope)

    elementTag = 1

    # Local element axes coincide with global axes
    ops.element('zeroLength', elementTag, 1, 2, '-mat', *
                [99, 99], '-dir', *[1, 2], '-doRayleigh', 1)
