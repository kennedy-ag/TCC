from django.shortcuts import render
from .models import Acao

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
	dados['ultimo'] = list(dados['datas'])


	return render(request, 'acoes.html', {'dados': dados})








def teste(request, codigo_da_acao, dias=20):

	if(Acao.objects.get(codigo=codigo_da_acao)):
		acoes = Acao.objects.filter(codigo=codigo_da_acao)
		dados = {}
		dados['aberturas'] = []
		dados['altas'] = []
		dados['baixas'] = []
		dados['fechamentos'] = []
		dados['volumes'] = []

		for i in acoes:
			dados['aberturas'].append(round(float(i.abertura), 2))
			dados['altas'].append(round(float(i.alta), 2))
			dados['baixas'].append(round(float(i.baixa), 2))
			dados['fechamentos'].append(round(float(i.fechamento), 2))
			dados['volumes'].append(i.volume)
		dados['codigo'] = codigo_da_acao
	else:

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
		dados['ultimo'] = list(dados['datas'])


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

		for i in lista_de_acoes:
			acao = Acao(abertura=lista_de_acoes[i][0], fechamento=lista_de_acoes[i][1], baixa=lista_de_acoes[i][2], alta=lista_de_acoes[i][3], codigo=lista_de_acoes[i][4], volume=lista_de_acoes[i][5], empresa=lista_de_acoes[i][6], media=lista_de_acoes[i][7], data=lista_de_acoes[i][8])

	return render(request, 'teste.html', {'dados': dados})