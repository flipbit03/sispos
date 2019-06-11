-- HHREAL.SQL
-- Usado na produção dos dados/cálculos para a planilha ORÇADO x REAL
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 3;

select 
	a.fkPeriodo Periodo, 
	os.ESTRUTURA PROJETO_BENNER, 
	os.APELIDO OS_ANTIGA, 
	os.CODIGOREDUZIDO OS_REDUZIDA, 
	f.nome Funcao, 
	d.sigla Depto,
	at.codigo Atividade, 
	a.fkFA FA,
	-- somatório de horas convertido em base 10
	replace(sum(a.qtdHoraMin)/60.0,'.',',')HHREAL_@@MESABREV@@_@@ANONUM@@

from
	Apropriacao a, TipoApropriacao t,
	Empregado e, Empresa emp, Funcao f, OS_VIEW os,
	Departamento d, Atividade at

where 
	-- Joins
	a.fkTipoApropriacao = t.pkTipoApropriacao and
	a.fkEmpregado = e.pkEmpregado and 
	e.fkEmpresa = emp.pkEmpresa and
	e.fkFuncao = f.pkFuncao and
	a.fkProjeto = os.HANDLE and
	e.fkDepartamento = d.pkDepartamento and
	a.fkAtividade = at.pkAtividade and

	-- Apenas este periodo
	a.fkPeriodo = @PERIODO and

	-- Apropriação de Homem-Hora
	t.pkTipoApropriacao = 1 and

	-- Apenas atividades específicas 
	at.codigo between 00 and 97 and
	at.codigo not between 21 and 37

group by 
	a.fkPeriodo, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, f.nome, at.codigo, d.sigla, a.fkFA

order by
	 os.ESTRUTURA, f.nome, d.sigla, a.fkFA, at.codigo

