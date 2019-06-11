-- APEI:Tudo HM [Apropria��o praticada em Empregados do "I": TUDO - HORAS-M�QUINA]
-- Listagem de horas completa, por nome, sem agrupamentos. Usada para confer�ncias gerais e an�lises pertinentes � B�blia.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 1;

select
	p.ESTRUTURA ESTRUTURA_BENNER, p.APELIDO OS_ANTIGA, p.CODIGOREDUZIDO OS_REDUZIDA,
	
	-- Remove a 'hora' do objeto DateTime, para importar facilmente no Excel
	CAST(a.dataApropriacao as date) DATA,
	
	m.matricula CODMAQUINA ,m.nome NOME_MAQUINA,
	ativ.codigo cod_atividade,
	a.qtdHoraMin/60.0 hora, a.qtdHoraMin minutos

from
	Apropriacao a left outer join OS_VIEW p on a.fkProjeto = p.HANDLE, 
	Maquina m,
	TipoApropriacao ta,
	Atividade ativ
	-- Lista de Projetos ("OS") do Benner

where
	-- Junte TipoApropria��o, selecione propria��o de hora-m�quina
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'M�quina' and

	-- Junte m�quinas
	a.fkMaquina = m.pkMaquina and

	-- Junte projetos do Benner
	--a.fkProjeto = p.HANDLE and

	-- Junte atividade
	a.fkAtividade = ativ.pkAtividade

	and a.fkPeriodo = @PERIODO

order by p.ESTRUTURA, a.dataApropriacao, m.nome