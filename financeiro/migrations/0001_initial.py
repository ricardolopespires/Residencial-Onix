# Generated by Django 2.2 on 2022-04-01 19:01

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('condominio', '0001_initial'),
        ('accounts', '0001_initial'),
        ('moradores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.CharField(blank=True, help_text='Código do banco', max_length=150, primary_key=True, serialize=False)),
                ('ispb', models.IntegerField(blank=True, help_text='ISPB (Identificador do Sistema de Pagamento Brasileiro)')),
                ('img', models.URLField(blank=True, help_text='Logo do banco')),
                ('nome', models.CharField(blank=True, help_text='Nome do Banco onde está a conta', max_length=150)),
                ('agencia', models.CharField(blank=True, help_text='O numero da agência onde está a conta', max_length=150)),
                ('endereco', models.CharField(blank=True, help_text='Endereço onde está localizada a Agência', max_length=150)),
                ('telefone', phone_field.models.PhoneField(blank=True, help_text='Numero do Telefone do Síndico ', max_length=150)),
            ],
            options={
                'verbose_name': 'Banco',
                'verbose_name_plural': 'Bancos',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.URLField(blank=True, help_text=' logo da categoria', null=True)),
                ('title', models.CharField(help_text='O titulo da categoria prestação de serviço', max_length=150)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.CharField(help_text='O numero da conta', max_length=150, primary_key=True, serialize=False)),
                ('tipo', models.CharField(choices=[('conta corrente', 'Conta Corrente'), ('poupança', 'Poupança')], default='conta corrente', help_text='A conta é corrente ou poupança', max_length=150)),
                ('estilo', models.CharField(choices=[('pessoa jurídica', 'Pessoa Jurídica'), ('pessoa fisíca', 'Pessoa Fisíca')], default='pessoa jurídica', help_text='A conta é de pessoa juridica ou', max_length=150)),
                ('criada', models.DateTimeField(blank=True, help_text='Data em que foi aberta a conta')),
                ('fechada', models.DateTimeField(blank=True, help_text='Data do fechamento da conta', null=True)),
                ('creditos', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='O valores creditados na conta', max_digits=10, null=True)),
                ('debitos', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='O valores debitados da conta', max_digits=10, null=True)),
                ('saldo', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='O valor do saldo da conta', max_digits=10)),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banco_agencia', to='financeiro.Banco')),
                ('sindico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sindico_conta', to='accounts.Administradores')),
                ('titular_da_conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_condominios', to='condominio.Condominios')),
            ],
        ),
        migrations.CreateModel(
            name='Prazo',
            fields=[
                ('id', models.CharField(help_text='Indentificador da despesas', max_length=150, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('descricao', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('aberta', 'aberta'), ('em dia', 'em dia'), ('atrasada', 'atrasada'), ('paga', 'PAGA')], default=0, max_length=19)),
                ('complete', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('complete_per', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('due', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategoria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='O titulo da categoria prestação de serviço', max_length=150)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoria', to='financeiro.Categoria')),
            ],
            options={
                'verbose_name': 'Sub-Categoria',
                'verbose_name_plural': 'Sub Categorias',
            },
        ),
        migrations.CreateModel(
            name='Saldo_Anterior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(help_text='A data de movimento')),
                ('valor', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='O valor do saldo da conta do mês passado', max_digits=10)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saldo_mes_anterior', to='financeiro.Conta')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.CharField(blank=True, max_length=40, primary_key=True, serialize=False)),
                ('unidade', models.CharField(help_text='numero de unidade', max_length=150)),
                ('data_vencimento', models.DateTimeField(help_text='Data do vencimento do boleto')),
                ('data_pagamento', models.DateTimeField(help_text='Data de Pagamento')),
                ('juros', models.DecimalField(decimal_places=2, default=0, help_text='O valor do juros', max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, help_text='O valor total do Pagamento', max_digits=10)),
                ('morador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamento_morador', to='moradores.Morador')),
            ],
        ),
        migrations.CreateModel(
            name='Movimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField(help_text='A data de movimento')),
                ('descricao', models.TextField(help_text='Descrição do movimento')),
                ('tipo', models.CharField(choices=[('-', '-'), ('D', 'Debito'), ('C', 'Cretido')], default='-', help_text='O tipo do movimento bancario', max_length=150)),
                ('valor', models.DecimalField(decimal_places=2, help_text='O valor do movimento', max_digits=10)),
                ('saldo', models.DecimalField(decimal_places=2, help_text='O valor que ficou de saldo na conta', max_digits=10)),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conta_movimentação', to='financeiro.Conta')),
                ('sindico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sindico_movimentação', to='accounts.Administradores')),
            ],
        ),
        migrations.CreateModel(
            name='Inadimplência',
            fields=[
                ('id', models.CharField(blank=True, max_length=40, primary_key=True, serialize=False)),
                ('unidade', models.CharField(help_text='Numero da unidade ', max_length=40)),
                ('acordo', models.BooleanField(help_text='Fazendo acordo para pagamento de parcela atrasadas')),
                ('status', models.CharField(choices=[('atrasado', 'Atrasado'), ('inadinplente', 'Inadinplente'), ('acordo', 'Acordo'), ('quitado', 'Quitado')], default='inadinplente', max_length=150)),
                ('vencimento', models.DateTimeField(help_text='O mês do vencimento do boleto')),
                ('referente', models.DateTimeField(help_text='O mês de referência')),
                ('dias', models.IntegerField(help_text='quantidade de dia que estão em atraso')),
                ('boleto', models.DecimalField(decimal_places=2, help_text='O valor da condominial do mês equivalente', max_digits=10)),
                ('juros', models.DecimalField(decimal_places=2, help_text='Juros do valor da condominial do mês equivalente', max_digits=10)),
                ('multa', models.DecimalField(decimal_places=2, help_text='multa do valor da condominial do mês equivalente', max_digits=10)),
                ('atualizacao', models.DecimalField(decimal_places=2, help_text='atualização ', max_digits=10)),
                ('honorarios', models.DecimalField(decimal_places=2, help_text='Honorários da Administradora ', max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, help_text='O valor total do debito da inadinplência', max_digits=10)),
                ('morador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='morador_inadimplente', to='moradores.Morador')),
            ],
        ),
        migrations.CreateModel(
            name='Despesas',
            fields=[
                ('id', models.CharField(help_text='Numero da nota ou RG se for pessoa fisica', max_length=150, primary_key=True, serialize=False)),
                ('beneficiario', models.CharField(help_text='O Nome do Benefiçiario ', max_length=150)),
                ('tipo', models.CharField(choices=[('pessoa juridica', 'Pessoa Juridica'), ('pessoa fisica', 'Pessoas Fisica')], default='pessoa juridica', help_text='Forma de regime do prestador do serviço', max_length=150)),
                ('status', models.CharField(choices=[('aberta', 'Aberta'), ('paga', 'Paga'), ('atrasada', 'Atrasada')], default='aberta', help_text='O status da conta', max_length=150)),
                ('despesas', models.CharField(choices=[('funcionario', 'Funcionario'), ('manutencao', 'Manutencao'), ('consumo', 'Consumo'), ('outros', 'Outros')], default='consumo', help_text='Tipo de despesa mensal', max_length=150)),
                ('descricao', models.TextField(help_text='Descrição do documento')),
                ('lancamento', models.DateTimeField(auto_now_add=True, help_text='Data do Vencimento do documento')),
                ('vencimento', models.DateTimeField(blank=True, help_text='Data do Vencimento do documento')),
                ('pagamento', models.DateTimeField(help_text='Data que foi Pago o Documento')),
                ('valor', models.DecimalField(decimal_places=2, help_text='valor total do documento', max_digits=10)),
                ('desconto', models.DecimalField(decimal_places=2, help_text='Valor do Desconto', max_digits=10)),
                ('multa', models.DecimalField(decimal_places=2, help_text='Valor da Multa', max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, help_text='O valor Total do documento', max_digits=10)),
                ('categoria', models.ForeignKey(help_text='Categoria da Prestação de Serviços', on_delete=django.db.models.deletion.CASCADE, related_name='despesa_categoria', to='financeiro.Categoria')),
                ('servico', models.ForeignKey(help_text='Serviço Prestado', on_delete=django.db.models.deletion.CASCADE, related_name='despesa_subcategoria', to='financeiro.SubCategoria')),
                ('sindico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sindico_despesa', to='accounts.Administradores')),
            ],
            options={
                'verbose_name': 'Despesa',
                'verbose_name_plural': 'Despesas',
            },
        ),
        migrations.CreateModel(
            name='Acordo',
            fields=[
                ('id', models.CharField(blank=True, max_length=40, primary_key=True, serialize=False)),
                ('unidade', models.CharField(help_text='Numero da unidade ', max_length=40)),
                ('acordo', models.BooleanField(help_text='Fazendo acordo para pagamento de parcela atrasadas')),
                ('status', models.CharField(choices=[('atrasado', 'Atrasado'), ('inadinplente', 'Inadinplente'), ('quitado', 'Quitado')], default='inadinplente', max_length=150)),
                ('vencimento', models.DateTimeField(help_text='O mês do vencimento do boleto')),
                ('referente', models.DateTimeField(help_text='O mês de referência')),
                ('dias', models.IntegerField(help_text='quantidade de dia que estão em atraso')),
                ('boleto', models.DecimalField(decimal_places=2, help_text='O valor da condominial do mês equivalente', max_digits=10)),
                ('juros', models.DecimalField(decimal_places=2, help_text='Juros do valor da condominial do mês equivalente', max_digits=10)),
                ('multa', models.DecimalField(decimal_places=2, help_text='multa do valor da condominial do mês equivalente', max_digits=10)),
                ('atualizacao', models.DecimalField(decimal_places=2, help_text='atualização ', max_digits=10)),
                ('honorarios', models.DecimalField(decimal_places=2, help_text='Honorários da Administradora', max_digits=10)),
                ('valor_total', models.DecimalField(decimal_places=2, help_text='O valor total do debito da inadinplência', max_digits=10)),
                ('morador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='morador_acordo', to='moradores.Morador')),
            ],
        ),
    ]
