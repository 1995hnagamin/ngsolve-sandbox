SetFactory("OpenCASCADE");

/*  Outermost boundary
    [-1353, 1647] x [-1353, 1647] x [-300, 449] (mm)
*/
Box(1) = {-1.353, -1.353, -0.300, 3.000, 3.000, 0.749};

/*  Alminum
    294 x 294 x 19 (mm)
    with hole 108 x 108 x 19 (mm)
*/
almiLengthX = 0.294;
almiLengthY = 0.294;
almiLengthZ = 0.019;
Box(2) = {0, 0, 0, almiLengthX, almiLengthY, almiLengthZ};

almiHoleOffsetX = 0.018;
almiHoleLengthX = 0.108;
almiHoleOffsetY = 0.018;
almiHoleLengthY = 0.108;
Box(3) = {almiHoleOffsetX, almiHoleOffsetY, 0, almiHoleLengthX, almiHoleLengthY, almiLengthZ};

Almi() = BooleanDifference{ Volume{2}; Delete; }{ Volume{3}; Delete; };

/* Coil
*/

coilAlmiGap = 0.030;
coilLengthZ = 0.100;

//+
Point(33) = {0.244, 0, 0.049, 1.0};
//+
Point(34) = {0.294, 0.050, 0.049, 1.0};
//+
Point(35) = {0.244, 0.050, 0.049, 1.0};
//+
Circle(49) = {33, 35, 34};
//+
Point(36) = {0.294, 0.150, 0.049, 1.0};
//+
Point(37) = {0.244, 0.200, 0.049, 1.0};
//+
Point(38) = {0.244, 0.150, 0.049, 1.0};
//+
Line(50) = {34, 36};
//+
Circle(51) = {36, 38, 37};
//+
Point(39) = {0.144, 0.200, 0.049, 1.0};
Point(40) = {0.094, 0.150, 0.049, 1.0};
Point(41) = {0.144, 0.150, 0.049, 1.0};
//+
Line(52) = {37, 39};
//+
Circle(53) = {39, 41, 40};

Point(42) = {0.094, 0.050, 0.049, 1.0};
Point(43) = {0.144,   0.0, 0.049, 1.0};
Point(44) = {0.144, 0.050, 0.049, 1.0};
//+
Line(54) = {40, 42};
//+
Circle(55) = {42, 44, 43};
//+
Line(56) = {43, 33};

Curve Loop(25) = {56, 49, 50, 51, 52, 53, 54, 55};

Point(45) = {0.244, 0.025, 0.049, 1.0};
Point(46) = {0.269, 0.050, 0.049, 1.0};
Circle(57) = {45, 35, 46};

Point(47) = {0.269, 0.150, 0.049, 1.0};
Point(48) = {0.244, 0.175, 0.049, 1.0};
Line(58) = {46, 47};
Circle(59) = {47, 38, 48};

Point(49) = {0.144, 0.175, 0.049, 1.0};
Point(50) = {0.119, 0.150, 0.049, 1.0};
Line(60) = {48, 49};
Circle(61) = {49, 41, 50};

Point(51) = {0.119, 0.050, 0.049, 1.0};
Point(52) = {0.144, 0.025, 0.049, 1.0};
//+
Line(62) = {50, 51};
//+
Circle(63) = {51, 44, 52};
//+
Line(64) = {52, 45};
//+
Curve Loop(26) = {50, 51, 52, 53, 54, 55, 56, 49};
//+
Curve Loop(27) = {58, 59, 60, 61, 62, 63, 64, 57};
//+
Plane Surface(23) = {26, 27};
//+
Extrude {0, 0, coilLengthZ} {
  Surface{23}; 
}
//+
Physical Volume("Air", 97) = {1};
//+
Physical Volume("Alminum", 98) = {2};
//+
Physical Volume("Coil", 99) = {3};

Save "team7.step";
