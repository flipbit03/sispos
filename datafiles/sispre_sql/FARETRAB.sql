-- FARETRAB
-- Lista todas as FA's de tipo "SEGUNDA FABRICAÇÃO"
-- Autor: Carlos Eduardo S.

select pkFA from FA where fkTipoFA = 8

order by pkFA;