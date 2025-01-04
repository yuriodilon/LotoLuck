from django.db import models

# Create your models here.

from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User  # Importa a tabela padrão de usuários do Django

class Jogo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jogos')
    nJogo = models.AutoField(primary_key=True)  # Número único do jogo
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação do jogo
    nomeJogo = models.CharField(max_length=255)
    bola1 = models.IntegerField()
    bola2 = models.IntegerField()
    bola3 = models.IntegerField()
    bola4 = models.IntegerField()
    bola5 = models.IntegerField()
    bola6 = models.IntegerField()
    bola7 = models.IntegerField()
    bola8 = models.IntegerField()
    bola9 = models.IntegerField()
    bola10 = models.IntegerField()
    bola11 = models.IntegerField()
    bola12 = models.IntegerField()
    bola13 = models.IntegerField()
    bola14 = models.IntegerField()
    bola15 = models.IntegerField()

    def __str__(self):
        return f"Jogo {self.nJogo} - Usuário: {self.usuario.username}"

#====================SOBRE CONCURSO PASSADOS ===========================+#
class Concurso(models.Model):
    nConcurso = models.IntegerField(verbose_name="Número do Concurso")
    data_concurso = models.DateField(verbose_name="Data do Concurso")
    bola1 = models.IntegerField(verbose_name="Bola 1")
    bola2 = models.IntegerField(verbose_name="Bola 2")
    bola3 = models.IntegerField(verbose_name="Bola 3")
    bola4 = models.IntegerField(verbose_name="Bola 4")
    bola5 = models.IntegerField(verbose_name="Bola 5")
    bola6 = models.IntegerField(verbose_name="Bola 6")
    bola7 = models.IntegerField(verbose_name="Bola 7")
    bola8 = models.IntegerField(verbose_name="Bola 8")
    bola9 = models.IntegerField(verbose_name="Bola 9")
    bola10 = models.IntegerField(verbose_name="Bola 10")
    bola11 = models.IntegerField(verbose_name="Bola 11")
    bola12 = models.IntegerField(verbose_name="Bola 12")
    bola13 = models.IntegerField(verbose_name="Bola 13")
    bola14 = models.IntegerField(verbose_name="Bola 14")
    bola15 = models.IntegerField(verbose_name="Bola 15")

    # Campos opcionais com null=True e blank=True
    ganhadores_15 = models.IntegerField(verbose_name="Ganhadores 15 Acertos", null=True, blank=True)
    rateio_15 = models.DecimalField(verbose_name="Rateio 15 Acertos", max_digits=10, decimal_places=2, null=True, blank=True)
    ganhadores_14 = models.IntegerField(verbose_name="Ganhadores 14 Acertos", null=True, blank=True)
    rateio_14 = models.DecimalField(verbose_name="Rateio 14 Acertos", max_digits=10, decimal_places=2, null=True, blank=True)
    ganhadores_13 = models.IntegerField(verbose_name="Ganhadores 13 Acertos", null=True, blank=True)
    rateio_13 = models.DecimalField(verbose_name="Rateio 13 Acertos", max_digits=10, decimal_places=2, null=True, blank=True)
    ganhadores_12 = models.IntegerField(verbose_name="Ganhadores 12 Acertos", null=True, blank=True)
    rateio_12 = models.DecimalField(verbose_name="Rateio 12 Acertos", max_digits=10, decimal_places=2, null=True, blank=True)
    ganhadores_11 = models.IntegerField(verbose_name="Ganhadores 11 Acertos", null=True, blank=True)
    rateio_11 = models.DecimalField(verbose_name="Rateio 11 Acertos", max_digits=10, decimal_places=2, null=True, blank=True)
    acumulado_total = models.DecimalField(verbose_name="Acumulado Total", max_digits=10, decimal_places=2, null=True, blank=True)
    estimativa_premio = models.DecimalField(verbose_name="Estimativa de Prêmio", max_digits=10, decimal_places=2, null=True, blank=True)
    acumulado_especial = models.DecimalField(verbose_name="Acumulado Sorteio Especial", max_digits=10, decimal_places=2, null=True, blank=True)
    cidade_uf = models.CharField(verbose_name="Cidade/UF", max_length=255, null=True, blank=True)
    observacao = models.TextField(verbose_name="Observação", null=True, blank=True)

    def __str__(self):
        return f"Concurso {self.nConcurso} - {self.data_concurso.strftime('%d/%m/%Y')}"

