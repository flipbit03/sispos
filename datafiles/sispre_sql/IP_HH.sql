-- SQL IP_HH
-- Usado na construcao do indice ABSENTEÍSMO -- Total de Horas apropriadas "IP", por turno.
-- Atualizado para o novo sistema de apropriação em 19-01-2018
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select
	t.nome, sum(a.qtdHoraMin)/60.0 t61_IP_TOTAL_@@MESNUM@@_@@ANONUM@@
from
	Turno t,
	TipoHora th,
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	Departamento dep
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- junte turnos
	and a.fkTurno = t.pkTurno

	-- filtre somente HORAS TIPO 0 (horas normais, sem horas extras)
	and a.fkTipoHora = th.pkTipoHora
	and th.codigo = 0
	
	-- escolha apenas departamentos específicos [Toda a gerência IP]
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

group by t.nome
order by t.nome;


select
	sum(a.qtdHoraMin)/60.0 SUM_61_IP_TOTAL_@@MESNUM@@_@@ANONUM@@
from
	Turno t,
	TipoHora th,
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	Departamento dep
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- junte turnos
	and a.fkTurno = t.pkTurno

	-- filtre somente HORAS TIPO 0 (horas normais, sem horas extras)
	and a.fkTipoHora = th.pkTipoHora
	and th.codigo = 0
	
	-- escolha apenas departamentos específicos [Toda a gerência IP]
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