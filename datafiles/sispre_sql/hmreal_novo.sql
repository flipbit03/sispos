-- HM_POR_OS.SQL
-- Usado na produção dos dados/cálculos para a planilha ORÇADO x REAL
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 16;
--DECLARE @PERIODO AS INT = 3;

select 
	a.fkPeriodo Periodo, 
	CAST(pa.anoReferencia as varchar) + '-' + cast(pa.mesReferencia as varchar) ANO_MES_PERIODO,

	-- os
	os.ESTRUTURA PROJETO_BENNER, 
	os.CODIGOREDUZIDO OS_REDUZIDA, 
	
	-- matricula da maquina e nome da maquina
	m.matricula matr_maquina, m.nome nome_maquina,
	
	-- somatório de horas convertido em base 10
	replace(sum(a.qtdHoraMin)/60.0,'.',',')HM_POR_OS_@@MESABREV@@_@@ANONUM@@

from
	Apropriacao a, TipoApropriacao t,
	Maquina m, OS_VIEW os,
	PeriodoApropriacao pa

where 
	-- Joins
	a.fkPeriodo = pa.pkPeriodo and 
	a.fkTipoApropriacao = t.pkTipoApropriacao and
	a.fkMaquina = m.pkMaquina and 
	a.fkProjeto = os.HANDLE and

	-- Apenas este periodo
	a.fkPeriodo = @PERIODO and

	-- Apropriação de Hora-Máquina
	t.pkTipoApropriacao = 2

group by 
	a.fkPeriodo, pa.anoReferencia, pa.mesReferencia, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, m.matricula, m.nome

order by
	 os.ESTRUTURA, m.matricula

