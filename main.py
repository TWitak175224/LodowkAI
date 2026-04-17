from ultralytics import YOLO


def testuj_lodowke(sciezka_do_zdjecia):

    wagi = r"runs\detect\train8\weights\best.pt"
    model = YOLO(wagi)
    results = model(sciezka_do_zdjecia, conf=0.5)
    znalezione = []

    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            nazwa = model.names[class_id]
            znalezione.append(nazwa)

    print("Wynik skanowania")
    if not znalezione:
        print("Lodówka jest pusta.")
    else:
        for produkt in set(znalezione):
            ile_sztuk = znalezione.count(produkt)
            print(f" Znaleziono: {produkt} (Sztuk: {ile_sztuk})")
    results[0].show()

if __name__ == "__main__":
    testuj_lodowke(r"..\lodowkatest2.jpg")