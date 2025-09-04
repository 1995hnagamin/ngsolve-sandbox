from netgen.occ import *
from ngsolve import *

e1 = Segment((0,0,-0.03), (0,0,0.06))
spiral = Wire([e1])
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

material_cf = CoefficientFunction([1, 2])  # coil=1, air=2

fespot = H1(mesh, order=2, definedon=mesh.Materials("coil"), dirichlet="out")
phi,psi = fespot.TnT()
sigma = 58.7e6
with TaskManager():
    bfa = BilinearForm(sigma*grad(phi)*grad(psi)*dx+1e-6*sigma*phi*psi*dx).Assemble()
    inv = bfa.mat.Inverse(freedofs=fespot.FreeDofs(), inverse="sparsecholesky")
    lff = LinearForm(1/crosssection*psi*ds("in")).Assemble()
    gfphi = GridFunction(fespot)
    gfphi.vec.data = inv * lff.vec

fesL2 = VectorL2(mesh, order=1, definedon=mesh.Materials("coil"))
gfJ = GridFunction(fesL2)
gfJ = -sigma*grad(gfphi)

pairs = [
    (material_cf, "MaterialID"),
    (gfphi, "electr.scala.pot."),
    (gfJ, "J"),
]

vtk = VTKOutput(ma=mesh,
    coefs=[p[0] for p in pairs],
    names=[p[1] for p in pairs],
    filename="out/mesh",
    legacy=True)
vtk.Do()
