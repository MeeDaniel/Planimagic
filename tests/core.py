import core


shape = core.Shape()
key_points = shape.get_key_points()
point = key_points[0]

print("Pos of first key point:", point.get_pos())

point.set_pos(10, 10)
print("Pos of first key point:", point.get_pos())

print("Actual pos of first key point:", shape.get_key_points()[0].get_pos())

key_points.remove(point)
print("After removing first point, key points are:", shape.get_key_points())

del key_points[0]
print("After deleting first point, key points are:", shape.get_key_points())

