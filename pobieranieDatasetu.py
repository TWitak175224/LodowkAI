from roboflow import Roboflow


def download_dataset():

    rf = Roboflow(api_key="EENgdxiQcge1QdgZYySw")
    project = rf.workspace("norberts-workspace-g7hdk").project("whatsinyourfridge-1cbaa-qz6us")
    version = project.version(1)
    dataset = version.download("yolo26")

if __name__ == "__main__":
    download_dataset()