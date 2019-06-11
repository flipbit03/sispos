-- OCIOSIDADE NO MES
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;

select emp.nome Empresa,
os.ESTRUTURA PROJETO_BENNER, 
os.APELIDO OS_ANTIGA, 
os.CODIGOREDUZIDO OS_REDUZIDA, 
os.NOME,
f.nome Funcao, 
replace(sum(a.qtdHoraMin)/60.0,'.',',')Total_Ociosidade_@@MESNUM@@_@@ANONUM@@

from
Apropriacao a, TipoApropriacao t, Empregado e, Empresa emp, Funcao f, OS_VIEW os, Atividade ativ
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
--and os.ESTRUTURA in 
-- 22.000.0000                36.000.0000                   83.022.0000
--('101.05106.01.0410.0009.03', '101.05106.01.0611.0017.01', '195.11739.19.0410.0022.01')

-- ativ 24
and a.fkAtividade = ativ.pkAtividade
and ativ.codigo = '24'

group by emp.nome, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, os.NOME, f.nome
order by emp.nome, os.ESTRUTURA, f.nome;

-- AVULSO OCIOSIDADE -- nomes
-- Autor: Carlos Eduardo S.

select emp.nome Empresa,
os.ESTRUTURA PROJETO_BENNER, 
os.APELIDO OS_ANTIGA, 
os.CODIGOREDUZIDO OS_REDUZIDA, 
os.NOME,
e.matricula,
e.nome,
f.nome Funcao, 
replace(sum(a.qtdHoraMin)/60.0,'.',',')Total_Ociosidade_@@MESNUM@@_@@ANONUM@@

from
Apropriacao a, TipoApropriacao t, Empregado e, Empresa emp, Funcao f, OS_VIEW os, Atividade ativ
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
--and os.ESTRUTURA in 
-- 22.000.0000                36.000.0000                   83.022.0000
--('101.05106.01.0410.0009.03', '101.05106.01.0611.0017.01', '195.11739.19.0410.0022.01')

-- ativ 24
and a.fkAtividade = ativ.pkAtividade
and ativ.codigo = '24'

group by emp.nome, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, os.NOME, e.matricula, e.nome, f.nome
order by emp.nome, os.ESTRUTURA, f.nome

