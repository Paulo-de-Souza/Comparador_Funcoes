import os
from code_parser import parse_file
from compare import compare_files
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

folder = "python_DG_Alberto"

def encontrar_funcao_em_arquivos(nome_funcao):
    """
    Encontra todos os arquivos que contêm uma função específica
    """
    arquivos_com_funcao = []
    resultados = []
    
    print(f"\n🔍 Procurando função '{nome_funcao}' em todos os arquivos...")
    print("-" * 60)
    
    for filename in os.listdir(folder):
        if filename.endswith(".py"):
            filepath = os.path.join(folder, filename)
            parsed = parse_file(filepath)
            
            # Verificar se a função existe neste arquivo
            funcao_encontrada = False
            for func in parsed.functions:
                if func.name == nome_funcao:
                    funcao_encontrada = True
                    arquivos_com_funcao.append({
                        'file': parsed,
                        'filename': filename,
                        'function': func
                    })
                    break
            
            if funcao_encontrada:
                print(f"✅ {filename} - Função '{nome_funcao}' encontrada")
            else:
                print(f"❌ {filename} - Função '{nome_funcao}' NÃO encontrada")
    
    print("-" * 60)
    print(f"\n📊 Total de arquivos com a função '{nome_funcao}': {len(arquivos_com_funcao)}")
    
    return arquivos_com_funcao

def comparar_funcao_em_todos_arquivos(arquivos_com_funcao, nome_funcao):
    """
    Compara a mesma função em todos os arquivos encontrados
    """
    if len(arquivos_com_funcao) < 2:
        print(f"\n⚠️  Precisa de pelo menos 2 arquivos com a função '{nome_funcao}' para comparar.")
        return None
    
    resultados_comparacao = []
    
    # Comparar cada arquivo com os subsequentes
    for i in range(len(arquivos_com_funcao)):
        for j in range(i + 1, len(arquivos_com_funcao)):
            arquivo1 = arquivos_com_funcao[i]['file']
            arquivo2 = arquivos_com_funcao[j]['file']
            nome1 = arquivos_com_funcao[i]['filename']
            nome2 = arquivos_com_funcao[j]['filename']
            
            # Comparar os arquivos
            comparacao = compare_files(arquivo1, arquivo2)
            
            # Filtrar apenas a função específica
            for item in comparacao:
                if item['name'] == nome_funcao:
                    resultados_comparacao.append({
                        'arquivo1': nome1,
                        'arquivo2': nome2,
                        'status': item['status'],
                        'detalhes': item.get('detalhes', '')
                    })
                    break
    
    return resultados_comparacao

# def exibir_resultados(resultados, nome_funcao):
#     """
#     Exibe os resultados de forma organizada
#     """
#     if not resultados:
#         print("\n❌ Nenhum resultado para exibir.")
#         return
    
#     print("\n" + "="*80)
#     print(f"📊 RESULTADOS DA COMPARAÇÃO PARA FUNÇÃO: {nome_funcao}")
#     print("="*80)
    
#     # Contar status
#     status_count = {}
#     for r in resultados:
#         status_count[r['status']] = status_count.get(r['status'], 0) + 1
    
#     print("\n📈 RESUMO:")
#     for status, count in status_count.items():
#         print(f"  {status}: {count} comparação(ões)")
    
#     print("\n" + "-"*80)
#     print(f"{'Arquivo 1':<30} {'Arquivo 2':<30} {'Status':<20}")
#     print("-"*80)
    
#     for r in resultados:
#         print(f"{r['arquivo1']:<30} {r['arquivo2']:<30} {r['status']:<20}")
    
#     print("="*80)

def criar_matriz_comparacao(resultados):
    """
    Converte os resultados da comparação em uma matriz simétrica.
    """

    nomes = sorted(
        set(r["arquivo1"] for r in resultados) |
        set(r["arquivo2"] for r in resultados)
    )

    indice = {nome: i for i, nome in enumerate(nomes)}

    matriz = np.eye(len(nomes))

    # np.fill_diagonal(matriz, 1.0)

    for r in resultados:

        status = r["status"]

        if "Idêntica" in status or "Identical" in status:
            valor = 1.0

        elif "Hash diferente" in status:
            valor = 0.75

        elif "Diferente" in status or "Different" in status:
            valor = 0.5

        else:
            raise ValueError(f"Status desconhecido retornado por compare_files(): {status}")

        i = indice[r["arquivo1"]]
        j = indice[r["arquivo2"]]

        matriz[i, j] = valor
        matriz[j, i] = valor

    return matriz, nomes

