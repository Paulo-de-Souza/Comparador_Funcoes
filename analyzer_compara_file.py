import os
from code_parser import parse_file
from compare import compare_files

folder = "python_DG_Alberto"

# Listar todos os arquivos .py
all_files = []
file_names = []

for filename in os.listdir(folder):
    if filename.endswith(".py"):
        filepath = os.path.join(folder, filename)
        all_files.append(parse_file(filepath))
        file_names.append(filename)

# Mostrar lista de arquivos disponíveis
# print("\nArquivos disponíveis:")
# print("-" * 40)
# for i, name in enumerate(file_names):
#     print(f"[{i}] {name}")
# print("-" * 40)

# Selecionar arquivos para comparar
# Loop de comparação
while True:
    # Mostrar lista de arquivos disponíveis
    print("\nArquivos disponíveis:")
    print("-" * 40)
    for i, name in enumerate(file_names):
        print(f"[{i}] {name}")
    print("-" * 40)

    # Selecionar arquivos para comparar
    while True:
        try:
            id1 = int(input("\nDigite o número do primeiro arquivo: "))
            id2 = int(input("Digite o número do segundo arquivo: "))
            
            if 0 <= id1 < len(all_files) and 0 <= id2 < len(all_files):
                break
            else:
                print("Índice inválido! Escolha um número da lista.")

        except ValueError:
            print("Digite um número válido!")


    # Mostrar arquivos escolhidos
    print("\n" + "="*80)
    print(all_files[id1].filename)
    print("X")
    print(all_files[id2].filename)
    print("="*80)


    # Comparação
    comparison = compare_files(all_files[id1], all_files[id2])


    # Mostrar resultado
    print("\n" + "="*80)
    print("RESULTADO DA COMPARAÇÃO")
    print("="*80)
    print(f"{'Função':<30} {'Status':<45}")
    print("-"*75)

    for item in comparison:
        name = item['name']
        status = item['status']
        print(f"{name:<30} {status:<45}")

    print("="*80)


    # Perguntar se continua
    continuar = input("\nDeseja comparar mais arquivos? [y/n]: ").strip().lower()

    if continuar in ["n", "no", "nao", "não"]:
        print("\nPrograma finalizado.")
        break

    elif continuar not in ["y", "yes", "sim", "s"]:
        print("\nResposta inválida. Encerrando.")
        break