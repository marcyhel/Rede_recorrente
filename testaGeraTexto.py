import nltk 
from nltk.stem import RSLPStemmer
import copy
from rede_1 import *
import random
f = open('database.txt', 'r',encoding="utf8")
dados=f.read()
dados=dados.split('\n')
#print(dados)

def Tokenize(sentence):
	sentence = sentence.lower()
	sentence = nltk.word_tokenize(sentence)
	return sentence


def Learning(training_data):
	corpus_words = {}
	lista_palavras=[]
	for data in training_data:
		frase = data
		frase = Tokenize(frase)
		#frase = RemoveStopWords(frase)
		#frase = Stemming(frase)
		
		for word in frase:
			corpus_words[word] = 0
			if(word not in lista_palavras):
				lista_palavras.append(word)
	corpus_words[' '] = 0	
	return corpus_words,lista_palavras
saida,lista=Learning(dados)
#print(saida)
novodado=[]
total_pontos=0
for c,i in enumerate(dados):
	novodado.append(i.split(' '))
	total_pontos+=len(novodado[c])-1
#print(novodado)
#a=get_lista_vetor(dados[1])
#print(a)

class Rede:
	def __init__(self):
		self.pontos=0
		self.id=random.randint(0,1000)
		self.rede=RedeNeural()
		self.rede.ativador=RedeNeural.tanh
		self.rede.addNeuronio(len(saida),10)
		self.rede.addNeuronio(10,10)
		self.rede.addNeuronio(10,len(saida))
		self.rede.neuronios[0].dado=self.rede.ler('gera_texto0')
		self.rede.neuronios[1].dado=self.rede.ler('gera_texto1')
		self.rede.neuronios[2].dado=self.rede.ler('gera_texto2')

		self.rede.pesos_recorre[0].dado=self.rede.ler('pesos_gera_texto0')
		self.rede.pesos_recorre[1].dado=self.rede.ler('pesos_gera_texto1')
		self.rede.pesos_recorre[2].dado=self.rede.ler('pesos_gera_texto2')
	def reset(self):
		self.pontos=0
		self.rede.limparRecorre()
	def releitura(self,frase):
		for i in frase:
			print(lista[(i.index(1))])
	def get_vetor(self,entrada):
		aux_saida=copy.deepcopy(saida)

		try:
			aux_saida[entrada]+=1
		except:
			aux_saida[' ']+=1
		
		aux=[]
		for chave , valor in aux_saida.items():
			aux.append(valor)
		return aux
	def get_lista_vetor(self,fase):
		#print(fase)
		frase= fase.split(' ')
		aux=[]
		for i in frase:
			aux.append(self.get_vetor(i))
		return aux
	def verifica(self,entrada):
		resposta=self.rede.predictRecore(entrada)
		index=0
		aux=resposta.dado[0][0]
		#print(resposta.dado)
		for i in range(len(resposta.dado)):
			if(resposta.dado[i][0]>aux):
				aux=resposta.dado[i][0]
				index=i
		return index
rede=Rede()
while True:
	entrada=input('digite uma frase:')
	rede.rede.limparRecorre()
	entradas=rede.get_lista_vetor(entrada)
	aux=0
	print('')
	for i in entradas:
		aux=rede.verifica(i)
		print(lista[aux] ,end=' ')

	for i in range(10):
		aux=rede.verifica(rede.get_vetor(lista[aux]))
		print(lista[aux] ,end=' ')
	print('')
	print('')

#rede=Rede()
#print(rede.verifica(rede.get_vetor(novodado[0][0])))
#print(rede.get_vetor(novodado[0][1]).index(1))
#print(rede.verifica(rede.get_vetor('dia')))
#print(rede.verifica(rede.get_vetor('dia')))