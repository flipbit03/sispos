-- HHTOTESP_EMP
-- Total por OS e por FUNÇÃO de horas, separado por EMPRESA
-- Excluem-se códigos de atividade 34, 35, 36, 37
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 13;

select
	p.CODIGOREDUZIDO, p.NOME,
	p.APELIDO,
	p.CLIENTE,
	f.nome funcao,
	sum(a.qtdHoraMin)/60.0 HHTOTESP_EMP_@@MESNUM@@_@@ANONUM@@,
	emp.nome empresa

from
	Apropriacao a, 
	Empregado e,
	Funcao f,
	Empresa emp,
	TipoApropriacao ta,
	Atividade ativ,
	-- Lista de Projetos ("OS") do Benner
	OS_VIEW p

where
	-- Junte tabelas gerais
	a.fkEmpregado = e.pkEmpregado and
	e.fkFuncao = f.pkFuncao and
	e.fkEmpresa = emp.pkEmpresa and

	-- Junte projetos do Benner
	a.fkProjeto = p.HANDLE and

	-- Junte atividade e exclua atividades específicas
	a.fkAtividade = ativ.pkAtividade and
	ativ.codigo not in (34, 35, 36, 37) and

	-- Junte TipoApropriação, selecione propriação de hora-homem
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Homem' and

	-- Junte Empresa
	e.fkEmpresa = emp.pkEmpresa
		
	and a.fkPeriodo = @PERIODO

group by
	p.CODIGOREDUZIDO, p.NOME, p.APELIDO, p.CLIENTE, f.nome, emp.nome

order by 
	p.APELIDO, p.CODIGOREDUZIDO, p.NOME, p.CLIENTE, f.nome, emp.nome