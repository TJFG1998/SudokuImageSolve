import sys
from PIL import Image
import image_slicer
import cv2
import numpy as np

numbersDict = { 0 : "zero.png",
				1 : "um.png",
				2 : "dois.png",
				3 : "tres.png",
				4 : "quatro.png",
				5 : "cinco.png",
				6 : "seis.png",
				7 : "sete.png",
				8 : "oito.png",
				9 : "nove.png" }

board = [[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],]

#corata a imagem
def recorte():
	image_slicer.slice('example.png', 81)

# coloca a imagem com uma altura e largura desejada
def resize(largura, altura, img, nome):
    imagem = Image.open(img,'r')
    imagem = imagem.resize((largura,altura), Image.ANTIALIAS)
    imagem.save('{}.png'.format(nome))

#ve qual é o numero para a celula dada
def analisis(number,cell):
	img = cv2.imread(cell)
	template = cv2.imread(number)
	w, h = template.shape[:-1]
	count = 0
	result = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
	loc = np.where(result >= 0.4)
	for pt in zip(*loc[::-1]):
		cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
		count += 1

	if count > 0:
		return True
	else:
		return False

def valueFromValues(values):
	if len(values) == 1:
		print(values)
	else:
		print(values)

#corre os numeros para ver qual esta na celula
def numberForCellNotZero(cell):
	timesTrue = 0
	actualValueCell = 0
	possibleValues = []
	for i in range(1,10):
		if analisis(numbersDict[i],cell): 
			timesTrue+=1
			possibleValues.append(i)

	return valueFromValues(possibleValues)

#precorre as parcelas para
def cellCatch():
	recorte()
	for i in range(1,10):
		for j in range(1,10):
			cell = "example_0"+str(i)+"_0"+str(j)+".png"
			nr_cell = numberForCellNotZero(cell)
			print(cell + " : " + str(nr_cell))
			board[i-1][j-1] = nr_cell
	return board

cellCatch()