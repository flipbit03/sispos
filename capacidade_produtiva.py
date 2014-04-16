# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS

class CapacidadeProdutiva(BaseSISPOS):
    findfiles = ( 
                ## datas 
                ("#DTFECH","Datas:\n\nData de Fechamento do Mes (DD/MM/AAAA)"),
                ("#MES","Mes (FORMATO: MM)"),
                ("#ANO","Ano (FORMATO: AAAA)"),
                ("#DIU","Quantidade de Dias Uteis no Mes"),
                ## HH 
                ("#HPD","\nHH:\n\nHoras Produtivas Diretas (Total HH)"),
                ## pessoal
                ("#EFN","\nPessoal\n\nEfetivo NUCLEP (Tot. Pessoas)"), 
                ("#EFPER","Efetivo PERSONAL (Tot. Pessoas)"), 
                ("#EFRPA","Efetivo RPA (Tot. Pessoas)"), 
                ("#EFENGC","Efetivo ENGENHEIRA CEDIDA (Tot. Pessoas)")
                )

    def process (self, f):
        # Strip newlines and carriage returns
        
        f['#HPD'] = f['#HPD'].replace(',','.')
        
        hpd = float(f['#HPD'])
        
        # efetivo
        efn = int(f['#EFN'])
        efper = int(f['#EFPER'])
        efrpa = int(f['#EFRPA'])
        efengc = int(f['#EFENGC'])
        
        # total efetivo
        eftotal = efn + efper + efrpa + efengc

        # dias uteis
        diu = int(f['#DIU'])
        
        #### CALCULA     
        ## capacidade produtiva do i
        
        hpd_pessoas = int(round((hpd/float(diu*8))))
        
        cpi = hpd_pessoas / (float(eftotal))
        
        
        o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))

        o1.write("\n")
        o1.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o1.write("INDICE DE CAPACIDADE PRODUTIVA DO I (ICPI-%s/%s)\n\n\n" % (f['#MES'], f['#ANO']))

        o1.write("HORAS PRODUTIVAS DIRETAS - FECHAMENTO EM \"%s\":\n\n" % (f['#DTFECH']))
        o1.write("\tTotal HH = %.2f\n\n" % (hpd))
        o1.write("\tTotal HH em pessoas = %d pessoas\n\n" % (hpd_pessoas))

        o1.write("EFETIVO DO I - BIBLIA DE %s/%s:\n\n\tTotais:\n\n" % (f['#MES'], f['#ANO']))

        o1.write("\tNUCLEP:\t\t\t\t%d pessoas\n" % (efn))
        o1.write("\tPERSONAL:\t\t\t%d pessoas\n" % (efper))
        o1.write("\tRPA:\t\t\t\t%d pessoas\n" % (efrpa))
        o1.write("\tENGENHEIRA CEDIDA:\t\t%d pessoas\n" % (efengc))
        o1.write("\tAPRENDIZES:\t\t\t(Não considerar)\n")
        o1.write('\n\tTotal: %d pessoas\n' % (eftotal,))
        
        #o1.write("\n\n\tDias Uteis em %s/%s = %d\n\n" % (f['#MES'],f['#ANO'], diu))

        o1.write('\n\n')
        o1.write('               (HPD / %2d dias úteis / 8h)\n' % (diu,))
        o1.write(' INDICE CP = ------------------------------ = %.0f%%\n' % ((cpi*100)))
        o1.write('                       EFETIVO\n')
        
                
a = CapacidadeProdutiva()
a.run()
