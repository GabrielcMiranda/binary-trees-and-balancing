# Red-Black Tree (Árvore Rubro-Negra)

## O que é uma Red-Black Tree?

A Red-Black Tree é uma árvore binária de busca **auto-balanceada** que utiliza um esquema de cores (vermelho 🔴 e preto ⚫) para garantir que a árvore permaneça aproximadamente balanceada durante inserções e remoções. Foi inventada por Rudolf Bayer em 1972 e é amplamente utilizada em estruturas de dados de alto desempenho.

## Propriedades Fundamentais

Uma Red-Black Tree deve satisfazer as seguintes propriedades:

1. **Propriedade de Cor**: Todo nó é vermelho 🔴 ou preto ⚫
2. **Propriedade da Raiz**: A raiz é sempre preta
3. **Propriedade das Folhas**: Todas as folhas (nós NIL) são pretas
4. **Propriedade Vermelha**: Se um nó é vermelho, ambos os seus filhos são pretos (não pode haver dois nós vermelhos consecutivos)
5. **Propriedade da Black-Height**: Todos os caminhos de qualquer nó até suas folhas descendentes contêm o mesmo número de nós pretos

## Por que usar Red-Black Trees?

### Vantagens
- **Balanceamento Garantido**: Altura máxima de 2·log₂(n+1)
- **Operações Eficientes**: O(log n) para inserção, busca e remoção
- **Menos Rotações**: Comparado com AVL, requer menos rotações em inserções
- **Performance Consistente**: Não há casos degenerados

### Comparação com outras estruturas

| Estrutura | Busca | Inserção | Remoção | Altura |
|-----------|-------|----------|---------|--------|
| Array não ordenado | O(n) | O(1) | O(n) | - |
| Array ordenado | O(log n) | O(n) | O(n) | - |
| BST (pior caso) | O(n) | O(n) | O(n) | O(n) |
| Red-Black Tree | O(log n) | O(log n) | O(log n) | O(log n) |
| AVL Tree | O(log n) | O(log n) | O(log n) | O(log n) |

## Operações e Complexidade

| Operação | Complexidade | Descrição |
|----------|--------------|-----------|
| **Inserção** | O(log n) | Adiciona elemento com rebalanceamento automático |
| **Busca** | O(log n) | Localiza elemento na árvore |
| **Remoção** | O(log n) | Remove elemento com rebalanceamento automático |
| **Espaço** | O(n) | Memória proporcional ao número de elementos |

## Mecanismos de Balanceamento

### Rotações

As rotações são operações fundamentais para manter o balanceamento:

- **Rotação à Esquerda**: Move um nó para baixo e seu filho direito para cima
- **Rotação à Direita**: Move um nó para baixo e seu filho esquerdo para cima

### Recoloração

Durante inserções e remoções, nós podem ter suas cores alteradas para manter as propriedades da Red-Black Tree.

## Aplicações Práticas

Red-Black Trees são usadas em:

- **std::map e std::set** do C++
- **TreeMap e TreeSet** do Java
- **Kernel do Linux**: Gerenciamento de processos e memória virtual
- **Banco de Dados**: Índices e estruturas de ordenação
- **Compiladores**: Tabelas de símbolos

## Casos de Uso Ideais

Use Red-Black Tree quando você precisa:
- ✅ Inserções, remoções e buscas frequentes
- ✅ Garantia de performance O(log n) no pior caso
- ✅ Percorrimento ordenado dos elementos
- ✅ Estrutura auto-balanceada sem manutenção manual

Evite quando:
- ❌ Dados raramente mudam (array ordenado pode ser melhor)
- ❌ Acesso por índice é frequente (use array)
- ❌ Memória é extremamente limitada (overhead de ponteiros e cores)

## Estrutura do Nó

```python
class Node:
    data: any           # Valor armazenado
    color: str          # '🔴' (vermelho) ou '⚫' (preto)
    count: int          # Contador de repetições
    left: Node          # Filho esquerdo
    right: Node         # Filho direito
    parent: Node        # Nó pai
```

## Uso Básico

```python
from red_black_tree import RedBlackTree

# Criar árvore
rbt = RedBlackTree()

# Inserir elementos (com balanceamento automático)
rbt.insert(50)
rbt.insert(25)
rbt.insert(75)
rbt.insert(25)  # Incrementa contador

# Buscar
node = rbt.search(25)
if node:
    print(f"Valor: {node.data}, Count: {node.count}")

# Remover (com balanceamento automático)
rbt.delete(25)

# Visualizar
rbt.visualize("arvore", view=True)
```

## Referências

- **Cormen, T. H., et al.** (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Capítulo 13: Red-Black Trees.
- **Sedgewick, R., & Wayne, K.** (2011). *Algorithms* (4th ed.). Addison-Wesley.
- **Bayer, R.** (1972). Symmetric binary B-Trees: Data structure and maintenance algorithms.
