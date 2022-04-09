from django.db import models
from phone_field import PhoneField

# Create your models here.








class Contato(models.Model):

    nome = models.CharField(max_length = 150,  help_text = "Digite seu Nome")   
    email = models.EmailField(help_text = "Digite seu Email")
    assunto = models. CharField(max_length = 150, help_text = "Digite o Assunto")
    message = models.TextField()


    def __srt__(self):
        return self.nome



class Newletter(models.Model):
    
    email = models.EmailField(help_text = "Digite seu Email") 


    def __srt__(self):
        return self.email