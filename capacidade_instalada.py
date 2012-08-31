# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS


class CapacidadeInstalada(BaseSISPOS):
    findfiles = ( ("HTOT","HTOT"),
                  ("HEFET","HEFET"),
                  ("HDISP","HDISP"), 
                  ("#MES","Mes (FORMATO: MM)"),
                  ("#ANO","Ano (FORMATO: AAAA)") )

    def process (self, f):
        # Strip newlines and carriage returns
        f['HTOT'] = re.sub(r'[\r\n]', ' ', f['HTOT'])
        f['HEFET'] = re.sub(r'[\r\n]', ' ', f['HEFET'])
        f['HDISP'] = re.sub(r'[\r\n]', ' ', f['HDISP'])
        
        # Horas totais
        ipcuc_htot = float(re.search(r'ipcuc.+?([0-9]{1,9}\.[0-9]{2})', f['HTOT']).group(1))
        ipf_htot = float(re.search(r'ipf.+?([0-9]{1,9}\.[0-9]{2})', f['HTOT']).group(1))
        icq_htot = float(re.search(r'icq.+?([0-9]{1,9}\.[0-9]{2})', f['HTOT']).group(1))
        fech_htot = re.search(r'ipcuc.+?(([0-9]{2}\/){2}[0-9]{4})', f['HTOT']).group(1)
        
        total_htot = icq_htot+ipcuc_htot+ipf_htot

        # Horas efetivas
        ipcuc_hefet = float(re.search(r'ipcuc.+?([0-9]{1,9}\.[0-9]{2})', f['HEFET']).group(1))
        ipf_hefet = float(re.search(r'ipf.+?([0-9]{1,9}\.[0-9]{2})', f['HEFET']).group(1))
        icq_hefet = float(re.search(r'icq.+?([0-9]{1,9}\.[0-9]{2})', f['HEFET']).group(1))
        fech_hefet = re.search(r'ipcuc.+?(([0-9]{2}\/){2}[0-9]{4})', f['HEFET']).group(1)
        
        total_hefet = icq_hefet+ipcuc_hefet+ipf_hefet

        # Horas disp
        ipcuc_hdisp = float(re.search(r'ipcuc.+?([0-9]{1,9}\.[0-9]{2})', f['HDISP']).group(1))
        ipf_hdisp = float(re.search(r'ipf.+?([0-9]{1,9}\.[0-9]{2})', f['HDISP']).group(1))
        icq_hdisp = float(re.search(r'icq.+?([0-9]{1,9}\.[0-9]{2})', f['HDISP']).group(1))
        fech_hdisp = re.search(r'ipcuc.+?(([0-9]{2}\/){2}[0-9]{4})', f['HDISP']).group(1)
        
        total_hdisp = icq_hdisp+ipcuc_hdisp+ipf_hdisp

        # Arquivo de Saída #1 -- CAPAC Normal
        o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))
        
        o1.write("\n")
        o1.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o1.write("CAPACIDADE INSTALADA - %s/%s\n\n" % (f['#MES'], f['#ANO']))

        o1.write("HORAS DISPONIVEIS:\n")
        o1.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hdisp))
        o1.write("\tTotais:\n")
        o1.write("\tIPF\t\t%.2f\n" % (ipf_hdisp))
        o1.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hdisp))
        o1.write("\tIQ\t\t%.2f\n\n" % (icq_hdisp))
        o1.write("\tTOTAL:\t\t%.2f\n\n\n" % (icq_hdisp+ipcuc_hdisp+ipf_hdisp))

        o1.write("HORAS EFETIVAS:\n")
        o1.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hefet))
        o1.write("\tTotais:\n")
        o1.write("\tIPF\t\t%.2f\n" % (ipf_hefet))
        o1.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hefet))
        o1.write("\tIQ\t\t%.2f\n\n" % (icq_hefet))
        o1.write("\tTOTAL:\t\t%.2f\n\n\n" % (icq_hefet+ipcuc_hefet+ipf_hefet))

        o1.write("HORAS TOTAIS:\n")
        o1.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_htot))
        o1.write("\tTotais:\n")
        o1.write("\tIPF\t\t%.2f\n" % (ipf_htot))
        o1.write("\tIPCUC\t\t%.2f\n" % (ipcuc_htot))
        o1.write("\tIQ\t\t%.2f\n\n" % (icq_htot))
        o1.write("\tTOTAL:\t\t%.2f\n\n\n" % (icq_htot+ipcuc_htot+ipf_htot))
        
        indice_total = ( (icq_hefet+ipcuc_hefet+ipf_hefet) / (icq_htot+ipcuc_htot+ipf_htot) )*100
        
        o1.write('\n\n')
        o1.write('                HORAS EFETIVAS\n')
        o1.write(' INDICE = -------------------------- = %.0f%%\n' % (indice_total))
        o1.write('                HORAS TOTAIS\n')
        
        # Arquivo de Saída #2 -- CAPAC Dario (Sem IQ)
        o2 = self.getoutputfile(append='%s-%s_DARIO' % (f['#MES'], f['#ANO']))
        
        o2.write("\n")
        o2.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o2.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o2.write("CAPACIDADE INSTALADA (Dario) - %s/%s\n\n" % (f['#MES'], f['#ANO']))

        o2.write("HORAS DISPONIVEIS:\n")
        o2.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hdisp))
        o2.write("\tTotais:\n")
        o2.write("\tIPF\t\t%.2f\n" % (ipf_hdisp))
        o2.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hdisp))
        o2.write("\tTOTAL:\t\t%.2f\n\n\n" % (ipcuc_hdisp+ipf_hdisp))

        o2.write("HORAS EFETIVAS:\n")
        o2.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hefet))
        o2.write("\tTotais:\n")
        o2.write("\tIPF\t\t%.2f\n" % (ipf_hefet))
        o2.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hefet))
        o2.write("\tTOTAL:\t\t%.2f\n\n\n" % (ipcuc_hefet+ipf_hefet))

        o2.write("HORAS TOTAIS:\n")
        o2.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_htot))
        o2.write("\tTotais:\n")
        o2.write("\tIPF\t\t%.2f\n" % (ipf_htot))
        o2.write("\tIPCUC\t\t%.2f\n" % (ipcuc_htot))
        o2.write("\tTOTAL:\t\t%.2f\n\n\n" % (ipcuc_htot+ipf_htot))
        
        indice_dario = ( (ipcuc_hefet+ipf_hefet) / (ipcuc_htot+ipf_htot) )*100
        
        o2.write('\n\n')
        o2.write('                HORAS EFETIVAS\n')
        o2.write(' INDICE = -------------------------- = %.0f%%\n' % (indice_dario))
        o2.write('                HORAS TOTAIS\n')
        
                
a = CapacidadeInstalada()
a.run()
