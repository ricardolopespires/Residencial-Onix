from datetime import datetime, timedelta
from datetime import date
import random
import sys, os 
import pandas as pd
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Onix.settings")

import django
django.setup()


from financeiro.models import Banco, Conta, Despesas, Movimentacao, Saldo_Anterior, Prazo, Inadimplência
from condominio.models import Condominios, Taxa_Extraordinaria, Taxa_Ordinaria, Ocorrencias
from django.db.models import Avg, Count, Sum ,F
from accounts.models import Administradores
from moradores.models import Morador
from financeiro.models import Banco, Conta
from boleto.models import Boleto





'''


for inadinplencia in Inadimplência.objects.filter(status = 'inadinplente'):
              
        
        data_atual = date.today()
        
        inicial = inadinplencia.vencimento.strftime('%d-%m-%Y')
        final = data_atual.strftime('%d-%m-%Y')
        valor_total = float("{0:.2f}".format(inadinplencia.valor_total))
        # Data inicial
        d1 = datetime.strptime(inicial, '%d-%m-%Y')       
        # Data final
        d2 =  datetime.strptime(final, '%d-%m-%Y')    
        # Realizamos o calculo da quantidade de dias
        quantidade_dias = abs((d1 - d2).days)
        if quantidade_dias > 0 and quantidade_dias == 1 and quantidade_dias < 2:
                valor_total = float(valor_total * 2)
                inadinplencia.multa += valor_total
                inadinplencia.save()

        elif quantidade_dias > 0 and quantidade_dias  <  31:
                
                Inadimplência.objects.filter(status = 'inadinplente').update( juros = float(quantidade_dias * 0.11))
                valor_total  = inadinplencia.boleto + inadinplencia.juros + inadinplencia.multa + inadinplencia.atualizacao
                Inadimplência.objects.filter(status = 'inadinplente').update( valor_total = valor_total )

                
                print("O valor a pagar pelos {0} dias, será de R$: {1:.2f}".format(quantidade_dias, valor_total))

        



'''
for morador in Morador.objects.all():
    print(morador.unidade)
    for administrador in Administradores.objects.all():
    
        if administrador.morador == True:
            if administrador.unidade == morador.unidade:
                print("Insento")
            else:
                print("Boleto para pagar")


def gerador_de_boleto():


    for condominio in Condominios.objects.all():
        cedente = condominio.nome

    for morador in Morador.objects.all():        
        for administrador in Administradores.objects.all():
            if administrador.morador == True:
                if administrador.unidade == morador.unidade:
                    #print("Insento")
                    pass
                else:
                    data_atual = date.today()
                    data_do_vencimento = '15/0{}/{}'.format( data_atual.month, data_atual.year)+ " 00:00"
                    vencimento = datetime.strptime(data_do_vencimento, '%d/%m/%Y %H:%M')
                    taxa = Condominios.objects.all().aggregate(total=Sum('valor_total'))['total']
                    Morador.objects.all().update(valor_total = taxa, )
                    boleto = Boleto.objects.all()
                    boleto.create(

                    unidade = morador.unidade,
                    status = 'aberto',
                    codigo_banco = '104',
                    carteira = '108',
                    aceite = 'N',
                    valor_documento = taxa ,
                    valor = taxa,
                    data_vencimento = vencimento,
                    data_documento= data_atual,
                    data_processamento= data_atual,
                    numero_documento= random.randint(100, 10000),
                    agencia_cedente= "0816" ,
                    conta_cedente= "0002070-3",
                    cedente = condominio.nome,    
                    cedente_documento = condominio.cnpj,
                    cedente_cidade = condominio.city,
                    cedente_uf = "DF",
                    cedente_endereco=  condominio.address,
                    cedente_bairro = "Setor Sul",
                    cedente_cep= condominio.cep,
                    sacado_nome = morador.nome ,
                    sacado_documento = morador.cpf,
                    sacado_cidade = morador.city,
                    sacado_uf = "DF",
                    sacado_endereco = morador.endereco,
                    sacado_bairro = "Setor Sul",
                    sacado_cep = morador.cep ,
                    quantidade=   "",
                    especie_documento= ""  ,
                    especie=  "",
                    moeda= "R$"  ,
                    local_pagamento= "",
                    demonstrativo= " " ,
                    instrucoes= "1- Não receber após 20 dias. 2- Multa de 2,00% =R$ 1,30 após o vencimento.3- Taxa diária de permanência de 0,033% a.d.= R$ 0,02/dia"
                    

                        )
                    
                    print(morador.unidade)
                    
    
     


gerador_de_boleto()


'''





for taxa in Condominios.objects.all():
        taxa = taxa.valor_total
        
        data_atual = date.today()
        data_do_vencimento = '15/0{}/{}'.format( data_atual.month + 1, data_atual.year)+ " 00:00"
        vencimento = datetime.strptime(data_do_vencimento, '%d/%m/%Y %H:%M')
        

        for condominio in Condominios.objects.all():
                cedente = condominio.nome  


        for morador in Morador.objects.all():
                morador.unidade
                sacado_nome = morador.nome
                sacado_documento = morador.cpf
                sacado_cidade = morador.city
                sacado_uf = "DF"
                sacado_endereco = morador.endereco
                sacado_bairro = "Setor Sul",
                sacado_cep = "72415-206"
                

                boleto = Boleto.objects.all()

                numero_documento = random.randint(100, 10000)

        for morador in Morador.objects.all():
                print(morador.unidade)
                for administrador in Administradores.objects.all():
                        if administrador.morador == True:
                                if administrador.unidade == morador.unidade:
                                        pass
                        else:
                                boleto.create(
                            status = 'aberto',
                            codigo_banco = '104',
                            carteira = '108',
                            aceite = 'N',
                            valor_documento = taxa ,
                            valor = taxa,
                            data_vencimento = vencimento,
                            data_documento= data_atual,
                            data_processamento= data_atual,
                            numero_documento= numero_documento,
                            agencia_cedente= "0816" ,
                            conta_cedente= "0002070-3",
                            cedente = condominio.nome,    
                            cedente_documento = condominio.cnpj,
                            cedente_cidade = condominio.city,
                            cedente_uf = "DF",
                            cedente_endereco=  condominio.address,
                            cedente_bairro = "Setor Sul",
                            cedente_cep= condominio.cep,
                            sacado_nome = sacado_nome ,
                            sacado_documento = sacado_documento,
                            sacado_cidade = sacado_cidade,
                            sacado_uf = "DF",
                            sacado_endereco = sacado_endereco,
                            sacado_bairro = "Setor Sul",
                            sacado_cep = sacado_cep ,
                            quantidade=   "0",
                            especie_documento= ""  ,
                            especie=  "",
                            moeda= "R$"  ,
                            local_pagamento= "",
                            demonstrativo= " " ,
                            instrucoes= "1- Não receber após 20 dias. 2- Multa de 2,00% =R$ 1,30 após o vencimento.3- Taxa diária de permanência de 0,033% a.d.= R$ 0,02/dia"
                            )
'''
