-- CRIMES_HH
-- Usado na verificação de fechamento de mês
-- Lista todas as horas-homem para importação no Excel e posterior análise.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 1;

select
	e.matricula matricula,
	t.codigo turno,
	CONVERT(varchar, a.dataApropriacao,3) Data,
	th.codigo htipo,
	replace(sum(a.qtdHoraMin)/60.0,'.',',')CRIMES_HH_Horas_@@MESNUM@@_@@ANONUM@@,
	        sum(a.qtdHoraMin)              CRIMES_HH_Minut_@@MESNUM@@_@@ANONUM@@ 

from 
	Apropriacao a, 
	Empregado e,
	Turno t,
	TipoHora th,
	TipoApropriacao ta

where 
	a.fkTipoHora = th.pkTipoHora and
	a.fkTurno = t.pkTurno and
	a.fkEmpregado = e.pkEmpregado and

	-- apropriação de homem
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Homem' and

	-- selecione o periodo
	a.fkPeriodo = @PERIODO
group by 
	e.matricula, t.codigo, a.dataApropriacao, th.codigo
	
order by a.dataApropriacao, t.codigo, e.matricula;