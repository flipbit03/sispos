-- ATIV_EMP
-- Total de Horas por FUNCAO e por CODIGO de ATIVIDADE
-- Mostra a EMPRESA a que se refere a linha.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 1;

select
	f.nome funcao,
	ativ.codigo codigo_atividade,
	sum(a.qtdHoraMin)/60.0 ATIV_EMP_@@MESNUM@@_@@ANONUM@@,
	emp.nome empresa

from
	Funcao f,
	Atividade ativ,
	Apropriacao a, 
	Empregado e,
	Empresa emp,
	TipoApropriacao ta

where 
	-- Junte tabelas gerais
	a.fkEmpregado = e.pkEmpregado and
	a.fkAtividade = ativ.pkAtividade and
	e.fkFuncao = f.pkFuncao and
	e.fkEmpresa = emp.pkEmpresa and

	-- Junte TipoApropriação, selecione propriação de hora-homem
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Homem' and

	-- Junte Empresa
	e.fkEmpresa = emp.pkEmpresa
		
	and a.fkPeriodo = @PERIODO

group by
	f.nome, ativ.codigo, emp.nome

order by 
	ativ.codigo, f.nome, emp.nome;