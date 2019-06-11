-- SGQ_DISPONIVELPRODUTIVO
-- Soma todas as horas de clientes no período analisado e algumas horas de códigos de atividade específicos (em qualquer OS)
-- Atualizado para o novo sistema de apropriação em 19-01-2018
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME, 
	sum(a.qtdHoraMin)/60.0 SGQ_DISPONIVELPRODUTIVO_@@MESNUM@@_@@ANONUM@@

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
	-- 1- Todas as horas apropriadas nas Ordens de Serviço de CLIENTE
	-- 2- Horas em códigos de atividade (21, 23, 24), neste caso em QUALQUER OS (mesmo internas).
	and (
	
		(a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Serviço de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)
		) or (
		(ativ.codigo in (21, 23, 24))
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


-- GERA_GER_2 - somatório

select 
	sum(a.qtdHoraMin)/60.0 SGQ_DISPONIVELPRODUTIVO_@@MESNUM@@_@@ANONUM@@
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
	-- 1- Todas as horas apropriadas nas Ordens de Serviço de CLIENTE
	-- 2- Horas em códigos de atividade (21, 23, 24), neste caso em QUALQUER OS (mesmo internas).
	and (
	
		(a.fkProjeto in (SELECT HANDLE
						FROM ControleProducao.dbo.OS_VIEW
						where 
						-- Somente Ordens de Serviço de Clientes
						not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)
		) or (
		(ativ.codigo in (21, 23, 24))
		)
	)

	and a.fkProjeto = p.HANDLE

	and a.fkPeriodo = @PERIODO;