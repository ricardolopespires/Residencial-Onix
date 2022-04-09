from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, UserManager)
#from livros.models import Ebook, Playlist, Favoritos, Review, Leitura
#from dashboard.views import reviews
from phone_field import PhoneField
from django.core import validators
from django.utils import timezone 
from django.conf import settings
#from movie.models import Movie
from datetime import timedelta

from django.db import models
import re
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):

    STATUS_GENRE = (
                    ('masculino', 'Masculino'),
                    ('feminino','Feminino')
                    )

    CONDICAO_CHOICES = (
                        ('ativos','Ativos'),
                        ('pendentes','Pendentes'),
                        ('inativos','Inativos'),
                     )

    STATUS_CHOICES = (
                        ('morador','Morador'),
                        ('adminitrador','Administrador'),
                        ('sindico','sindico'),
                     )
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True, 
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    name = models.CharField('Nome', max_length=100, blank=True)
    unidade = models.CharField(max_length = 150, blank=True, null = True)
    address = models.CharField('Endereço', max_length = 190, blank = True)
    date_of_birth = models.DateTimeField(default=timezone.now) 
    state = models.CharField('Estado',  max_length = 100, blank = True)
    condicao = models.CharField(max_length = 100, choices = CONDICAO_CHOICES, default = 'morador')
    status = models.CharField(max_length = 100, choices = STATUS_CHOICES, default = 'ativos')
    genre = models.CharField(max_length = 100, choices = STATUS_GENRE, default = 'masculino')
    city = models.CharField('Cidade', max_length = 190, blank = True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    is_administradora = models.BooleanField('Administradora', blank=True, default=False)
    is_profissional = models.BooleanField('Síndico profissional', blank=True, default=False)
    is_sindico = models.BooleanField('Síndico', blank=True, default=False)
    is_morador = models.BooleanField('Morador', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    img = models.ImageField(upload_to = 'user', blank = True)

 

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', on_delete = models.CASCADE
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']




class Newsletter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário_newsletter',
       related_name='usuário_newsletter', on_delete = models.CASCADE, blank = True, null = True )
    email = models.EmailField()

    def __str__(self):
        return self.email



class Administradores(models.Model):
    
    STATUS_MANDATO = (

        ('vigente','Vigente'),
        ('não vigente','Não Vigente'),
    )

    STATUS_TIPO = (

        
        ('sindico profissional', 'Sindico Profissional'),
        ('administradora', 'Administradora'),
        ('sindico','Sindico'),
        ('presidente do conselho fiscal ', 'Presidente do Conselho Fiscal '),
        ('1º membro', '1º Membro'),
        ('2º membro', '2º Membro'),
        ('3º membro', '3º Membro'),
        ('4º membro', '4º Membro'),
        ('5º membro', '5º Membro'),


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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='usuário_condominio_sindico', related_name='usuário_condominio_sindico', on_delete = models.CASCADE, blank = True, null = True )
    unidade = models.CharField(max_length = 150, blank=True, null = True)
    data_de_inicio = models.DateTimeField(auto_now_add = False, help_text = " Data de Inicio do Mandato de Síndico")
    termino = models.DateTimeField(auto_now_add = False, help_text = "O Fim do Mandato de Síndico")
    mandato = models.CharField(max_length = 150, choices = STATUS_MANDATO, default = 'vigente', blank=True,)
    status = models.CharField(max_length = 150, choices = STATUS_TIPO, default = 'morador',blank=True,)
    nome = models.CharField(max_length = 150 , help_text = 'Nome do sindico do mandato')
    img = models.ImageField(upload_to = 'sindico/img', blank = True, help_text = "Image do Síndico")
    sexo = models.CharField(max_length = 150, choices = STATUS_GENRE, default = 'masculino', help_text = "O Genero do Síndico ")
    data_nascimento = models.CharField(max_length = 150, help_text = "Data de Nacimento do Pestador de Serviço", blank=True)
    estado_civil = models.CharField(max_length = 150, choices = STATUS_CIVIL, default = 'solteiro', help_text = 'O Estado Civil do Síndico ' )   
    cpf = models.CharField( max_length = 150, blank = True, help_text = "Documento CPF do do Síndico ")
    rg = models.CharField('RG', max_length = 150, blank = True, help_text = "Documento RG do Síndico ")
    mae = models.CharField(max_length = 150, help_text = "O Nome da Mãe do Síndico ", blank=True)
    pai = models.CharField(max_length = 150, help_text = "O Nome da Pai do Síndico ", blank=True)
    naturalidade = models.CharField(max_length = 150, help_text = " A cidade do Síndico onde Nasceu", blank=True)
    nacionalidade = models.CharField(max_length = 150, help_text = "O pais que  Síndico  Nasceu", blank=True)
    endereco = models.CharField(max_length = 150, help_text = "Endereço onde o Síndico Mora", blank=True)
    numero = models.IntegerField(help_text = "Numero da Casa do Síndico", blank=True)
    complemento = models.CharField(max_length = 150, help_text = "Complemento de informações", blank=True)
    bairro = models.CharField(max_length = 150, help_text = "Bairro onde o Síndico Mora", blank=True)
    cidade = models.CharField(max_length = 150, help_text = "A Cidade onde o Síndico Mora", blank=True)
    cep = models.CharField(max_length = 150, help_text = "Numero Postal do Síndico ", blank=True)
    telefone = PhoneField(max_length = 150, help_text = "Numero do Telefone do Síndico ", blank=True)
    celular = PhoneField(max_length = 150, help_text = "Numero do celular do Síndico ", blank=True)
    email = models.EmailField(help_text = "Email do Síndico ", blank=True)
    is_active = models.BooleanField('Está ativo?', blank=True, default=True)
    is_staff = models.BooleanField('É da equipe?', blank=True, default=False)
    profissional = models.BooleanField('Síndico profissional', blank=True, default=False)
    sindico = models.BooleanField('Síndico', blank=True, default=False)
    morador = models.BooleanField('morador', blank=True, default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)


    class Meta:
        ordering = ['nome']
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'

    def __str__(self):
        return self.nome
    