# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS

class HTipo0G(BaseSISPOS):
    # ----------------------------------
    # Initalization parameters
    # ----------------------------------

    findfiles = [ ('#MES', "Digite o mes atual MM"),
                  ('#ANO', "Digite o ano atual AAAA") ]

    def dynfindfiles(self):
        mainfile = ( self.__class__.__name__.upper(), self.__class__.__name__.lower() )
        self.findfiles.append(mainfile)

    # ----------------------------------
    # Data
    # ----------------------------------

    # CSS used for formatting the HTML file.
    inlinecss = \
"""
.ignoredhour
{
color: LightSteelBlue;
}

.unknownhour
{
color: LightSteelBlue;
background-color: red;
}

.normalhour
{
}

.hiliteativ
{
    color: Red;
    font-weight: bold;
}

.totalcargo
{
    font-size: small ;
    font-weight: bold ;
    font-style: italic ;
}

.totalos
{
    font-weight: bold ;
    font-style: italic ;
}
"""
    # EXCEPTIONS - Client renames based on codped/cliente
    
    renclientdata = (
    # NEW NAME, Curr Client Name, Codped
    ('ELETRO-MENOS','ELETRONUCLEAR', 
    ('040200000', '831100000', '040230000', '220000000','830220000','340070000')),
    
    ('ELETRO-MAIS','ELETRONUCLEAR', 
    ('140000000','835520000','830140000')),
    
    ('ELETRO-PONTO1','ELETRONUCLEAR', 
    ('350000000')),
    
    ('ELETRO-PONTO2','ELETRONUCLEAR', 
    ('360000000')),
    
    ('ELETRO-PONTO3','ELETRONUCLEAR', 
    ('260040000'))
    
    )


    # "Cargo" categories:
    catCALD = "Caldeireiro"
    catSOLD = "Soldador"
    catESME = "Esmerilhador"
    catMACA = "Macariqueiro"
    catTRAC = "Tracador"
    catAJUS = "Ajustador Mecanico"
    catFRES = "Fresador"
    catFORN = "Tratamento Termico"
    catMQSP = "Op. Maquina Especializado"
    catTORN = "Torneiro Mecanico"
    catCALA = "Op. Calandra"
    catUNK  = "DESCONHECIDO"   # Unknown hours because of missing rules, programmer should check these.

    # Work categories, ordered:
    catsORD = ( catCALD, catSOLD, catESME, catMACA, catTRAC, catAJUS, catFRES, 
                catFORN, catMQSP, catTORN, catCALA, catUNK )
                
                
    # STRING x "Cargo" mapping
    
    strcargomap = {
        ('CALDEIREIRO', 'CALDEIREIRO ESP') : catCALD,
        ('SOLDADOR',) : catSOLD,
        ('OP.ESMER.',) : catESME,
        ('MACARIQUE',) : catMACA,
        ('TRACADOR',) : catTRAC,
        ('AJUST.MEC',) : catAJUS,
        ('FRESADOR',) : catFRES,
        ('OP.T.TERM',) : catFORN,
        ('OP.MAQ.ESPECIALI',) : catMQSP,
        ('TORN.MEC.',) : catTORN,
        ('OP.CALAND','OP.CALAND.') : catCALA
        }

    # ----------------------------------
    # Code
    # ----------------------------------

    # Dict used to store OS judgement data
    jdata = {}

    
    def judgecliente(self, line):
        ## fields: codped || cliente || cargo || htipo || tothora || <ignored>
        # Get main variables
        codped, cliente, cargo, htipo, tothora, ign = line
        
        # Try to fetch a line from self.renclientdata
        newnamecand = [x[0] for x in self.renclientdata if x[1] == cliente and codped in x[2]]
        
        if newnamecand:
            return newnamecand[0]
        else:
            return cliente
            
    def judgecargo(self, line):
        ## fields: codped || cliente || cargo || htipo || tothora || <ignored>
                
        # Get main variables
        codped, cliente, cargo, htipo, tothora, ign = line
        
        
        # Return a 'cargo' category if found
        for key in self.strcargomap.keys():
            if cargo in key:
                return self.strcargomap[key]
                

        # Return catUNK if not found, signalling that rules should be revised.
        return self.catUNK
        

    def processjdata(self, line):
        ## fields: codped || cliente || cargo || htipo || tothora || <ignored>
        # Get main variables
        codped, cliente, cargo, htipo, tothora, ign = line
        
        aliasedcliente = self.judgecliente(line)
        cargocat = self.judgecargo(line)
        
        if not self.jdata.has_key(aliasedcliente):
            self.jdata[aliasedcliente] = {}
            
        if not self.jdata[aliasedcliente].has_key(cargocat):
            self.jdata[aliasedcliente][cargocat] = 0
            
        #sum tothora to the appropriate category inside its client    
        self.jdata[aliasedcliente][cargocat] += float(tothora)
        
        self.jdata[aliasedcliente][cargocat] = round(self.jdata[aliasedcliente][cargocat], 2)
        
    def process (self, f):
        # strip carriage returns
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].strip()
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].replace('\r','')

        # split lines and split each line to a tuple
        # fields: codped || cliente || cargo || htipo || tothora || <ignored>
        fs = [x.split('|') for x in f[self.__class__.__name__.upper()].split('\n')]

        
        # Get output file for HTML
        #o1 = self.getoutputfile(ext='html', append='%s-%s' % (f['#MES'], f['#ANO']))
        # Get output file for CSV
        #o2 = self.getoutputfile(ext='csv', append='%s-%s-excel' % (f['#MES'], f['#ANO']))
        
        for l in fs:
            self.processjdata(l)
            print l, self.judgecliente(l), self.judgecargo(l)

        return self.jdata

if __name__ == "__main__":
    a = HTipo0G()
    r = a.run()
