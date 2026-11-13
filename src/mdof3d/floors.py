import openseespy.opensees as ops


def add_floors() -> None:
    """Add floors to ops domain (retained nodes & diaphrams).
    """
    # Floor no. 1
    # Retained floor node
    ops.node(90000001, 7.525, 3.85402847, 2.7)
    # Rigid floor diaphragm - multi-point constraints
    ops.rigidDiaphragm(3, 90000001, 10000001, 10010001, 10020001, 10030001, 10000101, 10010101, 10020101, 10030101, 10000201, 10010201, 10020201, 10030201)
    # Fix the floating dofs of the retained node
    ops.fix(90000001, 0, 0, 1, 1, 1, 0)

    # Floor no. 2
    # Retained floor node
    ops.node(90000002, 7.525, 3.87378919, 5.4)
    # Rigid floor diaphragm - multi-point constraints
    ops.rigidDiaphragm(3, 90000002, 10000002, 10010002, 10020002, 10030002, 10000102, 10010102, 10020102, 10030102, 10000202, 10010202, 10020202, 10030202)
    # Fix the floating dofs of the retained node
    ops.fix(90000002, 0, 0, 1, 1, 1, 0)

    # Floor no. 3
    # Retained floor node
    ops.node(90000003, 7.525, 3.89886307, 8.1)
    # Rigid floor diaphragm - multi-point constraints
    ops.rigidDiaphragm(3, 90000003, 10000003, 10010003, 10020003, 10030003, 10000103, 10010103, 10020103, 10030103, 10000203, 10010203, 10020203, 10030203)
    # Fix the floating dofs of the retained node
    ops.fix(90000003, 0, 0, 1, 1, 1, 0)
