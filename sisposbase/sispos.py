# -*- coding: cp1252 -*-
import os
from filefinder import findfile, findfilel

INPUTPATH = os.path.join(os.getcwdu(), "inputs")
OUTPUTPATH = os.path.join(os.getcwdu(), "outputs")

class BaseSISPOS:
    #FILL THIS IN
    findfiles = []
    
    inputpath = INPUTPATH
    outputpath = OUTPUTPATH
    inputfiles = {}
    outputfiles = {}
    txtlog = []
    canrun = False
    outputfileno = 0

    # Override me to dynamically add files to findfiles 
    def dynfindfiles(self):
        pass #self.findfiles.append ( (xx,xx) )...
    
    def __init__(self):
        print "-----------------------------"
        print "SISPOS - Modulo %s" % (self.__class__.__name__)
        print "-----------------------------"
        print ""

        # Call this function to populate dynamically self.findfiles
        self.dynfindfiles()
        
        if self.findfiles:
            # Arquivos
            files = [b for b in self.findfiles if not b[0][0] == '#']
            print "Precisamos de %d arquivo(s)...\n" % (len(files))
            for entry in files:
                fname, freg = entry
                outfname, outdata = findfilel(self.inputpath, fname, freg)
                if outfname and outdata:
                    if fname[0] == "!":
                        self.inputfiles[fname] = outfname
                    else:
                        self.inputfiles[fname] = outdata
                print ""

            # Perguntas
            questions = [b for b in self.findfiles if b[0][0] == '#']
            print "Precisamos fazer %d pergunta(s)...\n" % (len(questions))
            for entry in questions:
                fname, fquestionprompt = entry
                outdata = raw_input(fquestionprompt+" ? ")
                if outdata:
                    self.inputfiles[fname] = outdata
                print ""

            # Garantir que temos tudo que precisamos
            try:
                for f in [z[0] for z in self.findfiles]:
                    a = self.inputfiles[f]
                self.canrun = True
            except:
                self.canrun = False

        else:
            print "Sem arquivos de entrada"

    def run(self):
        if self.canrun:
            retval = self.process(self.inputfiles)
            self.closeall()
            raw_input("\n\n---- Fim do processamento, pressione ENTER ----")
            return retval
        else:
            print "ERRO: O modulo nao pode ser executado pois faltam arquivos de entrada!"
            raw_input("--pressione enter--")
            exit(1)

    def getoutputfile(self, append='', ext="txt", fmode='w'):
        fname = "%s_%s_%d.%s" % (self.__class__.__name__, append, self.outputfileno, ext)
        self.outputfileno += 1
        fpath = os.path.join(self.outputpath, fname)

        #open file
        ofile = open(fpath, fmode)

        #insert the reference into a dictionary as well (for closing everything later)
        self.outputfiles[self.outputfileno] = ofile

        return ofile

    def closeall(self):
        for key in self.outputfiles.keys():
            self.outputfiles[key].flush()
            self.outputfiles[key].close()

    def process (self, f):
        ## OVERRIDE THIS FUNCTION TO PROCESS FILES
        print "\n-------------------"
        print "process():"
        print "I found %d file(s)" % (len(f))
        print "Override me so i can do something..."
        print "-------------------\n"


