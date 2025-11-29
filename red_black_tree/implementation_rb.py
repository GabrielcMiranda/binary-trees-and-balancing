import os
from datetime import datetime
from red_black_tree.red_black_tree import RedBlackTree


class RedBlackTreeSession:
    
    def __init__(self):
        self.tree = RedBlackTree()
        self.session_name = self._create_session_name()
        self.base_path = self._create_directory_structure()
        
    def _create_session_name(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"arvore_{timestamp}"
    
    def _create_directory_structure(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(current_dir, 'files', self.session_name)
        
        os.makedirs(os.path.join(base_path, 'adicoes'), exist_ok=True)
        os.makedirs(os.path.join(base_path, 'remocoes'), exist_ok=True)
        
        return base_path
    
    def _save_visualization(self, filename, subfolder=None):
        if subfolder:
            path = os.path.join(self.base_path, subfolder, filename)
        else:
            path = os.path.join(self.base_path, filename)
        
        try:
            # Criar diretório temporário para o graphviz
            temp_dir = os.path.dirname(path)
            os.makedirs(temp_dir, exist_ok=True)
            
            output = self.tree.visualize(path, view=False)
            return output
        except Exception as e:
            print(f"Erro ao gerar visualização: {e}")
            return None
    
    def inserir_no(self):
        print("\n" + "=" * 60)
        print("INSERIR NÓ")
        print("=" * 60)
        
        try:
            valor = input("\nDigite o valor a inserir (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
            return
        
        print(f"\nSalvando estado ANTES da inserção...")
        antes_path = self._save_visualization(f"valor_{valor}_antes", "adicoes")
        
        self.tree.insert(valor)
        node = self.tree.search(valor)
        
        print(f"Salvando estado DEPOIS da inserção...")
        depois_path = self._save_visualization(f"valor_{valor}_depois", "adicoes")
        
        print(f"\nValor {valor} inserido com sucesso!")
        if node and node.count > 1:
            print(f"Este valor já existia. Contador incrementado para {node.count}")
        
        print(f"\nImagens salvas em:")
        if antes_path:
            print(f"   • Antes:  {os.path.basename(antes_path)}")
        if depois_path:
            print(f"   • Depois: {os.path.basename(depois_path)}")
    
    def remover_no(self):
        print("\n" + "=" * 60)
        print("REMOVER NÓ")
        print("=" * 60)
        
        try:
            valor = input("\nDigite o valor a remover (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
            return
        
        node = self.tree.search(valor)
        if not node:
            print(f"\nValor {valor} não encontrado na árvore!")
            return
        
        count_antes = node.count
        
        print(f"\nSalvando estado ANTES da remoção...")
        antes_path = self._save_visualization(f"valor_{valor}_antes", "remocoes")
        
        self.tree.delete(valor)
        node_depois = self.tree.search(valor)
        
        print(f"Salvando estado DEPOIS da remoção...")
        depois_path = self._save_visualization(f"valor_{valor}_depois", "remocoes")
        
        if node_depois:
            print(f"\nContador do valor {valor} decrementado!")
            print(f"Contador: {count_antes} → {node_depois.count}")
        else:
            print(f"\nValor {valor} removido completamente da árvore!")
        
        print(f"\nImagens salvas em:")
        if antes_path:
            print(f"   • Antes:  {os.path.basename(antes_path)}")
        if depois_path:
            print(f"   • Depois: {os.path.basename(depois_path)}")
    
    def buscar_no(self):

        print("\n" + "=" * 60)
        print("BUSCAR NÓ")
        print("=" * 60)
        
        try:
            valor = input("\nDigite o valor a buscar (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("Erro: Digite um número inteiro válido!")
            return
        
        print(f"\nGerando visualização do estado atual...")
        estado_path = self._save_visualization("estado_atual")
        
        node = self.tree.search(valor)
        
        print(f"\n{'='*60}")
        if node:
            print(f"VALOR ENCONTRADO!")
            print(f"{'='*60}")
            print(f"\nDetalhes do nó:")
            print(f"   • Valor: {node.data}")
            print(f"   • Cor: {node.color} ({'Vermelho' if node.color == '🔴' else 'Preto'})")
            print(f"   • Contador: {node.count}")
            
            print(f"\nEstrutura:")
            if node.parent and node.parent != self.tree.NIL:
                print(f"   • Pai: {node.parent.data}{node.parent.color}")
            else:
                print(f"   • Pai: (Raiz)")
            
            if node.left != self.tree.NIL:
                print(f"   • Filho Esquerdo: {node.left.data}{node.left.color}")
            else:
                print(f"   • Filho Esquerdo: NIL")
            
            if node.right != self.tree.NIL:
                print(f"   • Filho Direito: {node.right.data}{node.right.color}")
            else:
                print(f"   • Filho Direito: NIL")
        else:
            print(f"VALOR NÃO ENCONTRADO!")
            print(f"{'='*60}")
            print(f"\n   O valor {valor} não existe na árvore.")
        
        if estado_path:
            print(f"\nEstado atual salvo em: {os.path.basename(estado_path)}")
    
    def exibir_menu(self):
        print("\n" + "=" * 60)
        print("RED-BLACK TREE - MENU INTERATIVO")
        print("=" * 60)
        print(f"📂 Sessão: {self.session_name}")
        print(f"📁 Pasta: {os.path.relpath(self.base_path)}")
        print("=" * 60)
        print("\n1. 📥 Inserir nó")
        print("2. 🗑️  Remover nó")
        print("3. 🔍 Buscar nó")
        print("4. 📊 Informações da árvore")
        print("5. 🚪 Sair")
        print("\n" + "=" * 60)
    
    def mostrar_info_arvore(self):
        print("\n" + "=" * 60)
        print("INFORMAÇÕES DA ÁRVORE")
        print("=" * 60)
        
        def contar_nos(node):
            if node == self.tree.NIL:
                return 0, 0  
            
            left_nos, left_vals = contar_nos(node.left)
            right_nos, right_vals = contar_nos(node.right)
            
            return (1 + left_nos + right_nos, node.count + left_vals + right_vals)
        
        total_nos, total_valores = contar_nos(self.tree.root)
        
        print(f"\n   • Nós únicos: {total_nos}")
        print(f"   • Total de valores (com repetições): {total_valores}")
        
        if self.tree.root != self.tree.NIL:
            print(f"   • Raiz: {self.tree.root.data}{self.tree.root.color}")
        else:
            print(f"   • Árvore vazia")
        
        print(f"\nDiretório da sessão:")
        print(f"   {os.path.relpath(self.base_path)}")
    
    def executar(self):
        print("\n" + "🌳" * 30)
        print("\n   BEM-VINDO À RED-BLACK TREE INTERATIVA!")
        print("\n" + "🌳" * 30)
        
        while True:
            self.exibir_menu()
            
            escolha = input("\nEscolha uma opção: ").strip()
            
            if escolha == '1':
                self.inserir_no()
            elif escolha == '2':
                self.remover_no()
            elif escolha == '3':
                self.buscar_no()
            elif escolha == '4':
                self.mostrar_info_arvore()
            elif escolha == '5':
                print("\n" + "=" * 60)
                print("👋 Encerrando sessão...")
                print("=" * 60)
                print(f"\n📁 Todos os arquivos foram salvos em:")
                print(f"   {os.path.relpath(self.base_path)}")
                print("\n✅ Sessão encerrada com sucesso!")
                print("\n" + "🌳" * 30 + "\n")
                break
            else:
                print("\n❌ Opção inválida! Digite um número de 1 a 5.")
            
            input("\n⏎ Pressione ENTER para continuar...")


def main():
    session = RedBlackTreeSession()
    session.executar()


if __name__ == "__main__":
    main()
