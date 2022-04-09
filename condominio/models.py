from administration.models import Regimento_Interno
from moradores.models import Morador
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Value
from django.db.models.fields import CharField, DateTimeField, DecimalField
from django.db.models.fields.related import ForeignKey
from accounts.models import Administradores
from phone_field import PhoneField
from django.conf import settings
from django.core import validators
from django.utils import timezone 


# Create your models here.


class Condominios(models.Model):

    
    STATUS_CHOICES = (
                        ('Positivo','Positivo'),
                        ('negativo','Negativo'),
                        ('inadimplente','Inadimplente'),
                     )
    administradores = models.ForeignKey(Administradores, related_name = 'administrador_condominio', on_delete = models.CASCADE)
    nome = models.CharField(max_length = 150, )
    start_of_activities = models.DateTimeField('Início das atividades', auto_now_add = False, blank = True)
    main_activity = models.CharField(max_length = 150, default ='Condomínios Prediais',blank = True ) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'usuário_administrador', on_delete = models.CASCADE)
    descritpion = models.TextField('Descricao do condominio', blank = True)
    logo = models.ImageField(upload_to = 'settings/img', help_text = 'logotipo do condominio',) 
    img = models.URLField(help_text = 'Image do Condominio') 
    google_analytics = models.TextField('Google Analytics Code', blank = True) 
    cnpj = models.CharField(max_length = 150, blank = True)
    inscricao_estatual = models.CharField(max_length = 150, blank = True)
    email = models.EmailField('E-mail', unique=True)
    address = models.CharField('Endereço', max_length = 190, blank = True)
    cep = models.CharField('CEP da Localidade', max_length = 150, blank = True)    
    state = models.CharField('Estado',  max_length = 100, blank = True)
    status = models.CharField(max_length = 100, choices = STATUS_CHOICES, default = 'Positivo')
    uf = models.CharField(max_length = 2, help_text = "O UF do estador exemplo DF", default = 'DF')   
    city = models.CharField('Cidade', max_length = 190, blank = True)
    phone = PhoneField(blank=True, help_text='Numero do Telefone', default = '(00) 0000-0000')
    periodo = models.DateTimeField(auto_now_add = False, help_text="Periodo do movimento")
    is_active = models.BooleanField('Está ativo?', blank=True, default = False)     
    receitas = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Total das Receitas Condominial', default = 0,blank = True)
    despesas = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Total das Despesas Condominial', default = 0, blank = True)
    inadinplencia= models.DecimalField(decimal_places = 2, max_digits =10, help_text='Total do valor dos Inadinplentes', default = 0,blank = True)
    caixa = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Caixa do condomino', default = 0)
    valor_taxa = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Valor da taxa mensal', default = 0,blank = True)
    taxa_extra_ordinaria = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Valor da taxa Ordinária', default = 0,blank = True)
    fundo_de_reserva = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Valor da taxa Ordinária', default = 0,blank = True)
    valor_total = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Valor total da taxa mensal', default = 0,blank = True)
    lancamento_futuro = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Boletos a serem pagos', default = 0,blank = True)
    conta_corrente = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Saldo da Conta Corrente', default = 0,blank = True)
    conta_poupança = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Saldo da Poupança', default = 0,blank = True)
    
    
    
    
    
    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Condomínio'
        verbose_name_plural = 'Condomínio'





class Taxa_Ordinaria(models.Model):
    administradores = models.ForeignKey(Administradores, related_name = 'administrador', on_delete = models.CASCADE)
    condominio = ForeignKey(Condominios, related_name = "taxa_odinaria", on_delete = models.CASCADE)
    created = DateTimeField(auto_now_add = True, help_text = " Criação da Taxa Condominal Mensal")
    updated = DateTimeField(auto_now_add = True, help_text = "Taxa Condominal Mensal")
    taxa = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Taxa Ordinária Condiminial Mensal', default = 0, blank = True)
    extra = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Taxa Extraordinária Condiminial Mensal', default = 0, blank = True)
    fundo = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Taxa para Fundo de Reserva', default = 0, blank = True)
    total = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Total das Taxas mensais', default = 0, blank = True)
    multa_mes = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Porcetagem do valor da multa mensal', default = 0, blank = True)
    multa_diaria = models.CharField(max_length= 11 ,help_text='Porcetagem do valor da multa diaria', blank = True)



    class Meta:
        verbose_name = 'Taxa Ordinaria'
        verbose_name_plural = 'Taxas Ordinaria'



    def __str__(self):
        return f'{self.condominio}'




