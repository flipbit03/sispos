# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS


ding = None

class HHReal(BaseSISPOS):
    findfiles = ( ("HHREAL","hhreal"), )

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

        
        categ = 'DESCONHECIDO' #tracagem, corte, ....
        motiv = 'Linha não entrou em nenhuma regra! Verificar...' # motivo em caso de regra especial
        

        # -------------
        # -- Ignorar --
        # -------------

        # Técnico de Planejamento
        if cargo.find("TEC.PLANE") >= 0:
            categ = 'IGNORADO'
            motiv = 'Tecnico de Planejamento'
            return (categ, motiv)

        # Auxiliar Administrativo
        if cargo.find("AUX.ADM") >= 0:
            categ = 'IGNORADO'
            motiv = 'Auxiliar Administrativo'
            return (categ, motiv)

        # Arquivista Técnico
        if cargo.find("ARQ. TEC.") >= 0:
            categ = 'IGNORADO'
            motiv = 'Arquivista Tecnico'
            return (categ, motiv)

        # Supervisores e Mestres
        if ((cargo.find("SUP") >= 0) or
            (cargo.find("MEST") >= 0)):
            categ = 'IGNORADO'
            motiv = 'Supervisor ou Mestre'
            return (categ, motiv)

        # Departamentos ignorados
        if depto in ("IC", "ICC", "ICP", "IG-1", "IG-2", "IG-3", "IG-CPR-2", "IP-CUC", "IPM"):
            categ = "IGNORADO"
            motiv = "Setor Ignorado: \"%s\"" % (depto)
            return (categ,motiv)


        # -------------
        # -- Setores --
        # -------------

        #Tracagem
        if depto in ("IPF/T", "IPF-T"):
            categ = "Tracagem"
            return (categ,'')

        #Corte
        if depto in ("IPF/C", "IPF-C"):
            categ = "Corte"
            return (categ,'')

        #Calandra
        if depto in ("IP-CUC/C", "IP-CUC/D", "IP-CPP-D"):
            categ = "Calandra"
            return (categ,'')

        #Montagem
        if depto in ("IPF/M"):
            categ = "Montagem"
            return (categ,'')
        elif depto in ("IPF") and (cargo.find('IND.') >= 0):
            categ = "Montagem"
            motiv = "Regra especial: Tecnico Industrial no IPF"
            return (categ,motiv)

        #Soldagem
        if depto in ("IPF/S"):
            categ = "Soldagem"
            return (categ,'')

        #Tratamento Termico
        if depto in ("IPF/TT"):
            categ = "Trat.Termico"
            return (categ,'')

        #Jato/Pintura
        if depto in ("IPF/JP"):
            categ = "Jato/Pintura"
            return (categ,'')

        #Usinagem/Ferramentaria
        if depto in ("IP-CUC/U", "IP-CUC/F"):
            categ = "Usinagem/Ferramentaria"
            return (categ,'')

        #ITE
        if depto in ("ITI", "IT-CEP", "IT-CPL", "I-EES", "IG-CPR-1"):
            categ = "ITE"
            return (categ,'')

        #TEC. M. PRO
        if cargo in ("TEC.M.PRO"):
            categ = "TEC.M.PRO"
            return (categ,'')

        #ICQ
        if depto in ("IQ"):
            categ = "ICQ"
            return (categ,'')


        # Else? IGNORED
        return (categ, motiv)

    def process (self, f):
        # strip carriage returns
        f['HHREAL'] = f['HHREAL'].strip()
        f['HHREAL'] = f['HHREAL'].replace('\r','')

        # split lines and split each line to a tuple
        # fields: codped || descricao || depto || fa || atividade || tothora || <ignore>
        fs = [x.split('|') for x in f['HHREAL'].split('\n')]


        data = {}
        
        for line in fs:
            #codped || descricao || depto || fa || atividade || tothora || <ignore>
            print "--> %s" % (str(line))

            # Get main variables
            codped, descricao, depto, fa, atividade, tothora, ign = line

            # Generate additional vars from main
            cat, catmotiv = self.judgecat(line)
            wts = self.judgewts(line)
            
            
            if not data.has_key(codped):
                data[codped] = {}

            if not data[codped].has_key(cat):
                
                data[codped][cat] = {}

            for htype in wts:
                if not data[codped][cat].has_key(htype):
                    data[codped][cat][htype] = float(0)
                    
                data[codped][cat][htype] += float(tothora)                        



        return data

        #o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))

        
        
                
a = HHReal()

r = a.run()
