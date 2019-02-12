#!python2
# -*- coding: cp1252 -*-

import os
import re
import warnings
import locale
from openpyxl import load_workbook
from sisposbase.sispos import BaseSISPOS

warnings.filterwarnings('ignore')

def levenshtein(s, t):
    ''' From Wikipedia article; Iterative with two matrix rows. '''
    if s == t: return 0
    elif len(s) == 0: return len(t)
    elif len(t) == 0: return len(s)
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):
        v1[0] = i + 1
        for j in range(len(t)):
            cost = 0 if s[i] == t[j] else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return v1[len(t)]

class ComparaMNFDT(object):
    TIPO_MO_DIRETA = '0'
    TIPO_MO_INDIRETA = '1'
    TIPO_MO_NAOAPROP = '2'

    SITUACAO_NCPDEMITIDO = '10'

    def __init__(self, rpessi, rpessiname, empregados, empregadosname):

        # LEFT : DESTINO (resultado final)
        self.rpessi_data = rpessi
        self.rpessi_name = rpessiname

        # RIGHT: Origem (dados iniciais)
        self.empreg_data = empregados
        self.empreg_name = empregadosname

    def compara(self):

        empregdict = self.empreg_data

        mudsql = []
        rsql = lambda x: mudsql.append(unicode(x))

        mudtxt = []
        rtxt = lambda x: mudtxt.append(unicode(x))

        bannermsg = "000 Transformando a partir de \"%s\" para \"%s\"." % (self.empreg_name, self.rpessi_name)
        rtxt(bannermsg)

        qtddif = 0
        for linha in self.rpessi_data:
            matr, nome, codfunc, descricao, depto, tipo = linha

            muds = []

            if empregdict.has_key(matr):

                # codfunc
                if (codfunc != empregdict[matr]['codfunc']) and (descricao.find("(I)") == -1):
                    muds.append("  CODFUNC | de %s(%s) para %s(%s)" % (empregdict[matr]['codfunc'],
                                                                empregdict[matr]['descricao'],
                                                                codfunc,
                                                                descricao))
                    codfuncsql = "update empregados set codfunc = \"%s\" where matr = %s;" % (codfunc, matr)
                    rsql(codfuncsql)

                # departamento
                if (depto != empregdict[matr]['depto']):
                    muds.append("  DEPTO | de \"%s\" para \"%s\"" % (empregdict[matr]['depto'],
                                                              depto))
                    deptosql = "update empregados set depto = \"%s\" where matr = %s;" % (depto, matr)
                    rsql(deptosql)

                # tipo
                if (tipo != empregdict[matr]['tipo']):
                    muds.append("  TIPO | de \"%s\" para \"%s\" [avaliar: %s %s/%s]" % (empregdict[matr]['tipo'],
                                                                                        tipo,
                                                                                        empregdict[matr]['depto'],
                                                                                        descricao,
                                                                                        empregdict[matr]['descricao']))

                # situacao = demitido
                if empregdict[matr]['situacao'] in (self.SITUACAO_NCPDEMITIDO,):
                    muds.append(u"""  ---------
    Atenção: matr %s consta como DEMITIDO na base -%s-:
    matr: %s / nome: %s
    codfunc: %s (%s)
    depto: %s / tipo: %s
  ---------""" % (matr, self.empreg_name,
                matr, nome, codfunc, descricao, depto, tipo))

            else:
                if tipo <> self.TIPO_MO_NAOAPROP:
                    muds.append(u"""  ---------
    Atenção: matr %s nao existe na base -%s-:
    matr: %s / nome: %s
    codfunc: %s (%s)
    depto: %s / tipo: %s
  ---------""" % (matr, self.empreg_name,
                matr, nome, codfunc, descricao, depto, tipo))

            if muds:
                rtxt("\nMATR: %s (%s):" % (str(matr).ljust(5),
                                           nome.ljust(20)[0:17]))

                qtddif += len(muds)

                for mud in muds:
                    rtxt(mud)

        return [mudtxt, mudsql, qtddif]

