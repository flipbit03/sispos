-- SGQ_DISPONIVELTOTAL
-- Soma todas as horas de clientes no per�odo analisado e algumas horas de c�digos de atividade espec�ficos (em qualquer OS), incluindo FALTA(34)
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME, 
	sum(a.qtdHoraMin)/60.0 SGQ_DISPONIVELTOTAL_@@MESNUM@@_@@ANONUM@@

from 
	Apropriacao a, 
	Atividade ativ,
	OS_VIEW p -- View que cont�m as listas de Ordens de Servi�o do BENNER

where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- Cl�usula principal:
	-- SOME:
	-- 1- Todas as horas apropriadas nas Ordens de Servi�o de CLIENTE
	-- 2- Horas em c�digos de atividade (21, 23, 24), neste caso em QUALQUER OS (mesmo internas).
	and (
	
		(a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Servi�o de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)
		) or (
		(ativ.codigo in (21, 23, 24, 34))
		)
	)

	and a.fkProjeto = p.HANDLE

	
	and a.fkPeriodo = @PERIODO

group by 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME

order by 
	APELIDO;


-- GERA_GER_3 - somat�rio

select 
	sum(a.qtdHoraMin)/60.0 SGQ_DISPONIVELTOTAL_@@MESNUM@@_@@ANONUM@@
from 
	Apropriacao a, 
	Atividade ativ,
	OS_VIEW p -- View que cont�m as listas de Ordens de Servi�o do BENNER

where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- Cl�usula principal:
	-- SOME:
	-- 1- Todas as horas apropriadas nas Ordens de Servi�o de CLIENTE
	-- 2- Horas em c�digos de atividade (21, 23, 24), neste caso em QUALQUER OS (mesmo internas).
	and (
	
		(a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Servi�o de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)
		) or (
		(ativ.codigo in (21, 23, 24, 34))
		)
	)

	and a.fkProjeto = p.HANDLE

	
	and a.fkPeriodo = @PERIODO;