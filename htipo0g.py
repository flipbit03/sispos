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

.groupedhour
{
color: blue;
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
    ('350000000',)),
    
    ('ELETRO-PONTO2','ELETRONUCLEAR', 
    ('360000000',)),
    
    ('ELETRO-PONTO3','ELETRONUCLEAR', 
    ('260040000',))
    
    )

    # --------------------------------------------------------------
    # "Cargo" categories:
    # --------------------------------------------------------------
    
    # Factory - Lower Class
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
    catDESE = "Desempenador"
    
    # Technical - Medium Class
    catARQT = "Arquivista Tecnico"
    catASSE = "Assistente Especializado"
    catDESN = "Desenhista"
    catDESP = "Desenhista Projetista"
    catENGO = "Engenheiro"
    catINSQ = "Inspetor de Cont. Qualidade"
    catPROJ = "Projetista"
    catTMET = "Tecnico de Met. e Processos"
    catTPLA = "Tecnico de Planejamento"
    catTCQU = "Tecnico de Cont. da Qualidade"
    catTELC = "Tecnico em Eletricidade"
    catTELE = "Tecnico em Eletronica"
    catTINF = "Tecnico de Informatica"
    catTMEC = "Tecnico em Mecanica"
    catMMAN = "Tecnico em Mec. de Manutencao"
    catTMEQ = "Tecnico em Mec. do Cont. Qualidade"
    catTIND = "Tecnico Industrial"
    catTELM = "Tecnico em Eletromecanica"
    
    # Unknown
    catUNK  = "DESCONHECIDO"   # Unknown hours because of missing rules, programmer should check these.

    # Work categories, ordered:
    catsORD1 = ( catCALD, catSOLD, catESME, catMACA, catTRAC, catAJUS, catFRES, 
                 catFORN, catMQSP, catTORN, catCALA, catDESE )
                 
    catsORD2 = ( catARQT,catASSE,catDESN,catDESP,catENGO,catINSQ,catPROJ,catTMET,
                catTPLA,catTCQU,catTELC,catTELE,catTINF,catTMEC,catMMAN,catTMEQ,catTIND,catTELM )
                
    catsORD = catsORD1 + catsORD2 + (catUNK,)
                
                
    # STRING x "Cargo" mapping
    
    strcargomap = {
        # Factory - Lower Class
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
        ('OP.CALAND','OP.CALAND.') : catCALA,
        ('DESEMPENADOR') : catDESE,
        
        # Technical - Medium Class
        ('ARQ. TEC.') : catARQT,
        ('ASS.ESP.') : catASSE,
        ('DESENHIST') : catDESN,
        ('DES.PROJ.') : catDESP,
        ('ENGENHEIRO') : catENGO,
        ('INSP.C.QU') : catINSQ,
        ('PROJETIST') : catPROJ,
        ('TEC.M.PRO') : catTMET,
        ('TEC.PLANE') : catTPLA,
        ('TEC.CONT.') : catTCQU,
        ('TEC.ELETR') : catTELC
        
        
        
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
        
        # Round to 2 decimal places
        self.jdata[aliasedcliente][cargocat] = round(self.jdata[aliasedcliente][cargocat], 2)
        
    def process (self, f):
        # strip carriage returns
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].strip()
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].replace('\r','')

        # split lines and split each line to a tuple
        # fields: codped || cliente || cargo || htipo || tothora || <ignored>
        fs = [x.split('|') for x in f[self.__class__.__name__.upper()].split('\n')]

        
        # Get output file for HTML
        o1 = self.getoutputfile(ext='html', append='%s-%s' % (f['#MES'], f['#ANO']))
        # Get output file for CSV
        o2 = self.getoutputfile(ext='csv', append='%s-%s-excel' % (f['#MES'], f['#ANO']))
        
        
        # HTML, Start headers
        o1.write('<!DOCTYPE html>')
        o1.write('<html>')
        o1.write('<head><title>%s - SISPOS</title><style>%s</style>' % (self.__class__.__name__.upper(), self.inlinecss))
        o1.write('<body>')
        o1.write('<h1>%s (%s/%s)</h1>' % (self.__class__.__name__.upper(),f['#MES'], f['#ANO']))
        
        # HTML, Open table
        o1.write('<table border="0">')
        o1.write('<tr>')
        o1.write("""<th width="100">codped</th>
                <th width="220">Cliente</th>
                <th width="80">Cargo</th>
                <th width="10">Htipo</th>
                <th width="80">Horas</th>
                <th width="250">Especialidade:</th>
                <th width="250">Cliente considerado:</th>""")
        o1.write('</tr>')
        
        for l in fs:
            # split values       
            codped, cliente, cargo, htipo, tothora, ign = l
        
            # Process line and build statistics.
            self.processjdata(l)
            
            # HTML
            jcl = self.judgecliente(l)
            jca = self.judgecargo(l)
            
            
            # Alter formatting from outcome (cat/catmotiv/wts)
            if jca == self.catUNK:
                trclass = 'unknownhour'
                trtitle = "verificar se faltam regras ou se regras com erro!"
            else:
                # If 'judgeclient' is different from cliente, then it's a grouping and should be highlighted
                if jcl != cliente:
                    trclass = "groupedhour"
                else:
                    trclass = "normalhour"
                trtitle = ""
                
                # if the client is modified by renclientdata, explain and show what OS's are inside this group
                renclientoslist = [x[2] for x in self.renclientdata if x[0] == jcl]
                if renclientoslist:
                    oslisttxt = ' '.join(renclientoslist[0])
                    trtitle = "(Grupo %s) --> OS %s" % (jcl, oslisttxt)

            # Write it out
            o1.write('<tr class="%s" title="%s">' % (trclass, trtitle))
            o1.write('<td>%s</td>' % (codped))
            o1.write('<td>%s</td>' % (cliente))
            o1.write('<td>%s</td>' % (cargo))
            o1.write('<td align="center">%s</td>' % (htipo))
            o1.write('<td align="left">%s</td>' % (tothora))
            o1.write('<td align="left">%s</td>' % (jca,))
            o1.write('<td align="left">%s</td>' % (jcl,))
            o1.write('</tr>')
            
        # Close HTML Table
        o1.write('</table>')
        
        o1.write('<hr />')
        
        # Print outcome tables in HTML and CSV
        totclientes = self.jdata.keys()
        totclientes.sort()
        for clnome in totclientes:
            clespecs = self.jdata[clnome].keys()
            clespecs.sort()
            totclhora = 0
        
            gclientoslist = ""
            # if the client is modified by renclientdata, explain and show what OS's are inside this group
            renclientoslist = [x[2] for x in self.renclientdata if x[0] == clnome]
            if renclientoslist:
                oslisttxt = ' '.join(renclientoslist[0])
                gclientoslist = "[ %s ]" % (oslisttxt)

            #CSV
            o2.write('%s\t\t%s\r\n' % (clnome, gclientoslist))
            
            #HTML        
            o1.write('<table border="1">')
            o1.write('<tr><td colspan="2"><b>%s</b> <i>%s</i></td></tr>' % (clnome,gclientoslist))
            o1.write('<tr><td>Especialidade: </td><td>Total de Horas: </td></tr>')
            for espec in clespecs:
                o1.write('<tr><td>%s</td><td>%s</td></tr>' % (espec, self.jdata[clnome][espec]))
                totclhora += self.jdata[clnome][espec]
                
                #CSV
                o2.write('%s\t%s\r\n' % (espec, str(self.jdata[clnome][espec]).replace('.',',')))
                
                
            #CSV
            o2.write('\r\n-\r\n-\r\n')
                
            #HTML    
            o1.write('<tr><td colspan="2" align="center">TOTAL: %.2f</td></tr>' % (totclhora))
            o1.write('</table>')
            o1.write('<br />')
        
        # Close HTML document
        o1.write('</body></html>')

        return self.jdata

if __name__ == "__main__":
    a = HTipo0G()
    r = a.run()
