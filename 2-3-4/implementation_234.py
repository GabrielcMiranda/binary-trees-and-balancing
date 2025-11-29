"""
Menu Interativo para Árvore 2-3-4 (B-tree de grau mínimo t=2)
Implementação com interface semelhante à Red-Black Tree Session
Salva visualizações com Graphviz após cada operação
"""

import os
import sys
from datetime import datetime
from collections import deque

# Importar a classe BTree234 do módulo 2-3-4
# Usando importlib para importar nome com hífen
import importlib.util
spec = importlib.util.spec_from_file_location("btree234", os.path.join(os.path.dirname(__file__), "2-3-4.py"))
btree_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(btree_module)
BTree234 = btree_module.BTree234


class BTree234Session:
    """Gerencia uma sessão interativa da Árvore 2-3-4 com visualizações."""
    
    def __init__(self):
        self.tree = BTree234()
        self.session_name = self._create_session_name()
        self.base_path = self._create_directory_structure()
        
    def _create_session_name(self):
        """Cria um nome único para a sessão com timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"arvore_{timestamp}"
    
    def _create_directory_structure(self):
        """Cria a estrutura de pastas para armazenar as visualizações."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(current_dir, 'files', self.session_name)
        os.makedirs(os.path.join(base_path, 'insercoes'), exist_ok=True)
        os.makedirs(os.path.join(base_path, 'remocoes'), exist_ok=True)
        # Não cria mais a pasta buscas
        return base_path
    
    def _save_visualization(self, filename, subfolder=None):
        """Salva a visualização da árvore em arquivo PNG com graphviz."""
        if not filename.endswith('.png'):
            filename = f"{filename}.png"
        if subfolder:
            folder_path = os.path.join(self.base_path, subfolder)
        else:
            folder_path = self.base_path
        try:
            os.makedirs(folder_path, exist_ok=True)
            output_path = os.path.join(folder_path, filename)
            # Remove extensão duplicada se houver
            if output_path.endswith('.png.png'):
                output_path = output_path[:-4]
            rendered_path = self.tree.visualize(output_path[:-4], view=False)
            return rendered_path
        except Exception as e:
            print(f"❌ Erro ao gerar visualização: {e}")
            return None
    
    def _get_tree_structure(self) -> str:
        """Retorna a estrutura da árvore em formato de texto."""
        from collections import deque
        
        lines = []
        q = deque([(self.tree.root, 0)])
        current_level = 0
        line = []
        
        while q:
            node, lvl = q.popleft()
            if lvl != current_level:
                lines.append(f"Nível {current_level}: {' | '.join(line)}")
                line = []
                current_level = lvl
            line.append("[" + ", ".join(map(str, node.keys)) + "]")
            if not node.leaf:
                for child in node.children:
                    q.append((child, lvl + 1))
        
        if line:
            lines.append(f"Nível {current_level}: {' | '.join(line)}")
        
        return "\n".join(lines)
    
    def _get_info_arvore(self):
        """Retorna informações sobre a árvore."""
        def contar_nos_e_chaves(node):
            if not node or (node.leaf and len(node.keys) == 0 and len(node.children) == 0):
                return 0, 0
            total_nos = 1
            total_chaves = len(node.keys)
            if not node.leaf:
                for child in node.children:
                    nos, chaves = contar_nos_e_chaves(child)
                    total_nos += nos
                    total_chaves += chaves
            return total_nos, total_chaves
        
        total_nos, total_chaves = contar_nos_e_chaves(self.tree.root)
        return {
            'total_nos': total_nos,
            'total_chaves': total_chaves,
            'raiz': self.tree.root.keys if self.tree.root.keys else [],
            'profundidade': self._calcular_profundidade()
        }
    
    def _calcular_profundidade(self):
        """Calcula a profundidade da árvore."""
        def depth(node):
            if node.leaf:
                return 1
            if len(node.children) == 0:
                return 1
            return 1 + depth(node.children[0])
        return depth(self.tree.root)
    
    def _log_operacao(self, operacao, detalhes):
        """Registra uma operação no arquivo de log."""
        if not self.base_path:
            return
        
        log_file = os.path.join(self.base_path, "operacoes.log")
        
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            info = self._get_info_arvore()
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"OPERAÇÃO: {operacao}\n")
                f.write(f"Timestamp: {timestamp}\n")
                f.write("=" * 70 + "\n")
                f.write(f"Detalhes: {detalhes}\n")
                f.write(f"\nEstado da Árvore após operação:\n")
                f.write(f"  • Nós: {info['total_nos']}\n")
                f.write(f"  • Chaves: {info['total_chaves']}\n")
                f.write(f"  • Raiz: {info['raiz'] if info['raiz'] else 'Vazia'}\n")
                f.write(f"  • Profundidade: {info['profundidade']}\n")
                f.write(f"  • Chaves em ordem: {self.tree.traverse()}\n")
                f.write("-" * 70 + "\n")
        except Exception as e:
            print(f"❌ Erro ao registrar operação: {e}")
    
    def inserir_no(self):
        """Menu para inserir um nó interativamente."""
        print("\n" + "=" * 60)
        print("INSERIR NÓ")
        print("=" * 60)
        try:
            valor = input("\nDigite o valor a inserir (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("❌ Erro: Digite um número inteiro válido!")
            return
        print(f"\n📊 Salvando estado ANTES da inserção...")
        antes_path = self._save_visualization(f"valor_{valor}_antes.png", "insercoes")
        inserido = self.tree.insert(valor)
        print(f"📊 Salvando estado DEPOIS da inserção...")
        depois_path = self._save_visualization(f"valor_{valor}_depois.png", "insercoes")
        if inserido:
            print(f"\n✅ Valor {valor} inserido com sucesso!")
        else:
            print(f"\n⚠️  Valor {valor} já existe na árvore (duplicata ignorada)!")
        print(f"\n📁 Arquivos salvos em:")
        if antes_path:
            print(f"   • Antes:  {os.path.basename(antes_path)}")
        if depois_path:
            print(f"   • Depois: {os.path.basename(depois_path)}")
        self._exibir_estado_arvore()
    
    def remover_no(self):
        """Menu para remover um nó interativamente."""
        print("\n" + "=" * 60)
        print("REMOVER NÓ")
        print("=" * 60)
        try:
            valor = input("\nDigite o valor a remover (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("❌ Erro: Digite um número inteiro válido!")
            return
        node, idx = self.tree.search(valor)
        if not node:
            print(f"\n❌ Valor {valor} não encontrado na árvore!")
            return
        print(f"\n📊 Salvando estado ANTES da remoção...")
        antes_path = self._save_visualization(f"valor_{valor}_antes.png", "remocoes")
        removido = self.tree.delete(valor)
        print(f"📊 Salvando estado DEPOIS da remoção...")
        depois_path = self._save_visualization(f"valor_{valor}_depois.png", "remocoes")
        if removido:
            print(f"\n✅ Valor {valor} removido com sucesso da árvore!")
        else:
            print(f"\n❌ Erro ao remover o valor {valor}!")
        print(f"\n📁 Arquivos salvos em:")
        if antes_path:
            print(f"   • Antes:  {os.path.basename(antes_path)}")
        if depois_path:
            print(f"   • Depois: {os.path.basename(depois_path)}")
        self._exibir_estado_arvore()
    
    def buscar_no(self):
        """Menu para buscar um nó interativamente."""
        print("\n" + "=" * 60)
        print("BUSCAR NÓ")
        print("=" * 60)
        try:
            valor = input("\nDigite o valor a buscar (número inteiro): ").strip()
            valor = int(valor)
        except ValueError:
            print("❌ Erro: Digite um número inteiro válido!")
            return
        print(f"\n📊 Gerando visualização do estado atual...")
        # Sempre sobrescreve o mesmo arquivo na raiz da sessão
        estado_path = self._save_visualization("estado_atual.png")
        node, idx = self.tree.search(valor)
        print(f"\n{'='*60}")
        if node:
            print(f"✅ VALOR ENCONTRADO!")
            print(f"{'='*60}")
            print(f"\nDetalhes do nó:")
            print(f"   • Valor: {valor}")
            print(f"   • Chaves do nó: {node.keys}")
            print(f"   • Índice no nó: {idx}")
            print(f"   • Posição na lista: {idx + 1}/{len(node.keys)}")
            print(f"   • É folha: {'Sim' if node.leaf else 'Não'}")
        else:
            print(f"❌ VALOR NÃO ENCONTRADO!")
            print(f"{'='*60}")
            print(f"\n   O valor {valor} não existe na árvore.")
        if estado_path:
            print(f"\n📁 Visualização salva em: {os.path.basename(estado_path)}")
        self._exibir_estado_arvore()
    
    def _exibir_estado_arvore(self):
        """Exibe o estado atual da árvore."""
        print(f"\n📊 Estado atual da árvore:")
        self.tree.pretty_print()
    
    def mostrar_info_arvore(self):
        """Exibe informações detalhadas sobre a árvore."""
        print("\n" + "=" * 60)
        print("INFORMAÇÕES DA ÁRVORE")
        print("=" * 60)
        
        info = self._get_info_arvore()
        
        print(f"\n   • Total de nós: {info['total_nos']}")
        print(f"   • Total de chaves: {info['total_chaves']}")
        print(f"   • Grau mínimo (t): {self.tree.t}")
        print(f"   • Máximo de chaves por nó: {2 * self.tree.t - 1}")
        print(f"   • Raiz: {info['raiz'] if info['raiz'] else '(Vazia)'}")
        print(f"   • Profundidade: {info['profundidade']}")
        
        print(f"\n📋 Chaves em ordem (travessia em-ordem):")
        chaves_ordenadas = self.tree.traverse()
        if chaves_ordenadas:
            print(f"   {chaves_ordenadas}")
        else:
            print(f"   (Árvore vazia)")
        
        print(f"\n📁 Diretório da sessão:")
        print(f"   {self.base_path}")
    
    def listar_em_ordem(self):
        """Exibe as chaves em ordem crescente."""
        print("\n" + "=" * 60)
        print("TRAVESSIA EM-ORDEM")
        print("=" * 60)
        
        chaves = self.tree.traverse()
        
        if chaves:
            print(f"\n✅ Chaves em ordem crescente:")
            print(f"\n   {chaves}")
            print(f"\n   Total de chaves: {len(chaves)}")
        else:
            print(f"\n⚠️  Árvore vazia!")
    
    def exibir_menu(self):
        """Exibe o menu principal."""
        print("\n" + "=" * 60)
        print("ÁRVORE 2-3-4 - MENU INTERATIVO")
        print("=" * 60)
        print(f"📂 Sessão: {self.session_name}")
        print(f"📁 Pasta: {os.path.relpath(self.base_path)}")
        print("=" * 60)
        print("\n1. 📥 Inserir nó")
        print("2. 🗑️  Remover nó")
        print("3. 🔍 Buscar nó")
        print("4. 📊 Informações da árvore")
        print("5. 📋 Listar em ordem")
        print("6. 🚪 Sair")
        print("\n" + "=" * 60)
    
    def executar(self):
        """Inicia o loop principal da interface interativa."""
        print("\n" + "🌳" * 30)
        print("\n   BEM-VINDO À ÁRVORE 2-3-4 INTERATIVA!")
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
                self.listar_em_ordem()
            elif escolha == '6':
                print("\n" + "=" * 60)
                print("👋 Encerrando sessão...")
                print("=" * 60)
                print(f"\n📁 Todos os arquivos foram salvos em:")
                print(f"   {os.path.relpath(self.base_path)}")
                print("\n✅ Sessão encerrada com sucesso!")
                print("\n" + "🌳" * 30 + "\n")
                break
            else:
                print("\n❌ Opção inválida! Digite um número de 1 a 6.")
            
            input("\n⏎ Pressione ENTER para continuar...")


def main():
    """Função principal."""
    session = BTree234Session()
    session.executar()


if __name__ == "__main__":
    main()
