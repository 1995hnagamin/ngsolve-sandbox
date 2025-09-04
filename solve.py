# https://ngsolve.github.io/TEAM-problems/TEAM-7/team7.html

import ngsolve as ngs
from ngsolve import x, y, curl, dx, ds
from netgen.read_gmsh import ReadGmsh
import numpy as np

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

mu0 = 4e-7 * np.pi
sigma = mesh.MaterialCF({"Aluminum":35.26e6}, default=1e-10)

turns = 2742

def Solve(f):
    jw = 1j * 2 * np.pi * f
    fes = ngs.HCurl(mesh, order=2, complex=True, dirichlet="Outer", gradientdomains="Aluminum")
    print("free dofs", sum(fes.FreeDofs()))
    u, v = fes.TnT()
    
    a = ngs.BilinearForm(fes, symmetric=True, condense=True)
    a += 1/mu0 * curl(u) * curl(v) * dx
    a += jw * sigma * u * v * dx

    # boundary current density + div-free correction
    f = ngs.LinearForm(
            -turns/(0.100)*tau_coil*v.Trace() * ds("Coil", bonus_intorder=4) \
            +turns/(0.025 * 0.100)*pot_coil*curl(v) * dx("Coil", bonus_intorder=4))
    
    A = ngs.GridFunction(fes)
    pre = ngs.Preconditioner(a, type="bddc", inverse="sparsecholesky")
    # a.Assemble()
    # f.Assemble()
    # inv = solvers.CGSolver(mat=a.mat, pre=pre, printrates='\r', maxiter=200)
    # A.vec[:] = inv*f.vec
    ngs.solvers.BVP(bf=a, lf=f, gf=A, pre=pre, solver=ngs.solvers.CGSolver, solver_flags={"tol" : 1e-12})
    
    B = curl(A)
    J = -jw * sigma * A
    return {"A":A, "B":B, "J":J}

with ngs.TaskManager():
    ret = Solve(f=50)
A, B, J = ret["A"], ret["B"], ret["J"]

# Visualize

V_vis = ngs.VectorH1(mesh, order=1)
gf_current = ngs.GridFunction(V_vis)
gf_current.Set(tau_coil_only)

gf_A_real = ngs.GridFunction(V_vis)
gf_A_real.Set(A.real)

gf_A_imag = ngs.GridFunction(V_vis)
gf_A_imag.Set(A.imag)

gf_B_real = ngs.GridFunction(V_vis)
gf_B_real.Set(B.real)

gf_B_imag = ngs.GridFunction(V_vis)
gf_B_imag.Set(B.imag)

gf_J_real = ngs.GridFunction(V_vis)
gf_J_real.Set(J.real)

gf_J_imag = ngs.GridFunction(V_vis)
gf_J_imag.Set(J.imag)

# 全フィールドを出力
vtk = ngs.VTKOutput(mesh, 
                   coefs=[gf_current, gf_A_real, gf_A_imag,  gf_B_real, gf_B_imag, gf_J_real, gf_J_imag],
                   names=["current_vector", "A_real", "A_imag", "B_real", "B_imag",
                         "J_real", "J_imag"], 
                   filename="electromagnetic_fields",
                   legacy=True)

vtk.Do()
