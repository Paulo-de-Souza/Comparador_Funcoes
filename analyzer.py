import os

from code_parser import parse_file


folder = "python_DG_Alberto"

all_files = []

# -------------------------------------------------

for filename in os.listdir(folder):

    if filename.endswith(".py"):

        filepath = os.path.join(folder, filename)

        all_files.append(parse_file(filepath))

# -------------------------------------------------

for info in all_files:

    print("=" * 80)
    print(info.filename)
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