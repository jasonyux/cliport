"""Sorting Task."""

import numpy as np
import os
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p


class PlaceObjInContainer(Task):
    """Sorting Task."""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.pos_eps = 0.05
        self.lang_template = "place {color1} {object} into {color2} {container}"
        self.task_completed_desc = "done placing object in container."

    def reset(self, env):
        super().reset(env)
        n_bowls = 1
        n_blocks = 1
        objects = {
            'block': 'block/block.urdf',
            'hexagon': 'kitting/object-template.urdf'
        }
        containers = {
            'box': 'container/container-template.urdf',
            'bowl': 'bowl/bowl.urdf'
        }

        # Add bowls.
        zone_size = self.get_random_size(0.05, 0.3, 0.05, 0.3, 0.05, 0.05)
        bowl_size = (0.1, 0.1, 0)
        bowl_poses = []
        container_color = np.random.choice(["green", "red"])
        container =  np.random.choice(list(containers.keys()))
        container_urdf = containers[container]
        for _ in range(n_bowls):
            if container == 'box': 
                container_pose = self.get_random_pose(env, zone_size)
                half = np.float32(zone_size) / 2
                replace = {'DIM': zone_size, 'HALF': half}
                container_urdf = self.fill_template(container_urdf, replace)
            else:
                container_pose = self.get_random_pose(env, bowl_size)
            
            container_id = env.add_object(container_urdf, container_pose, 'fixed')
            p.changeVisualShape(container_id, -1, rgbaColor=utils.COLORS[container_color] + [1])
            bowl_poses.append(container_pose)

        # Add blocks.
        obj_color = np.random.choice(["green", "red", "yellow"])
        obj = np.random.choice(list(objects.keys()))
        obj_urdf = objects[obj]
        blocks = []
        block_size = (0.02, 0.02, 0.02)
        for _ in range(n_blocks):
            if obj == 'hexagon':
                size = (0.2, 0.2, 0.05)
                pose = self.get_random_pose(env, size)
                fname = os.path.join(self.assets_root, 'kitting', '17.obj')
                scale = [0.005, 0.005, 0.002]
                replace = {'FNAME': (fname,), 'SCALE': scale, 'COLOR': utils.COLORS[obj_color]}
                obj_urdf = self.fill_template(obj_urdf, replace)
            else:
                pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(obj_urdf, pose)
            p.changeVisualShape(block_id, -1, rgbaColor=utils.COLORS[obj_color] + [1])

            blocks.append((block_id, (0, None)))
        

        # Goal: place object into container
        self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses))),
                           bowl_poses, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template.format(
            color1=obj_color, object=obj,
            color2=container_color, container=container)
        )

        """ # Colors of distractor objects.
        bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c != 'green']
        block_colors = [utils.COLORS[c] for c in utils.COLORS if c != 'blue']

        # Add distractors.
        n_distractors = 0
        block_urdf = 'block/block.urdf'
        bowl_urdf = 'bowl/bowl.urdf'
        while n_distractors < 6:
            is_block = np.random.rand() > 0.5
            urdf = block_urdf if is_block else bowl_urdf
            size = block_size if is_block else bowl_size
            colors = block_colors if is_block else bowl_colors
            pose = self.get_random_pose(env, size)
            if not pose:
                continue
            obj_id = env.add_object(urdf, pose)
            color = colors[n_distractors % len(colors)]
            if not obj_id:
                continue
            p.changeVisualShape(obj_id, -1, rgbaColor=color + [1])
            n_distractors += 1 """
