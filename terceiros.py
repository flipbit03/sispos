# -*- coding: cp1252 -*-
import os
import re
import datetime
from decimal import *

from sisposbase.sispos import BaseSISPOS

class Terceiros(BaseSISPOS):
    """ Este é um modulo customizado para um relatório avulso, contemplando o total
    de horas apropriadas por OS, mês a mês. 
    
    Precisa de um arquivo txt extraído do sistema no seguinte formato:
    
    # ex.out: 17/12/2012|820180000|    1   | 23015|  8.0  |    13     |
    # fields:    DATA   | CODPED  | CODCLI | MATR | HORAS | ATIVIDADE | <ignored>
    
    A partir do campo CODCLI (1=nuclep / etc=Clientes) agrupamos as horas em Serviços Internos NCP
    """

    # ----------------------------------
    # Initalization parameters
    # ----------------------------------

    #findfiles = [ ('#MES', "Digite o mes atual MM"),
    #              ('#ANO', "Digite o ano atual AAAA") ]

    def dynfindfiles(self):
        mainfile = ( self.__class__.__name__.upper(), self.__class__.__name__.lower() )
        self.findfiles.append(mainfile)

    # ----------------------------------
    # Data
    # ----------------------------------

    # OS Groupings
    osgroupings = {
        u"Submarino"     : ("710000000", "710000001", "710000002", "710000003", "710000004",
                            "710000005", "710000006", "710000007", "710000008", "710000009",
                            "710000010", "710000011", "710000012", "710000013", "710000014",
                            "710000015", "710000016", "710000017", "710000018", "823600000", 
                            "790010000"),
                            
        u"Boca de Sino"  : ("640540000", "830540000"),
        
        u"Acumulador"    : ("140000000", "830140000"),
        
        u"Condensador"   : ("220000000", "830220000"),
        
        u"Componentes CTMSP": ("240000000", "240000001", "240000002", "240000003"),
        
        u"Vasos EBSE" : ("610280000", "830280000")
    }

    # Month Names
    mnames = {
    1 : u"Janeiro",
    2 : u"Fevereiro",
    3 : u"Março",
    4 : u"Abril",
    5 : u"Maio",
    6 : u"Junho",
    7 : u"Julho",
    8 : u"Agosto",
    9 : u"Setembro",
    10: u"Outubro",
    11: u"Novembro",
    12: u"Dezembro"
    }
    
    # ----------------------------------
    # Code
    # ----------------------------------

    # Dict used to store OS judgement data
    jdata = {}
    jdata2 = {}
        
    def getcodped(self, _l):
        # Get main variables
        _data, _codped, _codcli, _matr, _horas, _ativ, _ign = _l
        
        if _codcli.strip() == "1":
            return u"_Serviços Internos NCP"
        else:
            for groupname in self.osgroupings.keys():
                if _codped in self.osgroupings[groupname]:
                    return unicode(groupname)
                    
        # if we reach here, nothing has been grouped, return the original _codped
        return unicode(_codped)
        
    def processjdata(self, _l):
        # Get main variables
        _data, _codped, _codcli, _matr, _horas, _ativ, _ign = _l
        
        #get Month-Year
        datas = _data.strip()
        dia, mes, ano = datas.split("/")
        _anomes = "%s-%s" % (ano, mes)
        
        #get OS name
        codped = self.getcodped(_l)
        
        #sum TOTAL OS
        if not self.jdata2.has_key(codped):
            self.jdata2[codped] = Decimal("0")
        self.jdata2[codped] += Decimal(_horas)
        
        #per month
        if not self.jdata.has_key(_anomes):
            self.jdata[_anomes] = {}
        if not self.jdata[_anomes].has_key(codped):
            self.jdata[_anomes][codped] = Decimal("0")
        
        self.jdata[_anomes][codped] += Decimal(_horas)

    def process(self, f):
        # strip carriage returns
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].strip()
        f[self.__class__.__name__.upper()] = f[self.__class__.__name__.upper()].replace('\r','')

        # split lines and split each line to a tuple
        # ex.out: 17/12/2012|820180000|    1   | 23015|  8.0  |    13     |
        # fields:    DATA   | CODPED  | CODCLI | MATR | HORAS | ATIVIDADE | <ignored>
        fs = [x.split('|') for x in f[self.__class__.__name__.upper()].split('\n')]

        for l in fs:
            # split values       
            _data, _codped, _codcli, _matr, _horas, _ativ, _ign = l
        
            # Process line and build statistics.
            self.processjdata(l)
        
        #OUTPUT
        o1 = self.getoutputfile(ext='csv', append='%s-excel' % (self.__class__.__name__.upper(),))
        
        # ANOMES pairs
        anomespairs = self.jdata.keys()
        anomespairs.sort()
        
        mespairs_strgen = [u"%s-%s" % (self.mnames[int(x.split('-')[1])], x.split('-')[0]) for x in anomespairs]
        
        #import code; code.interact(local=locals())
        
        header1 = u"Ordem de Serviço|%s|(TOTAL)" % ("|".join(mespairs_strgen))
                
        ov = []
        ov.append(header1)
                
        # Get all codpeds.
        codpeds = self.jdata2.keys()
        codpeds.sort()
        
        for cp in codpeds:
            line = []
            # Append OS
            line.append(cp)
            
            for anomes in anomespairs:
                if self.jdata[anomes].has_key(cp):
                    hora = u'%s' % (self.jdata[anomes][cp],)
                    hora = hora.replace('.',',')
                    line.append(hora)
                else:
                    line.append(u"")
                    
            # Append total hh
            totalhh = u'%s' % (self.jdata2[cp],)
            totalhh = totalhh.replace('.',',')
            line.append(totalhh)
            
            ov.append(u'|'.join(line))
            
        # append totais by month
        totline = []
        totline.append('TOTAIS:')
        bigtot = 0
        for anomes in anomespairs:
            tot = Decimal(0)
            for codp in self.jdata[anomes]:
                tot = tot + self.jdata[anomes][codp]
            bigtot = bigtot + tot
            totline_s = '%s' % (tot,)
            totline_s = totline_s.replace('.',',')
            totline.append(totline_s)
            
        bigtot_s = '%s' % (bigtot,)
        bigtot_s = bigtot_s.replace('.',',')
        totline.append(bigtot_s)

        ov.append('|'.join(totline))
        
        # append groups
        ov.append('')
        ov.append('OS Agrupadas:')
        ov.append('')
        
        for group in self.osgroupings.keys():
            if group in self.jdata2:
                groupl = []
                groupl.append(group)
                groupl.append(u',\n|'.join(self.osgroupings[group]))
                
                ov.append('|'.join(groupl))
                ov.append('')
            
        fulltext = u"\n".join(ov)
        
        o1.write(fulltext.encode('windows-1252'))
        
        return self.jdata

if __name__ == "__main__":
    a = Terceiros()
    r = a.run()
