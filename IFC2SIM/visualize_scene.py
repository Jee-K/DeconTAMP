#!/usr/bin/env python3
"""Standalone PyBullet viewer for IFC2SIM scene manifests.

Usage:
    python3 visualize_scene.py --scene example_scene.json
"""

import argparse
import json
import time
from pathlib import Path


GROUP_COLORS = (
    (0.90, 0.10, 0.10, 1.0),  # red
    (0.10, 0.25, 0.90, 1.0),  # blue
    (1.00, 0.50, 0.00, 1.0),  # orange
    (0.20, 0.75, 0.25, 1.0),  # green
    (0.65, 0.25, 0.80, 1.0),  # purple
)


def load_manifest(path):
    with Path(path).expanduser().open(encoding='utf-8') as stream:
        manifest = json.load(stream)
    if manifest.get('schema_version') != 1:
        raise ValueError('Expected IFC2SIM scene schema_version 1.')
    if not manifest.get('members'):
        raise ValueError('The IFC2SIM manifest has no members.')
    return manifest


def main():
    parser = argparse.ArgumentParser(description='Visualize an IFC2SIM JSON scene manifest in PyBullet.')
    parser.add_argument('--scene', default='example_scene.json',
                        help='IFC2SIM JSON manifest (default: example_scene.json).')
    args = parser.parse_args()
    manifest = load_manifest(args.scene)

    import pybullet as p
    import pybullet_data

    groups = list(manifest.get('group_order', []))
    for member in manifest['members']:
        if member['group'] not in groups:
            groups.append(member['group'])
    colors = {group: GROUP_COLORS[index % len(GROUP_COLORS)]
              for index, group in enumerate(groups)}

    client = p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.loadURDF('plane.urdf')
    p.setGravity(0, 0, 0)

    lower, upper = manifest['aabb_min'], manifest['aabb_max']
    center = [(lower[i] + upper[i]) / 2.0 for i in range(3)]
    extent = max(upper[i] - lower[i] for i in range(3))
    p.resetDebugVisualizerCamera(cameraDistance=max(2.0, 2.5 * extent),
                                 cameraYaw=45, cameraPitch=-30,
                                 cameraTargetPosition=center)

    for member in manifest['members']:
        dimensions = member['dimensions']
        center = member['center']
        shape = p.createCollisionShape(p.GEOM_BOX,
                                       halfExtents=[dimension / 2.0 for dimension in dimensions])
        visual = p.createVisualShape(p.GEOM_BOX,
                                     halfExtents=[dimension / 2.0 for dimension in dimensions],
                                     rgbaColor=colors[member['group']])
        body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=shape,
                                 baseVisualShapeIndex=visual, basePosition=center)
        p.addUserDebugText('{}\n{} ({})'.format(member['name'], member['group'], member['removal_rank']),
                           textPosition=center, textColorRGB=(0, 0, 0), textSize=0.8,
                           parentObjectUniqueId=body)

    print('[IFC2SIM] Visualizing {} members from {}'.format(len(manifest['members']), args.scene))
    print('[IFC2SIM] Close the PyBullet window or press Ctrl-C here to exit.')
    try:
        while p.isConnected(client):
            p.stepSimulation()
            time.sleep(1.0 / 120.0)
    except KeyboardInterrupt:
        pass
    finally:
        if p.isConnected(client):
            p.disconnect(client)


if __name__ == '__main__':
    main()
