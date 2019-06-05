-- SQL Horas Totais
-- Usado na construcao do indice CAPACIDADE INSTALADA
-- Atualizado para o novo sistema de apropria��o em 17-01-2018
-- Autor: Carlos Eduardo S.

--DECLARE @PERIODO AS INT = 15;
DECLARE @PERIODO AS INT = @@PERIODO@@;

-------------------------------------------------
-- IPU (Antigo IP-CUC) Horas Totais
-------------------------------------------------
select
	p.dataFechamento, dep.sigla, sum(a.qtdHoraMin)/60.0 HorasTotais_@@MESNUM@@_@@ANONUM@@
from
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- somente horas de m�o de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos espec�ficos
	and e.fkDepartamento = dep.pkDepartamento

	-- exclua alguns c�digos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo not in (35, 36, 37)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento, dep.sigla
order by p.dataFechamento, dep.sigla;