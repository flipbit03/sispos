# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS

class HHReal(BaseSISPOS):
    # ----------------------------------
    # Initalization parameters
    # ----------------------------------

    findfiles = ( ("HHREAL","hhreal"), )

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

    # Work categories:
    catTRAC = "Traçagem"
    catCORT = "Corte"
    catCALA = "Calandra"
    catMONT = "Montagem"
    catSOLD = "Soldagem"
    catTRAT = "Trat. Térmico"
    catJATO = "Jato/Pintura"
    catUSIF = "Usin./Ferram."
    catITE  = "ITE"
    catTECM = "TEC.M.PRO"
    catICQ  = "ICQ"
    catIGN  = "IGNORADO"       # Ignored hours
    catUNK  = "DESCONHECIDO"   # Unknown hours because of missing rules, programmer should check these.

    # Work categories, ordered:
    catsORD = [catTRAC, catCORT, catCALA, catMONT, catSOLD, catTRAT, catJATO, catUSIF,
               catITE, catTECM, catICQ, catIGN, catUNK]

    # Hour types:
    hourTOTAL = 'total'
    hour18    = 'h18'
    hour80    = 'h80'
    hour92    = 'h92'

    # ----------------------------------
    # Code
    # ----------------------------------

    # Dict used to store OS judgement data
    jdata = {}


    def processjdata(self, line):
        #codped || descricao || depto || fa || atividade || tothora || <ignore>

        # Get main variables
        codped, descricao, depto, fa, atividade, tothora, ign = line

        # Generate additional vars from main
        cat, catmotiv = self.judgecat(line)
        wts = self.judgewts(line)
                       
        if not self.jdata.has_key(codped):
            self.jdata[codped] = {}

        if not self.jdata[codped].has_key(cat):
            self.jdata[codped][cat] = {}

        for htype in wts:
            if not self.jdata[codped][cat].has_key(htype):
                self.jdata[codped][cat][htype] = float(0)
                    
            self.jdata[codped][cat][htype] += float(tothora)

            # round everything to 2 decimal places.
            self.jdata[codped][cat][htype] = round(self.jdata[codped][cat][htype],2)

    def generateoutcomelist(self, os):

        def gvn(dictvar, dictkey):
            try:
                return dictvar[dictkey]
            except:
                return ''
        
        rv = []

        rv.append( (os,) )

        z = gvn(self.jdata, os)

        if z:
            for categ in self.catsORD:

                t = gvn(z, categ)

                ht, h18, h80, h92 = ('','','','')
                if t:
                    ht = gvn(t, self.hourTOTAL)
                    h18 = gvn(t, self.hour18)
                    h80 = gvn(t, self.hour80)
                    h92 = gvn(t, self.hour92)
                
                rv.append( (categ, str(ht).replace('.',','), str(h80).replace('.',','), str(h18).replace('.',','), str(h92).replace('.',',')) )

        return rv

    def generateoutcomecsv(self, os):

        rv = []

        data = self.generateoutcomelist(os)

        data.insert(1, ('---Categoria---', '||Horas totais||', '||Horas 80||', '||Horas 18||', '||Horas 92-97||') )

        data.insert(10, ('Carpintaria', '¬', '¬', '¬', '¬'))

        for line in data:
            rv.append('\t'.join(line))

        rv.append('\n\n')


        return '\n'.join(rv)

    def generateoutcomechart(self, os):

        def gvn(dictvar, dictkey):
            try:
                return dictvar[dictkey]
            except:
                return ''
        
        rv = []

        rv.append('<table border="1">')
        rv.append('<tr>')
        rv.append('<tr><td colspan="5" align="center">%s</td></tr>' % (os))
        rv.append('<tr><td>Categoria</td><td>Horas Totais:</td><td>Horas 80</td><td>Horas 18</td><td>Horas 92</td></tr>')

        z = gvn(self.jdata, os)

        if z:
            for categ in self.catsORD:

                t = gvn(z, categ)

                ht, h18, h80, h92 = ('','','','')
                if t:
                    ht = gvn(t, self.hourTOTAL)
                    h18 = gvn(t, self.hour18)
                    h80 = gvn(t, self.hour80)
                    h92 = gvn(t, self.hour92)
                
                rv.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (categ, ht, h80, h18, h92))

        rv.append('</table>')

        return ''.join(rv)

    def judgewts(self, line):
        '''Explains where to put the hours, total or total+(18,80,92-97)'''
        #get data
        codped, cargo, depto, fa, atividade, tothora, ign = line

        # Where to sum? 18, 80 or 92-97
        wts = []

        # Qualquer hora é somada as horas totais
        wts.append('total')

        # Código 18 -- Preparação
        if atividade in ("18"):
            wts.append('h18')

        # Código 80 -- Reparo
        elif atividade in ("80"):
            wts.append('h80')

        # Códigos 92-97
        elif atividade in ("92", "93", "94", "95", "96", "97"):
            wts.append('h92')


        return list(wts)

    def judgecat(self, line):
        #get data
        codped, cargo, depto, fa, atividade, tothora, ign = line
        
        categ = self.catUNK #tracagem, corte, ....
        motiv = 'Linha não entrou em nenhuma regra! Verificar...' # motivo em caso de regra especial

        # -------------
        # -- Ignorar --
        # -------------

        # Técnico de Planejamento
        if cargo.find("TEC.PLANE") >= 0:
            categ = self.catIGN
            motiv = 'Cargo Ignorado: Tecnico de Planejamento'
            return (categ, motiv)

        # Auxiliar Administrativo
        if cargo.find("AUX.ADM") >= 0:
            categ = self.catIGN
            motiv = 'Cargo Ignorado: Auxiliar Administrativo'
            return (categ, motiv)

        # Arquivista Técnico
        if cargo.find("ARQ. TEC.") >= 0:
            categ = self.catIGN
            motiv = 'Cargo Ignorado: Arquivista Tecnico'
            return (categ, motiv)

        # Supervisores e Mestres
        if ((cargo.find("SUP") >= 0) or
            (cargo.find("MEST") >= 0)):
            categ = self.catIGN
            motiv = 'Cargo Ignorado: Supervisor ou Mestre'
            return (categ, motiv)

        # Departamentos ignorados
        if depto in ("IC", "ICC", "ICP", "IG-1", "IG-2", "IG-3", "IG-CPR-2", "IP-CUC", "IPM", "IG-AS", "IG-CLF"):
            categ = self.catIGN
            motiv = "Setor Ignorado: %s" % (depto)
            return (categ,motiv)

        # -----------
        # -- CARGO --
        # -----------
    
        #TEC. M. PRO
        if cargo in ("TEC.M.PRO"):
            categ = self.catTECM
            return (categ,'')

        # -------------
        # -- Setores --
        # -------------

        #Tracagem
        if depto in ("IPF/T", "IPF-T"):
            categ = self.catTRAC
            return (categ,'')

        #Corte
        if depto in ("IPF/C", "IPF-C"):
            categ = self.catCORT
            return (categ,'')

        #Calandra
        if depto in ("IP-CUC/C", "IP-CUC/D", "IP-CPP-D"):
            categ = self.catCALA
            return (categ,'')

        #Montagem
        if depto in ("IPF/M"):
            categ = self.catMONT
            return (categ,'')
        elif depto in ("IPF") and (cargo.find('IND.') >= 0):
            categ = self.catMONT
            motiv = "Regra especial: Tecnico Industrial no IPF"
            return (categ,motiv)

        #Soldagem
        if depto in ("IPF/S"):
            categ = self.catSOLD
            return (categ,'')

        #Tratamento Termico
        if depto in ("IPF/TT"):
            categ = self.catTRAT
            return (categ,'')

        #Jato/Pintura
        if depto in ("IPF/JP"):
            categ = self.catJATO
            return (categ,'')

        #Usinagem/Ferramentaria
        if depto in ("IP-CUC/U", "IP-CUC/F"):
            categ = self.catUSIF
            return (categ,'')

        #ITE
        if depto in ("ITI", "IT-CEP", "IT-CPL", "I-EES", "IG-CPR-1"):
            categ = self.catITE
            return (categ,'')

        #ICQ
        if depto in ("IQ"):
            categ = self.catICQ
            return (categ,'')


        # Else? DESCONHECIDO (Programmer should check it out)
        return (categ, motiv)

    def process (self, f):
        # strip carriage returns
        f['HHREAL'] = f['HHREAL'].strip()
        f['HHREAL'] = f['HHREAL'].replace('\r','')

        # split lines and split each line to a tuple
        # fields: codped || descricao || depto || fa || atividade || tothora || <ignore>
        fs = [x.split('|') for x in f['HHREAL'].split('\n')]

        # Get output file for HTML
        o1 = self.getoutputfile(ext='html')  #, append='%s-%s' % (f['#MES'], f['#ANO']))

        o2 = self.getoutputfile(ext='csv', append='excel')

        # init output html
        o1.write('<!DOCTYPE html>')
        o1.write('<html>')
        o1.write('<head><title>HHREAL - SISPOS</title><style>%s</style>' % (self.inlinecss))
        
        o1.write('<body>')
        o1.write('<h1>HHREAL</h1>')

        # Get OS list
        oses = list(set([x[0] for x in fs]))
        oses.sort()
        for os in oses:
            # Open HTML TABLE
            o1.write('<table>')
            o1.write('<tr>')
            o1.write("""<th width="100">codped</th>
                    <th width="170">cargo</th>
                    <th width="80">depto</th>
                    <th width="100">fa-ativ</th>
                    <th width="50">horas</th>
                    <th width="150">outcome</th>""")
            o1.write('</tr>')

            #In this OS, get distinct PROFESSIONS
            professions = list(set([x[1] for x in fs if x[0] == os]))
            professions.sort()
            for profession in professions:
                # List and process hours for this profession
                lines = [x for x in fs if x[0] == os and x[1] == profession]

                for line in lines:
                    ## MAIN LOOP HERE!

                    ## Process OS statistics
                    self.processjdata(line)

                    ## Split line
                    codped, descricao, depto, fa, atividade, tothora, ign = line

                    ## Generate additional vars
                    cat, catmotiv = self.judgecat(line)
                    wts = self.judgewts(line)

                    
                    # Alter formatting from outcome (cat/catmotiv/wts)
                    trclass = ''
                    trtitle = ''
                    tdtothora = ''
                    if cat == "IGNORADO": # Ignored hours
                        trclass = 'class="ignoredhour"'
                        trtitle = 'title="%s"' % (catmotiv)
                    elif cat == "DESCONHECIDO": # Unknown hours (Programmer should check these so highlight!)
                        trclass = 'class="unknownhour"'
                    else:
                        trclass = 'class="normalhour"' # Normal hours
                        if ('h18' in wts) or ('h80' in wts) or ('h92' in wts):
                            tdtothora='class="hiliteativ"'

                    # Write it out
                    o1.write('<tr %s %s>' % (trclass, trtitle))
                    o1.write('<td>%s</td>' % (codped))
                    o1.write('<td>%s</td>' % (descricao))
                    o1.write('<td>%s</td>' % (depto))
                    o1.write('<td %s align="center">%s %s</td>' % (tdtothora, fa,atividade))
                    o1.write('<td align="center">%s</td>' % (tothora))
                    o1.write('<td align="right">%s</td>' % (cat))
                    o1.write('</tr>')
                
                # Total hours for this profession:
                sumhp = sum([float(x[5]) for x in fs if x[0] == os and x[1] == profession])
                #print "\t total de HH de %s --> %.2f" % (profession, sumhp) #debug
                o1.write('<tr class="totalcargo">')
                o1.write('<td colspan="4" align="center">Total de HH de %s</td>' % (profession))
                o1.write('<td colspan="2">%.2f</td>' % (sumhp))
                o1.write('</tr>')
                o1.write('<tr>')
                o1.write('<td>&nbsp;</td>')
                o1.write('</tr>')


            # Total hours for this OS
            sumhos = sum([float(x[5]) for x in fs if x[0] == os])
            #print "total de HH da OS %s --> %.2f" % (os, sumhos) #debug
            o1.write('<tr>')
            o1.write('<td colspan="4" align="center" class="totalos">Total de HH da OS %s</td>' % (os))
            o1.write('<td colspan="2" class="totalos">%.2f</td>' % (sumhos))
            o1.write('<td>&nbsp;</td>')
            o1.write('</tr>')
            o1.write('<tr>')
            o1.write('<td>&nbsp;</td>')
            o1.write('</tr>')

            # Write CSV outcome for this OS
            o2.write(self.generateoutcomecsv(os))


            # Close HTML Table
            o1.write('</table>')

            # Generate outcome chart (Result)
            o1.write(self.generateoutcomechart(os))

            o1.write('<hr />')

        # Close HTML document
        o1.write('</body></html>')

        return self.jdata
        
                
a = HHReal()

r = a.run()
#r2 = r[1]
