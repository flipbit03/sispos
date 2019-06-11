-- APROP_SEM_OS
-- Listagem de apropriações com ORDEM DE SERVIÇO EM BRANCO (Erro!)
-- Usado na verificação pré-fechamento "CRIMES"
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 1;

select 
	a.fkPeriodo, CONVERT(varchar, a.dataApropriacao,3) Data, ta.nome, 
	e.matricula MATR_EMP, e.nome NOME_EMP, 
	m.matricula MATR_MAQ, m.nome NOME_MAQ,
	at.codigo, a.qtdHoraMin/60

from Apropriacao a
		left outer join Empregado e on a.fkEmpregado = e.pkEmpregado
		left outer join Maquina m on a.fkMaquina = m.pkMaquina
				
, Atividade at, TipoApropriacao ta

where
	a.fkAtividade = at.pkAtividade and 
	a.fkTipoApropriacao = ta.pkTipoApropriacao and 
	fkProjeto is null and
	fkPeriodo = @PERIODO
