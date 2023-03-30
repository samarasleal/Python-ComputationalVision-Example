# -*- coding: utf-8 -*-
"""VisaoComputacional.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qtfVOz120-b6xPY2kEfRMhLberxBq37T
"""

# Ler a imagem
import cv2
from skimage import io
from google.colab.patches import cv2_imshow
def ler_imagem(nome_arquivo):    
     imagem = io.imread(nome_arquivo)
     # cv2_imshow(imagem)
     return imagem

# Carregar os nomes dos objetos pré-classificados
!git clone https://github.com/AlexeyAB/darknet
!wget https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights
def carregar_classes():
  with open('darknet/data/coco.names', 'r') as f:
    classes = f.read().splitlines()
    return classes

# Montar o modelo de classificação - rede neural
def carregar_dnn():
  rede = cv2.dnn.readNetFromDarknet('darknet/cfg/yolov4.cfg','yolov4.weights')
  modelo = cv2.dnn_DetectionModel(rede)
  modelo.setInputParams(scale=1 / 255, 
                           size=(416, 416), 
                           swapRB=True)
  return modelo
carregar_dnn()

# Reconhecer os objetos
def reconhecer_objetos(modelo, classes, imagem):
  classIds, scores, boxes = modelo.detect(imagem,
                                          confThreshold=0.55,
                                          nmsThreshold=0.45)
  for (classId, score, box) in zip(classIds, scores, boxes):
    cv2.rectangle(imagem,
                  (box[0], box[1]),
                  (box[0] + box[2], box[1] + box[3]),
                  color=(0, 255, 0), thickness=2)
    texto = '%s: %2.f'% (classes[classId], score)
    cv2.putText(imagem, texto,
                (box[0], box[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                color = (0, 255, 0),thickness=2)
  return imagem

#Implementação da função para o processamento da imagem
def processar_imagem(nome_arquivo):
     imagem = ler_imagem(nome_arquivo)
     classes = carregar_classes()
     modelo = carregar_dnn()
     imagem = reconhecer_objetos(modelo, classes, imagem)
     cv2_imshow(imagem)
     cv2.waitKey(0)
     cv2.destroyAllWindows()

# Método principal
if __name__ == '__main__':
  path = 'https://img.freepik.com/fotos-gratis/garota-feliz-com-capuz-cinza-brinca-com-corgi-no-fundo-rosa-cachorro-lambe-bochecha-de-mulher-feliz-senhora-de-otimo-humor-segurando-animal-domestico-isolado_197531-18535.jpg'  
  processar_imagem(path)