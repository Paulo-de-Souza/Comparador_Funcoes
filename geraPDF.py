import os
import textwrap
from collections import defaultdict
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfgen import canvas

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
# Geração do PDF
# =====================================================

def generate_pdf(filename="relatorio_funcoes.pdf"):
    # Cria o documento
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    # Estilos
    styles = getSampleStyleSheet()
    
    # Estilo para o título
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.darkblue,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    # Estilo para o cabeçalho da tabela
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading4'],
        fontSize=11,
        textColor=colors.white,
        backColor=colors.darkblue,
        alignment=TA_LEFT,
        spaceAfter=6,
        spaceBefore=6,
        leftIndent=5,
        rightIndent=5
    )
    
    # Estilo para a função
    func_style = ParagraphStyle(
        'FunctionStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier',
        alignment=TA_LEFT,
        spaceAfter=2,
        leftIndent=0
    )
    
    # Estilo para os arquivos (primeira linha)
    files_style = ParagraphStyle(
        'FilesStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        alignment=TA_LEFT,
        spaceAfter=2,
        leftIndent=0
    )
    
    # Estilo para os arquivos (linhas seguintes)
    files_indent_style = ParagraphStyle(
        'FilesIndentStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        alignment=TA_LEFT,
        spaceAfter=2,
        leftIndent=50  # Mesmo alinhamento do print original
    )
    
    # Estilo para o separador
    separator_style = ParagraphStyle(
        'SeparatorStyle',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=6,
        spaceBefore=6
    )

    # Coleta os dados
    nfiles = len(all_files)
    
    # Lista para armazenar os elementos do PDF
    elements = []
    
    # Título
    elements.append(Paragraph("Relatório de Funções por Arquivo", title_style))
    elements.append(Spacer(1, 0.2*cm))
    
    # Informações de resumo
    summary_style = ParagraphStyle(
        'SummaryStyle',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_LEFT,
        spaceAfter=4
    )
    
    elements.append(Paragraph(f"<b>Arquivos analisados:</b> {nfiles}", summary_style))
    elements.append(Paragraph(f"<b>Funções distintas:</b> {len(function_index)}", summary_style))
    elements.append(Spacer(1, 0.5*cm))
    
    # Cabeçalho da tabela
    header_text = f"<font color='white'><b>{'Função':<35} {'Uso':>10}   Arquivos</b></font>"
    elements.append(Paragraph(header_text, header_style))
    elements.append(Spacer(1, 0.1*cm))
    
    # Função para adicionar uma linha de separação
    def add_separator():
        elements.append(Paragraph("─" * 100, separator_style))
    
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
        
        # Formata a linha da função
        func_line = f"<font color='darkblue'><b>{function}</b></font>"
        count_line = f"<b>{count:>6}x</b>"
        
        # Primeira linha com a função e o contador
        first_line = f"{func_line:<35} {count_line}   {wrapped[0]}"
        elements.append(Paragraph(first_line, func_style))
        
        # Linhas seguintes dos arquivos (indentadas)
        for line in wrapped[1:]:
            elements.append(Paragraph(line, files_indent_style))
        
        # Adiciona separador entre funções (exceto após a última)
        if function_count < len(function_index):
            add_separator()
        
        # Adiciona quebra de página a cada 20 funções (ajuste conforme necessário)
        if function_count % 20 == 0 and function_count < len(function_index):
            elements.append(PageBreak())
            # Re-adiciona o cabeçalho após a quebra de página
            elements.append(Paragraph(header_text, header_style))
            elements.append(Spacer(1, 0.1*cm))
    
    # Gera o PDF
    doc.build(elements)
    print(f"PDF gerado com sucesso: {filename}")

# =====================================================
# Executa a geração do PDF
# =====================================================

if __name__ == "__main__":
    generate_pdf()