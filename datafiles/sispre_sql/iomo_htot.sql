-- SQL Horas Totais
-- Usado na construcao do indice CAPACIDADE INSTALADA
-- Atualizado para o novo sistema de apropriação em 17-01-2018
-- Autor: Carlos Eduardo S.

--DECLARE @PERIODO AS INT = 5;
DECLARE @PERIODO AS INT = @@PERIODO@@;

-------------------------------------------------
-- IPU (Antigo IP-CUC) Horas Totais
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IPCUC_HTOT_@@MESNUM@@_@@ANONUM@@
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

	-- exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo not in (35, 36, 37)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;

-------------------------------------------------
-- IPS + IPC (Antigo 'IPF todo') Horas Totais
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IPSIPCCM_HTOT_@@MESNUM@@_@@ANONUM@@
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
	and ativ.codigo not in (35, 36, 37)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;

-------------------------------------------------
-- IQ Horas Totais
-------------------------------------------------
select
	p.dataFechamento, sum(a.qtdHoraMin)/60.0 total_IQ_HTOT_@@MESNUM@@_@@ANONUM@@
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
	and ativ.codigo not in (35, 36, 37)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;

-- total

-------------------------------------------------
-- TOTAL HORAS TOTAIS
-------------------------------------------------
select
	sum(a.qtdHoraMin)/60.0 TOTAL_HORAS_TOTAIS_@@MESNUM@@_@@ANONUM@@
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
	and dep.sigla in  ('IPU', 'IPU/C', 'IPU/F', 'IPU/U',

		-- IPS + IPC (Antigo 'IPF todo')
		'IPS', 'IPS/S', 'IPS/TT',
		'IPC', 'IPC/M', 'IPC/T', 'IPC/C', 'IPC/MC', 'IPC/JP',
		-- IQ
		'IQ')

	-- exclua alguns códigos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo not in (35, 36, 37)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento
order by p.dataFechamento;