class ComparaRpessiEmpregados(BaseSISPOS):
    findfiles = [ ('!RPESSI', ur'RELAÇÃO.*EFETIVO.*\.xlsx'),
                  ('EMPREG',  ur'empreg.*\.txt')]

    def getrpessidata(self, rpessifname):

        # Abrir aba geral da planilha usando openPYXL
        # Ignorar 'warning' usando função específica
        with warnings.catch_warnings():
            wb = load_workbook(rpessifname)
            abageral = wb.get_sheet_by_name("GERAL")

        rows = [[x.value for x in row] for row in abageral.rows]

        # achar intervalo que contem os nomes de pessoas.
        namestart = -1
        nameend = -1
        for row, rowno in zip(rows, range(len(rows))):
            nome, setor = row[1:3]

            if namestart == -1:
                if nome == "Nome" and setor == "Setor":
                    # Se a linha atual contem "Nome" e " Setor" o inicio dos nomes é na próxima linha.
                    namestart = rowno+1
                    #print u"Encontrado início dos nomes na linha %d" % (namestart+1,)
            if nameend == -1:
                if nome == None and setor == None:
                    # Se a linha atual contem None o fim dos nomes é na penúltima linha.
                    nameend = rowno-1
                    #print u"Encontrado fim dos nomes na linha %d" % (nameend+1,)

        employeelist = rows[namestart:nameend+1]

        retval = []
        for employee in employeelist:
            #[3567, u'LIBERAL ENIO ZANELATTO', u'I', 29, '=CONCATENATE(C2," ",G2)', None, u'DIRETOR', None, 2, 1, None, None, None, None, None, None]
            matr = str(employee[0])
            nome = unicode(employee[1])
            depto = str(employee[2])
            codfunc = str(employee[3])
            prof = unicode(employee[6])
            tipo = str(employee[8])

            # add data
            entry = [matr, nome, codfunc, prof, depto,  tipo]

            retval.append(entry)

        return retval

    def getempregdata(self, _ed):

        ed_split = _ed.strip().split('\r\n')

        retval = {}
        for line in ed_split:

            line_s = line.split("|")
            line_s = [x.strip() for x in line_s]

            #matr, nome, codfunc, descricao, depto, tipo = linha
            matr, nome, codfunc, descricao, depto, tipo, situacao, _ = line_s

            retval[matr] = {}
            retval[matr]['nome'] = nome
            retval[matr]['codfunc'] = codfunc
            retval[matr]['descricao'] = descricao
            retval[matr]['depto'] = depto
            retval[matr]['tipo'] = tipo
            retval[matr]['situacao'] = situacao

        return retval


    def process (self, f):

        # Relacao de Pessoal do I (matriz)
        rpessidata = self.getrpessidata(f['!RPESSI'])

        # Relacao de Empregados no Sistema (dicionario)
        empregdata = self.getempregdata(f['EMPREG'])



        #print "matr, nome, codfunc, descricao, depto, situacao = linha"
        #from code import interact; interact(local=locals())

        # Ativa o comparador
        comp = ComparaMNFDT(rpessidata, "RPESSI", empregdata, "TABELA EMPREGADOS", )

        # Realiza comparação, grava resultados em mudtxt e mudsql, qtdmud = quantidade de mudanças
        mudtxt, mudsql, qtdmud = comp.compara()

        print u"----------------------------------------"
        print u"%d diferença(s) detectadas..." % (qtdmud)
        print u"----------------------------------------"

        #from code import interact; interact(local=locals())

        if qtdmud:
            # Salvando em texto as mudanças textuais
            txtfile = self.getoutputfile(append='txt')
            txtdata = u"\n".join(mudtxt)
            txtfile.write(txtdata.encode(locale.getpreferredencoding()))

            # Salvando em texto as mudanças SQL
            sqlfile = self.getoutputfile(append='sqlfile')
            sqldata = u"\n".join(mudsql)
            sqlfile.write(sqldata.encode(locale.getpreferredencoding()))


a = ComparaRpessiEmpregados()
a.run()
