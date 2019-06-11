-- HHREALINT.SQL
-- Usado na produ��o dos dados/c�lculos para a planilha HORAS REAIS INTERNAS
-- � id�ntico ao "Or�ado X Real" por�m agrupa todas as horas internas numa �nica 'super OS'
-- Autor: Carlos Eduardo S.

DECLARE @PERIODO AS INT = @@PERIODO@@;
--DECLARE @PERIODO AS INT = 3;

select 
	a.fkPeriodo Periodo,
	'os_interna' OS, 
	'os_interna' OS, 
	'os_interna' OS, 
	f.nome Funcao, 
	d.sigla Depto,
	at.codigo Atividade, 
	a.fkFA FA,
	-- somat�rio de horas convertido em base 10
	replace(sum(a.qtdHoraMin)/60.0,'.',',')HHREALINT_@@MESABREV@@_@@ANONUM@@

from
	Apropriacao a, TipoApropriacao t,
	Empregado e, Empresa emp, Funcao f, OS_VIEW os,
	Departamento d, Atividade at

where 
	-- Joins
	a.fkTipoApropriacao = t.pkTipoApropriacao and
	a.fkEmpregado = e.pkEmpregado and 
	e.fkEmpresa = emp.pkEmpresa and
	e.fkFuncao = f.pkFuncao and
	a.fkProjeto = os.HANDLE and
	e.fkDepartamento = d.pkDepartamento and
	a.fkAtividade = at.pkAtividade and

	-- Apenas este periodo
	a.fkPeriodo = @PERIODO and

	-- Apropria��o de Homem-Hora
	t.pkTipoApropriacao = 1 and

	-- Apenas atividades espec�ficas 
	at.codigo between 00 and 97 and
	at.codigo not between 21 and 37

	-- Filtre somente Ordens de Servi�o de CLIENTES
	and a.fkProjeto in (SELECT HANDLE
						FROM OS_VIEW
						where 
						-- Somente Ordens de Servi�o INTERNAS (195.xxx ou 199.xxx)
						((ESTRUTURA like '195%') or (ESTRUTURA like '199%'))
						)

group by 
	a.fkPeriodo, f.nome, at.codigo, d.sigla, a.fkFA

order by
	 f.nome, d.sigla, a.fkFA, at.codigo

