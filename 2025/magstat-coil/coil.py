# https://docu.ngsolve.org/latest/i-tutorials/wta/coil.html

from netgen.occ import *
from ngsolve import *

cyl = Cylinder((0,0,0), Z, r=0.01, h=0.03).faces[0]
heli = Edge(Segment((0,0), (12*pi, 0.03)), cyl)
ps = heli.start
vs = heli.start_tangent
pe = heli.end
ve = heli.end_tangent

e1 = Segment((0,0,-0.03), (0,0,-0.01))
c1 = BezierCurve( [(0,0,-0.01), (0,0,0), ps-vs, ps])
e2 = Segment((0,0,0.04), (0,0,0.06))
c2 = BezierCurve( [pe, pe+ve, (0,0,0.03), (0,0,0.04)])
spiral = Wire([e1, c1, heli, c2, e2])
circ = Face(Wire([Circle((0,0,-0.03), Z, 0.001)]))
coil = Pipe(spiral, circ)

coil.faces.maxh=0.2
coil.faces.name="coilbnd"
coil.faces.Max(Z).name="in"
coil.faces.Min(Z).name="out"
coil.mat("coil")
crosssection = coil.faces.Max(Z).mass

box = Box((-0.04,-0.04,-0.03), (0.04,0.04,0.06))
box.faces.name = "outer"
air = box-coil
air.mat("air")
geo = OCCGeometry(Glue([coil,air]))
with TaskManager():
    mesh = Mesh(geo.GenerateMesh(meshsize.coarse, maxh=0.01)).Curve(3)


print(mesh.ne, mesh.nv, mesh.GetMaterials(), mesh.GetBoundaries())

fespot = H1(mesh, order=2, definedon=mesh.Materials("coil"), dirichlet="out")
phi,psi = fespot.TnT()
sigma = 58.7e6
with TaskManager():
    bfa = BilinearForm(sigma*grad(phi)*grad(psi)*dx).Assemble()
    inv = bfa.mat.Inverse(freedofs=fespot.FreeDofs(), inverse="sparsecholesky")
    lff = LinearForm(1/crosssection*psi*ds("in")).Assemble()
    gfphi = GridFunction(fespot)
    gfphi.vec.data = inv * lff.vec


fes = HCurl(mesh, order=1, nograds=True)
print ("HCurl dofs:", fes.ndof)
u,v = fes.TnT()
mu = 4*pi*1e-7
a = BilinearForm(1/mu*curl(u)*curl(v)*dx+1e-6/mu*u*v*dx)
pre = preconditioners.BDDC(a)
f = LinearForm(sigma*grad(gfphi)*v*dx("coil"))
with TaskManager():
    a.Assemble()
    f.Assemble()
inv = solvers.CGSolver(a.mat, pre)
gfu = GridFunction(fes)
with TaskManager():
    gfu.vec.data = inv * f.vec

gfB = GridFunction(fes)
gfB = curl(gfu)

gfJ = GridFunction(fes)
gfJ = -sigma*grad(gfphi)

J = -sigma*grad(gfphi)
n = specialcf.normal(3)
region_in_coil = mesh.Boundaries("in") * mesh.Materials("coil")

Iin = Integrate(J*n, mesh, BND, definedon=region_in_coil)
print("I(in) =", float(Iin))

material_cf = CoefficientFunction([1, 2])  # coil=1, air=2
vtk = VTKOutput(ma=mesh,
    coefs=[material_cf, gfphi, gfu, gfB, gfJ],
    names=["MaterialID", "electr.scala.pot.", "A", "B", "J"],
    filename="out/mesh",
    legacy=True)
vtk.Do()
