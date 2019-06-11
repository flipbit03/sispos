-- SGQ_PERDAS
-- Soma todas as PERDAS de Ordens de Servi�o de Cliente (n�o entram Internas)
-- O que s�o perdas:
--		c�digos de atividade "21","23","24","80","92","93","94","95","96","97"
--		FA's que sejam de RETRABALHO (2a Fabrica��o)
--
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME, 
	sum(a.qtdHoraMin)/60.0 SGQ_PERDAS_@@MESNUM@@_@@ANONUM@@

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
	-- 1- FA's de RETRABALHO
	-- 2- Horas em c�digos de atividade consideradas como PERDA
	and (
			(a.fkFA in (select pkFA from FA where fkTipoFA = 8))
		or 
			((ativ.codigo in ('21','23','24','80','92','93','94','95','96','97')))
	)

	-- Junte Ordem de Servi�o do Benner
	and a.fkProjeto = p.HANDLE

	-- Filtre somente Ordens de Servi�o de CLIENTES
	and a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Servi�o de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)

	
	and a.fkPeriodo = @PERIODO

group by 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME

order by 
	APELIDO;

-- GERA_GER_4 -- Somat�rio

select 
	sum(a.qtdHoraMin)/60.0 SGQ_PERDAS_@@MESNUM@@_@@ANONUM@@

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
	-- 1- FA's de RETRABALHO
	-- 2- Horas em c�digos de atividade consideradas como PERDA
	and (
			(a.fkFA in (select pkFA from FA where fkTipoFA = 8))
		or 
			((ativ.codigo in ('21','23','24','80','92','93','94','95','96','97')))
	)

	-- Junte Ordem de Servi�o do Benner
	and a.fkProjeto = p.HANDLE

	-- Filtre somente Ordens de Servi�o de CLIENTES
	and a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Servi�o de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)

	
	and a.fkPeriodo = @PERIODO;