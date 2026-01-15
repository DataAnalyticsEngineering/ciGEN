import numpy as np
import meshio

count = 0
# --- Read nodes ---
points = []
with open("trial_n4-node.inp") as f:
    for line in f:
        if line.strip() and not line.startswith("*"):
            parts = line.strip().split(",")
            node_id = int(parts[0])
            x, y, z = map(float, parts[1:])
            points.append([x, y, z])

points = np.array(points)

# --- Read bulk elements ---
bulk_elements = []
with open("trial_n4-bulk-elems.inp") as f:
    for line in f:
        if line.strip() and not line.startswith("*"):
            parts = line.strip().split(",")
            elem_id = int(parts[0])
            conn = [int(x) - 1 for x in parts[1:]]
            bulk_elements.append(conn)

cells = [("tetra", np.array(bulk_elements))]

# --- Read interface elements ---
interface_elements = []
with open("trial_n4-int-elems.inp") as f:
    for line in f:
        if line.strip() and not line.startswith("*"):
            parts = line.strip().split(",")
            elem_id = int(parts[0])
            conn = [int(x) - 1 for x in parts[1:]]
            if conn[:3] == conn[-3:]:
                count += 1
                continue
            interface_elements.append(conn)



cells = []
cells.append(("wedge", np.array(interface_elements)))

print(f"Read {len(points)} points, {len(bulk_elements)} bulk elements, {len(interface_elements)} interface elements.")
print(f"Number of interface elements with identical node sets: {count}")

# --- Write to VTK ---
mesh = meshio.Mesh(points=points, cells=cells)
mesh.write("interfaceelements_trial2_n4_new.vtk")

print("Written interfaceelements_trial2_n4_new.vtk (open in ParaView)")