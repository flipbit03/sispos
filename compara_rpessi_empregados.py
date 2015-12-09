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
    def __init__(self, left, leftname, right, rightname):

        # LEFT : DESTINO (resultado final)
        self.left = left
        self.leftname = leftname

        # RIGHT: Origem (dados iniciais)
        self.right = right
        self.rightname = rightname

    def compara(self):

        rightdict = {}

        mudsql = []
        rsql = lambda x: mudsql.append(unicode(x))

        mudtxt = []
        rtxt = lambda x: mudtxt.append(unicode(x))

        bannermsg = "000 Transformando a partir de \"%s\" para \"%s\"." % (self.rightname, self.leftname)
        rtxt(bannermsg)

        for linha in self.right:
            matr, nome, codfunc, descricao, depto, tipo = linha

            rightdict[matr] = {}
            rightdict[matr]['nome'] = nome
            rightdict[matr]['codfunc'] = codfunc
            rightdict[matr]['descricao'] = descricao
            rightdict[matr]['depto'] = depto
            rightdict[matr]['tipo'] = tipo

        qtddif = 0
        for linha in self.left:
            matr, nome, codfunc, descricao, depto, tipo = linha

            if rightdict.has_key(matr):
                # codfunc
                if (codfunc != rightdict[matr]['codfunc']) and (descricao.find("(I)") == -1):
                    qtddif += 1
                    rtxt("MATR: %s (%s): CODFUNC | de %s(%s) para %s(%s)" % (str(matr).ljust(5),
                                                                            nome.ljust(20)[0:17],
                                                                            rightdict[matr]['codfunc'],
                                                                            rightdict[matr]['descricao'],
                                                                            codfunc, descricao))
                    codfuncsql = "update empregados set codfunc = \"%s\" where matr = %s;" % (codfunc, matr)
                    rsql(codfuncsql)

                # departamento
                if (depto != rightdict[matr]['depto']):
                    qtddif += 1
                    rtxt("MATR: %s (%s):   DEPTO | de \"%s\" para \"%s\"" % (str(matr).ljust(5),
                                                                            nome.ljust(20)[0:17],
                                                                            rightdict[matr]['depto'],
                                                                            depto))
                    deptosql = "update empregados set depto = \"%s\" where matr = %s;" % (depto, matr)
                    rsql(deptosql)

                # nome
                if (levenshtein(nome.ljust(11), rightdict[matr]['nome'].ljust(11))) > 8:
                    qtddif += 1
                    rtxt("MATR: %s (%s):    NOME | de \"%s\" para \"%s\"" % (str(matr).ljust(5),
                                                                            nome.ljust(20)[0:17],
                                                                            rightdict[matr]['nome'].ljust(39),
                                                                            nome.ljust(39)))

                # tipo
                if (tipo != rightdict[matr]['tipo']):
                    qtddif += 1
                    rtxt("MATR: %s (%s):    TIPO | de \"%s\" para \"%s\" [avaliar: %s %s/%s]" % (str(matr).ljust(5),
                                                                            nome.ljust(20)[0:17],
                                                                            rightdict[matr]['tipo'],
                                                                            tipo,
                                                                            rightdict[matr]['depto'],
                                                                            descricao,
                                                                            rightdict[matr]['descricao']))
                    #ccustosql = "update empregados set tipo = \"%s\" where matr = %s;" % (tipo, matr)
                    #rsql(ccustosql)
            else:
                if tipo <> 2:
                    qtddif += 1
                    rtxt(u"""---------
Atenção: Matrícula %d nao existe na base -%s-:
matr:    %d
nome:    %s
codfunc: %d (%s)
depto:   %s
tipo:    %d
---------""" % (matr, self.rightname,
                matr, nome, codfunc, descricao, depto, tipo))

        #mudsql.sort()
        #mudtxt.sort()

        return [mudtxt, mudsql, qtddif]

class ComparaRpessiEmpregados(BaseSISPOS):
    findfiles = [ ('!RPESSI', ur'RELAÇÃO.*EFETIVO.*\.xlsx'),
                  ('EMPREG',  ur'empregados.txt')]


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
            matr = employee[0]
            nome = employee[1]
            depto = employee[2]
            codfunc = employee[3]
            prof = employee[6]
            tipo = employee[8]

            # add data
            entry = [matr, nome, codfunc, prof, depto,  tipo]

            retval.append(entry)

        return retval

    def getempregdata(self, _ed):

        ed_split = _ed.strip().split('\r\n')

        retval = []
        for line in ed_split:

            line_s = line.split("|")
            line_s = [x.strip() for x in line_s]

            #matr, nome, codfunc, descricao, depto, tipo = linha
            matr, nome, codfunc, descricao, depto, tipo, _ = line_s

            entry = (int(matr), nome, int(codfunc), descricao, depto, int(tipo))

            retval.append(entry)

        return retval

        #from code import interact; interact(local=locals())


    def process (self, f):

        rpessidata = self.getrpessidata(f['!RPESSI'])

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