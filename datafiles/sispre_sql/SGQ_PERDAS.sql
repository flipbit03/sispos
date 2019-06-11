-- SGQ_PERDAS
-- Soma todas as PERDAS de Ordens de Serviço de Cliente (não entram Internas)
-- O que são perdas:
--		códigos de atividade "21","23","24","80","92","93","94","95","96","97"
--		FA's que sejam de RETRABALHO (2a Fabricação)
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
	OS_VIEW p -- View que contém as listas de Ordens de Serviço do BENNER

where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- Cláusula principal:
	-- SOME:
	-- 1- FA's de RETRABALHO
	-- 2- Horas em códigos de atividade consideradas como PERDA
	and (
			(a.fkFA in (select pkFA from FA where fkTipoFA = 8))
		or 
			((ativ.codigo in ('21','23','24','80','92','93','94','95','96','97')))
	)

	-- Junte Ordem de Serviço do Benner
	and a.fkProjeto = p.HANDLE

	-- Filtre somente Ordens de Serviço de CLIENTES
	and a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Serviço de Clientes
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

-- GERA_GER_4 -- Somatório

select 
	sum(a.qtdHoraMin)/60.0 SGQ_PERDAS_@@MESNUM@@_@@ANONUM@@

from 
	Apropriacao a, 
	Atividade ativ,
	OS_VIEW p -- View que contém as listas de Ordens de Serviço do BENNER

where
	-- somente apropriação de HOMEM (não usar MÁQUINAS)
	a.fkTipoApropriacao = 1

	-- junte Atividades
	and a.fkAtividade = ativ.pkAtividade

	-- Cláusula principal:
	-- SOME:
	-- 1- FA's de RETRABALHO
	-- 2- Horas em códigos de atividade consideradas como PERDA
	and (
			(a.fkFA in (select pkFA from FA where fkTipoFA = 8))
		or 
			((ativ.codigo in ('21','23','24','80','92','93','94','95','96','97')))
	)

	-- Junte Ordem de Serviço do Benner
	and a.fkProjeto = p.HANDLE

	-- Filtre somente Ordens de Serviço de CLIENTES
	and a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Serviço de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)

	
	and a.fkPeriodo = @PERIODO;