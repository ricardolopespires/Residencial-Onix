from django.db import models

# Create your models here.





class Item(models.Model):

    STATUS_LOCAL = (

                ('topo','Topo'),
                ('andares','Andares'),
                ('terreo','Terreo'),
                ('subsolo','SubSolo'),
                
                    )
    
    local = models.CharField(max_length = 150, choices = STATUS_LOCAL, default = 'topo')
    nome = models.CharField(max_length = 150, help_text = 'Nome o Item de manutenção')
    descricao = models.TextField(help_text = "Descrição do item da manutenção")

    
    def __srt__(self):  
        return self.nome





class Manutencao(models.Model):

    STATUS_TIPO = (

        ('preventiva','Preventiva'),
        ('preditiva','Preditiva'),
        ('corretiva','Corretiva'),

    )


    STATUS_CHOICES = (

            ('não realizada', 'Não Realizada'),
            ('realizada','Realizada'),
            ('pendente','Pedente'),

    )


    STATUS_PERIODO = (
            
            ('semanal','Semanal'),
            ('quizenal','Quinzenal'),
            ('mensal','Mensal'),
            ('bimestral', 'Bimestral'),
            ('trimestral','Trimestral'),
            ('anual','Anual')
        
        )

    status = models.CharField( max_length = 150, choices = STATUS_CHOICES, default = "não realizada", help_text = "Status da Manutenção")
    tipo = models.CharField( max_length = 150, choices = STATUS_TIPO, default = 'preventiva', help_text = "O tipo de Manutenção a ser realizada")
    item = models.ForeignKey(Item, related_name ='mantencao_item' , on_delete = models.CASCADE)
    periodicidade = models.CharField(max_length = 150, choices = STATUS_PERIODO, default = "semanal", help_text = "Periodo da manutenção")
    fornecedor = models.CharField(max_length = 150 , help_text = 'fornecedor do material para manutencao')
    responsavel = models.CharField( max_length = 150, help_text = "A Pessoa Responsável pela manutenção")
    data_inicial = models.DateTimeField(auto_now_add = False, help_text = "Data de Inicio da Manutenção ", blank = True, null = True)
    data_termino = models.DateTimeField(auto_now_add = False, help_text = "Data do Termino da Manutenção", blank = True, null = True)
    data_previsao = models.DateTimeField(auto_now_add = False, help_text = "Data da Previsão do Termino da Manutenção")
    descricao = models.TextField(help_text = "Descrição da Manutenção")
    valor_total = models.DecimalField( decimal_places = 2, max_digits = 10, default = 0, help_text = "O valor Total da Manutenção") 

            
    def __str__(self):
        return f'{self.item}'