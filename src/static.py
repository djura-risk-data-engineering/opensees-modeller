import openseespy.opensees as op


class Static:
    NSTEP = 1
    TOL = 1.e-08

    def static_analysis(self, flag3d: bool = True) -> None:
        """Static gravity analysis parameters

        Parameters
        ----------
        flag3d : bool, optional
            Performs analysis for a 3D model, by default True
        """
        # Load increment
        dgravity = 1.0 / self.NSTEP
        # Determine next time step for an analysis
        op.integrator('LoadControl', dgravity)
        # Renumber dofs to minimize band-width (optimization)
        op.numberer('RCM')
        # Handling of boundary conditions
        if flag3d:
            op.constraints('Penalty', 1.0e15, 1.0e15)
            # Determine if convergence has been achieved at the end of
            # an iteration step
            op.test('EnergyIncr', self.TOL, 10)
            # How to store and solve the system of equations in the analysis
            # (large model: try UmfPack)
            op.system('UmfPack')
        else:
            op.constraints('Plain')
            op.test('NormDispIncr', self.TOL, 6)
            op.system('BandGeneral')

        # Use Newton's solution algorithm: updates tangent stiffness
        # at every iteration
        op.algorithm('Newton')
        # Define type of analysis (static or transient)
        op.analysis('Static')
        # Apply gravity
        op.analyze(self.NSTEP)
        # Maintain constant gravity loads and reset time to zero
        op.loadConst('-time', 0.0)
