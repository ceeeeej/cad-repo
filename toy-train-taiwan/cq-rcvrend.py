import cadquery as cq

socket_offset = 8.75
socket_radius = 4
socket_wall_thickness = 0.5

# Create a 2D plan for the mount
mount_plan = (
    cq.Sketch()
    .rect(7, 7)  # centered on the origin
    .push([(3.5, 0)])  # locate the next rect
    .rect(4.5, 3.5, mode="a")  # add the rects together
    .push([(0, 0)])  # locate first hole
    .circle(3.6 / 2, mode="s")  # substract it
    .push([(socket_offset, 0)])  # locate socket hole
    .circle(socket_radius - socket_wall_thickness, mode="s")
    .clean()  # remove all internal edges
    .reset()  # reset all selections
    .vertices("not >X")  # fillet all but the socket end
    .fillet(0.5)
)
# Extrude the 2D plan into a 3D object
mount = cq.Workplane("XY").placeSketch(mount_plan).extrude(1, both=True)

# Create a socket from a hollow sphere
socket = (
    cq.Workplane("YZ")
    .sphere(socket_radius)
    .cut(cq.Workplane("YZ").sphere(socket_radius - socket_wall_thickness))
    .cut(cq.Workplane("XY").box(4, 8, 1))  # add a box to cut out
    .cut(cq.Workplane("XY").box(4, 1, 8))  # add a box to cut out
    .workplane(offset=2)  # offset a little to catch the other sphere
    .split(keepBottom=True)  # slice on the YZ plane and keep the "bottom"
    .translate((socket_offset, 0, 0))  # move into position
)

result = mount.union(socket)  # combine the objects
