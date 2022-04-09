from phone_field import PhoneField
from datetime import timedelta
from django.db import models
from accounts.models import Administradores

# Create your models here.



class Morador(models.Model):

    STATUS_FINANCE = (

        
        ('em dia', "Em dia"),
        ('atrasada', 'Atrasada'),
        ('inadinplente', "Inadinplente"),
        ('paga', "Paga")
    )

    STATUS_CHOICES = (

        ('proprietario','Proprietario'),
        ('iquilino', 'Inquilino'),
        
        )

    STATUS_GENRE = (

        ('masculino', 'Masculino'),
        ('feminino','Feminino')

        )
    administrador = models.ForeignKey(Administradores, related_name = 'administradores', on_delete = models.CASCADE)
    unidade = models.CharField(max_length = 150,  help_text='Unidade')
    img = models.ImageField(upload_to = 'User', blank = True)
    proprietario = models.CharField(max_length = 150, blank = 150)
    emergencia = models.CharField(max_length = 150, blank = 150)
    nome = models.CharField('Nome', max_length=100, blank=True)    
    cpf = models.CharField('CPF', max_length = 150, blank = True)
    rg = models.CharField('RG', max_length = 150, blank = True)
    email = models.EmailField('E-mail', unique=True, blank =True, null= True)  
    endereco = models.CharField('Endereço', max_length = 190, blank = True)
    date_of_birth = models.DateTimeField('Data de Nascimento', auto_now_add =False,  blank = True, null = True)
    quantidade = models.IntegerField( help_text='Quantidade de moradores fixo', default = '0', blank = True, ) 
    estado = models.CharField('Estado',  max_length = 100, blank = True)
    financeiro = models.CharField(max_length = 28, choices = STATUS_FINANCE, default = 'em dia', blank = True, )
    status = models.CharField('Satus', max_length = 100, choices = STATUS_CHOICES, default = 'proprietario', blank = True, )
    uf = models.CharField(max_length = 150, help_text = 'UF do estado', blank = True, )
    genero = models.CharField('Genero', max_length = 100, choices = STATUS_GENRE, default = 'masculino', blank = True, )
    city = models.CharField('Cidade', max_length = 190, blank = True)
    bairro = models.CharField(max_length = 150, help_text = 'bairro do Morador', blank = True, )
    cep = models.CharField(max_length = 150, help_text = 'Cep da rua do  Morador', blank = True, )
    telefone = PhoneField(blank=True, help_text='Telefone para contato')
    is_active = models.BooleanField('Está ativo?', blank=True, default = False)    
    carro = models.BooleanField('Tem Veiculo',help_text = 'O morador tem Carro', blank = True, )
    animais = models.BooleanField('Tem Animais', help_text = 'Posssuidor de animais de Pequeno Porte', blank = True, )
    taxa = models.DecimalField( decimal_places = 2, max_digits = 10, help_text='Taxa Condominial', default =0, blank = True, null = True)
    taxa_extra = models.DecimalField( decimal_places = 2, max_digits = 10, help_text='Taxa Exraordinaria', default = 0, blank = True, null = True)
    valor_total = models.DecimalField( decimal_places = 2, max_digits = 10, help_text='Valor Total', default = 0, blank = True, null = True)
    created = models.DateTimeField('Data do cadastramento do Morador', auto_now_add = True, blank = True, )
    updated = models.DateTimeField('Data da ultima atualização dos dados do morador', auto_now_add = True, blank = True, )
    mudanca = models.DateTimeField(auto_now_add = False, help_text='Data que Morador mudou', blank=True, null=True)
    saida = models.DateTimeField(auto_now_add = False, help_text='Data do Morador saiu', blank=True, null=True) 
    entrada = models.DateTimeField('Data de Entrada', auto_now_add = False, blank = True, null = True)    
    funcionario = models.BooleanField(blank=True, default = False, help_text = 'O morador tem funcionario') 

    class Meta:
        ordering = [ '-id' ]
        verbose_name ='Modador'
        verbose_name_plural = 'Moradores'

    def __str__(self):
        return self.nome




