# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from datetime import datetime
import sys
import time
from django.db import models
from localflavor.br.br_states import STATE_CHOICES
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.utils.html import mark_safe
from django.db.models import F, FloatField, Sum
from decimal import Decimal
from django import forms


class Carro(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
        
class Localidade(models.Model):
    nome = models.CharField(max_length=200)
    uf = models.CharField(max_length=50, choices = STATE_CHOICES)

    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False):
        self.nome = self.nome.upper()
        super(Localidade, self).save(force_insert, force_update)

class Agencia(models.Model):
    localidade = models.ForeignKey(Localidade, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=50, choices = STATE_CHOICES)
    cep = models.CharField(max_length=8, null=True)
    telefone = models.CharField(max_length=14)
    email = models.CharField(max_length=100, null=True, blank=True)

    @staticmethod
    def autocomplete_search_fields():
        return 'nome',
    
    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False):
        self.nome = self.nome.upper()
        self.endereco = self.endereco.upper()
        self.bairro = self.bairro.upper()
        self.cidade = self.cidade.upper()
        super(Cliente, self).save(force_insert, force_update)

class Empresa(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18)
    ie = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False):
        self.nome = self.nome.upper()
        self.cnpj = self.cnpj.upper()
        self.ie = self.ie.upper()
        super(Empresa, self).save(force_insert, force_update)

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    valor = models.DecimalField(verbose_name=u'valor',
                                 max_digits=15, decimal_places=2)
    #estoque = models.PositiveIntegerField(null=True, blank=False)
    
    def __str__(self):
        return '%s %s' % (self.nome,  str(self.valor))

    def save(self, force_insert=False, force_update=False):
        self.nome = self.nome.upper()
        super(Produto, self).save(force_insert, force_update)


class Motorista(models.Model):
    chapa = models.CharField(max_length=200)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=14)

    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False):
        self.chapa = self.chapa.upper()
        self.nome = self.nome.upper()
        super(Motorista, self).save(force_insert, force_update)


TIPO_FRETE = (
        ('PAGO', 'PAGO'),
        ('A PAGAR', 'A PAGAR'),
	    ('CORTESIA', 'CORTESIA')
    )

RESPONSAVEL_FRETE = (
        ('REMETENTE', 'REMETENTE'),
        ('DESTINATARIO', 'DESTINATARIO'),
	    ('REDESPACHO', 'REDESPACHO')
    )
SITUACAO_VENDA = (
        ('ATIVA', 'ATIVA'),
        ('CANCELADA', 'CANCELADA')
    )

CARTOES = (
        ('DINNER CLUBS', 'DINNER CLUBS'),
        ('AMERICAN EXPRESS', 'AMERICAN EXPRESS'),
        ('CRED SHOP', 'CRED SHOP'),
        ('MASTER CARD', 'MASTER CARD'),
        ('VISA', 'VISA')
    )

