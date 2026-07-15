import os
import textwrap
from collections import defaultdict

from code_parser import parse_file


folder = "python_DG_Alberto"

all_files = []

# =====================================================
# Analisa todos os arquivos
# =====================================================

for filename in os.listdir(folder):

    if filename.endswith(".py"):

        filepath = os.path.join(folder, filename)

        all_files.append(parse_file(filepath))


# =====================================================
# Índice global de funções
# =====================================================

function_index = defaultdict(list)

for file in all_files:

    filename = os.path.basename(file.filename)

    for function in file.functions:

        function_index[function.name].append(filename)


# =====================================================
# Relatório
# =====================================================

nfiles = len(all_files)

print("=" * 120)
print(f"{'Arquivos analisados':<25}: {nfiles}")
print(f"{'Funções distintas':<25}: {len(function_index)}")
print("=" * 120)

print()

header = (
    f"{'Função':<35}"
    f"{'Uso':>7}"
    f"   Arquivos"
)

print(header)
print("-" * 120)

# Função para quebrar a string nos ponto-e-vírgula
def split_by_semicolon(text, max_width=70):
    if len(text) <= max_width:
        return [text]
    
    parts = text.split("; ")
    result = []
    current_line = ""
    
    for part in parts:
        # Adiciona o ponto-e-vírgula de volta (exceto no último)
        part_with_sep = part + "; " if part != parts[-1] else part
        
        if len(current_line) + len(part_with_sep) <= max_width:
            current_line += part_with_sep
        else:
            if current_line:
                result.append(current_line.rstrip("; "))
            current_line = part_with_sep
    
    if current_line:
        result.append(current_line.rstrip("; "))
    
    return result

# Ordena as funções por frequência de uso (da mais usada para a menos usada)
for function in sorted(function_index, key=lambda x: len(function_index[x]), reverse=True):

    files = sorted(function_index[function])

    count = len(files)

    if count == nfiles:

        location = "Todos os arquivos"

    else:

        location = "; ".join(files)

    # Aplica a quebra personalizada
    wrapped = split_by_semicolon(location, max_width=70)

    print(
        f"{function:<35}"
        f"{count:>6}x"
        f"   {wrapped[0]}"
    )

    for line in wrapped[1:]:
        print(f"{' ' * 45}{line}")  # Alinha corretamente as linhas seguintes