from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import Administradores
from condominio.models import Condominios
from moradores.models import Morador
from phone_field import PhoneField
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from django.db import models

# Create your models here.







class Categoria(models.Model):   
    img = models.URLField(help_text = " logo da categoria", blank = True, null=True)
    title =  models.CharField(max_length = 150, help_text = "O titulo da categoria prestação de serviço")
    

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
    
    def __str__(self):
        return self.title



class SubCategoria(models.Model):    
    categorie = models.ForeignKey(Categoria, related_name = 'categoria', on_delete = models.CASCADE)
    title =  models.CharField(max_length = 150, help_text = "O titulo da categoria prestação de serviço")


    class Meta:
        verbose_name = "Sub-Categoria"
        verbose_name_plural = "Sub Categorias"

    def __str__(self):
        return self.title






class Banco(models.Model):   

    id =  models.CharField(max_length = 150,  primary_key = True ,help_text = 'Código do banco', blank = True)   
    ispb = models.IntegerField(help_text = 'ISPB (Identificador do Sistema de Pagamento Brasileiro)' ,blank = True)
    img = models.URLField(help_text = "Logo do banco", blank = True)
    nome = models.CharField(max_length = 150, help_text = "Nome do Banco onde está a conta", blank = True)   
    agencia = models.CharField(max_length = 150, help_text = "O numero da agência onde está a conta", blank = True)    
    endereco = models.CharField(max_length = 150, help_text = "Endereço onde está localizada a Agência", blank = True)
    telefone =  PhoneField(max_length = 150, help_text = "Numero do Telefone do Síndico ", blank=True)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = 'Bancos'

    def __str__(self):
        return self.nome

        


class Conta(models.Model):
    
    STATUS_TIPO = (
        
        ('conta corrente','Conta Corrente'),
        ('poupança', 'Poupança')

    )

    STATUS_ESTILO = (

        ('pessoa jurídica','Pessoa Jurídica'),
        ('pessoa fisíca', 'Pessoa Fisíca')
    )

    id = models.CharField(primary_key = True ,max_length = 150, help_text = "O numero da conta",) 
    sindico = models.ForeignKey(Administradores, related_name = 'sindico_conta', on_delete = models.CASCADE)
    titular_da_conta = models.ForeignKey(Condominios, related_name = 'conta_condominios', on_delete = models.CASCADE)  
    agencia = models.ForeignKey(Banco, related_name = "banco_agencia", on_delete = models.CASCADE  )
    tipo = models.CharField(max_length = 150, choices = STATUS_TIPO, default = 'conta corrente', help_text = "A conta é corrente ou poupança")
    estilo = models.CharField(max_length = 150, choices = STATUS_ESTILO, default = 'pessoa jurídica', help_text = "A conta é de pessoa juridica ou")   
    criada = models.DateTimeField(auto_now_add = False, help_text = "Data em que foi aberta a conta", blank = True)
    fechada = models.DateTimeField( auto_now_add = False, help_text = "Data do fechamento da conta", blank = True, null = True)
    creditos = models.DecimalField(decimal_places = 2, max_digits =10, help_text = "O valores creditados na conta",default = 0, blank = True, null = True)
    debitos =  models.DecimalField(decimal_places = 2, max_digits =10, help_text = "O valores debitados da conta", default = 0 , blank = True, null = True )  
    saldo = models.DecimalField(decimal_places = 2, max_digits =10, help_text = "O valor do saldo da conta", blank = True,  default = 0 ,)

    
    def __str__(self):
        return self.tipo


class Saldo_Anterior(models.Model):
    conta = models.ForeignKey(Conta,  related_name = 'saldo_mes_anterior', on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add = False, help_text = "A data de movimento")  
    valor = models.DecimalField(decimal_places = 2, max_digits =10, help_text = "O valor do saldo da conta do mês passado", blank = True,  default = 0 ,)



class Movimentacao(models.Model):
    
    
    STATUS_TIPO =(
 
        ('-','-'),
        ('D','Debito'),
        ('C','Cretido')
    )
    sindico = models.ForeignKey(Administradores, related_name = 'sindico_movimentação', on_delete = models.CASCADE)
    conta = models.ForeignKey(Conta,  related_name = 'conta_movimentação', on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add = False, help_text = "A data de movimento")
    descricao = models.TextField(help_text = "Descrição do movimento")
    tipo = models.CharField(max_length = 150, choices = STATUS_TIPO, default = '-', help_text = "O tipo do movimento bancario")
    valor = models.DecimalField(max_digits = 10, decimal_places = 2 ,help_text = "O valor do movimento")
    saldo = models.DecimalField(max_digits = 10, decimal_places = 2,  help_text = "O valor que ficou de saldo na conta")


    def __str__(self):
        return f"{self.conta}"



#------------------------------------- CONTAS -----------------------------------------