def exibir_matriz(matriz, nomes):

    print("\n")
    print("="*100)
    print("MATRIZ DE COMPARAÇÃO")
    print("="*100)

    print(f"{'Arquivo':35}", end="")

    for i in range(len(nomes)):
        print(f"{i+1:^6}", end="")

    print()

    print("-"*100)

    for i, nome in enumerate(nomes):

        texto = nome[:32]
        print(f"{texto:35}", end="")

        for j in range(len(nomes)):

            if matriz[i, j] == 1:
                s = "✓"

            elif matriz[i, j] == 0.75:
                s = "≈"

            elif matriz[i, j] == 0.5:
                s = "≠"

            else:
                raise ValueError(f"Valor inválido na matriz: {matriz[i,j]}")

            print(f"{s:^6}", end="")

        print()

    print("="*100)
    print("✓ = idêntica  ≈ = Hash diferente  ≠ = diferente")

def gerar_heatmap(matriz, nomes, nome_funcao):

    fig, ax = plt.subplots(figsize=(10,10))

    cores = np.zeros((len(nomes), len(nomes), 3))

    for i in range(len(nomes)):
        for j in range(len(nomes)):

            if matriz[i,j] == 1:
                cores[i,j] = [0.18,0.80,0.25]

            elif matriz[i,j] == 0.75:
                cores[i,j] = [1.00,0.90,0.10]

            elif matriz[i,j] == 0.5:
                cores[i,j] = [0.90,0.20,0.20]

            else:
                raise ValueError(f"Valor inválido na matriz: {matriz[i,j]}")

    ax.imshow(cores)

    from matplotlib.patches import Patch

    legend_elements = [
        Patch(facecolor=[0.18,0.80,0.25], label="Idêntica"),
        Patch(facecolor=[1.00,0.90,0.10], label="Hash diferente, AST igual"),
        Patch(facecolor=[0.90,0.20,0.20], label="Hash+AST diferente"),
    ]

    ax.legend(handles=legend_elements, loc="upper right")

    ax.set_xticks(range(len(nomes)))
    ax.set_yticks(range(len(nomes)))

    ax.set_xticklabels(nomes, rotation=45, ha="right", fontsize=8)
    ax.set_yticklabels(nomes, fontsize=8)

    for i in range(len(nomes)):
        for j in range(len(nomes)):

            if matriz[i,j] == 1:
                txt = "✓"

            elif matriz[i,j] == 0.75:
                txt = "≈"

            elif matriz[i,j] == 0.5:
                txt = "≠"

            else:
                raise ValueError(f"Valor inválido na matriz: {matriz[i,j]}")

            ax.text(j, i, txt,
                    ha="center",
                    va="center",
                    color="white",
                    fontsize=10,
                    fontweight="bold")

    plt.title(f"Comparação da função {nome_funcao}")

    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    plt.savefig(
        f"heatmap_{nome_funcao}_{timestamp}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

def main():
    print("="*80)
    print("🔍 ANALISADOR DE FUNÇÕES ENTRE MÚLTIPLOS ARQUIVOS")
    print("="*80)
    
    while True:
        # Mostrar arquivos disponíveis
        # print("\n📁 Arquivos disponíveis:")
        # print("-" * 40)
        # arquivos = [f for f in os.listdir(folder) if f.endswith(".py")]
        # for i, nome in enumerate(arquivos):
        #     print(f"  {i+1}. {nome}")
        # print("-" * 40)
        
        # Perguntar qual função analisar
        nome_funcao = input("\n🔤 Digite o nome da função para analisar (ou 'sair' para encerrar): ").strip()
        
        if nome_funcao.lower() in ['sair', 'exit', 'quit', 'q']:
            print("\n👋 Programa finalizado.")
            break
        
        if not nome_funcao:
            print("❌ Nome da função não pode estar vazio!")
            continue
        
        # Encontrar arquivos com a função
        arquivos_com_funcao = encontrar_funcao_em_arquivos(nome_funcao)

        if len(arquivos_com_funcao) == 0:
            print(f"\n❌ A função '{nome_funcao}' não foi encontrada em nenhum arquivo da pasta '{folder}'.")
            print("   Verifique a grafia e tente novamente.")
            continue

        if len(arquivos_com_funcao) == 1:
            print(f"\n⚠️ A função '{nome_funcao}' foi encontrada em apenas um arquivo.")
            print("   São necessários pelo menos dois arquivos para realizar uma comparação.")
            continue
        
        # Comparar a função em todos os arquivos
        resultados = comparar_funcao_em_todos_arquivos(arquivos_com_funcao, nome_funcao)
        
        if resultados:

            #exibir_resultados(resultados, nome_funcao)

            matriz, nomes = criar_matriz_comparacao(resultados)

            exibir_matriz(matriz, nomes)

            gerar = input(
                "\n📊 Deseja gerar o heatmap? [y/n]: "
            ).lower()

            if gerar in ["y", "yes", "s", "sim"]:

                gerar_heatmap(matriz, nomes, nome_funcao)

if __name__ == "__main__":
    main()