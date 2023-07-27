import numpy as np
import os
import torch
from isaacgym import gymutil, gymtorch, gymapi

class Ur5OpenDoor():
    def __init__(self):
        self.num_envs = 36

    def create_sim(self):
        pass

    def _create_ground_plane(self):
        pass

    def _create_envs(self, num_envs, spacing, num_per_row):
        pass

    def init_data(self):
        pass

    def compute_reward(self, actions):
        pass

    def compute_observations(self):
        pass

    def reset_idx(self, env_ids):
        pass

    def pre_physics_step(self, actions):
        pass

    def post_physics_step(self):
        pass
