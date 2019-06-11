-- SGQ_TOTALFATURAVEL
-- Soma todas as horas de clientes no per�odo analisado.
-- Atualizado para o novo sistema de apropria��o em 19-01-2018
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME, 
	sum(a.qtdHoraMin)/60.0 SGQ_TOTALFATURAVEL_@@MESNUM@@_@@ANONUM@@

from 
	Apropriacao a, 
	Empregado e, 
	OS_VIEW p

where 
-- OS esteja dentro da lista de OS's de cliente do Benner
	a.fkProjeto in (SELECT HANDLE
					FROM ControleProducao.dbo.OS_VIEW
					where 
					-- Somente Ordens de Servi�o de Clientes
					not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%')))

	and a.fkProjeto = p.HANDLE
	and a.fkEmpregado = e.pkEmpregado

	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	and a.fkTipoApropriacao = 1
		
	and a.fkPeriodo = @PERIODO

group by 
	p.ESTRUTURA, 
	p.CODIGOREDUZIDO, 
	p.APELIDO, 
	p.NOME

order by 
	APELIDO;

-- GERA_GER_1 -- Somat�rio

select 
	sum(a.qtdHoraMin)/60.0 SGQ_TOTALFATURAVEL_@@MESNUM@@_@@ANONUM@@

from 
	Apropriacao a, 
	Empregado e, 
	OS_VIEW p

where 
-- OS esteja dentro da lista de OS's de cliente do Benner
	a.fkProjeto in (SELECT HANDLE
					FROM ControleProducao.dbo.OS_VIEW
					where 
					-- Somente Ordens de Servi�o de Clientes
					not ((ESTRUTURA like '195%') or (ESTRUTURA like '199%')))

	and a.fkProjeto = p.HANDLE
	and a.fkEmpregado = e.pkEmpregado

	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	and a.fkTipoApropriacao = 1
		
	and a.fkPeriodo = @PERIODO;