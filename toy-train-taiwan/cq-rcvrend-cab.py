import cadquery as cq
socket_offset = 7.75
socket_radius = 4
socket_wall_thickness = 0.5

post_height = 6
post_offset = 5.75
post_width = 3

extension_offset = post_offset+post_width

# Create a 2D plan for the mount
mount_plan = (
    cq.Sketch()
    .rect(8.5, 5.3)  # centered on the origin

    .push([(1, 0)])  # locate first hole
    .circle(3.7 / 2, mode="s")  # substract it
    .clean()  # remove all internal edges
    .reset()  # reset all selections
    .vertices("not >X")  # fillet all but the socket end
    .fillet(0.5))
# Extrude the 2D plan into a 3D object
mount = cq.Workplane("XY").placeSketch(mount_plan).extrude(1, both=True)

# Create a post
post = (
    cq.Workplane("XZ")
    .box(3,post_height,5.3) # create a sphere for the ball
    .translate((post_offset, 0, 2))  # move into position
)

# Create a post
extension = (
    cq.Workplane("XZ")
    .box(post_width,post_width,post_width) # create a sphere for the ball
    .translate((post_offset+post_width, 0, 3))  # move into position
)

socket = (
    cq.Workplane("YZ")
    .sphere(socket_radius)
    .cut(cq.Workplane("YZ").sphere(socket_radius - socket_wall_thickness))
    .cut(cq.Workplane("XY").box(4,8,1)) # add a box to cut out
    .cut(cq.Workplane("XY").box(4,1,8)) # add a box to cut out
    .workplane(offset=2)  # offset a little to catch the other sphere
    .split(keepBottom=True)  # slice on the YZ plane and keep the "bottom"
    .translate((extension_offset+socket_radius, 0, 3))  # move into position
)

result = mount.union(post)
result = result.union(extension)
result = result.union(socket) # combine the objects