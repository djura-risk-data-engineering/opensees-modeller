import os
import openseespy.opensees as ops


def do_modal(numModes=5, outsdir='', nodes=[]):
    """Perform modal analysis

    Parameters
    ----------
    numModes : int, optional
        Number modes to be considered. Default=5
    outsdir : str, optional
        Output directory. Default=''
    """
    ops.wipeAnalysis()
    ops.eigen(numModes)  # returns list of eigenvalues
    # Print the eigen vectors
    for i in range(1, numModes + 1):
        modal_disps = []
        for node in nodes:
            disps = ', '.join([
                f'{disp}' for disp in ops.nodeEigenvector(node, i)
            ])
            modal_disps.append(f'{node}, {disps}')
        modal_disps = '\n'.join(modal_disps)
        eigen_path = os.path.join(outsdir, f'EigenVectors_Mode{i}.txt')
        with open(eigen_path, 'w') as file:
            file.write(modal_disps)
    report_file = os.path.join(outsdir, "ModalProperties.txt")
    ops.modalProperties('-print', '-file', report_file, '-unorm')


def do_nspa(dref, mu, ctrl_node, disp_dir, n_steps, io_flag=1):
    """
    Perform a static pushover analysis (displacement controlled).

    Parameters
    ----------
    dref : float
        Reference displacement (e.g., yield displacement or 1 mm).
    mu : float
        Multiple of dref (target displacement = mu * dref).
    ctrl_node : int
        Node tag to control.
    disp_dir : int
        DOF direction of the displacement control.
    n_steps : int
        Number of steps.
    io_flag : int, optional
        Print detail level: 0=off, 1=basic, 2=each step. Default=1.
    """

    # --------------------------------------------------
    # Initial Analysis Parameters
    # --------------------------------------------------
    ops.wipeAnalysis()
    ops.constraints('Penalty', 1e14, 1e14)
    ops.numberer('RCM')
    ops.system("UmfPack")

    # test_type = "NormUnbalance"     # Don't use with Penalty constraints
    test_type = "NormDispIncr"
    # test_type = "EnergyIncr"        # Don't use with Penalty constraints
    # test_type = "RelativeNormUnbalance"     # Don't use with Penalty
    # test_type = "RelativeNormDispIncr"      # Don't use with Lagrange
    # test_type = "RelativeTotalNormDispIncr" # Don't use with Lagrange
    # test_type = "RelativeEnergyIncr"        # Don't use with Penalty

    tol_init = 1.0e-6   # initial tolerance (reference)
    iter_init = 50      # initial max iterations

    algorithm_type = "KrylovNewton"
    # algorithm_type = "Newton"
    # algorithm_type = "ModifiedNewton"

    ops.test(test_type, tol_init, iter_init)
    ops.algorithm(algorithm_type)

    disp = dref * mu
    dU = disp / n_steps

    ops.integrator("DisplacementControl", ctrl_node, disp_dir, dU)
    ops.analysis("Static")

    if io_flag >= 1:
        print(f"singlePush: Push node {ctrl_node} to mu={mu}")

    # --------------------------------------------------
    # Iterative push
    # --------------------------------------------------
    ok = 0
    step = 1
    loadf = 1.0

    while step <= n_steps and ok == 0 and loadf > 0:
        ok = ops.analyze(1)
        loadf = ops.getTime()
        temp = ops.nodeDisp(ctrl_node, disp_dir)

        if io_flag >= 2:
            print(f"Pushed node {ctrl_node} dir {disp_dir} "
                  f"to {temp:.6f} with loadf={loadf:.6f}")

        # If convergence fails, try relaxation strategies
        if ok != 0:
            print("Trying relaxed convergence..")
            ops.test(test_type, tol_init * 0.01, iter_init * 50)
            ok = ops.analyze(1)
            ops.test(test_type, tol_init, iter_init)

        if ok != 0:
            print("Trying Newton with initialThenCurrent ..")
            ops.test(test_type, tol_init * 0.01, iter_init * 50)
            ops.algorithm("Newton", "-initialThenCurrent")
            ok = ops.analyze(1)
            ops.algorithm(algorithm_type)
            ops.test(test_type, tol_init, iter_init)

        if ok != 0:
            print("Trying ModifiedNewton with initial ..")
            ops.test(test_type, tol_init * 0.01, iter_init * 50)
            ops.algorithm("ModifiedNewton", "-initial")
            ok = ops.analyze(1)
            ops.algorithm(algorithm_type)
            ops.test(test_type, tol_init, iter_init)

        if ok != 0:
            print("Trying KrylovNewton ..")
            ops.test(test_type, tol_init * 0.01, iter_init * 50)
            ops.algorithm("KrylovNewton")
            ok = ops.analyze(1)
            ops.algorithm(algorithm_type)
            ops.test(test_type, tol_init, iter_init)

        if ok != 0:
            print("Performing a Hail Mary ....")
            ops.test("FixedNumIter", iter_init)
            ok = ops.analyze(1)

        # Update state
        temp = ops.nodeDisp(ctrl_node, disp_dir)
        loadf = ops.getTime()
        step += 1

    # --------------------------------------------------
    # Post-analysis reporting
    # --------------------------------------------------
    if ok != 0:
        print("DispControl Analysis FAILED")
        # Alternative interactive handling in Tcl (not used in batch):
        # ans = input("Do you wish to continue y/n ?")
        # if ans.lower() == "n":
        #     exit()
    else:
        print("DispControl Analysis SUCCESSFUL")

    if loadf <= 0:
        print(f"Stopped because of Load factor below zero: {loadf}")
