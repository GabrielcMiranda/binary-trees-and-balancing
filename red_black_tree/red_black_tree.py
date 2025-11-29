class Node:
    
    def __init__(self, data):
        self.data = data
        self.color = '🔴' 
        self.count = 1  
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        if self.count > 1:
            return f"{self.data}({self.count}){self.color}"
        return f"{self.data}{self.color}"


class RedBlackTree:
   
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.color = '⚫'
        self.NIL.left = None
        self.NIL.right = None
        self.root = self.NIL

    def insert(self, data):
        parent = None
        current = self.root
        
        while current != self.NIL:
            parent = current
            if data == current.data:
                
                current.count += 1
                return
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        
        new_node = Node(data)
        new_node.left = self.NIL
        new_node.right = self.NIL
        new_node.parent = parent
        
        if parent is None:
            self.root = new_node
        elif data < parent.data:
            parent.left = new_node
        else:
            parent.right = new_node
        
        if new_node.parent is None:
            new_node.color = '⚫'
            return
        
        if new_node.parent.parent is None:
            return
        
        self._fix_insert(new_node)

    def _fix_insert(self, node):
       
        while node.parent.color == '🔴':
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                
                if uncle.color == '🔴':
                    
                    uncle.color = '⚫'
                    node.parent.color = '⚫'
                    node.parent.parent.color = '🔴'
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        
                        node = node.parent
                        self._rotate_right(node)
                    
                    node.parent.color = '⚫'
                    node.parent.parent.color = '🔴'
                    self._rotate_left(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                
                if uncle.color == '🔴':
                    
                    uncle.color = '⚫'
                    node.parent.color = '⚫'
                    node.parent.parent.color = '🔴'
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                       
                        node = node.parent
                        self._rotate_left(node)
                    
                    node.parent.color = '⚫'
                    node.parent.parent.color = '🔴'
                    self._rotate_right(node.parent.parent)
            
            if node == self.root:
                break
        
        self.root.color = '⚫'

    def _rotate_left(self, node):
       
        right_child = node.right
        node.right = right_child.left
        
        if right_child.left != self.NIL:
            right_child.left.parent = node
        
        right_child.parent = node.parent
        
        if node.parent is None:
            self.root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        
        right_child.left = node
        node.parent = right_child

    def _rotate_right(self, node):
        
        left_child = node.left
        node.left = left_child.right
        
        if left_child.right != self.NIL:
            left_child.right.parent = node
        
        left_child.parent = node.parent
        
        if node.parent is None:
            self.root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        
        left_child.right = node
        node.parent = left_child

    def search(self, data):
    
        return self._search_helper(self.root, data)

    def _search_helper(self, node, data):
      
        if node == self.NIL or data == node.data:
            return node if node != self.NIL else None
        
        if data < node.data:
            return self._search_helper(node.left, data)
        return self._search_helper(node.right, data)

    def delete(self, data):
      
        node = self.search(data)
        if node is None:
            return False
        
        if node.count > 1:
            node.count -= 1
            return True
        
        self._delete_node(node)
        return True

    def _delete_node(self, node):
      
        y = node
        y_original_color = y.color
        
        if node.left == self.NIL:
            x = node.right
            self._transplant(node, node.right)
        elif node.right == self.NIL:
            x = node.left
            self._transplant(node, node.left)
        else:
            y = self._minimum(node.right)
            y_original_color = y.color
            x = y.right
            
            if y.parent == node:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = node.right
                y.right.parent = y
            
            self._transplant(node, y)
            y.left = node.left
            y.left.parent = y
            y.color = node.color
        
        if y_original_color == '⚫':
            self._fix_delete(x)

    def _fix_delete(self, node):
       
        while node != self.root and node.color == '⚫':
            if node == node.parent.left:
                sibling = node.parent.right
                
                if sibling.color == '🔴':
                    sibling.color = '⚫'
                    node.parent.color = '🔴'
                    self._rotate_left(node.parent)
                    sibling = node.parent.right
                
                if sibling.left.color == '⚫' and sibling.right.color == '⚫':
                    sibling.color = '🔴'
                    node = node.parent
                else:
                    if sibling.right.color == '⚫':
                        sibling.left.color = '⚫'
                        sibling.color = '🔴'
                        self._rotate_right(sibling)
                        sibling = node.parent.right
                    
                    sibling.color = node.parent.color
                    node.parent.color = '⚫'
                    sibling.right.color = '⚫'
                    self._rotate_left(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                
                if sibling.color == '🔴':
                    sibling.color = '⚫'
                    node.parent.color = '🔴'
                    self._rotate_right(node.parent)
                    sibling = node.parent.left
                
                if sibling.right.color == '⚫' and sibling.left.color == '⚫':
                    sibling.color = '🔴'
                    node = node.parent
                else:
                    if sibling.left.color == '⚫':
                        sibling.right.color = '⚫'
                        sibling.color = '🔴'
                        self._rotate_left(sibling)
                        sibling = node.parent.left
                    
                    sibling.color = node.parent.color
                    node.parent.color = '⚫'
                    sibling.left.color = '⚫'
                    self._rotate_right(node.parent)
                    node = self.root
        
        node.color = '⚫'

    def _transplant(self, u, v):
       
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
      
        while node.left != self.NIL:
            node = node.left
        return node

    def visualize(self, filename="red_black_tree", view=True):
        
        try:
            from graphviz import Digraph
            import os
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
        
        dot = Digraph(comment='Red-Black Tree')
        dot.attr(rankdir='TB')
        dot.attr('node', shape='circle', style='filled', fontsize='12', fontname='Arial Bold')
        
        nil_counter = [0]
        
        def add_nodes(node):
            if node == self.NIL:
                return
            
            if node.color == '🔴':
                color = 'red'
                fontcolor = 'white'
            else:
                color = 'black'
                fontcolor = 'white'
            

            if node.count > 1:
                label = f"{node.data}\n({node.count})"
            else:
                label = str(node.data)
            
            # Adiciona o nó
            dot.node(str(id(node)), label, fillcolor=color, fontcolor=fontcolor)
            
            # Adiciona filho esquerdo
            if node.left != self.NIL:
                dot.edge(str(id(node)), str(id(node.left)), label='L')
                add_nodes(node.left)
            else:
                # Adiciona NIL visual
                nil_id = f"nil_{nil_counter[0]}"
                nil_counter[0] += 1
                dot.node(nil_id, 'NIL', fillcolor='lightgray', fontcolor='black', 
                        shape='square', style='filled')
                dot.edge(str(id(node)), nil_id, style='dashed')
            
            # Adiciona filho direito
            if node.right != self.NIL:
                dot.edge(str(id(node)), str(id(node.right)), label='R')
                add_nodes(node.right)
            else:
                # Adiciona NIL visual
                nil_id = f"nil_{nil_counter[0]}"
                nil_counter[0] += 1
                dot.node(nil_id, 'NIL', fillcolor='lightgray', fontcolor='black',
                        shape='square', style='filled')
                dot.edge(str(id(node)), nil_id, style='dashed')
        
        if self.root != self.NIL:
            add_nodes(self.root)
        else:
            dot.node('empty', 'Árvore Vazia', shape='plaintext')
        
        # Renderiza o grafo no diretório files
        rendered_path = dot.render(output_path, format='png', cleanup=True, view=view)
        return rendered_path

