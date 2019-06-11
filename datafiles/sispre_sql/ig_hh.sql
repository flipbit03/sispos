-- IGHH
-- Relatório para IG que lista as horas em Ordens de Serviço específicas, por profissão.
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 2;

select emp.nome Empresa,
os.ESTRUTURA PROJETO_BENNER, 
os.APELIDO OS_ANTIGA, 
os.CODIGOREDUZIDO OS_REDUZIDA, 
f.nome Funcao, 
replace(sum(a.qtdHoraMin)/60.0,'.',',')Total_@@MESABREV@@_@@ANONUM@@

from
Apropriacao a, TipoApropriacao t, Empregado e, Empresa emp, Funcao f, OS_VIEW os
where 

-- escolha o período
a.fkPeriodo = @PERIODO and

-- somente homem
a.fkTipoApropriacao = t.pkTipoApropriacao and
t.pkTipoApropriacao = 1

-- junte empregado
and a.fkEmpregado = e.pkEmpregado

-- junte empresa
and e.fkEmpresa = emp.pkEmpresa

-- junte função
and e.fkFuncao = f.pkFuncao

-- junte lista de os e filtre os específicas.
and a.fkProjeto = os.HANDLE
and os.ESTRUTURA in 
-- 22.000.0000                36.000.0000                   83.022.0000
('101.05106.01.0410.0009.03', '101.05106.01.0611.0017.01', '195.11739.19.0410.0022.01')

group by emp.nome, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, f.nome
order by emp.nome, os.ESTRUTURA, f.nome

