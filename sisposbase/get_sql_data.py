# -*- coding: windows-1252 -*-
import re, subprocess
import os, tempfile, shutil
import subprocess
from collections import namedtuple

# Executable path of the program that connects to the Database
sqlrunner_path = os.path.join(os.getcwd(), "tools", "SingleSQLExecutor.exe")

# Exectuable path of the program that lists periods in ControleProducao system
listaperiodosconsole_path = os.path.join(
    os.getcwd(), "tools", "ListaPeriodosConsole.exe"
)


def lesplit(regex, prompt="", _input=""):
    if _input:
        a = _input
        print("{} --> {}".format(prompt, _input))
    else:
        a = input(prompt + " --> ")
    rec = re.compile(regex)
    return [a] + list(rec.match(a).groups())


def le_int(prompt):
    a = lesplit("([0-9]+)", prompt)
    a[1] = int(a[1])
    return a[1]


def getsqldata(sqlcode: str):
    # Create TMPDIR
    tmpdir = tempfile.mkdtemp()

    sqlfp = os.path.join(tmpdir, "sqlcode.sql")
    with open(sqlfp, "wb") as sqlf:
        sqlf.write(sqlcode.encode())

    outf = os.path.join(tmpdir, "out.txt")

    # Run it!
    process = subprocess.run([sqlrunner_path, sqlfp, outf], capture_output=True)

    # Bail if failed
    if process.returncode != 0:
        print("Erro: Não foi possível executar o Relatório SQL\n")
        errmsg = process.stdout.decode()
        print(errmsg)
        exit(0)

    # Read data
    with open(outf, "rb") as data:
        _ed = data.read().decode("windows-1252")

    # Delete tempdir
    shutil.rmtree(tmpdir)

    # Get all queries.
    result_sets = _ed.strip().split("\r\n\r\n")

    retval = []
    for resultset, resultsetno in zip(result_sets, range(len(result_sets))):
        rss = [x.strip().split("|")[:-1] for x in resultset.split("\r\n")]

        # First line is always the header, ignore the last field which is always blank.
        headerfields = [field.strip() for field in rss[0]]

        # Build a namedtuple custom type based on this.
        ResultSet = namedtuple(f"result{resultsetno:02}", headerfields)

        query_retval = []
        for resulttuple in rss:
            record = ResultSet(*resulttuple)
            query_retval.append(record)

        retval.append(query_retval)

    return retval


def get_periodo_data():
    svar = {}

    # Run and display ListaPeriodosConsole.exe
    pg_output = subprocess.check_output(listaperiodosconsole_path)
    pgou = pg_output.decode("cp850")
    print(pg_output.decode("cp850"))

    # Extract all periodos from the output
    pt = r"ID=([0-9]+)\W+ \[([0-9]+)\/([0-9]+)\] \[(.*)\] de ([0-9\/]*) até ([0-9\/]*)"
    db = re.findall(pt, pgou, re.MULTILINE)

    dbd = {}
    for entry in db:
        perid, mes, ano, status, dtini, dtfim = entry
        dbd[int(perid)] = (mes, ano, status, dtini, dtfim)

    #print("---\nEntre com os seguintes parametros:\n---")

    svar["PERIODO"] = le_int("ID DO PERIODO DE APROPRIACAO")

    # error out if incorrect periodnumber
    if not svar["PERIODO"] in dbd.keys():
        raise Exception("Periodo Invalido")

    # from periodo de apropriacao infer other needed variables
    mes, ano, status, dtini, dtfim = dbd[svar["PERIODO"]]

    # update mes and ano to XX format
    mes = "{:02}".format(int(mes))
    ano = "{:02}".format(int(ano))

    return svar["PERIODO"], mes, ano, status, dtini, dtfim


def get_periodo_additional_data(periodoid):
    sqlcode = f"""
    -- 00parametros.sql
    -- Listagem dos Parâmetros de Digitação para o Período Selecionado
    -- Autor: Carlos Eduardo S.
    
    DECLARE @PERIODO AS INT = {periodoid};
    
    declare @datainicio as datetime = (select dataInicio     from PeriodoApropriacao p where p.pkPeriodo = @PERIODO);
    declare @datafim    as datetime = (select datafim        from PeriodoApropriacao p where p.pkPeriodo = @PERIODO);
    declare @datafech   as datetime = (select dataFechamento from PeriodoApropriacao p where p.pkPeriodo = @PERIODO);
    declare @mesperiodo as integer  = (select mesReferencia  from PeriodoApropriacao p where p.pkPeriodo = @PERIODO);
    declare @anoperiodo as integer  = (select anoReferencia  from PeriodoApropriacao p where p.pkPeriodo = @PERIODO);
    
    ----------------------------------------------------------
    -- Lista Parametros do PERIODO e Quantidade de Dias Úteis  
    ----------------------------------------------------------
    select @PERIODO ID_PERIODO, 
        @mesperiodo Mes,
        @anoperiodo Ano,
        CONVERT(VARCHAR,@dataInicio ,103) Data_Inicial_Periodo, 
        CONVERT(VARCHAR,@datafim    ,103) Data_Fim_Periodo,
        CONVERT(VARCHAR,@datafech   ,103) Data_Fechamento;
    
    ----------------------------------------------------------
    -- Quantidade de Dias Úteis  
    ----------------------------------------------------------
    with 
    daterange as (  
        SELECT TOP (DATEDIFF(DAY, @datainicio, @datafim) + 1) 
        n = ROW_NUMBER() OVER (ORDER BY [object_id])
        FROM sys.all_objects
        ),
    feriados as (
        select f.data Dia
        from Feriado f join TipoHora t on f.fkTipoHora = t.pkTipoHora 
        where data between @datainicio and @datafim
        and t.codigo in (1,2)
        ),
    dias_uteis as (
        SELECT DATEADD(DAY, n-1, @datainicio) dia_util
        FROM daterange
        where 
        datepart(weekday, DATEADD(DAY, n-1, @datainicio)) in (2,3,4,5,6) and
        DATEADD(DAY, n-1, @datainicio) not in (select * from feriados))
    select 
        count(*) QTD_DIAS_UTEIS from dias_uteis;
    
    
    ----------------------------------------------------------
    -- Lista Digitação, data mínima e máxima
    ----------------------------------------------------------
    select 
        CONVERT(VARCHAR,min(dataApropriacao),103) data_minima_digitada, 
        CONVERT(VARCHAR,max(dataApropriacao),103) data_maxima_digitada 
    from Apropriacao a 
    where a.fkPeriodo = @PERIODO;
    
    ----------------------------------------------------------
    -- Lista feriados
    ----------------------------------------------------------
    select 
        CONVERT(VARCHAR,f.data,103) Dia, 
        f.descricao Descricao,
        t.codigo TIPO_DE_HORA 
    from Feriado f join TipoHora t on f.fkTipoHora = t.pkTipoHora 
    where data between @datainicio and @datafim
    order by f.data
    
    """

    data = getsqldata(sqlcode)

    # Working Days in the Period
    dias_uteis = int(data[1][1][0])

    # Type=1 and Type=2 holidays.
    dias_1 = []
    dias_2 = []
    for line in data[3][1:]:
        dia, descricao, tipohora = line
        if int(tipohora) == 1:
            dias_1.append(line)

        if int(tipohora) == 2:
            dias_2.append(line)

    return dias_uteis, dias_1, dias_2
