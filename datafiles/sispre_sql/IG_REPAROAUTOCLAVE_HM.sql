-- IG_REPAROAUTOCLAVE_HM
-- Total de Horas-MAQUINA por Período / Por Máquina 
-- OS: Reparo da Autoclave
--
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 15;

select 
	cast(pa.mesreferencia as varchar) + '/' + cast(pa.anoreferencia as varchar) MES_ANO,
	P.ESTRUTURA PROJETO_BENNER, p.APELIDO OS_ANTIGA, p.CODIGOREDUZIDO OS_REDUZIDA,
	m.matricula CODMAQUINA ,m.nome NOME_MAQUINA,
	REPLACE(sum(a.qtdHoraMin)/60.0, '.',',') hora

from
	-- junte ordem de serviço do benner.
	Apropriacao a left outer join OS_VIEW p on a.fkProjeto = p.HANDLE, 
	Maquina m,
	TipoApropriacao ta,
	PeriodoApropriacao pa
	-- Lista de Projetos ("OS") do Benner

where
	-- Junte PeriodoApropriacao
	a.fkPeriodo = pa.pkPeriodo and

	-- Junte TipoApropriação, selecione propriação de hora-máquina
	a.fkTipoApropriacao = ta.pkTipoApropriacao and
	ta.nome = 'Máquina' and

	-- Junte máquinas
	a.fkMaquina = m.pkMaquina and

	-- Filtre o periodo
	a.fkPeriodo = @PERIODO and

	-- Escolha a OS pelo número antigo
	p.APELIDO = '1100600001'

group by pa.anoReferencia, pa.mesReferencia, P.ESTRUTURA, p.APELIDO, p.CODIGOREDUZIDO, m.matricula, m.nome