from pathlib import Path
import openseespy.opensees as ops


def gravity():

    ops.timeSeries('Linear', 1)
    ops.pattern('Plain', 1, 1)
    # loading BeamsX
    ops.eleLoad('-ele', 50101, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50102, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50103, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50104, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50105, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50106, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50107, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50108, '-type', '-beamUniform', -25.4, 0)
    ops.eleLoad('-ele', 50109, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50110, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50111, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50112, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50113, '-type', '-beamUniform', -13.4, 0)
    ops.eleLoad('-ele', 50114, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50115, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50201, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50202, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50203, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50204, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50205, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50206, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50207, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50208, '-type', '-beamUniform', -25.4, 0)
    ops.eleLoad('-ele', 50209, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50210, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50211, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50212, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50213, '-type', '-beamUniform', -13.4, 0)
    ops.eleLoad('-ele', 50214, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50215, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50301, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50302, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50303, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50304, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50305, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50306, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50307, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50308, '-type', '-beamUniform', -25.4, 0)
    ops.eleLoad('-ele', 50309, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50310, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50311, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50312, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50313, '-type', '-beamUniform', -13.4, 0)
    ops.eleLoad('-ele', 50314, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50315, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50401, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50402, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50403, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50404, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50405, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50406, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50407, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50408, '-type', '-beamUniform', -25.4, 0)
    ops.eleLoad('-ele', 50409, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50410, '-type', '-beamUniform', -25.3, 0)
    ops.eleLoad('-ele', 50411, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50412, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50413, '-type', '-beamUniform', -13.4, 0)
    ops.eleLoad('-ele', 50414, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50415, '-type', '-beamUniform', -15.4, 0)
    ops.eleLoad('-ele', 50501, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50502, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50503, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50504, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50505, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50506, '-type', '-beamUniform', -23.0, 0)
    ops.eleLoad('-ele', 50507, '-type', '-beamUniform', -23.0, 0)
    ops.eleLoad('-ele', 50508, '-type', '-beamUniform', -24.2, 0)
    ops.eleLoad('-ele', 50509, '-type', '-beamUniform', -23.0, 0)
    ops.eleLoad('-ele', 50510, '-type', '-beamUniform', -23.0, 0)
    ops.eleLoad('-ele', 50511, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50512, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50513, '-type', '-beamUniform', -11.5, 0)
    ops.eleLoad('-ele', 50514, '-type', '-beamUniform', -13.5, 0)
    ops.eleLoad('-ele', 50515, '-type', '-beamUniform', -13.5, 0)
    # loading BeamsY
    ops.eleLoad('-ele', 50151, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50157, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50152, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50158, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50153, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50159, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50154, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50160, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50155, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50161, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50156, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50162, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50251, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50257, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50252, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50258, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50253, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50259, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50254, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50260, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50255, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50261, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50256, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50262, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50351, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50357, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50352, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50358, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50353, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50359, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50354, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50360, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50355, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50361, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50356, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50362, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50451, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50457, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50452, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50458, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50453, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50459, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50454, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50460, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50455, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50461, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50456, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50462, '-type', '-beamUniform', -2.1, 0)
    ops.eleLoad('-ele', 50551, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50557, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50552, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50558, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50553, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50559, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50554, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50560, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50555, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50561, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50556, '-type', '-beamUniform', -1.4, 0)
    ops.eleLoad('-ele', 50562, '-type', '-beamUniform', -1.4, 0)
    # loading BeamsStair
    ops.eleLoad('-ele', 51103, '-type', '-beamUniform', -15.1, 0)
    ops.eleLoad('-ele', 51203, '-type', '-beamUniform', -15.1, 0)
    ops.eleLoad('-ele', 51303, '-type', '-beamUniform', -15.1, 0)
    ops.eleLoad('-ele', 51403, '-type', '-beamUniform', -15.1, 0)
    ops.eleLoad('-ele', 51503, '-type', '-beamUniform', -15.1, 0)
    # Perform gravity analysis
    ops.system('UmfPack')
    ops.numberer('RCM')
    ops.constraints('Transformation')
    ops.test('NormDispIncr', 1e-06, 6)
    ops.integrator('LoadControl', 1)
    ops.algorithm('Linear')
    ops.analysis('Static')
    ops.analyze(1)
    print('Gravity analysis complete..')
    ops.loadConst('-time', 0.0)


def modal(num_eigen=3):

    print('Wait a second... Ready to go for modal analysis...')
    output_directory = Path(__file__).parent / 'Modal'
    if not Path.exists(output_directory):
        Path.mkdir(output_directory)
    report_file_path = (output_directory / 'ModalProperties.txt').as_posix()
    ops.eigen(num_eigen)
    ops.modalProperties('-print', '-file', report_file_path, '-unorm')
    print('Modal Analysis Done')


