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
circ = Face(Wire([Circle((0,0,-0.03), Z, 0.0015)]))
coil = Pipe(spiral, circ)

coil.faces.maxh=0.05
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
    mesh = Mesh(geo.GenerateMesh(meshsize.fine, maxh=0.005)).Curve(3)


print(mesh.ne, mesh.nv, mesh.GetMaterials(), mesh.GetBoundaries())

fespot = H1(mesh, order=2, definedon=mesh.Materials("coil"), dirichlet="out")
phi,psi = fespot.TnT()
sigma = 58.7e6
with TaskManager():
    bfa = BilinearForm(fespot)
    bfa += sigma*grad(phi)*grad(psi)*dx
    # bfa += 1e-6*sigma*phi*psi*dx
    bfa.Assemble()
    inv = bfa.mat.Inverse(freedofs=fespot.FreeDofs(), inverse="sparsecholesky")
    lff = LinearForm(fespot)
    lff += 1/crosssection*psi*ds("in")
    lff.Assemble()
    gfphi = GridFunction(fespot)
    gfphi.vec.data = inv * lff.vec


fes = HCurl(mesh, order=2, nograds=True)
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


material_cf = CoefficientFunction([1, 2])  # coil=1, air=2

pairs = [
    (material_cf, "MaterialID"),
    (gfphi, "electr.scala.pot."),
    (gfu, "A"),
    (gfB, "B"),
    (gfJ, "J"),
]

vtk = VTKOutput(ma=mesh,
    coefs=[p[0] for p in pairs],
    names=[p[1] for p in pairs],
    filename="out/mesh",
    legacy=True)
vtk.Do()
