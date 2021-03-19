from django.shortcuts import render
from .models import Acao
from datetime import date, timedelta
from django.http import HttpRequest
import numpy as np

def index(request): 
    return render(request, 'index.html')


def acoes(request, codigo_da_acao, dias=25):

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

		media = np.mean(dados['fechamentos'])
		recente = dados['fechamentos'][0]
		rendimento = round(((recente/media)*100)-100, 2)

		dados['rendimento'] = rendimento
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

		for i in dados:
			if(type(dados[i]) is list):
				dados[i].reverse()

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


	def verificar_datas(acao, ultima):
		from datetime import datetime
		l = []
		for i in acao.keys():
			if(datetime.strptime(i, '%Y-%m-%d').date()<=ultima):
				l.append(i)
		for i in l:
			del acao[i]
		return acao




	# Verifica se já existe registro desse código no banco, se existir, gera a estrutura de dados
	# que será passada para o template de acordo com os dados capturados do banco.

	if(len(list(Acao.objects.filter(codigo=codigo_da_acao)))>0):
		registros = Acao.objects.filter(codigo=codigo_da_acao)
		registros = list(registros)
		if(date.today().weekday()==6):
			dd = 2
		elif(date.today().weekday()==0):
			dd = 3
		else:
			dd = 1
		ontem = date.today() - timedelta(dd)
		ultima_data_registrada = registros[len(registros)-1].data
		registros.reverse()
		if(ultima_data_registrada==ontem):
			dados = gerar_estrutura(registros)
		else:
			quantidade_dias = abs((ontem - ultima_data_registrada).days)
			acao = Acao.buscar(codigo_da_acao, quantidade_dias, 'compact')
			a = verificar_datas(acao, ultima_data_registrada)
			d = gerar_estrutura_banco(acao)
			salvar(d)
			registros = Acao.objects.filter(codigo=codigo_da_acao)
			dados = gerar_estrutura(registros)



	# Caso não exista registro ainda, ele busca as informações direto da API, monta a estrutura
	# que será passada ao template, preenche com os dados da API, gera o insert que manda as in-
	# formações ao banco a partir dessa estrutura.
	else:
		acao = Acao.buscar(codigo_da_acao, 300)
		dados = gerar_estrutura_banco(acao)
		d = gerar_estrutura_banco(acao)
		salvar(d)
		registros = Acao.objects.filter(codigo=codigo_da_acao)
		dados = gerar_estrutura(registros)

		
	return render(request, 'acoes.html', {'dados': dados})


def introducao(request):
	return render(request, 'introducao.html')

def tecnicas(request):
	return render(request, 'tecnicas.html')

def lista(request):
	acoes = Acao.objects.all()
	lista_de_tickers = []
	tabela = {}
	aux = 1

	for i in acoes:
		if(i.codigo not in lista_de_tickers):
			lista_de_tickers.append(i.codigo)

	for i in lista_de_tickers:
		acao = Acao.objects.filter(codigo=i)
		acao = list(acao)
		acao.reverse()
		acao = acao[0]
		tabela[acao.codigo] = {
			'linha': aux,
			'empresa': acao.empresa,
			'fechamento': acao.fechamento
		}
		aux += 1

	return render(request, 'lista_de_acoes.html', {'tabela': tabela})


def comparacao(request, dias=50):
	lista_de_acoes = request.GET.lists()
	lista_de_acoes = dict(lista_de_acoes)
	lista_de_acoes = lista_de_acoes['acoes_lista']
	lista_de_fechamentos = []
	lista_de_datas = []

	for i in range(0, len(lista_de_acoes)):
		lista_de_fechamentos.append([])

	for i in range(0, len(lista_de_acoes)):
		controlador = 0
		registros = Acao.objects.filter(codigo=lista_de_acoes[i])
		registros = list(registros)
		registros.reverse()

		for registro in registros:
			if(controlador==dias):
				break
			lista_de_fechamentos[i].append(registro.fechamento)
			if(registro.data not in lista_de_datas):
				lista_de_datas.append(registro.data)
			controlador += 1

	return render(request, 'comparativo.html', {'dados': lista_de_fechamentos, 'datas': lista_de_datas, 'dias': len(lista_de_datas), 'tickers': lista_de_acoes})


