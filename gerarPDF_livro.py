import os
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors

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
# Função para quebrar a string nos ponto-e-vírgula
# =====================================================

def split_by_semicolon(text, max_width=70):
    if len(text) <= max_width:
        return [text]
    
    parts = text.split("; ")
    result = []
    current_line = ""
    
    for part in parts:
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


# =====================================================
# Geração do PDF - Sugestão 3: Estilo Livro com Numeração
# =====================================================

def generate_pdf_book(filename="relatorio_funcoes_livro.pdf"):
    # Cria o documento
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2.5*cm,
        leftMargin=2.5*cm,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
    )

    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para o título principal
    title_style = ParagraphStyle(
        'MainTitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=10
    )
    
    # Estilo para o subtítulo
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=20
    )
    
    # Estilo para o número da função
    number_style = ParagraphStyle(
        'NumberStyle',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=colors.darkblue,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    # Estilo para o nome da função e uso
    func_style = ParagraphStyle(
        'FunctionStyle',
        parent=styles['Normal'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    # Estilo para o label "Arquivos:"
    label_style = ParagraphStyle(
        'LabelStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=colors.darkblue,
        alignment=TA_LEFT,
        spaceAfter=2
    )
    
    # Estilo para os arquivos (lista)
    files_style = ParagraphStyle(
        'FilesStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        alignment=TA_LEFT,
        leftIndent=20,
        leading=14,
        spaceAfter=2
    )
    
    # Estilo para o separador
    separator_style = ParagraphStyle(
        'SeparatorStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=8,
        spaceBefore=8
    )

    # Coleta os dados
    nfiles = len(all_files)
    
    # Lista para armazenar os elementos do PDF
    elements = []
    
    # Título
    elements.append(Paragraph("RELATÓRIO DE FUNÇÕES POR ARQUIVO", title_style))
    elements.append(Paragraph(f"Total: {nfiles} arquivos analisados | {len(function_index)} funções distintas", subtitle_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Função para adicionar um separador
    def add_separator():
        elements.append(Paragraph("─" * 90, separator_style))
    
    # Processa cada função (ordenada por frequência)
    function_count = 0
    for function in sorted(function_index, key=lambda x: len(function_index[x]), reverse=True):
        function_count += 1
        
        files = sorted(function_index[function])
        count = len(files)
        
        if count == nfiles:
            location = "Todos os arquivos"
        else:
            location = "; ".join(files)
        
        # Quebra os nomes dos arquivos
        wrapped = split_by_semicolon(location, max_width=70)
        
        # Número da função
        elements.append(Paragraph(f"{function_count:3d}. {function}", number_style))
        
        # Uso (quantidade)
        elements.append(Paragraph(f"     <b>Uso:</b> {count}x", func_style))
        
        # Label "Arquivos:"
        elements.append(Paragraph("     <b>Arquivos:</b>", label_style))
        
        # Lista de arquivos com numeração
        for i, line in enumerate(wrapped, 1):
            # Formata com letras minúsculas para sub-itens
            letter = chr(96 + i)  # a, b, c, ...
            elements.append(Paragraph(f"          {letter}. {line}", files_style))
        
        # Adiciona separador entre funções (exceto após a última)
        if function_count < len(function_index):
            add_separator()
        
        # Adiciona quebra de página a cada 15 funções (ajustável)
        if function_count % 15 == 0 and function_count < len(function_index):
            elements.append(PageBreak())
            # Re-adiciona o título após a quebra de página (opcional)
            elements.append(Paragraph("RELATÓRIO DE FUNÇÕES POR ARQUIVO (continuação)", title_style))
            elements.append(Spacer(1, 0.3*cm))
    
    # Gera o PDF
    doc.build(elements)
    print(f"PDF gerado com sucesso: {filename}")

# Executa
if __name__ == "__main__":
    generate_pdf_book()