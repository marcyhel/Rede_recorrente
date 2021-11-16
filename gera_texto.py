import nltk 
from nltk.stem import RSLPStemmer
import copy
from rede_1 import *
import random
import re, string
f = open('database.txt', 'r',encoding="utf8")
dados=f.read()
dados=dados.split('\n')

print(dados)

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
print(saida)
novodado=[]
total_pontos=0
for c,i in enumerate(dados):
	novodado.append(i.split(' '))
	total_pontos+=len(novodado[c])-1
print(novodado)
print(total_pontos)
#a=get_lista_vetor(dados[1])
#print(a)

class Rede:
	def __init__(self):
		self.pontos=0
		self.id=random.randint(0,1000)
		self.rede=RedeNeural()
		self.rede.ativador=RedeNeural.tanh
		self.rede.addNeuronio(len(saida),20)
		self.rede.addNeuronio(20,10)
		self.rede.addNeuronio(10,len(saida))
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

class Genetico:
	def __init__(self,populacao=50,melhores=10,porcentagem=0.5,voltas=3):
		self.populacao=populacao
		self.qtd_melhores=melhores
		self.porcentagem=porcentagem
		self.individuos=[]
		self.voltas=voltas
		self.voltasDadas=0
		self.tamanhoTabuleiro=60
		self.criaPopulacao()
		self.contGeracao=0
	def criaPopulacao(self):
		for i in range(self.populacao):
			self.individuos.append(Rede())
	def verificaPontos(self):
		cont=0
		for i in self.individuos:
			for j in novodado:
				i.rede.limparRecorre()
				for c in range(len(j)-1):
					result=i.verifica(i.get_vetor(j[c]))
					resultado_ideal=i.get_vetor(j[c+1]).index(1)
					if(result==resultado_ideal):
						i.pontos+=1
	def ordena(self):
		for i in range(len(self.individuos)):
			for j in range(len(self.individuos)):
				if(self.individuos[i].pontos>self.individuos[j].pontos):
					aux=self.individuos[i]
					self.individuos[i]=self.individuos[j]
					self.individuos[j]=aux
		aux=[]
		for i in range(self.populacao-self.qtd_melhores):
			self.individuos.pop()
	def crossOver(self):
		melhores=copy.deepcopy(self.individuos)
		for i in range(self.populacao-self.qtd_melhores):
			novo=Rede()
			#cross
			if(random.random()<=0.7):
				pai=random.sample(melhores,3)
				for i in range(len(novo.rede.neuronios)):
					novo.rede.neuronios[i]=copy.deepcopy(pai[random.randint(0,len(pai)-1)].rede.neuronios[i])
			#mutacao
			if(random.random()<=self.porcentagem):
				for i in range(int(len(novo.rede.neuronios)/random.randint(2,5))+1):
					x=random.randint(0,len(novo.rede.neuronios[i].dado)-1)
					y=random.randint(0,len(novo.rede.neuronios[i].dado[0])-1)
					novo.rede.neuronios[i].dado[x][y]=random.random()* 2-1

				for i in range(int(len(novo.rede.pesos_recorre)/random.randint(2,5))+1):
					x=random.randint(0,len(novo.rede.pesos_recorre[i].dado)-1)
					y=random.randint(0,len(novo.rede.pesos_recorre[i].dado[0])-1)
					novo.rede.pesos_recorre[i].dado[x][y]=random.random()* 2-1
			#add individuo
			self.individuos.append(novo)
	def update(self):
		
		
		self.verificaPontos()
		self.ordena()
		print("geracao: {}".format(self.contGeracao))
		self.individuos[0].rede.salvar('Status',[[self.contGeracao,self.individuos[0].pontos]])
		for i in self.individuos:
			print(i.id,i.pontos,total_pontos)
			i.reset()
		for i in range(len(self.individuos[0].rede.neuronios)):
			self.individuos[0].rede.salvar('gera_texto'+str(i),self.individuos[0].rede.neuronios[i].dado)
		for i in range(len(self.individuos[0].rede.pesos_recorre)):
			self.individuos[0].rede.salvar('pesos_gera_texto'+str(i),self.individuos[0].rede.neuronios[i].dado)

		self.contGeracao+=1
		self.crossOver()
		

	
	

gene=Genetico(populacao=30,melhores=5,porcentagem=0.5,)

while True:
	gene.update()
#rede=Rede()
#print(rede.verifica(rede.get_vetor(novodado[0][0])))
#print(rede.get_vetor(novodado[0][1]).index(1))
#print(rede.verifica(rede.get_vetor('dia')))
#print(rede.verifica(rede.get_vetor('dia')))