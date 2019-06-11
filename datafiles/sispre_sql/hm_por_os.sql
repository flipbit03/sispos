-- HM_POR_OS.SQL
-- Usado na produção dos dados/cálculos para a planilha ORÇADO x REAL
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 3;

select 
	a.fkPeriodo Periodo, 

	-- os
	os.ESTRUTURA PROJETO_BENNER, 
	os.APELIDO OS_ANTIGA, 
	os.CODIGOREDUZIDO OS_REDUZIDA, 
	
	-- matricula da maquina e nome da maquina
	m.matricula, m.nome,
	
	-- atividade
	at.codigo Atividade, 

	-- fa
	a.fkFA FA,
	-- somatório de horas convertido em base 10
	replace(sum(a.qtdHoraMin)/60.0,'.',',')HM_POR_OS_@@MESABREV@@_@@ANONUM@@

from
	Apropriacao a, TipoApropriacao t,
	Maquina m, OS_VIEW os,
	Atividade at

where 
	-- Joins
	a.fkTipoApropriacao = t.pkTipoApropriacao and
	a.fkMaquina = m.pkMaquina and 
	a.fkProjeto = os.HANDLE and
	a.fkAtividade = at.pkAtividade and

	-- Apenas este periodo
	a.fkPeriodo = @PERIODO and

	-- Apropriação de Hora-Máquina
	t.pkTipoApropriacao = 2

group by 
	a.fkPeriodo, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, m.matricula, m.nome, at.codigo, a.fkFA

order by
	 os.ESTRUTURA, m.matricula, at.codigo, a.fkFA

