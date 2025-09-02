import ngsolve as ngs
from netgen.read_gmsh import ReadGmsh

mesh = ngs.Mesh(ReadGmsh("team7.msh"))
print(mesh.GetMaterials())

