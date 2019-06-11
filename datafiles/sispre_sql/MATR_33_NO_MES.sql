-- MATR_33_NO_MES
-- Listagem de apropriações EM BRANCO no mês
-- Usado para análise e redução destas horas.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 2;

with matr_33_equipes as
(
select eq.nome Equipe, eq.fkApontador,
e.matricula Matricula_Funcionario_33, E.nome Nome_Funcionario, Convert(varchar(12), a.dataApropriacao, 103) Data_da_Apropriacao, sum(a.qtdHoraMin/60) Horas

from 
	Apropriacao a , Atividade ativ, 
	Empregado e left join Equipe eq on e.fkEquipe = eq.pkEquipe

where
	a.fkAtividade = ativ.pkAtividade and 
	a.fkEmpregado = e.pkEmpregado and
	fkPeriodo = @PERIODO and
	ativ.codigo = 33
group by
	eq.nome, eq.fkApontador, e.matricula, e.nome, a.dataApropriacao
	)
,

m_com_apontador as
(
select 
	m.Matricula_Funcionario_33, 
	m.Nome_Funcionario Nome_Funcionario_33, 
	m.Data_da_Apropriacao, 
	m.Horas, 
	e.nome Apontador, 
	e.matricula MatrApontador, 
	m.Equipe
from 
	matr_33_equipes m left join Empregado e on m.fkApontador = e.pkEmpregado
)
select 
	* into #matriculas33
from m_com_apontador
order by Apontador, Equipe, Matricula_Funcionario_33, Data_da_Apropriacao;

select * from #matriculas33


select m.Apontador, m.Equipe, sum(m.Horas) Total_Horas_33_No_Mes from #matriculas33 m
group by Apontador, m.Equipe
order by Total_Horas_33_No_Mes desc;


drop table #matriculas33;

--select * from #temptable1