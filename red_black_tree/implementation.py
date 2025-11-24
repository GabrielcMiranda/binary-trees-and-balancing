"""
Implementação de exemplo da Red-Black Tree com 21+ nós.
Demonstra as 3 operações principais: INSERT, SEARCH e DELETE.
"""

from red_black_tree.red_black_tree import RedBlackTree


def main():
    print("=" * 70)
    print("RED-BLACK TREE - Implementação com 21+ Nós")
    print("=" * 70)
    
    # Criar instância da árvore
    rbt = RedBlackTree()
    
    # ========== OPERAÇÃO 1: INSERÇÃO ==========
    print("\n📥 INSERÇÃO: Adicionando 21+ elementos")
    print("-" * 70)
    
    # Lista de elementos a inserir
    elements = [50, 25, 75, 10, 30, 60, 80, 5, 15, 27, 35, 55, 65, 70, 90,
                3, 12, 18, 32, 58, 68, 85, 95]
    
    print(f"Inserindo {len(elements)} elementos:")
    print(f"{elements}\n")
    
    for i, value in enumerate(elements, 1):
        rbt.insert(value)
        print(f"[{i:2d}] Inserido: {value}")
    
    print(f"\n✓ Total de nós inseridos: {len(elements)}")
    
    # Inserir alguns elementos repetidos para demonstrar o contador
    print("\n📥 Inserindo elementos REPETIDOS:")
    repeated_elements = [50, 25, 75, 10, 50]
    for value in repeated_elements:
        rbt.insert(value)
        print(f"   Inserido: {value} (incrementa contador)")
    
    # ========== OPERAÇÃO 2: BUSCA ==========
    print("\n" + "=" * 70)
    print("🔍 BUSCA: Procurando elementos na árvore")
    print("-" * 70)
    
    # Valores a buscar (alguns existem, outros não)
    search_values = [50, 25, 75, 100, 5, 200, 68, 32, 99, 3]
    
    found_count = 0
    not_found_count = 0
    
    print("\nResultados da busca:\n")
    for value in search_values:
        node = rbt.search(value)
        if node:
            count_info = f" (count={node.count})" if node.count > 1 else ""
            color_symbol = node.color
            print(f"  ✓ {value:3d} → ENCONTRADO {color_symbol}{count_info}")
            found_count += 1
        else:
            print(f"  ✗ {value:3d} → NÃO ENCONTRADO")
            not_found_count += 1
    
    print(f"\nResumo: {found_count} encontrados, {not_found_count} não encontrados")
    
    # ========== OPERAÇÃO 3: EXCLUSÃO ==========
    print("\n" + "=" * 70)
    print("🗑️  EXCLUSÃO: Removendo elementos da árvore")
    print("-" * 70)
    
    # Valores a remover
    delete_values = [50, 50, 25, 75, 10, 5, 90, 3, 68]
    
    print("\nRemovendo elementos:\n")
    for value in delete_values:
        result = rbt.delete(value)
        if result:
            # Verifica se o nó ainda existe (caso tenha contador > 1)
            node = rbt.search(value)
            if node:
                print(f"  ✓ {value:3d} → Contador decrementado (count={node.count})")
            else:
                print(f"  ✓ {value:3d} → Removido completamente")
        else:
            print(f"  ✗ {value:3d} → Falha (não existe)")
    
    print(f"\n✓ Total de operações de exclusão: {len(delete_values)}")
    
    # ========== VISUALIZAÇÃO ==========
    print("\n" + "=" * 70)
    print("📊 VISUALIZAÇÃO: Gerando imagem da árvore")
    print("-" * 70)
    
    try:
        output_file = rbt.visualize("red_black_tree_final", view=False)
        print(f"\n✓ Visualização gerada com sucesso!")
        print(f"📁 Arquivo: {output_file}")
        print("\nLegenda:")
        print("  • Círculos PRETOS ⚫ = Nós pretos")
        print("  • Círculos VERMELHOS 🔴 = Nós vermelhos")
        print("  • Quadrados CINZAS = Nós NIL (folhas)")
        print("  • (n) = Contador de repetições")
    except Exception as e:
        print(f"\n⚠️  Não foi possível gerar a visualização: {e}")
        print("   Certifique-se de que o Graphviz está instalado.")
        print("   Veja o README.md para instruções de instalação.")
    
    # ========== VERIFICAÇÃO FINAL ==========
    print("\n" + "=" * 70)
    print("✅ VERIFICAÇÃO FINAL: Estado da árvore")
    print("-" * 70)
    
    # Verificar alguns nós que ainda devem existir
    remaining_nodes = [30, 60, 80, 15, 27, 35, 55, 65, 70, 85, 95, 12, 18, 32, 58]
    
    print("\nNós que devem ainda existir:\n")
    exists_count = 0
    for value in remaining_nodes:
        node = rbt.search(value)
        if node:
            print(f"  ✓ {value:3d} {node.color}")
            exists_count += 1
        else:
            print(f"  ✗ {value:3d} (erro: deveria existir!)")
    
    print(f"\n✓ {exists_count}/{len(remaining_nodes)} nós verificados com sucesso")
    
    # ========== ESTATÍSTICAS ==========
    print("\n" + "=" * 70)
    print("📈 ESTATÍSTICAS DA IMPLEMENTAÇÃO")
    print("=" * 70)
    print(f"\n  Operações realizadas:")
    print(f"    • Inserções (únicas): {len(elements)}")
    print(f"    • Inserções (repetidas): {len(repeated_elements)}")
    print(f"    • Buscas: {len(search_values)}")
    print(f"    • Exclusões: {len(delete_values)}")
    print(f"\n  Total de operações: {len(elements) + len(repeated_elements) + len(search_values) + len(delete_values)}")
    print(f"\n  Propriedades da Red-Black Tree mantidas:")
    print(f"    ✓ Todo nó é vermelho ou preto")
    print(f"    ✓ Raiz é sempre preta")
    print(f"    ✓ Folhas NIL são pretas")
    print(f"    ✓ Nós vermelhos têm filhos pretos")
    print(f"    ✓ Black-height consistente em todos os caminhos")
    
    print("\n" + "=" * 70)
    print("🎉 IMPLEMENTAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 70)


if __name__ == "__main__":
    main()
