-- 00parametros.sql
-- Listagem dos Parâmetros de Digitação para o Período Selecionado
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 14;

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

