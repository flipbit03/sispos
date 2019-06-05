#!python3
# -*- coding: cp1252 -*-
import os
from .filefinder import findfile, findfilel
from sisposbase.get_sql_data import get_periodo_data, get_periodo_additional_data

INPUTPATH = os.path.join(os.getcwd(), "inputs")
OUTPUTPATH = os.path.join(os.getcwd(), "outputs")
DATAFILEPATH = os.path.join(os.getcwd(), "datafiles")


class BaseSISPOS:
    # FILL THIS IN
    findfiles = []

    inputpath = INPUTPATH
    outputpath = OUTPUTPATH
    datafilepath = DATAFILEPATH
    inputfiles = {}
    outputfiles = {}
    txtlog = []
    canrun = False
    outputfileno = 0

    def getdatafile(self, filename, encoding="windows-1252"):
        fullpath = os.path.join(self.datafilepath, filename)
        if not os.path.isfile(fullpath):
            raise FileNotFoundError(fullpath)

        with open(fullpath, "r", encoding=encoding) as f:
            return f.read()

    # Override me to dynamically add files to findfiles
    def dynfindfiles(self):
        pass  # self.findfiles.append ( (xx,xx) )...

    def __init__(self):
        print("-----------------------------")
        print("Modulo %s" % (self.__class__.__name__))
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
            print("Calculando...")
            retval = self.process(self.inputfiles)
            self.closeall()
            input("\n\n---- Fim do processamento, pressione ENTER ----")
            return retval
        else:
            print(
                "ERRO: O modulo nao pode ser executado pois faltam arquivos de entrada!"
            )
            input("--pressione enter--")
            exit(1)

    def getoutputfile(self, append="", ext="txt", fmode="w"):
        fname = "%s_%s_%d.%s" % (
            self.__class__.__name__,
            append,
            self.outputfileno,
            ext,
        )
        self.outputfileno += 1
        fpath = os.path.join(self.outputpath, fname)

        # open file
        ofile = open(fpath, fmode)

        # insert the reference into a dictionary as well (for closing everything later)
        self.outputfiles[self.outputfileno] = ofile

        return ofile

    def closeall(self):
        for key in self.outputfiles.keys():
            self.outputfiles[key].flush()
            self.outputfiles[key].close()

    def process(self, f):
        ## OVERRIDE THIS FUNCTION TO PROCESS FILES
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
        print(f"\nPeríodo Selecionado --> {f['#MES']}/{f['#ANO']}")

        # Print and save DIASUTEIS
        self.inputfiles["#DIASUTEIS"] = dias_uteis
        print(f"\nDias úteis neste período: {dias_uteis}")

        if dias_1:
            print("")
            print(f"Feriados tipo=1:")
            for l in dias_1:
                print(f"{l[0]} / {l[1]}")
            print("")

        self.inputfiles["#DIAS1"] = dias_1

        if dias_2:
            print(f"Feriados tipo=2:")
            for l in dias_2:
                print(f"{l[0]} / {l[1]}")
        self.inputfiles["#DIAS2"] = dias_2

        print("")

        return periododata

    findfiles = (("#PERIODO", pega_periodo_and_get_data),)

    def process(self, f):
        pass
