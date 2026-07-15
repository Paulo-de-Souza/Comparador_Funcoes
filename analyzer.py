import os
from code_parser import parse_file

folder = "python_DG_Alberto"
all_files = []

# -------------------------------------------------
# Listar todos os arquivos .py
# -------------------------------------------------
for filename in os.listdir(folder):
    if filename.endswith(".py"):
        filepath = os.path.join(folder, filename)
        all_files.append(parse_file(filepath))

# -------------------------------------------------
# Mostrar lista de arquivos disponíveis
# -------------------------------------------------
print("\n" + "="*80)
print("ARQUIVOS PYTHON DISPONÍVEIS")
print("="*80)
print()

for i, file in enumerate(all_files):
    print(f"[{i}] {os.path.basename(file.filename)} ({len(file.functions)} funções)")

print()
print("-"*80)

# -------------------------------------------------
# Escolher um arquivo
# -------------------------------------------------
while True:
    try:
        escolha = int(input("\nDigite o número do arquivo que deseja analisar: "))
        
        if 0 <= escolha < len(all_files):
            break
        else:
            print(f"❌ Índice inválido! Escolha um número entre 0 e {len(all_files)-1}")
    except ValueError:
        print("❌ Digite um número válido!")

# -------------------------------------------------
# Mostrar informações do arquivo escolhido
# -------------------------------------------------
info = all_files[escolha]

print("\n" + "="*80)
print(f"ANALISANDO: {os.path.basename(info.filename)}")
print("="*80)
print(f"Número de funções: {len(info.functions)}\n")

for function in info.functions:
    print(f"{function.name:<30} ({function.nlines:>3} linhas)")

    if function.calls:
        print("    Chama:")
        for c in function.calls:
            print(f"       - {c}")
    else:
        print("    Chama: nenhuma")

    print("    Dependências:")
    if function.dependencies:
        for d in function.dependencies:
            print(f"       - {d}")
    else:
        print("       nenhuma")

    print("    Variáveis locais:")
    if function.local_variables:
        for d in function.local_variables:
            print(f"       - {d}")
    else:
        print("       nenhuma")
    print()

print("="*80)

# import os

# from code_parser import parse_file


# folder = "python_DG_Alberto"

# all_files = []

# # -------------------------------------------------

# for filename in os.listdir(folder):

#     if filename.endswith(".py"):

#         filepath = os.path.join(folder, filename)

#         all_files.append(parse_file(filepath))

# # -------------------------------------------------

# for info in all_files:

#     print("=" * 80)
#     print(info.filename)
#     print(f"Número de funções: {len(info.functions)}\n")

#     for function in info.functions:

#         print(f"{function.name:<30} ({function.nlines:>3} linhas)")

#         if function.calls:

#             print("    Chama:")

#             for c in function.calls:
#                 print(f"       - {c}")

#         else:
#             print("    Chama: nenhuma")

#         print("    Dependências:")

#         if function.dependencies:

#             for d in function.dependencies:
#                 print(f"       - {d}")

#         else:
#             print("       nenhuma")

#         print("    Variáveis locais:")

#         if function.local_variables:

#             for d in function.local_variables:
#                 print(f"       - {d}")

#         else:
#             print("       nenhuma")

#         print()

