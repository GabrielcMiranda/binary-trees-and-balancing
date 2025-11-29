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

## Casos de Balanceamento (Inserção e Remoção)

A seguir estão os casos mais comuns que requerem balanceamento em uma Red-Black Tree. Para cada caso apresentamos um diagrama "antes" e "depois" (ASCII), e uma breve descrição das ações: rotações e/ou recolorações.

Obs.: usamos os símbolos `🔴` para nós vermelhos e `⚫` para nós pretos. `NIL` representa o nó sentinela preto.

### Inserção — Caso 1: Tio vermelho (Recoloração)
Quando o nó recém-inserido tem o pai e o tio vermelhos, a solução é recolorar pai e tio para preto e o avô para vermelho, e então continuar a verificação a partir do avô.

Antes:
```
         G⚫
        /   \\
    P🔴    U🔴
    /
 N🔴
```

Depois (após recoloração):
```
         G🔴
        /   \\
    P⚫    U⚫
    /
 N🔴
```

Se `G` for a raiz, ele deve ser recolorado para preto.

### Inserção — Caso 2: Left-Left (Rotação à direita)
Quando o nó é filho esquerdo de um pai que é filho esquerdo do avô e o tio é preto. Resolve-se com uma rotação à direita em `G` e recoloração adequada.

Antes (LL):
```
         G⚫
        /  \\
    P🔴   U⚫
    /
 N🔴
```

Depois (rot. direita em G + recolor):
```
         P⚫
        /  \\
    N🔴   G🔴
                 \\
                 U⚫
```

Regra prática: após a rotação o antigo `P` passa a ter cor preta e `G` torna-se vermelho (se necessário), preservando as propriedades.

### Inserção — Caso 3: Right-Right (Rotação à esquerda)
Simétrico ao caso LL: quando o nó é filho direito de um pai que é filho direito do avô e o tio é preto. Faz-se uma rotação à esquerda em `G`.

Antes (RR):
```
     G⚫
    /  \\
 U⚫  P🔴
             \\
             N🔴
```

Depois (rot. esquerda em G + recolor):
```
         P⚫
        /  \\
     G🔴  N🔴
    /
 U⚫
```

### Inserção — Caso 4: Left-Right / Right-Left (Dupla rotação)
Quando o nó forma um padrão LR ou RL (pai e nó não estão alinhados), é necessário primeiro rotacionar no pai (para alinhar) e então rotacionar no avô.

Antes (LR):
```
        G⚫
     /  \\
 P🔴   U⚫
    \\
    N🔴
```

Passo intermédio: rotaciona `P` para a esquerda (torna LL)

Depois do passo intermédio:
```
        G⚫
     /  \\
 N🔴   U⚫
 /
P🔴
```

Depois (rot. direita em G + recolor):
```
         N⚫
        /  \\
    P🔴   G🔴
                 \\
                 U⚫
```

O mesmo raciocínio aplica-se para RL (espelhando as direções e rotações).

### Remoção — Caso típico: caso do "double-black" (exemplo resumido)
A remoção pode introduzir um `double-black` (quando um nó preto é removido ou um substituto preto é movido). O reparo possui vários sub-casos (irmão vermelho, irmão preto com filhos pretos, irmão preto com um filho vermelho, ...). Abaixo um exemplo comum quando o irmão é preto e possui um filho vermelho: rotaciona-se e recolora-se para redistribuir o preto.

Antes (remoção gerou double-black em `X`):
```
            P⚫
         /   \\
     X(DB)  S⚫
                 /  \\
            SR🔴  SN⚫
```

Depois (rotação e recolor — exemplo para o filho direito vermelho):
```
            P⚫
         /   \\
     S⚫    
    /  \\
SR🔴  P⚫(com X removido)
     
```

Observação: a correção da remoção envolve até várias iterações subindo a árvore; por isso a lógica é mais extensa que a de inserção. Consulte Cormen (CLRS) ou Sedgewick para o detalhamento completo dos sub-casos.

---

### Referências para os casos
- Para descrição formal e provas: `Cormen et al., Introduction to Algorithms` (Capítulo 13)
- Para implementação passo-a-passo com pseudocódigo: `Sedgewick & Wayne, Algorithms`.

## Referências

- **Cormen, T. H., et al.** (2009). *Introduction to Algorithms* (3rd ed.). MIT Press. Capítulo 13: Red-Black Trees.
- **Sedgewick, R., & Wayne, K.** (2011). *Algorithms* (4th ed.). Addison-Wesley.
- **Bayer, R.** (1972). Symmetric binary B-Trees: Data structure and maintenance algorithms.
