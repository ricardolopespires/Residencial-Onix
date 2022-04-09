from django.db.models.fields import DecimalField
from condominio.models import Condominios
from accounts.models import Administradores
from django.conf import settings
from phone_field import PhoneField
from django.db import models

# Create your models here.





class Funcionario(models.Model):

    STATUS_FUNCAO = (

        ('sindico','Sindico'),
        ('subsindico','Subsindico'),
        ('zelador','Zelador'),
        ('gerente predial','Gerente predial'),
        ('auxiliar de service gerais','Auxiliar de serviços gerais'),
        ('auxiliar administrativo','Auxiliar administrativo'),
        ('recepcionista','Recepcionista'),
        ('porteiro','Porteiro'),
        ('vigias','Vigias'),

    )

    STATUS_CONDICAO =  (

            ('experiencia','Experiencia'),
            ('trabalhando', 'Trabalhando'),
            ('afastado','Afastado'),
            ('aviso', 'Aviso'),
            ('demitido','Demitido')
    )

    STATUS_GENRE = (

        ('masculino','Masculino'),
        ('feminino', 'Feminino'),
    )

    
    STATUS_CIVIL = (

        ('solteiro','Solteiro'),
        ('solteira','Solteira'),
        ('casado','Casado'), 
        ('casada','Casada'),
        ('viuvo','Viuvo'),
        ('viuva','viuva'),

    )
    sindico = models.ForeignKey(Administradores, related_name = 'funcionarios', on_delete = models.CASCADE)
    emprego = models.ForeignKey(Condominios, related_name = 'condominio_emprego', on_delete = models.CASCADE)
    status = models.CharField(max_length = 150, choices = STATUS_CONDICAO, default = 'experiencia')
    img = models.ImageField(upload_to = 'condominio/funcionario', blank = True)
    nome = models.CharField(max_length = 150, help_text = "Nome do Funcionário do Condominio") 
    sexo = models.CharField(max_length = 150, choices = STATUS_GENRE, default = 'masculino', help_text = "O Genero do Síndico ")
    data_nascimento = models.CharField(max_length = 150, help_text = "Data de Nacimento do Pestador de Serviço", blank=True)
    estado_civil = models.CharField(max_length = 150, choices = STATUS_CIVIL, default = 'solteiro', help_text = 'O Estado Civil do Funcionário' )   
    cpf = models.CharField( max_length = 150, blank = True, help_text = "Documento CPF do do Funcinário ")
    rg = models.CharField('RG', max_length = 150, blank = True, help_text = "Documento RG do Funcionário ")
    endereco = models.CharField(max_length = 150, help_text = "Endereço da residencia do Funcionário") 
    bairro = models.CharField(max_length = 150, help_text = "Bairro onde o Funcionário Reside") 
    cep = models.CharField(max_length = 150, help_text = "CEP do Endereço do Funcionário do Condominio") 
    cidade = models.CharField(max_length = 150, help_text = "cidade onde do Funcionário do Condominio Reside") 
    UF = models.CharField(max_length = 150, help_text = "Cdigo UF da localidade do Funcionário do Condominio") 
    telefone  = PhoneField(blank=True, help_text='Numero do telefone do funcionário')
    celular = PhoneField(blank=True, help_text='Numero do celular do funcionário do condominio')
    email = models.EmailField(help_text = 'Email do funcionário')
    endereço_do_trabalho  = models.CharField(max_length = 150, help_text = "Endereço do local de trabalho")
    telefone_do_servico = PhoneField(blank=True, help_text='Numero do telefone do loca de trabalho')
    funcao = models.CharField(max_length = 150, choices = STATUS_FUNCAO, default = 'zelador', )
    horario_de_trabalho = models.CharField(max_length = 150, help_text = "O horário de trabalho")
    admitido = models.DateTimeField( auto_now_add = False, help_text = 'data da Adimição do funcionario', blank = True )
    demitido = models.DateTimeField( auto_now_add = False, help_text = 'data da demição do funcionario', blank = True, null= True )
    salario_bruto = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Salário Bruto do Funcionário",default = 0, blank = True)
    vale_transporte = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Valor do Vale Transporte",default = 0, blank = True)
    vale_refeicao = models.DecimalField( max_digits = 10, decimal_places = 2, help_text = "Valor do vale Refeição", default = 0, blank = True)        
    ferias = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Valor da Férias", default = 0, blank = True)
    decimo_terceiro_1 = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Quanto o Funcionário ganha por Horas", default = 0, blank = True)
    decimo_terceiro_2 = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Quanto o Funcionário ganha por Horas", default = 0, blank = True)
    salario_liquido = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Salário Líquido do Funcionário", default = 0, blank = True)



    class Meta:

        verbose_name = 'funcionário'
        verbose_name_plural = 'funcionários'

    def __str__(self):
        return self.nome




