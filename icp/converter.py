import numpy as np
from stl import mesh
from plyfile import PlyData
import trimesh


class PointsGenerator:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def load_stl(self, num_points: int = 9000):
        mesh = trimesh.load_mesh(self.file_path)
        
        sampled_points, _ = trimesh.sample.sample_surface(mesh, num_points)
        
        return sampled_points
    
    def load_stl_tops(self):
        model = mesh.Mesh.from_file(self.file_path)
        points = np.concatenate([model.v0, model.v1, model.v2])
        points = np.unique(points, axis=0)
        return points
    
    def load_point_cloud(self):
        return np.loadtxt(self.file_path)
    
    def ply_to_point_cloud(self):
        plydata = PlyData.read(self.file_path)
        vertex = plydata['vertex']
        points = np.vstack([vertex['x'], vertex['y'], vertex['z']]).T
        return points
