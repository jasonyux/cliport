"""Sorting Task."""

import numpy as np
from cliport.tasks.task import Task
from cliport.utils import utils

import pybullet as p


class PlaceObjInContainer(Task):
    """Sorting Task."""

    def __init__(self):
        super().__init__()
        self.max_steps = 10
        self.pos_eps = 0.05
        self.lang_template = "place {color1} {object} in a green bowl"
        self.task_completed_desc = "done placing object in container."

    def reset(self, env):
        super().reset(env)
        n_bowls = 1
        n_blocks = 1

        # Add bowls.
        bowl_size = (0.12, 0.12, 0)
        bowl_urdf = 'bowl/bowl.urdf'
        bowl_poses = []
        for _ in range(n_bowls):
            bowl_pose = self.get_random_pose(env, bowl_size)
            env.add_object(bowl_urdf, bowl_pose, 'fixed')

        # Add blocks.
        obj_color = np.random.choice(["green", "red", "yellow"])
        obj_urdf = np.random.choice(['block/block.urdf'])
        blocks = []
        block_size = (0.04, 0.04, 0.04)
        for _ in range(n_blocks):
            block_pose = self.get_random_pose(env, block_size)
            block_id = env.add_object(obj_urdf, block_pose)
            p.changeVisualShape(block_id, -1, rgbaColor=utils.COLORS[obj_color] + [1])
			
            bowl_poses.append(bowl_pose)

            blocks.append((block_id, (0, None)))

        # Goal: each red block is in a different green bowl.
        self.goals.append((blocks, np.ones((len(blocks), len(bowl_poses))),
                           bowl_poses, False, True, 'pose', None, 1))
        self.lang_goals.append(self.lang_template.format(color1=obj_color, object=obj_urdf))

        # Colors of distractor objects.
        bowl_colors = [utils.COLORS[c] for c in utils.COLORS if c != 'green']
        block_colors = [utils.COLORS[c] for c in utils.COLORS if c != 'blue']

        # Add distractors.
        n_distractors = 0
        block_urdf = 'block/block.urdf'
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
            n_distractors += 1
