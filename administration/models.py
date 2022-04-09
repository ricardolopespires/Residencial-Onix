from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class Capitulo(models.Model):

    STATUS_CHOICES =    (

        ('vigente', 'Vigente'),
        ('revogado','revogado'),
    )


    title = models.CharField(max_length = 150, help_text = 'Titulo do Capítulo')
    subtitle = models.CharField(max_length = 150, help_text = 'Subtitulo do capítulo')
    status = models.CharField( max_length = 150, choices = STATUS_CHOICES, default = 'vigente', help_text = 'Status do código no momento atual' )

    def __str__(self):
        return self.title


class Regimento_Interno(models.Model):
    
    STATUS_CHOICES =    (

        ('vigente', 'Vigente'),
        ('revogado','revogado'),
    )

    id = models.CharField(max_length = 150, primary_key = True, help_text = 'numero do código')
    title = models.ManyToManyField(Capitulo)
    codigo = models.TextField( help_text = 'código')   
    status = models.CharField( max_length = 150, choices = STATUS_CHOICES, default = 'vigente', help_text = 'Status do código no momento atual' )


    def __str__(self):
        return self.codigo



class Checklist(models.Model):
    TIME_COURSE = (
                ('1', 'No prazo'),
                ('2', 'Atrasado'),
                ('3', 'Concluído'),
            )
    titulo = models.CharField(max_length = 150)
    slug = models.SlugField(verbose_name="Slug", unique="True", help_text="Slug é um campo em modo de preenchimento automático, mas se você quiser, pode modificar seu conteúdo")
    status = models.CharField(max_length=7, choices= TIME_COURSE, default=1)
    descricao = models.TextField() 
    data_entrega = models.DateTimeField(auto_now_add = False, help_text = "Estipular data para entrega dos documentos da gestão anterior", blank = True, null = True)
    data_entregou = models.DateTimeField(auto_now_add = False, help_text = "Data que foi entregue os documentos da gestão anterior", blank = True, null = True) 
    complete_per = models.IntegerField( validators = [MinValueValidator(0), MaxValueValidator(100)], default=0)

    def __str__(self):
        return self.titulo

class Item(models.Model):

    STATUS_TAREFA = (
        (0, "ABERTA"),
        (1, "TRABALHANDO"),
        (2, "PAUSADA"),
        (3, "CONCLUíDA")
    )

    
    titulo = models.CharField(max_length = 150)
    slug = models.SlugField( help_text="Slug é um campo em modo de preenchimento automático, mas se você quiser, pode modificar seu conteúdo")
    descricao = models.CharField(max_length = 100)
    data_entrega = models.DateTimeField(auto_now_add = False, help_text = "Estipular data para entrega dos documentos da gestão anterior", blank = True, null = True)
    data_entregou = models.DateTimeField(auto_now_add = False, help_text = "Data que foi entregue os documentos da gestão anterior", blank = True, null = True) 
    documentos = models.ForeignKey(
        Checklist,
        on_delete=models.CASCADE,
        related_name="tarefas"
    )    
    status = models.CharField(max_length=19, default=0, choices=STATUS_TAREFA)
    complete_per = models.IntegerField( validators = [MinValueValidator(0), MaxValueValidator(100)])
    
    def __str__(self):
        return self.titulo

    @property
    def is_open(self):
        return self.status == '0'

    @property
    def is_running(self):
        return self.status == '1'

    @property
    def is_paused(self):
        return self.status == '2'

    @property
    def is_done(self):
        return self.status == '3'

    def iniciar(self):
        self.horario_de_inicio_atual = timezone.now()
        self.status = 1

        self.save()

    def concluir(self):

        self.dataconclusao = timezone.now()
        self.duracao_total += timezone.now() - self.dataconclusao
        self.status = 3
        self.save()

    def pausar(self):
        diferenca = timezone.now() - self.horario_de_inicio_atual
        self.duracao_total += diferenca
        self.status = 2
        self.save()

    @property
    def permitido_iniciar(self):

        for requisito in self.pre_requisitos:
            if requisito.status != 3:
                return False
        return True

    class Meta:
        db_table = "tarefa"

    def __str__(self):
        return "{}, {}".format(self.titulo, self.status)
