import cadquery as cq

ball_offset = 7.5
ball_radius = 2.7
ball_wall_thickness = 0.5

# Create a 2D plan for the mount
mount_plan = (
    cq.Sketch()
    .rect(7, 7)  # centered on the origin
    .push([(3.5, 0)])  # locate the next rect
    .rect(4.5, 3.5, mode="a")  # add the rects together
    .push([(0, 0)])  # locate first hole
    .circle(3.6 / 2, mode="s")  # substract it
    .clean()  # remove all internal edges
    .reset()  # reset all selections
    .vertices("not >X")  # fillet all but the socket end
    .fillet(0.5)
)
# Extrude the 2D plan into a 3D object
mount = cq.Workplane("XY").placeSketch(mount_plan).extrude(1, both=True)

# Create a ball
ball = (
    cq.Workplane("YZ")
    .sphere(ball_radius)  # create a sphere for the ball
    .translate((ball_offset, 0, 0))  # move into position
)

result = mount.union(ball)  # combine the objects
