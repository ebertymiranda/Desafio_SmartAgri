import cv2
import sys
from random import randint


argument = sys.argv

cap = cv2.VideoCapture(argument[1])

ok, frame = cap.read()
if not ok:
    print("Não foi possível ler o arquivo")
    sys.exit(1)

bboxes = []
colors = []


#Seleciona pontos espeficicos e passa cores randomicas para o bound box
while True:
    bbox = cv2.selectROI('Tracker', frame)
    bboxes.append(bbox)
    colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
    print("Pressione Q para sair ou qualquer outra para continuar proximo objeto")
    k = cv2.waitKey(0) & 0XFF
    if (k == 113):
        break

# se sua versão OpenCV for menor que 4.5 usar o legacy
tracker = cv2.legacy.TrackerCSRT_create()
multitracker = cv2.legacy.MultiTracker_create()


#adiciona os pontos no multitracker
for bbox in bboxes:
    multitracker.add(tracker, frame, bbox)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        break
    ok, boxes = multitracker.update(frame)

    #cria o arquivo csv com todos os pontos  
    with open('positions.csv', 'a') as archive:         
            for value in boxes:

                archive.write(str(boxes) + '\n')

    for i, newbox in enumerate(boxes):
        (x, y, w, h) = [int(v) for v in newbox]
        cv2.rectangle(frame, (x, y), (x+w, y+h), colors[i], 2, 1)

    cv2.imshow('MultiTracker', frame)

    if cv2.waitKey(1) & 0XFF == 27:
        break 