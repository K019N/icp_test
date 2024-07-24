from clouds_comparer import CloudsComparer

def main():
    model_path = "./input_files/model.stl"
    point_cloud_path = "./input_files/1_ideal_cloud"
    point_cloud_path_1mm = "./input_files/1_cloud_maxerr_1mm"
    clouds_comparer = CloudsComparer(model_path, point_cloud_path)
    clouds_comparer.compare_clouds()
    clouds_comparer = CloudsComparer(model_path, point_cloud_path_1mm)
    clouds_comparer.compare_clouds()

    ply_model = "./input_files/dino/model.ply"
    ply_scene = "./input_files/dino/scene.ply"
    clouds_comparer = CloudsComparer(ply_model, ply_scene)
    clouds_comparer.compare_clouds()

main()
