SetFactory("OpenCASCADE");

/*  Outermost boundary
    [-1353, 1647] x [-1353, 1647] x [-300, 449] (mm)
*/
Box(1) = {-1.353, -1.353, -0.300, 3.000, 3.000, 0.749};
Physical Surface("Outer") = {1, 2, 3, 4, 5, 6};

/*  Aluminum
    294 x 294 x 19 (mm)
    with hole 108 x 108 x 19 (mm)
*/
alumiLengthX = 0.294;
alumiLengthY = 0.294;
alumiLengthZ = 0.019;

lc = 1e-2;

Point(9) = {0, 0, 0, lc};
Point(10) = {alumiLengthX, 0, 0, lc};
Point(11) = {alumiLengthX, alumiLengthY, 0, lc};
Point(12) = {0, alumiLengthY, 0, lc};
Line(13) = {9, 10};
Line(14) = {10, 11};
Line(15) = {11, 12};
Line(16) = {12, 9};
Curve Loop(7) = {13, 14, 15, 16};

alumiHoleOffsetX = 0.018;
alumiHoleLengthX = 0.108;
alumiHoleOffsetY = 0.018;
alumiHoleLengthY = 0.108;
Point(13) = {alumiHoleOffsetX, alumiHoleOffsetY, 0, lc};
Point(14) = {alumiHoleOffsetX+alumiHoleLengthX, alumiHoleOffsetY, 0, lc};
Point(15) = {alumiHoleOffsetX+alumiHoleLengthX, alumiHoleOffsetY+alumiHoleLengthY, 0, lc};
Point(16) = {alumiHoleOffsetX, alumiHoleOffsetY+alumiHoleLengthY, 0, lc};
Line(17) = {13, 14};
Line(18) = {14, 15};
Line(19) = {15, 16};
Line(20) = {16, 13};
Curve Loop(8) = {18, 19, 20, 17};

Plane Surface(7) = {7, 8};

Extrude {0, 0, alumiLengthZ} {
  Surface{7}; 
}

coilAlumiGap = 0.030;
coilLengthZ = 0.100;

Point(33) = {0.244, 0, 0.049, lc};
Point(34) = {0.294, 0.050, 0.049, lc};
Point(35) = {0.244, 0.050, 0.049, lc};
Circle(49) = {33, 35, 34};

Point(36) = {0.294, 0.150, 0.049, lc};
Point(37) = {0.244, 0.200, 0.049, lc};
Point(38) = {0.244, 0.150, 0.049, lc};
Line(50) = {34, 36};
Circle(51) = {36, 38, 37};

Point(39) = {0.144, 0.200, 0.049, lc};
Point(40) = {0.094, 0.150, 0.049, lc};
Point(41) = {0.144, 0.150, 0.049, lc};
Line(52) = {37, 39};
Circle(53) = {39, 41, 40};

Point(42) = {0.094, 0.050, 0.049, lc};
Point(43) = {0.144,   0.0, 0.049, lc};
Point(44) = {0.144, 0.050, 0.049, lc};
Line(54) = {40, 42};
Circle(55) = {42, 44, 43};
Line(56) = {43, 33};

Curve Loop(25) = {56, 49, 50, 51, 52, 53, 54, 55};

Point(45) = {0.244, 0.025, 0.049, lc};
Point(46) = {0.269, 0.050, 0.049, lc};
Circle(57) = {45, 35, 46};

Point(47) = {0.269, 0.150, 0.049, lc};
Point(48) = {0.244, 0.175, 0.049, lc};
Line(58) = {46, 47};
Circle(59) = {47, 38, 48};

Point(49) = {0.144, 0.175, 0.049, lc};
Point(50) = {0.119, 0.150, 0.049, lc};
Line(60) = {48, 49};
Circle(61) = {49, 41, 50};

Point(51) = {0.119, 0.050, 0.049, lc};
Point(52) = {0.144, 0.025, 0.049, lc};
Line(62) = {50, 51};
Circle(63) = {51, 44, 52};
Line(64) = {52, 45};

Curve Loop(26) = {50, 51, 52, 53, 54, 55, 56, 49};
Curve Loop(27) = {58, 59, 60, 61, 62, 63, 64, 57};
Plane Surface(23) = {26, 27};

Extrude {0, 0, coilLengthZ} {
  Surface{23}; 
}

Physical Volume("Air", 97) = {1};
Physical Volume("Aluminum", 98) = {2};
Physical Volume("Coil", 99) = {3};

Save "team7.step";
