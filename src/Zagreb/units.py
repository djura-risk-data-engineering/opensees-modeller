# Standardised Units
pi = 3.141592654
g = 9.81

# Length
m = 1.0
mm = m / 1000.0
cm = m / 100.0
inch = 25.4 * mm
ft = 12 * inch

# Area
m2 = m * m
mm2 = mm * mm
cm2 = cm * cm
in2 = inch * inch

# Second Moment of Area
m4 = m * m * m * m
cm4 = cm * cm * cm * cm
mm4 = mm * mm * mm * mm
in4 = inch * inch * inch * inch

# Force
kN = 1.0
N = kN / 1000.0
kips = kN * 4.448221615

# Moment
kNm = kN * m

# Mass (tonnes)
tonne = 1.0
kg = tonne / 1000.0

# Stress (kN/m2 or kPa)
Pa = N / (m * m)
kPa = Pa * 1.0e3
MPa = Pa * 1.0e6
Nmm2 = N / (mm * mm)
kNmm2 = Nmm2 * 1.0e3
GPa = Pa * 1.0e9
ksi = 6.8947573 * MPa
kgcm2 = kg * g / (cm * cm)

# Angles
degrees = pi / 180.0
