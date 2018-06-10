# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 15:37:32 2018

@author: sofia
"""

from graphs import MyGraph
import plotly
import plotly.graph_objs as go


#Projeto 
def open_file(filename = 'harry.txt'):
    h= open(filename,'r')
    harry = h.readlines()
    h.close()
    return harry

def num_phrases(list_lines):
    phrases = 0
    for i in range(len(list_lines)):
        if list_lines[i]== '\n':
            phrases += 1
    return phrases

    
def all_lines_with_NP (list_lines):
    np = []
    for i in range(len(list_lines)):         #tentar retirar só os que têm Nomes Próprios
        if 'NP' in list_lines[i]:
            np.append(list_lines[i])
    return np

def all_NP(lines_NP):
    name = []
    for i in range(len(lines_NP)):
        l = lines_NP[i].split(' ')
        name.append(l[0])
    return name

def dic_NP(list_names):
    dic={}
    for p in list_names:
        if p in dic:
            dic[p] +=1
        else: dic[p]=1
    
    dic_sort = sorted((value,key) for (key,value) in dic.items())       
    return dic_sort

def rank50 (dic_NP):
    return dic_NP[-50:]

def list_phrases(list_lines):    #chave é o numero da linha, valor é uma lista com todas as palavras da frase
    dic_lines={}
    ind = 1
    for i in range(len(list_lines)):
        if list_lines[i] != '\n':
            if ind not in dic_lines:
                dic_lines[ind]=[list_lines[i]]
            else:
                dic_lines[ind].append(list_lines[i])
        else:
            ind += 1
    return dic_lines


#### para fazer grafo de relações!!!

def relationship(dic_lines): #dicionario com a chave como o número da frase e o valor com os nomes proprios existentes nessa frase (só com as frases que têm mais do que um nome próprio)
    dic = {}
    dic_relat = {}
    for k in dic_lines:
        for v in dic_lines[k]:  #isto já dá cada elemento da lista que está nos valores
                if 'NP' in v:
                    if k not in dic:
                        dic[k]=[v]
                    else: dic[k].append(v)
#    print(dic)
    for key in dic:
        if len(dic[key])>1:
            dic_relat[key]=dic[key]
#    print(dic_relat)
    return dic_relat


def graph_relat(dic_relat):   #assumindo que nomes próprios na mesma frase estão relacionados
    graph = {}
    for key in dic_relat:
        lista = []
        for value in dic_relat[key]:
            v = value.split(' ')
#            print(v)
            if v[3] == '1\n':           #filtrar as probabilidades maiores!
                lista.append(v[0])
        for i in lista:
            if i not in graph:
                graph[i]=lista    
#    print(graph)
    for k in graph:             #remover dos values do graph a propria chave
        if k in graph[k]:
            graph[k].remove(k)
#    print(graph)
    return graph


def graph_relat_50(dic_graph, r50):
    graph_50={}
    for np in r50:
#        print(np[1]) 
        for key in dic_graph:    
            for value in dic_graph[key]:
                if np[1] in dic_graph and len(dic_graph[np[1]]):
                    graph_50[np[1]]=dic_graph[np[1]]
                elif np[1] in dic_graph[value]:
                    if value not in graph_50:
                        graph_50[value] = [np[1]]
                    else: 
                        if np[1] not in graph_50[value]:
                            graph_50[value].append(np[1])
    return graph_50
        

### para fazer histograma de chunks 

def chunks (num_chunks,phrases, dic_relat):
    dic_chunks={}                      #key é o número do chunck, valor é o conjunto de linhas(lista de listas)
    d = phrases/num_chunks       
    i = 1
    chunk = 1
    while chunk <= num_chunks:
            while i <= d*chunk:  
                if chunk not in dic_chunks:
                    dic_chunks[chunk]=dic_relat[i]
                else: dic_chunks[chunk].append(dic_relat[i])
                i += 1
            chunk += 1
            
    return dic_chunks           

def freq_per_NP (NP, dic_chunks):  #fazer tabela com frequencia que é mencionado o nome escolhido pelo livro 
    freq = []
    for key in dic_chunks:
        num_np = 0
        for value in dic_chunks[key]:
            for word in value:
                if NP in word:  ## in porque nao vai ser igual, vai ter mais coisas como os números à frente e isso (nao conta duas vezes porque a palavra vai estar na frase)
                    num_np += 1
        freq.append(num_np)


    #parte do grafico
    data = [go.Bar(
            x = [i for i in range(1, len(freq)+1)],
            y = [i for i in freq]
        )]
    plotly.offline.plot(data, filename='grafico.html')

    return freq

def higher_freq(dic_chunks,r50):   #encontrar qual o nome próprio mais vezes mencionado em cada chunk
    freq = []
    for key in dic_chunks:
        num_np = {}
        for np in r50:
#            print(np[1])
            for value in dic_chunks[key]:
#                print(value)
                for word in value:
                    if np[1] in word:
                        if np[1] not in num_np:
                            num_np[np[1]] = 1
                        else: num_np[np[1]] += 1
#        print(num_np)
                    
        num_np_sorted = sorted(num_np, key=num_np.get, reverse = True)
#        print(num_np_sorted)
        
        freq.append((num_np_sorted[0], num_np[num_np_sorted[0]]))
#        print(freq)
            
     #parte do grafico          não dá direito
    data = [go.Bar(
            x = [i for i in range(len(freq))],
            y = [i[1] for i in freq]
        )]
    plotly.offline.plot(data, filename='grafico_HighFreq.html')

    return freq



if __name__ == '__main__':
    harry = open_file()
#    harry = open_file('frei.txt')
#    print(harry)
    phrases = num_phrases(harry)
    chunk = chunks(phrases, harry)
    np = all_lines_with_NP (harry)
    names_NP = all_NP(np)
#    print(names_NP)
    dic_np = dic_NP(names_NP)
#    print(dic_NP(names_NP))
    r50 = rank50(dic_np)
#    print(r50)
#    print(phrases)
#    print(phrases/60)
#    print(chunk)
    dic_lines=list_phrases(harry)
    dic_relat = relationship(dic_lines)
#    print(dic_relat)
    dic_graph= graph_relat(dic_relat)
    graph_50 = graph_relat_50(dic_graph, r50)
#    print(dic_graph)
    graph = MyGraph(graph_50)
    graph.print_graph()             #grafo de relações!!!
    dic_chunks = chunks(60,phrases, dic_lines)
#    print(dic_chunks)
    freq = freq_per_NP('Harry', dic_chunks)    #freq = freq_per_NP('Dudley', dic_chunks)
#    print(freq)
    highFreq = higher_freq(dic_chunks, r50)
#    print(highFreq)
    