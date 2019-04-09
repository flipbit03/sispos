# -*- coding: cp1252 -*-
import os
import re
import locale

def findfile(_searchdirectory, idname, regexp):
    searchdirectory = _searchdirectory
    retval = ""
    print("Procurando por %s dentro de \"%s\"..." % (idname.upper(), searchdirectory))
    flist = os.listdir(searchdirectory)
    flist.sort()
    compre = re.compile(regexp, re.IGNORECASE)
    arqs = [os.path.join(searchdirectory,a) for a in flist if os.path.isfile(os.path.join(searchdirectory,a))]
    matches = filter(lambda x: compre.search(os.path.basename(x)), arqs)

    for fname in matches:
        question = u"  O arquivo %s e realmente o arquivo \"%s\"? [s/n]:" % (idname.upper(), os.path.basename(fname))
        print(question,)
        if input().upper() == "S":
            retval = fname
            break

    if not retval:
        print("\tNao pude encontrar um arquivo com o nome procurado...")

    return retval

def findfilel(searchdirectory, idname, regexp):
    retval = ['', '']
    ffrv = findfile(searchdirectory, idname, regexp)
    if ffrv:
        ff = open(ffrv, 'rb')
        fd = ff.read()
        ff.close()
        retval[0] = ffrv
        retval[1] = fd
        

    return retval
    
        
