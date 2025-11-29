"""
Implementação de uma Árvore 2-3-4 (B-tree de grau mínimo t=2) em Python.

Características:
- Suporta inserção de chaves.
- Busca (search)
- Remoção (delete) com redistribuição e mesclagem
- Travessia em-ordem (traverse)
- Visualização com graphviz
- Impressão 'pretty' da árvore para visualização

Exemplo de uso:
    python 2-3-4.py
"""

from __future__ import annotations
from typing import List, Optional, Any
from collections import deque
import os


class BTreeNode:
    """Nó de B-tree de grau mínimo t. Para 2-3-4 tree usamos t=2 (max 3 chaves).

    Atributos:
        t: grau mínimo
        keys: lista de chaves ordenadas armazenadas no nó
        children: lista de filhos (len = len(keys)+1 quando não é folha)
        leaf: bool, se é folha
    """

    def __init__(self, t: int, leaf: bool = True) -> None:
        self.t = t
        self.keys: List[Any] = []
        self.children: List[BTreeNode] = []
        self.leaf = leaf

    def is_full(self) -> bool:
        # máximo de chaves = 2*t - 1
        return len(self.keys) == 2 * self.t - 1

    def find_key_index(self, k: Any) -> int:
        """Retorna o índice onde k deveria estar (primeiro índice >= k)."""
        i = 0
        while i < len(self.keys) and self.keys[i] < k:
            i += 1
        return i

    def __repr__(self) -> str:
        return f"BTreeNode(keys={self.keys}, leaf={self.leaf})"


