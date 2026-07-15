# Guia de Funções

### `library.py`
Lista todas as funções dos diferentes arquivos mostrando quantidade e em qual arquivo está presente (caso não esteja em todos) 

**Exemplo de Saída:**
```
Função                                 Uso   Arquivos
------------------------------------------------------------------------------------------------------------------------
DJacobiP                               35x   Todos os arquivos
LagrangeBasis                           1x   Traffic-Flow-1D-Nodal-Sub-cell-shock-cap-smooth-eps.py
ViscousBurgers                          1x   Viscous-Burgers-1D-Modal.py
```

### `analyzer.py`
Lista todas as funções de um arquivo.py selecionado pelo usuário (uma lista com todos os arquivos é disponibilizada para o usuário que deve escolher qual ele deseja inspecionar)

**Exemplo de Saída:**
```
================================================================================
ARQUIVOS PYTHON DISPONÍVEIS
================================================================================

[0] Allen-Cahn-1D-Modal-DG-BR2-v0.py (25 funções)
[1] Allen-Cahn-1D-Modal-DG-BR2.py (25 funções)
[2] Allen-Cahn-1D-Modal-DG.py (23 funções)

--------------------------------------------------------------------------------

Digite o número do arquivo que deseja analisar: 0

================================================================================
ANALISANDO: Allen-Cahn-1D-Modal-DG-BR2-v0.py
================================================================================
Número de funções: 25

DJacobiP                       ( 37 linhas)
    Chama: nenhuma
    Dependências:
       nenhuma
    Variáveis locais:
       - DPm
       - DPn1
       - Pn0
       - Pn1
       - Pn2
       - a1n
       - a2n
       - a3n
       - a4n
       - alpha
       - b1n
       - b2n
       - b3n
       - beta
       - m
       - n
       - r
```
### `analyzer_compara.py`
Pode ser utilizada para encontrar diferenças funções com mesmo nome em scripts diferentes (usa `hash` e `AST`)

**Exemplo de saída:**
```
Arquivos disponíveis:
----------------------------------------
[0] Allen-Cahn-1D-Modal-DG-BR2-v0.py
[1] Allen-Cahn-1D-Modal-DG-BR2.py

----------------------------------------

Digite o número do primeiro arquivo: 0
Digite o número do segundo arquivo: 1

================================================================================
Allen-Cahn-1D-Modal-DG-BR2-v0.py
X
Allen-Cahn-1D-Modal-DG-BR2.py
================================================================================

================================================================================
RESULTADO DA COMPARAÇÃO
================================================================================
Função                         Status                                       
---------------------------------------------------------------------------
DJacobiP                       ✅ Idêntica (Hash+AST)                        
DLiftMatrix                    ✅ Idêntica (Hash+AST)                        
DMatrix1D                      ✅ Idêntica (Hash+AST)                        
DflipLiftMatrix                ✅ Idêntica (Hash+AST)                        
Euler                          ✅ Idêntica (Hash+AST)                        
FluxProjection                 ✅ Idêntica (Hash+AST)                        
Grad2SitffMatrix               ✅ Idêntica (Hash+AST)                        
IC                             ✅ Idêntica (Hash+AST)                        
JacobiGaussQuad                ✅ Idêntica (Hash+AST)                        
JacobiGaussWeights             ✅ Idêntica (Hash+AST)                        
JacobiP                        ✅ Idêntica (Hash+AST)                        
JacobiRoots                    ✅ Idêntica (Hash+AST)                        
Jacobian                       ✅ Idêntica (Hash+AST)                        
LegendreBasis                  ✅ Idêntica (Hash+AST)                        
Lh                             ⚠️ Hash diferente, AST igual                 
LiftMatrix                     ✅ Idêntica (Hash+AST)                        
MeshGen1D                      ✅ Idêntica (Hash+AST)                        
Periodic                       ✅ Idêntica (Hash+AST)                        
RK4                            ✅ Idêntica (Hash+AST)                        
RKSSP104                       ✅ Idêntica (Hash+AST)                        
RKSSP54                        ✅ Idêntica (Hash+AST)                        
StiffMatrix                    ✅ Idêntica (Hash+AST)                        
Timestep                       ✅ Idêntica (Hash+AST)                        
d2PQ                           ✅ Idêntica (Hash+AST)                        
dPQ                            ✅ Idêntica (Hash+AST)                        
================================================================================
```
