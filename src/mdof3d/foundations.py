import openseespy.opensees as ops


def add_foundations() -> None:
    """Add foundation components to ops domain (nodes and constraints).
    """
    # Foundation or support under the column 3000000
    ops.node(80000000, 0.0, 0.0, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80000000, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3000100
    ops.node(80000100, 0.0, 3.75, 0.0, '-mass', 0.4045871559633027, 0.4045871559633027, 0.4045871559633027, 0.0, 0.0, 0.0)
    ops.fix(80000100, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3000200
    ops.node(80000200, 0.0, 7.5, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80000200, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 4010000
    ops.node(80010000, 6.1, 0.0, 0.0, '-mass', 0.10321100917431195, 0.10321100917431195, 0.10321100917431195, 0.0, 0.0, 0.0)
    ops.fix(80010000, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3010100
    ops.node(80010100, 6.1, 3.75, 0.0, '-mass', 0.29724770642201837, 0.29724770642201837, 0.29724770642201837, 0.0, 0.0, 0.0)
    ops.fix(80010100, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3010200
    ops.node(80010200, 6.1, 7.5, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80010200, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 4020000
    ops.node(80020000, 8.95, 0.0, 0.0, '-mass', 0.10321100917431195, 0.10321100917431195, 0.10321100917431195, 0.0, 0.0, 0.0)
    ops.fix(80020000, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3020100
    ops.node(80020100, 8.95, 3.75, 0.0, '-mass', 0.29724770642201837, 0.29724770642201837, 0.29724770642201837, 0.0, 0.0, 0.0)
    ops.fix(80020100, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3020200
    ops.node(80020200, 8.95, 7.5, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80020200, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3030000
    ops.node(80030000, 15.05, 0.0, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80030000, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3030100
    ops.node(80030100, 15.05, 3.75, 0.0, '-mass', 0.4045871559633027, 0.4045871559633027, 0.4045871559633027, 0.0, 0.0, 0.0)
    ops.fix(80030100, 1, 1, 1, 1, 1, 1)

    # Foundation or support under the column 3030200
    ops.node(80030200, 15.05, 7.5, 0.0, '-mass', 0.2064220183486239, 0.2064220183486239, 0.2064220183486239, 0.0, 0.0, 0.0)
    ops.fix(80030200, 1, 1, 1, 1, 1, 1)
