-- IG_REPAROAUTOCLAVE
-- Total de Horas por Período / Por Pessoa / Por Departamento
-- OS: Reparo da Autoclave
--
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 13;

select 
cast(p.mesreferencia as varchar) + '/' + cast(p.anoreferencia as varchar) MES_ANO,
os.ESTRUTURA PROJETO_BENNER,
os.APELIDO OS_ANTIGA,
os.CODIGOREDUZIDO OS_REDUZIDA,
e.matricula,
e.nome,
f.nome Funcao,
d.sigla Depto,
-- at.codigo Atividade, 
replace(sum(a.qtdHoraMin)/60.0,'.',',') Total

from
Apropriacao a, Empregado e, Funcao f, TipoApropriacao t, OS_VIEW os, Departamento d, Empresa emp, PeriodoApropriacao p
where 
a.fkTipoApropriacao = t.pkTipoApropriacao
and p.pkPeriodo = @PERIODO
and a.fkPeriodo = p.pkPeriodo
and t.pkTipoApropriacao = 1
and a.fkEmpregado = e.pkEmpregado
and e.fkEmpresa = emp.pkEmpresa
and e.fkFuncao = f.pkFuncao
and a.fkProjeto = os.HANDLE
and e.fkDepartamento = d.pkDepartamento
and os.ESTRUTURA like '101.11038.09.0117%'


group by p.mesReferencia, d.sigla, p.anoReferencia, os.ESTRUTURA, os.APELIDO, os.CODIGOREDUZIDO, e.matricula, e.nome, f.nome
order by os.ESTRUTURA

