#!python2
# -*- coding: cp1252 -*-
import os
import re
import datetime
from decimal import Decimal

from sisposbase.sispos import BaseSISPOS

import sys
import copy
import datetime


class CrimesHH(BaseSISPOS):
    findfiles = ( ("CRIMES","CRIMESHH"),
                  ("#MES","Mes (FORMATO: MM)"),
                  ("#ANO","Data Final (FORMATO: AAAA)"),
                  ("##dias1", "Dias Tipo=1 (Sabado ou Dias emendados, FORMATO: DD/MM/AAAA[,...])"),
                  ("##dias2", "Dias Tipo=2 (Domingo ou Feriados)")
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

            # pula a primeira linha pois ela e o cabecalho, no sistema novo.
            for _linha in arquivoexterno.strip().split('\n')[1:]:

                matr, turno, data, htipo, _ign, minutos, _ign = _linha.strip().split('|')

                matr = int(matr)
                turno = int(turno)
                htipo = int(float(htipo))
                minutos = int(minutos)

                # Convert data as obj
                data_obj = datetime.datetime.strptime(data, r"%d/%m/%y")

                if not arm.has_key(matr):
                    arm[matr] = {}

                if data_obj not in arm[matr].keys():
                    arm[matr][data_obj] = []

                arm[matr][data_obj].append([turno, htipo, minutos])

            return arm


     # Lancamento

        def julga(dateobj, evento):

            #dateobj = datetime.date(int(ano), int(mes), int(dia))
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
            _turno, _htipo, _minutos = evento


            ## Se TURNO=4 (21h) Regra especial.
            # 1260 minutos = 21 horas
            if _turno == 4 and _htipo == 3 and _minutos != 21*60:
                return True

            if _turno == 4 and _htipo != 3:
                return True

            ## Dias
            if tipohora in (0,):

                if _htipo == 0 and _turno == 1:
                    # 8h
                    if _minutos != 8*60:
                        return True

                if _htipo == 0 and _turno == 2:
                    # 7h 37min
                    if _minutos != (7*60+37):
                        return True

                if _htipo == 0 and _turno == 3:
                    # 7h 15min
                    if _minutos != (7*60+15):
                        return True

                if _htipo == 1 and _turno == 1:
                    # 2 horas extras
                    if _minutos > 2*60:
                        return True

                if _htipo == 1 and _turno == 2:
                    # 2 horas extras
                    if _minutos > 2*60:
                        return True

                if _htipo == 1 and _turno == 3:
                    # 2 horas extras
                    if _minutos > 2*60:
                        return True

                if _htipo == 2:
                        return True

            ## Dia de Feriado Emendado ("Feriado 50%")
            if tipohora in (1,):

                if _htipo in (0, 2):
                    return True

                # 8h
                if _htipo == 1 and _turno == 1 and _minutos > 8*60:
                        return True

                # 7h37m
                if _htipo == 1 and _turno == 2 and _minutos > (7*60+37):
                        return True

                # 7h15m
                if _htipo == 1 and _turno == 3 and _minutos > (7*60+15):
                        return True


            ## Dia de Feriado Real ("Feriado 100%")
            if tipohora in (2,):

                if _htipo in (0, 1):
                    return True

                # 8h
                if _htipo == 2 and _turno == 1 and _minutos > 8*60:
                        return True

                # 7h37m
                if _htipo == 2 and _turno == 2 and _minutos > (7*60+37):
                        return True

                # 7h15m
                if _htipo == 2 and _turno == 3 and _minutos > (7*60+15):
                        return True

        def julgalinhas(levents):

            leventscopy = copy.deepcopy(levents)

            if len(levents) == 1:
                return False
            elif len(levents) > 3:
                return True

            trabadm = False

            adm8h = [1,0,8*60]
            pedegalinha_adm2h = [1,1,2*60]
            pedegalinha_adm1h = [1,1,1*60]

            if ((adm8h in leventscopy) and (pedegalinha_adm2h in leventscopy) or
                (adm8h in leventscopy) and (pedegalinha_adm1h in leventscopy)):
                return False
            else:
                return True

        arm = cria_bancodedados(f['CRIMES'])

        # Cria dias_1 e dias_2
        def faz_dias(datastr):
            if not datastr.strip():
                return None
            try:
                return datetime.datetime.strptime(datastr, "%d/%m/%Y")
            except:
                print "erro convertendo linha --> \"{}\"".format(datastr)

        dias_1 = [faz_dias(i) for i in f['##dias1'].split(',') if f['##dias1']]
        dias_2 = [faz_dias(i) for i in f['##dias2'].split(',') if f['##dias2']]

        # Processamento
        for _matr in arm.keys():
            for _data in arm[_matr].keys():
                # Dia da Semana
                #dia, mes, ano = _data.strip().split(r'/')

                #dateobj = datetime.strptime(_data, r"%d/%m/%Y %H:%M:%S")
                #dateobj = datetime.date(int(ano), int(mes), int(dia))

                weekday = _data.weekday()

                for evento in arm[_matr][_data]:
                    #print evento
                    if julga(_data, evento):

                        feriado = ""
                        if _data in dias_1:
                            feriado = "Feriado 50%"
                        elif _data in dias_2:
                            feriado = "Feriado 100%"

                        _datas = "{}/{}/{}".format(_data.day, _data.month, _data.year)
                        o1.write("[%s] [%s] [%s] %s\n" % (_matr, _datas, wkdays[weekday], feriado))
                        o1.write("%s%s%s\n" % ('turno'.ljust(7), 'htipo'.ljust(7),'hora'.ljust(7)))
                        entrada = evento
                        et, eht, emin = evento
                        ehoras = "{0:02}:{1:02}".format(emin//60, emin%60)
                        o1.write("%s%s%s (%s min)\n" % (str(et).ljust(7), str(eht).ljust(7), str(ehoras).ljust(7), emin))
                        o1.write('\n')

                        #raw_input("ERRO DETECTADO")

                if julgalinhas(arm[_matr][_data]):
                    _datas = "{}/{}/{}".format(_data.day, _data.month, _data.year)
                    o1.write("[%s] [%s] [%s]\n" % (_matr, _datas, wkdays[weekday]))
                    o1.write("%s%s%s\n" % ('turno'.ljust(7), 'htipo'.ljust(7),'hora'.ljust(7)))
                    for entrada in arm[_matr][_data]:
                        et, eht, emin = entrada
                        ehoras = "{0:02}:{1:02}".format(emin // 60, emin % 60)
                        o1.write(
                            "%s%s%s (%s min)\n" % (str(et).ljust(7), str(eht).ljust(7), str(ehoras).ljust(7), emin))
                    o1.write('\n')

if __name__ == "__main__":
    a = CrimesHH()
    a.run()
