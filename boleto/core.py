from django.shortcuts import get_object_or_404
from django.db.models import Sum
from decimal import Decimal
import random




def gerador_de_boleto(Condominios, Morador, Administradores, date, datetime, Boleto):


    for condominio in Condominios.objects.all():
        cedente = condominio.nome

    for administrador in Administradores.objects.all():
        administrador

    for morador in Morador.objects.all():
        
        if  morador.unidade == administrador.unidade:
            print("Insento")

            
        elif Boleto.objects.all().count() > 0:
            if Boleto.objects.filter(unidade = morador.unidade).exists():
                
                print("Boleto Gerado", morador.unidade)

            else:
                data_atual = date.today()
                if data_atual.month + 1 > 9:
                    data_do_vencimento = '15/{}/{}'.format( data_atual.month + 1, data_atual.year)+ " 00:00"
                else:
                     data_do_vencimento = '15/0{}/{}'.format( data_atual.month + 1, data_atual.year)+ " 00:00"
                vencimento = datetime.strptime(data_do_vencimento, '%d/%m/%Y %H:%M')
                taxa = Condominios.objects.all().aggregate(total=Sum('valor_total'))['total']
                multa = float(Decimal(taxa) * Decimal(0.02))
                boleto = Boleto.objects.all()
                print("Gerando Boleto", morador.unidade)
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
                    instrucoes= "1- Não receber após 20 dias. 2- Multa de 2,00% = R$ " + str(multa) + " após o vencimento. 3- Taxa diária de permanência de 0,033% a.d.= R$ 0,11/dia"
                    

                        )


        else:
            data_atual = date.today()
            if data_atual.month + 1 > 9:
                data_do_vencimento = '15/{}/{}'.format( data_atual.month + 1, data_atual.year)+ " 00:00"
            else:
                data_do_vencimento = '15/0{}/{}'.format( data_atual.month + 1, data_atual.year)+ " 00:00"
            vencimento = datetime.strptime(data_do_vencimento, '%d/%m/%Y %H:%M')
            taxa = Condominios.objects.all().aggregate(total=Sum('valor_total'))['total']
            multa = float(Decimal(taxa) * Decimal(0.02))
            boleto = Boleto.objects.all()
            print("Gerando Boleto", morador.unidade)
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
                    instrucoes= "1- Não receber após 20 dias. 2- Multa de 2,00% = R$ " + str(multa) + " após o vencimento. 3- Taxa diária de permanência de 0,033% a.d.= R$ 0,11/dia"
                    

                        )
     
        





def calculo_entre_datas(datas, datetime, date, relativedelta):
    for data in datas:        
        data_inicial = str(date.today())+" 23:59:59" 
        data_final = str(data.data_vencimento) +" 23:59:59" 
        f = "%Y-%m-%d %H:%M:%S"
        inicio = datetime.strptime(data_inicial, f)
        fim = datetime.strptime(data_final, f)
        di = abs(relativedelta(inicio, fim))

        return di    