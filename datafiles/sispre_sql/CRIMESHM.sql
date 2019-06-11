-- CRIMES_HM
-- Usado na verificação de fechamento de mês
-- Lista todas as horas-MÁQUINA para importação no Excel e posterior análise.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 1;

select
	m.matricula matricula_maquina,
	t.codigo turno,
	CONVERT(varchar, a.dataApropriacao,3) Data,
	th.codigo htipo,
	replace(sum(a.qtdHoraMin)/60.0,'.',',')CRIMES_HM_Horas_@@MESNUM@@_@@ANONUM@@,
		    sum(a.qtdHoraMin)              CRIMES_HM_Minut_@@MESNUM@@_@@ANONUM@@ 

from 
	Apropriacao a, 
	Maquina m,
	Turno t,
	TipoHora th,
	TipoApropriacao ta

where 
	a.fkTipoHora = th.pkTipoHora and
	a.fkTurno = t.pkTurno and
	a.fkMaquina = m.pkMaquina and

	-- apropriação de homem
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Máquina' and

	-- selecione o periodo
	a.fkPeriodo = @PERIODO
group by 
	m.matricula, t.codigo, a.dataApropriacao, th.codigo
	
order by a.dataApropriacao, t.codigo, m.matricula;