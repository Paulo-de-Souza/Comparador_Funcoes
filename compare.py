# import hashlib
# from comparador_ast import ComparadorAST

# def function_hash(source):
#     """
#     Retorna um hash SHA256 da função (método original)
#     """
#     return hashlib.sha256(
#         source.encode("utf-8")
#     ).hexdigest()

# def function_hash_ast(source):
#     """
#     Retorna um hash SHA256 da função normalizada pelo AST
#     """
#     normalizado = ComparadorAST.normalizar_funcao(source)
#     return hashlib.sha256(
#         normalizado.encode("utf-8")
#     ).hexdigest()

# def compare_files(file1, file2, usar_ast=True):
#     """
#     Compara dois arquivos, com opção de usar AST
#     """
#     dict1 = {f.name: f for f in file1.functions}
#     dict2 = {f.name: f for f in file2.functions}
    
#     names = sorted(set(dict1.keys()) | set(dict2.keys()))
#     result = []
    
#     for name in names:
#         if name not in dict1:
#             status = "Somente Arquivo 2"
#         elif name not in dict2:
#             status = "Somente Arquivo 1"
#         else:
#             if usar_ast:
#                 # Comparação inteligente com AST
#                 codigo1 = dict1[name].source
#                 codigo2 = dict2[name].source
                
#                 resultado = ComparadorAST.comparar_funcoes(codigo1, codigo2)
                
#                 if resultado.get("igual", False):
#                     status = "Idêntica (AST)"
#                 else:
#                     status = "Modificada (AST)"
#             else:
#                 # Comparação tradicional (texto)
#                 h1 = function_hash(dict1[name].source)
#                 h2 = function_hash(dict2[name].source)
#                 status = "Idêntica (Hash)" if h1 == h2 else "Modificada (Hash)"
        
#         result.append((name, status))
    
#     return result

import hashlib
from comparador_ast import ComparadorAST

def function_hash(source):
    """
    Retorna um hash SHA256 da função (método original)
    """
    return hashlib.sha256(
        source.encode("utf-8")
    ).hexdigest()

def function_hash_ast(source):
    """
    Retorna um hash SHA256 da função normalizada pelo AST
    """
    normalizado = ComparadorAST.normalizar_funcao(source)
    return hashlib.sha256(
        normalizado.encode("utf-8")
    ).hexdigest()

def compare_files(file1, file2, mostrar_ambos=True):
    """
    Compara dois arquivos mostrando ambos os métodos (Hash e AST)
    
    Args:
        file1: Primeiro arquivo
        file2: Segundo arquivo
        mostrar_ambos: Se True, mostra ambos os resultados; se False, mostra apenas AST
    """
    dict1 = {f.name: f for f in file1.functions}
    dict2 = {f.name: f for f in file2.functions}
    
    names = sorted(set(dict1.keys()) | set(dict2.keys()))
    result = []
    
    for name in names:
        if name not in dict1:
            status = "Somente Arquivo 2"
            hash_status = "-"
            ast_status = "-"
        elif name not in dict2:
            status = "Somente Arquivo 1"
            hash_status = "-"
            ast_status = "-"
        else:
            codigo1 = dict1[name].source
            codigo2 = dict2[name].source
            
            # Comparação por Hash (texto)
            h1 = function_hash(codigo1)
            h2 = function_hash(codigo2)
            hash_igual = h1 == h2
            hash_status = "Idêntico" if hash_igual else "Diferente"
            
            # Comparação por AST (estrutura)
            try:
                resultado_ast = ComparadorAST.comparar_funcoes(codigo1, codigo2)
                ast_igual = resultado_ast.get("igual", False)
                ast_status = "Idêntico" if ast_igual else "Diferente"
            except Exception as e:
                ast_status = f"Erro: {str(e)[:30]}..."
            
            # Status combinado
            if hash_igual and ast_igual:
                status = "✅ Idêntica (Hash+AST)"
            elif hash_igual and not ast_igual:
                status = "⚠️ Hash igual, AST diferente"
            elif not hash_igual and ast_igual:
                status = "⚠️ Hash diferente, AST igual"
            else:
                status = "❌ Diferente (Hash+AST)"
        
        result.append({
            'name': name,
            'status': status,
            'hash_status': hash_status if 'hash_status' in locals() else '-',
            'ast_status': ast_status if 'ast_status' in locals() else '-'
        })
    
    return result