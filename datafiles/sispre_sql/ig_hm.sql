-- IGHM
-- Relatório para IG que lista as horas de máquinas em Ordens de Serviço específicas
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 2;

select 
os.ESTRUTURA PROJETO_BENNER, 
os.APELIDO OS_ANTIGA, 
os.CODIGOREDUZIDO OS_REDUZIDA, 
m.matricula Maquina,
replace(sum(a.qtdHoraMin)/60.0,'.',',')Total_@@MESABREV@@_@@ANONUM@@

from
Apropriacao a, TipoApropriacao t, Maquina m, OS_VIEW os
where 

-- escolha o período
a.fkPeriodo = @PERIODO and

-- somente homem
a.fkTipoApropriacao = t.pkTipoApropriacao and
t.pkTipoApropriacao = 2

-- junte empregado
and a.fkMaquina = m.pkMaquina

-- junte lista de os e filtre os específicas.
and a.fkProjeto = os.HANDLE
and os.ESTRUTURA in 
-- 22.000.0000                36.000.0000                   83.022.0000
('101.05106.01.0410.0009.03', '101.05106.01.0611.0017.01', '195.11739.19.0410.0022.01')

group by os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, m.matricula
order by os.ESTRUTURA

