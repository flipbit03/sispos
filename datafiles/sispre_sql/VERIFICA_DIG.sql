-- Verifica horários da digitacão

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 19;

select a.fkPeriodo, a.criadoPor, 
CONVERT(VARCHAR(12),a.dataHoraCriacao,103) AS 'Data_Digitacao',
CONVERT(VARCHAR(8),a.dataHoraCriacao,108) AS 'Hora_Digitacao',
CONVERT(VARCHAR(12),a.dataApropriacao,103) AS 'Data_Apropriacao'

from Apropriacao a where fkPeriodo = @PERIODO
order by fkPeriodo, criadoPor, dataHoraCriacao


