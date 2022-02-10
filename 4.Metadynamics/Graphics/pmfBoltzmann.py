#!/usr/bin/env python
#Linha de comando para execução: python pmfBoltzmann.py arquivo.pmf > arquivosaida.txt
import sys
import math
import numpy as np

#Parametro - arquivo pmf
param = sys.argv[1:]

#leitura do arquivo e descarte das 3 primeiras linhas
read=open(param[0]).readlines()

firstLine = read.pop(0) #removes the first line
a = read
secondLine = a.pop(0) #removes the second line
c = a
thirdLine = c.pop(0) #removes the third line

#Valores das constantes
constBoltz = 0.001985875 #Boltzmann em kcal/(mol.K)
temp = 300 #Temperatura
kt = constBoltz * temp
beta = (1/kt)

new=[] #Coluna 0
ener=[] #Coluna 2

#Separacao do arquivo
for line in c:
    columns = line.split()
    if len(columns) >= 3:
       new.append(columns[0])
       ener.append(float(columns[2]))

energiaTotal = 0
energiaparcial=[]

enerparcial = 0
energiainicial = new[0]
newinicial=[]

dist = []
dist.append(energiainicial)

#Calculo da Energia
for i in range(len(ener)):
	energiaTotal = energiaTotal + math.exp(-beta*ener[i])

	if energiainicial == new[i]:
		enerparcial = enerparcial + math.exp(-beta*ener[i])
	else:
		energiaparcial.append(enerparcial)
		enerparcial = math.exp(-beta*ener[i])
		energiainicial = new[i]
		dist.append(energiainicial)

energiaparcial.append(enerparcial)

maior = float('-inf')

#Calculo energia total
for j in range(len(energiaparcial)):
	
	total = np.log(energiaparcial[j]/energiaTotal)*(-kt)

	if total <= float('inf') and total > maior:
		maior = total

	newinicial.append(total)

#Apresentacao dos dados
for j in range(len(newinicial)):
	#if newinicial[j] == float('inf'):
	#	newinicial[j] = maior

	print (dist[j] + " " + str(newinicial[j]))
