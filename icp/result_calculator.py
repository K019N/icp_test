import numpy as np
from scipy.spatial import KDTree


class ResultCalculator:
    def __init__(self, source, target, transformation):
        self.source = source
        self.target = target
        self.transformation = transformation

    def calculate_alignment_percentage(self, threshold=400):
        source_transformed = (self.transformation[:3, :3] @ self.source.T).T + self.transformation[:3, 3]
        kdtree = KDTree(self.target)
        distances, _ = kdtree.query(source_transformed)
        within_threshold = np.sum(distances < threshold)
        percentage = (within_threshold / len(distances)) * 100
        return percentage

    def rotation_matrix_to_euler_angles(self):
        R = self.transformation[:3, :3]
        sy = np.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
        singular = sy < 1e-6

        if not singular:
            x = np.arctan2(R[2, 1], R[2, 2])
            y = np.arctan2(-R[2, 0], sy)
            z = np.arctan2(R[1, 0], R[0, 0])
        else:
            x = np.arctan2(-R[1, 2], R[1, 1])
            y = np.arctan2(-R[2, 0], sy)
            z = 0

        return np.degrees([x, y, z])
