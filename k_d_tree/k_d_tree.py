from graphviz import Digraph
import math

class Node:
    def __init__(self, point: list[float], depth: int = 0, k: int = 2):
        self.point = point
        self.depth = depth
        self.k = k
        
        self.left = None
        self.right = None
        self.parent = None

    def axis(self):
        return self.depth % self.k

class KDTree:
    def __init__(self, k: int = 2):
        self.k = k
        self.root = None
        self.size = 0

    def insert(self, point: list[float]) -> bool:
        if self.root is None:
            self.root = Node(point, 0, self.k)
            self.size += 1
            return True
        
        node = self.root
        depth = 0
        
        while True:
            if node.point == point:
                return False
            
            axis = depth % self.k
            
            if point[axis] < node.point[axis]:
                if node.left is None:
                    node.left = Node(point, depth + 1, self.k)
                    node.left.parent = node
                    self.size += 1
                    self._check_and_rebuild()
                    return True
                else:
                    node = node.left
                    depth += 1
            else:
                if node.right is None:
                    node.right = Node(point, depth + 1, self.k)
                    node.right.parent = node
                    self.size += 1
                    self._check_and_rebuild()
                    return True
                else:
                    node = node.right
                    depth += 1

    def delete(self, point: list[float]) -> bool:
        node = self.root
        parent = None
        is_left_child = False
        
        while node:
            if node.point == point:
                break
            
            axis = node.axis()
            parent = node
            
            if point[axis] < node.point[axis]:
                node = node.left
                is_left_child = True
            else:
                node = node.right
                is_left_child = False
        
        if node is None or node.point != point:
            return False
        
        self.size -= 1

        # sem filho
        if node.left is None and node.right is None:
            if parent is None:
                self.root = None
            elif is_left_child:
                parent.left = None
            else:
                parent.right = None
        
        # só filho esquerdo
        elif node.right is None:
            if parent is None:
                self.root = node.left
            elif is_left_child:
                parent.left = node.left
            else:
                parent.right = node.left
            
            if node.left:
                node.left.parent = parent
        
        # só filho direito
        elif node.left is None:
            if parent is None:
                self.root = node.right
            elif is_left_child:
                parent.left = node.right
            else:
                parent.right = node.right
            
            if node.right:
                node.right.parent = parent
        
        # dois filhos
        else:
            # Encontrar o mínimo na subárvore direita (iterativo!)
            min_node = node.right
            min_parent = node
            
            while min_node.left:
                min_parent = min_node
                min_node = min_node.left
            
            # Substituir o nó pelo mínimo
            node.point = min_node.point
            
            # Agora deletar o mínimo (que tem no máximo um filho direito)
            if min_parent == node:
                # Mínimo é filho direito direto
                node.right = min_node.right
                if min_node.right:
                    min_node.right.parent = node
            else:
                # Mínimo é neto
                min_parent.left = min_node.right
                if min_node.right:
                    min_node.right.parent = min_parent
        
        if self.root:
            self._check_and_rebuild()
        
        return True

    def search(self, point: list[float]) -> list[float] | None:
        node = self.root
        depth = 0
        
        while node is not None:
            if node.point == point:
                return node.point
            
            axis = depth % self.k
            
            if point[axis] < node.point[axis]:
                node = node.left
            else:
                node = node.right
            
            depth += 1
        
        return None

    def _check_and_rebuild(self):
        if self.size < 3:
            return
        
        # coletando os pontos de coordenada dos nós
        points = []
        stack = [self.root]
        
        while stack:
            node = stack.pop()
            if node:
                points.append(node.point)
                if node.right:
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
        
        # Construindo a árvore novamente
        if not points:
            self.root = None
            return
        
        # pilha
        stack = [(0, len(points), 0, None, False)]
        self.root = None
        
        while stack:
            start, end, depth, parent, is_left = stack.pop()
            
            if start >= end:
                continue
            
            # ordena pelo eixo atual e encontra mediana
            axis = depth % self.k
            mid = (start + end) // 2
            points[start:end] = sorted(points[start:end], key=lambda p: p[axis])
            
            # cria o no
            node = Node(points[mid], depth, self.k)
            node.parent = parent
            
            if parent is None:
                self.root = node
            elif is_left:
                parent.left = node
            else:
                parent.right = node
            
            # adiciona subárvores à pilha (direita primeiro, depois esquerda)
            if mid + 1 < end:
                stack.append((mid + 1, end, depth + 1, node, False))
            if start < mid:
                stack.append((start, mid, depth + 1, node, True))

    def visualize(self, filename: str = "kdtree", silent: bool = False) -> str:
        if self.root is None:
            if not silent:
                print("Árvore vazia!")
            return ""
        
        dot = Digraph(comment='k-D Tree', format='png')
        dot.attr(rankdir='TB', bgcolor='white')
        dot.attr('node', shape='circle', style='filled', fillcolor='#4ECDC4', 
                color='black', penwidth='2.5', fontname='monospace', fontsize='14', fontweight='bold')
        dot.attr('edge', color='black', penwidth='2')
        
        counter = [0]
        self._add_nodes_to_graph(self.root, dot, counter)
        
        output_path = dot.render(filename, cleanup=True)
        if not silent:
            print(f"Visualização gerada: {output_path}")
        return output_path
    
    def _add_nodes_to_graph(self, root: Node | None, dot: Digraph, counter: list):
        if root is None:
            return
        
        # pilha   node parent_id é_raiz
        stack = [(root, None, True)]
        
        while stack:
            node, parent_id, eh_raiz = stack.pop()
            
            if node is None:
                continue
            
            counter[0] += 1
            node_id = f"node_{counter[0]}"
            
            coords_str = ', '.join(f"{c:.0f}" for c in node.point)
            label = coords_str.replace(', ', '\n')
            
            if eh_raiz:
                dot.node(node_id, label=label, fillcolor='#FF6B6B', fontsize='16')
            else:
                dot.node(node_id, label=label)

            if parent_id is not None:
                dot.edge(parent_id, node_id)
            
            # adicionando os filhos
            if node.right:
                stack.append((node.right, node_id, False))
            if node.left:
                stack.append((node.left, node_id, False))
