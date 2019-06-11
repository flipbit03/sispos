import re, os
from csv import reader

a = os.getcwd()

import json

for fname in [x for x in os.listdir() if re.search('csv$', x)]:
    print(fname)

    with open(fname, mode='r') as f:
        fd = f.readlines()

    csvfile = reader(fd, delimiter=';')

    out = {}

    # <class 'list'>: ['grupo', 'func', 'arquivo', 'tipo', 'emp', 'arqout', 'unload?']
    for line in [t for t in csvfile][1:]:
        lines = [l.strip() for l in line]

        _, _, arquivo, _, _, arqout, _ = lines

        print(f"{arquivo} -- {arqout}")

        out[arquivo] = arqout


    with open(os.path.splitext(fname)[0]+'.json',mode='w') as of:
        of.write(json.dumps(out, indent=4))


    print(fd)







pass