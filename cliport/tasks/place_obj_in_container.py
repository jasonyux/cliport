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

    def __generate_box(self, zone_size, template):
        half = np.float32(zone_size) / 2
        replace = {'DIM': zone_size, 'HALF': half}
        return self.fill_template(template, replace)

    def __generate_hexagon(self, obj_color, template):
        fname = os.path.join(self.assets_root, 'kitting', '17.obj')
        scale = [0.005, 0.005, 0.002]
        replace = {'FNAME': (fname,), 'SCALE': scale, 'COLOR': utils.COLORS[obj_color]}
        return self.fill_template(template, replace)

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

        # Add container.
        zone_size = self.get_random_size(0.15, 0.25, 0.15, 0.25, 0.05, 0.05)
        bowl_size = (0.1, 0.1, 0)
        bowl_poses = []
        container_color = np.random.choice(["green", "red"])
        container =  np.random.choice(list(containers.keys()))
        container_urdf = containers[container]
        for _ in range(n_bowls):
            if container == 'box': 
                container_urdf = self.__generate_box(zone_size, container_urdf)
                container_pose = self.get_random_pose(env, zone_size)
            else:
                container_pose = self.get_random_pose(env, bowl_size)
            
            container_id = env.add_object(container_urdf, container_pose, 'fixed')
            p.changeVisualShape(container_id, -1, rgbaColor=utils.COLORS[container_color] + [1])
            bowl_poses.append(container_pose)

        # Add block.
        obj_color = np.random.choice(["green", "red", "yellow"])
        obj = np.random.choice(list(objects.keys()))
        obj_urdf = objects[obj]
        blocks = []
        block_size = (0.02, 0.02, 0.02)
        for _ in range(n_blocks):
            if obj == 'hexagon':
                size = (0.2, 0.2, 0.05)
                obj_urdf = self.__generate_hexagon(obj_color, obj_urdf)
                pose = self.get_random_pose(env, size)
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

        # Colors of distractor objects.
        container_colors = [c for c in utils.COLORS.keys() if c != container_color]
        obj_colors = [c for c in utils.COLORS if c != obj_color]

        # Add distractors.
        n_distractors = 0
        while n_distractors < 4:
            distractor_class = np.random.choice([objects, containers])
            distractor = np.random.choice(list(distractor_class.keys()))

            colors = container_colors if distractor_class == containers else obj_colors
            color = np.random.choice(colors)
            urdf = distractor_class[distractor]

            if distractor in objects.keys():
                if distractor == 'hexagon':
                    size = (0.2, 0.2, 0.05)
                    urdf = self.__generate_hexagon(color, urdf)
                    pose = self.get_random_pose(env, size)
                else:
                    pose = self.get_random_pose(env, block_size)
            else:
                if distractor == 'box': 
                    urdf = self.__generate_box(zone_size, urdf)
                    pose = self.get_random_pose(env, zone_size)
                else:
                    pose = self.get_random_pose(env, bowl_size)
            
            if not pose:
                continue
            id = env.add_object(urdf, pose)
            if not id:
                continue
            p.changeVisualShape(id, -1, rgbaColor=utils.COLORS[color] + [1])
            n_distractors += 1
