from django.db import models


# Create your models here.


class Orcamento(models.Model):
    ordem = models.CharField(max_length=10, choices={'RECEITA': 'RECEITA', 'DESPESA': 'DESPESA'})
    descricao = models.CharField(max_length=150, verbose_name='descrição')
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.CharField(max_length=25, choices={
        'Salário': 'Salário',
        'Renda Extra': 'Renda Extra',
        'Renda Passiva': 'Renda Passiva',
        'Investimento': 'Investimento',
        'Skin': 'Skin',
        'Transporte': 'Transporte',
        'Moradia': 'Moradia',
        'Alimentação': 'Alimentação',
        'Lazer': 'Lazer',
        'Outros': 'Outros'
    })
    periodo = models.DateField()
    fixo = models.BooleanField()
    credito = models.BooleanField(verbose_name='crédito')

    def __str__(self):
        return "{} - {} ({})".format(self.ordem, self.descricao, self.periodo)
