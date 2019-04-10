#!python3
# -*- coding: cp1252 -*-
import os
import re
from sisposbase.sispos import BaseSISPOS


class IndiceOcupacaoMaoObra(BaseSISPOS):
    findfiles = ( ("HEFET","HEFET"),
                  ("HDISP","HDISP"), 
                  ("#MES","Mes (FORMATO: MM)"),
                  ("#ANO","Ano (FORMATO: AAAA)") )

    def process (self, f):
        # Strip newlines and carriage returns
        f['HEFET'] = re.sub(r'[\r\n]', ' ', f['HEFET'].decode())
        f['HDISP'] = re.sub(r'[\r\n]', ' ', f['HDISP'].decode())

        fe = f['HEFET']
        fd = f['HDISP']

        # Horas efetivas
        ipcuc_hefet = float(re.search(r'total_IPCUC_HEFET.+?([0-9]{1,9}\,[0-9]{2})', f['HEFET']).group(1)
                            .replace(',','.'))

        ipsccm_hefet = float(re.search(r'total_IPSIPCCM_HEFET.+?([0-9]{1,9}\,[0-9]{2})', f['HEFET']).group(1)
                             .replace(',', '.'))

        icq_hefet = float(re.search(r'total_IQ_HEFET.+?([0-9]{1,9}\,[0-9]{2})', f['HEFET']).group(1)
                             .replace(',', '.'))

        fech_hefet = re.search(r'IPCUC.+?(([0-9]{2}\/){2}[0-9]{4})', f['HEFET']).group(1)

        total_hefet = icq_hefet+ipcuc_hefet+ipsccm_hefet

        # Horas disp
        ipcuc_hdisp = float(re.search(r'total_IPCUC_HDISP.+?([0-9]{1,9}\,[0-9]{2})', f['HDISP']).group(1)
                             .replace(',', '.'))

        ipsccm_hdisp = float(re.search(r'total_IPSIPCCM_HDISP.+?([0-9]{1,9}\,[0-9]{2})', f['HDISP']).group(1)
                             .replace(',', '.'))

        icq_hdisp = float(re.search(r'total_IQ_HDISP.+?([0-9]{1,9}\,[0-9]{2})', f['HDISP']).group(1)
                             .replace(',', '.'))

        fech_hdisp = re.search(r'IPCUC.+?(([0-9]{2}\/){2}[0-9]{4})', f['HDISP']).group(1)

        total_hdisp = icq_hdisp+ipcuc_hdisp+ipsccm_hdisp

        o1 = self.getoutputfile(append='%s-%s' % (f['#MES'], f['#ANO']))

        o1.write("\n")
        o1.write("\t\tNUCLEBRAS EQUIPAMENTOS PESADOS S.A. - NUCLEP\n")
        o1.write("\tGERENCIA DE CONTROLE - ICC\n\n")
        o1.write("INDICE DE OCUPACAO DE MAO DE OBRA (IOMO) - %s/%s\n\n" % (f['#MES'], f['#ANO']))

        o1.write("HORAS DISPONIVEIS:\n")
        o1.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hdisp))
        o1.write("\tTotais:\n")
        o1.write("\tIPS + IP-CCM\t%.2f\n" % (ipsccm_hdisp))
        o1.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hdisp))
        o1.write("\tIQ\t\t%.2f\n\n" % (icq_hdisp))
        o1.write("\tTOTAL:\t\t%.2f\n\n\n" % (total_hdisp))

        o1.write("HORAS EFETIVAS:\n")
        o1.write("\tDATA DE FECHAMENTO:\t%s\n\n" % (fech_hefet))
        o1.write("\tTotais:\n")
        o1.write("\tIPS + IP-CCM\t%.2f\n" % (ipsccm_hefet))
        o1.write("\tIPCUC\t\t%.2f\n" % (ipcuc_hefet))
        o1.write("\tIQ\t\t%.2f\n\n" % (icq_hefet))
        o1.write("\tTOTAL:\t\t%.2f\n\n\n" % (total_hefet))

        o1.write('\n\n')
        o1.write('                HORAS EFETIVAS\n')
        o1.write(' INDICE = -------------------------- = %.0f%%\n' % ((total_hefet/total_hdisp)*100))
        o1.write('                HORAS DISPONIVEIS\n')
        

if __name__ == "__main__":
    a = IndiceOcupacaoMaoObra()
    a.run()
