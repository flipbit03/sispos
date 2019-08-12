#!python3
# -*- coding: windows-1252 -*-
import os
from datetime import datetime
from io import TextIOWrapper
import re
from sisposbase.sispos import BaseSISPOSSQL

from sisposbase.get_sql_data import getsqldata, sql_substitute_variables

from decimal import Decimal

D = Decimal


class IomoCapac(BaseSISPOSSQL):
    """Calcula o �ndice de Ocupa��o de M�o de Obra (IOMO) e o Capacidade Instalada"""

    def get_data(self, f):

        variables = {
            "PERIODO": f["#PERIODOID"],
            "MESNUM": f["#MES"],
            "ANONUM": f["#ANO"],
        }

        hdisp_sql = getsqldata(
            sql_substitute_variables(
                self.getdatafile("iomo_horasdisponiveis.sql"), variables
            )
        )
        hefet_sql = getsqldata(
            sql_substitute_variables(
                self.getdatafile("iomo_horasefetivas.sql"), variables
            )
        )
        htot_sql = getsqldata(
            sql_substitute_variables(
                self.getdatafile("iomo_horastotais.sql"), variables
            )
        )

        def fixdata(table):
            return [table[0]] + [
                (i[0], i[1], D(i[2].replace(",", "."))) for i in table[1:]
            ]

        return fixdata(hdisp_sql[0]), fixdata(hefet_sql[0]), fixdata(htot_sql[0])

    def process(self, f):

        hdisp, hefet, htot = self.get_data(f)

        # Lista de Setores que Comp�em os Totais
        setores = {
            "IPU": ("IPU", "IPU/C", "IPU/F", "IPU/U"),
            "IPS + IPC": (
                "IPS",
                "IPS/S",
                "IPS/TT",
                "IPC",
                "IPC/M",
                "IPC/T",
                "IPC/C",
                "IPC/MC",
                "IPC/JP",
            ),
            "IQ": ("IQ", "IQI"),
        }

        def depto_index(table, value: str):
            deptotable = [i[1] for i in table]
            if value in deptotable:
                return deptotable.index(value)
            else:
                return None

        def gera_totais_por_setor(table: list):
            soma = {}
            for grupo in setores:
                for setor in setores[grupo]:
                    i = depto_index(table, setor)
                    if i:
                        _, _, horas = table.pop(i)
                        if grupo not in soma:
                            soma[grupo] = {}

                        if setor not in soma[grupo]:
                            soma[grupo][setor] = D("0")

                        soma[grupo][setor] += horas

            return soma

        # Totais Calculados
        hdisp_totais = gera_totais_por_setor(hdisp)
        hefet_totais = gera_totais_por_setor(hefet)
        htot_totais = gera_totais_por_setor(htot)

        #########################
        # Come�a a escrita dos arquivos.
        #########################

        o1 = self.getoutputfile(append=f"�ndices Calculados_{f['#MES']}-{f['#ANO']}")

        o1.write(f"NUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write(f"Ger�ncia Geral de Programa��o e Controle da Produ��o � IC\n\n")
        o1.write(f"C�lculos do:\n")
        o1.write(f"- �ndice de Ocupa��o de M�o de Obra (SGQ)\n")
        o1.write(f"- �ndice da Capacidade Instalada\n\n")
        o1.write("##################\n")
        o1.write(f"Per�odo: {f['#MES']}/{f['#ANO']}\n")
        o1.write("##################\n\n")

        def print_table_totais(title: str, d: dict, o: TextIOWrapper):

            o.write(f"-------------------------------------\n")
            o.write(f"{title}:\n")
            o.write(f"-------------------------------------\n")

            total_geral = D("0")

            for grupo in d:
                total_grupo = D("0")
                o.write(f"[{grupo}]\n")

                for setor in d[grupo]:
                    total_grupo += d[grupo][setor]
                    o.write(f"  {setor:21}{d[grupo][setor]:10.2f}\n")

                total_geral += total_grupo

                o.write("\n")
            o.write(f"  {'total:':>21}{total_geral:10.2f}\n\n")

            return total_geral

        # Horas Efetivas:
        soma_hefet = print_table_totais("Horas Efetivas", hefet_totais, o1)

        # Horas Dispon�veis:
        soma_hdisp = print_table_totais("Horas Disponiveis", hdisp_totais, o1)

        # Horas Totais:
        soma_htot = print_table_totais("Horas Totais", htot_totais, o1)

        # �ndices calculados
        indice_iomo = round((soma_hefet / soma_hdisp) * D("100"), 0)
        indice_capac = round((soma_hefet / soma_htot) * D("100"), 0)

        o1.write(f"-------------------------------------\n\n")

        # Gera os �ndices

        o1.write(f"IOMO {f['#MES']}/{f['#ANO']}\n\n")
        o1.write(f"   IOMO = {'HORAS EFETIVAS':14} / {'HORAS DISPONIVEIS':17}\n")
        o1.write(f"   IOMO = {soma_hefet:^14.2f} / {soma_hdisp:^17.2f}\n")
        o1.write(f"   IOMO = {indice_iomo}%\n\n")

        o1.write(f"CAPACIDADE INSTALADA {f['#MES']}/{f['#ANO']}\n\n")
        o1.write(f"   CAPAC = {'HORAS EFETIVAS':14} / {'HORAS TOTAIS':12}\n")
        o1.write(f"   CAPAC = {soma_hefet:^14.2f} / {soma_htot:^12.2f}\n")
        o1.write(f"   CAPAC = {indice_capac}%\n\n")

        o1.write(f"\nEmitido em: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")

        #####################################
        # Escreve mem�ria de c�lculo.
        #####################################

        o2 = self.getoutputfile(append=f"Mem�ria de C�lculo_{f['#MES']}-{f['#ANO']}")

        o2.write(f"NUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o2.write(f"Ger�ncia Geral de Programa��o e Controle da Produ��o � IC\n\n")
        o2.write(f"Mem�ria de C�lculo do IOMO e CAPACIDADE INSTALADA\n\n")
        o2.write("##################\n")
        o2.write(f"Per�odo: {f['#MES']}/{f['#ANO']}\n")
        o2.write("##################\n\n")

        def print_sobra(table: list, o: TextIOWrapper):
            # skippa o cabe�alho
            o.write("Setores que n�o entraram no c�lculo:\n")
            for item in table[1:]:
                _, depto, hora = item

                o.write(f"{depto:8} - {hora:9.2f}\n")
            o.write("\n\n")

        # Horas Efetivas:
        print_table_totais("Horas Efetivas", hefet_totais, o2)
        print_sobra(hefet, o2)

        # Horas Dispon�veis:
        print_table_totais("Horas Disponiveis", hdisp_totais, o2)
        print_sobra(hdisp, o2)

        # Horas Totais:
        print_table_totais("Horas Totais", htot_totais, o2)
        print_sobra(htot, o2)


