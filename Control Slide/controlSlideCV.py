import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
import sys

# Inicialização da captura de vídeo da webcam
video = cv2.VideoCapture(0)

# Definindo as dimensões do vídeo (deixando em uma qualidade boa)
video.set(3, 1280)
video.set(4, 720)

# Inicialização do controlador do teclado através do KeyBoard Controller
kb = Controller()

# Inicialização do detector de mãos
detector = HandDetector(detectionCon=0.8)
estadoAtual = [0, 0, 0, 0, 0] # Estado atual da detecção dos dedos da mão (partindo do zero)

# Carregando as imagens das setas direita e esquerda
setaDir = cv2.imread('seta dir.PNG')
setaEsq = cv2.imread('seta esq.PNG')

# Redimensionando as matrizes de substituição para corresponder às regiões de destino em img
setaDir = cv2.resize(setaDir, (246, 166))
setaEsq = cv2.resize(setaEsq, (246, 166))


while True:
    _, img = video.read()
    hands, img = detector.findHands(img)

    if hands:
        estado = detector.fingersUp(hands[0])
        print(estado)
        # Se o mindinho estiver aberto ele passa o slide
        if estado != estadoAtual and estado == [0, 0, 0, 0, 1]:
            print('passar slide')
            kb.press(Key.right) # "Aperta para passar o slide"
            kb.release(Key.right) # "Solta o slide"
        # Se o Dedão estiver aberto ele volta o slide
        if estado != estadoAtual and estado == [1, 0, 0, 0, 0]:
            print('voltar slide')
            kb.press(Key.left) # "Aperta para passar o slide"
            kb.release(Key.left) # "Solta o slide"

        # Exibe a imagem da seta direita se o estado atual for [0, 0, 0, 0, 1]
        if estadoAtual == [0, 0, 0, 0, 1]:
            setaDir_altura, setaDir_largura, _ = setaDir.shape
            img[50:50 + setaDir_altura, 50:50 + setaDir_largura] = setaDir

        # Exibe a imagem da seta direita se o estado atual for [0, 0, 0, 0, 1]
        if estadoAtual == [1, 0, 0, 0, 0]:
            setaEsq_altura, setaEsq_largura, _ = setaEsq.shape
            img[50:50 + setaEsq_altura, 50:50 + setaEsq_largura] = setaEsq

        estadoAtual = estado

        # Se o estado atual for [0, 1, 1, 0, 0], pressiona a tecla Esc para encerrar a apresentação
        if estadoAtual == [0, 1, 1, 0, 0]:
            pyautogui.press('esc')  # Simula o pressionamento da tecla Esc para encerrar a apresentação
            print('Encerrando o programa')
            break

    cv2.imshow('img',cv2.resize(img,(640,420))) # Redimensiona a imagem tratada inicialmente
    if cv2.waitKey(1) == ord('q'): # Encerra o programa ao clicar
        break

cv2.destroyAllWindows()
sys.exit()