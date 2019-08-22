-- APEI:Tudo [Apropriação praticada em Empregados do "I": TUDO]
-- Listagem de horas completa, por nome, sem agrupamentos. Usada para conferências gerais e análises pertinentes à Bíblia.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 7;

select
	p.ESTRUTURA ESTRUTURA_BENNER, p.APELIDO OS_ANTIGA, p.CODIGOREDUZIDO OS_REDUZIDA, p.NOME,
	COALESCE(CAST(fa.pkFA as varchar), '') 'FA', 
	COALESCE(operfa.numero, '') 'OF',
	
	-- Remove a 'hora' do objeto DateTime, para importar facilmente no Excel
	CAST(a.dataApropriacao as date) DATA,
	CAST(pa.anoReferencia as varchar) + '-' + cast(pa.mesReferencia as varchar) PERIODO,

	e.matricula, e.nome,
	f.nome funcao,
	d.sigla,
	emp.nome,
	ativ.codigo cod_atividade,
	
	a.qtdHoraMin/60.0 hora, a.qtdHoraMin minutos

from
	Apropriacao a 
		left outer join FA fa on a.fkFA = fa.pkFA
		left outer join OperacaoFA operfa on a.fkOperacaoFA = operfa.pkOperacaoFA
		left outer join PeriodoApropriacao pa on a.fkPeriodo = pa.pkPeriodo,
	Empregado e,
	Funcao f,
	Departamento d,
	Empresa emp,
	TipoApropriacao ta,
	Atividade ativ,
	-- Lista de Projetos ("OS") do Benner
	OS_VIEW p

where
	-- Junte tabelas gerais
	a.fkEmpregado = e.pkEmpregado and
	e.fkFuncao = f.pkFuncao and
	e.fkDepartamento = d.pkDepartamento and
	e.fkEmpresa = emp.pkEmpresa and

	-- Junte projetos do Benner
	a.fkProjeto = p.HANDLE and

	-- Junte atividade
	a.fkAtividade = ativ.pkAtividade and

	-- Junte TipoApropriação, selecione propriação de hora-homem
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Homem' and

	-- Junte Empresa
	e.fkEmpresa = emp.pkEmpresa

	and a.fkPeriodo = @PERIODO

order by a.dataApropriacao, e.matricula