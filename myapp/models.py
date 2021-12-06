from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
import datetime
from .soft_delete import *

# Create your models here.
class Representada(SoftDeletionModel):
    nome = models.CharField(max_length=255, null=True, blank=True,
                            help_text="Nome da representada")
    contato = models.CharField(max_length=255, null=True, blank=True)    
    cnpj = models.CharField(max_length=255, null=True, blank=True)
    inscEstadual = models.CharField(max_length=255, null=True, blank=True)
    inscMunicipal = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    linha = models.CharField(max_length=255, null=True, blank=True)
    comissao = models.CharField(max_length=255, null=True, blank=True)
    ipi = models.CharField(max_length=255, null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('representada-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.nome, self.contato)

    def get_text(self):
        return 'Contato: {0}, CNPJ: {1}, Cidade: {2} '.format(self.contato, self.cnpj, self.cidade)

    def get_edit_url(self):
        return reverse('representada-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('representada-delete', args=[str(self.id)])


# Create your models here.
class Produto(SoftDeletionModel):
    nome = models.CharField(max_length=255, null=True, blank=True,
                            help_text="Nome do produto")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    referencia = models.CharField(max_length=255, null=True, blank=True)
    # codRepresentada = models.CharField(max_length=255, null=True, blank=True) #TODO
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
        return 'Valor: {0} \n Referencia: {1} \n Representada: {2} '.format(self.valor, self.referencia, self.representada)

    def get_edit_url(self):
        return reverse('produto-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('produto-delete', args=[str(self.id)])

# Create your models here.
class Pedido(SoftDeletionModel):
    data = models.DateField()
    ordemCompra = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    # codCliente = models.CharField(max_length=255, null=True, blank=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    # codRepresentada = models.CharField(max_length=255, null=True, blank=True)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    # codVendedor = models.CharField(max_length=255, null=True, blank=True)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.SET_NULL, null=True)
    # codTransportadora = models.CharField(max_length=255, null=True, blank=True)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    tipoFrete = models.CharField(max_length=255, null=True, blank=True)
    formaPagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True)
    tipoCobranca = models.CharField(max_length=255, null=True, blank=True)

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
        return self.ordemCompra

    def get_text(self):
        return 'Ordem Compra: {0} \n  '.format(self.ordemCompra)

    def get_edit_url(self):
        return reverse('pedido-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('pedido-delete', args=[str(self.id)])

class ItemPedido(SoftDeletionModel):
    pedido = models.ForeignKey('Pedido', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200, null=True, blank=True)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True, blank=True)
    tecido = models.ForeignKey('Tecido', on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField(default=1)
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorParcial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_valorParcial(self):
        return self.produto.valor * self.quantidade

    def __str__(self):
        return self.produto.nome +" "+ self.pedido.ordemCompra +" "+self.produto.referencia

# Create your models here.
class Cliente(SoftDeletionModel):
    razaoSocial = models.CharField(max_length=500, null=True, blank=True)
    nomeFantasia = models.CharField(max_length=500, null=True, blank=True)
    diretor = models.CharField(max_length=500, null=True, blank=True)
    comprador = models.CharField(max_length=500, null=True, blank=True)
    financeiro = models.CharField(max_length=500, null=True, blank=True)
    regApuracao = models.CharField(max_length=500, null=True, help_text="Regime de apuração", blank=True)
    telefone = models.CharField(max_length=500, null=True, blank=True)
    celular = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    observacoes = models.CharField(max_length=500, null=True, blank=True)

    # Dados de Faturamento
    fat_inscEstadual = models.CharField(max_length=500, null=True, blank=True)
    fat_estado = models.CharField(max_length=500, null=True, blank=True)
    fat_cidade = models.CharField(max_length=500, null=True, blank=True)
    fat_cep = models.CharField(max_length=500, null=True, blank=True)
    fat_endereco = models.CharField(max_length=500, null=True, blank=True)
    fat_bairro = models.CharField(max_length=500, null=True, blank=True)
    fat_cnpj = models.CharField(max_length=500, null=True, blank=True)

    # Dados de Cobrança
    cob_inscEstadual = models.CharField(max_length=500, null=True, blank=True)
    cob_estado = models.CharField(max_length=500, null=True, blank=True)
    cob_cidade = models.CharField(max_length=500, null=True, blank=True)
    cob_cep = models.CharField(max_length=500, null=True, blank=True)
    cob_endereco = models.CharField(max_length=500, null=True, blank=True)
    cob_bairro = models.CharField(max_length=500, null=True, blank=True)
    cob_cnpj = models.CharField(max_length=500, null=True, blank=True)

    # Dados de Entrega
    entr_inscEstadual = models.CharField(max_length=500, null=True, blank=True)
    entr_estado = models.CharField(max_length=500, null=True, blank=True)
    entr_cidade = models.CharField(max_length=500, null=True, blank=True)
    entr_cep = models.CharField(max_length=500, null=True, blank=True)
    entr_endereco = models.CharField(max_length=500, null=True, blank=True)
    entr_bairro = models.CharField(max_length=500, null=True, blank=True)
    entr_cnpj = models.CharField(max_length=500, null=True, blank=True)


    lastUpdate = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['razaoSocial']

    def get_absolute_url(self):
        return reverse('cliente-detail', args=[str(self.id)])

    def __str__(self):
        return self.razaoSocial

    def get_text(self):
        return 'Nome Fantasia: {0} \n  '.format(self.nomeFantasia)

    def get_edit_url(self):
        return reverse('cliente-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('cliente-delete', args=[str(self.id)])

# Create your models here.
class Transportadora(SoftDeletionModel):
    nome = models.CharField(max_length=255, null=True, blank=True, help_text="Nome da Transportadora")
    contato = models.CharField(max_length=255, null=True, blank=True)    
    cnpj = models.CharField(max_length=255, null=True, blank=True)
    inscEstadual = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    observacoes = models.CharField(max_length=255, null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('transportadora-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.nome, self.contato)

    def get_text(self):
        return 'Contato: {0}, CNPJ: {1}, Cidade: {2} '.format(self.contato, self.cnpj, self.cidade)

    def get_edit_url(self):
        return reverse('transportadora-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('transportadora-delete', args=[str(self.id)])


# Create your models here.
class Vendedor(SoftDeletionModel):
    nome = models.CharField(max_length=255, null=True, blank=True, help_text="Nome do Vendedor")
    cpf = models.CharField(max_length=255, null=True, blank=True)
    estado = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=255, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=255, null=True, blank=True)
    celular = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']

    def get_absolute_url(self):
        return reverse('vendedor-detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1}'.format(self.nome, self.email)

    def get_text(self):
        return 'CPF: {0}, Telefone: {1}, Celular: {2} '.format(self.cpf, self.telefone, self.celular)

    def get_edit_url(self):
        return reverse('vendedor-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('vendedor-delete', args=[str(self.id)])


# Create your models here.
class Assistencia(SoftDeletionModel):
    data = models.DateField()
    numeroSolicitacao = models.CharField(max_length=255, null=True, blank=True)
    # codCliente = models.CharField(max_length=255, null=True, blank=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    # codRepresentada = models.CharField(max_length=255, null=True, blank=True)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    # codTransportadora = models.CharField(max_length=255, null=True, blank=True)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    observacoes = models.TextField(max_length=600, blank=True)
    #Itens da Assistencia
    # itemAssistencia = models.ManyToManyField('ItemAssistencia')
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('assistencia-detail', args=[str(self.id)])

    def __str__(self):
        return self.numeroSolicitacao

    def get_text(self):
        return 'Num. Solicitacao: {0} \n  '.format(self.numeroSolicitacao)

    def get_edit_url(self):
        return reverse('assistencia-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('assistencia-delete', args=[str(self.id)])

# Create your models here.
class ItemAssistencia(SoftDeletionModel):
    

    #Itens da Assistencia
    assistencia = models.ForeignKey('Assistencia', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200, null=True, blank=True)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True)
    tecido = models.ForeignKey('Tecido', on_delete=models.SET_NULL, null=True, blank=True)
    quantidade = models.IntegerField()
    observacoes = models.TextField(max_length=255, null=True, blank=True)
    mostruario = models.BooleanField()
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('produto-detail', args=[str(self.id)])

    def __str__(self):
        
        if self.assistencia is not None and self.produto is not None:
            return self.referencia+ ' '+self.produto.nome + ' ' + self.assistencia.numeroSolicitacao
        return self.referencia

# Create your models here.
class Acabamento(SoftDeletionModel):
    acabamento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de acabamento")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['acabamento']

    def get_absolute_url(self):
        return reverse('acabamento-detail', args=[str(self.id)])

    def __str__(self):
        return self.acabamento

    def get_text(self):
        return ''

    def get_edit_url(self):
        return reverse('acabamento-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('acabamento-delete', args=[str(self.id)])

# Create your models here.
class Tecido(SoftDeletionModel):
    tecido = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de Tecido")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['tecido']

    def get_absolute_url(self):
        return reverse('tecido-detail', args=[str(self.id)])

    def __str__(self):
        return self.tecido

    def get_text(self):
        return ''

    def get_edit_url(self):
        return reverse('tecido-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('tecido-delete', args=[str(self.id)])

# Create your models here.
class FormaPagamento(SoftDeletionModel):
    formaDePagamento = models.CharField(max_length=255, null=True, blank=True, help_text="Tipo de Forma de Pagamento")
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['formaDePagamento']

    def get_absolute_url(self):
        return reverse('formaPagamento-detail', args=[str(self.id)])

    def __str__(self):
        return self.formaDePagamento

    def get_text(self):
        return ''

    def get_edit_url(self):
        return reverse('formaPagamento-update', args=[str(self.id)])

    def get_delete_url(self):
        return reverse('formaPagamento-delete', args=[str(self.id)])

        