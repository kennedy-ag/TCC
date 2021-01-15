from django.shortcuts import render

def index(request): 
    return render(request, 'index.html')

def acoes(request, codigo_da_acao, dias=7):

	from alpha_vantage.timeseries import TimeSeries
	import json

	def get_stock_info(symbol, tempo=0):
	  ts = TimeSeries(key="mykey")
	  data, _ = ts.get_daily(symbol=symbol+'.SAO', outputsize='full')
	  if(tempo==0):
	    return data
	  else:
	    lista_temporal = {}
	    limitador = 0
	    for i in data:
	      if(limitador==tempo):
	        break
	      else:
	        lista_temporal[i] = data[i]
	        lista_temporal[i]['0. empresa'] = name_stock(symbol)
	        limitador += 1
	    return lista_temporal

	def name_stock(stock_id):
		import json
		nomes = open('static/nomes.json').read()
		nomes = json.loads(nomes)
		stock_name = nomes[stock_id]
		return stock_name



	acao = get_stock_info(codigo_da_acao, dias)

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