"""Bimanual IK

Same as 01_basic_ik.py, but with two end effectors!
"""

import time
import viser
from robot_descriptions.loaders.yourdfpy import load_robot_description
import numpy as np

import pyroki as pk
from viser.extras import ViserUrdf
import pyroki_snippets as pks


def main():
    """Main function for bimanual IK."""

    urdf = load_robot_description("yumi_description")
    target_link_names = ["yumi_link_7_r", "yumi_link_7_l"]

    # Create robot.
    robot = pk.Robot.from_urdf(urdf)

    # Set up visualizer.
    server = viser.ViserServer()
    server.scene.add_grid("/ground", width=2, height=2)
    urdf_vis = ViserUrdf(server, urdf, root_node_name="/base")

    # Create interactive controller with initial position.
    ik_target_0 = server.scene.add_transform_controls(
        "/ik_target_0", scale=0.2, position=(0.41, -0.3, 0.56), wxyz=(0, 0, 1, 0)
    )
    ik_target_1 = server.scene.add_transform_controls(
        "/ik_target_1", scale=0.2, position=(0.41, 0.3, 0.56), wxyz=(0, 0, 1, 0)
    )
    timing_handle = server.gui.add_number("Elapsed (ms)", 0.001, disabled=True)

    while True:
        # Solve IK.
        start_time = time.time()
        solution = pks.solve_ik_with_multiple_targets(
            robot=robot,
            target_link_names=target_link_names,
            target_positions=np.array([ik_target_0.position, ik_target_1.position]),
            target_wxyzs=np.array([ik_target_0.wxyz, ik_target_1.wxyz]),
        )

        # Update timing handle.
        elapsed_time = time.time() - start_time
        timing_handle.value = 0.99 * timing_handle.value + 0.01 * (elapsed_time * 1000)

        # Update visualizer.
        urdf_vis.update_cfg(solution)


if __name__ == "__main__":
    main()
