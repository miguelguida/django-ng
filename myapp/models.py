from django.db import models
from django.urls import reverse  # To generate URLS by reversing URL patterns
import uuid  # Required for unique book instances
from datetime import date
import datetime

# Create your models here.
class Representada(models.Model):
    nome = models.CharField(max_length=200,
                            help_text="Nome da representada")
    contato = models.CharField(max_length=200)    
    cnpj = models.CharField(max_length=200)
    inscEstadual = models.CharField(max_length=200)
    inscMunicipal = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    celular = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    linha = models.CharField(max_length=200)
    comissao = models.CharField(max_length=200)
    ipi = models.CharField(max_length=200)
    lastUpdate = models.DateTimeField(auto_now=True)

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
class Produto(models.Model):
    nome = models.CharField(max_length=200,
                            help_text="Nome do produto")
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    referencia = models.CharField(max_length=200)
    codRepresentada = models.CharField(max_length=200) #TODO
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    observacoes = models.TextField(max_length=600)
    lastUpdate = models.DateTimeField(auto_now=True)

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
class Pedido(models.Model):
    data = models.DateField()
    ordemCompra = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    codCliente = models.CharField(max_length=200)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    codRepresentada = models.CharField(max_length=200)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    codVendedor = models.CharField(max_length=200)
    vendedor = models.ForeignKey('Vendedor', on_delete=models.SET_NULL, null=True)
    codTransportadora = models.CharField(max_length=200)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    tipoFrete = models.CharField(max_length=200)
    formaPagamento = models.ForeignKey('FormaPagamento', on_delete=models.SET_NULL, null=True)
    tipoCobranca = models.CharField(max_length=200)

    lastUpdate = models.DateTimeField(auto_now=True)

    #Itens do Pedido
    
    
    #Valor do Pedido
    valorBruto = models.DecimalField(max_digits=10, decimal_places=2)
    desconto1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto3 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto4 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto5 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ipi = models.DecimalField(max_digits=10, decimal_places=2)
    valorIpi = models.DecimalField(max_digits=10, decimal_places=2)
    valorTotal = models.DecimalField(max_digits=10, decimal_places=2)
    porcentagemComissao = models.DecimalField(max_digits=10, decimal_places=2)
    valorComissao = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(max_length=600, default='')


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

class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField()
    valorUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    valorParcial = models.DecimalField(max_digits=10, decimal_places=2)
    lastUpdate = models.DateTimeField(auto_now=True)

# Create your models here.
class Cliente(models.Model):
    razaoSocial = models.CharField(max_length=200)
    nomeFantasia = models.CharField(max_length=200)
    diretor = models.CharField(max_length=200)
    comprador = models.CharField(max_length=200)
    financeiro = models.CharField(max_length=200)
    regApuracao = models.CharField(max_length=200, help_text="Regime de apuração")
    telefone = models.CharField(max_length=200)
    celular = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    observacoes = models.CharField(max_length=200)

    # Dados de Faturamento
    fat_inscEstadual = models.CharField(max_length=200)
    fat_estado = models.CharField(max_length=200)
    fat_cidade = models.CharField(max_length=200)
    fat_cep = models.CharField(max_length=200)
    fat_endereco = models.CharField(max_length=200)
    fat_bairro = models.CharField(max_length=200)
    fat_cnpj = models.CharField(max_length=200)

    # Dados de Cobrança
    cob_inscEstadual = models.CharField(max_length=200)
    cob_estado = models.CharField(max_length=200)
    cob_cidade = models.CharField(max_length=200)
    cob_cep = models.CharField(max_length=200)
    cob_endereco = models.CharField(max_length=200)
    cob_bairro = models.CharField(max_length=200)
    cob_cnpj = models.CharField(max_length=200)

    # Dados de Entrega
    entr_inscEstadual = models.CharField(max_length=200)
    entr_estado = models.CharField(max_length=200)
    entr_cidade = models.CharField(max_length=200)
    entr_cep = models.CharField(max_length=200)
    entr_endereco = models.CharField(max_length=200)
    entr_bairro = models.CharField(max_length=200)
    entr_cnpj = models.CharField(max_length=200)


    lastUpdate = models.DateTimeField(auto_now=True)

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
class Transportadora(models.Model):
    nome = models.CharField(max_length=200, help_text="Nome da Transportadora")
    contato = models.CharField(max_length=200)    
    cnpj = models.CharField(max_length=200)
    inscEstadual = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    celular = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    observacoes = models.CharField(max_length=200)
    lastUpdate = models.DateTimeField(auto_now=True)

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
class Vendedor(models.Model):
    nome = models.CharField(max_length=200, help_text="Nome do Vendedor")
    cpf = models.CharField(max_length=200)
    estado = models.CharField(max_length=200)
    cidade = models.CharField(max_length=200)
    cep = models.CharField(max_length=200)
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    telefone = models.CharField(max_length=200)
    celular = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    lastUpdate = models.DateTimeField(auto_now=True)

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
class Assistencia(models.Model):
    data = models.DateField()
    numeroSolicitacao = models.CharField(max_length=200)
    codCliente = models.CharField(max_length=200)
    cliente = models.ForeignKey('Cliente', on_delete=models.SET_NULL, null=True)
    codRepresentada = models.CharField(max_length=200)
    representada = models.ForeignKey('Representada', on_delete=models.SET_NULL, null=True)
    codTransportadora = models.CharField(max_length=200)
    transportadora = models.ForeignKey('Transportadora', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200)
    observacoes = models.TextField(max_length=600)
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
class ItemAssistencia(models.Model):
    

    #Itens da Assistencia
    assistencia = models.ForeignKey('Assistencia', on_delete=models.SET_NULL, null=True)
    produto = models.ForeignKey('Produto', on_delete=models.SET_NULL, null=True)
    referencia = models.CharField(max_length=200)
    acabamento = models.ForeignKey('Acabamento', on_delete=models.SET_NULL, null=True)
    quantidade = models.IntegerField()
    observacoes = models.CharField(max_length=200)
    mostruario = models.BooleanField()
    lastUpdate = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('produto-detail', args=[str(self.id)])

    def __str__(self):
        
        if self.assistencia is not None and self.produto is not None:
            return self.referencia+ ' '+self.produto.nome + ' ' + self.assistencia.numeroSolicitacao
        return self.referencia

# Create your models here.
class Acabamento(models.Model):
    acabamento = models.CharField(max_length=200, help_text="Tipo de acabamento")
    lastUpdate = models.DateTimeField(auto_now=True)

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
class Tecido(models.Model):
    tecido = models.CharField(max_length=200, help_text="Tipo de Tecido")
    lastUpdate = models.DateTimeField(auto_now=True)

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
class FormaPagamento(models.Model):
    formaDePagamento = models.CharField(max_length=200, help_text="Tipo de Forma de Pagamento")
    lastUpdate = models.DateTimeField(auto_now=True)

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

        