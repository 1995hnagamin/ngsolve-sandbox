from ngsolve import *
from netgen.read_gmsh import ReadGmsh

mesh = Mesh(ReadGmsh("team7.msh"))
print(mesh.GetMaterials())