class Salario (models.Model):

    STATUS_TIPO = (
        
        ('conta corrente','Conta Corrente'),
        ('poupança', 'Poupança')

    )
    sindico = models.ForeignKey(Administradores, related_name = 'salario_funcionario', on_delete = models.CASCADE)
    mes_referente = models.DateTimeField( auto_now_add = False, help_text = 'Mês de referência')
    funcionario = models.ForeignKey(Funcionario, related_name = "funcionario_holerite", on_delete = models.CASCADE, help_text = "Nome do Funcionário")
    banco = models.CharField(max_length = 150, help_text = "Banco do funcionario tem conta", blank = True)
    agencia = models.CharField(max_length = 150,help_text = "Agência da conta funcionário ", blank = True)
    conta = models.CharField(max_length = 150, help_text = "Numero da conta", blank = True)
    tipo = models.CharField(max_length = 150, choices = STATUS_TIPO, default = 'conta corrente', help_text = "A conta é corrente ou poupança")
    salario_bruto = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Salário Bruto do Funcionário",default = 0, blank = True)
    valor_por_horas = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Quanto o Funcionário ganha por Horas", default = 0, blank = True)
    vale_transporte = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Valor do Vale Transporte",default = 0, blank = True)
    vale_refeicao = models.DecimalField( max_digits = 10, decimal_places = 2, help_text = "Valor do vale Refeição", default = 0, blank = True)        
    ferias = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Valor da Férias", default = 0, blank = True)
    decimo_terceiro_1 = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Quanto o Funcionário ganha por Horas", default = 0, blank = True)
    decimo_terceiro_2 = models,DecimalField(max_digits = 10, decimal_places = 2, help_text = "Quanto o Funcionário ganha por Horas", default = 0, blank = True)
    inss = models.DecimalField( max_digits = 10, decimal_places = 2, help_text = "O Valor de o INSS", default = 0, blank = True)   
    fgts = models.DecimalField( max_digits = 10, decimal_places = 2, help_text = "O Valor de Fundo de Garantia por Tempo de Serviço", default = 0, blank = True)
    salario_liquido = models.DecimalField(max_digits = 10, decimal_places = 2, help_text = "Salário Líquido do Funcionário", default = 0, blank = True)


    class Meta:

        verbose_name = 'Salário'
        verbose_name_plural = 'Salários'

    def __str__(self):
        return f'{self.banco}'

    
    
    
class Vale_Transporte(models.Model):
    sindico = models.ForeignKey(Administradores, related_name = 'vale_transporte', on_delete = models.CASCADE)
    funcionario = models.CharField(max_length = 150, help_text = 'Nome do funcionario')
    mes_referente = models.DateTimeField( auto_now_add = False, help_text = 'Mês de referência')
    data_do_pagamento  = models.DateTimeField( auto_now_add = False, help_text = 'Data do pagamento')
    descricao = models.TextField(help_text = "descrição do local do pagamento")
    valor = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor do vale Transporte')
    quantidade = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'quantidade de vales a ser pago')
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor total do vale Transporte a ser pago')

  
    
    
class Vale_Alimentacao(models.Model):
    sindico = models.ForeignKey(Administradores, related_name = 'vale_alimentacao', on_delete = models.CASCADE)
    funcionario = models.CharField(max_length = 150, help_text = 'Nome do funcionario')
    mes_referente = models.DateTimeField( auto_now_add = False, help_text = 'Mês de referência')
    data_do_pagamento  = models.DateTimeField( auto_now_add = False, help_text = 'Data do pagamento')
    descricao = models.TextField(help_text = "descrição do local do pagamento")
    valor = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor do vale alimentação')
    quantidade = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'quantidade de vales a ser pago')
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor total do vale alimentação a ser pago')

    
    
class Ferias(models.Model):
    sindico = models.ForeignKey(Administradores, related_name = 'ferias', on_delete = models.CASCADE)
    funcionario = models.CharField(max_length = 150, help_text = 'Nome do funcionario')
    periodo = models.DateTimeField( auto_now_add = False, help_text = 'Periodo')
    data_do_pagamento  = models.DateTimeField( auto_now_add = False, help_text = 'Data do pagamento')
    descricao = models.TextField(help_text = "descrição do local do pagamento")
    quantidade = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'Valor da férias vencidas' )
    quantidade = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'quantidade de férias vencidas')
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor total do vale Transporte a ser pago')


    
class Decimo_Terceiro(models.Model):
    
    STATUS_CHOICES = (

        ('primeira parcela', 'Primeira Parcela'),
        ('segunda Parcela','Segunda Parcela'),

    )
    sindico = models.ForeignKey(Administradores, related_name = 'decimo_terceiro', on_delete = models.CASCADE)
    funcionario = models.CharField(max_length = 150, help_text = 'Nome do funcionario')
    status = models.CharField(max_length = 150, choices = STATUS_CHOICES, default = 'primeira parcela')
    periodo = models.DateTimeField( auto_now_add = False, help_text = 'Periodo')
    data_do_pagamento  = models.DateTimeField( auto_now_add = False, help_text = 'Data do pagamento')
    descricao = models.TextField(help_text = "descrição do local do pagamento")   
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'valor total da parcela a ser pago')

  

class Avaliacao(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'user_unidade_avaliacao', on_delete=models.CASCADE)
	funcionario = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)	
	rate = models.IntegerField()
	
	
	def __str__(self):
		return self.user.username