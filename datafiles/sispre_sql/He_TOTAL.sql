-- SQL HE_TOTAL
-- Usado para quantificar o total de horas extras apropriadas no per�odo.
-- Atualizado para o novo sistema de apropria��o em 19-01-2018
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select
	sum(a.qtdHoraMin)/60.0 SUM_71TOT_HE_@@MESNUM@@_@@ANONUM@@
from
	TipoHora th,
	PeriodoApropriacao p,
	Apropriacao a
where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- filtre somente HORAS TIPO 1 e 2 (horas extras 50% e 100%, respectivamente)
	and a.fkTipoHora = th.pkTipoHora
	and th.codigo in (1, 2)

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO;