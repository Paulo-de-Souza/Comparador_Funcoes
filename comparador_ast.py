import ast
import hashlib
from typing import Dict, Any

class ComparadorAST:
    """
    Compara funções usando AST para ignorar diferenças de formatação
    """
    
    @staticmethod
    def normalizar_funcao(codigo: str) -> str:
        """
        Normaliza o código da função para comparação.
        Remove espaços extras, nomes de variáveis, etc.
        """
        try:
            # Parse do código
            arvore = ast.parse(codigo)
            
            # Encontrar a função
            for node in ast.walk(arvore):
                if isinstance(node, ast.FunctionDef):
                    # Criar uma versão normalizada da função
                    return ComparadorAST._normalizar_node(node)
            
            return codigo
        except:
            # Se der erro, volta ao método original
            return codigo
    
    @staticmethod
    def _normalizar_node(node) -> str:
        """
        Normaliza um nó AST recursivamente
        """
        if isinstance(node, ast.FunctionDef):
            # Normalizar nome da função (opcional)
            nome = "funcao_normalizada"
            
            # Normalizar argumentos
            args = []
            for arg in node.args.args:
                args.append("arg")  # Todos os argumentos viram "arg"
            
            # Normalizar corpo da função
            corpo = []
            for item in node.body:
                corpo.append(ComparadorAST._normalizar_node(item))
            
            return f"def {nome}({', '.join(args)}):\n    " + "\n    ".join(corpo)
        
        elif isinstance(node, ast.Return):
            if node.value:
                return f"return {ComparadorAST._normalizar_node(node.value)}"
            return "return"
        
        elif isinstance(node, ast.BinOp):
            # Operações binárias (soma, subtração, etc)
            esquerda = ComparadorAST._normalizar_node(node.left)
            direita = ComparadorAST._normalizar_node(node.right)
            operador = type(node.op).__name__
            return f"({esquerda} {operador} {direita})"
        
        elif isinstance(node, ast.Name):
            # Todas as variáveis viram "var"
            return "var"
        
        elif isinstance(node, ast.Constant):
            # Constantes (números, strings, etc)
            return f"const_{type(node.value).__name__}"
        
        elif isinstance(node, ast.Assign):
            # Atribuições
            alvos = [ComparadorAST._normalizar_node(t) for t in node.targets]
            valor = ComparadorAST._normalizar_node(node.value)
            return f"{' = '.join(alvos)} = {valor}"
        
        elif isinstance(node, ast.If):
            # Estruturas condicionais
            teste = ComparadorAST._normalizar_node(node.test)
            corpo = [ComparadorAST._normalizar_node(n) for n in node.body]
            orelse = [ComparadorAST._normalizar_node(n) for n in node.orelse] if node.orelse else []
            
            resultado = f"if {teste}:\n    " + "\n    ".join(corpo)
            if orelse:
                resultado += f"\nelse:\n    " + "\n    ".join(orelse)
            return resultado
        
        elif isinstance(node, ast.Compare):
            # Comparações
            esquerda = ComparadorAST._normalizar_node(node.left)
            ops = [type(op).__name__ for op in node.ops]
            comparadores = [ComparadorAST._normalizar_node(c) for c in node.comparators]
            return f"({esquerda} {' '.join(ops)} {' '.join(comparadores)})"
        
        elif isinstance(node, ast.Call):
            # Chamadas de função
            func = ComparadorAST._normalizar_node(node.func)
            args = [ComparadorAST._normalizar_node(a) for a in node.args]
            return f"{func}({', '.join(args)})"
        
        else:
            # Outros tipos de nó
            return f"{type(node).__name__}"
    
    @staticmethod
    def comparar_funcoes(codigo1: str, codigo2: str) -> Dict[str, Any]:
        """
        Compara duas funções usando AST
        """
        try:
            normalizado1 = ComparadorAST.normalizar_funcao(codigo1)
            normalizado2 = ComparadorAST.normalizar_funcao(codigo2)
            
            # Gerar hashes do código normalizado
            hash1 = hashlib.sha256(normalizado1.encode("utf-8")).hexdigest()
            hash2 = hashlib.sha256(normalizado2.encode("utf-8")).hexdigest()
            
            return {
                "igual": hash1 == hash2,
                "normalizado1": normalizado1,
                "normalizado2": normalizado2,
                "hash1": hash1[:8] + "...",
                "hash2": hash2[:8] + "..."
            }
        except Exception as e:
            return {
                "igual": False,
                "erro": str(e)
            }