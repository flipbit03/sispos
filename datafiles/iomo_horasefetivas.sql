-- SQL Horas Efetivas
-- Usado na construcao do indice CAPACIDADE INSTALADA e IOMO
-- Atualizado para o novo sistema de apropria��o em 17-01-2018
-- Autor: Carlos Eduardo S.

--DECLARE @PERIODO AS INT = 15;
DECLARE @PERIODO AS INT = @@PERIODO@@;

-------------------------------------------------
-- Horas Efetivas
-------------------------------------------------
select
	p.dataFechamento, dep.sigla, sum(a.qtdHoraMin)/60.0 HorasEfetivas_@@MESNUM@@_@@ANONUM@@
from
	PeriodoApropriacao p,
	Empregado e,
	Apropriacao a,
	TipoMaoObra tmo,
	Departamento dep,
	Atividade ativ
where
	-- somente apropria��o de HOMEM (n�o usar M�QUINAS)
	a.fkTipoApropriacao = 1

	-- junte empregados
	and a.fkEmpregado = e.pkEmpregado

	-- somente horas de m�o de obra direta (funcionario tipo "0")
	and e.fkTipoMaoObra = tmo.pkTipoMaoObra
	and tmo.codigo = 0

	-- apenas departamentos espec�ficos
	and e.fkDepartamento = dep.pkDepartamento

	-- inclua somente at� a serie 80 e depois exclua alguns c�digos de atividade especificos
	and a.fkAtividade = ativ.pkAtividade
	and ativ.codigo between 0 and 81
	and ativ.codigo not between 21 and 37

	-- escolha o periodo
	and a.fkPeriodo = p.pkPeriodo
	and p.pkPeriodo = @PERIODO

group by p.dataFechamento, dep.sigla
order by p.dataFechamento, dep.sigla;