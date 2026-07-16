# IFC2SIM converter

IFC2SIM converts an IFC structural model into a portable JSON scene manifest.
The output contains the selected components, their box geometry, IFC GUIDs,
component types, removal groups, removal ranks, and group order.

## Requirements

- tested on Python 3.9
- `numpy`
- `ifcopenshell` 
- `pybullet` 

## How to use

From the copied directory:

```bash
python3 ifc2sim.py \
  --ifc /path/to/model_ranked.ifc \
  --output selected_scene.json \
  --require-ifc-ranks \
  --select-ifc-types
```

## Visualize a scene manifest

The repository includes `example_scene.json`, containing the timber-frame
example. Open it in the standalone PyBullet viewer:

```bash
python3 visualize_scene.py --scene example_scene.json
```

The viewer colors components by removal group and labels each with its name,
group, and rank. Close the PyBullet window or press `Ctrl-C` in the terminal to
exit.
