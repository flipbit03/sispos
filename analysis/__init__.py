from sisposbase.sispos import BaseSISPOS

# Importa todas as análises.

# IOMO / CAPACIDADE INSTALADA
from .iomo_capacidadeinstalada import IomoCapac

# CRITICAS À APROPRIACAO
from .Criticas_HH_e_HM import Criticas

# COMPARA RELAÇÃO DE PESSOAL DO I COM EMPREGADOS
try:
    # Esta análise utiliza OpenPYXL, se não estiver disponível, pule.
    from .compara_rpessi_empregados import ComparaRpessiEmpregados
except ImportError:
    pass


# Gera a lista de análises listadas aqui, para importação no módulo principal.
analysis_list = sorted(
    [
        x
        for x in vars().values()
        if isinstance(x, type) and issubclass(x, BaseSISPOS) and x != BaseSISPOS
    ],
    key=lambda x: x.__name__,
)
