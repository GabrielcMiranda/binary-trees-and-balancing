"""
Pacote Árvore 2-3-4 - Implementação de B-tree com grau mínimo t=2

Este pacote contém:
- 2-3-4.py: Implementação da estrutura de dados Árvore 2-3-4
- implementation_234.py: Interface interativa com menu e visualizações
"""

# Importar usando importlib para contornar o nome com hífen
import importlib.util
import os

# Carregar o módulo 2-3-4.py
spec = importlib.util.spec_from_file_location(
    "btree234", 
    os.path.join(os.path.dirname(__file__), "2-3-4.py")
)
btree234_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(btree234_module)

# Expor as classes principais
BTree234 = btree234_module.BTree234
BTreeNode = btree234_module.BTreeNode

__all__ = ['BTree234', 'BTreeNode']
