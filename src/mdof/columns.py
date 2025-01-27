import openseespy.opensees as ops


def add_columns() -> None:
    """Add components of all columns to ops domain (plastic hinges, column elements and nodes)
    """
    # Create elastic column element nodes
    ops.node(170003, 7.9, 0.0, 0.0)
    ops.node(121003, 7.9, 0.0, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3, 170003, 121003, 0.12, 32283809.27225804, 13451587.19677418, 0.00194385, 0.00176, 0.00099, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20003, 85.40101624, 0.00084597, 102.51350931, 0.04715903, 10.25135093, 0.12686611, -85.40101624, -0.00084597, -102.51350931, -0.04715903, -10.25135093, -0.12686611, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10003, 93.81043472, 0.00068161, 112.60799106, 0.05223729, 11.26079911, 0.15223729, -93.81043472, -0.00068161, -112.60799106, -0.05223729, -11.26079911, -0.15223729, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20003, 3, 0.0, 168.96436239, 0.01691937, 168.96436239, 0.05075812, 118.27505367, -2125.82586108, 0.05, 2, 0, 70003, 21003, 2, 3)
    ops.uniaxialMaterial('LimitState', 40003, 42.2410906, 0.00010991, 126.72327179, 0.00032972, 422.41090598, 0.00109908, -42.2410906, -0.00010991, -126.72327179, -0.00032972, -422.41090598, -0.00109908, 0.4, 0.3, 0.003, 0.0, 0.0, 20003, 2)
    ops.limitCurve('ThreePoint', 10003, 3, 0.0, 194.19015381, 0.0136321, 194.19015381, 0.04089631, 135.93310767, -3086.11422507, 0.05, 2, 0, 70003, 21003, 1, 3)
    ops.uniaxialMaterial('LimitState', 30003, 48.54753845, 0.00012632, 145.64261536, 0.00037895, 485.47538452, 0.00126317, -48.54753845, -0.00012632, -145.64261536, -0.00037895, -485.47538452, -0.00126317, 0.4, 0.3, 0.003, 0.0, 0.0, 10003, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3, 99999, 'P', 40003, 'Vy', 30003, 'Vz', 20003, 'My', 10003, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170003, 70003, 170003, 3, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121003, 121003, 21003, 3, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170004, 12.9, 0.0, 0.0)
    ops.node(121004, 12.9, 0.0, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4, 170004, 121004, 0.075, 33525914.22556178, 13969130.92731741, 0.00077515, 0.00061875, 0.00042969, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20004, 34.4389826, 0.00106529, 41.19873084, 0.01613527, 4.11987308, 0.06537311, -34.4389826, -0.00106529, -41.19873084, -0.01613527, -4.11987308, -0.06537311, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10004, 39.55631905, 0.00089362, 47.3205077, 0.01689822, 4.73205077, 0.07369022, -39.55631905, -0.00089362, -47.3205077, -0.01689822, -4.73205077, -0.07369022, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20004, 4, 0.0, 65.57513951, 0.02130581, 65.57513951, 0.06391742, 45.90259766, -480.00473845, 0.05, 2, 0, 70004, 21004, 2, 3)
    ops.uniaxialMaterial('LimitState', 40004, 16.39378488, 6.572e-05, 49.18135463, 0.00019716, 163.93784878, 0.0006572, -16.39378488, -6.572e-05, -49.18135463, -0.00019716, -163.93784878, -0.0006572, 0.4, 0.3, 0.003, 0.0, 0.0, 20004, 2)
    ops.limitCurve('ThreePoint', 10004, 4, 0.0, 79.13939693, 0.01787232, 79.13939693, 0.05361695, 55.39757785, -555.24853556, 0.05, 2, 0, 70004, 21004, 1, 3)
    ops.uniaxialMaterial('LimitState', 30004, 19.78484923, 7.931e-05, 59.35454769, 0.00023794, 197.84849232, 0.00079314, -19.78484923, -7.931e-05, -59.35454769, -0.00023794, -197.84849232, -0.00079314, 0.4, 0.3, 0.003, 0.0, 0.0, 10004, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4, 99999, 'P', 40004, 'Vy', 30004, 'Vz', 20004, 'My', 10004, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170004, 70004, 170004, 4, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121004, 121004, 21004, 4, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170005, 0.0, 4.05, 0.0)
    ops.node(121005, 0.0, 4.05, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 5, 170005, 121005, 0.075, 30053306.53512759, 12522211.05630316, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20005, 41.32341548, 0.00081297, 49.78541812, 0.0193235, 4.97854181, 0.06875426, -41.32341548, -0.00081297, -49.78541812, -0.0193235, -4.97854181, -0.06875426, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10005, 36.24380275, 0.0009538, 43.66562767, 0.01838338, 4.36656277, 0.06123912, -36.24380275, -0.0009538, -43.66562767, -0.01838338, -4.36656277, -0.06123912, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20005, 5, 0.0, 76.56475313, 0.0162593, 76.56475313, 0.04877791, 53.59532719, -603.14832848, 0.05, 2, 0, 70005, 21005, 2, 3)
    ops.uniaxialMaterial('LimitState', 40005, 19.14118828, 8.56e-05, 57.42356485, 0.0002568, 191.41188282, 0.000856, -19.14118828, -8.56e-05, -57.42356485, -0.0002568, -191.41188282, -0.000856, 0.4, 0.3, 0.003, 0.0, 0.0, 20005, 2)
    ops.limitCurve('ThreePoint', 10005, 5, 0.0, 64.6208985, 0.01907607, 64.6208985, 0.05722822, 45.23462895, -530.74242348, 0.05, 2, 0, 70005, 21005, 1, 3)
    ops.uniaxialMaterial('LimitState', 30005, 16.15522462, 7.225e-05, 48.46567387, 0.00021674, 161.55224625, 0.00072247, -16.15522462, -7.225e-05, -48.46567387, -0.00021674, -161.55224625, -0.00072247, 0.4, 0.3, 0.003, 0.0, 0.0, 10005, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 5, 99999, 'P', 40005, 'Vy', 30005, 'Vz', 20005, 'My', 10005, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170005, 70005, 170005, 5, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121005, 121005, 21005, 5, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170006, 2.9, 4.05, 0.0)
    ops.node(121006, 2.9, 4.05, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 6, 170006, 121006, 0.1575, 31646818.44444759, 13186174.35185316, 0.00337604, 0.00176859, 0.00292359, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20006, 148.72767369, 0.00062532, 178.90825146, 0.05002074, 17.89082515, 0.13945653, -148.72767369, -0.00062532, -178.90825146, -0.05002074, -17.89082515, -0.13945653, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10006, 144.48859424, 0.00073545, 173.80895639, 0.04579333, 17.38089564, 0.11770961, -144.48859424, -0.00073545, -173.80895639, -0.04579333, -17.38089564, -0.11770961, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20006, 6, 0.0, 203.69543931, 0.01250645, 203.69543931, 0.03751934, 142.58680752, -2367.59435865, 0.05, 2, 0, 70006, 21006, 2, 3)
    ops.uniaxialMaterial('LimitState', 40006, 50.92385983, 0.00010298, 152.77157948, 0.00030895, 509.23859827, 0.00102984, -50.92385983, -0.00010298, -152.77157948, -0.00030895, -509.23859827, -0.00102984, 0.4, 0.3, 0.003, 0.0, 0.0, 20006, 2)
    ops.limitCurve('ThreePoint', 10006, 6, 0.0, 184.6191694, 0.01470903, 184.6191694, 0.0441271, 129.23341858, -1784.183792, 0.05, 2, 0, 70006, 21006, 1, 3)
    ops.uniaxialMaterial('LimitState', 30006, 46.15479235, 9.334e-05, 138.46437705, 0.00028002, 461.54792349, 0.0009334, -46.15479235, -9.334e-05, -138.46437705, -0.00028002, -461.54792349, -0.0009334, 0.4, 0.3, 0.003, 0.0, 0.0, 10006, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 6, 99999, 'P', 40006, 'Vy', 30006, 'Vz', 20006, 'My', 10006, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170006, 70006, 170006, 6, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121006, 121006, 21006, 6, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170007, 7.9, 4.05, 0.0)
    ops.node(121007, 7.9, 4.05, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 7, 170007, 121007, 0.175, 32227716.50171055, 13428215.20904606, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20007, 187.62761862, 0.00058255, 225.37475599, 0.05137299, 22.5374756, 0.14223297, -187.62761862, -0.00058255, -225.37475599, -0.05137299, -22.5374756, -0.14223297, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10007, 168.00844617, 0.00073328, 201.80857614, 0.04536073, 20.18085761, 0.11221184, -168.00844617, -0.00073328, -201.80857614, -0.04536073, -20.18085761, -0.11221184, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20007, 7, 0.0, 216.76513531, 0.011651, 216.76513531, 0.034953, 151.73559472, -2252.04465621, 0.05, 2, 0, 70007, 21007, 2, 3)
    ops.uniaxialMaterial('LimitState', 40007, 54.19128383, 9.686e-05, 162.57385148, 0.00029057, 541.91283827, 0.00096855, -54.19128383, -9.686e-05, -162.57385148, -0.00029057, -541.91283827, -0.00096855, 0.4, 0.3, 0.003, 0.0, 0.0, 20007, 2)
    ops.limitCurve('ThreePoint', 10007, 7, 0.0, 191.81552557, 0.01466566, 191.81552557, 0.04399698, 134.2708679, -1552.73228445, 0.05, 2, 0, 70007, 21007, 1, 3)
    ops.uniaxialMaterial('LimitState', 30007, 47.95388139, 8.571e-05, 143.86164418, 0.00025712, 479.53881392, 0.00085707, -47.95388139, -8.571e-05, -143.86164418, -0.00025712, -479.53881392, -0.00085707, 0.4, 0.3, 0.003, 0.0, 0.0, 10007, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 7, 99999, 'P', 40007, 'Vy', 30007, 'Vz', 20007, 'My', 10007, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170007, 70007, 170007, 7, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121007, 121007, 21007, 7, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170008, 12.9, 4.05, 0.0)
    ops.node(121008, 12.9, 4.05, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 8, 170008, 121008, 0.12, 27621387.81201945, 11508911.58834144, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20008, 87.83777177, 0.00067472, 106.45952454, 0.03935576, 10.64595245, 0.1031185, -87.83777177, -0.00067472, -106.45952454, -0.03935576, -10.64595245, -0.1031185, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10008, 80.89934512, 0.0008358, 98.05013997, 0.03581646, 9.805014, 0.08604811, -80.89934512, -0.0008358, -98.05013997, -0.03581646, -9.805014, -0.08604811, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20008, 8, 0.0, 147.3055936, 0.01349445, 147.3055936, 0.04048334, 103.11391552, -2013.16225634, 0.05, 2, 0, 70008, 21008, 2, 3)
    ops.uniaxialMaterial('LimitState', 40008, 36.8263984, 0.00011199, 110.4791952, 0.00033598, 368.26398401, 0.00111994, -36.8263984, -0.00011199, -110.4791952, -0.00033598, -368.26398401, -0.00111994, 0.4, 0.3, 0.003, 0.0, 0.0, 20008, 2)
    ops.limitCurve('ThreePoint', 10008, 8, 0.0, 129.33997298, 0.01671594, 129.33997298, 0.05014781, 90.53798109, -1444.45888874, 0.05, 2, 0, 70008, 21008, 1, 3)
    ops.uniaxialMaterial('LimitState', 30008, 32.33499325, 9.833e-05, 97.00497974, 0.000295, 323.34993245, 0.00098335, -32.33499325, -9.833e-05, -97.00497974, -0.000295, -323.34993245, -0.00098335, 0.4, 0.3, 0.003, 0.0, 0.0, 10008, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 8, 99999, 'P', 40008, 'Vy', 30008, 'Vz', 20008, 'My', 10008, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170008, 70008, 170008, 8, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121008, 121008, 21008, 8, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170009, 0.0, 8.1, 0.0)
    ops.node(121009, 0.0, 8.1, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 9, 170009, 121009, 0.075, 28062364.70407342, 11692651.96003059, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20009, 38.40832067, 0.00085635, 46.50373778, 0.02339952, 4.65037378, 0.07212358, -38.40832067, -0.00085635, -46.50373778, -0.02339952, -4.65037378, -0.07212358, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10009, 33.66625023, 0.00101236, 40.76216938, 0.02223907, 4.07621694, 0.06448213, -33.66625023, -0.00101236, -40.76216938, -0.02223907, -4.07621694, -0.06448213, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20009, 9, 0.0, 78.01332092, 0.0171269, 78.01332092, 0.0513807, 54.60932465, -782.09939089, 0.05, 2, 0, 70009, 21009, 2, 3)
    ops.uniaxialMaterial('LimitState', 40009, 19.50333023, 9.341e-05, 58.50999069, 0.00028022, 195.03330231, 0.00093408, -19.50333023, -9.341e-05, -58.50999069, -0.00028022, -195.03330231, -0.00093408, 0.4, 0.3, 0.003, 0.0, 0.0, 20009, 2)
    ops.limitCurve('ThreePoint', 10009, 9, 0.0, 73.11585925, 0.02024725, 73.11585925, 0.06074176, 51.18110147, -658.08462847, 0.05, 2, 0, 70009, 21009, 1, 3)
    ops.uniaxialMaterial('LimitState', 30009, 18.27896481, 8.754e-05, 54.83689444, 0.00026263, 182.78964812, 0.00087544, -18.27896481, -8.754e-05, -54.83689444, -0.00026263, -182.78964812, -0.00087544, 0.4, 0.3, 0.003, 0.0, 0.0, 10009, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 9, 99999, 'P', 40009, 'Vy', 30009, 'Vz', 20009, 'My', 10009, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170009, 70009, 170009, 9, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121009, 121009, 21009, 9, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170010, 2.9, 8.1, 0.0)
    ops.node(121010, 2.9, 8.1, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 10, 170010, 121010, 0.12, 33104230.44974995, 13793429.35406248, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20010, 114.67763266, 0.00071389, 137.27064882, 0.05034004, 13.72706488, 0.15034004, -114.67763266, -0.00071389, -137.27064882, -0.05034004, -13.72706488, -0.15034004, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10010, 101.12904426, 0.00089007, 121.05280862, 0.04546981, 12.10528086, 0.12552868, -101.12904426, -0.00089007, -121.05280862, -0.04546981, -12.10528086, -0.12552868, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20010, 10, 0.0, 179.26535897, 0.01427772, 179.26535897, 0.04283316, 125.48575128, -2300.10846203, 0.05, 2, 0, 70010, 21010, 2, 3)
    ops.uniaxialMaterial('LimitState', 40010, 44.81633974, 0.00011372, 134.44901923, 0.00034116, 448.16339743, 0.00113719, -44.81633974, -0.00011372, -134.44901923, -0.00034116, -448.16339743, -0.00113719, 0.4, 0.3, 0.003, 0.0, 0.0, 20010, 2)
    ops.limitCurve('ThreePoint', 10010, 10, 0.0, 158.86299378, 0.01780138, 158.86299378, 0.05340414, 111.20409564, -1644.26831254, 0.05, 2, 0, 70010, 21010, 1, 3)
    ops.uniaxialMaterial('LimitState', 30010, 39.71574844, 0.00010078, 119.14724533, 0.00030233, 397.15748444, 0.00100776, -39.71574844, -0.00010078, -119.14724533, -0.00030233, -397.15748444, -0.00100776, 0.4, 0.3, 0.003, 0.0, 0.0, 10010, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 10, 99999, 'P', 40010, 'Vy', 30010, 'Vz', 20010, 'My', 10010, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170010, 70010, 170010, 10, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121010, 121010, 21010, 10, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170011, 7.9, 8.1, 0.0)
    ops.node(121011, 7.9, 8.1, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 11, 170011, 121011, 0.175, 33297663.2399203, 13874026.34996679, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20011, 192.8420402, 0.0005962, 230.88975318, 0.05172654, 23.08897532, 0.14432608, -192.8420402, -0.0005962, -230.88975318, -0.05172654, -23.08897532, -0.14432608, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10011, 171.47747153, 0.00075526, 205.3099575, 0.04568137, 20.53099575, 0.11381237, -171.47747153, -0.00075526, -205.3099575, -0.04568137, -20.53099575, -0.11381237, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20011, 11, 0.0, 242.97679179, 0.01192398, 242.97679179, 0.03577194, 170.08375425, -2912.9558558, 0.05, 2, 0, 70011, 21011, 2, 3)
    ops.uniaxialMaterial('LimitState', 40011, 60.74419795, 0.00010508, 182.23259384, 0.00031524, 607.44197947, 0.00105078, -60.74419795, -0.00010508, -182.23259384, -0.00031524, -607.44197947, -0.00105078, 0.4, 0.3, 0.003, 0.0, 0.0, 20011, 2)
    ops.limitCurve('ThreePoint', 10011, 11, 0.0, 211.96926784, 0.01510518, 211.96926784, 0.04531553, 148.37848749, -1933.00824312, 0.05, 2, 0, 70011, 21011, 1, 3)
    ops.uniaxialMaterial('LimitState', 30011, 52.99231696, 9.167e-05, 158.97695088, 0.00027501, 529.9231696, 0.00091669, -52.99231696, -9.167e-05, -158.97695088, -0.00027501, -529.9231696, -0.00091669, 0.4, 0.3, 0.003, 0.0, 0.0, 10011, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 11, 99999, 'P', 40011, 'Vy', 30011, 'Vz', 20011, 'My', 10011, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170011, 70011, 170011, 11, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121011, 121011, 21011, 11, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170012, 12.9, 8.1, 0.0)
    ops.node(121012, 12.9, 8.1, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 12, 170012, 121012, 0.12, 33138508.77280142, 13807711.98866726, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20012, 86.090404, 0.00059084, 103.10451338, 0.03267219, 10.31045134, 0.10642877, -86.090404, -0.00059084, -103.10451338, -0.03267219, -10.31045134, -0.10642877, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10012, 80.50960269, 0.00071143, 96.42077424, 0.02972375, 9.64207742, 0.08782846, -80.50960269, -0.00071143, -96.42077424, -0.02972375, -9.64207742, -0.08782846, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20012, 12, 0.0, 145.56045023, 0.01181683, 145.56045023, 0.0354505, 101.89231516, -1325.53293836, 0.05, 2, 0, 70012, 21012, 2, 3)
    ops.uniaxialMaterial('LimitState', 40012, 36.39011256, 9.224e-05, 109.17033768, 0.00027673, 363.90112558, 0.00092242, -36.39011256, -9.224e-05, -109.17033768, -0.00027673, -363.90112558, -0.00092242, 0.4, 0.3, 0.003, 0.0, 0.0, 20012, 2)
    ops.limitCurve('ThreePoint', 10012, 12, 0.0, 133.13225216, 0.01422858, 133.13225216, 0.04268573, 93.19257651, -1002.40194268, 0.05, 2, 0, 70012, 21012, 1, 3)
    ops.uniaxialMaterial('LimitState', 30012, 33.28306304, 8.437e-05, 99.84918912, 0.0002531, 332.8306304, 0.00084366, -33.28306304, -8.437e-05, -99.84918912, -0.0002531, -332.8306304, -0.00084366, 0.4, 0.3, 0.003, 0.0, 0.0, 10012, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 12, 99999, 'P', 40012, 'Vy', 30012, 'Vz', 20012, 'My', 10012, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170012, 70012, 170012, 12, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121012, 121012, 21012, 12, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170013, 0.0, 12.15, 0.0)
    ops.node(121013, 0.0, 12.15, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 13, 170013, 121013, 0.075, 27417666.48591228, 11424027.70246345, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20013, 36.46359264, 0.00080243, 44.18108907, 0.0258023, 4.41810891, 0.07329531, -36.46359264, -0.00080243, -44.18108907, -0.0258023, -4.41810891, -0.07329531, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10013, 31.94329374, 0.00094535, 38.70407176, 0.02448529, 3.87040718, 0.06566104, -31.94329374, -0.00094535, -38.70407176, -0.02448529, -3.87040718, -0.06566104, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20013, 13, 0.0, 77.4574544, 0.01604865, 77.4574544, 0.04814596, 54.22021808, -805.10259822, 0.05, 2, 0, 70013, 21013, 2, 3)
    ops.uniaxialMaterial('LimitState', 40013, 19.3643636, 9.492e-05, 58.0930908, 0.00028477, 193.643636, 0.00094923, -19.3643636, -9.492e-05, -58.0930908, -0.00028477, -193.643636, -0.00094923, 0.4, 0.3, 0.003, 0.0, 0.0, 20013, 2)
    ops.limitCurve('ThreePoint', 10013, 13, 0.0, 72.41590219, 0.01890696, 72.41590219, 0.05672089, 50.69113154, -675.65693907, 0.05, 2, 0, 70013, 21013, 1, 3)
    ops.uniaxialMaterial('LimitState', 30013, 18.10397555, 8.874e-05, 54.31192665, 0.00026623, 181.03975548, 0.00088745, -18.10397555, -8.874e-05, -54.31192665, -0.00026623, -181.03975548, -0.00088745, 0.4, 0.3, 0.003, 0.0, 0.0, 10013, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 13, 99999, 'P', 40013, 'Vy', 30013, 'Vz', 20013, 'My', 10013, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170013, 70013, 170013, 13, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121013, 121013, 21013, 13, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170014, 2.9, 12.15, 0.0)
    ops.node(121014, 2.9, 12.15, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 14, 170014, 121014, 0.12, 28033971.61025435, 11680821.50427265, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20014, 106.12043821, 0.00074227, 128.41427368, 0.05695175, 12.84142737, 0.14641503, -106.12043821, -0.00074227, -128.41427368, -0.05695175, -12.84142737, -0.14641503, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10014, 91.56346791, 0.00094636, 110.79916768, 0.05143998, 11.07991677, 0.12080957, -91.56346791, -0.00094636, -110.79916768, -0.05143998, -11.07991677, -0.12080957, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20014, 14, 0.0, 173.66473159, 0.01484543, 173.66473159, 0.04453628, 121.56531211, -2787.96004095, 0.05, 2, 0, 70014, 21014, 2, 3)
    ops.uniaxialMaterial('LimitState', 40014, 43.4161829, 0.00013009, 130.24854869, 0.00039027, 434.16182896, 0.00130091, -43.4161829, -0.00013009, -130.24854869, -0.00039027, -434.16182896, -0.00130091, 0.4, 0.3, 0.003, 0.0, 0.0, 20014, 2)
    ops.limitCurve('ThreePoint', 10014, 14, 0.0, 149.92958272, 0.01892727, 149.92958272, 0.05678182, 104.95070791, -1951.94719695, 0.05, 2, 0, 70014, 21014, 1, 3)
    ops.uniaxialMaterial('LimitState', 30014, 37.48239568, 0.00011231, 112.44718704, 0.00033693, 374.82395681, 0.00112311, -37.48239568, -0.00011231, -112.44718704, -0.00033693, -374.82395681, -0.00112311, 0.4, 0.3, 0.003, 0.0, 0.0, 10014, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 14, 99999, 'P', 40014, 'Vy', 30014, 'Vz', 20014, 'My', 10014, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170014, 70014, 170014, 14, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121014, 121014, 21014, 14, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170015, 7.9, 12.15, 0.0)
    ops.node(121015, 7.9, 12.15, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 15, 170015, 121015, 0.175, 35440713.12957535, 14766963.80398973, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20015, 190.38426983, 0.00058767, 226.21261461, 0.05169135, 22.62126146, 0.14720195, -190.38426983, -0.00058767, -226.21261461, -0.05169135, -22.62126146, -0.14720195, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10015, 166.02222911, 0.0007482, 197.26589053, 0.04565088, 19.72658905, 0.11592373, -166.02222911, -0.0007482, -197.26589053, -0.04565088, -19.72658905, -0.11592373, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20015, 15, 0.0, 264.23431626, 0.0117534, 264.23431626, 0.0352602, 184.96402138, -3229.51690544, 0.05, 2, 0, 70015, 21015, 2, 3)
    ops.uniaxialMaterial('LimitState', 40015, 66.05857906, 0.00010736, 198.17573719, 0.00032209, 660.58579064, 0.00107362, -66.05857906, -0.00010736, -198.17573719, -0.00032209, -660.58579064, -0.00107362, 0.4, 0.3, 0.003, 0.0, 0.0, 20015, 2)
    ops.limitCurve('ThreePoint', 10015, 15, 0.0, 230.57065209, 0.01496397, 230.57065209, 0.04489192, 161.39945646, -2112.86510359, 0.05, 2, 0, 70015, 21015, 1, 3)
    ops.uniaxialMaterial('LimitState', 30015, 57.64266302, 9.368e-05, 172.92798907, 0.00028105, 576.42663022, 0.00093684, -57.64266302, -9.368e-05, -172.92798907, -0.00028105, -576.42663022, -0.00093684, 0.4, 0.3, 0.003, 0.0, 0.0, 10015, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 15, 99999, 'P', 40015, 'Vy', 30015, 'Vz', 20015, 'My', 10015, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170015, 70015, 170015, 15, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121015, 121015, 21015, 15, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170016, 12.9, 12.15, 0.0)
    ops.node(121016, 12.9, 12.15, 3.225)
    # Create elastic column element
    ops.element('elasticBeamColumn', 16, 170016, 121016, 0.12, 30384791.09508305, 12660329.62295127, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20016, 82.65120913, 0.00061212, 99.71254908, 0.0366652, 9.97125491, 0.10623247, -82.65120913, -0.00061212, -99.71254908, -0.0366652, -9.97125491, -0.10623247, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10016, 75.05086978, 0.00075164, 90.54330378, 0.03335574, 9.05433038, 0.08816015, -75.05086978, -0.00075164, -90.54330378, -0.03335574, -9.05433038, -0.08816015, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20016, 16, 0.0, 140.33657327, 0.01224235, 140.33657327, 0.03672706, 98.23560129, -1474.86705762, 0.05, 2, 0, 70016, 21016, 2, 3)
    ops.uniaxialMaterial('LimitState', 40016, 35.08414332, 9.699e-05, 105.25242995, 0.00029097, 350.84143318, 0.00096992, -35.08414332, -9.699e-05, -105.25242995, -0.00029097, -350.84143318, -0.00096992, 0.4, 0.3, 0.003, 0.0, 0.0, 20016, 2)
    ops.limitCurve('ThreePoint', 10016, 16, 0.0, 126.60188868, 0.01503277, 126.60188868, 0.04509831, 88.62132208, -1099.44158681, 0.05, 2, 0, 70016, 21016, 1, 3)
    ops.uniaxialMaterial('LimitState', 30016, 31.65047217, 8.75e-05, 94.95141651, 0.0002625, 316.5047217, 0.00087499, -31.65047217, -8.75e-05, -94.95141651, -0.0002625, -316.5047217, -0.00087499, 0.4, 0.3, 0.003, 0.0, 0.0, 10016, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 16, 99999, 'P', 40016, 'Vy', 30016, 'Vz', 20016, 'My', 10016, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170016, 70016, 170016, 16, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121016, 121016, 21016, 16, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170017, 0.0, 16.2, 0.0)
    ops.node(121017, 0.0, 16.2, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 17, 170017, 121017, 0.0625, 30281459.0337965, 12617274.59741521, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20017, 22.58527042, 0.00094344, 27.30384332, 0.01898492, 2.73038433, 0.07487122, -22.58527042, -0.00094344, -27.30384332, -0.01898492, -2.73038433, -0.07487122, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10017, 22.58527042, 0.00094344, 27.30384332, 0.01898492, 2.73038433, 0.07487122, -22.58527042, -0.00094344, -27.30384332, -0.01898492, -2.73038433, -0.07487122, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20017, 17, 0.0, 49.4120637, 0.01886888, 49.4120637, 0.05660663, 34.58844459, -505.5992413, 0.05, 2, 0, 70017, 21017, 2, 3)
    ops.uniaxialMaterial('LimitState', 40017, 12.35301592, 6.579e-05, 37.05904777, 0.00019738, 123.53015925, 0.00065793, -12.35301592, -6.579e-05, -37.05904777, -0.00019738, -123.53015925, -0.00065793, 0.4, 0.3, 0.003, 0.0, 0.0, 20017, 2)
    ops.limitCurve('ThreePoint', 10017, 17, 0.0, 49.4120637, 0.01886888, 49.4120637, 0.05660663, 34.58844459, -505.5992413, 0.05, 2, 0, 70017, 21017, 1, 3)
    ops.uniaxialMaterial('LimitState', 30017, 12.35301592, 6.579e-05, 37.05904777, 0.00019738, 123.53015925, 0.00065793, -12.35301592, -6.579e-05, -37.05904777, -0.00019738, -123.53015925, -0.00065793, 0.4, 0.3, 0.003, 0.0, 0.0, 10017, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 17, 99999, 'P', 40017, 'Vy', 30017, 'Vz', 20017, 'My', 10017, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170017, 70017, 170017, 17, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121017, 121017, 21017, 17, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170018, 2.9, 16.2, 0.0)
    ops.node(121018, 2.9, 16.2, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 18, 170018, 121018, 0.105, 26846510.47027726, 11186046.02928219, 0.00152551, 0.00117906, 0.00086625, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20018, 64.30069283, 0.00080899, 78.04547445, 0.04702433, 7.80454744, 0.125441, -64.30069283, -0.00080899, -78.04547445, -0.04702433, -7.80454744, -0.125441, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10018, 62.47014338, 0.00071577, 75.82363058, 0.04968957, 7.58236306, 0.13966667, -62.47014338, -0.00071577, -75.82363058, -0.04968957, -7.58236306, -0.13966667, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20018, 18, 0.0, 125.16303695, 0.01617974, 125.16303695, 0.04853923, 87.61412586, -1769.97188034, 0.05, 2, 0, 70018, 21018, 2, 3)
    ops.uniaxialMaterial('LimitState', 40018, 31.29075924, 0.00011189, 93.87227771, 0.00033568, 312.90759237, 0.00111892, -31.29075924, -0.00011189, -93.87227771, -0.00033568, -312.90759237, -0.00111892, 0.4, 0.3, 0.003, 0.0, 0.0, 20018, 2)
    ops.limitCurve('ThreePoint', 10018, 18, 0.0, 135.56262044, 0.01431531, 135.56262044, 0.04294592, 94.89383431, -2157.43555961, 0.05, 2, 0, 70018, 21018, 1, 3)
    ops.uniaxialMaterial('LimitState', 30018, 33.89065511, 0.00012119, 101.67196533, 0.00036357, 338.9065511, 0.00121189, -33.89065511, -0.00012119, -101.67196533, -0.00036357, -338.9065511, -0.00121189, 0.4, 0.3, 0.003, 0.0, 0.0, 10018, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 18, 99999, 'P', 40018, 'Vy', 30018, 'Vz', 20018, 'My', 10018, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170018, 70018, 170018, 18, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121018, 121018, 21018, 18, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170019, 7.9, 16.2, 0.0)
    ops.node(121019, 7.9, 16.2, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 19, 170019, 121019, 0.14, 30248071.4251516, 12603363.09381317, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20019, 105.68574225, 0.00073919, 127.64562048, 0.05145659, 12.76456205, 0.13008266, -105.68574225, -0.00073919, -127.64562048, -0.05145659, -12.76456205, -0.13008266, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10019, 102.74226918, 0.00066996, 124.0905388, 0.05394852, 12.40905388, 0.14232131, -102.74226918, -0.00066996, -124.0905388, -0.05394852, -12.40905388, -0.14232131, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20019, 19, 0.0, 190.735358, 0.01478373, 190.735358, 0.0443512, 133.5147506, -2798.65634027, 0.05, 2, 0, 70019, 21019, 2, 3)
    ops.uniaxialMaterial('LimitState', 40019, 47.6838395, 0.0001135, 143.0515185, 0.00034051, 476.83839501, 0.00113503, -47.6838395, -0.0001135, -143.0515185, -0.00034051, -476.83839501, -0.00113503, 0.4, 0.3, 0.003, 0.0, 0.0, 20019, 2)
    ops.limitCurve('ThreePoint', 10019, 19, 0.0, 204.15133923, 0.0133991, 204.15133923, 0.04019731, 142.90593746, -3354.34603931, 0.05, 2, 0, 70019, 21019, 1, 3)
    ops.uniaxialMaterial('LimitState', 30019, 51.03783481, 0.00012149, 153.11350442, 0.00036446, 510.37834808, 0.00121486, -51.03783481, -0.00012149, -153.11350442, -0.00036446, -510.37834808, -0.00121486, 0.4, 0.3, 0.003, 0.0, 0.0, 10019, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 19, 99999, 'P', 40019, 'Vy', 30019, 'Vz', 20019, 'My', 10019, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170019, 70019, 170019, 19, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121019, 121019, 21019, 19, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170020, 12.9, 16.2, 0.0)
    ops.node(121020, 12.9, 16.2, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 20, 170020, 121020, 0.09, 28611692.23575707, 11921538.43156545, 0.00114075, 0.0007425, 0.0007425, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 20020, 40.44151142, 0.00082859, 49.03430292, 0.02721607, 4.90343029, 0.0819813, -40.44151142, -0.00082859, -49.03430292, -0.02721607, -4.90343029, -0.0819813, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 10020, 37.75357878, 0.00082859, 45.77525304, 0.02721607, 4.5775253, 0.0819813, -37.75357878, -0.00082859, -45.77525304, -0.02721607, -4.5775253, -0.0819813, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 20020, 20, 0.0, 90.61631553, 0.01657188, 90.61631553, 0.04971565, 63.43142087, -907.75280996, 0.05, 2, 0, 70020, 21020, 2, 3)
    ops.uniaxialMaterial('LimitState', 40020, 22.65407888, 8.868e-05, 67.96223665, 0.00026604, 226.54078882, 0.00088679, -22.65407888, -8.868e-05, -67.96223665, -0.00026604, -226.54078882, -0.00088679, 0.4, 0.3, 0.003, 0.0, 0.0, 20020, 2)
    ops.limitCurve('ThreePoint', 10020, 20, 0.0, 90.61631553, 0.01657188, 90.61631553, 0.04971565, 63.43142087, -907.75280996, 0.05, 2, 0, 70020, 21020, 1, 3)
    ops.uniaxialMaterial('LimitState', 30020, 22.65407888, 8.868e-05, 67.96223665, 0.00026604, 226.54078882, 0.00088679, -22.65407888, -8.868e-05, -67.96223665, -0.00026604, -226.54078882, -0.00088679, 0.4, 0.3, 0.003, 0.0, 0.0, 10020, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 20, 99999, 'P', 40020, 'Vy', 30020, 'Vz', 20020, 'My', 10020, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170020, 70020, 170020, 20, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121020, 121020, 21020, 20, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171003, 7.9, 0.0, 3.75)
    ops.node(122003, 7.9, 0.0, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1003, 171003, 122003, 0.12, 29875441.34994986, 12448100.56247911, 0.00194385, 0.00176, 0.00099, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21003, 47.5165046, 0.00069994, 57.50634316, 0.02813672, 5.75063432, 0.07411274, -47.5165046, -0.00069994, -57.50634316, -0.02813672, -5.75063432, -0.07411274, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11003, 73.549329, 0.00058472, 89.01229136, 0.03074548, 8.90122914, 0.08829559, -73.549329, -0.00058472, -89.01229136, -0.03074548, -8.90122914, -0.08829559, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21003, 1003, 0.0, 119.16824796, 0.01399887, 119.16824796, 0.04199661, 83.41777357, -1303.53197751, 0.05, 2, 0, 71003, 22003, 2, 3)
    ops.uniaxialMaterial('LimitState', 41003, 29.79206199, 6.941e-05, 89.37618597, 0.00020822, 297.9206199, 0.00069406, -29.79206199, -6.941e-05, -89.37618597, -0.00020822, -297.9206199, -0.00069406, 0.4, 0.3, 0.003, 0.0, 0.0, 21003, 2)
    ops.limitCurve('ThreePoint', 11003, 1003, 0.0, 132.60040289, 0.01169449, 132.60040289, 0.03508348, 92.82028202, -1817.05193667, 0.05, 2, 0, 71003, 22003, 1, 3)
    ops.uniaxialMaterial('LimitState', 31003, 33.15010072, 7.723e-05, 99.45030216, 0.00023169, 331.50100722, 0.00077229, -33.15010072, -7.723e-05, -99.45030216, -0.00023169, -331.50100722, -0.00077229, 0.4, 0.3, 0.003, 0.0, 0.0, 11003, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1003, 99999, 'P', 41003, 'Vy', 31003, 'Vz', 21003, 'My', 11003, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171003, 71003, 171003, 1003, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122003, 122003, 22003, 1003, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171004, 12.9, 0.0, 3.75)
    ops.node(122004, 12.9, 0.0, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1004, 171004, 122004, 0.075, 28823615.95871537, 12009839.98279807, 0.00077515, 0.00061875, 0.00042969, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21004, 27.26089434, 0.00077564, 33.07813922, 0.02644611, 3.30781392, 0.08340915, -27.26089434, -0.00077564, -33.07813922, -0.02644611, -3.30781392, -0.08340915, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11004, 30.84827296, 0.00067178, 37.43103417, 0.02801439, 3.74310342, 0.09417551, -30.84827296, -0.00067178, -37.43103417, -0.02801439, -3.74310342, -0.09417551, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21004, 1004, 0.0, 69.90889689, 0.01551279, 69.90889689, 0.04653837, 48.93622782, -760.57164518, 0.05, 2, 0, 71004, 22004, 2, 3)
    ops.uniaxialMaterial('LimitState', 41004, 17.47722422, 6.752e-05, 52.43167267, 0.00020257, 174.77224223, 0.00067523, -17.47722422, -6.752e-05, -52.43167267, -0.00020257, -174.77224223, -0.00067523, 0.4, 0.3, 0.003, 0.0, 0.0, 21004, 2)
    ops.limitCurve('ThreePoint', 11004, 1004, 0.0, 74.61252243, 0.01343563, 74.61252243, 0.0403069, 52.2287657, -934.11625955, 0.05, 2, 0, 71004, 22004, 1, 3)
    ops.uniaxialMaterial('LimitState', 31004, 18.65313061, 7.207e-05, 55.95939182, 0.0002162, 186.53130608, 0.00072066, -18.65313061, -7.207e-05, -55.95939182, -0.0002162, -186.53130608, -0.00072066, 0.4, 0.3, 0.003, 0.0, 0.0, 11004, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1004, 99999, 'P', 41004, 'Vy', 31004, 'Vz', 21004, 'My', 11004, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171004, 71004, 171004, 1004, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122004, 122004, 22004, 1004, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171005, 0.0, 4.05, 3.775)
    ops.node(122005, 0.0, 4.05, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1005, 171005, 122005, 0.075, 28154086.51478868, 11730869.38116195, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21005, 39.17303672, 0.00079108, 47.48241767, 0.02496909, 4.74824177, 0.085837, -39.17303672, -0.00079108, -47.48241767, -0.02496909, -4.74824177, -0.085837, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11005, 34.8227648, 0.00091772, 42.20936647, 0.02361712, 4.22093665, 0.07602284, -34.8227648, -0.00091772, -42.20936647, -0.02361712, -4.22093665, -0.07602284, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21005, 1005, 0.0, 76.17903574, 0.01582162, 76.17903574, 0.04746486, 53.32532502, -923.0016946, 0.05, 2, 0, 71005, 22005, 2, 3)
    ops.uniaxialMaterial('LimitState', 41005, 19.04475894, 7.533e-05, 57.13427681, 0.00022599, 190.44758936, 0.00075329, -19.04475894, -7.533e-05, -57.13427681, -0.00022599, -190.44758936, -0.00075329, 0.4, 0.3, 0.003, 0.0, 0.0, 21005, 2)
    ops.limitCurve('ThreePoint', 11005, 1005, 0.0, 71.39837789, 0.01835435, 71.39837789, 0.05506306, 49.97886452, -769.62076307, 0.05, 2, 0, 71005, 22005, 1, 3)
    ops.uniaxialMaterial('LimitState', 31005, 17.84959447, 7.06e-05, 53.54878342, 0.00021181, 178.49594472, 0.00070602, -17.84959447, -7.06e-05, -53.54878342, -0.00021181, -178.49594472, -0.00070602, 0.4, 0.3, 0.003, 0.0, 0.0, 11005, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1005, 99999, 'P', 41005, 'Vy', 31005, 'Vz', 21005, 'My', 11005, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171005, 71005, 171005, 1005, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122005, 122005, 22005, 1005, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171006, 2.9, 4.05, 3.775)
    ops.node(122006, 2.9, 4.05, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1006, 171006, 122006, 0.1575, 33943153.55169822, 14142980.64654093, 0.00337604, 0.00176859, 0.00292359, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21006, 106.80529104, 0.00052806, 127.77138155, 0.03479752, 12.77713815, 0.10351257, -106.80529104, -0.00052806, -127.77138155, -0.03479752, -12.77713815, -0.10351257, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11006, 74.94424657, 0.00060144, 89.65595084, 0.03206191, 8.96559508, 0.08815988, -74.94424657, -0.00060144, -89.65595084, -0.03206191, -8.96559508, -0.08815988, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21006, 1006, 0.0, 176.09940765, 0.01056119, 176.09940765, 0.03168358, 123.26958536, -1728.81148933, 0.05, 2, 0, 71006, 22006, 2, 3)
    ops.uniaxialMaterial('LimitState', 41006, 44.02485191, 6.878e-05, 132.07455574, 0.00020634, 440.24851913, 0.00068779, -44.02485191, -6.878e-05, -132.07455574, -0.00020634, -440.24851913, -0.00068779, 0.4, 0.3, 0.003, 0.0, 0.0, 21006, 2)
    ops.limitCurve('ThreePoint', 11006, 1006, 0.0, 164.27244351, 0.01202877, 164.27244351, 0.0360863, 114.99071046, -1330.12607549, 0.05, 2, 0, 71006, 22006, 1, 3)
    ops.uniaxialMaterial('LimitState', 31006, 41.06811088, 6.416e-05, 123.20433263, 0.00019248, 410.68110877, 0.0006416, -41.06811088, -6.416e-05, -123.20433263, -0.00019248, -410.68110877, -0.0006416, 0.4, 0.3, 0.003, 0.0, 0.0, 11006, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1006, 99999, 'P', 41006, 'Vy', 31006, 'Vz', 21006, 'My', 11006, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171006, 71006, 171006, 1006, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122006, 122006, 22006, 1006, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171007, 7.9, 4.05, 3.775)
    ops.node(122007, 7.9, 4.05, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1007, 171007, 122007, 0.175, 29666351.93697295, 12360979.97373873, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21007, 123.33737105, 0.00054548, 149.39675279, 0.03160526, 14.93967528, 0.08292972, -123.33737105, -0.00054548, -149.39675279, -0.03160526, -14.93967528, -0.08292972, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11007, 77.51839772, 0.00066694, 93.89690085, 0.02843894, 9.38969009, 0.06779957, -77.51839772, -0.00066694, -93.89690085, -0.02843894, -9.38969009, -0.06779957, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21007, 1007, 0.0, 183.08269372, 0.01090969, 183.08269372, 0.03272907, 128.1578856, -1916.26822943, 0.05, 2, 0, 71007, 22007, 2, 3)
    ops.uniaxialMaterial('LimitState', 41007, 45.77067343, 7.363e-05, 137.31202029, 0.0002209, 457.70673429, 0.00073634, -45.77067343, -7.363e-05, -137.31202029, -0.0002209, -457.70673429, -0.00073634, 0.4, 0.3, 0.003, 0.0, 0.0, 21007, 2)
    ops.limitCurve('ThreePoint', 11007, 1007, 0.0, 153.78349072, 0.0133387, 153.78349072, 0.04001611, 107.6484435, -1327.77225854, 0.05, 2, 0, 71007, 22007, 1, 3)
    ops.uniaxialMaterial('LimitState', 31007, 38.44587268, 6.185e-05, 115.33761804, 0.00018555, 384.4587268, 0.0006185, -38.44587268, -6.185e-05, -115.33761804, -0.00018555, -384.4587268, -0.0006185, 0.4, 0.3, 0.003, 0.0, 0.0, 11007, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1007, 99999, 'P', 41007, 'Vy', 31007, 'Vz', 21007, 'My', 11007, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171007, 71007, 171007, 1007, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122007, 122007, 22007, 1007, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171008, 12.9, 4.05, 3.775)
    ops.node(122008, 12.9, 4.05, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1008, 171008, 122008, 0.12, 34104298.09360304, 14210124.20566794, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21008, 65.10340473, 0.00062156, 77.83877045, 0.03660673, 7.78387705, 0.11496577, -65.10340473, -0.00062156, -77.83877045, -0.03660673, -7.78387705, -0.11496577, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11008, 44.81679782, 0.00079498, 53.58374807, 0.03333767, 5.35837481, 0.09506814, -44.81679782, -0.00079498, -53.58374807, -0.03333767, -5.35837481, -0.09506814, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21008, 1008, 0.0, 155.97959208, 0.01243115, 155.97959208, 0.03729344, 109.18571446, -2188.97707342, 0.05, 2, 0, 71008, 22008, 2, 3)
    ops.uniaxialMaterial('LimitState', 41008, 38.99489802, 7.958e-05, 116.98469406, 0.00023874, 389.94898021, 0.00079581, -38.99489802, -7.958e-05, -116.98469406, -0.00023874, -389.94898021, -0.00079581, 0.4, 0.3, 0.003, 0.0, 0.0, 21008, 2)
    ops.limitCurve('ThreePoint', 11008, 1008, 0.0, 140.54396005, 0.01589953, 140.54396005, 0.04769859, 98.38077203, -1532.34123627, 0.05, 2, 0, 71008, 22008, 1, 3)
    ops.uniaxialMaterial('LimitState', 31008, 35.13599001, 7.171e-05, 105.40797004, 0.00021512, 351.35990012, 0.00071705, -35.13599001, -7.171e-05, -105.40797004, -0.00021512, -351.35990012, -0.00071705, 0.4, 0.3, 0.003, 0.0, 0.0, 11008, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1008, 99999, 'P', 41008, 'Vy', 31008, 'Vz', 21008, 'My', 11008, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171008, 71008, 171008, 1008, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122008, 122008, 22008, 1008, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171009, 0.0, 8.1, 3.775)
    ops.node(122009, 0.0, 8.1, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1009, 171009, 122009, 0.075, 30611081.42311148, 12754617.25962978, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21009, 33.9792936, 0.00084427, 41.05097895, 0.03093582, 4.10509789, 0.09868999, -33.9792936, -0.00084427, -41.05097895, -0.03093582, -4.10509789, -0.09868999, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11009, 29.32085817, 0.00101986, 35.42304163, 0.02927116, 3.54230416, 0.08760578, -29.32085817, -0.00101986, -35.42304163, -0.02927116, -3.54230416, -0.08760578, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21009, 1009, 0.0, 85.98845254, 0.01688533, 85.98845254, 0.050656, 60.19191677, -1192.95966018, 0.05, 2, 0, 71009, 22009, 2, 3)
    ops.uniaxialMaterial('LimitState', 41009, 21.49711313, 7.82e-05, 64.4913394, 0.00023461, 214.97113134, 0.00078204, -21.49711313, -7.82e-05, -64.4913394, -0.00023461, -214.97113134, -0.00078204, 0.4, 0.3, 0.003, 0.0, 0.0, 21009, 2)
    ops.limitCurve('ThreePoint', 11009, 1009, 0.0, 80.15859443, 0.02039714, 80.15859443, 0.06119143, 56.1110161, -958.93829449, 0.05, 2, 0, 71009, 22009, 1, 3)
    ops.uniaxialMaterial('LimitState', 31009, 20.03964861, 7.29e-05, 60.11894582, 0.00021871, 200.39648607, 0.00072902, -20.03964861, -7.29e-05, -60.11894582, -0.00021871, -200.39648607, -0.00072902, 0.4, 0.3, 0.003, 0.0, 0.0, 11009, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1009, 99999, 'P', 41009, 'Vy', 31009, 'Vz', 21009, 'My', 11009, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171009, 71009, 171009, 1009, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122009, 122009, 22009, 1009, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171010, 2.9, 8.1, 3.775)
    ops.node(122010, 2.9, 8.1, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1010, 171010, 122010, 0.12, 30922243.96162294, 12884268.31734289, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21010, 64.1606345, 0.00063213, 77.42260751, 0.0418938, 7.74226075, 0.11549789, -64.1606345, -0.00063213, -77.42260751, -0.0418938, -7.74226075, -0.11549789, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11010, 46.67822313, 0.00080087, 56.32658992, 0.03811528, 5.63265899, 0.09609985, -46.67822313, -0.00080087, -56.32658992, -0.03811528, -5.63265899, -0.09609985, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21010, 1010, 0.0, 152.93630498, 0.01264268, 152.93630498, 0.03792805, 107.05541349, -2453.72767567, 0.05, 2, 0, 71010, 22010, 2, 3)
    ops.uniaxialMaterial('LimitState', 41010, 38.23407625, 8.606e-05, 114.70222874, 0.00025817, 382.34076246, 0.00086058, -38.23407625, -8.606e-05, -114.70222874, -0.00025817, -382.34076246, -0.00086058, 0.4, 0.3, 0.003, 0.0, 0.0, 21010, 2)
    ops.limitCurve('ThreePoint', 11010, 1010, 0.0, 135.64398241, 0.01601735, 135.64398241, 0.04805205, 94.95078768, -1717.2269621, 0.05, 2, 0, 71010, 22010, 1, 3)
    ops.uniaxialMaterial('LimitState', 31010, 33.9109956, 7.633e-05, 101.7329868, 0.00022898, 339.10995601, 0.00076327, -33.9109956, -7.633e-05, -101.7329868, -0.00022898, -339.10995601, -0.00076327, 0.4, 0.3, 0.003, 0.0, 0.0, 11010, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1010, 99999, 'P', 41010, 'Vy', 31010, 'Vz', 21010, 'My', 11010, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171010, 71010, 171010, 1010, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122010, 122010, 22010, 1010, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171011, 7.9, 8.1, 3.775)
    ops.node(122011, 7.9, 8.1, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1011, 171011, 122011, 0.175, 30103926.94287218, 12543302.89286341, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21011, 120.89586997, 0.00052537, 146.29358536, 0.02941809, 14.62935854, 0.08117529, -120.89586997, -0.00052537, -146.29358536, -0.02941809, -14.62935854, -0.08117529, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11011, 76.07468087, 0.00063551, 92.05639385, 0.02646986, 9.20563939, 0.06616235, -76.07468087, -0.00063551, -92.05639385, -0.02646986, -9.20563939, -0.06616235, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21011, 1011, 0.0, 173.40221497, 0.01050737, 173.40221497, 0.0315221, 121.38155048, -1497.43954905, 0.05, 2, 0, 71011, 22011, 2, 3)
    ops.uniaxialMaterial('LimitState', 41011, 43.35055374, 6.873e-05, 130.05166123, 0.00020618, 433.50553742, 0.00068726, -43.35055374, -6.873e-05, -130.05166123, -0.00020618, -433.50553742, -0.00068726, 0.4, 0.3, 0.003, 0.0, 0.0, 21011, 2)
    ops.limitCurve('ThreePoint', 11011, 1011, 0.0, 147.53057654, 0.01271025, 147.53057654, 0.03813074, 103.27140358, -1081.33795843, 0.05, 2, 0, 71011, 22011, 1, 3)
    ops.uniaxialMaterial('LimitState', 31011, 36.88264414, 5.847e-05, 110.64793241, 0.00017542, 368.82644136, 0.00058472, -36.88264414, -5.847e-05, -110.64793241, -0.00017542, -368.82644136, -0.00058472, 0.4, 0.3, 0.003, 0.0, 0.0, 11011, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1011, 99999, 'P', 41011, 'Vy', 31011, 'Vz', 21011, 'My', 11011, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171011, 71011, 171011, 1011, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122011, 122011, 22011, 1011, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171012, 12.9, 8.1, 3.775)
    ops.node(122012, 12.9, 8.1, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1012, 171012, 122012, 0.12, 32387054.34767244, 13494605.97819685, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21012, 61.75729048, 0.00056917, 74.26128586, 0.03296702, 7.42612859, 0.10966725, -61.75729048, -0.00056917, -74.26128586, -0.03296702, -7.42612859, -0.10966725, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11012, 51.02736102, 0.00068385, 61.35886814, 0.0299824, 6.13588681, 0.09040608, -51.02736102, -0.00068385, -61.35886814, -0.0299824, -6.13588681, -0.09040608, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21012, 1012, 0.0, 139.09172073, 0.01138342, 139.09172073, 0.03415025, 97.36420451, -1738.8885557, 0.05, 2, 0, 71012, 22012, 2, 3)
    ops.uniaxialMaterial('LimitState', 41012, 34.77293018, 7.473e-05, 104.31879054, 0.00022418, 347.72930182, 0.00074727, -34.77293018, -7.473e-05, -104.31879054, -0.00022418, -347.72930182, -0.00074727, 0.4, 0.3, 0.003, 0.0, 0.0, 21012, 2)
    ops.limitCurve('ThreePoint', 11012, 1012, 0.0, 126.22479172, 0.01367707, 126.22479172, 0.04103122, 88.35735421, -1248.22575271, 0.05, 2, 0, 71012, 22012, 1, 3)
    ops.uniaxialMaterial('LimitState', 31012, 31.55619793, 6.781e-05, 94.66859379, 0.00020344, 315.56197931, 0.00067814, -31.55619793, -6.781e-05, -94.66859379, -0.00020344, -315.56197931, -0.00067814, 0.4, 0.3, 0.003, 0.0, 0.0, 11012, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1012, 99999, 'P', 41012, 'Vy', 31012, 'Vz', 21012, 'My', 11012, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171012, 71012, 171012, 1012, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122012, 122012, 22012, 1012, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171013, 0.0, 12.15, 3.775)
    ops.node(122013, 0.0, 12.15, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1013, 171013, 122013, 0.075, 28755403.92336452, 11981418.30140189, 0.00077515, 0.00042969, 0.00061875, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21013, 31.04884328, 0.00076232, 37.66143145, 0.02949427, 3.76614315, 0.0946242, -31.04884328, -0.00076232, -37.66143145, -0.02949427, -3.76614315, -0.0946242, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11013, 26.80394224, 0.00091279, 32.51247798, 0.02788764, 3.2512478, 0.08396285, -26.80394224, -0.00091279, -32.51247798, -0.02788764, -3.2512478, -0.08396285, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21013, 1013, 0.0, 79.87072331, 0.0152464, 79.87072331, 0.04573921, 55.90950632, -1112.09887149, 0.05, 2, 0, 71013, 22013, 2, 3)
    ops.uniaxialMaterial('LimitState', 41013, 19.96768083, 7.733e-05, 59.90304248, 0.00023198, 199.67680827, 0.00077328, -19.96768083, -7.733e-05, -59.90304248, -0.00023198, -199.67680827, -0.00077328, 0.4, 0.3, 0.003, 0.0, 0.0, 21013, 2)
    ops.limitCurve('ThreePoint', 11013, 1013, 0.0, 74.36481744, 0.01825586, 74.36481744, 0.05476757, 52.05537221, -898.44931513, 0.05, 2, 0, 71013, 22013, 1, 3)
    ops.uniaxialMaterial('LimitState', 31013, 18.59120436, 7.2e-05, 55.77361308, 0.00021599, 185.9120436, 0.00071997, -18.59120436, -7.2e-05, -55.77361308, -0.00021599, -185.9120436, -0.00071997, 0.4, 0.3, 0.003, 0.0, 0.0, 11013, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1013, 99999, 'P', 41013, 'Vy', 31013, 'Vz', 21013, 'My', 11013, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171013, 71013, 171013, 1013, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122013, 122013, 22013, 1013, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171014, 2.9, 12.15, 3.775)
    ops.node(122014, 2.9, 12.15, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1014, 171014, 122014, 0.12, 29827345.9865905, 12428060.82774604, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21014, 71.61784309, 0.00063362, 86.64323639, 0.03866968, 8.66432364, 0.11063398, -71.61784309, -0.00063362, -86.64323639, -0.03866968, -8.66432364, -0.11063398, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11014, 52.2610559, 0.00077257, 63.22540341, 0.03516995, 6.32254034, 0.09186271, -52.2610559, -0.00077257, -63.22540341, -0.03516995, -6.32254034, -0.09186271, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21014, 1014, 0.0, 132.84292309, 0.01267249, 132.84292309, 0.03801748, 92.99004616, -1764.31197197, 0.05, 2, 0, 71014, 22014, 2, 3)
    ops.uniaxialMaterial('LimitState', 41014, 33.21073077, 7.749e-05, 99.63219232, 0.00023248, 332.10730772, 0.00077495, -33.21073077, -7.749e-05, -99.63219232, -0.00023248, -332.10730772, -0.00077495, 0.4, 0.3, 0.003, 0.0, 0.0, 21014, 2)
    ops.limitCurve('ThreePoint', 11014, 1014, 0.0, 119.57235831, 0.01545144, 119.57235831, 0.04635433, 83.70065081, -1280.98751601, 0.05, 2, 0, 71014, 22014, 1, 3)
    ops.uniaxialMaterial('LimitState', 31014, 29.89308958, 6.975e-05, 89.67926873, 0.00020926, 298.93089577, 0.00069753, -29.89308958, -6.975e-05, -89.67926873, -0.00020926, -298.93089577, -0.00069753, 0.4, 0.3, 0.003, 0.0, 0.0, 11014, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1014, 99999, 'P', 41014, 'Vy', 31014, 'Vz', 21014, 'My', 11014, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171014, 71014, 171014, 1014, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122014, 122014, 22014, 1014, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171015, 7.9, 12.15, 3.775)
    ops.node(122015, 7.9, 12.15, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1015, 171015, 122015, 0.175, 28405895.62552819, 11835789.84397008, 0.00405757, 0.0019651, 0.00401042, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21015, 118.71410103, 0.00053578, 144.15970722, 0.03074797, 14.41597072, 0.08068288, -118.71410103, -0.00053578, -144.15970722, -0.03074797, -14.41597072, -0.08068288, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11015, 74.69726447, 0.00065494, 90.70814405, 0.02766908, 9.0708144, 0.06596407, -74.69726447, -0.00065494, -90.70814405, -0.02766908, -9.0708144, -0.06596407, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21015, 1015, 0.0, 167.85319394, 0.0107157, 167.85319394, 0.03214709, 117.49723576, -1634.66954595, 0.05, 2, 0, 71015, 22015, 2, 3)
    ops.uniaxialMaterial('LimitState', 41015, 41.96329848, 7.05e-05, 125.88989545, 0.00021151, 419.63298485, 0.00070504, -41.96329848, -7.05e-05, -125.88989545, -0.00021151, -419.63298485, -0.00070504, 0.4, 0.3, 0.003, 0.0, 0.0, 21015, 2)
    ops.limitCurve('ThreePoint', 11015, 1015, 0.0, 141.64119125, 0.0130989, 141.64119125, 0.03929669, 99.14883387, -1162.65324479, 0.05, 2, 0, 71015, 22015, 1, 3)
    ops.uniaxialMaterial('LimitState', 31015, 35.41029781, 5.949e-05, 106.23089344, 0.00017848, 354.10297812, 0.00059494, -35.41029781, -5.949e-05, -106.23089344, -0.00017848, -354.10297812, -0.00059494, 0.4, 0.3, 0.003, 0.0, 0.0, 11015, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1015, 99999, 'P', 41015, 'Vy', 31015, 'Vz', 21015, 'My', 11015, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171015, 71015, 171015, 1015, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122015, 122015, 22015, 1015, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171016, 12.9, 12.15, 3.775)
    ops.node(122016, 12.9, 12.15, 6.125)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1016, 171016, 122016, 0.12, 31007748.7985116, 12919895.33271317, 0.00194385, 0.00099, 0.00176, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21016, 58.71380696, 0.00055256, 70.87845688, 0.03345256, 7.08784569, 0.10855021, -58.71380696, -0.00055256, -70.87845688, -0.03345256, -7.08784569, -0.10855021, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11016, 48.19370698, 0.00066433, 58.17874464, 0.03041699, 5.81787446, 0.08957818, -48.19370698, -0.00066433, -58.17874464, -0.03041699, -5.81787446, -0.08957818, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21016, 1016, 0.0, 127.89655901, 0.01105118, 127.89655901, 0.03315355, 89.52759131, -1498.55811612, 0.05, 2, 0, 71016, 22016, 2, 3)
    ops.uniaxialMaterial('LimitState', 41016, 31.97413975, 7.177e-05, 95.92241926, 0.00021531, 319.74139753, 0.00071769, -31.97413975, -7.177e-05, -95.92241926, -0.00021531, -319.74139753, -0.00071769, 0.4, 0.3, 0.003, 0.0, 0.0, 21016, 2)
    ops.limitCurve('ThreePoint', 11016, 1016, 0.0, 116.53896339, 0.01328664, 116.53896339, 0.03985992, 81.57727437, -1094.85956957, 0.05, 2, 0, 71016, 22016, 1, 3)
    ops.uniaxialMaterial('LimitState', 31016, 29.13474085, 6.54e-05, 87.40422254, 0.00019619, 291.34740847, 0.00065396, -29.13474085, -6.54e-05, -87.40422254, -0.00019619, -291.34740847, -0.00065396, 0.4, 0.3, 0.003, 0.0, 0.0, 11016, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1016, 99999, 'P', 41016, 'Vy', 31016, 'Vz', 21016, 'My', 11016, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171016, 71016, 171016, 1016, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122016, 122016, 22016, 1016, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171017, 0.0, 16.2, 3.75)
    ops.node(122017, 0.0, 16.2, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1017, 171017, 122017, 0.0625, 34004847.90993069, 14168686.62913779, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21017, 17.59484011, 0.00066016, 21.06361411, 0.02461315, 2.10636141, 0.08595017, -17.59484011, -0.00066016, -21.06361411, -0.02461315, -2.10636141, -0.08595017, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11017, 17.59484011, 0.00066016, 21.06361411, 0.02461315, 2.10636141, 0.08595017, -17.59484011, -0.00066016, -21.06361411, -0.02461315, -2.10636141, -0.08595017, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21017, 1017, 0.0, 68.98211676, 0.01320312, 68.98211676, 0.03960937, 48.28748173, -752.58434853, 0.05, 2, 0, 71017, 22017, 2, 3)
    ops.uniaxialMaterial('LimitState', 41017, 17.24552919, 6.777e-05, 51.73658757, 0.00020331, 172.4552919, 0.00067771, -17.24552919, -6.777e-05, -51.73658757, -0.00020331, -172.4552919, -0.00067771, 0.4, 0.3, 0.003, 0.0, 0.0, 21017, 2)
    ops.limitCurve('ThreePoint', 11017, 1017, 0.0, 68.98211676, 0.01320312, 68.98211676, 0.03960937, 48.28748173, -752.58434853, 0.05, 2, 0, 71017, 22017, 1, 3)
    ops.uniaxialMaterial('LimitState', 31017, 17.24552919, 6.777e-05, 51.73658757, 0.00020331, 172.4552919, 0.00067771, -17.24552919, -6.777e-05, -51.73658757, -0.00020331, -172.4552919, -0.00067771, 0.4, 0.3, 0.003, 0.0, 0.0, 11017, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1017, 99999, 'P', 41017, 'Vy', 31017, 'Vz', 21017, 'My', 11017, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171017, 71017, 171017, 1017, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122017, 122017, 22017, 1017, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171018, 2.9, 16.2, 3.75)
    ops.node(122018, 2.9, 16.2, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1018, 171018, 122018, 0.105, 33740350.63941918, 14058479.43309133, 0.00152551, 0.00117906, 0.00086625, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21018, 51.2586513, 0.00069725, 61.38026851, 0.03311279, 6.13802685, 0.10219199, -51.2586513, -0.00069725, -61.38026851, -0.03311279, -6.13802685, -0.10219199, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11018, 52.62282701, 0.0006302, 63.0138166, 0.03486328, 6.30138166, 0.11348608, -52.62282701, -0.0006302, -63.0138166, -0.03486328, -6.30138166, -0.11348608, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21018, 1018, 0.0, 125.02876543, 0.01394497, 125.02876543, 0.04183491, 87.5201358, -1527.02376159, 0.05, 2, 0, 71018, 22018, 2, 3)
    ops.uniaxialMaterial('LimitState', 41018, 31.25719136, 7.369e-05, 93.77157408, 0.00022107, 312.57191359, 0.00073689, -31.25719136, -7.369e-05, -93.77157408, -0.00022107, -312.57191359, -0.00073689, 0.4, 0.3, 0.003, 0.0, 0.0, 21018, 2)
    ops.limitCurve('ThreePoint', 11018, 1018, 0.0, 132.46276374, 0.01260394, 132.46276374, 0.03781181, 92.72393462, -1861.3072918, 0.05, 2, 0, 71018, 22018, 1, 3)
    ops.uniaxialMaterial('LimitState', 31018, 33.11569094, 7.807e-05, 99.34707281, 0.00023421, 331.15690936, 0.0007807, -33.11569094, -7.807e-05, -99.34707281, -0.00023421, -331.15690936, -0.0007807, 0.4, 0.3, 0.003, 0.0, 0.0, 11018, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1018, 99999, 'P', 41018, 'Vy', 31018, 'Vz', 21018, 'My', 11018, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171018, 71018, 171018, 1018, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122018, 122018, 22018, 1018, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171019, 7.9, 16.2, 3.75)
    ops.node(122019, 7.9, 16.2, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1019, 171019, 122019, 0.14, 31659405.20120712, 13191418.8338363, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21019, 58.51747377, 0.00060154, 70.5531787, 0.02720588, 7.05531787, 0.07571803, -58.51747377, -0.00060154, -70.5531787, -0.02720588, -7.05531787, -0.07571803, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11019, 71.07276484, 0.00055461, 85.69080576, 0.0283318, 8.56908058, 0.08207129, -71.07276484, -0.00055461, -85.69080576, -0.0283318, -8.56908058, -0.08207129, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21019, 1019, 0.0, 131.79801479, 0.01203073, 131.79801479, 0.03609218, 92.25861035, -1108.70783388, 0.05, 2, 0, 71019, 22019, 2, 3)
    ops.uniaxialMaterial('LimitState', 41019, 32.9495037, 6.209e-05, 98.84851109, 0.00018626, 329.49503697, 0.00062088, -32.9495037, -6.209e-05, -98.84851109, -0.00018626, -329.49503697, -0.00062088, 0.4, 0.3, 0.003, 0.0, 0.0, 21019, 2)
    ops.limitCurve('ThreePoint', 11019, 1019, 0.0, 136.72885563, 0.01109222, 136.72885563, 0.03327666, 95.71019894, -1273.68816321, 0.05, 2, 0, 71019, 22019, 1, 3)
    ops.uniaxialMaterial('LimitState', 31019, 34.18221391, 6.441e-05, 102.54664172, 0.00019323, 341.82213907, 0.00064411, -34.18221391, -6.441e-05, -102.54664172, -0.00019323, -341.82213907, -0.00064411, 0.4, 0.3, 0.003, 0.0, 0.0, 11019, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1019, 99999, 'P', 41019, 'Vy', 31019, 'Vz', 21019, 'My', 11019, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171019, 71019, 171019, 1019, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122019, 122019, 22019, 1019, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171020, 12.9, 16.2, 3.75)
    ops.node(122020, 12.9, 16.2, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 1020, 171020, 122020, 0.09, 29816314.73911797, 12423464.47463249, 0.00114075, 0.0007425, 0.0007425, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 21020, 36.61804854, 0.00066201, 44.3821924, 0.02689346, 4.43821924, 0.08672962, -36.61804854, -0.00066201, -44.3821924, -0.02689346, -4.43821924, -0.08672962, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 11020, 33.49976744, 0.00066201, 40.60274053, 0.02689346, 4.06027405, 0.08672962, -33.49976744, -0.00066201, -40.60274053, -0.02689346, -4.06027405, -0.08672962, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 21020, 1020, 0.0, 85.97436986, 0.01324022, 85.97436986, 0.03972065, 60.1820589, -976.76511517, 0.05, 2, 0, 71020, 22020, 2, 3)
    ops.uniaxialMaterial('LimitState', 41020, 21.49359247, 6.69e-05, 64.4807774, 0.00020069, 214.93592466, 0.00066896, -21.49359247, -6.69e-05, -64.4807774, -0.00020069, -214.93592466, -0.00066896, 0.4, 0.3, 0.003, 0.0, 0.0, 21020, 2)
    ops.limitCurve('ThreePoint', 11020, 1020, 0.0, 85.97436986, 0.01324022, 85.97436986, 0.03972065, 60.1820589, -976.76511517, 0.05, 2, 0, 71020, 22020, 1, 3)
    ops.uniaxialMaterial('LimitState', 31020, 21.49359247, 6.69e-05, 64.4807774, 0.00020069, 214.93592466, 0.00066896, -21.49359247, -6.69e-05, -64.4807774, -0.00020069, -214.93592466, -0.00066896, 0.4, 0.3, 0.003, 0.0, 0.0, 11020, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 1020, 99999, 'P', 41020, 'Vy', 31020, 'Vz', 21020, 'My', 11020, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171020, 71020, 171020, 1020, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122020, 122020, 22020, 1020, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172003, 7.9, 0.0, 6.65)
    ops.node(123003, 7.9, 0.0, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2003, 172003, 123003, 0.0875, 26799800.78889846, 11166583.66204102, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22003, 27.67085739, 0.00087027, 33.71323147, 0.02601335, 3.37132315, 0.07507559, -27.67085739, -0.00087027, -33.71323147, -0.02601335, -3.37132315, -0.07507559, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12003, 43.45042459, 0.00066759, 52.93851942, 0.02886426, 5.29385194, 0.0932558, -43.45042459, -0.00066759, -52.93851942, -0.02886426, -5.29385194, -0.0932558, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22003, 2003, 0.0, 72.52194195, 0.0174055, 72.52194195, 0.0522165, 50.76535936, -792.36549847, 0.05, 2, 0, 72003, 23003, 2, 3)
    ops.uniaxialMaterial('LimitState', 42003, 18.13048549, 6.457e-05, 54.39145646, 0.00019372, 181.30485487, 0.00064574, -18.13048549, -6.457e-05, -54.39145646, -0.00019372, -181.30485487, -0.00064574, 0.4, 0.3, 0.003, 0.0, 0.0, 22003, 2)
    ops.limitCurve('ThreePoint', 12003, 2003, 0.0, 82.32332605, 0.01335179, 82.32332605, 0.04005538, 57.62632824, -1172.31659071, 0.05, 2, 0, 72003, 23003, 1, 3)
    ops.uniaxialMaterial('LimitState', 32003, 20.58083151, 7.33e-05, 61.74249454, 0.0002199, 205.80831514, 0.00073302, -20.58083151, -7.33e-05, -61.74249454, -0.0002199, -205.80831514, -0.00073302, 0.4, 0.3, 0.003, 0.0, 0.0, 12003, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2003, 99999, 'P', 42003, 'Vy', 32003, 'Vz', 22003, 'My', 12003, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172003, 72003, 172003, 2003, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123003, 123003, 23003, 2003, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172004, 12.9, 0.0, 6.65)
    ops.node(123004, 12.9, 0.0, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2004, 172004, 123004, 0.0625, 31437639.2543034, 13099016.35595975, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22004, 18.81187326, 0.00081093, 22.71671577, 0.01894018, 2.27167158, 0.07919132, -18.81187326, -0.00081093, -22.71671577, -0.01894018, -2.27167158, -0.07919132, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12004, 18.81187326, 0.00081093, 22.71671577, 0.01894018, 2.27167158, 0.07919132, -18.81187326, -0.00081093, -22.71671577, -0.01894018, -2.27167158, -0.07919132, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22004, 2004, 0.0, 46.93547627, 0.01621859, 46.93547627, 0.04865578, 32.85483339, -622.05352092, 0.05, 2, 0, 72004, 23004, 2, 3)
    ops.uniaxialMaterial('LimitState', 42004, 11.73386907, 4.988e-05, 35.20160721, 0.00014963, 117.33869068, 0.00049877, -11.73386907, -4.988e-05, -35.20160721, -0.00014963, -117.33869068, -0.00049877, 0.4, 0.3, 0.003, 0.0, 0.0, 22004, 2)
    ops.limitCurve('ThreePoint', 12004, 2004, 0.0, 46.93547627, 0.01621859, 46.93547627, 0.04865578, 32.85483339, -622.05352092, 0.05, 2, 0, 72004, 23004, 1, 3)
    ops.uniaxialMaterial('LimitState', 32004, 11.73386907, 4.988e-05, 35.20160721, 0.00014963, 117.33869068, 0.00049877, -11.73386907, -4.988e-05, -35.20160721, -0.00014963, -117.33869068, -0.00049877, 0.4, 0.3, 0.003, 0.0, 0.0, 12004, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2004, 99999, 'P', 42004, 'Vy', 32004, 'Vz', 22004, 'My', 12004, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172004, 72004, 172004, 2004, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123004, 123004, 23004, 2004, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172005, 0.0, 4.05, 6.675)
    ops.node(123005, 0.0, 4.05, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2005, 172005, 123005, 0.0625, 26456984.81261575, 11023743.67192323, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22005, 21.83166945, 0.00083824, 26.5811801, 0.02377708, 2.65811801, 0.07518484, -21.83166945, -0.00083824, -26.5811801, -0.02377708, -2.65811801, -0.07518484, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12005, 21.83166945, 0.00083824, 26.5811801, 0.02377708, 2.65811801, 0.07518484, -21.83166945, -0.00083824, -26.5811801, -0.02377708, -2.65811801, -0.07518484, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22005, 2005, 0.0, 56.1105928, 0.0167649, 56.1105928, 0.05029469, 39.27741496, -701.85125618, 0.05, 2, 0, 72005, 23005, 2, 3)
    ops.uniaxialMaterial('LimitState', 42005, 14.0276482, 7.085e-05, 42.0829446, 0.00021256, 140.276482, 0.00070852, -14.0276482, -7.085e-05, -42.0829446, -0.00021256, -140.276482, -0.00070852, 0.4, 0.3, 0.003, 0.0, 0.0, 22005, 2)
    ops.limitCurve('ThreePoint', 12005, 2005, 0.0, 56.1105928, 0.0167649, 56.1105928, 0.05029469, 39.27741496, -701.85125618, 0.05, 2, 0, 72005, 23005, 1, 3)
    ops.uniaxialMaterial('LimitState', 32005, 14.0276482, 7.085e-05, 42.0829446, 0.00021256, 140.276482, 0.00070852, -14.0276482, -7.085e-05, -42.0829446, -0.00021256, -140.276482, -0.00070852, 0.4, 0.3, 0.003, 0.0, 0.0, 12005, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2005, 99999, 'P', 42005, 'Vy', 32005, 'Vz', 22005, 'My', 12005, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172005, 72005, 172005, 2005, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123005, 123005, 23005, 2005, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172006, 2.9, 4.05, 6.675)
    ops.node(123006, 2.9, 4.05, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2006, 172006, 123006, 0.0875, 29172662.78796365, 12155276.16165152, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22006, 51.43949053, 0.00066072, 62.29959165, 0.03284046, 6.22995916, 0.09721075, -51.43949053, -0.00066072, -62.29959165, -0.03284046, -6.22995916, -0.09721075, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12006, 35.23356339, 0.00086059, 42.67220746, 0.02955538, 4.26722075, 0.07860143, -35.23356339, -0.00086059, -42.67220746, -0.02955538, -4.26722075, -0.07860143, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22006, 2006, 0.0, 87.21264829, 0.01321435, 87.21264829, 0.03964304, 61.04885381, -978.57661785, 0.05, 2, 0, 72006, 23006, 2, 3)
    ops.uniaxialMaterial('LimitState', 42006, 21.80316207, 7.134e-05, 65.40948622, 0.00021402, 218.03162073, 0.00071339, -21.80316207, -7.134e-05, -65.40948622, -0.00021402, -218.03162073, -0.00071339, 0.4, 0.3, 0.003, 0.0, 0.0, 22006, 2)
    ops.limitCurve('ThreePoint', 12006, 2006, 0.0, 78.52785298, 0.01721178, 78.52785298, 0.05163534, 54.96949709, -707.60806335, 0.05, 2, 0, 72006, 23006, 1, 3)
    ops.uniaxialMaterial('LimitState', 32006, 19.63196325, 6.423e-05, 58.89588974, 0.0001927, 196.31963246, 0.00064235, -19.63196325, -6.423e-05, -58.89588974, -0.0001927, -196.31963246, -0.00064235, 0.4, 0.3, 0.003, 0.0, 0.0, 12006, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2006, 99999, 'P', 42006, 'Vy', 32006, 'Vz', 22006, 'My', 12006, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172006, 72006, 172006, 2006, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123006, 123006, 23006, 2006, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172007, 7.9, 4.05, 6.675)
    ops.node(123007, 7.9, 4.05, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2007, 172007, 123007, 0.1, 29054783.77804935, 12106159.90752056, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22007, 58.62114732, 0.00056608, 71.05247726, 0.03235162, 7.10524773, 0.09759247, -58.62114732, -0.00056608, -71.05247726, -0.03235162, -7.10524773, -0.09759247, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12007, 34.85091556, 0.00078635, 42.24147767, 0.02793289, 4.22414777, 0.07280693, -34.85091556, -0.00078635, -42.24147767, -0.02793289, -4.22414777, -0.07280693, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22007, 2007, 0.0, 97.82242173, 0.01132158, 97.82242173, 0.03396473, 68.47569521, -1104.4596551, 0.05, 2, 0, 72007, 23007, 2, 3)
    ops.uniaxialMaterial('LimitState', 42007, 24.45560543, 7.03e-05, 73.3668163, 0.0002109, 244.55605432, 0.00070299, -24.45560543, -7.03e-05, -73.3668163, -0.0002109, -244.55605432, -0.00070299, 0.4, 0.3, 0.003, 0.0, 0.0, 22007, 2)
    ops.limitCurve('ThreePoint', 12007, 2007, 0.0, 85.00520505, 0.01572704, 85.00520505, 0.04718112, 59.50364354, -703.33672953, 0.05, 2, 0, 72007, 23007, 1, 3)
    ops.uniaxialMaterial('LimitState', 32007, 21.25130126, 6.109e-05, 63.75390379, 0.00018327, 212.51301263, 0.00061088, -21.25130126, -6.109e-05, -63.75390379, -0.00018327, -212.51301263, -0.00061088, 0.4, 0.3, 0.003, 0.0, 0.0, 12007, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2007, 99999, 'P', 42007, 'Vy', 32007, 'Vz', 22007, 'My', 12007, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172007, 72007, 172007, 2007, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123007, 123007, 23007, 2007, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172008, 12.9, 4.05, 6.675)
    ops.node(123008, 12.9, 4.05, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2008, 172008, 123008, 0.0875, 36746678.58269997, 15311116.07612499, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22008, 44.14176677, 0.0005818, 52.24265201, 0.01765098, 5.2242652, 0.07977713, -44.14176677, -0.0005818, -52.24265201, -0.01765098, -5.2242652, -0.07977713, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12008, 28.18548642, 0.00072801, 33.35807935, 0.0160349, 3.33580794, 0.06400975, -28.18548642, -0.00072801, -33.35807935, -0.0160349, -3.33580794, -0.06400975, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22008, 2008, 0.0, 98.52345041, 0.01163609, 98.52345041, 0.03490828, 68.96641529, -769.16860533, 0.05, 2, 0, 72008, 23008, 2, 3)
    ops.uniaxialMaterial('LimitState', 42008, 24.6308626, 6.398e-05, 73.89258781, 0.00019194, 246.30862602, 0.0006398, -24.6308626, -6.398e-05, -73.89258781, -0.00019194, -246.30862602, -0.0006398, 0.4, 0.3, 0.003, 0.0, 0.0, 22008, 2)
    ops.limitCurve('ThreePoint', 12008, 2008, 0.0, 82.51300119, 0.01456023, 82.51300119, 0.04368068, 57.75910083, -549.43294283, 0.05, 2, 0, 72008, 23008, 1, 3)
    ops.uniaxialMaterial('LimitState', 32008, 20.6282503, 5.358e-05, 61.88475089, 0.00016075, 206.28250296, 0.00053583, -20.6282503, -5.358e-05, -61.88475089, -0.00016075, -206.28250296, -0.00053583, 0.4, 0.3, 0.003, 0.0, 0.0, 12008, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2008, 99999, 'P', 42008, 'Vy', 32008, 'Vz', 22008, 'My', 12008, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172008, 72008, 172008, 2008, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123008, 123008, 23008, 2008, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172009, 0.0, 8.1, 6.675)
    ops.node(123009, 0.0, 8.1, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2009, 172009, 123009, 0.0625, 30433494.13294119, 12680622.55539216, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22009, 20.6119669, 0.00086401, 24.95178445, 0.01839583, 2.49517844, 0.07737064, -20.6119669, -0.00086401, -24.95178445, -0.01839583, -2.49517844, -0.07737064, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12009, 20.6119669, 0.00086401, 24.95178445, 0.01839583, 2.49517844, 0.07737064, -20.6119669, -0.00086401, -24.95178445, -0.01839583, -2.49517844, -0.07737064, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22009, 2009, 0.0, 45.42029877, 0.01728026, 45.42029877, 0.05184077, 31.79420914, -578.66072667, 0.05, 2, 0, 72009, 23009, 2, 3)
    ops.uniaxialMaterial('LimitState', 42009, 11.35507469, 4.986e-05, 34.06522408, 0.00014958, 113.55074692, 0.0004986, -11.35507469, -4.986e-05, -34.06522408, -0.00014958, -113.55074692, -0.0004986, 0.4, 0.3, 0.003, 0.0, 0.0, 22009, 2)
    ops.limitCurve('ThreePoint', 12009, 2009, 0.0, 45.42029877, 0.01728026, 45.42029877, 0.05184077, 31.79420914, -578.66072667, 0.05, 2, 0, 72009, 23009, 1, 3)
    ops.uniaxialMaterial('LimitState', 32009, 11.35507469, 4.986e-05, 34.06522408, 0.00014958, 113.55074692, 0.0004986, -11.35507469, -4.986e-05, -34.06522408, -0.00014958, -113.55074692, -0.0004986, 0.4, 0.3, 0.003, 0.0, 0.0, 12009, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2009, 99999, 'P', 42009, 'Vy', 32009, 'Vz', 22009, 'My', 12009, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172009, 72009, 172009, 2009, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123009, 123009, 23009, 2009, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172010, 2.9, 8.1, 6.675)
    ops.node(123010, 2.9, 8.1, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2010, 172010, 123010, 0.0875, 30266160.65313503, 12610900.2721396, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22010, 48.50218011, 0.00067998, 58.67060135, 0.03575407, 5.86706013, 0.10394452, -48.50218011, -0.00067998, -58.67060135, -0.03575407, -5.86706013, -0.10394452, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12010, 33.02465209, 0.00090226, 39.94822899, 0.03217796, 3.9948229, 0.08413472, -33.02465209, -0.00090226, -39.94822899, -0.03217796, -3.9948229, -0.08413472, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22010, 2010, 0.0, 96.90900374, 0.01359953, 96.90900374, 0.04079859, 67.83630262, -1343.89554636, 0.05, 2, 0, 72010, 23010, 2, 3)
    ops.uniaxialMaterial('LimitState', 42010, 24.22725094, 7.641e-05, 72.68175281, 0.00022922, 242.27250935, 0.00076406, -24.22725094, -7.641e-05, -72.68175281, -0.00022922, -242.27250935, -0.00076406, 0.4, 0.3, 0.003, 0.0, 0.0, 22010, 2)
    ops.limitCurve('ThreePoint', 12010, 2010, 0.0, 85.74244371, 0.01804511, 85.74244371, 0.05413532, 60.0197106, -904.68927036, 0.05, 2, 0, 72010, 23010, 1, 3)
    ops.uniaxialMaterial('LimitState', 32010, 21.43561093, 6.76e-05, 64.30683278, 0.00020281, 214.35610928, 0.00067602, -21.43561093, -6.76e-05, -64.30683278, -0.00020281, -214.35610928, -0.00067602, 0.4, 0.3, 0.003, 0.0, 0.0, 12010, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2010, 99999, 'P', 42010, 'Vy', 32010, 'Vz', 22010, 'My', 12010, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172010, 72010, 172010, 2010, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123010, 123010, 23010, 2010, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172011, 7.9, 8.1, 6.675)
    ops.node(123011, 7.9, 8.1, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2011, 172011, 123011, 0.1, 31403513.59646365, 13084797.33185985, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22011, 65.08618189, 0.00063875, 78.45929495, 0.03233619, 7.84592949, 0.10075306, -65.08618189, -0.00063875, -78.45929495, -0.03233619, -7.84592949, -0.10075306, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12011, 38.45159108, 0.00091886, 46.352154, 0.02799014, 4.6352154, 0.07504873, -38.45159108, -0.00091886, -46.352154, -0.02799014, -4.6352154, -0.07504873, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22011, 2011, 0.0, 108.37659904, 0.01277506, 108.37659904, 0.03832519, 75.86361933, -1226.9138259, 0.05, 2, 0, 72011, 23011, 2, 3)
    ops.uniaxialMaterial('LimitState', 42011, 27.09414976, 7.206e-05, 81.28244928, 0.00021618, 270.94149759, 0.00072059, -27.09414976, -7.206e-05, -81.28244928, -0.00021618, -270.94149759, -0.00072059, 0.4, 0.3, 0.003, 0.0, 0.0, 22011, 2)
    ops.limitCurve('ThreePoint', 12011, 2011, 0.0, 94.27493472, 0.01837713, 94.27493472, 0.05513138, 65.9924543, -764.06331002, 0.05, 2, 0, 72011, 23011, 1, 3)
    ops.uniaxialMaterial('LimitState', 32011, 23.56873368, 6.268e-05, 70.70620104, 0.00018805, 235.68733679, 0.00062683, -23.56873368, -6.268e-05, -70.70620104, -0.00018805, -235.68733679, -0.00062683, 0.4, 0.3, 0.003, 0.0, 0.0, 12011, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2011, 99999, 'P', 42011, 'Vy', 32011, 'Vz', 22011, 'My', 12011, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172011, 72011, 172011, 2011, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123011, 123011, 23011, 2011, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172012, 12.9, 8.1, 6.675)
    ops.node(123012, 12.9, 8.1, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2012, 172012, 123012, 0.0875, 29686409.6982895, 12369337.37428729, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22012, 41.08995408, 0.00057797, 49.80912714, 0.02138865, 4.98091271, 0.07888672, -41.08995408, -0.00057797, -49.80912714, -0.02138865, -4.98091271, -0.07888672, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12012, 26.18511684, 0.0007262, 31.74152522, 0.01938831, 3.17415252, 0.06378927, -26.18511684, -0.0007262, -31.74152522, -0.01938831, -3.17415252, -0.06378927, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22012, 2012, 0.0, 81.69235751, 0.01155939, 81.69235751, 0.03467818, 57.18465026, -873.93533394, 0.05, 2, 0, 72012, 23012, 2, 3)
    ops.uniaxialMaterial('LimitState', 42012, 20.42308938, 6.567e-05, 61.26926814, 0.000197, 204.23089379, 0.00065667, -20.42308938, -6.567e-05, -61.26926814, -0.000197, -204.23089379, -0.00065667, 0.4, 0.3, 0.003, 0.0, 0.0, 22012, 2)
    ops.limitCurve('ThreePoint', 12012, 2012, 0.0, 65.25887215, 0.01452397, 65.25887215, 0.04357192, 45.6812105, -612.36764668, 0.05, 2, 0, 72012, 23012, 1, 3)
    ops.uniaxialMaterial('LimitState', 32012, 16.31471804, 5.246e-05, 48.94415411, 0.00015737, 163.14718037, 0.00052457, -16.31471804, -5.246e-05, -48.94415411, -0.00015737, -163.14718037, -0.00052457, 0.4, 0.3, 0.003, 0.0, 0.0, 12012, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2012, 99999, 'P', 42012, 'Vy', 32012, 'Vz', 22012, 'My', 12012, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172012, 72012, 172012, 2012, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123012, 123012, 23012, 2012, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172013, 0.0, 12.15, 6.675)
    ops.node(123013, 0.0, 12.15, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2013, 172013, 123013, 0.0625, 28224021.69655268, 11760009.04023028, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22013, 19.65552369, 0.00080764, 23.91240819, 0.02496111, 2.39124082, 0.08183911, -19.65552369, -0.00080764, -23.91240819, -0.02496111, -2.39124082, -0.08183911, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12013, 19.65552369, 0.00080764, 23.91240819, 0.02496111, 2.39124082, 0.08183911, -19.65552369, -0.00080764, -23.91240819, -0.02496111, -2.39124082, -0.08183911, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22013, 2013, 0.0, 60.97459078, 0.01615284, 60.97459078, 0.04845851, 42.68221354, -888.87967962, 0.05, 2, 0, 72013, 23013, 2, 3)
    ops.uniaxialMaterial('LimitState', 42013, 15.24364769, 7.217e-05, 45.73094308, 0.00021652, 152.43647694, 0.00072174, -15.24364769, -7.217e-05, -45.73094308, -0.00021652, -152.43647694, -0.00072174, 0.4, 0.3, 0.003, 0.0, 0.0, 22013, 2)
    ops.limitCurve('ThreePoint', 12013, 2013, 0.0, 60.97459078, 0.01615284, 60.97459078, 0.04845851, 42.68221354, -888.87967962, 0.05, 2, 0, 72013, 23013, 1, 3)
    ops.uniaxialMaterial('LimitState', 32013, 15.24364769, 7.217e-05, 45.73094308, 0.00021652, 152.43647694, 0.00072174, -15.24364769, -7.217e-05, -45.73094308, -0.00021652, -152.43647694, -0.00072174, 0.4, 0.3, 0.003, 0.0, 0.0, 12013, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2013, 99999, 'P', 42013, 'Vy', 32013, 'Vz', 22013, 'My', 12013, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172013, 72013, 172013, 2013, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123013, 123013, 23013, 2013, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172014, 2.9, 12.15, 6.675)
    ops.node(123014, 2.9, 12.15, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2014, 172014, 123014, 0.0875, 32715470.66364646, 13631446.10985269, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22014, 46.96292759, 0.00062239, 56.42191384, 0.03034201, 5.64219138, 0.10113632, -46.96292759, -0.00062239, -56.42191384, -0.03034201, -5.64219138, -0.10113632, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12014, 32.08700331, 0.00080916, 38.54977169, 0.02731026, 3.85497717, 0.08125101, -32.08700331, -0.00080916, -38.54977169, -0.02731026, -3.85497717, -0.08125101, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22014, 2014, 0.0, 95.94941753, 0.01244776, 95.94941753, 0.03734329, 67.16459227, -1035.39303201, 0.05, 2, 0, 72014, 23014, 2, 3)
    ops.uniaxialMaterial('LimitState', 42014, 23.98735438, 6.999e-05, 71.96206315, 0.00020996, 239.87354383, 0.00069986, -23.98735438, -6.999e-05, -71.96206315, -0.00020996, -239.87354383, -0.00069986, 0.4, 0.3, 0.003, 0.0, 0.0, 22014, 2)
    ops.limitCurve('ThreePoint', 12014, 2014, 0.0, 86.95550696, 0.01618328, 86.95550696, 0.04854983, 60.86885488, -722.36610011, 0.05, 2, 0, 72014, 23014, 1, 3)
    ops.uniaxialMaterial('LimitState', 32014, 21.73887674, 6.343e-05, 65.21663022, 0.00019028, 217.38876741, 0.00063426, -21.73887674, -6.343e-05, -65.21663022, -0.00019028, -217.38876741, -0.00063426, 0.4, 0.3, 0.003, 0.0, 0.0, 12014, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2014, 99999, 'P', 42014, 'Vy', 32014, 'Vz', 22014, 'My', 12014, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172014, 72014, 172014, 2014, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123014, 123014, 23014, 2014, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172015, 7.9, 12.15, 6.675)
    ops.node(123015, 7.9, 12.15, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2015, 172015, 123015, 0.1, 31525240.14797461, 13135516.72832276, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22015, 59.17898224, 0.00054511, 71.31469085, 0.03188498, 7.13146909, 0.10044287, -59.17898224, -0.00054511, -71.31469085, -0.03188498, -7.13146909, -0.10044287, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12015, 35.36863231, 0.00074301, 42.62160287, 0.02750892, 4.26216029, 0.0746645, -35.36863231, -0.00074301, -42.62160287, -0.02750892, -4.26216029, -0.0746645, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22015, 2015, 0.0, 105.96815046, 0.01090211, 105.96815046, 0.03270632, 74.17770532, -1126.78899156, 0.05, 2, 0, 72015, 23015, 2, 3)
    ops.uniaxialMaterial('LimitState', 42015, 26.49203761, 7.019e-05, 79.47611284, 0.00021056, 264.92037614, 0.00070186, -26.49203761, -7.019e-05, -79.47611284, -0.00021056, -264.92037614, -0.00070186, 0.4, 0.3, 0.003, 0.0, 0.0, 22015, 2)
    ops.limitCurve('ThreePoint', 12015, 2015, 0.0, 92.91159884, 0.01486015, 92.91159884, 0.04458046, 65.03811919, -714.46150258, 0.05, 2, 0, 72015, 23015, 1, 3)
    ops.uniaxialMaterial('LimitState', 32015, 23.22789971, 6.154e-05, 69.68369913, 0.00018461, 232.2789971, 0.00061538, -23.22789971, -6.154e-05, -69.68369913, -0.00018461, -232.2789971, -0.00061538, 0.4, 0.3, 0.003, 0.0, 0.0, 12015, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2015, 99999, 'P', 42015, 'Vy', 32015, 'Vz', 22015, 'My', 12015, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172015, 72015, 172015, 2015, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123015, 123015, 23015, 2015, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172016, 12.9, 12.15, 6.675)
    ops.node(123016, 12.9, 12.15, 9.025)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2016, 172016, 123016, 0.0875, 28698356.20047531, 11957648.41686471, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22016, 42.70447179, 0.00066793, 51.87623932, 0.01959871, 5.18762393, 0.07606155, -42.70447179, -0.00066793, -51.87623932, -0.01959871, -5.18762393, -0.07606155, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12016, 27.3260258, 0.00087861, 33.19491834, 0.0178549, 3.31949183, 0.06145644, -27.3260258, -0.00087861, -33.19491834, -0.0178549, -3.31949183, -0.06145644, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22016, 2016, 0.0, 76.93488514, 0.01335862, 76.93488514, 0.04007586, 53.8544196, -793.29841661, 0.05, 2, 0, 72016, 23016, 2, 3)
    ops.uniaxialMaterial('LimitState', 42016, 19.23372129, 6.397e-05, 57.70116386, 0.00019192, 192.33721286, 0.00063972, -19.23372129, -6.397e-05, -57.70116386, -0.00019192, -192.33721286, -0.00063972, 0.4, 0.3, 0.003, 0.0, 0.0, 22016, 2)
    ops.limitCurve('ThreePoint', 12016, 2016, 0.0, 59.50617924, 0.01757218, 59.50617924, 0.05271653, 41.65432547, -563.98260057, 0.05, 2, 0, 72016, 23016, 1, 3)
    ops.uniaxialMaterial('LimitState', 32016, 14.87654481, 4.948e-05, 44.62963443, 0.00014844, 148.76544809, 0.0004948, -14.87654481, -4.948e-05, -44.62963443, -0.00014844, -148.76544809, -0.0004948, 0.4, 0.3, 0.003, 0.0, 0.0, 12016, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2016, 99999, 'P', 42016, 'Vy', 32016, 'Vz', 22016, 'My', 12016, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172016, 72016, 172016, 2016, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123016, 123016, 23016, 2016, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172017, 0.0, 16.2, 6.65)
    ops.node(123017, 0.0, 16.2, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2017, 172017, 123017, 0.0625, 28096800.86488177, 11707000.3603674, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22017, 14.57454723, 0.00083121, 17.77457336, 0.02790636, 1.77745734, 0.0885125, -14.57454723, -0.00083121, -17.77457336, -0.02790636, -1.77745734, -0.0885125, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12017, 14.57454723, 0.00083121, 17.77457336, 0.02790636, 1.77745734, 0.0885125, -14.57454723, -0.00083121, -17.77457336, -0.02790636, -1.77745734, -0.0885125, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22017, 2017, 0.0, 59.73820773, 0.01662419, 59.73820773, 0.04987256, 41.81674541, -1190.54957615, 0.05, 2, 0, 72017, 23017, 2, 3)
    ops.uniaxialMaterial('LimitState', 42017, 14.93455193, 7.103e-05, 44.80365579, 0.00021309, 149.34551932, 0.00071031, -14.93455193, -7.103e-05, -44.80365579, -0.00021309, -149.34551932, -0.00071031, 0.4, 0.3, 0.003, 0.0, 0.0, 22017, 2)
    ops.limitCurve('ThreePoint', 12017, 2017, 0.0, 59.73820773, 0.01662419, 59.73820773, 0.04987256, 41.81674541, -1190.54957615, 0.05, 2, 0, 72017, 23017, 1, 3)
    ops.uniaxialMaterial('LimitState', 32017, 14.93455193, 7.103e-05, 44.80365579, 0.00021309, 149.34551932, 0.00071031, -14.93455193, -7.103e-05, -44.80365579, -0.00021309, -149.34551932, -0.00071031, 0.4, 0.3, 0.003, 0.0, 0.0, 12017, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2017, 99999, 'P', 42017, 'Vy', 32017, 'Vz', 22017, 'My', 12017, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172017, 72017, 172017, 2017, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123017, 123017, 23017, 2017, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172018, 2.9, 16.2, 6.65)
    ops.node(123018, 2.9, 16.2, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2018, 172018, 123018, 0.0625, 28393126.07904687, 11830469.19960286, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22018, 22.63057672, 0.00089032, 27.48494986, 0.02529359, 2.74849499, 0.08006301, -22.63057672, -0.00089032, -27.48494986, -0.02529359, -2.74849499, -0.08006301, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12018, 22.63057672, 0.00089032, 27.48494986, 0.02529359, 2.74849499, 0.08006301, -22.63057672, -0.00089032, -27.48494986, -0.02529359, -2.74849499, -0.08006301, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22018, 2018, 0.0, 63.0514186, 0.0178063, 63.0514186, 0.05341891, 44.13599302, -852.0534652, 0.05, 2, 0, 72018, 23018, 2, 3)
    ops.uniaxialMaterial('LimitState', 42018, 15.76285465, 7.419e-05, 47.28856395, 0.00022256, 157.62854651, 0.00074188, -15.76285465, -7.419e-05, -47.28856395, -0.00022256, -157.62854651, -0.00074188, 0.4, 0.3, 0.003, 0.0, 0.0, 22018, 2)
    ops.limitCurve('ThreePoint', 12018, 2018, 0.0, 63.0514186, 0.0178063, 63.0514186, 0.05341891, 44.13599302, -852.0534652, 0.05, 2, 0, 72018, 23018, 1, 3)
    ops.uniaxialMaterial('LimitState', 32018, 15.76285465, 7.419e-05, 47.28856395, 0.00022256, 157.62854651, 0.00074188, -15.76285465, -7.419e-05, -47.28856395, -0.00022256, -157.62854651, -0.00074188, 0.4, 0.3, 0.003, 0.0, 0.0, 12018, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2018, 99999, 'P', 42018, 'Vy', 32018, 'Vz', 22018, 'My', 12018, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172018, 72018, 172018, 2018, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123018, 123018, 23018, 2018, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172019, 7.9, 16.2, 6.65)
    ops.node(123019, 7.9, 16.2, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2019, 172019, 123019, 0.0875, 29025653.18559633, 12094022.16066514, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22019, 31.48512711, 0.00077745, 38.2144008, 0.03714075, 3.82144008, 0.10225185, -31.48512711, -0.00077745, -38.2144008, -0.03714075, -3.82144008, -0.10225185, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12019, 45.87567327, 0.00060999, 55.68061895, 0.04164614, 5.5680619, 0.12838181, -45.87567327, -0.00060999, -55.68061895, -0.04164614, -5.5680619, -0.12838181, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22019, 2019, 0.0, 84.07925611, 0.0155491, 84.07925611, 0.0466473, 58.85547928, -1014.87024462, 0.05, 2, 0, 72019, 23019, 2, 3)
    ops.uniaxialMaterial('LimitState', 42019, 21.01981403, 6.912e-05, 63.05944208, 0.00020737, 210.19814028, 0.00069124, -21.01981403, -6.912e-05, -63.05944208, -0.00020737, -210.19814028, -0.00069124, 0.4, 0.3, 0.003, 0.0, 0.0, 22019, 2)
    ops.limitCurve('ThreePoint', 12019, 2019, 0.0, 96.26771446, 0.01219989, 96.26771446, 0.03659967, 67.38740012, -1554.75376349, 0.05, 2, 0, 72019, 23019, 1, 3)
    ops.uniaxialMaterial('LimitState', 32019, 24.06692861, 7.914e-05, 72.20078584, 0.00023743, 240.66928615, 0.00079145, -24.06692861, -7.914e-05, -72.20078584, -0.00023743, -240.66928615, -0.00079145, 0.4, 0.3, 0.003, 0.0, 0.0, 12019, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2019, 99999, 'P', 42019, 'Vy', 32019, 'Vz', 22019, 'My', 12019, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172019, 72019, 172019, 2019, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123019, 123019, 23019, 2019, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172020, 12.9, 16.2, 6.65)
    ops.node(123020, 12.9, 16.2, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 2020, 172020, 123020, 0.0625, 33676743.05205359, 14031976.27168899, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 22020, 18.93587665, 0.00075422, 22.70091838, 0.02255513, 2.27009184, 0.08412115, -18.93587665, -0.00075422, -22.70091838, -0.02255513, -2.27009184, -0.08412115, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 12020, 18.93587665, 0.00075422, 22.70091838, 0.02255513, 2.27009184, 0.08412115, -18.93587665, -0.00075422, -22.70091838, -0.02255513, -2.27009184, -0.08412115, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 22020, 2020, 0.0, 66.97398951, 0.01508443, 66.97398951, 0.0452533, 46.88179265, -727.25198906, 0.05, 2, 0, 72020, 23020, 2, 3)
    ops.uniaxialMaterial('LimitState', 42020, 16.74349738, 6.644e-05, 50.23049213, 0.00019932, 167.43497377, 0.0006644, -16.74349738, -6.644e-05, -50.23049213, -0.00019932, -167.43497377, -0.0006644, 0.4, 0.3, 0.003, 0.0, 0.0, 22020, 2)
    ops.limitCurve('ThreePoint', 12020, 2020, 0.0, 66.97398951, 0.01508443, 66.97398951, 0.0452533, 46.88179265, -727.25198906, 0.05, 2, 0, 72020, 23020, 1, 3)
    ops.uniaxialMaterial('LimitState', 32020, 16.74349738, 6.644e-05, 50.23049213, 0.00019932, 167.43497377, 0.0006644, -16.74349738, -6.644e-05, -50.23049213, -0.00019932, -167.43497377, -0.0006644, 0.4, 0.3, 0.003, 0.0, 0.0, 12020, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 2020, 99999, 'P', 42020, 'Vy', 32020, 'Vz', 22020, 'My', 12020, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172020, 72020, 172020, 2020, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123020, 123020, 23020, 2020, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173003, 7.9, 0.0, 9.55)
    ops.node(124003, 7.9, 0.0, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3003, 173003, 124003, 0.0875, 27580987.97149002, 11492078.32145417, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23003, 20.16438318, 0.00075646, 24.65973678, 0.02517858, 2.46597368, 0.07409799, -20.16438318, -0.00075646, -24.65973678, -0.02517858, -2.46597368, -0.07409799, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13003, 32.69436492, 0.000597, 39.98309423, 0.02783086, 3.99830942, 0.09118019, -32.69436492, -0.000597, -39.98309423, -0.02783086, -3.99830942, -0.09118019, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23003, 3003, 0.0, 66.57180719, 0.01512913, 66.57180719, 0.04538739, 46.60026503, -1190.81140875, 0.05, 2, 0, 73003, 24003, 2, 3)
    ops.uniaxialMaterial('LimitState', 43003, 16.6429518, 5.76e-05, 49.92885539, 0.00017279, 166.42951798, 0.00057597, -16.6429518, -5.76e-05, -49.92885539, -0.00017279, -166.42951798, -0.00057597, 0.4, 0.3, 0.003, 0.0, 0.0, 23003, 2)
    ops.limitCurve('ThreePoint', 13003, 3003, 0.0, 75.92634299, 0.01194001, 75.92634299, 0.03582002, 53.14844009, -2079.65319847, 0.05, 2, 0, 73003, 24003, 1, 3)
    ops.uniaxialMaterial('LimitState', 33003, 18.98158575, 6.569e-05, 56.94475724, 0.00019707, 189.81585748, 0.00065691, -18.98158575, -6.569e-05, -56.94475724, -0.00019707, -189.81585748, -0.00065691, 0.4, 0.3, 0.003, 0.0, 0.0, 13003, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3003, 99999, 'P', 43003, 'Vy', 33003, 'Vz', 23003, 'My', 13003, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173003, 73003, 173003, 3003, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124003, 124003, 24003, 3003, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173004, 12.9, 0.0, 9.55)
    ops.node(124004, 12.9, 0.0, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3004, 173004, 124004, 0.0625, 27943078.5619329, 11642949.40080538, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23004, 14.28033536, 0.00081467, 17.45750562, 0.02286172, 1.74575056, 0.08720571, -14.28033536, -0.00081467, -17.45750562, -0.02286172, -1.74575056, -0.08720571, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13004, 14.28033536, 0.00081467, 17.45750562, 0.02286172, 1.74575056, 0.08720571, -14.28033536, -0.00081467, -17.45750562, -0.02286172, -1.74575056, -0.08720571, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23004, 3004, 0.0, 42.22148052, 0.01629347, 42.22148052, 0.04888042, 29.55503636, -1133.59252285, 0.05, 2, 0, 73004, 24004, 2, 3)
    ops.uniaxialMaterial('LimitState', 43004, 10.55537013, 5.048e-05, 31.66611039, 0.00015144, 105.5537013, 0.00050479, -10.55537013, -5.048e-05, -31.66611039, -0.00015144, -105.5537013, -0.00050479, 0.4, 0.3, 0.003, 0.0, 0.0, 23004, 2)
    ops.limitCurve('ThreePoint', 13004, 3004, 0.0, 42.22148052, 0.01629347, 42.22148052, 0.04888042, 29.55503636, -1133.59252285, 0.05, 2, 0, 73004, 24004, 1, 3)
    ops.uniaxialMaterial('LimitState', 33004, 10.55537013, 5.048e-05, 31.66611039, 0.00015144, 105.5537013, 0.00050479, -10.55537013, -5.048e-05, -31.66611039, -0.00015144, -105.5537013, -0.00050479, 0.4, 0.3, 0.003, 0.0, 0.0, 13004, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3004, 99999, 'P', 43004, 'Vy', 33004, 'Vz', 23004, 'My', 13004, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173004, 73004, 173004, 3004, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124004, 124004, 24004, 3004, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173005, 0.0, 4.05, 9.575)
    ops.node(124005, 0.0, 4.05, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3005, 173005, 124005, 0.0625, 31549734.78890552, 13145722.82871064, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23005, 16.93179582, 0.00074533, 20.47395083, 0.02000851, 2.04739508, 0.08342422, -16.93179582, -0.00074533, -20.47395083, -0.02000851, -2.04739508, -0.08342422, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13005, 16.93179582, 0.00074533, 20.47395083, 0.02000851, 2.04739508, 0.08342422, -16.93179582, -0.00074533, -20.47395083, -0.02000851, -2.04739508, -0.08342422, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23005, 3005, 0.0, 47.16572152, 0.01490665, 47.16572152, 0.04471995, 33.01600507, -783.93280141, 0.05, 2, 0, 73005, 24005, 2, 3)
    ops.uniaxialMaterial('LimitState', 43005, 11.79143038, 4.994e-05, 35.37429114, 0.00014983, 117.91430381, 0.00049944, -11.79143038, -4.994e-05, -35.37429114, -0.00014983, -117.91430381, -0.00049944, 0.4, 0.3, 0.003, 0.0, 0.0, 23005, 2)
    ops.limitCurve('ThreePoint', 13005, 3005, 0.0, 47.16572152, 0.01490665, 47.16572152, 0.04471995, 33.01600507, -783.93280141, 0.05, 2, 0, 73005, 24005, 1, 3)
    ops.uniaxialMaterial('LimitState', 33005, 11.79143038, 4.994e-05, 35.37429114, 0.00014983, 117.91430381, 0.00049944, -11.79143038, -4.994e-05, -35.37429114, -0.00014983, -117.91430381, -0.00049944, 0.4, 0.3, 0.003, 0.0, 0.0, 13005, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3005, 99999, 'P', 43005, 'Vy', 33005, 'Vz', 23005, 'My', 13005, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173005, 73005, 173005, 3005, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124005, 124005, 24005, 3005, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173006, 2.9, 4.05, 9.575)
    ops.node(124006, 2.9, 4.05, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3006, 173006, 124006, 0.0875, 30156650.95734419, 12565271.23222675, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23006, 41.13927097, 0.00061554, 49.93672882, 0.02713431, 4.99367288, 0.08122072, -41.13927097, -0.00061554, -49.93672882, -0.02713431, -4.99367288, -0.08122072, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13006, 28.11168164, 0.00078238, 34.12324501, 0.02468523, 3.4123245, 0.06696166, -28.11168164, -0.00078238, -34.12324501, -0.02468523, -3.4123245, -0.06696166, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23006, 3006, 0.0, 78.21208807, 0.0123109, 78.21208807, 0.03693269, 54.74846165, -1082.91656324, 0.05, 2, 0, 73006, 24006, 2, 3)
    ops.uniaxialMaterial('LimitState', 43006, 19.55302202, 6.189e-05, 58.65906605, 0.00018567, 195.53022018, 0.00061889, -19.55302202, -6.189e-05, -58.65906605, -0.00018567, -195.53022018, -0.00061889, 0.4, 0.3, 0.003, 0.0, 0.0, 23006, 2)
    ops.limitCurve('ThreePoint', 13006, 3006, 0.0, 65.44414427, 0.01564754, 65.44414427, 0.04694261, 45.81090099, -678.25019772, 0.05, 2, 0, 73006, 24006, 1, 3)
    ops.uniaxialMaterial('LimitState', 33006, 16.36103607, 5.179e-05, 49.0831082, 0.00015536, 163.61036067, 0.00051786, -16.36103607, -5.179e-05, -49.0831082, -0.00015536, -163.61036067, -0.00051786, 0.4, 0.3, 0.003, 0.0, 0.0, 13006, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3006, 99999, 'P', 43006, 'Vy', 33006, 'Vz', 23006, 'My', 13006, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173006, 73006, 173006, 3006, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124006, 124006, 24006, 3006, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173007, 7.9, 4.05, 9.575)
    ops.node(124007, 7.9, 4.05, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3007, 173007, 124007, 0.1, 29832229.11454792, 12430095.46439497, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23007, 47.09993261, 0.00058274, 57.24497857, 0.02612686, 5.72449786, 0.08073038, -47.09993261, -0.00058274, -57.24497857, -0.02612686, -5.72449786, -0.08073038, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13007, 27.51664239, 0.00081566, 33.44356387, 0.02297326, 3.34435639, 0.06194061, -27.51664239, -0.00081566, -33.44356387, -0.02297326, -3.34435639, -0.06194061, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23007, 3007, 0.0, 86.3047506, 0.01165488, 86.3047506, 0.03496464, 60.41332542, -1270.17766324, 0.05, 2, 0, 73007, 24007, 2, 3)
    ops.uniaxialMaterial('LimitState', 43007, 21.57618765, 6.041e-05, 64.72856295, 0.00018122, 215.76187651, 0.00060406, -21.57618765, -6.041e-05, -64.72856295, -0.00018122, -215.76187651, -0.00060406, 0.4, 0.3, 0.003, 0.0, 0.0, 23007, 2)
    ops.limitCurve('ThreePoint', 13007, 3007, 0.0, 67.70251037, 0.01631327, 67.70251037, 0.04893982, 47.39175726, -651.65166595, 0.05, 2, 0, 73007, 24007, 1, 3)
    ops.uniaxialMaterial('LimitState', 33007, 16.92562759, 4.739e-05, 50.77688278, 0.00014216, 169.25627592, 0.00047386, -16.92562759, -4.739e-05, -50.77688278, -0.00014216, -169.25627592, -0.00047386, 0.4, 0.3, 0.003, 0.0, 0.0, 13007, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3007, 99999, 'P', 43007, 'Vy', 33007, 'Vz', 23007, 'My', 13007, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173007, 73007, 173007, 3007, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124007, 124007, 24007, 3007, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173008, 12.9, 4.05, 9.575)
    ops.node(124008, 12.9, 4.05, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3008, 173008, 124008, 0.0875, 31647634.1778168, 13186514.240757, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23008, 32.80232216, 0.00057823, 39.67673828, 0.02430534, 3.96767383, 0.08892567, -32.80232216, -0.00057823, -39.67673828, -0.02430534, -3.96767383, -0.08892567, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13008, 20.31112003, 0.00072868, 24.56774217, 0.02200611, 2.45677422, 0.071907, -20.31112003, -0.00072868, -24.56774217, -0.02200611, -2.45677422, -0.071907, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23008, 3008, 0.0, 86.53240889, 0.01156462, 86.53240889, 0.03469385, 60.57268622, -2078.97851043, 0.05, 2, 0, 73008, 24008, 2, 3)
    ops.uniaxialMaterial('LimitState', 43008, 21.63310222, 6.525e-05, 64.89930667, 0.00019574, 216.33102223, 0.00065247, -21.63310222, -6.525e-05, -64.89930667, -0.00019574, -216.33102223, -0.00065247, 0.4, 0.3, 0.003, 0.0, 0.0, 23008, 2)
    ops.limitCurve('ThreePoint', 13008, 3008, 0.0, 77.13187363, 0.0145736, 77.13187363, 0.04372081, 53.99231154, -1191.27395336, 0.05, 2, 0, 73008, 24008, 1, 3)
    ops.uniaxialMaterial('LimitState', 33008, 19.28296841, 5.816e-05, 57.84890522, 0.00017448, 192.82968407, 0.00058159, -19.28296841, -5.816e-05, -57.84890522, -0.00017448, -192.82968407, -0.00058159, 0.4, 0.3, 0.003, 0.0, 0.0, 13008, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3008, 99999, 'P', 43008, 'Vy', 33008, 'Vz', 23008, 'My', 13008, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173008, 73008, 173008, 3008, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124008, 124008, 24008, 3008, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173009, 0.0, 8.1, 9.575)
    ops.node(124009, 0.0, 8.1, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3009, 173009, 124009, 0.0625, 27124967.12587672, 11302069.63578197, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23009, 13.4510804, 0.00079411, 16.47108998, 0.02750535, 1.647109, 0.09125269, -13.4510804, -0.00079411, -16.47108998, -0.02750535, -1.647109, -0.09125269, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13009, 13.4510804, 0.00079411, 16.47108998, 0.02750535, 1.647109, 0.09125269, -13.4510804, -0.00079411, -16.47108998, -0.02750535, -1.647109, -0.09125269, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23009, 3009, 0.0, 53.67429183, 0.01588216, 53.67429183, 0.04764649, 37.57200428, -1757.6577468, 0.05, 2, 0, 73009, 24009, 2, 3)
    ops.uniaxialMaterial('LimitState', 43009, 13.41857296, 6.611e-05, 40.25571887, 0.00019832, 134.18572957, 0.00066107, -13.41857296, -6.611e-05, -40.25571887, -0.00019832, -134.18572957, -0.00066107, 0.4, 0.3, 0.003, 0.0, 0.0, 23009, 2)
    ops.limitCurve('ThreePoint', 13009, 3009, 0.0, 53.67429183, 0.01588216, 53.67429183, 0.04764649, 37.57200428, -1757.6577468, 0.05, 2, 0, 73009, 24009, 1, 3)
    ops.uniaxialMaterial('LimitState', 33009, 13.41857296, 6.611e-05, 40.25571887, 0.00019832, 134.18572957, 0.00066107, -13.41857296, -6.611e-05, -40.25571887, -0.00019832, -134.18572957, -0.00066107, 0.4, 0.3, 0.003, 0.0, 0.0, 13009, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3009, 99999, 'P', 43009, 'Vy', 33009, 'Vz', 23009, 'My', 13009, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173009, 73009, 173009, 3009, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124009, 124009, 24009, 3009, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173010, 2.9, 8.1, 9.575)
    ops.node(124010, 2.9, 8.1, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3010, 173010, 124010, 0.0875, 25891560.66763712, 10788150.27818213, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23010, 37.78106384, 0.00062596, 46.32920953, 0.02719526, 4.63292095, 0.08035252, -37.78106384, -0.00062596, -46.32920953, -0.02719526, -4.63292095, -0.08035252, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13010, 25.68148632, 0.0008016, 31.49204494, 0.02475, 3.14920449, 0.06630016, -25.68148632, -0.0008016, -31.49204494, -0.02475, -3.14920449, -0.06630016, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23010, 3010, 0.0, 65.04952558, 0.01251921, 65.04952558, 0.03755764, 45.53466791, -1151.05161622, 0.05, 2, 0, 73010, 24010, 2, 3)
    ops.uniaxialMaterial('LimitState', 43010, 16.2623814, 5.995e-05, 48.78714419, 0.00017986, 162.62381395, 0.00059953, -16.2623814, -5.995e-05, -48.78714419, -0.00017986, -162.62381395, -0.00059953, 0.4, 0.3, 0.003, 0.0, 0.0, 23010, 2)
    ops.limitCurve('ThreePoint', 13010, 3010, 0.0, 49.85739003, 0.01603193, 49.85739003, 0.04809578, 34.90017302, -698.563877, 0.05, 2, 0, 73010, 24010, 1, 3)
    ops.uniaxialMaterial('LimitState', 33010, 12.46434751, 4.595e-05, 37.39304252, 0.00013785, 124.64347507, 0.00045951, -12.46434751, -4.595e-05, -37.39304252, -0.00013785, -124.64347507, -0.00045951, 0.4, 0.3, 0.003, 0.0, 0.0, 13010, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3010, 99999, 'P', 43010, 'Vy', 33010, 'Vz', 23010, 'My', 13010, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173010, 73010, 173010, 3010, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124010, 124010, 24010, 3010, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173011, 7.9, 8.1, 9.575)
    ops.node(124011, 7.9, 8.1, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3011, 173011, 124011, 0.1, 29951790.31460587, 12479912.63108578, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23011, 49.08722851, 0.00059559, 59.6411052, 0.02156176, 5.96411052, 0.07620944, -49.08722851, -0.00059559, -59.6411052, -0.02156176, -5.96411052, -0.07620944, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13011, 28.75985443, 0.00083216, 34.94329494, 0.01901874, 3.49432949, 0.0580176, -28.75985443, -0.00083216, -34.94329494, -0.01901874, -3.49432949, -0.0580176, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23011, 3011, 0.0, 82.09468759, 0.01191171, 82.09468759, 0.03573514, 57.46628132, -986.93518107, 0.05, 2, 0, 73011, 24011, 2, 3)
    ops.uniaxialMaterial('LimitState', 43011, 20.5236719, 5.723e-05, 61.57101569, 0.00017169, 205.23671898, 0.0005723, -20.5236719, -5.723e-05, -61.57101569, -0.00017169, -205.23671898, -0.0005723, 0.4, 0.3, 0.003, 0.0, 0.0, 23011, 2)
    ops.limitCurve('ThreePoint', 13011, 3011, 0.0, 57.52984246, 0.01664322, 57.52984246, 0.04992967, 40.27088972, -523.83544573, 0.05, 2, 0, 73011, 24011, 1, 3)
    ops.uniaxialMaterial('LimitState', 33011, 14.38246061, 4.011e-05, 43.14738184, 0.00012032, 143.82460614, 0.00040105, -14.38246061, -4.011e-05, -43.14738184, -0.00012032, -143.82460614, -0.00040105, 0.4, 0.3, 0.003, 0.0, 0.0, 13011, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3011, 99999, 'P', 43011, 'Vy', 33011, 'Vz', 23011, 'My', 13011, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173011, 73011, 173011, 3011, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124011, 124011, 24011, 3011, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173012, 12.9, 8.1, 9.575)
    ops.node(124012, 12.9, 8.1, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3012, 173012, 124012, 0.0875, 35698018.23574786, 14874174.26489494, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23012, 33.02255777, 0.0005694, 39.33809329, 0.01861604, 3.93380933, 0.08399573, -33.02255777, -0.0005694, -39.33809329, -0.01861604, -3.93380933, -0.08399573, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13012, 20.51552935, 0.00071634, 24.43910654, 0.01689978, 2.44391065, 0.06738706, -20.51552935, -0.00071634, -24.43910654, -0.01689978, -2.44391065, -0.06738706, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23012, 3012, 0.0, 89.75384399, 0.01138799, 89.75384399, 0.03416396, 62.82769079, -1302.17998567, 0.05, 2, 0, 73012, 24012, 2, 3)
    ops.uniaxialMaterial('LimitState', 43012, 22.438461, 6e-05, 67.31538299, 0.00017999, 224.38460997, 0.00059997, -22.438461, -6e-05, -67.31538299, -0.00017999, -224.38460997, -0.00059997, 0.4, 0.3, 0.003, 0.0, 0.0, 23012, 2)
    ops.limitCurve('ThreePoint', 13012, 3012, 0.0, 72.78573805, 0.01432679, 72.78573805, 0.04298036, 50.95001663, -768.50475518, 0.05, 2, 0, 73012, 24012, 1, 3)
    ops.uniaxialMaterial('LimitState', 33012, 18.19643451, 4.865e-05, 54.58930353, 0.00014596, 181.96434511, 0.00048655, -18.19643451, -4.865e-05, -54.58930353, -0.00014596, -181.96434511, -0.00048655, 0.4, 0.3, 0.003, 0.0, 0.0, 13012, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3012, 99999, 'P', 43012, 'Vy', 33012, 'Vz', 23012, 'My', 13012, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173012, 73012, 173012, 3012, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124012, 124012, 24012, 3012, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173013, 0.0, 12.15, 9.575)
    ops.node(124013, 0.0, 12.15, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3013, 173013, 124013, 0.0625, 31291733.24726329, 13038222.1863597, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23013, 14.98942726, 0.00076913, 18.15505734, 0.02364065, 1.81550573, 0.08858111, -14.98942726, -0.00076913, -18.15505734, -0.02364065, -1.81550573, -0.08858111, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13013, 14.98942726, 0.00076913, 18.15505734, 0.02364065, 1.81550573, 0.08858111, -14.98942726, -0.00076913, -18.15505734, -0.02364065, -1.81550573, -0.08858111, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23013, 3013, 0.0, 57.84200964, 0.01538262, 57.84200964, 0.04614786, 40.48940675, -1459.14059034, 0.05, 2, 0, 73013, 24013, 2, 3)
    ops.uniaxialMaterial('LimitState', 43013, 14.46050241, 6.175e-05, 43.38150723, 0.00018526, 144.6050241, 0.00061754, -14.46050241, -6.175e-05, -43.38150723, -0.00018526, -144.6050241, -0.00061754, 0.4, 0.3, 0.003, 0.0, 0.0, 23013, 2)
    ops.limitCurve('ThreePoint', 13013, 3013, 0.0, 57.84200964, 0.01538262, 57.84200964, 0.04614786, 40.48940675, -1459.14059034, 0.05, 2, 0, 73013, 24013, 1, 3)
    ops.uniaxialMaterial('LimitState', 33013, 14.46050241, 6.175e-05, 43.38150723, 0.00018526, 144.6050241, 0.00061754, -14.46050241, -6.175e-05, -43.38150723, -0.00018526, -144.6050241, -0.00061754, 0.4, 0.3, 0.003, 0.0, 0.0, 13013, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3013, 99999, 'P', 43013, 'Vy', 33013, 'Vz', 23013, 'My', 13013, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173013, 73013, 173013, 3013, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124013, 124013, 24013, 3013, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173014, 2.9, 12.15, 9.575)
    ops.node(124014, 2.9, 12.15, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3014, 173014, 124014, 0.0875, 27557530.63483626, 11482304.43118177, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23014, 35.62697285, 0.00059413, 43.54830658, 0.02442949, 4.35483066, 0.0784707, -35.62697285, -0.00059413, -43.54830658, -0.02442949, -4.35483066, -0.0784707, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13014, 24.1557218, 0.00075941, 29.52652708, 0.02224356, 2.95265271, 0.06448467, -24.1557218, -0.00075941, -29.52652708, -0.02224356, -2.95265271, -0.06448467, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23014, 3014, 0.0, 66.49548548, 0.01188252, 66.49548548, 0.03564756, 46.54683984, -977.67726531, 0.05, 2, 0, 73014, 24014, 2, 3)
    ops.uniaxialMaterial('LimitState', 43014, 16.62387137, 5.758e-05, 49.87161411, 0.00017274, 166.2387137, 0.0005758, -16.62387137, -5.758e-05, -49.87161411, -0.00017274, -166.2387137, -0.0005758, 0.4, 0.3, 0.003, 0.0, 0.0, 23014, 2)
    ops.limitCurve('ThreePoint', 13014, 3014, 0.0, 44.18131866, 0.01518813, 44.18131866, 0.04556439, 30.92692306, -601.76232674, 0.05, 2, 0, 73014, 24014, 1, 3)
    ops.uniaxialMaterial('LimitState', 33014, 11.04532967, 3.826e-05, 33.135989, 0.00011477, 110.45329665, 0.00038258, -11.04532967, -3.826e-05, -33.135989, -0.00011477, -110.45329665, -0.00038258, 0.4, 0.3, 0.003, 0.0, 0.0, 13014, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3014, 99999, 'P', 43014, 'Vy', 33014, 'Vz', 23014, 'My', 13014, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173014, 73014, 173014, 3014, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124014, 124014, 24014, 3014, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173015, 7.9, 12.15, 9.575)
    ops.node(124015, 7.9, 12.15, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3015, 173015, 124015, 0.1, 30604419.50546829, 12751841.46061179, 0.00127345, 0.00057292, 0.00146667, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23015, 48.86832892, 0.00055689, 59.26688628, 0.02578428, 5.92668863, 0.08066059, -48.86832892, -0.00055689, -59.26688628, -0.02578428, -5.92668863, -0.08066059, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13015, 29.11531268, 0.00075027, 35.31068001, 0.02263313, 3.531068, 0.06179515, -29.11531268, -0.00075027, -35.31068001, -0.02263313, -3.531068, -0.06179515, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23015, 3015, 0.0, 89.88649366, 0.01113785, 89.88649366, 0.03341354, 62.92054556, -1356.59341562, 0.05, 2, 0, 73015, 24015, 2, 3)
    ops.uniaxialMaterial('LimitState', 43015, 22.47162342, 6.133e-05, 67.41487025, 0.00018398, 224.71623415, 0.00061325, -22.47162342, -6.133e-05, -67.41487025, -0.00018398, -224.71623415, -0.00061325, 0.4, 0.3, 0.003, 0.0, 0.0, 23015, 2)
    ops.limitCurve('ThreePoint', 13015, 3015, 0.0, 70.22375083, 0.01500539, 70.22375083, 0.04501616, 49.15662558, -690.25608178, 0.05, 2, 0, 73015, 24015, 1, 3)
    ops.uniaxialMaterial('LimitState', 33015, 17.55593771, 4.791e-05, 52.66781312, 0.00014373, 175.55937708, 0.0004791, -17.55593771, -4.791e-05, -52.66781312, -0.00014373, -175.55937708, -0.0004791, 0.4, 0.3, 0.003, 0.0, 0.0, 13015, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3015, 99999, 'P', 43015, 'Vy', 33015, 'Vz', 23015, 'My', 13015, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173015, 73015, 173015, 3015, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124015, 124015, 24015, 3015, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173016, 12.9, 12.15, 9.575)
    ops.node(124016, 12.9, 12.15, 11.95)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3016, 173016, 124016, 0.0875, 27451092.18970525, 11437955.07904386, 0.0010204, 0.0005013, 0.00098255, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23016, 33.31662474, 0.00063982, 40.75467637, 0.02202872, 4.07546764, 0.08527851, -33.31662474, -0.00063982, -40.75467637, -0.02202872, -4.07546764, -0.08527851, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13016, 20.62391671, 0.00083015, 25.22827741, 0.02001077, 2.52282774, 0.06885332, -20.62391671, -0.00083015, -25.22827741, -0.02001077, -2.52282774, -0.06885332, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23016, 3016, 0.0, 69.50330983, 0.01279632, 69.50330983, 0.03838895, 48.65231688, -1456.78849974, 0.05, 2, 0, 73016, 24016, 2, 3)
    ops.uniaxialMaterial('LimitState', 43016, 17.37582746, 6.042e-05, 52.12748237, 0.00018125, 173.75827458, 0.00060418, -17.37582746, -6.042e-05, -52.12748237, -0.00018125, -173.75827458, -0.00060418, 0.4, 0.3, 0.003, 0.0, 0.0, 23016, 2)
    ops.limitCurve('ThreePoint', 13016, 3016, 0.0, 53.4570191, 0.01660297, 53.4570191, 0.0498089, 37.41991337, -853.1762548, 0.05, 2, 0, 73016, 24016, 1, 3)
    ops.uniaxialMaterial('LimitState', 33016, 13.36425477, 4.647e-05, 40.09276432, 0.00013941, 133.64254775, 0.00046469, -13.36425477, -4.647e-05, -40.09276432, -0.00013941, -133.64254775, -0.00046469, 0.4, 0.3, 0.003, 0.0, 0.0, 13016, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3016, 99999, 'P', 43016, 'Vy', 33016, 'Vz', 23016, 'My', 13016, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173016, 73016, 173016, 3016, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124016, 124016, 24016, 3016, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173017, 0.0, 16.2, 9.55)
    ops.node(124017, 0.0, 16.2, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3017, 173017, 124017, 0.0625, 34968064.05786089, 14570026.69077537, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23017, 13.2160441, 0.00068396, 15.79967626, 0.02115343, 1.57996763, 0.08732625, -13.2160441, -0.00068396, -15.79967626, -0.02115343, -1.57996763, -0.08732625, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13017, 13.2160441, 0.00068396, 15.79967626, 0.02115343, 1.57996763, 0.08732625, -13.2160441, -0.00068396, -15.79967626, -0.02115343, -1.57996763, -0.08732625, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23017, 3017, 0.0, 58.57952944, 0.0136792, 58.57952944, 0.0410376, 41.00567061, -2233.11935735, 0.05, 2, 0, 73017, 24017, 2, 3)
    ops.uniaxialMaterial('LimitState', 43017, 14.64488236, 5.597e-05, 43.93464708, 0.0001679, 146.44882361, 0.00055966, -14.64488236, -5.597e-05, -43.93464708, -0.0001679, -146.44882361, -0.00055966, 0.4, 0.3, 0.003, 0.0, 0.0, 23017, 2)
    ops.limitCurve('ThreePoint', 13017, 3017, 0.0, 58.57952944, 0.0136792, 58.57952944, 0.0410376, 41.00567061, -2233.11935735, 0.05, 2, 0, 73017, 24017, 1, 3)
    ops.uniaxialMaterial('LimitState', 33017, 14.64488236, 5.597e-05, 43.93464708, 0.0001679, 146.44882361, 0.00055966, -14.64488236, -5.597e-05, -43.93464708, -0.0001679, -146.44882361, -0.00055966, 0.4, 0.3, 0.003, 0.0, 0.0, 13017, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3017, 99999, 'P', 43017, 'Vy', 33017, 'Vz', 23017, 'My', 13017, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173017, 73017, 173017, 3017, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124017, 124017, 24017, 3017, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173018, 2.9, 16.2, 9.55)
    ops.node(124018, 2.9, 16.2, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3018, 173018, 124018, 0.0625, 28702396.30429944, 11959331.7934581, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23018, 14.61848609, 0.00072928, 17.82817984, 0.02092474, 1.78281798, 0.08443731, -14.61848609, -0.00072928, -17.82817984, -0.02092474, -1.78281798, -0.08443731, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13018, 14.61848609, 0.00072928, 17.82817984, 0.02092474, 1.78281798, 0.08443731, -14.61848609, -0.00072928, -17.82817984, -0.02092474, -1.78281798, -0.08443731, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23018, 3018, 0.0, 38.27610901, 0.01458555, 38.27610901, 0.04375665, 26.79327631, -1039.71591689, 0.05, 2, 0, 73018, 24018, 2, 3)
    ops.uniaxialMaterial('LimitState', 43018, 9.56902725, 4.455e-05, 28.70708176, 0.00013365, 95.69027253, 0.00044551, -9.56902725, -4.455e-05, -28.70708176, -0.00013365, -95.69027253, -0.00044551, 0.4, 0.3, 0.003, 0.0, 0.0, 23018, 2)
    ops.limitCurve('ThreePoint', 13018, 3018, 0.0, 38.27610901, 0.01458555, 38.27610901, 0.04375665, 26.79327631, -1039.71591689, 0.05, 2, 0, 73018, 24018, 1, 3)
    ops.uniaxialMaterial('LimitState', 33018, 9.56902725, 4.455e-05, 28.70708176, 0.00013365, 95.69027253, 0.00044551, -9.56902725, -4.455e-05, -28.70708176, -0.00013365, -95.69027253, -0.00044551, 0.4, 0.3, 0.003, 0.0, 0.0, 13018, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3018, 99999, 'P', 43018, 'Vy', 33018, 'Vz', 23018, 'My', 13018, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173018, 73018, 173018, 3018, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124018, 124018, 24018, 3018, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173019, 7.9, 16.2, 9.55)
    ops.node(124019, 7.9, 16.2, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3019, 173019, 124019, 0.0875, 32955291.79842982, 13731371.58267909, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23019, 24.46042895, 0.00081303, 29.45623096, 0.01853212, 2.9456231, 0.06253621, -24.46042895, -0.00081303, -29.45623096, -0.01853212, -2.9456231, -0.06253621, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13019, 36.3196227, 0.00062252, 43.73754837, 0.02028077, 4.37375484, 0.07657747, -36.3196227, -0.00062252, -43.73754837, -0.02028077, -4.37375484, -0.07657747, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23019, 3019, 0.0, 57.14179801, 0.01626059, 57.14179801, 0.04878176, 39.99925861, -641.56823211, 0.05, 2, 0, 73019, 24019, 2, 3)
    ops.uniaxialMaterial('LimitState', 43019, 14.2854495, 4.138e-05, 42.85634851, 0.00012413, 142.85449503, 0.00041376, -14.2854495, -4.138e-05, -42.85634851, -0.00012413, -142.85449503, -0.00041376, 0.4, 0.3, 0.003, 0.0, 0.0, 23019, 2)
    ops.limitCurve('ThreePoint', 13019, 3019, 0.0, 77.53685071, 0.01245037, 77.53685071, 0.0373511, 54.2757955, -1072.73944503, 0.05, 2, 0, 73019, 24019, 1, 3)
    ops.uniaxialMaterial('LimitState', 33019, 19.38421268, 5.614e-05, 58.15263803, 0.00016843, 193.84212678, 0.00056144, -19.38421268, -5.614e-05, -58.15263803, -0.00016843, -193.84212678, -0.00056144, 0.4, 0.3, 0.003, 0.0, 0.0, 13019, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3019, 99999, 'P', 43019, 'Vy', 33019, 'Vz', 23019, 'My', 13019, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173019, 73019, 173019, 3019, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124019, 124019, 24019, 3019, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173020, 12.9, 16.2, 9.55)
    ops.node(124020, 12.9, 16.2, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 3020, 173020, 124020, 0.0625, 35529751.58766035, 14804063.16152515, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 23020, 15.54640657, 0.00070843, 18.53699421, 0.0249472, 1.85369942, 0.09071118, -15.54640657, -0.00070843, -18.53699421, -0.0249472, -1.85369942, -0.09071118, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 13020, 15.54640657, 0.00070843, 18.53699421, 0.0249472, 1.85369942, 0.09071118, -15.54640657, -0.00070843, -18.53699421, -0.0249472, -1.85369942, -0.09071118, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 23020, 3020, 0.0, 73.29776761, 0.01416856, 73.29776761, 0.04250567, 51.30843733, -2502.46773255, 0.05, 2, 0, 73020, 24020, 2, 3)
    ops.uniaxialMaterial('LimitState', 43020, 18.3244419, 6.892e-05, 54.97332571, 0.00020676, 183.24441902, 0.00068921, -18.3244419, -6.892e-05, -54.97332571, -0.00020676, -183.24441902, -0.00068921, 0.4, 0.3, 0.003, 0.0, 0.0, 23020, 2)
    ops.limitCurve('ThreePoint', 13020, 3020, 0.0, 73.29776761, 0.01416856, 73.29776761, 0.04250567, 51.30843733, -2502.46773255, 0.05, 2, 0, 73020, 24020, 1, 3)
    ops.uniaxialMaterial('LimitState', 33020, 18.3244419, 6.892e-05, 54.97332571, 0.00020676, 183.24441902, 0.00068921, -18.3244419, -6.892e-05, -54.97332571, -0.00020676, -183.24441902, -0.00068921, 0.4, 0.3, 0.003, 0.0, 0.0, 13020, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 3020, 99999, 'P', 43020, 'Vy', 33020, 'Vz', 23020, 'My', 13020, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173020, 73020, 173020, 3020, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124020, 124020, 24020, 3020, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170001, 0.0, 0.0, 0.0)
    ops.node(124021, 0.0, 0.0, 1.55)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4052, 170001, 124021, 0.0625, 28922270.60143225, 12050946.0839301, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24052, 30.80700693, 0.00076024, 37.26306234, 0.0413045, 3.72630623, 0.11894166, -30.80700693, -0.00076024, -37.26306234, -0.0413045, -3.72630623, -0.11894166, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14052, 28.88950492, 0.00076024, 34.94371996, 0.0413045, 3.494372, 0.11894166, -28.88950492, -0.00076024, -34.94371996, -0.0413045, -3.494372, -0.11894166, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24052, 4052, 0.0, 84.5906835, 0.01520474, 84.5906835, 0.04561422, 59.21347845, -2458.42135716, 0.05, 2, 0, 70001, 24021, 2, 3)
    ops.uniaxialMaterial('LimitState', 44052, 21.14767088, 5.896e-05, 63.44301263, 0.00017689, 211.47670876, 0.00058963, -21.14767088, -5.896e-05, -63.44301263, -0.00017689, -211.47670876, -0.00058963, 0.4, 0.3, 0.003, 0.0, 0.0, 24052, 2)
    ops.limitCurve('ThreePoint', 14052, 4052, 0.0, 84.5906835, 0.01520474, 84.5906835, 0.04561422, 59.21347845, -2458.42135716, 0.05, 2, 0, 70001, 24021, 1, 3)
    ops.uniaxialMaterial('LimitState', 34052, 21.14767088, 5.896e-05, 63.44301263, 0.00017689, 211.47670876, 0.00058963, -21.14767088, -5.896e-05, -63.44301263, -0.00017689, -211.47670876, -0.00058963, 0.4, 0.3, 0.003, 0.0, 0.0, 14052, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4052, 99999, 'P', 44052, 'Vy', 34052, 'Vz', 24052, 'My', 14052, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170001, 70001, 170001, 4052, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124021, 124021, 24021, 4052, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174021, 0.0, 0.0, 1.95)
    ops.node(121001, 0.0, 0.0, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4053, 174021, 121001, 0.0625, 27285601.97141774, 11369000.82142406, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24053, 27.70521264, 0.00075046, 33.64981628, 0.05407222, 3.36498163, 0.15407222, -27.70521264, -0.00075046, -33.64981628, -0.05407222, -3.36498163, -0.15407222, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14053, 25.96391717, 0.00075046, 31.53489756, 0.05407222, 3.15348976, 0.15407222, -25.96391717, -0.00075046, -31.53489756, -0.05407222, -3.15348976, -0.15407222, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24053, 4053, 0.0, 88.54987618, 0.01500921, 88.54987618, 0.04502762, 61.98491333, -3381.45825588, 0.05, 2, 0, 74021, 21001, 2, 3)
    ops.uniaxialMaterial('LimitState', 44053, 22.13746904, 6.543e-05, 66.41240713, 0.00019628, 221.37469045, 0.00065425, -22.13746904, -6.543e-05, -66.41240713, -0.00019628, -221.37469045, -0.00065425, 0.4, 0.3, 0.003, 0.0, 0.0, 24053, 2)
    ops.limitCurve('ThreePoint', 14053, 4053, 0.0, 88.54987618, 0.01500921, 88.54987618, 0.04502762, 61.98491333, -3381.45825588, 0.05, 2, 0, 74021, 21001, 1, 3)
    ops.uniaxialMaterial('LimitState', 34053, 22.13746904, 6.543e-05, 66.41240713, 0.00019628, 221.37469045, 0.00065425, -22.13746904, -6.543e-05, -66.41240713, -0.00019628, -221.37469045, -0.00065425, 0.4, 0.3, 0.003, 0.0, 0.0, 14053, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4053, 99999, 'P', 44053, 'Vy', 34053, 'Vz', 24053, 'My', 14053, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174021, 74021, 174021, 4053, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121001, 121001, 21001, 4053, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(170002, 2.9, 0.0, 0.0)
    ops.node(124022, 2.9, 0.0, 1.55)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4054, 170002, 124022, 0.14, 30334364.10172336, 12639318.37571807, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24054, 94.87298653, 0.00062778, 114.56614384, 0.05869022, 11.45661438, 0.15869022, -94.87298653, -0.00062778, -114.56614384, -0.05869022, -11.45661438, -0.15869022, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14054, 97.65761555, 0.00058292, 117.9287892, 0.0529632, 11.79287892, 0.14156162, -97.65761555, -0.00058292, -117.9287892, -0.0529632, -11.79287892, -0.14156162, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24054, 4054, 0.0, 208.09354112, 0.01255553, 208.09354112, 0.03766658, 145.66547878, -4826.0005929, 0.05, 2, 0, 70002, 24022, 2, 3)
    ops.uniaxialMaterial('LimitState', 44054, 52.02338528, 6.174e-05, 156.07015584, 0.00018522, 520.2338528, 0.0006174, -52.02338528, -6.174e-05, -156.07015584, -0.00018522, -520.2338528, -0.0006174, 0.4, 0.3, 0.003, 0.0, 0.0, 24054, 2)
    ops.limitCurve('ThreePoint', 14054, 4054, 0.0, 285.67881389, 0.01165834, 285.67881389, 0.03497501, 199.97516972, -10227.62142603, 0.05, 2, 0, 70002, 24022, 1, 3)
    ops.uniaxialMaterial('LimitState', 34054, 71.41970347, 8.476e-05, 214.25911042, 0.00025428, 714.19703472, 0.00084759, -71.41970347, -8.476e-05, -214.25911042, -0.00025428, -714.19703472, -0.00084759, 0.4, 0.3, 0.003, 0.0, 0.0, 14054, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4054, 99999, 'P', 44054, 'Vy', 34054, 'Vz', 24054, 'My', 14054, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 170002, 70002, 170002, 4054, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124022, 124022, 24022, 4054, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174022, 2.9, 0.0, 1.95)
    ops.node(121002, 2.9, 0.0, 3.25)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4055, 174022, 121002, 0.14, 31677887.20402108, 13199119.66834212, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24055, 86.08320748, 0.00057191, 103.66468501, 0.0515399, 10.3664685, 0.1515399, -86.08320748, -0.00057191, -103.66468501, -0.0515399, -10.3664685, -0.1515399, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14055, 90.32246751, 0.00054241, 108.76976379, 0.04652252, 10.87697638, 0.13920105, -90.32246751, -0.00054241, -108.76976379, -0.04652252, -10.87697638, -0.13920105, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24055, 4055, 0.0, 188.45972321, 0.01143823, 188.45972321, 0.0343147, 131.92180625, -3218.44692272, 0.05, 2, 0, 74022, 21002, 2, 3)
    ops.uniaxialMaterial('LimitState', 44055, 47.1149308, 5.354e-05, 141.34479241, 0.00016063, 471.14930802, 0.00053543, -47.1149308, -5.354e-05, -141.34479241, -0.00016063, -471.14930802, -0.00053543, 0.4, 0.3, 0.003, 0.0, 0.0, 24055, 2)
    ops.limitCurve('ThreePoint', 14055, 4055, 0.0, 249.09234235, 0.01084813, 249.09234235, 0.0325444, 174.36463965, -6424.7292616, 0.05, 2, 0, 74022, 21002, 1, 3)
    ops.uniaxialMaterial('LimitState', 34055, 62.27308559, 7.077e-05, 186.81925676, 0.00021231, 622.73085588, 0.0007077, -62.27308559, -7.077e-05, -186.81925676, -0.00021231, -622.73085588, -0.0007077, 0.4, 0.3, 0.003, 0.0, 0.0, 14055, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4055, 99999, 'P', 44055, 'Vy', 34055, 'Vz', 24055, 'My', 14055, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174022, 74022, 174022, 4055, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 121002, 121002, 21002, 4055, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171001, 0.0, 0.0, 3.75)
    ops.node(124023, 0.0, 0.0, 4.775)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4057, 171001, 124023, 0.0625, 32556606.65133039, 13565252.77138766, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24057, 22.80320048, 0.00057915, 27.39785371, 0.02873651, 2.73978537, 0.09847292, -22.80320048, -0.00057915, -27.39785371, -0.02873651, -2.73978537, -0.09847292, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14057, 22.80320048, 0.00057915, 27.39785371, 0.02873651, 2.73978537, 0.09847292, -22.80320048, -0.00057915, -27.39785371, -0.02873651, -2.73978537, -0.09847292, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24057, 4057, 0.0, 78.44246722, 0.01158303, 78.44246722, 0.03474909, 54.90972706, -1818.48535885, 0.05, 2, 0, 71001, 24023, 2, 3)
    ops.uniaxialMaterial('LimitState', 44057, 19.61061681, 4.025e-05, 58.83185042, 0.00012074, 196.10616806, 0.00040247, -19.61061681, -4.025e-05, -58.83185042, -0.00012074, -196.10616806, -0.00040247, 0.4, 0.3, 0.003, 0.0, 0.0, 24057, 2)
    ops.limitCurve('ThreePoint', 14057, 4057, 0.0, 78.44246722, 0.01158303, 78.44246722, 0.03474909, 54.90972706, -1818.48535885, 0.05, 2, 0, 71001, 24023, 1, 3)
    ops.uniaxialMaterial('LimitState', 34057, 19.61061681, 4.025e-05, 58.83185042, 0.00012074, 196.10616806, 0.00040247, -19.61061681, -4.025e-05, -58.83185042, -0.00012074, -196.10616806, -0.00040247, 0.4, 0.3, 0.003, 0.0, 0.0, 14057, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4057, 99999, 'P', 44057, 'Vy', 34057, 'Vz', 24057, 'My', 14057, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171001, 71001, 171001, 4057, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124023, 124023, 24023, 4057, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174023, 0.0, 0.0, 5.125)
    ops.node(122001, 0.0, 0.0, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4058, 174023, 122001, 0.0625, 30925217.49957624, 12885507.2914901, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24058, 20.19850824, 0.00055907, 24.41151266, 0.02565679, 2.44115127, 0.08445473, -20.19850824, -0.00055907, -24.41151266, -0.02565679, -2.44115127, -0.08445473, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14058, 20.19850824, 0.00055907, 24.41151266, 0.02565679, 2.44115127, 0.08445473, -20.19850824, -0.00055907, -24.41151266, -0.02565679, -2.44115127, -0.08445473, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24058, 4058, 0.0, 72.15836166, 0.01118144, 72.15836166, 0.03354433, 50.51085316, -1868.07600617, 0.05, 2, 0, 74023, 22001, 2, 3)
    ops.uniaxialMaterial('LimitState', 44058, 18.03959042, 3.898e-05, 54.11877125, 0.00011693, 180.39590416, 0.00038976, -18.03959042, -3.898e-05, -54.11877125, -0.00011693, -180.39590416, -0.00038976, 0.4, 0.3, 0.003, 0.0, 0.0, 24058, 2)
    ops.limitCurve('ThreePoint', 14058, 4058, 0.0, 72.15836166, 0.01118144, 72.15836166, 0.03354433, 50.51085316, -1868.07600617, 0.05, 2, 0, 74023, 22001, 1, 3)
    ops.uniaxialMaterial('LimitState', 34058, 18.03959042, 3.898e-05, 54.11877125, 0.00011693, 180.39590416, 0.00038976, -18.03959042, -3.898e-05, -54.11877125, -0.00011693, -180.39590416, -0.00038976, 0.4, 0.3, 0.003, 0.0, 0.0, 14058, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4058, 99999, 'P', 44058, 'Vy', 34058, 'Vz', 24058, 'My', 14058, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174023, 74023, 174023, 4058, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122001, 122001, 22001, 4058, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(171002, 2.9, 0.0, 3.75)
    ops.node(124024, 2.9, 0.0, 4.775)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4059, 171002, 124024, 0.14, 30743308.86647835, 12809712.02769931, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24059, 63.20851084, 0.00051002, 76.39460133, 0.05033824, 7.63946013, 0.13429696, -63.20851084, -0.00051002, -76.39460133, -0.05033824, -7.63946013, -0.13429696, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14059, 77.18679022, 0.00049389, 93.28892563, 0.05283836, 9.32889256, 0.14720486, -77.18679022, -0.00049389, -93.28892563, -0.05283836, -9.32889256, -0.14720486, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24059, 4059, 0.0, 235.16182812, 0.01020045, 235.16182812, 0.03060134, 164.61327968, -7268.82380131, 0.05, 2, 0, 71002, 24024, 2, 3)
    ops.uniaxialMaterial('LimitState', 44059, 58.79045703, 5.704e-05, 176.37137109, 0.00017112, 587.9045703, 0.00057041, -58.79045703, -5.704e-05, -176.37137109, -0.00017112, -587.9045703, -0.00057041, 0.4, 0.3, 0.003, 0.0, 0.0, 24059, 2)
    ops.limitCurve('ThreePoint', 14059, 4059, 0.0, 268.75637499, 0.00987773, 268.75637499, 0.02963319, 188.1294625, -8848.27602746, 0.05, 2, 0, 71002, 24024, 1, 3)
    ops.uniaxialMaterial('LimitState', 34059, 67.18909375, 6.519e-05, 201.56728125, 0.00019557, 671.89093748, 0.0006519, -67.18909375, -6.519e-05, -201.56728125, -0.00019557, -671.89093748, -0.0006519, 0.4, 0.3, 0.003, 0.0, 0.0, 14059, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4059, 99999, 'P', 44059, 'Vy', 34059, 'Vz', 24059, 'My', 14059, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 171002, 71002, 171002, 4059, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124024, 124024, 24024, 4059, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174024, 2.9, 0.0, 5.125)
    ops.node(122002, 2.9, 0.0, 6.15)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4060, 174024, 122002, 0.14, 26152865.64254241, 10897027.35105934, 0.00271929, 0.00205333, 0.00157208, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24060, 60.52200422, 0.00057809, 73.84823814, 0.04711214, 7.38482381, 0.12514014, -60.52200422, -0.00057809, -73.84823814, -0.04711214, -7.38482381, -0.12514014, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14060, 74.09495561, 0.00055071, 90.40979389, 0.04943467, 9.04097939, 0.13713525, -74.09495561, -0.00055071, -90.40979389, -0.04943467, -9.04097939, -0.13713525, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24060, 4060, 0.0, 172.16366932, 0.01156184, 172.16366932, 0.03468553, 120.51456853, -4243.67200371, 0.05, 2, 0, 74024, 22002, 2, 3)
    ops.uniaxialMaterial('LimitState', 44060, 43.04091733, 4.909e-05, 129.12275199, 0.00014727, 430.40917331, 0.0004909, -43.04091733, -4.909e-05, -129.12275199, -0.00014727, -430.40917331, -0.0004909, 0.4, 0.3, 0.003, 0.0, 0.0, 24060, 2)
    ops.limitCurve('ThreePoint', 14060, 4060, 0.0, 196.75847923, 0.01101423, 196.75847923, 0.03304268, 137.73093546, -5082.81574073, 0.05, 2, 0, 74024, 22002, 1, 3)
    ops.uniaxialMaterial('LimitState', 34060, 49.18961981, 5.61e-05, 147.56885942, 0.00016831, 491.89619806, 0.00056103, -49.18961981, -5.61e-05, -147.56885942, -0.00016831, -491.89619806, -0.00056103, 0.4, 0.3, 0.003, 0.0, 0.0, 14060, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4060, 99999, 'P', 44060, 'Vy', 34060, 'Vz', 24060, 'My', 14060, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174024, 74024, 174024, 4060, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 122002, 122002, 22002, 4060, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172001, 0.0, 0.0, 6.65)
    ops.node(124025, 0.0, 0.0, 7.675)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4062, 172001, 124025, 0.0625, 32024267.03178781, 13343444.59657826, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24062, 18.62729019, 0.00060158, 22.45314125, 0.03156998, 2.24531413, 0.10422762, -18.62729019, -0.00060158, -22.45314125, -0.03156998, -2.24531413, -0.10422762, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14062, 18.62729019, 0.00060158, 22.45314125, 0.03156998, 2.24531413, 0.10422762, -18.62729019, -0.00060158, -22.45314125, -0.03156998, -2.24531413, -0.10422762, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24062, 4062, 0.0, 76.81972208, 0.01203166, 76.81972208, 0.03609498, 53.77380546, -2296.08811349, 0.05, 2, 0, 72001, 24025, 2, 3)
    ops.uniaxialMaterial('LimitState', 44062, 19.20493052, 4.007e-05, 57.61479156, 0.00012021, 192.0493052, 0.0004007, -19.20493052, -4.007e-05, -57.61479156, -0.00012021, -192.0493052, -0.0004007, 0.4, 0.3, 0.003, 0.0, 0.0, 24062, 2)
    ops.limitCurve('ThreePoint', 14062, 4062, 0.0, 76.81972208, 0.01203166, 76.81972208, 0.03609498, 53.77380546, -2296.08811349, 0.05, 2, 0, 72001, 24025, 1, 3)
    ops.uniaxialMaterial('LimitState', 34062, 19.20493052, 4.007e-05, 57.61479156, 0.00012021, 192.0493052, 0.0004007, -19.20493052, -4.007e-05, -57.61479156, -0.00012021, -192.0493052, -0.0004007, 0.4, 0.3, 0.003, 0.0, 0.0, 14062, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4062, 99999, 'P', 44062, 'Vy', 34062, 'Vz', 24062, 'My', 14062, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172001, 72001, 172001, 4062, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124025, 124025, 24025, 4062, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174025, 0.0, 0.0, 8.025)
    ops.node(123001, 0.0, 0.0, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4063, 174025, 123001, 0.0625, 31444981.88794966, 13102075.78664569, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24063, 16.15619652, 0.00053115, 19.53559216, 0.02098776, 1.95355922, 0.08370498, -16.15619652, -0.00053115, -19.53559216, -0.02098776, -1.95355922, -0.08370498, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14063, 16.15619652, 0.00053115, 19.53559216, 0.02098776, 1.95355922, 0.08370498, -16.15619652, -0.00053115, -19.53559216, -0.02098776, -1.95355922, -0.08370498, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24063, 4063, 0.0, 52.48324591, 0.01062296, 52.48324591, 0.03186887, 36.73827214, -1466.57926207, 0.05, 2, 0, 74025, 23001, 2, 3)
    ops.uniaxialMaterial('LimitState', 44063, 13.12081148, 2.788e-05, 39.36243443, 8.364e-05, 131.20811478, 0.0002788, -13.12081148, -2.788e-05, -39.36243443, -8.364e-05, -131.20811478, -0.0002788, 0.4, 0.3, 0.003, 0.0, 0.0, 24063, 2)
    ops.limitCurve('ThreePoint', 14063, 4063, 0.0, 52.48324591, 0.01062296, 52.48324591, 0.03186887, 36.73827214, -1466.57926207, 0.05, 2, 0, 74025, 23001, 1, 3)
    ops.uniaxialMaterial('LimitState', 34063, 13.12081148, 2.788e-05, 39.36243443, 8.364e-05, 131.20811478, 0.0002788, -13.12081148, -2.788e-05, -39.36243443, -8.364e-05, -131.20811478, -0.0002788, 0.4, 0.3, 0.003, 0.0, 0.0, 14063, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4063, 99999, 'P', 44063, 'Vy', 34063, 'Vz', 24063, 'My', 14063, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174025, 74025, 174025, 4063, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123001, 123001, 23001, 4063, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(172002, 2.9, 0.0, 6.65)
    ops.node(124026, 2.9, 0.0, 7.675)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4064, 172002, 124026, 0.0875, 34260163.38482346, 14275068.07700977, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24064, 32.95178724, 0.00056356, 39.3861294, 0.04548184, 3.93861294, 0.14388786, -32.95178724, -0.00056356, -39.3861294, -0.04548184, -3.93861294, -0.14388786, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14064, 47.84887588, 0.00049397, 57.19210321, 0.0515407, 5.71921032, 0.1515407, -47.84887588, -0.00049397, -57.19210321, -0.0515407, -5.71921032, -0.1515407, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24064, 4064, 0.0, 123.45900442, 0.01127126, 123.45900442, 0.03381379, 86.42130309, -3563.68970532, 0.05, 2, 0, 72002, 24026, 2, 3)
    ops.uniaxialMaterial('LimitState', 44064, 30.8647511, 4.3e-05, 92.59425331, 0.00012899, 308.64751105, 0.00042996, -30.8647511, -4.3e-05, -92.59425331, -0.00012899, -308.64751105, -0.00042996, 0.4, 0.3, 0.003, 0.0, 0.0, 24064, 2)
    ops.limitCurve('ThreePoint', 14064, 4064, 0.0, 172.84260619, 0.00987937, 172.84260619, 0.0296381, 120.98982433, -5780.08138081, 0.05, 2, 0, 72002, 24026, 1, 3)
    ops.uniaxialMaterial('LimitState', 34064, 43.21065155, 6.019e-05, 129.63195464, 0.00018058, 432.10651546, 0.00060194, -43.21065155, -6.019e-05, -129.63195464, -0.00018058, -432.10651546, -0.00060194, 0.4, 0.3, 0.003, 0.0, 0.0, 14064, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4064, 99999, 'P', 44064, 'Vy', 34064, 'Vz', 24064, 'My', 14064, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 172002, 72002, 172002, 4064, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124026, 124026, 24026, 4064, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174026, 2.9, 0.0, 8.025)
    ops.node(123002, 2.9, 0.0, 9.05)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4065, 174026, 123002, 0.0875, 31298424.85353174, 13041010.35563822, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24065, 31.08141639, 0.00061182, 37.54413021, 0.05191992, 3.75441302, 0.14973026, -31.08141639, -0.00061182, -37.54413021, -0.05191992, -3.75441302, -0.14973026, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14065, 45.49552032, 0.00052456, 54.95533788, 0.05883292, 5.49553379, 0.15883292, -45.49552032, -0.00052456, -54.95533788, -0.05883292, -5.49553379, -0.15883292, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24065, 4065, 0.0, 117.44117877, 0.01223641, 117.44117877, 0.03670923, 82.20882514, -4624.74377825, 0.05, 2, 0, 74026, 23002, 2, 3)
    ops.uniaxialMaterial('LimitState', 44065, 29.36029469, 4.477e-05, 88.08088408, 0.00013431, 293.60294692, 0.0004477, -29.36029469, -4.477e-05, -88.08088408, -0.00013431, -293.60294692, -0.0004477, 0.4, 0.3, 0.003, 0.0, 0.0, 24065, 2)
    ops.limitCurve('ThreePoint', 14065, 4065, 0.0, 164.41765027, 0.01049128, 164.41765027, 0.03147383, 115.09235519, -7837.28155303, 0.05, 2, 0, 74026, 23002, 1, 3)
    ops.uniaxialMaterial('LimitState', 34065, 41.10441257, 6.268e-05, 123.31323771, 0.00018804, 411.04412569, 0.00062678, -41.10441257, -6.268e-05, -123.31323771, -0.00018804, -411.04412569, -0.00062678, 0.4, 0.3, 0.003, 0.0, 0.0, 14065, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4065, 99999, 'P', 44065, 'Vy', 34065, 'Vz', 24065, 'My', 14065, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174026, 74026, 174026, 4065, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 123002, 123002, 23002, 4065, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173001, 0.0, 0.0, 9.55)
    ops.node(124027, 0.0, 0.0, 10.575)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4067, 173001, 124027, 0.0625, 27352134.51575175, 11396722.71489656, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24067, 16.10990396, 0.0006458, 19.69913671, 0.02352566, 1.96991367, 0.08563662, -16.10990396, -0.0006458, -19.69913671, -0.02352566, -1.96991367, -0.08563662, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14067, 16.10990396, 0.0006458, 19.69913671, 0.02352566, 1.96991367, 0.08563662, -16.10990396, -0.0006458, -19.69913671, -0.02352566, -1.96991367, -0.08563662, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24067, 4067, 0.0, 52.2024666, 0.01291595, 52.2024666, 0.03874785, 36.54172662, -2036.25943409, 0.05, 2, 0, 73001, 24027, 2, 3)
    ops.uniaxialMaterial('LimitState', 44067, 13.05061665, 3.188e-05, 39.15184995, 9.564e-05, 130.50616651, 0.0003188, -13.05061665, -3.188e-05, -39.15184995, -9.564e-05, -130.50616651, -0.0003188, 0.4, 0.3, 0.003, 0.0, 0.0, 24067, 2)
    ops.limitCurve('ThreePoint', 14067, 4067, 0.0, 52.2024666, 0.01291595, 52.2024666, 0.03874785, 36.54172662, -2036.25943409, 0.05, 2, 0, 73001, 24027, 1, 3)
    ops.uniaxialMaterial('LimitState', 34067, 13.05061665, 3.188e-05, 39.15184995, 9.564e-05, 130.50616651, 0.0003188, -13.05061665, -3.188e-05, -39.15184995, -9.564e-05, -130.50616651, -0.0003188, 0.4, 0.3, 0.003, 0.0, 0.0, 14067, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4067, 99999, 'P', 44067, 'Vy', 34067, 'Vz', 24067, 'My', 14067, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173001, 73001, 173001, 4067, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124027, 124027, 24027, 4067, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174027, 0.0, 0.0, 10.925)
    ops.node(124001, 0.0, 0.0, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4068, 174027, 124001, 0.0625, 27175885.41245709, 11323285.58852379, 0.00055013, 0.00035807, 0.00035807, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24068, 13.23119363, 0.00061191, 16.22171196, 0.02800252, 1.6221712, 0.09435756, -13.23119363, -0.00061191, -16.22171196, -0.02800252, -1.6221712, -0.09435756, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14068, 13.23119363, 0.00061191, 16.22171196, 0.02800252, 1.6221712, 0.09435756, -13.23119363, -0.00061191, -16.22171196, -0.02800252, -1.6221712, -0.09435756, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24068, 4068, 0.0, 54.82079844, 0.01223825, 54.82079844, 0.03671476, 38.37455891, -14971.79597709, 0.05, 2, 0, 74027, 24001, 2, 3)
    ops.uniaxialMaterial('LimitState', 44068, 13.70519961, 3.37e-05, 41.11559883, 0.00010109, 137.05199609, 0.00033696, -13.70519961, -3.37e-05, -41.11559883, -0.00010109, -137.05199609, -0.00033696, 0.4, 0.3, 0.003, 0.0, 0.0, 24068, 2)
    ops.limitCurve('ThreePoint', 14068, 4068, 0.0, 54.82079844, 0.01223825, 54.82079844, 0.03671476, 38.37455891, -14971.79597709, 0.05, 2, 0, 74027, 24001, 1, 3)
    ops.uniaxialMaterial('LimitState', 34068, 13.70519961, 3.37e-05, 41.11559883, 0.00010109, 137.05199609, 0.00033696, -13.70519961, -3.37e-05, -41.11559883, -0.00010109, -137.05199609, -0.00033696, 0.4, 0.3, 0.003, 0.0, 0.0, 14068, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4068, 99999, 'P', 44068, 'Vy', 34068, 'Vz', 24068, 'My', 14068, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174027, 74027, 174027, 4068, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124001, 124001, 24001, 4068, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(173002, 2.9, 0.0, 9.55)
    ops.node(124028, 2.9, 0.0, 10.575)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4069, 173002, 124028, 0.0875, 34430349.40684183, 14345978.91951743, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24069, 26.1433774, 0.00058982, 31.29703195, 0.02784556, 3.1297032, 0.08683335, -26.1433774, -0.00058982, -31.29703195, -0.02784556, -3.1297032, -0.08683335, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14069, 38.59415882, 0.0005072, 46.20224094, 0.03107312, 4.62022409, 0.1084914, -38.59415882, -0.0005072, -46.20224094, -0.03107312, -4.62022409, -0.1084914, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24069, 4069, 0.0, 92.72661073, 0.01179634, 92.72661073, 0.03538902, 64.90862751, -2035.80990685, 0.05, 2, 0, 73002, 24028, 2, 3)
    ops.uniaxialMaterial('LimitState', 44069, 23.18165268, 3.213e-05, 69.54495805, 9.64e-05, 231.81652683, 0.00032133, -23.18165268, -3.213e-05, -69.54495805, -9.64e-05, -231.81652683, -0.00032133, 0.4, 0.3, 0.003, 0.0, 0.0, 24069, 2)
    ops.limitCurve('ThreePoint', 14069, 4069, 0.0, 129.81725502, 0.01014404, 129.81725502, 0.03043213, 90.87207852, -3436.74943498, 0.05, 2, 0, 73002, 24028, 1, 3)
    ops.uniaxialMaterial('LimitState', 34069, 32.45431376, 4.499e-05, 97.36294127, 0.00013496, 324.54313756, 0.00044987, -32.45431376, -4.499e-05, -97.36294127, -0.00013496, -324.54313756, -0.00044987, 0.4, 0.3, 0.003, 0.0, 0.0, 14069, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4069, 99999, 'P', 44069, 'Vy', 34069, 'Vz', 24069, 'My', 14069, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 173002, 73002, 173002, 4069, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124028, 124028, 24028, 4069, '-orient', 0, 0, 1, 0, 1, 0)

    # Create elastic column element nodes
    ops.node(174028, 2.9, 0.0, 10.925)
    ops.node(124002, 2.9, 0.0, 12.0)
    # Create elastic column element
    ops.element('elasticBeamColumn', 4070, 174028, 124002, 0.0875, 30483017.31062885, 12701257.21276202, 0.0010204, 0.00098255, 0.0005013, 66666)
    # Create materials describing flexural behaviour of plastic hinge
    ops.uniaxialMaterial('Hysteretic', 24070, 25.84187983, 0.00062445, 31.38788047, 0.03488735, 3.13878805, 0.09475277, -25.84187983, -0.00062445, -31.38788047, -0.03488735, -3.13878805, -0.09475277, 1.0, 1.0, 0.0, 0.0, 0.0)
    ops.uniaxialMaterial('Hysteretic', 14070, 38.15818371, 0.00053413, 46.34742197, 0.03895821, 4.6347422, 0.11752834, -38.15818371, -0.00053413, -46.34742197, -0.03895821, -4.6347422, -0.11752834, 1.0, 1.0, 0.0, 0.0, 0.0)
    # Create new materials describing shear behaviour of plastic hinge
    ops.limitCurve('ThreePoint', 24070, 4070, 0.0, 84.52711241, 0.01248901, 84.52711241, 0.03746703, 59.16897869, -5545.8634191, 0.05, 2, 0, 74028, 24002, 2, 3)
    ops.uniaxialMaterial('LimitState', 44070, 21.1317781, 3.308e-05, 63.39533431, 9.925e-05, 211.31778102, 0.00033085, -21.1317781, -3.308e-05, -63.39533431, -9.925e-05, -211.31778102, -0.00033085, 0.4, 0.3, 0.003, 0.0, 0.0, 24070, 2)
    ops.limitCurve('ThreePoint', 14070, 4070, 0.0, 118.33795737, 0.01068262, 118.33795737, 0.03204786, 82.83657016, -10278.09005835, 0.05, 2, 0, 74028, 24002, 1, 3)
    ops.uniaxialMaterial('LimitState', 34070, 29.58448934, 4.632e-05, 88.75346803, 0.00013896, 295.84489343, 0.00046319, -29.58448934, -4.632e-05, -88.75346803, -0.00013896, -295.84489343, -0.00046319, 0.4, 0.3, 0.003, 0.0, 0.0, 14070, 2)
    # Create plastic hinge sections at both ends
    ops.section('Aggregator', 4070, 99999, 'P', 44070, 'Vy', 34070, 'Vz', 24070, 'My', 14070, 'Mz', 99999, 'T')
    # Create plastic hinge elements at both ends
    ops.element('zeroLengthSection', 174028, 74028, 174028, 4070, '-orient', 0, 0, 1, 0, 1, 0)
    ops.element('zeroLengthSection', 124002, 124002, 24002, 4070, '-orient', 0, 0, 1, 0, 1, 0)
