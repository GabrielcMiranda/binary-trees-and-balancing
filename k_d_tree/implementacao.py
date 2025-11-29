from k_d_tree import KDTree
import os

def remover_arquivo_se_existir(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)

def caminho_kd_tree(nome):
    pasta = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(pasta, nome)

def inserir_ponto(tree, contador_insercoes):
    print("Inserindo ponto:")
    
    try:
        coordenadas = input(f"\nDigite as {tree.k} coordenadas separadas por espaço: ").strip().split()
        ponto = [float(c) for c in coordenadas]
        
        if len(ponto) != tree.k:
            print(f"Erro: Digite exatamente {tree.k} coordenadas!")
            return contador_insercoes
    except ValueError:
        print("Erro: Digite apenas números válidos!")
        return contador_insercoes
    
    remover_arquivo_se_existir(caminho_kd_tree("estado_atual_antes.png"))
    remover_arquivo_se_existir(caminho_kd_tree("estado_atual_depois.png"))
    tree.print_tree(caminho_kd_tree("estado_atual_antes"), silent=True)
    
    if tree.insert(ponto):
        tree.print_tree(caminho_kd_tree("estado_atual_depois"), silent=True)
        
        print(f"\nPonto {ponto} inserido com sucesso!")
        print(f"Árvore agora tem {tree.size} pontos")
        
        return contador_insercoes + 1
    else:
        print(f"\nO ponto {ponto} já existe na árvore!")
        return contador_insercoes

def remover_ponto(tree, contador_remocoes):
    print("Removendo ponto:")
    
    try:
        coordenadas = input(f"\nDigite as {tree.k} coordenadas separadas por espaço: ").strip().split()
        ponto = [float(c) for c in coordenadas]
        
        if len(ponto) != tree.k:
            print(f"Erro: Digite exatamente {tree.k} coordenadas!")
            return contador_remocoes
    except ValueError:
        print("Erro: Digite apenas números válidos!")
        return contador_remocoes
    
    if not tree.search(ponto):
        print(f"\nPonto {ponto} não encontrado na árvore!")
        return contador_remocoes
    
    remover_arquivo_se_existir(caminho_kd_tree("estado_atual_antes.png"))
    remover_arquivo_se_existir(caminho_kd_tree("estado_atual_depois.png"))
    tree.print_tree(caminho_kd_tree("estado_atual_antes"), silent=True)
    
    if tree.delete(ponto):
        tree.print_tree(caminho_kd_tree("estado_atual_depois"), silent=True)
        
        print(f"\nPonto {ponto} removido com sucesso!")
        print(f"Árvore agora tem {tree.size} pontos")
        
        return contador_remocoes + 1
    else:
        print(f"\nErro ao remover ponto {ponto}!")
        return contador_remocoes

def buscar_ponto(tree):
    print("Buscando ponto:")
    
    try:
        coordenadas = input(f"\nDigite as {tree.k} coordenadas separadas por espaço: ").strip().split()
        ponto = [float(c) for c in coordenadas]
        
        if len(ponto) != tree.k:
            print(f"Erro: Digite exatamente {tree.k} coordenadas!")
            return
    except ValueError:
        print("Erro: Digite apenas números válidos!")
        return
    
    resultado = tree.search(ponto)
    
    print("=====================================")
    if resultado:
        print(f"Ponto encontrado!")
        print(f"\nCoordenadas: {resultado}")
    else:
        print(f"Ponto não encontrado!")
        print(f"\nO ponto {ponto} não existe na árvore.")

def visualizar_arvore(tree):
    if tree.root is None:
        print("\nÁrvore está vazia!")
        return
    
    remover_arquivo_se_existir(caminho_kd_tree("estado_atual.png"))
    tree.print_tree(caminho_kd_tree("estado_atual"), True)
    print("Arquivo para visualizar a árvore gerado em k_d_tree/estado_atual.png!")

def mostrar_info_arvore(tree):
    print("\nInformações da árvore:")
    
    print(f"\nDimensões: {tree.k}")
    print(f"Total de pontos: {tree.size}")
    
    if tree.root:
        print(f"Raiz: {tree.root.point}")
    else:
        print(f"Árvore vazia!")

def exibir_menu(k):
    print("=====================================")
    print(f"k-D TREE ({k}-D) - MENU INTERATIVO")
    print("\n1. Inserir ponto")
    print("2. Remover ponto")
    print("3. Buscar ponto")
    print("4. Informações da árvore")
    print("5. Visualizar árvore (gerar PNG)")
    print("6. Sair")
    print("=====================================")

def main():
    print("!k-D Tree!")
    
    try:
        k = int(input("\nDigite o número de dimensões (k): ").strip())
        if k < 1:
            print("Erro: k deve ser maior que 0!")
            return
    except ValueError:
        print("Erro: Digite um número válido!")
        return
    
    tree = KDTree(k=k)
    contador_insercoes = 1
    contador_remocoes = 1
    
    while True:
        exibir_menu(k)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            contador_insercoes = inserir_ponto(tree, contador_insercoes)
        elif escolha == '2':
            contador_remocoes = remover_ponto(tree, contador_remocoes)
        elif escolha == '3':
            buscar_ponto(tree)
        elif escolha == '4':
            mostrar_info_arvore(tree)
        elif escolha == '5':
            visualizar_arvore(tree)
        elif escolha == '6':
            print("Encerrando...")
            print(f"\nNumero de inserções: {contador_insercoes - 1}")
            print(f"Numero de remoções: {contador_remocoes - 1}")
            break
        else:
            print("\nOpção invalida! Digite um número de 1 a 6.")
        
        input("\nClique em qualquer tecla para continuar")


if __name__ == "__main__":
    main()
