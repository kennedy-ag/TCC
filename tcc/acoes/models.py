from django.db import models

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

	def buscar():
		pass