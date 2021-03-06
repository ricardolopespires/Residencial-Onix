# Generated by Django 2.2 on 2022-04-01 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local', models.CharField(choices=[('topo', 'Topo'), ('andares', 'Andares'), ('terreo', 'Terreo'), ('subsolo', 'SubSolo')], default='topo', max_length=150)),
                ('nome', models.CharField(help_text='Nome o Item de manutenção', max_length=150)),
                ('descricao', models.TextField(help_text='Descrição do item da manutenção')),
            ],
        ),
        migrations.CreateModel(
            name='Manutencao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('não realizada', 'Não Realizada'), ('realizada', 'Realizada'), ('pendente', 'Pedente')], default='não realizada', help_text='Status da Manutenção', max_length=150)),
                ('tipo', models.CharField(choices=[('preventiva', 'Preventiva'), ('preditiva', 'Preditiva'), ('corretiva', 'Corretiva')], default='preventiva', help_text='O tipo de Manutenção a ser realizada', max_length=150)),
                ('periodicidade', models.CharField(choices=[('semanal', 'Semanal'), ('quizenal', 'Quinzenal'), ('mensal', 'Mensal'), ('bimestral', 'Bimestral'), ('trimestral', 'Trimestral'), ('anual', 'Anual')], default='semanal', help_text='Periodo da manutenção', max_length=150)),
                ('fornecedor', models.CharField(help_text='fornecedor do material para manutencao', max_length=150)),
                ('responsavel', models.CharField(help_text='A Pessoa Responsável pela manutenção', max_length=150)),
                ('data_inicial', models.DateTimeField(blank=True, help_text='Data de Inicio da Manutenção ', null=True)),
                ('data_termino', models.DateTimeField(blank=True, help_text='Data do Termino da Manutenção', null=True)),
                ('data_previsao', models.DateTimeField(help_text='Data da Previsão do Termino da Manutenção')),
                ('descricao', models.TextField(help_text='Descrição da Manutenção')),
                ('valor_total', models.DecimalField(decimal_places=2, default=0, help_text='O valor Total da Manutenção', max_digits=10)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mantencao_item', to='manutencao.Item')),
            ],
        ),
    ]
