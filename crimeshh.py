 # -*- coding: cp1252 -*-
import os
import re
import datetime
from decimal import Decimal

from sisposbase.sispos import BaseSISPOS


import sys
import copy
import datetime

# ####
# #dias_1 = ()
#
# dias_1 = ("23/12/2015", "24/12/2015", "28/12/2015", "29/12/2015", "30/12/2015", "31/12/2015")
# dias_2 = ("25/12/2015", "01/01/2016")
#
# #dias_2 = ()
# ####
#
# d = None
#
# with open(sys.argv[1]) as f:
#     d = f.readlines()
#
#
#  arm = cria_bancodedados(d)
#  # Julgamento
#
# wkdays = {}
# wkdays[0] = "Segunda-Feira"
# wkdays[1] = "Terca-Feira"
# wkdays[2] = "Quarta-Feira"
# wkdays[3] = "Quinta-Feira"
# wkdays[4] = "Sexta-Feira"
# wkdays[5] = "Sabado"
# wkdays[6] = "Domingo"
#

class CrimesHH(BaseSISPOS):
    findfiles = ( ("CRIMESHH","CRIMESHH"),
                  ("#MES","Mes (FORMATO: MM)"),
                  ("#ANO","Data Final (FORMATO: AAAA)"),
                  ("#dias1", "Dias Tipo=1 (Sabado ou Dias emendados, FORMATO: DD/MM/AAAA[,...])"),
                  ("#dias2", "Dias Tipo=2 (Domingo ou Feriados)")
                  )
                 
    def splithh(self, arq):
    
        arqs = [l.strip().split('|') for l in arq.strip().split('\n')]
        
        arqsp = [[int(x[0]), int(x[1]), x[2], int(x[3]), Decimal(x[4])] for x in arqs]
        
        from code import interact
        interact(local=locals())
        
        #arqs_conv = [(int(matr), int(
        
        #for matr, turno, predata, htipo, horas, ign in arqs:
        #    print matr, turno, predata, htipo, horas
        

    def process (self, f):

        o1 = self.getoutputfile(ext='txt', append='%s-%s' % (f['#MES'], f['#ANO']))

        wkdays = {}
        wkdays[0] = "Segunda-Feira"
        wkdays[1] = "Terca-Feira"
        wkdays[2] = "Quarta-Feira"
        wkdays[3] = "Quinta-Feira"
        wkdays[4] = "Sexta-Feira"
        wkdays[5] = "Sabado"
        wkdays[6] = "Domingo"

        def cria_bancodedados(arquivoexterno):

            arm = {}

            for _linha in arquivoexterno.strip().split('\n'):

                matr, turno, data, htipo, hora, _ign = _linha.strip().split('|')

                matr = int(matr)
                turno = int(turno)
                htipo = int(float(htipo))
                hora = float(hora)

                if not arm.has_key(matr):
                    arm[matr] = {}

                if data not in arm[matr].keys():
                    arm[matr][data] = []

                arm[matr][data].append([turno, htipo, hora])

            return arm


     # Lancamento

        def julga(_data, evento):
            dia, mes, ano = _data.strip().split(r'/')
            dateobj = datetime.date(int(ano), int(mes), int(dia))
            weekday = dateobj.weekday()

            erro = False

            ## Tipo Hora
            tipohora = "?"
            if weekday in (0,1,2,3,4):
                tipohora = 0
            elif weekday in (5,):
                tipohora = 1
            elif weekday in (6,):
                tipohora = 2
            if _data in dias_1:
                #print "%s eh dia 1" % (_data,)
                tipohora = 1
            if _data in dias_2:
                tipohora = 2


            ## Separa informacoes do evento
            _turno, _htipo, _hora = evento


            ## Se TURNO=4 (24h) Regra especial.
            if _turno == 4 and _htipo == 3 and _hora != 24:
                return True

            if _turno == 4 and _htipo != 3:
                return True

            ## Dias
            if tipohora in (0,):

                if _htipo == 0 and _turno == 1:
                    if _hora != 8:
                        return True

                if _htipo == 0 and _turno == 2:
                    if _hora != 7.42:
                        return True

                if _htipo == 0 and _turno == 3:
                    if _hora != 6.08:
                        return True

                if _htipo == 1 and _turno == 1:
                    if _hora > 2:
                        return True

                if _htipo == 1 and _turno == 2:
                    if _hora > 2:
                        return True

                if _htipo == 1 and _turno == 3:
                    if _hora > 2:
                        return True

                if _htipo == 2:
                        return True

            ## Dia de Feriado Emendado ("Feriado 50%")
            if tipohora in (1,):

                if _htipo in (0, 2):
                    return True

                if _htipo == 1 and _turno == 1 and _hora > 8:
                        return True

                if _htipo == 1 and _turno == 2 and _hora > 7.42:
                        return True

                if _htipo == 1 and _turno == 3 and _hora > 6.08:
                        return True


            ## Dia de Feriado Real ("Feriado 100%")
            if tipohora in (2,):

                if _htipo in (0, 1):
                    return True

                if _htipo == 2 and _turno == 1 and _hora > 8:
                        return True

                if _htipo == 2 and _turno == 2 and _hora > 7.42:
                        return True

                if _htipo == 2 and _turno == 3 and _hora > 6.08:
                        return True

            #from code import interact; interact(local=locals())

            #raw_input()

        def julgalinhas(levents):

            leventscopy = copy.deepcopy(levents)

            if len(levents) == 1:
                return False
            elif len(levents) > 3:
                return True

            trabadm = False

            adm8h = [1,0,8]
            pedegalinha = [1,1,2]

            if (adm8h in leventscopy) and (pedegalinha in leventscopy):
                return False
            else:
                return True

        arm = cria_bancodedados(f['CRIMESHH'])

        # Cria dias_1 e dias_2
        dias_1 = [i.strip() for i in f['#dias1'].split(',')]
        dias_2 = [i.strip() for i in f['#dias2'].split(',')]

        # Processamento
        for _matr in arm.keys():
            for _data in arm[_matr].keys():
                # Dia da Semana
                dia, mes, ano = _data.strip().split(r'/')
                dateobj = datetime.date(int(ano), int(mes), int(dia))
                weekday = dateobj.weekday()

                for evento in arm[_matr][_data]:
                    #print evento
                    if julga(_data, evento):

                        feriado = ""
                        if _data in dias_1:
                            feriado = "Feriado 50%"
                        elif _data in dias_2:
                            feriado = "Feriado 100%"

                        o1.write("[%s] [%s] [%s] %s\r\n" % (_matr, _data, wkdays[weekday], feriado))
                        o1.write("%s%s%s\r\n" % ('turno'.ljust(7), 'htipo'.ljust(7),'hora'.ljust(7)))
                        entrada = evento
                        o1.write("%s%s%s\r\n" % (str(entrada[0]).ljust(7), str(entrada[1]).ljust(7), str(entrada[2]).ljust(7)))
                        o1.write('\r\n')

                        #raw_input("ERRO DETECTADO")

                if julgalinhas(arm[_matr][_data]):
                    o1.write("[%s] [%s] [%s]\r\n" % (_matr, _data, wkdays[weekday]))
                    o1.write("%s%s%s\r\n" % ('turno'.ljust(7), 'htipo'.ljust(7),'hora'.ljust(7)))
                    for entrada in arm[_matr][_data]:
                        o1.write("%s%s%s\r\n" %
                                 (str(entrada[0]).ljust(7), str(entrada[1]).ljust(7), str(entrada[2]).ljust(7)))
                    o1.write('\r\n')


a = CrimesHH()
a.run()
