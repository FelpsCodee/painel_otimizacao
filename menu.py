import os
import sys
import time
import ctypes
import colorama
from colorama import Fore, Back, Style, init
import shutil
import functions
import subprocess



""" if not functions.is_admin():
    print("ERRO: Este painel precisa ser executado como Administrador.")
    print("Por favor, abra um novo CMD como Administrador e execute o script novamente.")
    input("\nPressione Enter para sair.")
    sys.exit() """ # Encerra o programa

init(autoreset=True) 

def mostrar_painel():
    clear_screen()
    logo()
    print("                            ----------BEM VINDO AO PAINEL DE OTIMIZAÇÃO!----------\n")
    print("                                Escolha uma das opções de otimização abaixo: \n")
    for nome , valor in opcoes.items():
        print(f"                                    [{nome}]: {valor} ")
    

def clear_screen():
     os.system('cls' if os.name == 'nt' else 'clear')
def logo():
    print(Fore.GREEN +"""
          
   ___            _     _               _                 _     _                                                    _ 
  / _ \   _ __   | |_  (_)  _ __ ___   (_)  ____   __ _  | |_  (_)   ___    _ __      _ __     __ _   _ __     ___  | |
 | | | | | '_ \  | __| | | | '_ ` _ \  | | |_  /  / _` | | __| | |  / _ \  | '_ \    | '_ \   / _` | | '_ \   / _ \ | |
 | |_| | | |_) | | |_  | | | | | | | | | |  / /  | (_| | | |_  | | | (_) | | | | |   | |_) | | (_| | | | | | |  __/ | |
  \___/  | .__/   \__| |_| |_| |_| |_| |_| /___|  \__,_|  \__| |_|  \___/  |_| |_|   | .__/   \__,_| |_| |_|  \___| |_|
         |_|                                                                         |_|                               

                                                             ________
                                                            | ______o|
                                            _______________ ||__---_||
                                           |  ___________  || ______ |
                                           | |           | |||______||
                                           | | #         | ||--------|
                                           | |           | ||      O |
                                           | '-----------' ||      | |
                                      .==. |_____________-_||      | |ig 
                                      |::|   __/_______\__  |::::::::|
                                      |''|  ________________'-. _
                                      `""` /:::::::::':::'::\  |_|
                                           ------------------

    
                                       by: https://github.com/FelpsCodee
    """)
    
acoes = {
    2: functions.ativar_modo_desempenho,
    3: functions.limpeza_disco,
    4: functions.conexao_rede,
    7: functions.finalizar_tarefa,
    8: functions.limpar_cache_windows,
    11: functions.verificar_plano_energia
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
    11:"Verificar Plano de Energia",
    12:"Sair do Painel."
}

while True:
    mostrar_painel()
    
    try:
        choice = int(input("\n\nDigite a opcao de escolha: "))
      
        funcao_a_executar = acoes.get(choice)
        if funcao_a_executar:
        
            funcao_a_executar()
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