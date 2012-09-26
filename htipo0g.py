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
    catCALD = "f_Caldeireiro"
    catSOLD = "f_Soldador"
    catESME = "f_Esmerilhador"
    catMACA = "f_Macariqueiro"
    catTRAC = "f_Tracador"
    catAJUS = "f_Ajustador Mecanico"
    catFRES = "f_Fresador"
    catFORN = "f_Tratamento Termico"
    catMQSP = "f_Op. Maquina Especializado"
    catTORN = "f_Torneiro Mecanico"
    catCALA = "f_Op. Calandra"
    catDESE = "f_Desempenador"
    
    # Technical - Medium Class
    catARQT = "t_Arquivista Tecnico"
    catASSE = "t_Assistente Especializado"
    catDESN = "t_Desenhista"
    catDESP = "t_Desenhista Projetista"
    catENGO = "t_Engenheiro"
    catINSQ = "t_Inspetor de Cont. Qualidade"
    catPROJ = "t_Projetista"
    catTMET = "t_Tecnico de Met. e Processos"
    catTPLA = "t_Tecnico de Planejamento"
    catTCQU = "t_Tecnico de Cont. da Qualidade"
    catTELC = "t_Tecnico em Eletricidade"
    catTELE = "t_Tecnico em Eletronica"
    catTINF = "t_Tecnico de Informatica"
    catTMEC = "t_Tecnico em Mecanica"
    catMMAN = "t_Tecnico em Mec. de Manutencao"
    catTMEQ = "t_Tecnico em Mec. do Cont. Qualidade"
    catTIND = "t_Tecnico Industrial"
    catTELM = "t_Tecnico em Eletromecanica"
    
    # Unknown
    catUNK  = "zz_DESCONHECIDO"   # Unknown hours because of missing rules, programmer should check these.

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
        ('DESEMPENADOR',) : catDESE,
        
        # Technical - Medium Class
        ('ARQ. TEC.',) : catARQT,
        ('ASS.ESP.',) : catASSE,
        ('DESENHIST',) : catDESN,
        ('DES.PROJ.',) : catDESP,
        ('ENGENHEIRO',) : catENGO,
        ('INSP.C.QU',) : catINSQ,
        ('PROJETIST',) : catPROJ,
        ('TEC.M.PRO',) : catTMET,
        ('TEC.PLANE',) : catTPLA,
        ('TEC.CONT.',) : catTCQU,
        ('TEC.ELETRICIDADE',) : catTELC,
        ('TEC.ELETRONICA',): catTELE,
        ('TEC.INFOR',) : catTINF,
        ('TEC.MEC.',) : catTMEC,
        ('MEC.MAN.',) : catMMAN,
        ('TEC.MEC.CONT.QUA',) : catTMEQ,
        ('TEC.IND.',) : catTIND,
        ('TEC.ELETROMECANI',): catTELM 
        
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
            for kvalue in key:
                if cargo == kvalue: # must be identical, cannot use 'cargo in key'
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
            # Strip XXX_ from cargo
            jca_strip = re.sub(r'^.*?_','',jca)
            
            
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
            o1.write('<td align="left">%s</td>' % (jca_strip,))
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
                
                # remove XXX_ in cargonames
                espec_strip = re.sub(r'^.*?_','',espec)
                
                o1.write('<tr><td>%s</td><td>%s</td></tr>' % (espec_strip, self.jdata[clnome][espec]))
                totclhora += self.jdata[clnome][espec]
                
                #CSV
                o2.write('%s\t%s\r\n' % (espec_strip, str(self.jdata[clnome][espec]).replace('.',',')))
                
                
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
