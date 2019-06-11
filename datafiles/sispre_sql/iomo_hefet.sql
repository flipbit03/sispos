-- SQL Horas Efetivas
-- Usado na construcao do indice CAPACIDADE INSTALADA e IOMO
-- Atualizado para o novo sistema de apropriação em 17-01-2018 
-- Autor: Carlos Eduardo S.

--DECLARE @PERIODO AS INT = 5;
DECLARE @PERIODO AS INT = @@PERIODO@@;

-------------------------------------------------
-- IPU (Antigo IP-CUC) Horas Efetivas
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IPCUC_HEFET_@@MESNUM@@_@@ANONUM@@
from 
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado
	
	-- somente horas de mão de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos específicos
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in ('IPU', 'IPU/C', 'IPU/F', 'IPU/U')

	-- inclua somente até a serie 80 e depois exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo between 0 and 81
	and ativ.codigo not between 21 and 37

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;

-------------------------------------------------
-- IPS + IPC (Antigo 'IPF todo') Horas Efetivas
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IPSIPCCM_HEFET_@@MESNUM@@_@@ANONUM@@
from 
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado
	
	-- somente horas de mão de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos específicos
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in 
		-- IPS + IPC (Antigo 'IPF todo')
		('IPS', 'IPS/S', 'IPS/TT',
		'IPC', 'IPC/M', 'IPC/T', 'IPC/C', 'IPC/MC', 'IPC/JP')

	-- exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo between 0 and 81
	and ativ.codigo not between 21 and 37

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;

-------------------------------------------------
-- IQ Horas Efetivas
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IQ_HEFET_@@MESNUM@@_@@ANONUM@@
from 
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado
	
	-- somente horas de mão de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos específicos
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in 
		-- IQ
		('IQ')

	-- exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo between 0 and 81
	and ativ.codigo not between 21 and 37

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;


-- total

-------------------------------------------------
-- TOTAL HORAS EFETIVAS
-------------------------------------------------
select
	sum(a.qtdHoraMin)/60.0 TOTAL_HORAS_EFETIVAS_@@MESNUM@@_@@ANONUM@@
from 
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado
	
	-- somente horas de mão de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos específicos
	and e.fkDepartamento = dep.pkDepartamento
	and dep.sigla in 
	
	-- ipu
	('IPU', 'IPU/C', 'IPU/F', 'IPU/U',

	-- ips + ipc
	'IPS', 'IPS/S', 'IPS/TT',
	'IPC', 'IPC/M', 'IPC/T', 'IPC/C', 'IPC/MC', 'IPC/JP',

	--iq
	'IQ')

	-- inclua somente até a serie 80 e depois exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo between 0 and 81
	and ativ.codigo not between 21 and 37

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;