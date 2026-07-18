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

### `analyzer_file.py`
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
        ...
       - b2n
       - b3n
       - beta
       - m
       - n
       - r
```
### `analyzer_compara_file.py`
Pode ser utilizada para encontrar diferenças funções com mesmo nome em arquivos/scripts diferentes (usa `hash` e `AST`)

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
...                                         
RKSSP54                        ✅ Idêntica (Hash+AST)                        
StiffMatrix                    ✅ Idêntica (Hash+AST)                        
Timestep                       ✅ Idêntica (Hash+AST)                        
d2PQ                           ✅ Idêntica (Hash+AST)                        
dPQ                            ✅ Idêntica (Hash+AST)                        
================================================================================
```

### `analyzer_compara_func.py`
Pode ser utilizada para encontrar em arquivos/scripts uma determinada função digitada pelo usuário.
* Lista os arquivos e se a função foi encontrada nele
* Faz o comparativo entre os arquivos que contém a função
* Gera uma matriz de comparação entre os arquivos no qual a função foi encontrada
* Resume quantas semelhanças, diferenças Hash e diferenças Hash&AST encontrou
* Possibilita a geração de um heatmap da tabela

**Exemplo de saída:**
```
================================================================================
🔍 ANALISADOR DE FUNÇÕES ENTRE MÚLTIPLOS ARQUIVOS
================================================================================

🔤 Digite o nome da função para analisar (ou 'sair' para encerrar): epscompactsmoother

🔍 Procurando função 'epscompactsmoother' em todos os arquivos...
------------------------------------------------------------
❌ Allen-Cahn-1D-Modal-DG-BR2-v0.py - Função 'epscompactsmoother' NÃO encontrada
❌ Allen-Cahn-1D-Modal-DG-BR2.py - Função 'epscompactsmoother' NÃO encontrada
❌ Allen-Cahn-1D-Modal-DG.py - Função 'epscompactsmoother' NÃO encontrada
...
✅ Traffic-Flow-1D-Modal-Sub-cell-shock-cap.py - Função 'epscompactsmoother' encontrada
❌ Traffic-Flow-1D-Nodal-Sub-cell-shock-cap-const-eps.py - Função 'epscompactsmoother' NÃO encontrada
❌ Traffic-Flow-1D-Nodal-Sub-cell-shock-cap-smooth-eps.py - Função 'epscompactsmoother' NÃO encontrada
❌ Traffic-Flow-1D-Nodal-Sub-cell-shock-cap.py - Função 'epscompactsmoother' NÃO encontrada
❌ Viscous-Burgers-1D-Modal.py - Função 'epscompactsmoother' NÃO encontrada
------------------------------------------------------------

📊 Total de arquivos com a função 'epscompactsmoother': 6


====================================================================================================
MATRIZ DE COMPARAÇÃO
====================================================================================================
Arquivo                              1     2     3     4     5     6   
----------------------------------------------------------------------------------------------------
Euler-1D-Modal-Sub-cell-shock-ca     ✓     ≈     ≈     ✓     ≠     ≈   
Inviscid-Burgers-1D-Modal-Sub-ce     ≈     ✓     ≈     ≈     ≠     ✓   
Linear-Advection-1D-Modal-Subcel     ≈     ≈     ✓     ≈     ≠     ≈   
Shock-Density-1D-Modal-Sub-cell-     ✓     ≈     ≈     ✓     ≠     ≈   
Traffic-Flow-1D-Modal-Sub-cell-s     ≠     ≠     ≠     ≠     ✓     ≠   
Traffic-Flow-1D-Modal-Sub-cell-s     ≈     ✓     ≈     ≈     ≠     ✓   
====================================================================================================
✓ = idêntica  ≈ = Hash diferente  ≠ = diferente

📈 RESUMO:
  ⚠️ Hash diferente, AST igual: 8 comparação(ões)
  ✅ Idêntica (Hash+AST): 2 comparação(ões)
  ❌ Diferente (Hash+AST): 5 comparação(ões)

--------------------------------------------------------------------------------

📊 Deseja gerar o heatmap? [y/n]: y
```
<div align="center">
  <img src="https://raw.githubusercontent.com/Paulo-de-Souza/Comparador_Funcoes/main/imagens/heatmap_epscompactsmoother_20260718_130649.png" alt = "Exemplo de heatmap" width="500"><br>
  <em>Exemplo de heatmap</em>
</div>
