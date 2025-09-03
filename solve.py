# https://ngsolve.github.io/TEAM-problems/TEAM-7/team7.html

import ngsolve as ngs
from ngsolve import x, y
from netgen.read_gmsh import ReadGmsh

mesh = ngs.Mesh(ReadGmsh("team7.msh"))
print(mesh.GetMaterials())
print(mesh.GetBoundaries())
print("number of elements:", mesh.ne)

coilrect_xmin, coilrect_xmax = 0.294-0.150, 0.294-0.050
coilrect_ymin, coilrect_ymax = 0.050, 0.150

def Project(val, minval, maxval):
    return ngs.IfPos(val-minval, ngs.IfPos(val-maxval, maxval, val), minval)

projx = Project(x, coilrect_xmin, coilrect_xmax)
projy = Project(y, coilrect_ymin, coilrect_ymax)
tau_coil = ngs.CF( (projy-y, x-projx, 0) )
tau_coil /= ngs.Norm(tau_coil)
pot_coil = ngs.CF( (0, 0, ngs.sqrt((projy-y)**2+(projx-x)**2)-0.05) )

tau_coil_only = mesh.MaterialCF({"Coil":tau_coil}, default=ngs.CF((0, 0, 0)))


# Visualize

V_vis = ngs.VectorH1(mesh, order=1)
gf_current = ngs.GridFunction(V_vis)

gf_current.Set(tau_coil_only)

vtk = ngs.VTKOutput(mesh, coefs=[gf_current], names=["current_vector"], filename="current_vectors")
vtk.Do()
