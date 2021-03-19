from django.db import models
from alpha_vantage.timeseries import TimeSeries
import json

class Acao(models.Model):
	abertura = models.FloatField(null=False)
	fechamento = models.FloatField(null=False)
	baixa = models.FloatField(null=False)
	alta = models.FloatField(null=False)
	codigo = models.CharField(max_length=10, null=False)
	volume = models.IntegerField(null=False)
	empresa = models.CharField(max_length=25, null=False)
	media = models.FloatField(null=False)
	data = models.DateField(null=False)

	def buscar(codigo_da_acao, dias=20, output='full'):

		def get_stock_info(symbol, tempo):
		  ts = TimeSeries(key="Y776KGDDB6F03CB2")
		  data, _ = ts.get_daily(symbol=symbol+'.SAO', outputsize=output)
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
		return acao