class Taxa_Extraordinaria(models.Model):
    administradores = models.ForeignKey(Administradores, related_name = 'administradora_extraordinaria', on_delete = models.CASCADE)
    condominio = ForeignKey(Condominios, related_name = "taxa_extraordinaria", on_delete = models.CASCADE)
    created = DateTimeField(auto_now_add = True, help_text = " Criação da Taxa Condominal Extraordinária")
    updated = DateTimeField(auto_now_add = True, help_text = "Taxa Condominal Extraordinária")
    inicio = DateTimeField(auto_now_add = False, help_text = " Inicio da Taxa CondominalExtraordinária")
    fim = DateTimeField(auto_now_add = False, help_text = "Fim da Taxa Condominal Extraordinária")   
    valor = models.DecimalField(decimal_places = 2, max_digits =10, help_text='Valor das Taxas Extraordinária', default = 0, blank = True)



    
    class Meta:
        verbose_name = 'Taxa Extraordinária'
        verbose_name_plural = 'Taxas Extraordinária'



    def __str__(self):
        return self.valor


class Ocorrencias(models.Model):

    STATUS_CHOICES = (

        ('analizando','Analizando'),
        ('concluido','Concluido'),
    )

    id = models.CharField(max_length = 150, primary_key = True,  help_text = "Indentificador id da Ocorrência")
    sindico = models.ForeignKey(Administradores, related_name = "sindico_atual_ocorrencia", on_delete = models.CASCADE)
    status = models.CharField(max_length = 150, choices = STATUS_CHOICES, default = 'analizando')
    created = models.DateTimeField(auto_now_add = True,help_text = 'Data da criação da ocorrência')
    data_da_ocorrencia = models.DateTimeField(auto_now_add = False, help_text = 'Data da criação da ocorrência')
    unidade = models.CharField(max_length = 150,  help_text = "Unidade do autor da ocorrência")
    declarante = models.CharField(max_length = 150,  help_text = "Pessoas que esta fazendo a ocorrência")
    unidade_envolvida = models.CharField(max_length = 150,  help_text = "unidade envolvida na ocorrência")
    declarado = models.CharField(max_length = 150,  help_text = "Pessoas que esta fazendo a ocorrência")
    descricao = models.TextField(help_text = "Descrição da Ocorrêcia")
    dias = models.IntegerField(help_text = "Dias Restante")

    def __str__(self):
        return f'{self.declarante}'



class Advertencia(models.Model):
    STATUS_CHOICES = (

        ('analizando','Analizando'),
        ('concluido','Concluido'),
    )

    id = models.CharField(max_length = 150, primary_key = True,  help_text = "Indentificador id da Advertência")
    sindico = models.ForeignKey(Administradores, related_name = "sindico_atual_advertencia", on_delete = models.CASCADE)
    status = models.CharField(max_length = 150, choices = STATUS_CHOICES, default = 'analizando')
    created = models.DateTimeField(auto_now_add = True,help_text = 'Data da criação da Advertência')
    morador = models.ForeignKey(Morador, related_name = "morador_advertencia", on_delete = models.CASCADE)
    unidade = models.CharField(max_length = 9, help_text = "Unidade do morador")
    regimento_interno = models.ForeignKey(Regimento_Interno, related_name = "codigo_advertencia", on_delete = models.CASCADE)
    termo_proibido = models.CharField(max_length = 400, help_text="definição do termo proibido")
    data_reclamacao = models.DateTimeField(auto_now_add = True,help_text = 'Data Relamação por morador')
    fato_ocorrido = models.TextField(help_text = "descrição do fato ocorrido")

    def __str__(self):
        return f'{self.morador}'




