import os
import sys
import time
import ctypes
import colorama
from colorama import Fore, Back, Style, init
import shutil
import functions
import subprocess



if not functions.is_admin():
    print("ERRO: Este painel precisa ser executado como Administrador.")
    print("Por favor, abra um novo CMD como Administrador e execute o script novamente.")
    input("\nPressione Enter para sair.")
    sys.exit() # Encerra o programa

init(autoreset=True) 

def mostrar_painel():
    clear_screen()
    logo()
    print("  ----------BEM VINDO AO PAINEL OTIMIZADOR!----------\n")
    print("  Escolha uma das opções de otimização abaixo: \n")
    for nome , valor in opcoes.items():
        print(f"  [{nome}]: {valor}")
    

def clear_screen():
     os.system('cls' if os.name == 'nt' else 'clear')
def logo():
    print(Fore.RED+"""
  ⠤⣤⣤⣤⣄⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣠⣤⠤⠤⠴⠶⠶⠶⠶
⢠⣤⣤⡄⣤⣤⣤⠄⣀⠉⣉⣙⠒⠤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠘⣉⢡⣤⡤⠐⣶⡆⢶⠀⣶⣶⡦
⣄⢻⣿⣧⠻⠇⠋⠀⠋⠀⢘⣿⢳⣦⣌⠳⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠞⣡⣴⣧⠻⣄⢸⣿⣿⡟⢁⡻⣸⣿⡿⠁
⠈⠃⠙⢿⣧⣙⠶⣿⣿⡷⢘⣡⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣷⣝⡳⠶⠶⠾⣛⣵⡿⠋⠀⠀
⠀⠀⠀⠀⠉⠻⣿⣶⠂⠘⠛⠛⠛⢛⡛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠛⠀⠉⠒⠛⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⢸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢻⡁⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            
        by: https://github.com/FelpsCodee
    """)
    
acoes = {
    1: functions.otimizar_ram,
    2: functions.ativar_modo_desempenho,
    3: functions.limpeza_disco,
    10: functions.limpar_pasta_temp,
    11: functions.verificar_plano_energia
    # 3: functions.otimizar_disco,
    # ... etc ...
   }
    
opcoes = {
    1: "Otimização de memória ",
    2: "Ativar Modo Desempenho Máximo ",
    3: "Limpeza de Disco Avançada  ",
    4: "Reparar Conexão de Rede ",
    5: "Otimizar Inicialização do Sistema ",
    6: "Verificar Integridade do Windows ",
    7: "Finalizador de Tarefas por Nome ",
    8: "Limpeza do Cache de Atualizações do Windows ",
    9: "Analisador de Espaço em Disco ",
    10:"Limpar Pasta de Arquivos Temporários",
    11:"Verificar Plano de Energia",
    12:"Sair do Painel."
}

while True:
    mostrar_painel()
    
    try:
        choice = int(input("Digite a opcao de escolha: "))
      
        funcao_a_executar = acoes.get(choice)
        if funcao_a_executar:
        
            funcao_a_executar()
            input(f"\n{Fore.YELLOW}Otimização concluída. Pressione Enter para voltar ao menu...")
            continue
            
        elif choice == 12:
            clear_screen()
            logo()
            print(Fore.YELLOW + "Saindo do painel de otimizacao")
            time.sleep(1)
            clear_screen()
            break 
        
        else:
            print(Fore.RED + Style.BRIGHT + f"Opção '{choice}' inválida ou ainda não implementada!")
            time.sleep(2) 
            continue
    
    except ValueError:
        print(Fore.RED + Style.BRIGHT + "Entrada inválida! Digite apenas números.")
        time.sleep(2) 
        continue