class BTree234:
    """B-tree com t=2 (equivalente a árvore 2-3-4).

    Métodos principais:
      - insert(k)
      - search(k) -> (node, index) or (None, None)
      - delete(k) -> bool
      - traverse() -> lista ordenada de chaves
      - visualize() -> gera PNG com graphviz
      - pretty_print()
    """

    def __init__(self) -> None:
        self.t = 2
        self.root = BTreeNode(self.t, leaf=True)
        self.node_counter = 0

    def search(self, k: Any, node: Optional[BTreeNode] = None):
        """Procura pela chave k.
        Retorna (node, index) se encontrado; (None, None) caso contrário.
        """
        if node is None:
            node = self.root

        i = node.find_key_index(k)
        if i < len(node.keys) and node.keys[i] == k:
            return node, i
        if node.leaf:
            return None, None
        return self.search(k, node.children[i])

    def traverse(self) -> List[Any]:
        """Retorna a lista ordenada de chaves da árvore."""
        res: List[Any] = []

        def _traverse(node: BTreeNode):
            for i, key in enumerate(node.keys):
                if not node.leaf:
                    _traverse(node.children[i])
                res.append(key)
            if not node.leaf:
                _traverse(node.children[len(node.keys)])

        _traverse(self.root)
        return res

    def split_child(self, parent: BTreeNode, index: int) -> None:
        """Divide o filho full em dois e promove a chave mediana para o pai.

        parent.children[index] é assumido full (2*t - 1 chaves).
        """
        t = self.t
        y = parent.children[index]
        z = BTreeNode(t, leaf=y.leaf)

        # z recebe as últimas t-1 chaves de y
        z.keys = y.keys[t:]
        # se não for folha, z recebe os últimos t filhos de y
        if not y.leaf:
            z.children = y.children[t:]

        # reduzimos y para conter apenas as primeiras t-1 chaves
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            y.children = y.children[:t]

        # inserir z em parent.children logo após y
        parent.children.insert(index + 1, z)
        # promover a chave mediana y.keys[t-1] para parent.keys
        parent.keys.insert(index, y.keys.pop() if False else y.keys and None)
        # OBS: a linha acima tem que inserir corretamente a mediana — corrigimos abaixo

        # correção: mediana é a chave originalmente em posição t-1 antes do corte
        # como já truncamos y.keys, precisamos obter mediana diretamente do slice original.

    def split_child(self, parent: BTreeNode, index: int) -> None:
        # Implementação correta e clara do split
        t = self.t
        y = parent.children[index]
        assert y.is_full(), "split_child chamado em nó que não está cheio"

        # nova direita
        z = BTreeNode(t, leaf=y.leaf)

        # mediana é a chave em y.keys[t-1]
        median = y.keys[t - 1]

        # z recebe chaves à direita da mediana
        z.keys = y.keys[t:]

        # se y não for folha, transferir os filhos direitos
        if not y.leaf:
            z.children = y.children[t:]

        # reduzir y para as chaves à esquerda da mediana
        y.keys = y.keys[: t - 1]
        if not y.leaf:
            y.children = y.children[:t]

        # inserir z no parent
        parent.children.insert(index + 1, z)
        parent.keys.insert(index, median)

    def insert(self, k: Any) -> bool:
        """Insere a chave k na árvore. Retorna True se inserido, False se duplicata."""
        # checar duplicata
        node, idx = self.search(k)
        if node is not None:
            # já existe — não inserir novamente
            return False

        r = self.root
        if r.is_full():
            s = BTreeNode(self.t, leaf=False)
            s.children.append(r)
            self.root = s
            self.split_child(s, 0)
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(r, k)
        return True

    def _insert_non_full(self, node: BTreeNode, k: Any) -> None:
        i = len(node.keys) - 1
        if node.leaf:
            # inserir em posição correta na lista de chaves
            node.keys.append(None)  # espaço para expandir
            while i >= 0 and node.keys[i] > k:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = k
        else:
            # localizar o filho que deve receber a nova chave
            while i >= 0 and node.keys[i] > k:
                i -= 1
            i += 1
            # se o filho está cheio, split primeiro
            if node.children[i].is_full():
                self.split_child(node, i)
                # após split, a chave mediana sobe para node.keys[i]
                if node.keys[i] < k:
                    i += 1
            self._insert_non_full(node.children[i], k)

    def delete(self, k: Any) -> bool:
        """Remove a chave k da árvore. Retorna True se removido, False caso contrário."""
        node, idx = self.search(k)
        if node is None:
            return False
        
        self._delete_from_node(node, k, idx)
        
        # Se a raiz ficou vazia e tem um filho, o filho vira a nova raiz
        if len(self.root.keys) == 0:
            if not self.root.leaf and len(self.root.children) > 0:
                self.root = self.root.children[0]
        
        return True

    def _delete_from_node(self, node: BTreeNode, k: Any, k_index: int) -> None:
        """Remove a chave k do nó especificado (que já foi encontrado)."""
        t = self.t
        
        if node.leaf:
            # Se é folha, simplesmente remove a chave
            node.keys.pop(k_index)
        else:
            # Se não é folha, há três casos
            left_child = node.children[k_index]
            right_child = node.children[k_index + 1]
            
            if len(left_child.keys) >= t:
                # Caso 1: filho esquerdo tem pelo menos t chaves
                predecessor = self._get_predecessor(node, k_index)
                node.keys[k_index] = predecessor
                self._delete_from_node(left_child, predecessor, 
                                      left_child.find_key_index(predecessor))
            elif len(right_child.keys) >= t:
                # Caso 2: filho direito tem pelo menos t chaves
                successor = self._get_successor(node, k_index)
                node.keys[k_index] = successor
                self._delete_from_node(right_child, successor,
                                      right_child.find_key_index(successor))
            else:
                # Caso 3: ambos filhos têm t-1 chaves, mesclar
                self._merge(node, k_index)
                self._delete_from_node(left_child, k, left_child.find_key_index(k))

    def _get_predecessor(self, node: BTreeNode, k_index: int) -> Any:
        """Obtém o maior valor na subárvore enraizada no filho esquerdo."""
        current = node.children[k_index]
        while not current.leaf:
            current = current.children[-1]
        return current.keys[-1]

    def _get_successor(self, node: BTreeNode, k_index: int) -> Any:
        """Obtém o menor valor na subárvore enraizada no filho direito."""
        current = node.children[k_index + 1]
        while not current.leaf:
            current = current.children[0]
        return current.keys[0]

    def _merge(self, node: BTreeNode, k_index: int) -> None:
        """Mescla o filho direito com o filho esquerdo e move a chave do nó."""
        t = self.t
        left_child = node.children[k_index]
        right_child = node.children[k_index + 1]
        
        # Mover chave do nó para left_child
        left_child.keys.append(node.keys[k_index])
        
        # Mover todas as chaves de right_child para left_child
        left_child.keys.extend(right_child.keys)
        
        # Se não é folha, mover filhos também
        if not left_child.leaf:
            left_child.children.extend(right_child.children)
        
        # Remover chave do nó e remover referência ao right_child
        node.keys.pop(k_index)
        node.children.pop(k_index + 1)

    def _fill_child(self, node: BTreeNode, k_index: int) -> None:
        """Garante que o filho tenha pelo menos t chaves."""
        t = self.t
        
        # Se filho anterior tem pelo menos t chaves, pegar uma
        if k_index != 0 and len(node.children[k_index - 1].keys) >= t:
            self._borrow_from_prev(node, k_index)
        # Se filho posterior tem pelo menos t chaves, pegar uma
        elif k_index != len(node.children) - 1 and len(node.children[k_index + 1].keys) >= t:
            self._borrow_from_next(node, k_index)
        # Caso contrário, mesclar com irmão
        else:
            if k_index != len(node.children) - 1:
                self._merge(node, k_index)
            else:
                self._merge(node, k_index - 1)

    def _borrow_from_prev(self, node: BTreeNode, child_index: int) -> None:
        """Empresta uma chave do irmão anterior."""
        child = node.children[child_index]
        sibling = node.children[child_index - 1]
        
        # Mover chave do pai para filho
        child.keys.insert(0, node.keys[child_index - 1])
        
        # Mover última chave do irmão para pai
        node.keys[child_index - 1] = sibling.keys.pop()
        
        # Mover filho se necessário
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node: BTreeNode, child_index: int) -> None:
        """Empresta uma chave do irmão posterior."""
        child = node.children[child_index]
        sibling = node.children[child_index + 1]
        
        # Mover chave do pai para filho
        child.keys.append(node.keys[child_index])
        
        # Mover primeira chave do irmão para pai
        node.keys[child_index] = sibling.keys.pop(0)
        
        # Mover filho se necessário
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def visualize(self, filename="tree", view=False) -> str:
        """Gera visualização com graphviz e retorna o caminho do arquivo."""
        try:
            from graphviz import Digraph
        except ImportError:
            raise ImportError(
                "Biblioteca graphviz não está instalada.\n"
                "Execute: pip install graphviz\n\n"
                "Também é necessário instalar o executável Graphviz no sistema:\n"
                "- Windows: https://graphviz.org/download/ ou 'winget install graphviz'\n"
                "- Linux: sudo apt install graphviz\n"
                "- Mac: brew install graphviz"
            )
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        files_dir = os.path.join(current_dir, 'files')
        os.makedirs(files_dir, exist_ok=True)
        
        output_path = os.path.join(files_dir, filename)
        
        dot = Digraph(comment='BTree 2-3-4')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='box', style='filled', fontsize='10', fontname='Arial')
        
        self.node_counter = 0
        
        def add_nodes(node):
            node_id = f"node_{self.node_counter}"
            self.node_counter += 1
            
            # Label do nó com as chaves
            keys_str = " | ".join(map(str, node.keys)) if node.keys else "∅"
            dot.node(node_id, keys_str, fillcolor='lightblue', fontcolor='black')
            
            if not node.leaf:
                for child in node.children:
                    child_id = add_nodes(child)
                    dot.edge(node_id, child_id)
            
            return node_id
        
        if self.root.keys or not self.root.leaf:
            add_nodes(self.root)
        else:
            dot.node('empty', 'Árvore Vazia', shape='plaintext')
        
        # Renderiza o grafo
        rendered_path = dot.render(output_path, format='png', cleanup=True, view=view)
        return rendered_path

    def pretty_print(self) -> None:
        """Imprime a árvore por níveis (BFS), mostrando chaves de cada nó."""
        q = deque([(self.root, 0)])
        current_level = 0
        line = []
        while q:
            node, lvl = q.popleft()
            if lvl != current_level:
                print(f"Nível {current_level}: {' | '.join(line)}")
                line = []
                current_level = lvl
            line.append("[" + ", ".join(map(str, node.keys)) + "]")
            if not node.leaf:
                for child in node.children:
                    q.append((child, lvl + 1))
        if line:
            print(f"Nível {current_level}: {' | '.join(line)}")


if __name__ == "__main__":
    # Teste simples
    valores = [50, 40, 60, 30, 70, 10, 20, 55, 45, 35, 65, 75]
    tree = BTree234()
    
    print("Inserindo valores:", valores)
    for v in valores:
        tree.insert(v)

    print("\nTravessia em ordem:", tree.traverse())
    print("\nImpressão por níveis:")
    tree.pretty_print()

    # Teste de busca
    print("\nTeste de busca:")
    for k in [55, 99, 10, 70]:
        node, idx = tree.search(k)
        if node:
            print(f"✓ Encontrado {k} no nó {node.keys} no índice {idx}")
        else:
            print(f"✗ {k} não encontrado")

    # Teste de deleção
    print("\n" + "="*50)
    print("Testando deleção:")
    print("="*50)
    
    print("\nAntes da deleção:")
    tree.pretty_print()
    
    tree.delete(30)
    print("\nApós deletar 30:")
    tree.pretty_print()
    
    tree.delete(55)
    print("\nApós deletar 55:")
    tree.pretty_print()