def _solution_algorithm(ok, currentTolerance):

    if ok != 0:
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('KrylovNewton')
        ok = ops.analyze(1)
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Newton', '-initial')
    if ok != 0:
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('NewtonLineSearch', 0.1)
        ok = ops.analyze(1)
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Newton')
    if ok != 0:
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Broyden', 50)
        ok = ops.analyze(1)
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Newton')
    if ok != 0:
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('ModifiedNewton', 50)
        ok = ops.analyze(1)
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Newton')
    if ok != 0:
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('BFGS')
        ok = ops.analyze(1)
        ops.test('NormDispIncr', currentTolerance, 10)
        ops.algorithm('Newton')
    return ok


def pushover_x():

    output_directory = (Path(__file__).parent / 'PUSH_X')
    if not Path.exists(folder_name):
        Path.mkdir(folder_name)
    disp_file_path = (folder_name / 'nodeD.out').as_posix()
    reaction_file_path = (folder_name / 'nodeR.out').as_posix()
    # LATERAL-LOAD distribution for static pushover analysis
    # Calculate distribution of lateral load based on mass/weight distributions along building height
    # Fj = WjHj/sum(WiHi) * Weight at each floor j
    ops.timeSeries('Linear', 200)
    ops.pattern('Plain', 200, 200)
    ops.load(100001, 680.805510, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(200002, 1362.757033, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(300003, 2045.290490, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(400004, 2724.800991, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.load(500005, 2516.777977, 0.0, 0.0, 0.0, 0.0, 0.0)
    ops.recorder('Node', '-file', disp_file_path,
                 '-node', 500005, '-dof', 1, 'disp')
    ops.recorder('Node', '-file', reaction_file_path, '-node', 7001, 7002, 7003, 7004, 7005, 7006,
                 7007, 7008, 7009, 7010, 7011, 7012, 7013, 7014, 7015, 7016, 7017, 7018, '-dof', 1, 'reaction')
    testTolerance0 = 1.0e-5
    testTolerance1 = 1.0e-4
    testTolerance2 = 1.0e-3
    testTolerance3 = 1.0e-2
    # Perform static horizontal analysis
    ops.system('UmfPack')
    ops.numberer('RCM')
    ops.constraints('Penalty', 10e9, 10e9)
    ops.test('NormDispIncr', testTolerance0, 30, 0)
    IDctrlNode = 500005
    IDctrlDOF = 1
    Dmax = 0.840
    Dincr = 0.001
    ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    ops.algorithm('Newton')
    ops.analysis('Static')
    currentTolerance = testTolerance0
    currentTime = 0
    ok = 0
    avect = 0
    currentDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
    currentDrift = 100*currentDisp/14.000
    Tagum = 0
    Tagum1 = 0
    Tagum2 = 0
    maxavect = 0
    while ok == 0 and Tagum == 0:
        ops.test('NormDispIncr', currentTolerance, 10, 0)
        ok = ops.analyze(1)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance0
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance1
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance2
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance3
            ok = _solution_algorithm(ok, currentTolerance)
        if ok == 0:
            currentDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
            avect = ops.eleResponse(17001, 'forces')[0] + ops.eleResponse(17002, 'forces')[0] + ops.eleResponse(17003, 'forces')[0] + ops.eleResponse(17004, 'forces')[0] + ops.eleResponse(17005, 'forces')[0] + ops.eleResponse(17006, 'forces')[0] + ops.eleResponse(17007, 'forces')[0] + ops.eleResponse(17008, 'forces')[0] + ops.eleResponse(17009, 'forces')[
                0] + ops.eleResponse(17010, 'forces')[0] + ops.eleResponse(17011, 'forces')[0] + ops.eleResponse(17012, 'forces')[0] + ops.eleResponse(17013, 'forces')[0] + ops.eleResponse(17014, 'forces')[0] + ops.eleResponse(17015, 'forces')[0] + ops.eleResponse(17016, 'forces')[0] + ops.eleResponse(17017, 'forces')[0] + ops.eleResponse(17018, 'forces')[0]
            if avect < 0:
                avect = -1*avect
        else:
            return
        if avect < 50000:
            pass
        else:
            return
        if avect < 100:
            avect = 0
        if avect >= maxavect:
            maxavect = avect + 0
        else:
            if avect >= 0.20*maxavect:
                pass
            else:
                Tagum1 = 1
        if currentDisp < Dmax:
            pass
        else:
            Tagum2 = 1
        Tagum = Tagum1 + Tagum2
    ops.wipe()
    print('Pushover X done...')


def pushover_y():

    output_directory = (Path(__file__).parent / 'PUSH_Y')
    if not Path.exists(folder_name):
        Path.mkdir(folder_name)
    disp_file_path = (folder_name / 'nodeD.out').as_posix()
    reaction_file_path = (folder_name / 'nodeR.out').as_posix()
    # LATERAL-LOAD distribution for static pushover analysis
    # Calculate distribution of lateral load based on mass/weight distributions along building height
    # Fj = WjHj/sum(WiHi) * Weight at each floor j
    ops.timeSeries('Linear', 200)
    ops.pattern('Plain', 200, 200)
    ops.load(100001, 0.0, 680.805510, 0.0, 0.0, 0.0, 0.0)
    ops.load(200002, 0.0, 1362.757033, 0.0, 0.0, 0.0, 0.0)
    ops.load(300003, 0.0, 2045.290490, 0.0, 0.0, 0.0, 0.0)
    ops.load(400004, 0.0, 2724.800991, 0.0, 0.0, 0.0, 0.0)
    ops.load(500005, 0.0, 2516.777977, 0.0, 0.0, 0.0, 0.0)
    ops.recorder('Node', '-file', disp_file_path,
                 '-node', 500005, '-dof', 2, 'disp')
    ops.recorder('Node', '-file', reaction_file_path, '-node', 7001, 7002, 7003, 7004, 7005, 7006,
                 7007, 7008, 7009, 7010, 7011, 7012, 7013, 7014, 7015, 7016, 7017, 7018, '-dof', 2, 'reaction')
    testTolerance0 = 1.0e-5
    testTolerance1 = 1.0e-4
    testTolerance2 = 1.0e-3
    testTolerance3 = 1.0e-2
    # Perform static horizontal analysis
    ops.system('UmfPack')
    ops.numberer('RCM')
    ops.constraints('Penalty', 10e9, 10e9)
    ops.test('NormDispIncr', testTolerance0, 30, 0)
    IDctrlNode = 500005
    IDctrlDOF = 2
    Dmax = 0.840
    Dincr = 0.001
    ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
    ops.algorithm('Newton')
    ops.analysis('Static')
    currentTolerance = testTolerance0
    currentTime = 0
    ok = 0
    avect = 0
    currentDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
    currentDrift = 100*currentDisp/14.000
    Tagum = 0
    Tagum1 = 0
    Tagum2 = 0
    maxavect = 0
    while ok == 0 and Tagum == 0:
        ops.test('NormDispIncr', currentTolerance, 10, 0)
        ok = ops.analyze(1)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance0
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance1
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance2
            ok = _solution_algorithm(ok, currentTolerance)
        if ok != 0:
            ops.integrator('DisplacementControl', IDctrlNode, IDctrlDOF, Dincr)
            currentTolerance = testTolerance3
            ok = _solution_algorithm(ok, currentTolerance)
        if ok == 0:
            currentDisp = ops.nodeDisp(IDctrlNode, IDctrlDOF)
            avect = ops.eleResponse(17001, 'forces')[1] + ops.eleResponse(17002, 'forces')[1] + ops.eleResponse(17003, 'forces')[1] + ops.eleResponse(17004, 'forces')[1] + ops.eleResponse(17005, 'forces')[1] + ops.eleResponse(17006, 'forces')[1] + ops.eleResponse(17007, 'forces')[1] + ops.eleResponse(17008, 'forces')[1] + ops.eleResponse(17009, 'forces')[
                1] + ops.eleResponse(17010, 'forces')[1] + ops.eleResponse(17011, 'forces')[1] + ops.eleResponse(17012, 'forces')[1] + ops.eleResponse(17013, 'forces')[1] + ops.eleResponse(17014, 'forces')[1] + ops.eleResponse(17015, 'forces')[1] + ops.eleResponse(17016, 'forces')[1] + ops.eleResponse(17017, 'forces')[1] + ops.eleResponse(17018, 'forces')[1]
            if avect < 0:
                avect = -1*avect
        else:
            return
        if avect < 50000:
            pass
        else:
            return
        if avect < 100:
            avect = 0
        if avect >= maxavect:
            maxavect = avect + 0
        else:
            if avect >= 0.20*maxavect:
                pass
            else:
                Tagum1 = 1
        if currentDisp < Dmax:
            pass
        else:
            Tagum2 = 1
        Tagum = Tagum1 + Tagum2
    ops.wipe()
    print('Pushover Y done...')
