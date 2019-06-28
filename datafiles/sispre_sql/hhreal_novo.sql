-- HHREAL.SQL
-- Usado na produção dos dados/cálculos para a planilha ORÇADO x REAL
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 3;

select 
	a.fkPeriodo ID_PERIODO,
	CAST(pa.anoReferencia as varchar) + '-' + cast(pa.mesReferencia as varchar) ANO_MES_PERIODO,
	os.ESTRUTURA OS_BENNER, 
	os.CODIGOREDUZIDO OS_REDUZIDA, 
	f.nome Cargo, 
	replace(sum(a.qtdHoraMin)/60.0,'.',',')HHREAL_@@MESABREV@@_@@ANONUM@@

from
	Apropriacao a, TipoApropriacao t,
	Empregado e, Empresa emp, OS_VIEW os,
	PeriodoApropriacao pa, Funcao f

where 
	-- Joins
	a.fkPeriodo = pa.pkPeriodo and 
	a.fkTipoApropriacao = t.pkTipoApropriacao and
	a.fkEmpregado = e.pkEmpregado and 
	e.fkEmpresa = emp.pkEmpresa and
	e.fkFuncao = f.pkFuncao and
	a.fkProjeto = os.HANDLE and

	-- Apenas este periodo
	a.fkPeriodo = @PERIODO and

	-- Apropriação de Homem-Hora
	t.pkTipoApropriacao = 1

group by 
	a.fkPeriodo, pa.anoReferencia, pa.mesReferencia, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, f.nome

order by
	 os.ESTRUTURA, f.nome
