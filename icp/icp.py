import numpy as np
from scipy.spatial import KDTree


class ICP_test:
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def icp_method(self,max_iterations=50, tolerance=1e-6):
        src_mean = np.mean(self.source, axis=0)
        tgt_mean = np.mean(self.target, axis=0)
        src_centered = self.source - src_mean
        tgt_centered = self.target - tgt_mean

        transformation = np.eye(4)
        prev_error = float('inf')

        for i in range(max_iterations):
            kdtree = KDTree(tgt_centered)
            distances, indices = kdtree.query(src_centered)
            tgt_matched = tgt_centered[indices]

            H = np.dot(src_centered.T, tgt_matched)
            U, _, Vt = np.linalg.svd(H)
            R = np.dot(Vt.T, U.T)

            if np.linalg.det(R) < 0:
                Vt[2, :] *= -1
                R = np.dot(Vt.T, U.T)

            t = tgt_mean - np.dot(R, src_mean)

            transformation_step = np.eye(4)
            transformation_step[:3, :3] = R
            transformation_step[:3, 3] = t

            src_centered = np.dot(R, src_centered.T).T + t

            transformation = np.dot(transformation_step, transformation)

            mean_error = np.mean(distances)
            print(f"Iteration {i+1}: Mean error = {mean_error}")

            if np.abs(prev_error - mean_error) < tolerance:
                break
            prev_error = mean_error

        return transformation, prev_error
