import os
from lp_arv_gen_asc import ArvGenAsc, construir_arvore_de_ficheiro

def limpar_ecra():
    # Limpa o terminal para o menu ficar mais legível
    os.system('cls' if os.name == 'nt' else 'clear')

def main() -> None:
    # Definir o caminho do ficheiro (podes ajustar para o teu caminho absoluto se der erro)
    caminho_ficheiro = (r"c:\Users\rober\Desktop\codigovs\aulas\lab\lab-21-05\parentes.txt")
    
    if not os.path.exists(caminho_ficheiro):
        print(f"Erro: O ficheiro '{caminho_ficheiro}' não foi encontrado!")
        print("Por favor, verifica se o ficheiro está na pasta correta.")
        return

    # Carrega a árvore uma única vez ao iniciar
    arvore = construir_arvore_de_ficheiro(caminho_ficheiro)

    while True:
        limpar_ecra()
        print("==================================================")
        print("        SISTEMA DE ÁRVORE GENEALÓGICA             ")
        print("==================================================")
        print(" 1. Mostrar toda a árvore (Travessia Em-Ordem)")
        print(" 2. Pesquisar Pais de uma pessoa")
        print(" 3. Pesquisar Ascendentes por Grau (1=Pais, 2=Avós...)")
        print(" 4. Pesquisar TODOS os ascendentes (Ordem completa)")
        print(" 0. Sair do Programa")
        print("==================================================")
        
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Toda a Árvore (Em-Ordem) ---")
            print(arvore.in_ord_trav())
            input("\nPressione Enter para continuar...")

        elif opcao == "2":
            print("\n--- Pesquisar Pais ---")
            nome = input("Digite o nome da pessoa: ").strip()
            resultado = arvore.obter_pais(nome)
            if resultado:
                print(f"\nMãe: {resultado[0]}")
                print(f"Pai: {resultado[1]}")
            else:
                print("\nPessoa não encontrada ou sem pais registados na árvore.")
            input("\nPressione Enter para continuar...")

        elif opcao == "3":
            print("\n--- Pesquisar por Grau ---")
            nome = input("Digite o nome da pessoa: ").strip()
            try:
                grau = int(input("Digite o grau de parentesco (Ex: 1=Pais, 2=Avós): "))
                resultado = arvore.obter_ascendentes_por_grau(nome, grau)
                if resultado:
                    print(f"\nAscendentes de Grau {grau}: {resultado}")
                else:
                    print(f"\nNenhum ascendente de grau {grau} encontrado para esta pessoa.")
            except ValueError:
                print("\nPor favor, introduza um número inteiro válido para o grau.")
            input("\nPressione Enter para continuar...")

        elif opcao == "4":
            print("\n--- Pesquisar Todos os Ascendentes (Em-Ordem) ---")
            nome = input("Digite o nome da pessoa: ").strip()
            resultado = arvore.obter_todos_ascendentes(nome)
            if resultado:
                print(f"\nAscendentes de {nome} por ordem:")
                for i, asc in enumerate(resultado, 1):
                    print(f"  {i}. {asc}")
            else:
                print("\nPessoa não encontrada ou não tem ascendentes mapeados.")
            input("\nPressione Enter para continuar...")

        elif opcao == "0":
            print("\nA fechar o programa... Até à próxima!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()