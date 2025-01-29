import numpy as np
import openseespy.opensees as op


class Recorder:
    def __init__(self, elements) -> None:
        """Initialize recorder

        Parameters
        ----------
        elements : ElementIDModel
            Dictionary containing element IDs
        """
        self.elements = elements

    def eigenvalue(self, geometry, num_modes: int,
                   eigenvectors: list):
        """Generates outputs following eigenvalue analysis

        Parameters
        ----------
        geometry : Geometry
            Model containing properties of structural model
        num_modes : int
            Number of modes
        eigenvectors : list
            Eigenvectors attained following eigenvalue analysis

        Returns
        -------
        tuple[OutputModel, List[int]]
            Outputs,
            Positions of 1st and 2nd mode (principal horizontal directions),
            for example if [1, 0], then 2nd mode is associated with index 0,
            and 1st mode is associated with index 1

        """
        # Get all node rags
        nodes = op.getNodeTags()

        # Initialize mass computation
        total_mass = np.array([0] * 6)

        # Compute total masses
        masses = np.zeros(geometry.nst)

        for node in nodes:
            indf = len(op.nodeDisp(node))
            for i in range(indf):
                total_mass[i] += op.nodeMass(node, i + 1)

            node = str(node)
            if node[-1] != "0":
                masses[int(node[-1]) - 1] += op.nodeMass(int(node), 1)

        # Results for each mode
        mode_data = np.zeros((num_modes, 4))
        mode_mpm = np.zeros((num_modes, 6))
        mode_l = np.zeros((num_modes, 6))

        # Extract eigenvalues to appropriate arrays
        omega = []
        freq = []
        period = []
        for mode in range(num_modes):
            omega.append(np.sqrt(eigenvectors[mode]))
            freq.append(np.sqrt(eigenvectors[mode]) / 2 / np.pi)
            period.append(2 * np.pi / np.sqrt(eigenvectors[mode]))
            mode_data[mode, :] = np.array(
                [eigenvectors[mode], omega[mode], freq[mode], period[mode]])

            # Compute L and gm
            lam = np.zeros((6,))
            gm = 0
            for node in nodes:
                v = op.nodeEigenvector(node, mode + 1)
                indf = len(op.nodeDisp(node))
                for i in range(indf):
                    mi = op.nodeMass(node, i + 1)
                    vi = v[i]
                    li = mi * vi
                    gm += vi ** 2 * mi
                    lam[i] += li
            mode_l[mode, :] = lam

            # Compute MPM
            mpm = np.zeros((6,))
            for i in range(6):
                li = lam[i]
                tmi = total_mass[i]
                mpmi = li ** 2
                if gm > 0.0:
                    mpmi = mpmi / gm
                if tmi > 0.0:
                    mpmi = mpmi / tmi * 100.0
                mpm[i] = mpmi
            mode_mpm[mode, :] = mpm

        # Get modal positions based on mass participation
        positions = np.argmax(mode_mpm, axis=1)
        # Take the first two, as for symmetric structures higher modes are
        # not so important
        positions = positions[:2]

        outputs = {"Mode1": [], "Mode2": []}

        # Initialize modal shape
        modal_shape = np.zeros((geometry.nst, 2))

        for st in range(geometry.nst):
            nodetag = int(
                f"{geometry.nbays[0] + 1}{geometry.nbays[1] + 1}{st + 1}")

            # Mode 1 refers to X direction, and Mode 2 refers to Y direction
            outputs["Mode1"].append(op.nodeEigenvector(
                nodetag, 1, int(positions[0] + 1)))
            outputs["Mode2"].append(op.nodeEigenvector(
                nodetag, 2, int(positions[1] + 1)))

            # First mode shape (also for 2D model)
            modal_shape[st, 0] = op.nodeEigenvector(
                nodetag, 1, int(positions[0] + 1))
            # Second mode shape
            modal_shape[st, 1] = op.nodeEigenvector(
                nodetag, 2, int(positions[1] + 1))

        # Normalize the modal shapes (first two modes, most likely associated
        # with X and Y directions unless
        # there are large torsional effects)
        modal_shape = np.abs(modal_shape) / np.max(np.abs(modal_shape), axis=0)

        # Calculate the first mode participation factor and effective
        # modal mass
        mass_matrix = np.zeros((geometry.nst, geometry.nst))
        for st in range(geometry.nst):
            mass_matrix[st][st] = masses[st]

        # Identity matrix
        identity = np.ones((1, geometry.nst))

        gamma = np.zeros(2)
        mstar = np.zeros(2)
        for i in range(2):
            # Modal participation factor
            gamma[i] = (modal_shape[:, i].transpose().dot(mass_matrix)).dot(
                identity.transpose()) / (modal_shape[:, i].transpose().dot(
                    mass_matrix)).dot(modal_shape[:, i])

            # Modal mass
            mstar[i] = (modal_shape[:, i].transpose().dot(
                mass_matrix)).dot(identity.transpose())

        # Modify indices of modal properties as follows:
        # index 0 = direction x
        # index 1 = direction y
        period = [period[i] for i in range(len(positions))]
        gamma = [gamma[i] for i in range(len(positions))]
        mstar = [mstar[i] for i in range(len(positions))]

        outputs['Periods'] = period
        outputs['Participation Factors'] = gamma
        outputs['M*'] = mstar

        return outputs, positions
