-- SQL IP_ATIV
-- Usado na construcao do indice ABSENTE�SMO -- Total de Horas apropriadas "IP", POR C�DIGO DE ATIVIDADE [usa-se apenas o 34]
-- Atualizado para o novo sistema de apropria��o em 19-01-2018
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select
	ativ.codigo, sum(a.qtdHoraMin)/60.0 t61_IPATIV_TOTAL_@@MESNUM@@_@@ANONUM@@
from
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	Atividade ativ,
	Departamento dep
where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- escolha apenas departamentos espec�ficos [Toda a ger�ncia IP]
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in
	('IP', 'IPL',
	'IPM', 'IPM-AAMM', 'IPM-AAME',
	'IPS', 'IPS/S', 'IPS/TT',
	'IPU', 'IPU/C', 'IPU/F', 'IPU/U',
	'IPC', 'IPC/M', 'IPC/T', 'IPC/C', 'IPC/MC', 'IPC/JP', 'IPC-IF')

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by ativ.codigo
order by ativ.codigo;

select
	sum(a.qtdHoraMin)/60.0 SUM_61_IPATIV_TOTAL_@@MESNUM@@_@@ANONUM@@
from
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	Atividade ativ,
	Departamento dep
where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- escolha apenas departamentos espec�ficos [Toda a ger�ncia IP]
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in
	('IP', 'IPL',
	'IPM', 'IPM-AAMM', 'IPM-AAME',
	'IPS', 'IPS/S', 'IPS/TT',
	'IPU', 'IPU/C', 'IPU/F', 'IPU/U',
	'IPC', 'IPC/M', 'IPC/T', 'IPC/C', 'IPC/MC', 'IPC/JP', 'IPC-IF')

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO;

