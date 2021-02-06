from django.shortcuts import render
from .models import Acao
from datetime import date, timedelta

def index(request): 
    return render(request, 'index.html')


def acoes(request, codigo_da_acao, dias=20):

	acao = Acao.buscar(codigo_da_acao, dias)

	dados = {}
	media = 0
	quantidade = 0
	dados['aberturas'] = []
	dados['altas'] = []
	dados['baixas'] = []
	dados['fechamentos'] = []
	dados['volumes'] = []

	for i in acao:
		dados['aberturas'].append(round(float(acao[i]['1. open']), 2))
		dados['altas'].append(round(float(acao[i]['2. high']), 2))
		dados['baixas'].append(round(float(acao[i]['3. low']), 2))
		dados['fechamentos'].append(round(float(acao[i]['4. close']), 2))
		dados['volumes'].append(acao[i]['5. volume'])
		dados['empresa'] = acao[i]['0. empresa']
		
		media += float(acao[i]['4. close'])
		quantidade += 1

	media = round(media/quantidade, 2)
	dados['media'] = media
	dados['codigo'] = codigo_da_acao
	dados['dias'] = quantidade
	dados['datas'] = acao.keys()
	dados['ultimo'] = list(dados['datas'])[0]


	return render(request, 'acoes.html', {'dados': dados})








def teste(request, codigo_da_acao, dias=25):

	def gerar_estrutura(registros):
		dados = {}
		controlador_for = 0
		soma = 0
		dados['aberturas'] = []
		dados['altas'] = []
		dados['baixas'] = []
		dados['fechamentos'] = []
		dados['volumes'] = []
		dados['datas'] = []

		for i in registros:
			dados['aberturas'].append(round(float(i.abertura), 2))
			dados['altas'].append(round(float(i.alta), 2))
			dados['baixas'].append(round(float(i.baixa), 2))
			dados['fechamentos'].append(round(float(i.fechamento), 2))
			dados['volumes'].append(i.volume)
			dados['datas'].append(i.data)

			controlador_for += 1
			if(controlador_for==dias):
				break

		dados['codigo'] = codigo_da_acao
		dados['ultimo'] = dados['datas'][0]
		dados['empresa'] = i.empresa
		dados['dias'] = dias

		for i in dados['fechamentos']:
			soma += i
		dados['media'] = round(soma/len(dados['fechamentos']), 2)
		return dados




	def gerar_estrutura_banco(acao):

		dados = {}
		controlador_for = 0
		media = 0
		quantidade = 0
		dados['aberturas'] = []
		dados['altas'] = []
		dados['baixas'] = []
		dados['fechamentos'] = []
		dados['volumes'] = []

		for i in acao:
			dados['aberturas'].append(round(float(acao[i]['1. open']), 2))
			dados['altas'].append(round(float(acao[i]['2. high']), 2))
			dados['baixas'].append(round(float(acao[i]['3. low']), 2))
			dados['fechamentos'].append(round(float(acao[i]['4. close']), 2))
			dados['volumes'].append(acao[i]['5. volume'])
			dados['empresa'] = acao[i]['0. empresa']
			
			media += float(acao[i]['4. close'])
			quantidade += 1

			

		media = round(media/quantidade, 2)
		dados['media'] = media
		dados['codigo'] = codigo_da_acao
		dados['dias'] = quantidade
		dados['datas'] = list(acao.keys())[0:quantidade]
		dados['ultimo'] = dados['datas'][0]

		return dados


	def salvar(dados):
		# Parte responsável pelo envio dos dados ao banco
		lista_de_acoes = []
		for i in dados['aberturas']:
			lista_de_acoes.append([])
		for i in range(0, len(lista_de_acoes)):
			lista_de_acoes[i].append(dados['aberturas'][i])
			lista_de_acoes[i].append(dados['fechamentos'][i])
			lista_de_acoes[i].append(dados['baixas'][i])
			lista_de_acoes[i].append(dados['altas'][i])
			lista_de_acoes[i].append(dados['codigo'])
			lista_de_acoes[i].append(dados['volumes'][i])
			lista_de_acoes[i].append(dados['empresa'])
			lista_de_acoes[i].append(dados['media'])
			lista_de_acoes[i].append(dados['datas'][i])

		for i in range(len(lista_de_acoes)):
			a = Acao(abertura=lista_de_acoes[i][0], fechamento=lista_de_acoes[i][1], baixa=lista_de_acoes[i][2], alta=lista_de_acoes[i][3], codigo=lista_de_acoes[i][4], volume=lista_de_acoes[i][5], empresa=lista_de_acoes[i][6], media=lista_de_acoes[i][7], data=lista_de_acoes[i][8])
			a.save()




	# Verifica se já existe registro desse código no banco, se existir, gera a estrutura de dados
	# que será passada para o template de acordo com os dados capturados do banco.

	if(len(list(Acao.objects.filter(codigo=codigo_da_acao)))>0):
		registros = Acao.objects.filter(codigo=codigo_da_acao)
		ontem = date.today() - timedelta(1)
		ultima_data_registrada = registros[0].data
		dados = {'dracarys': 1000}



	# Caso não exista registro ainda, ele busca as informações direto da API, monta a estrutura
	# que será passada ao template, preenche com os dados da API, gera o insert que manda as in-
	# formações ao banco a partir dessa estrutura.
	else:
		acao = Acao.buscar(codigo_da_acao, 300)
		dados = gerar_estrutura_banco(acao)

		
	return render(request, 'test.html', {'dados': dados})