class Pessoa(models.Model):
    STATUS_KINSHIP = (

        ('responsável','Responsável'),        
        ('esposo', 'Esposo'),
        ('esposa','Esposa'),
        ('pai','PAi'),
        ('mãe','Mãe'),
        ('filho','Filho'),
        ('filha','Filha'),
        ('irmão', 'Irmão'),
        ('irmã','Irmã'),
        ('tio','Tio'),
        ('tia','Tia'),
        ('sobrinho','Sobrinho'),
        ('sobrinha','Sobrinha'),
        ('primo','Primo'),
        ('prima','Prima'),
        ('cunhado','Cunhado'),
        ('cunhada','Cunhada'),
        ('genro','Genro'),
        ('nora','Nora'),
        ('neto','Neto'),
        ('neta','Neta'),
        
    )

    morador = models.ForeignKey(Morador, related_name = 'moradores_parentes', on_delete = models.CASCADE)
    parente = models.CharField(max_length = 150,)
    status = models.CharField( max_length = 40, choices = STATUS_KINSHIP , default = 'responsável') 

    def __str__(self):
        return self.parentesco



class Funcionario(models.Model):
    morador = models.ForeignKey(Morador, related_name = "morador_funcionario", on_delete = models.CASCADE )
    nome = models.CharField( max_length=100, blank=True, help_text = "Nome do funcionário")    
    cpf = models.CharField( max_length = 150, blank = True, help_text = 'CPF do Funcionário')
    rg = models.CharField( max_length = 150, blank = True, help_text = 'RG do Funcionário')
    cargo = models.CharField( max_length = 150, blank = True, help_text = 'Cargo do Funcionário')
    Expediente = models.CharField( max_length = 150, blank = True, help_text = 'Horário do Expediente do Funcionário')
    img = models.ImageField(upload_to = 'Funcionario/Morador', blank = True, help_text = 'Image do funcionaro do Morador')




class Veiculo(models.Model):

    STATUS_TIPO = (

            ('carro','Carro'),
            ('moto','Moto'),
    ) 

    STATUS_CHOICES = (

        ('autorizado','Autorizado'),
        ('não autorizado','Não Autorizado'),
        ('avaliação','Avaliação'),
    )

    STATUS_CONDICAO = (

        ('proprietario', 'Proprietário'),
        ('aluguel','Aluguel'),
    )

    id = models.CharField(max_length = 40, primary_key=True, help_text="Numero da garagem")
    morador = models.ForeignKey(Morador, related_name = "condutor", on_delete = models.CASCADE )
    tipo = models.CharField( max_length = 150, choices = STATUS_TIPO, default = 'carro', help_text = 'O tipo do Veiculo do Morador')
    status = models.CharField(max_length = 150, choices = STATUS_CHOICES, default = 'avaliação', help_text = 'Status do Veiculo')
    condicao = models.CharField(max_length = 150, choices = STATUS_CONDICAO, default = 'proprietario', help_text = 'Condição da Vaga de Garagem')
    marca = models.CharField(max_length = 150, blank = True, help_text = "A Marca do Veiculo")
    modelo = models.CharField(max_length = 150, blank = True, help_text = "A Modelo do Veiculo")
    cor = models.CharField(max_length = 150, blank = True, help_text = "A Cor da Pintura do Veiculo")
    placa = models.CharField(max_length = 150, blank = True, help_text = "A placa do Veiculo")
    img = models.ImageField(upload_to = 'Veiculo/Morador', blank = True, help_text = 'Image do veiculo do Morador')




class Animal(models.Model):

    STATUS_TIPO = (

            ('cães','Cães'),
            ('gatos','Gatos'),
            ('pássaros','Pássaros'),
            ('peixes','Peixes'),
            ('hamster','Hamster'),
            ('porquinho da ídia','Porquinho da Índia'),
            ('coelho','Coelho'),
            
                ) 

    id = models.CharField(max_length = 40, primary_key=True, help_text="Numero da do apartamento")
    proprietario = models.ForeignKey(Morador, related_name = "animal_estimção", on_delete = models.CASCADE )
    nome = models.CharField(max_length = 150, blank = True, help_text = "O Nome do Animal")
    tipo = models.CharField( max_length = 150, choices = STATUS_TIPO, default = 'cães', help_text = "O Tipo do Animal de Estimação" )
    raca = models.CharField(max_length = 150, blank = True, help_text = "A Raça do Animal de Estimação")
    cor = models.CharField(max_length = 150, blank = True, help_text = "A Cor do Animal de Estimação")
    img = models.ImageField(upload_to = 'Animal/Morador', blank = True, help_text = 'Imagem do Animal de Estimação')
    

