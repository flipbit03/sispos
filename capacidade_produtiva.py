# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS

class CapacidadeProdutiva(BaseSISPOS):

    ## Altere aqui as categorias de pessoal informadas pela Stefania/ICP
    totpescategs = (
    "NUCLEP", 
    "PERSONAL ETN", 
    "MAZINI", 
    "RPA", 
    "ENGENHEIRA CEDIDA"
    )
    
    findfiles = [ 
                ## datas 
                ("#DTFECH","Data de Fechamento do Mes (DD/MM/AAAA)"),
                ("#MES","Mes (FORMATO: MM)"),
                ("#ANO","Ano (FORMATO: AAAA)"),
                ("#DIU","Quantidade de Dias Uteis no Mes"),
                ## HH 
                ("#HPD","\nHH:\n\nHoras Produtivas Diretas (Total HH)"),
                ]
    
    def dynfindfiles(self):
        ## Adiciona perguntas de PESSOAL de acordo com self.totpescategs
        for categname in self.totpescategs:
            self.findfiles.append( ("#EF%s" % (categname,), "Efetivo %s (Tot. Pessoas)" % (categname,)) )
    
    def process (self, f):
    
        # horas produtivas diretas em HH
        f['#HPD'] = f['#HPD'].replace(',','.')
        hpd = float(f['#HPD'])
        
        #import code; code.interact(local=locals())
        
        # Categorias que contem efetivo em PESSOAS (Começam com #EF)
        categorias_efetivo = [categ for categ in f.keys() if categ.find('#EF') <> -1]

        # Soma todas as pessoas das categorias
        eftotal = sum([int(f[categ]) for categ in categorias_efetivo])

        # Dias Uteis
        diu = int(f['#DIU'])
        
        #### CALCULA     
        ## Capacidade Produtiva do I
        
        ## Horas produtivas diretas, em PESSOAS
        
        ## total de hh dividido por (dias uteis vezes 8 horas de trabalho)
        hpd_pessoas = int(round((hpd/float(diu*8))))
        
        cpi = hpd_pessoas / (float(eftotal))
        
        #### GERA ARQUIVO TXT
        ##
        o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))
        
        o1.write("\n")
        o1.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o1.write("INDICE DE CAPACIDADE PRODUTIVA DO I (ICPI-%s/%s)\n\n\n" % (f['#MES'], f['#ANO']))

        o1.write("HORAS PRODUTIVAS DIRETAS - FECHAMENTO EM \"%s\":\n\n" % (f['#DTFECH']))
        o1.write("\tTotal HH = %.2f\n\n" % (hpd))
        o1.write("\tTotal HH em pessoas = %d pessoas\n\n" % (hpd_pessoas))

        o1.write("EFETIVO DO I - BIBLIA DE %s/%s:\n\n\tTotais:\n\n" % (f['#MES'], f['#ANO']))

        for categ in self.totpescategs:
            fcateg = categ.ljust(23)
            dictcateg = '#EF%s' % (categ)
            o1.write("\t%s%d pessoas\n" % (fcateg, int(f[dictcateg])))
        
        o1.write('\n\t%s%d pessoas\n' % ("Total:".ljust(23), eftotal))
        
        o1.write('\n\n')
        o1.write('               (HPD / %2d dias úteis / 8h)\n' % (diu,))
        o1.write(' INDICE CP = ------------------------------ = %.0f%%\n' % ((cpi*100)))
        o1.write('                       EFETIVO\n')
        

a = CapacidadeProdutiva()
a.run()
