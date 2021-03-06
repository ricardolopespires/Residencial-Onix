# Generated by Django 2.2 on 2022-04-01 19:01

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phone_field.models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'O nome de usuário só pode conter letras, digitos ou os seguintes caracteres: @/./+/-/_', 'invalid')], verbose_name='Nome de Usuário')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nome')),
                ('unidade', models.CharField(blank=True, max_length=150, null=True)),
                ('address', models.CharField(blank=True, max_length=190, verbose_name='Endereço')),
                ('date_of_birth', models.DateTimeField(default=django.utils.timezone.now)),
                ('state', models.CharField(blank=True, max_length=100, verbose_name='Estado')),
                ('condicao', models.CharField(choices=[('ativos', 'Ativos'), ('pendentes', 'Pendentes'), ('inativos', 'Inativos')], default='morador', max_length=100)),
                ('status', models.CharField(choices=[('morador', 'Morador'), ('adminitrador', 'Administrador'), ('sindico', 'sindico')], default='ativos', max_length=100)),
                ('genre', models.CharField(choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')], default='masculino', max_length=100)),
                ('city', models.CharField(blank=True, max_length=190, verbose_name='Cidade')),
                ('phone', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31)),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Está ativo?')),
                ('is_staff', models.BooleanField(blank=True, default=False, verbose_name='É da equipe?')),
                ('is_administradora', models.BooleanField(blank=True, default=False, verbose_name='Administradora')),
                ('is_profissional', models.BooleanField(blank=True, default=False, verbose_name='Síndico profissional')),
                ('is_sindico', models.BooleanField(blank=True, default=False, verbose_name='Síndico')),
                ('is_morador', models.BooleanField(blank=True, default=False, verbose_name='Morador')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de Entrada')),
                ('img', models.ImageField(blank=True, upload_to='user')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True, verbose_name='Chave')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('confirmed', models.BooleanField(blank=True, default=False, verbose_name='Confirmado?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resets', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Nova Senha',
                'verbose_name_plural': 'Novas Senhas',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuário_newsletter', to=settings.AUTH_USER_MODEL, verbose_name='usuário_newsletter')),
            ],
        ),
        migrations.CreateModel(
            name='Administradores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidade', models.CharField(blank=True, max_length=150, null=True)),
                ('data_de_inicio', models.DateTimeField(help_text=' Data de Inicio do Mandato de Síndico')),
                ('termino', models.DateTimeField(help_text='O Fim do Mandato de Síndico')),
                ('mandato', models.CharField(blank=True, choices=[('vigente', 'Vigente'), ('não vigente', 'Não Vigente')], default='vigente', max_length=150)),
                ('status', models.CharField(blank=True, choices=[('sindico profissional', 'Sindico Profissional'), ('administradora', 'Administradora'), ('sindico', 'Sindico'), ('presidente do conselho fiscal ', 'Presidente do Conselho Fiscal '), ('1º membro', '1º Membro'), ('2º membro', '2º Membro'), ('3º membro', '3º Membro'), ('4º membro', '4º Membro'), ('5º membro', '5º Membro')], default='morador', max_length=150)),
                ('nome', models.CharField(help_text='Nome do sindico do mandato', max_length=150)),
                ('img', models.ImageField(blank=True, help_text='Image do Síndico', upload_to='sindico/img')),
                ('sexo', models.CharField(choices=[('masculino', 'Masculino'), ('feminino', 'Feminino')], default='masculino', help_text='O Genero do Síndico ', max_length=150)),
                ('data_nascimento', models.CharField(blank=True, help_text='Data de Nacimento do Pestador de Serviço', max_length=150)),
                ('estado_civil', models.CharField(choices=[('solteiro', 'Solteiro'), ('solteira', 'Solteira'), ('casado', 'Casado'), ('casada', 'Casada'), ('viuvo', 'Viuvo'), ('viuva', 'viuva')], default='solteiro', help_text='O Estado Civil do Síndico ', max_length=150)),
                ('cpf', models.CharField(blank=True, help_text='Documento CPF do do Síndico ', max_length=150)),
                ('rg', models.CharField(blank=True, help_text='Documento RG do Síndico ', max_length=150, verbose_name='RG')),
                ('mae', models.CharField(blank=True, help_text='O Nome da Mãe do Síndico ', max_length=150)),
                ('pai', models.CharField(blank=True, help_text='O Nome da Pai do Síndico ', max_length=150)),
                ('naturalidade', models.CharField(blank=True, help_text=' A cidade do Síndico onde Nasceu', max_length=150)),
                ('nacionalidade', models.CharField(blank=True, help_text='O pais que  Síndico  Nasceu', max_length=150)),
                ('endereco', models.CharField(blank=True, help_text='Endereço onde o Síndico Mora', max_length=150)),
                ('numero', models.IntegerField(blank=True, help_text='Numero da Casa do Síndico')),
                ('complemento', models.CharField(blank=True, help_text='Complemento de informações', max_length=150)),
                ('bairro', models.CharField(blank=True, help_text='Bairro onde o Síndico Mora', max_length=150)),
                ('cidade', models.CharField(blank=True, help_text='A Cidade onde o Síndico Mora', max_length=150)),
                ('cep', models.CharField(blank=True, help_text='Numero Postal do Síndico ', max_length=150)),
                ('telefone', phone_field.models.PhoneField(blank=True, help_text='Numero do Telefone do Síndico ', max_length=150)),
                ('celular', phone_field.models.PhoneField(blank=True, help_text='Numero do celular do Síndico ', max_length=150)),
                ('email', models.EmailField(blank=True, help_text='Email do Síndico ', max_length=254)),
                ('is_active', models.BooleanField(blank=True, default=True, verbose_name='Está ativo?')),
                ('is_staff', models.BooleanField(blank=True, default=False, verbose_name='É da equipe?')),
                ('profissional', models.BooleanField(blank=True, default=False, verbose_name='Síndico profissional')),
                ('sindico', models.BooleanField(blank=True, default=False, verbose_name='Síndico')),
                ('morador', models.BooleanField(blank=True, default=False, verbose_name='morador')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de Entrada')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='usuário_condominio_sindico', to=settings.AUTH_USER_MODEL, verbose_name='usuário_condominio_sindico')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
                'ordering': ['nome'],
            },
        ),
    ]