class Multa(models.Model):
    id = models.CharField(max_length = 150, primary_key = True, help_text = "Indentificador id da multa")
    data_aplicacao = models.DateTimeField(auto_now_add = True, help_text = 'Data da aplicação da Multa')
    sindico = models.ForeignKey(Administradores, related_name = "sindico_atual_multa", on_delete = models.CASCADE)
    morador = models.ForeignKey(Morador, related_name = "morador_multa", on_delete = models.CASCADE)
    condominio = models.ForeignKey(Condominios, related_name = "condominio_multa", on_delete = models.CASCADE)
    valor_multa = models.DecimalField(decimal_places = 2, max_digits = 10, default = 0, help_text = "valor total da multa")
    Advertencia = models.ManyToManyField(Advertencia,help_text = "Advertência Aplicadas")
    data_decorrente = models.CharField( max_length = 150, help_text="Data das advertências")
    prazo = models.DateTimeField(auto_now_add = False, help_text = "Data de termino do prazo")
    local_data = models.CharField(max_length = 280, help_text = "Ex. Brasilia 01 de Janeiro de 2021")

    def __str__(self):
        return f'{self.morador}'



class Recurso_Multa(models.Model):
    id = models.CharField(max_length = 150, primary_key = True, help_text = "Indentificador id da multa")
    data_recurso = models.DateTimeField(auto_now_add = True, help_text = 'Data criação do recurso')
    sindico = models.ForeignKey(Administradores, related_name = "sindico_multa_recurso", on_delete = models.CASCADE)
    condominio = models.ForeignKey(Condominios, related_name = "condominio_recurso", on_delete = models.CASCADE)
    morador = models.ForeignKey(Morador, related_name = "morador_recurso", on_delete = models.CASCADE)
    multa = models.ForeignKey(Multa, related_name = "informativo_recurso", on_delete = models.CASCADE)
    apelacao = models.TextField(help_text = "argumento da apelação")
    local_data = models.CharField(max_length = 280, help_text = "Ex. Brasilia 01 de Janeiro de 2021")

    def __str__(self):
        return f'{self.morador}'




class Arrecadacao(models.Model):
    
    administradores = models.ForeignKey(Administradores, related_name = 'administrador_atual', on_delete = models.CASCADE)
    condominios = models.ForeignKey(Condominios, related_name = 'analise_mensal', on_delete = models.CASCADE)
    created = models.DateTimeField( auto_now_add = True, help_text = 'O dia que gerado o relatório')
    data_referencia = models.DateTimeField(auto_now_add = False, help_text = 'Data de Referência')
    arrecadacao_prevista = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = " Arrecadação Prevista")
    arrecadacao_realizada = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = " Arrecadação Realizada")
    Gastos = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Gasto Mensal")
    inadimplencia = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Total da Inadimplência")
    saldo_geral = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = "Saldo Geral")





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







class Contratos(models.Model):

    STATUS_MODELS = (

            ('aluguel','Aluguel'),
            ('seguro','Seguro'),
            ('manutenção','Manutenção'),
        
            )

    STATUS_CHOICES  = (

        ('vigente','Vigente'),
        ('não vigente','Não Vigente'),
    )

    id = CharField(max_length = 150, primary_key = True, help_text = 'Numero do Contrato')
    categoria = models.ForeignKey(Categoria, related_name = 'contrato_categoria', on_delete = models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, related_name = 'subcategoria_contrato', on_delete = models.CASCADE)
    tipo = CharField(max_length = 150, choices = STATUS_MODELS, default = 'aluguel')
    status = CharField(max_length = 150, choices = STATUS_CHOICES, default = 'vigente')
    img = models.ImageField(upload_to = 'logo/empresa/contrato')
    empresa = CharField(max_length = 150,  help_text = 'Nome da Empresa' )
    descricao = models.TextField(help_text = 'Descrição')
    inicio = models.DateTimeField(auto_now_add = False, help_text = 'Data de Inicio do Contrato' )
    termino = models.DateTimeField(auto_now_add = False, help_text = 'Termino do Contrato')
    parcelas = models.IntegerField(help_text = 'A quantidade de parcelas')
    valor_parcelas = DecimalField(decimal_places = 2, max_digits = 10, help_text = ' Valor da Parcelas')
    valor_total = models.DecimalField(decimal_places = 2, max_digits = 10, help_text = 'Valor total do Contratos')


    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'


    def __str__(self):
        return f'{self.empresa}'

