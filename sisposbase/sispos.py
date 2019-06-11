#!python3
# -*- coding: cp1252 -*-
import datetime
import os
import re
import json
from .filefinder import findfile, findfilel
from sisposbase.get_sql_data import get_periodo_data, get_periodo_additional_data

BASEPATH = os.getcwd()

INPUTPATH = os.path.join(BASEPATH, "inputs")
OUTPUTPATH = os.path.join(BASEPATH, "outputs")

DATAFILEPATH = os.path.join(BASEPATH, "datafiles")
TOOLFOLDER = os.path.join(BASEPATH, "tools")

# Crie paths de INPUT e OUTPUT se eles não existirem.
create_if_nonexistent = (INPUTPATH, OUTPUTPATH)
[os.mkdir(x) for x in create_if_nonexistent if not os.path.exists(x)]


class BaseSISPOS:
    # FILL THIS IN
    findfiles = []

    inputpath = INPUTPATH
    outputpath = OUTPUTPATH
    datafilepath = DATAFILEPATH

    inputfiles = {}

    outputfiles = {}
    outputfileno = 0

    txtlog = []
    canrun = False

    def getdatafile(self, filename, encoding="windows-1252", inside=""):
        fullpath = os.path.join(inside if inside else self.datafilepath, filename)
        if not os.path.isfile(fullpath):
            raise FileNotFoundError(fullpath)

        with open(fullpath, "r", encoding=encoding) as f:
            return f.read()

    # Override me to dynamically add files to findfiles
    def dynfindfiles(self):
        pass  # self.findfiles.append ( (xx,xx) )...

    def __init__(self):
        print("-----------------------------")
        print(f"Modulo {self.__class__.__name__}")
        print("-----------------------------")
        print("")

        # Call this function to populate dynamically self.findfiles
        self.dynfindfiles()

        if self.findfiles:
            # Arquivos
            files = [_f for _f in self.findfiles if not _f[0][0] == "#"]
            print("Precisamos de %d arquivo(s)...\n" % len(files))
            for entry in files:
                fname, freg = entry
                outfname, outdata = findfilel(self.inputpath, fname, freg)
                if outfname and outdata:
                    if fname[0] == "!":
                        self.inputfiles[fname] = outfname
                    else:
                        self.inputfiles[fname] = outdata
                print("")

            # Perguntas
            questions = [_q for _q in self.findfiles if _q[0][0] == "#"]
            print("Precisamos fazer %d pergunta(s)...\n" % (len(questions)))
            for entry in questions:
                fname, fquestionprompt = entry

                if callable(fquestionprompt):
                    # Instead of asking the question, call the method to fill the data.
                    self.inputfiles[fname] = fquestionprompt(self)

                else:
                    # Ask question
                    outdata = input(fquestionprompt + " ? ")
                    if outdata:
                        self.inputfiles[fname] = outdata
                    elif fname[1] == "#":
                        print("Pergunta opcional, deixada em branco [ok].")
                        self.inputfiles[fname] = ""
                print("")

            # Garantir que temos tudo que precisamos
            try:
                for f in [z[0] for z in self.findfiles]:
                    a = self.inputfiles[f]
                self.canrun = True
            except:
                self.canrun = False

        else:
            print("Sem arquivos de entrada")

    def run(self):
        if self.canrun:
            print("Calculando...\n")
            retval = self.process(self.inputfiles)

            # Fecha todos os arquivos que foram gerados e reporta em tela.
            self.closeall_and_report_files()
            input(
                "\n---- Fim do processamento, pressione ENTER para finalizar o programa ----"
            )
            return retval
        else:
            print(
                "ERRO: O modulo nao pode ser executado pois faltam arquivos de entrada!"
            )
            input("--pressione enter--")
            exit(1)

    def getoutputfile(
        self, append="", ext="txt", fmode="w", inside="", override_name="", encoding="windows-1252"
    ):
        fname = "%s_%s_%d.%s" % (
            self.__class__.__name__,
            append,
            self.outputfileno,
            ext,
        )

        self.outputfileno += 1
        fpath = os.path.join(
            inside if inside else self.outputpath,
            override_name if override_name else fname,
        )

        # open file
        ofile = open(fpath, fmode, encoding=encoding)

        # insert the reference into a dictionary as well (for closing everything later)
        self.outputfiles[self.outputfileno] = ofile

        return ofile

    def getoutputfolder(self, append=""):
        if self.outputpath != OUTPUTPATH:
            raise Exception("A função getoutputfolder() só deve ser chamada UMA vez")

        nowstr = datetime.datetime.now().strftime("%S")

        newpath = f"{self.__class__.__name__.lower()}_{append}__{nowstr}"
        newpath_out = os.path.join(OUTPUTPATH, newpath)

        # Cria
        os.mkdir(newpath_out)

        # Substitui o outputpath para o novo
        self.outputpath = newpath_out

        return newpath_out

    def closeall_and_report_files(self):
        if self.outputfiles.keys():
            print("##############################################################")
            print(f"Análise {self.__class__.__name__} executada com sucesso.")
            print("##############################################################\n")

            print(f"Esta análise gerou {len(self.outputfiles)} arquivo(s):\n")
            for key in self.outputfiles.keys():
                fobj = self.outputfiles[key]
                print(f"  {key} - {os.path.basename(fobj.name)}")
                fobj.flush()
                fobj.close()

            print("\nOs arquivos estão disponíveis na seguinte pasta:")
            print(f"\n  {self.outputpath}")
            print("\n##############################################################")

    def process(self, f):
        # OVERRIDE THIS FUNCTION TO PROCESS FILES
        print("\n-------------------")
        print("process():")
        print("I found %d file(s)" % (len(f)))
        print("Override me so i can do something...")
        print("-------------------\n")


class BaseSISPOSSQL(BaseSISPOS):
    def pega_periodo_and_get_data(self):
        periodoid, mes, ano, fechadoem, dtini, dtfim = periododata = get_periodo_data()

        f = self.inputfiles

        self.inputfiles["#PERIODOID"] = periodoid
        self.inputfiles["#MES"] = mes
        self.inputfiles["#ANO"] = ano
        self.inputfiles["#DTINI"] = dtini
        self.inputfiles["#DTFIM"] = dtfim

        # Com o período escolhido, pega parametros adicionais.
        dias_uteis, dias_1, dias_2 = get_periodo_additional_data(periodoid)

        # Print chosen Period
        print(f"\nPERÍODO SELECIONADO --> {f['#MES']}/{f['#ANO']}")

        # Print and save DIASUTEIS
        self.inputfiles["#DIASUTEIS"] = dias_uteis
        print(f"\nDIAS ÚTEIS NESTE PERÍODO --> {dias_uteis}")

        def lista_feriados(diasvar, tipodia):
            if diasvar:
                print("")
                print(f"FERIADOS TIPO={tipodia}:")
                for dia in diasvar:
                    print(f"  {dia[0].strftime('%d/%m/%Y')} / {dia[1]}")

        self.inputfiles["#DIAS1"] = dias_1
        lista_feriados(dias_1, 1)

        self.inputfiles["#DIAS2"] = dias_2
        lista_feriados(dias_2, 2)

        print("")

        return periododata

    findfiles = (("#PERIODO", pega_periodo_and_get_data),)

    def process(self, f):
        pass
