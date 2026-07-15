import os
from collections import defaultdict
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
# Geração do PDF - Sugestão 1: Tabela com Grade
# =====================================================

def generate_pdf_table(filename="relatorio_funcoes_tabela.pdf"):
    # Cria o documento em formato paisagem para melhor visualização
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(A4),
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
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
        spaceAfter=10
    )
    
    # Estilo para o subtítulo
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=15
    )
    
    # Estilo para o cabeçalho da tabela
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Estilo para o nome da função
    func_style = ParagraphStyle(
        'FunctionStyle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier-Bold',
        textColor=colors.darkblue,
        alignment=TA_LEFT
    )
    
    # Estilo para os arquivos
    files_style = ParagraphStyle(
        'FilesStyle',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        alignment=TA_LEFT,
        leading=12
    )

    # Coleta os dados
    nfiles = len(all_files)
    
    # Lista para armazenar os elementos do PDF
    elements = []
    
    # Título
    elements.append(Paragraph("RELATÓRIO DE FUNÇÕES POR ARQUIVO", title_style))
    elements.append(Paragraph(f"Total: {nfiles} arquivos | {len(function_index)} funções distintas", subtitle_style))
    elements.append(Spacer(1, 0.3*cm))
    
    # Prepara os dados para a tabela
    table_data = []
    
    # Cabeçalho da tabela
    header_cells = [
        Paragraph("<b>FUNÇÃO</b>", header_style),
        Paragraph("<b>USO</b>", header_style),
        Paragraph("<b>ARQUIVOS</b>", header_style)
    ]
    table_data.append(header_cells)
    
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
        
        # Cria o texto para os arquivos com quebras de linha
        files_text = wrapped[0]
        for line in wrapped[1:]:
            files_text += f"<br/>{line}"
        
        # Cria a célula da função
        func_cell = Paragraph(function, func_style)
        
        # Cria a célula do uso
        use_cell = Paragraph(f"<b>{count}x</b>", styles['Normal'])
        
        # Cria a célula dos arquivos
        files_cell = Paragraph(files_text, files_style)
        
        # Adiciona à tabela
        table_data.append([func_cell, use_cell, files_cell])
        
        # Adiciona uma linha de separação visual entre funções (linha cinza clara)
        if function_count < len(function_index):
            # Adiciona uma linha em branco como separador
            table_data.append([
                Paragraph("", styles['Normal']),
                Paragraph("", styles['Normal']),
                Paragraph("", styles['Normal'])
            ])
    
    # Cria a tabela
    table = Table(table_data, colWidths=[4*cm, 1.5*cm, 20*cm])
    
    # Estiliza a tabela
    table_style = TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        
        # Bordas da tabela
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.darkblue),
        
        # Alinhamento das células
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Cores alternadas para as linhas
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        
        # Padding das células
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('LEFTPADDING', (0, 1), (-1, -1), 6),
        ('RIGHTPADDING', (0, 1), (-1, -1), 6),
        
        # Linhas de separação entre funções (mais grossas)
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.darkblue),
    ])
    
    # Adiciona separadores mais grossos entre funções
    row = 1
    for i in range(1, len(table_data)):
        if table_data[i][0].text == "" and table_data[i][1].text == "" and table_data[i][2].text == "":
            table_style.add('LINEBELOW', (0, row), (-1, row), 1, colors.darkblue)
        row += 1
    
    table.setStyle(table_style)
    
    # Adiciona a tabela ao documento
    elements.append(table)
    
    # Gera o PDF
    doc.build(elements)
    print(f"PDF gerado com sucesso: {filename}")

# Executa
if __name__ == "__main__":
    generate_pdf_table()