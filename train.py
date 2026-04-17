from ultralytics import YOLO


def train_model():
    print("Rozpoczynam trening")

    model = YOLO(r"runs\detect\train8\weights\last.pt")

    results = model.train(
        data=r"..\whatsInYourFridge-1\data.yaml",
        epochs=20,
        imgsz=640,
        device='0'
    )

    print("Koniec. Wyniki: runs/detect/train/weights/best.pt")


if __name__ == "__main__":
    train_model()