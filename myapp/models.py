from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
import datetime
from .soft_delete import *
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    avatar = models.ImageField() # or whatever

    def __str__(self):
        return self.user.email

class Representada(SoftDeletionModel):
    nome = models.CharField(max_length=255,
                            help_text="Nome da representada")
    contato = models.CharField(max_length=255, blank=True)    
    cnpj = models.CharField(max_length=255)
    inscEstadual = models.CharField(max_length=255)
    inscMunicipal = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    celular = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    linha = models.CharField(max_length=255, blank=True)
    comissao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ipi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('representada-detail', args=[str(self.id)])

    def __str__(self):
        return self.nome

    def get_text(self):
        fields_dict = [ ('Nome: ', self.nome),
                        ('Contato: ',self.contato),
                        ('CNPJ: ', self.cnpj),
                        ('Cidade: ', self.cidade)]
        return fields_dict

    def get_edit_url(self):
        return reverse('representada-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('representada-delete', args=[str(self.id)])



class Produto(SoftDeletionModel):
    nome = models.CharField(max_length=255,
                            help_text="Nome do produto")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    referencia = models.CharField(max_length=255)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    observacoes = models.TextField(max_length=600, blank=True, null=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('produto-detail', args=[str(self.id)])

    def __str__(self):
        return self.nome

    def get_text(self):
        fields_dict = [ ('Código: ', self.id),
                        ('Nome: ', self.nome),
                        ('Referência: ',self.referencia),
                        ('Valor: ', self.valor),
                        ('Representada: ', self.representada)]
        return fields_dict

    def get_edit_url(self):
        return reverse('produto-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('produto-delete', args=[str(self.id)])


class Status(SoftDeletionModel):
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.status


class TipoFrete(SoftDeletionModel):
    tipoFrete = models.CharField(max_length=255)

    def __str__(self):
        return self.tipoFrete

class TipoCobranca(SoftDeletionModel):
    tipoCobranca = models.CharField(max_length=255)

    def __str__(self):
        return self.tipoCobranca


class Pedido(SoftDeletionModel):
    data = models.DateField()
    ordemCompra = models.CharField(max_length=255)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, default=1)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.SET_NULL, null=True)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    tipoFrete = models.ForeignKey('TipoFrete', on_delete=models.SET_NULL, null=True)
    formaPagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True)
    tipoCobranca = models.ForeignKey('TipoCobranca', on_delete=models.SET_NULL, null=True)

    lastUpdate = models.DateTimeField(auto_now=True)

    #Itens do Pedido
    
    
    #Valor do Pedido
    valorBruto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto4 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto5 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ipi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valorIpi = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    porcentagemComissao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valorComissao = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(max_length=600, blank=True)


    def get_absolute_url(self):
        return reverse('pedido-detail', args=[str(self.id)])

    def __str__(self):        
        if self.id:
            return str(self.id)
        return self.ordemCompra

    def get_text(self):
        fields_dict = [ ('N° Pedido: ',self.id),
                        ('Cliente: ', self.cliente),
                        ('Representada: ', self.representada)]
        return fields_dict

    def get_edit_url(self):
        return reverse('pedido-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('pedido-delete', args=[str(self.id)])

    def get_valor_descontos_aplicado(self):
        valor_bruto = self.valorBruto
        if self.desconto1 > 0:
            valor_bruto =  valor_bruto * ((100 - self.desconto1)/100)
        if self.desconto2 > 0:
            valor_bruto =  valor_bruto * ((100 - self.desconto2)/100)
        if self.desconto3 > 0:
            valor_bruto =  valor_bruto * ((100 - self.desconto3)/100)
        if self.desconto4 > 0:
            valor_bruto =  valor_bruto * ((100 - self.desconto4)/100)
        if self.desconto5 > 0:
            valor_bruto =  valor_bruto * ((100 - self.desconto5)/100)

        return round(valor_bruto, 2)

class ItemPedido(SoftDeletionModel):
    pedido = models.ForeignKey('Pedido', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True)
    tecido = models.ForeignKey('Tecido', on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(default=0)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    valorParcial = models.DecimalField(max_digits=10, decimal_places=2)
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_valorParcial(self):
        return self.produto.valor * self.quantidade

    def __str__(self):
        if self.produto and self.pedido:
            return self.produto.nome +" "+ self.pedido.ordemCompra +" "+self.produto.referencia
        return self.referencia


class Cliente(SoftDeletionModel):
    razaoSocial = models.CharField(max_length=500)
    nomeFantasia = models.CharField(max_length=500)
    diretor = models.CharField(max_length=500)
    comprador = models.CharField(max_length=500)
    financeiro = models.CharField(max_length=500, blank=True)
    regApuracao = models.CharField(max_length=500, null=True, help_text="Regime de apuração", blank=True)
    telefone = models.CharField(max_length=500)
    celular = models.CharField(max_length=500, blank=True)
    email = models.EmailField(max_length=500)
    observacoes = models.CharField(max_length=500, blank=True)

    # Dados de Faturamento
    fat_inscEstadual = models.CharField(max_length=500, blank=True)
    fat_estado = models.CharField(max_length=500, blank=True)
    fat_cidade = models.CharField(max_length=500, blank=True)
    fat_cep = models.CharField(max_length=500, blank=True)
    fat_endereco = models.CharField(max_length=500, blank=True)
    fat_bairro = models.CharField(max_length=500, blank=True)
    fat_cnpj = models.CharField(max_length=500, blank=True)

    # Dados de Cobrança
    cob_inscEstadual = models.CharField(max_length=500, blank=True)
    cob_estado = models.CharField(max_length=500, blank=True)
    cob_cidade = models.CharField(max_length=500, blank=True)
    cob_cep = models.CharField(max_length=500, blank=True)
    cob_endereco = models.CharField(max_length=500, blank=True)
    cob_bairro = models.CharField(max_length=500, blank=True)
    cob_cnpj = models.CharField(max_length=500, blank=True)

    # Dados de Entrega
    entr_inscEstadual = models.CharField(max_length=500, blank=True)
    entr_estado = models.CharField(max_length=500, blank=True)
    entr_cidade = models.CharField(max_length=500, blank=True)
    entr_cep = models.CharField(max_length=500, blank=True)
    entr_endereco = models.CharField(max_length=500, blank=True)
    entr_bairro = models.CharField(max_length=500, blank=True)
    entr_cnpj = models.CharField(max_length=500, blank=True)


    lastUpdate = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['razaoSocial']

    def get_absolute_url(self):
        return reverse('cliente-detail', args=[str(self.id)])

    def __str__(self):
        return self.razaoSocial

    def get_text(self):
        fields_dict = [ ('Nome: ', self.razaoSocial),
                        ('Telefone: ',self.telefone),
                        ('Email: ', self.email)]
        return fields_dict

    def get_edit_url(self):
        return reverse('cliente-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('cliente-delete', args=[str(self.id)])


class Transportadora(SoftDeletionModel):
    nome = models.CharField(max_length=255, help_text="Nome da Transportadora")
    contato = models.CharField(max_length=255, blank=True)    
    cnpj = models.CharField(max_length=255)
    inscEstadual = models.CharField(max_length=255, blank=True)
    estado = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    celular = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255)
    observacoes = models.CharField(max_length=255, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('transportadora-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.nome, self.contato)

    def get_text(self):
        fields_dict = [ ('Nome: ', self.nome),
                        ('Contato: ',self.contato),
                        ('CNPJ: ', self.cnpj),
                        ('Cidade: ', self.cidade)]
        return fields_dict

    def get_edit_url(self):
        return reverse('transportadora-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('transportadora-delete', args=[str(self.id)])



class Vendedor(SoftDeletionModel):
    nome = models.CharField(max_length=255, help_text="Nome do Vendedor")
    cpf = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    cep = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    telefone = models.CharField(max_length=255)
    celular = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('vendedor-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.nome, self.email)

    def get_text(self):
        fields_dict = [ ('Nome: ', self.nome),
                        ('CPF: ',self.cpf)]
        return fields_dict

    def get_edit_url(self):
        return reverse('vendedor-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('vendedor-delete', args=[str(self.id)])



class Assistencia(SoftDeletionModel):
    data = models.DateField()
    numeroSolicitacao = models.CharField(max_length=255)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, default=1)
    observacoes = models.TextField(max_length=600, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('assistencia-detail', args=[str(self.id)])

    def __str__(self):
        return self.numeroSolicitacao

    def get_text(self):
        fields_dict = [ ('N° Assist.: ',self.id),
                        ('Data: ', self.data),
                        ('Status: ', self.status),
                        ('N° Solicit.: ',self.numeroSolicitacao),
                        ('Cliente: ', self.cliente),
                        ('Representada: ', self.representada)
                        ]
        return fields_dict

    def get_edit_url(self):
        return reverse('assistencia-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('assistencia-delete', args=[str(self.id)])

class ItemAssistencia(SoftDeletionModel):
    assistencia = models.ForeignKey('Assistencia', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True)
    tecido = models.ForeignKey('Tecido', on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField(default=0)
    observacoes = models.TextField(max_length=255, blank=True)
    mostruario = models.BooleanField()
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('produto-detail', args=[str(self.id)])

    def __str__(self):
        
        if self.assistencia is not None and self.produto is not None:
            return self.referencia+ ' '+self.produto.nome + ' ' + self.assistencia.numeroSolicitacao
        return self.referencia


class Acabamento(SoftDeletionModel):
    acabamento = models.CharField(max_length=255, help_text="Tipo de acabamento")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['acabamento']

    def get_absolute_url(self):
        return reverse('acabamento-detail', args=[str(self.id)])

    def __str__(self):
        return self.acabamento

    def get_text(self):
        fields_dict = [ ('', self.acabamento)]
        return fields_dict

    def get_edit_url(self):
        return reverse('acabamento-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('acabamento-delete', args=[str(self.id)])


class Tecido(SoftDeletionModel):
    tecido = models.CharField(max_length=255, help_text="Tipo de Tecido")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tecido']

    def get_absolute_url(self):
        return reverse('tecido-detail', args=[str(self.id)])

    def __str__(self):
        return self.tecido

    def get_text(self):
        fields_dict = [ ('', self.tecido)]
        return fields_dict

    def get_edit_url(self):
        return reverse('tecido-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('tecido-delete', args=[str(self.id)])


class FormaPagamento(SoftDeletionModel):
    formaDePagamento = models.CharField(max_length=255, help_text="Tipo de Forma de Pagamento")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['formaDePagamento']

    def get_absolute_url(self):
        return reverse('formaPagamento-detail', args=[str(self.id)])

    def __str__(self):
        return self.formaDePagamento

    def get_text(self):
        fields_dict = [ ('', self.formaDePagamento)]
        return fields_dict

    def get_edit_url(self):
        return reverse('formaPagamento-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('formaPagamento-delete', args=[str(self.id)])

        