select 
  e.matricula Matricula, 
  e.nome Nome, 
  f.nome Cargo, 
  d.sigla Departamento, 
  tmo.codigo TMO, tmo.nome TMO_Nome, 
  e.dataHoraAlteracao Data_Ultima_Alteracao

from
  Empregado e, Situacao s, Departamento d, Funcao f, TipoMaoObra tmo

where 

-- junte situacao
e.fkSituacao = s.pkSituacao and
s.nome = 'ativo' and

-- junte departamento
e.fkDepartamento = d.pkDepartamento and

-- junte funcao
e.fkFuncao = f.pkFuncao and

-- junte tipomaodeobra
e.fkTipoMaoObra = tmo.pkTipoMaoObra

order by e.matricula


