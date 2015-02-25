# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS

class CapacidadeProdutiva(BaseSISPOS):

    ## Altere aqui as categorias de pessoal informadas pela Stefania/ICP
    totpescategs = (
    "NUCLEP", 
    "PERSONAL ETN", 
    "MAZZINI", 
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
                ("#HPDR","HH Capacidade Produtiva \"Real\" (Total HH)"),
                ("#HPDP","HH Capacidade Produtiva \"Planejada\" (Total HH)")
                ]
    
    def dynfindfiles(self):
        ## Adiciona perguntas de PESSOAL de acordo com self.totpescategs
        for categname in self.totpescategs:
            self.findfiles.append( ("#EF%s" % (categname,), "Efetivo %s (Tot. Pessoas)" % (categname,)) )
    
    def process (self, f):
        # Horas Produtivas Diretas "Reais" 
        f['#HPDR'] = f['#HPDR'].replace(',','.')
        hpd_real = float(f['#HPDR'])
        
        # Horas Produtivas Diretas "Planejadas" 
        f['#HPDP'] = f['#HPDP'].replace(',','.')
        hpd_plane = float(f['#HPDP'])
        
        #import code; code.interact(local=locals())
        
        # Categorias que contem efetivo em PESSOAS (Começam com #EF)
        categorias_efetivo = [categ for categ in f.keys() if categ.find('#EF') <> -1]

        # Soma todas as pessoas das categorias
        eftotal = sum([int(f[categ]) for categ in categorias_efetivo])

        # Dias Uteis
        diu = int(f['#DIU'])
        
        #### CALCULA     
        ## Capacidade Produtiva do I
        
        ## - Horas Produtivas Diretas REAIS, em PESSOAS
        ## - Total de hh dividido por (dias uteis vezes 8 horas de trabalho)
        hpd_real_pessoas = int(round((hpd_real/float(diu*8))))
        cpi_real = hpd_real_pessoas / (float(eftotal))
        
        ## - Horas Produtivas Diretas PLANEJADAS, em PESSOAS
        ## - Total de hh dividido por (dias uteis vezes 8 horas de trabalho)
        hpd_plane_pessoas = int(round((hpd_plane/float(diu*8))))
        cpi_plane = hpd_plane_pessoas / (float(eftotal))
        
        #### GERA ARQUIVO TXT
        ##
        o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))
        
        o1.write("\n")
        o1.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o1.write("INDICE DE CAPACIDADE PRODUTIVA DO I - REAL E PLANEJADO (ICPI_R e ICPI_P %s/%s)\n\n\n" % (f['#MES'], f['#ANO']))

        o1.write("HORAS PRODUTIVAS DIRETAS REAIS      (hpd_r) - FECHAMENTO EM \"%s\":\n\n" % (f['#DTFECH']))
        o1.write("\tTotal HH = %.2f\n\n" % (hpd_real))
        o1.write("\tTotal HH em pessoas = %d pessoas\n\n" % (hpd_real_pessoas))
        
        o1.write("HORAS PRODUTIVAS DIRETAS PLANEJADAS (hpd_p) - FECHAMENTO EM \"%s\":\n\n" % (f['#DTFECH']))
        o1.write("\tTotal HH = %.2f\n\n" % (hpd_plane))
        o1.write("\tTotal HH em pessoas = %d pessoas\n\n" % (hpd_plane_pessoas))

        o1.write("EFETIVO DO I - BIBLIA DE %s/%s:\n\n\tTotais:\n\n" % (f['#MES'], f['#ANO']))

        for categ in self.totpescategs:
            fcateg = categ.ljust(23)
            dictcateg = '#EF%s' % (categ)
            o1.write("\t%s%d pessoas\n" % (fcateg, int(f[dictcateg])))
        
        o1.write('\n\t%s%d pessoas\n' % ("Total:".ljust(23), eftotal))
        
        o1.write('\n\n')
        o1.write('                   (hpd_r / %2d dias úteis / 8h)\n' % (diu,))
        o1.write(' INDICE ICPI_R = ------------------------------ = %.0f%%\n' % ((cpi_real*100)))
        o1.write('                           EFETIVO\n')
        
        o1.write('\n\n')
        o1.write('                   (hpd_p / %2d dias úteis / 8h)\n' % (diu,))
        o1.write(' INDICE ICPI_P = ------------------------------ = %.0f%%\n' % ((cpi_plane*100)))
        o1.write('                           EFETIVO\n\n')
        

a = CapacidadeProdutiva()
a.run()
