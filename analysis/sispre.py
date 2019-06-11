# -*- coding: windows-1252 -*-
import json
import os
import re
import datetime
import shutil

from sisposbase.sispos import BaseSISPOSSQL, DATAFILEPATH, TOOLFOLDER

SISPRE_SCRIPTPATH = os.path.join(DATAFILEPATH, "sispre_scripts")
SISPRE_SQL = os.path.join(DATAFILEPATH, "sispre_sql")

mes_abreviado = (
    "JAN",
    "FEV",
    "MAR",
    "ABR",
    "MAI",
    "JUN",
    "JUL",
    "AGO",
    "SET",
    "OUT",
    "NOV",
    "DEZ",
)

sqlexecutorname = "SingleSQLExecutor.exe"


class Sispre(BaseSISPOSSQL):
    """Executa relatórios em Lotes para posterior análise"""

    def le_nome_do_script(self):
        print("Lotes disponíveis:")
        # Lista todos os arquivos finalizados em .json
        for fname in [
            x for x in os.listdir(SISPRE_SCRIPTPATH) if re.search("json$", x)
        ]:
            ln = os.path.splitext(fname)[0]
            print(f"  - {ln}")
        print("")

        scriptfolder = SISPRE_SCRIPTPATH
        chosenscriptname = input("DIGITE O NOME DO LOTE A SER EXECUTADO --> ")
        scriptfilename = chosenscriptname + ".json"
        scriptfilename = os.path.join(scriptfolder, scriptfilename)

        if os.path.isfile(scriptfilename):
            print("Confirmado.")
            with open(scriptfilename, "r", encoding="windows-1252") as fh:
                scriptdata = fh.read()
        else:
            print("Erro: Script nao existe. Saindo...")
            exit(0)

        # Convert script data to from json->DICT
        self.inputfiles["#SCRIPTDATA"] = json.loads(scriptdata, encoding="windows-1252")

        return chosenscriptname

    findfiles = (
        ("#PERIODO", BaseSISPOSSQL.pega_periodo_and_get_data),
        ("#SCRIPTNAME", le_nome_do_script),
    )

    ## --- SUBST and SVARS2 (Dynamic variables)
    @staticmethod
    def subst(data, vd, d="@@"):
        rv = data
        for k in vd.keys():
            rv = rv.replace(d + str(k) + d, str(vd[k]))
        return rv

    def cria_variaveis_subst(self):
        svar = {}

        # id do periodo
        svar["PERIODO"] = self.inputfiles["#PERIODOID"]

        # nome do script
        svar["SCRIPTNAME"] = self.inputfiles["#SCRIPTNAME"]

        # mes e ano que estão sendo executados
        svar["MESNUM"] = self.inputfiles["#MES"]
        svar["MESABREV"] = mes_abreviado[int(svar["MESNUM"]) - 1]

        svar["ANONUM"] = self.inputfiles["#ANO"]

        # data inicial / final do periodo
        svar["DTINI"] = self.inputfiles["#DTINI"]
        svar["DTFIM"] = self.inputfiles["#DTFIM"]

        return svar

    def process(self, f):

        # Cria variáveis a serem substituidas nos relatórios sql
        svars = self.cria_variaveis_subst()

        script = f["#SCRIPTDATA"]
        scriptname = f["#SCRIPTNAME"]

        # Get Output Folder.
        outputfolder = self.getoutputfolder(append=f"{scriptname}_{f['#MES']}-{f['#ANO']}")

        # copy sqlexecutor to outputfolder.
        sqlexecutorpath = os.path.join(TOOLFOLDER, sqlexecutorname)
        if not os.path.isfile(sqlexecutorpath):
            raise Exception(f"Erro Fatal: {sqlexecutorpath} não foi encontrado.")
        else:
            shutil.copyfile(
                sqlexecutorpath, os.path.join(outputfolder, sqlexecutorname)
            )

        def openfile(fn, c="windows-1252"):
            return self.getoutputfile(inside=outputfolder, override_name=fn, encoding=c)

        # Cria arquivo de execução:
        rfo = openfile("_executa.bat", c="cp850")
        # Cria arquivo de execucao
        rf = [
            "@echo off",
            f"rem ####################################",
            f"rem Script gerado automaticamente em {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}",
            f"rem ####################################",
            f"",
            f"echo --------------------------",
            f"echo SISPRE: Executando SCRIPT {scriptname}...",
            f"echo --------------------------",
            f"echo.",
            f"echo Criando pasta OUT...",
            f"md out",
            f"echo.",
            f"",
        ]

        # Itera o script, preenchendo os arquivos SQL.
        for reportfilename, n in zip(script, range(1, len(script)+1)):

            # Prepara nome de saida deste relatorio.
            reportoutputfilename_base = script[reportfilename]
            reportoutputfilename = self.subst(reportoutputfilename_base, svars)
            reportoutputfilename = reportoutputfilename + ".txt"

            # Carrega conteudo do SQL
            try:
                reportfiledata = self.getdatafile(reportfilename, inside=SISPRE_SQL)
                print(f" [ok ] - {reportfilename} --> {reportoutputfilename}")
            except FileNotFoundError:
                print(f" [ign] - {reportfilename} não foi encontrado. ignorando...")
                continue

            # Preenche as variaveis no conteudo do relatorio
            reportfiledata_s = self.subst(reportfiledata, svars)

            # Escreve o relatório modificado em um arquivo.
            reportf = openfile(reportfilename)
            reportf.write(reportfiledata_s)

            # Escreve a linha que executará o relatório.
            rf.append(
                f"{sqlexecutorname} {reportfilename} {os.path.join('out', reportoutputfilename)}"
            )
            rf.append(f"echo [ {n}/{len(script)} {(n/len(script))*100:.1f}%% ]")
            rf.append(f"echo.")
            rf.append(f"echo.")

        # Escreve final do arquivo que executa tudo.
        rf.append("echo.")
        rf.append("echo ------------------------------------------------")
        rf.append("echo Lote de relatórios executado com sucesso!")
        rf.append("echo Abra a subpasta out/ para buscar os arquivos.")
        rf.append("echo ------------------------------------------------")
        rf.append("echo.")
        rf.append("pause")

        # Write runfile out.
        rfo.write("\n".join(rf))

        print("")