def perfil(request):
	return render(request, 'perfil.html')

def sugestoes(request):
	info = dict(request.GET)
	acoes = Acao.objects.all()
	lista_de_tickers = []
	fechamentos = []
	tabela = {}
	aux = 1
	valor = int(info['valor'][0])
	meses = int(info['meses'][0])
	possui = int(info['possui'][0])
	precisa = 100 - round((possui/valor)*100, 2)

	for i in acoes:
		if(i.codigo not in lista_de_tickers):
			lista_de_tickers.append(i.codigo)

	for i in lista_de_tickers:
		acao = Acao.objects.filter(codigo=i)
		acao = list(acao)
		acao.reverse()

		for i in range(0, 70):
			fechamentos.append(acao[i].fechamento)

		media = np.mean(fechamentos)
		recente = fechamentos[0]
		rendimento = round(((recente/media)*100)-100, 2)
		fechamentos = []
		acao = acao[0]

		if(meses>=24):
			if(precisa>=50):
				if(possui>=2000):
					if(rendimento<=15 and rendimento>=5 and acao.fechamento>70):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
				else:
					if(rendimento<=15 and rendimento>=5 and acao.fechamento>=10 and acao.fechamento<=40):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
			else:
				if(rendimento<=18 and rendimento>=8 and acao.fechamento>10 and acao.fechamento<=70):
					tabela[acao.codigo] = {
						'empresa': acao.empresa,
						'fechamento': acao.fechamento,
						'rendimento': rendimento
					}


		elif(meses<=12):
			if(precisa>=50):
				if(possui>=2000):
					if(rendimento>=20 and acao.fechamento>70):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
				else:
					if(rendimento>=20 and acao.fechamento>=20 and acao.fechamento<=40):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
			else:
				if(rendimento>=20 and acao.fechamento>10 and acao.fechamento<=70):
					tabela[acao.codigo] = {
						'empresa': acao.empresa,
						'fechamento': acao.fechamento,
						'rendimento': rendimento
					}


		else:
			if(precisa>=50):
				if(possui>=2000):
					if(rendimento>10 and rendimento<20 and acao.fechamento>50):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
				else:
					if(rendimento>10 and rendimento<20 and acao.fechamento>=20 and acao.fechamento<=40):
						tabela[acao.codigo] = {
							'empresa': acao.empresa,
							'fechamento': acao.fechamento,
							'rendimento': rendimento
						}
			else:
				if(rendimento<=18 and rendimento>=8 and acao.fechamento>10 and acao.fechamento<=70):
					tabela[acao.codigo] = {
						'empresa': acao.empresa,
						'fechamento': acao.fechamento,
						'rendimento': rendimento
					}

		aux += 1

	return render(request, 'sugestoes.html', {'tabela': tabela, 'dados': info})


def queda(request):
	acoes = Acao.objects.all()
	lista_de_tickers = []
	fechamentos = []
	queda = {}

	for i in acoes:
		if(i.codigo not in lista_de_tickers):
			lista_de_tickers.append(i.codigo)

	for i in lista_de_tickers:
		acao = Acao.objects.filter(codigo=i)
		acao = list(acao)
		acao.reverse()

		for i in range(0, 50):
			fechamentos.append(acao[i].fechamento)

		media = np.mean(fechamentos)
		recente = fechamentos[0]
		rendimento = round(((recente/media)*100)-100, 2)
		fechamentos = []
		acao = acao[0]

		if(rendimento<0):
			queda[acao.codigo] = {
				'empresa': acao.empresa,
				'fechamento': acao.fechamento,
				'rendimento': rendimento
			}

	return render(request, 'queda.html', {'queda': queda})