class Venda(models.Model):
    id = models.AutoField(u'AÇAIEX', primary_key=True)
    hora_saida = models.TimeField(max_length=6)
    responsavel_frete = models.CharField(max_length=14, verbose_name=u'Resp. Frete', choices = RESPONSAVEL_FRETE, default='REMETENTE')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    localidade_origem = models.ForeignKey(Localidade, on_delete=models.CASCADE, verbose_name=u'Loc. Origem', related_name ='localidade_origem')
    localidade_destino = models.ForeignKey(Localidade, on_delete=models.CASCADE, verbose_name=u'Loc. Destino', related_name ='localidade_destino')	
    cliente_origem = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name ='cliente_origem')
    cliente_destino = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name ='cliente_destino')
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    motorista_principal = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name ='motorista_principal')
    motorista_reserva = models.ForeignKey(Motorista, on_delete=models.CASCADE , related_name ='motorista_reserva',  null=True, blank=True)
    #valores default
    data_venda = models.DateField(auto_now_add=True, verbose_name=u'Data',)
    situacao_venda = models.CharField(max_length=10, verbose_name=u'Situação', choices = SITUACAO_VENDA, default='ATIVA')  
    #aba de valores teste
    tipo_frete = models.CharField(max_length=10, choices = TIPO_FRETE, default='PAGO')
    dinheiro = models.BooleanField()
    cartao = models.BooleanField()
    cartoes = models.CharField(max_length=30, choices = CARTOES, default='DINNER CLUBS', null=True, blank=True)
    ano_processo = models.CharField(max_length=4, choices = CARTOES, default='VISA', null=True, blank=True)      
   
    #valor_nota = models.DecimalField(verbose_name=u'Valor Nota',
    #                            max_digits=15, decimal_places=2, null=True, blank=True)
    valor_dinheiro = models.DecimalField(verbose_name=u'Valor Dinheiro',
                                 max_digits=15, decimal_places=2,  default=Decimal('0.00'))
    valor_cartao = models.DecimalField(verbose_name=u'Valor Cartão',
                                 max_digits=15, decimal_places=2, default=Decimal('0.00'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    #produto = models.ManyToManyField(Produto, blank=False, default=None)

    #staticmethod
    #def autocomplete_search_fields():
    #    return id,

    @staticmethod
    def autocomplete_search_fields():
        return 'id',

    def __str__(self):
        return str(self.id)

    def imprimir(self):
        return mark_safe("<a target='_blank' href='%s'>Imprimir</a>" % self.get_absolute_url())
    imprimir.allow_tags = True

    def get_absolute_url(self):
        return reverse('venda_detail', args=[self.pk, ])

    def get_venda(self):
        return Venda.objects.get(pk=self.pk)
    
    #soma o total de volume no relatorio
    def total(self):
        soma = Venda.objects.filter(id=self.id).aggregate(total=Sum('item__qtde', flat = True))
        return soma['total']

    def valortotal(self):
        soma = Venda.objects.filter(id=self.id).aggregate(valortotal=Sum(F('item__produto__valor') * F('item__qtde'), output_field=FloatField()))
        return soma['valortotal']

    def valortotalnota(self):
        return self.valor_nota   

        
    def valor_nota(self, force_insert=False, force_update=False):
        valor_nota = self.valor_dinheiro + self.valor_cartao 
        return valor_nota
    
    def desconto(self):
        valortotal = Venda.objects.filter(id=self.id).aggregate(valortotal=Sum(F('item__produto__valor') * F('item__qtde'), output_field=FloatField()))
        valor_nota = self.valor_nota
        # exemplo de porcetagem return  100 - float(valor_nota.replace(",",".")) * 100 / float(valortotal['valortotal'])
        if self.tipo_frete == 'CORTESIA':
            return 0.00
        else:
            return  Decimal(valortotal['valortotal']) - valor_nota()
        #return  valor_nota()
        #return float(valortotal['valortotal'])
    
    def clean(self, *args, **kwargs):
        valortotal = Venda.objects.filter(id=self.id).aggregate(valortotal=Sum(F('item__produto__valor') * F('item__qtde'), output_field=FloatField()))
        valor_nota = self.valor_nota
#        if Decimal(valortotal['valortotal']) < valor_nota():
#         raise forms.ValidationError("O  valor do Tipo de Pagamento (dinheiro + cartão) não pode ser maior que o valor total da nota.")    

    
        #super(Venda, self).save(force_insert, force_update)

    #update apenas do campo situacao_venda
    #def save(self, *args, **kwargs):
    #   venda = Venda.objects.filter(id=self.id).update(situacao_venda=self.situacao_venda)
    
    #    self.valor_dinheiro = float(self.valor_dinheiro)
    #    super(Venda, self).save(*args, **kwargs)

    #def lista(self):
    #    return mark_safe("<a target='_blank' href='%s'>Listar</a>" % self.get_absolute_url2())
    #    imprimir.allow_tags = True

    #def get_absolute_url2(self):
    #    return reverse('venda_list', args=[self.pk, ])

class ExcessoBagagem(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, default=None,)
    cliente = models.CharField(max_length=200)
    numero = models.CharField(max_length=200)
    volume = models.PositiveIntegerField(null=True, blank=False)
    data = models.DateField(default=timezone.now)
    intinerario_origem = models.ForeignKey(Localidade, on_delete=models.CASCADE, verbose_name=u'Intinerario. Origem', related_name ='intinerario_origem')
    intinerario_destino = models.ForeignKey(Localidade, on_delete=models.CASCADE, verbose_name=u'Intinerario. Destino', related_name ='intinerario_destino')  
    valor = models.DecimalField(verbose_name=u'Valor',
                                 max_digits=15, decimal_places=2,  default=Decimal('0.00'))
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def imprimir(self):
        return mark_safe("<a target='_blank' href='%s'>Imprimir</a>" % self.get_absolute_url())
    imprimir.allow_tags = True  

    def get_absolute_url(self):
        return reverse('excessobagagem_detail', args=[self.pk, ])
    #sem essa função não aparece as variaveis
    def get_excessobagagem(self):
        return ExcessoBagagem.objects.get(pk=self.pk)

    
class Item(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, default=None)
    qtde = models.PositiveIntegerField(null=True, blank=False)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, default=None)


class Recebimento(models.Model):
    data_recebimento = models.DateField(auto_now_add=True, verbose_name=u'Data',)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, default=None, verbose_name=u'venda', related_name ='venda', unique=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    

    #class Meta:
    #    ordering = ["venda"]

    def _str_(self):
        return self.data_recebimento


class Manifesto(models.Model):
    data_venda = models.DateField(default=timezone.now)
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
   # venda = models.ForeignKey(Venda, on_delete=models.CASCADE, default=None, null=True, blank=True)

    #agencia = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    #class Meta:
    #    ordering = ["venda"]

    def imprimir(self):
        return mark_safe("<a target='_blank' href='%s'>Imprimir</a>" % self.get_absolute_url())
    imprimir.allow_tags = True  

    def get_absolute_url(self):
        return reverse('manifesto_detail', args=[self.pk, ])
    #sem essa função não aparece as variaveis
    def get_manifesto(self):
        return Manifesto.objects.get(pk=self.pk)
        
    def total(self):
        #Entry.objects.filter(blog_id=4)
        teste = Venda.objects.all()
        soma = Venda.objects.filter(id=self.id).aggregate(total=Sum('item__qtde', flat = True))
        return soma['total']
       

    
        

   # def valor_nota(self, force_insert=False, force_update=False):
    #    return Venda.objects.get(valor_dinheiro=self.valor_dinheiro) + self.valor_cartao

    
    def _str_(self):
        return self.carro

    
        #return  valor['valor']

TIPOS = (
        ('ENVIO', 'ENVIO'),
        ('RECEBIMENTO', 'RECEBIMENTO'),
        ('GERAL','GERAL')
    )

class Relatorio(models.Model):
    data_inicial = models.DateField(default=timezone.now)
    data_final = models.DateField(default=timezone.now)
    tipo = models.CharField(max_length=30, choices = TIPOS, default='ENVIO')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    agencia = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    def imprimir(self):
        return mark_safe("<a target='_blank' href='%s'>Imprimir</a>" % self.get_absolute_url())
    imprimir.allow_tags = True

    def get_absolute_url(self):
        return reverse('venda_data_list', args=[self.pk, ])

    def __str__(self):
        return str(self.data_inicial)

    def valor_nota(self, force_insert=False, force_update=False):
        return Venda.objects.get(valor_dinheiro=self.valor_dinheiro) + self.valor_cartao 
            

    def get_valor(self):
      inicio = self.data_inicial
      fim = self.data_final
      agencia = self.agencia
      
      valor = Venda.objects.filter(data_venda__range=[inicio, fim]).filter(agencia=agencia).aggregate(valor=Sum(F('valor_dinheiro') + F('valor_cartao'), output_field=FloatField()))
      #return  valor['valor']
      a = '{:,.2f}'.format(float(valor['valor']))
      b = a.replace(',','v')
      c = b.replace('.',',')
      return c.replace('v','.')

    def get_valor_geral(self):
      inicio = self.data_inicial
      fim = self.data_final
      agencia = self.agencia
      
      valor = Venda.objects.filter(data_venda__range=[inicio, fim]).aggregate(valor=Sum(F('valor_dinheiro') + F('valor_cartao'), output_field=FloatField()))
      #return  valor['valor']
      a = '{:,.2f}'.format(float(valor['valor']))
      b = a.replace(',','v')
      c = b.replace('.',',')
      return c.replace('v','.')



    def get_valor_recebimento(self):
      inicio = self.data_inicial
      fim = self.data_final
      usuario = self.usuario
      
      valor = Recebimento.objects.filter(data_recebimento__range=[inicio, fim]).filter(usuario=usuario).aggregate(valor=Sum(F('venda__valor_dinheiro') + F('venda__valor_cartao'), output_field=FloatField()))
      return  valor['valor']

    def get_valor_comissao(self):
      inicio = self.data_inicial
      fim = self.data_final
      usuario = self.usuario
      
      valor = Recebimento.objects.filter(data_recebimento__range=[inicio, fim]).filter(usuario=usuario).aggregate(valor=Sum(F('venda__valor_dinheiro') + F('venda__valor_cartao'), output_field=FloatField()))
      #return float(valor.replace(",",".")) * 3 / 100
      #Decimal(valortotal['valortotal']) - valor_nota()
      return  valor['valor'] * 3 / 100


    def get_total(self):
      inicio = self.data_inicial
      fim = self.data_final
      valor = Venda.objects.filter(data_venda__range=[inicio, fim]).aggregate(valor=Sum(F('valor_nota'), output_field=FloatField()))
      return  valor['valor']

    def clean(self, *args, **kwargs):
        if self.data_inicial > self.data_final:
            raise forms.ValidationError('A Data Inicial não pode ser maior que a Data Final')

    
#class SettingsForm(forms.Form):
#    delivery_time = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))