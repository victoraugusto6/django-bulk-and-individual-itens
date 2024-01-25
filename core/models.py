from django.db import models


class Pessoa(models.Model):
    nome = models.CharField(max_length=60)
    sobrenome = models.CharField(max_length=60)
    cpf = models.CharField(max_length=11)
    idade = models.SmallIntegerField()
