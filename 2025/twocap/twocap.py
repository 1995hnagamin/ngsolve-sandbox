import ngsolve as ngs
import netgen.occ as occ
from netgen.occ import Z

e1 = occ.Segment((0,0,-0.03), (0,0,0.06))
spiral = occ.Wire([e1])
circ = occ.Face(occ.Wire([occ.Circle((0,0,-0.03), Z, 0.002)]))
coil = occ.Pipe(spiral, circ)

box = occ.Box((-0.04,-0.04,-0.03), (0.04,0.04,0.06))

box.faces.name = "outer"
air = box - coil
air.mat("air")
geo = occ.OCCGeometry(occ.Glue([coil, air]))
with ngs.TaskManager():
    mesh = ngs.Mesh(geo.GenerateMesh(occ.meshsize.coarse, maxh=0.005)).Curve(3)

material_cf = ngs.CoefficientFunction([1, 2])  # coil=1, air=2

vtk = ngs.VTKOutput(ma=mesh,
    coefs=[material_cf],
    names=["material"],
    filename="out/twocap",
    legacy=True)
vtk.Do()
