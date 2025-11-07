import ngsolve as ngs
import netgen.occ as occ
from netgen.occ import Z

# Plate parameters
plate_thickness = 5e-3 # m
plate_radius = 30e-3 # m
gap_height = 10e-3 # m

# +Z
## Create pipe
central_radius = 0.1 # m
z_gap = gap_height / 2 + plate_thickness
pnt_startp = occ.Pnt(-central_radius, 0, z_gap)
pnt_midp = occ.Pnt(0, 0, central_radius+z_gap)
pnt_endp = occ.Pnt(+central_radius, 0, z_gap)
arcp = occ.Edge(occ.ArcOfCircle(pnt_startp, pnt_midp, pnt_endp))

tube_radius = 5e-3 # m
pipep_disk = occ.Face(occ.Wire([occ.Circle(pnt_startp, Z, tube_radius)]))
pipep = occ.Pipe(arcp, pipep_disk).mat("steel")

## Create plates
platep1_disk = occ.Face(occ.Wire([occ.Circle(pnt_startp, -Z, plate_radius)]))
platep1 = platep1_disk.Extrude(occ.Vec(0, 0, -plate_thickness)).mat("steel")

platep2_disk = occ.Face(occ.Wire([occ.Circle(pnt_endp, -Z, plate_radius)]))
platep2 = platep2_disk.Extrude(occ.Vec(0, 0, -plate_thickness)).mat("steel")

steelp = pipep + platep1 + platep2

# -Z
## Create pipe
pnt_startn = occ.Pnt(-central_radius, 0, -z_gap)
pnt_midn = occ.Pnt(0, 0, -central_radius-z_gap)
pnt_endn = occ.Pnt(+central_radius, 0, -z_gap)
arcn = occ.Edge(occ.ArcOfCircle(pnt_startn, pnt_midn, pnt_endn))

pipen_disk = occ.Face(occ.Wire([occ.Circle(pnt_startn, -Z, tube_radius)]))
pipen = occ.Pipe(arcn, pipen_disk).mat("steel")

## Create plates
platen1_disk = occ.Face(occ.Wire([occ.Circle(pnt_startn, Z, plate_radius)]))
platen1 = platen1_disk.Extrude(occ.Vec(0, 0, +plate_thickness)).mat("steel")

platen2_disk = occ.Face(occ.Wire([occ.Circle(pnt_endn, Z, plate_radius)]))
platen2 = platen2_disk.Extrude(occ.Vec(0, 0, +plate_thickness)).mat("steel")

steeln = pipen + platen1 + platen2

box = occ.Box((-0.5, -0.5,-0.5), (0.5, 0.5, 0.5))

box.faces.name = "outer"
air = box - steelp - steeln
air.mat("air")

geo = occ.OCCGeometry(occ.Glue([steelp, steeln, air]))
with ngs.TaskManager():
    mesh = ngs.Mesh(geo.GenerateMesh(occ.meshsize.coarse, maxh=0.1)).Curve(3)

material_cf = ngs.CoefficientFunction([1, 2])

vtk = ngs.VTKOutput(ma=mesh,
    coefs=[material_cf],
    names=["material"],
    filename="out/twocap",
    legacy=True)
vtk.Do()
