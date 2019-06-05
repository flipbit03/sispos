#!python3
# -*- coding: utf-8 -*-

from typing import Dict

import sys
from sisposbase.sispos import BaseSISPOS

from analysis import analysis_list


class SisposRunner:
    @staticmethod
    def buildmenu() -> Dict[str, BaseSISPOS]:
        r = {}
        for a in analysis_list:
            r[a.__name__] = a
        return r

    def __init__(self):
        self.menu = self.buildmenu()

    @staticmethod
    def banner():
        print(
            "\n"
            "######################\n"
            "SISPOS -- Análises, Ferramentas e Relatórios de Apropriação de Mão de Obra\n"
            "######################\n"
        )

    def run(self, chosen=""):
        self.banner()

        runnable = self.chooseanalysis(chosen)

        # instantiate and run the analysis
        analysis = runnable()  # type: BaseSISPOS
        analysis.run()

        # print(f"our runnable is {runnable.__name__}")

    def chooseanalysis(self, chosen="") -> BaseSISPOS:

        # A name was given
        if chosen:
            if chosen in self.menu:
                # return runnable
                return self.menu[chosen]
            else:
                print(f'Erro: Não existe análise de nome "{chosen}"')
                exit(1)

        # No name? Print menu and ask for choice.
        print("Escolha a ferramenta pelo número:\n---------------------------------")

        runnables_by_number = {}
        for analysis_name, i in zip(self.menu, range(1, len(self.menu) + 1)):
            runnables_by_number[i] = self.menu[analysis_name]
            print(f"({i}) {analysis_name} - {self.menu[analysis_name].__doc__}")
        print("")

        ans = 0
        while ans not in runnables_by_number:
            try:
                ans = int(input("Escolha a ferramenta pelo numero --> "))
            except ValueError:
                ans = -1

            if ans == 0:
                print("Saindo do programa...")
                exit(1)

            if ans not in runnables_by_number:
                print("Opção inválida. Selecione pelo número ou tecle 0 para sair")
                continue
            else:
                print("")
                return runnables_by_number[ans]


if __name__ == "__main__":
    z = SisposRunner()

    chosen_analysis_name = ""
    if len(sys.argv) == 2:
        chosen_analysis_name = sys.argv[1].strip()

    try:
        z.run(chosen_analysis_name)
    except Exception as e:
        print("")
        print(f"Erro Fatal: {e}")
        exit(1)
