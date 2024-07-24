from converter import PointsGenerator
from icp import ICP_test as ICP
from result_calculator import ResultCalculator


class CloudsComparer:
    def __init__(self, model_path, point_cloud_path):
        self.model_path = model_path
        self.point_cloud_path = point_cloud_path

    def compare_clouds(self):
        if ".ply" in self.model_path or ".ply" in self.point_cloud_path:
            model_points = PointsGenerator(self.model_path).ply_to_point_cloud()
            point_cloud = PointsGenerator(self.point_cloud_path).ply_to_point_cloud()
            print("Loaded model points (PLY):", model_points.shape)
            print("Loaded point cloud (PLY):", point_cloud.shape)
        else:
            model_points = PointsGenerator(self.model_path).load_stl()
            point_cloud = PointsGenerator(self.point_cloud_path).load_point_cloud()
            print("Loaded model points:", model_points.shape)
            print("Loaded point cloud:", point_cloud.shape)

        transformation, _ = ICP(point_cloud, model_points).icp_method()
        print("Transformation matrix:")
        print(transformation)

        result_calculator = ResultCalculator(model_points, point_cloud, transformation)
        percentage = result_calculator.calculate_alignment_percentage()
        print(f"Alignment percentage: {percentage:.2f}%")

        rotation_angles = result_calculator.rotation_matrix_to_euler_angles()
        print(f"Rotation angles (in degrees): {rotation_angles}")