class Despesas(models.Model):

    TIPO_PRESTADOR = (

        ('pessoa juridica','Pessoa Juridica'),
        ('pessoa fisica', 'Pessoas Fisica'),
    )


    STATUS_MODEL = ( 
        
        ('aberta','Aberta'),
        ('paga', 'Paga'),
        ('atrasada','Atrasada')
        
        
        )


    STATUS_DESPESAS = (

        ('funcionario','Funcionario'),
        ('manutencao','Manutencao'),
        ('consumo','Consumo'),
        ('outros','Outros'),

    )




    id = models.CharField(primary_key = True, max_length = 150, help_text = "Numero da nota ou RG se for pessoa fisica", )
    sindico = models.ForeignKey(Administradores, related_name = 'sindico_despesa', on_delete = models.CASCADE)
    categoria = models.ForeignKey(Categoria, related_name = "despesa_categoria", on_delete = models.CASCADE, help_text = "Categoria da Prestação de Serviços")
    servico = models.ForeignKey(SubCategoria, related_name = 'despesa_subcategoria', on_delete= models.CASCADE, help_text = "Serviço Prestado" )
    beneficiario = models.CharField(max_length = 150, help_text="O Nome do Benefiçiario ")
    tipo = models.CharField(max_length = 150 , choices = TIPO_PRESTADOR, default = 'pessoa juridica', help_text = 'Forma de regime do prestador do serviço')
    status = models.CharField(max_length = 150 , choices = STATUS_MODEL, default = 'aberta', help_text="O status da conta")   
    despesas = models.CharField( max_length = 150, choices = STATUS_DESPESAS, default = 'consumo', help_text = "Tipo de despesa mensal")
    descricao = models.TextField(help_text = 'Descrição do documento')
    lancamento = models.DateTimeField(auto_now_add = True, help_text = "Data do Vencimento do documento")
    vencimento = models.DateTimeField(auto_now_add = False, help_text = "Data do Vencimento do documento", blank = True)
    pagamento = models.DateTimeField(auto_now_add =False,help_text = "Data que foi Pago o Documento")
    valor = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "valor total do documento")
    desconto = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Valor do Desconto")
    multa = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Valor da Multa")
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'O valor Total do documento')


    class Meta:
        verbose_name = "Despesa"
        verbose_name_plural = "Despesas"


    def __str__(self):
        return self.id



class Prazo(models.Model):


    STATUS_TAREFA = (

        ('aberta', "aberta"),
        ('em dia', "em dia"),
        ('atrasada', "atrasada"),
        ('paga', "PAGA")
    )
    id = models.CharField(primary_key = True, max_length = 150, help_text = "Indentificador da despesas" )
    title = models.CharField(max_length=200)
    descricao = models.CharField(max_length=100)
    status = models.CharField(max_length = 19, default = 0, choices = STATUS_TAREFA)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    complete_per = models.IntegerField( validators = [MinValueValidator(0), MaxValueValidator(100)])
    due = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)


    def __str__(self):
        return self.title
        


class Inadimplência(models.Model):
    
    CHOICES_STATUS = (

        ('atrasado', "Atrasado"),        
        ('inadinplente','Inadinplente'),
        ('acordo','Acordo'),
        ('quitado', 'Quitado'),
    )

    id = models.CharField(max_length = 40, primary_key = True, blank = True)
    unidade = models.CharField(max_length = 40, help_text = 'Numero da unidade ')  
    acordo = models.BooleanField(help_text = 'Fazendo acordo para pagamento de parcela atrasadas') 
    status = models.CharField( max_length = 150, choices = CHOICES_STATUS, default = 'inadinplente') 
    morador  = models.ForeignKey(Morador, related_name ='morador_inadimplente', on_delete = models.CASCADE)
    vencimento = models.DateTimeField(auto_now_add = False, help_text = 'O mês do vencimento do boleto' )
    referente = models.DateTimeField(auto_now_add = False, help_text = 'O mês de referência' )
    dias = models.IntegerField(help_text = "quantidade de dia que estão em atraso")
    boleto = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "O valor da condominial do mês equivalente")
    juros = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Juros do valor da condominial do mês equivalente")
    multa = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "multa do valor da condominial do mês equivalente")
    atualizacao =  models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "atualização ")
    honorarios =  models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Honorários da Administradora ")  
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'O valor total do debito da inadinplência')

    def __str__(self):
        return f'{self.unidade}'




class Acordo(models.Model):
    
    CHOICES_STATUS = (

        ('atrasado', "Atrasado"),        
        ('inadinplente','Inadinplente'),        
        ('quitado', 'Quitado'),
    )

    id = models.CharField(max_length = 40, primary_key = True, blank = True)
    unidade = models.CharField(max_length = 40, help_text = 'Numero da unidade ')  
    acordo = models.BooleanField(help_text = 'Fazendo acordo para pagamento de parcela atrasadas') 
    status = models.CharField( max_length = 150, choices = CHOICES_STATUS, default = 'inadinplente') 
    morador  = models.ForeignKey(Morador, related_name ='morador_acordo', on_delete = models.CASCADE)
    vencimento = models.DateTimeField(auto_now_add = False, help_text = 'O mês do vencimento do boleto' )
    referente = models.DateTimeField(auto_now_add = False, help_text = 'O mês de referência' )
    dias = models.IntegerField(help_text = "quantidade de dia que estão em atraso")
    boleto = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "O valor da condominial do mês equivalente")
    juros = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Juros do valor da condominial do mês equivalente")
    multa = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "multa do valor da condominial do mês equivalente")
    atualizacao =  models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "atualização ")
    honorarios =  models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Honorários da Administradora")  
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'O valor total do debito da inadinplência')

    def __str__(self):
        return f'{self.unidade}'




class Pagamento(models.Model):
    id = models.CharField(max_length = 40, primary_key = True, blank = True)
    unidade = models.CharField( max_length = 150, help_text = 'numero de unidade' )
    morador  = models.ForeignKey(Morador, related_name ='pagamento_morador', on_delete = models.CASCADE)
    data_vencimento = models.DateTimeField(auto_now_add = False, help_text = 'Data do vencimento do boleto' )
    data_pagamento = models.DateTimeField(auto_now_add = False, help_text = 'Data de Pagamento' )
    juros = models.DecimalField(decimal_places = 2, max_digits = 10, default = 0, help_text = 'O valor do juros')
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'O valor total do Pagamento')

    def __str__(self):
        return f'{self.morador}'
        