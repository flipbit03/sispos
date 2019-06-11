-- QT_FAL_MES
-- Usado na RELAÇÃO DE PESSOAL DO I para construção da Aba "Resumo Função"
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select
	e.nome, 
	e.matricula, 
	f.nome, 
	dep.sigla, 
	sum(a.qtdHoraMin)/60.0 QT_FAL_MES_@@MESNUM@@_@@ANONUM@@

from 
	PeriodoApropriacao p,
	Empregado e,
	Funcao f,
	Apropriacao a,
	Departamento dep,
	Atividade ativ,
	Empresa emp
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados e inclua somente os que sejam da empresa 'NUCLEP' (não inclua Empreiteira)
	and a.fkEmpregado = e.pkEmpregado
	and e.fkEmpresa = emp.pkEmpresa
	and emp.nome = 'NUCLEP'

	-- junte departamentos
	and e.fkDepartamento = dep.pkDepartamento

	-- junte profissão (função)
	and e.fkFuncao = f.pkFuncao	

	-- ATIVIDADE=34 apenas (Faltas Não Justificadas)
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo = 34

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by 
	e.nome, 
	e.matricula, 
	f.nome, 
	dep.sigla
order by 
	f.nome, 
	e.matricula, 
	e.nome, 
	dep.sigla
