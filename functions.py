import os
import sys
import shutil
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import time
import subprocess
import tempfile
import psutil


def limpar_tela():
     os.system('cls' if os.name == 'nt' else 'clear')

def loading():
    for i in tqdm(range(100), desc="Otimizando Sistema"):
        time.sleep(0.0001)
        
        
    
    #FUNÇÃO 1   
def otimizar_ram():
    limpar_tela()
    processos_ordenados = sorted(psutil.process_iter(['pid', 'name', 'memory_info']),key=lambda p: p.info['memory_info'].rss, reverse=True)
    
    print("--- Top 5 Consumidores de Memória RAM ---")
    for processo in processos_ordenados[:5]:
        try:
            memoria_usada_mb = processo.info['memory_info'].rss / (1024 * 1024)
          
            if memoria_usada_mb > 1:
             
                print(f"  Nome: {Fore.GREEN}{processo.info['name']:<30}{Style.RESET_ALL} | "
                      f"Memória: {Fore.RED}{memoria_usada_mb:.2f} MB{Style.RESET_ALL}")
        except psutil.Error:
         
            pass

            
def ativar_modo_desempenho():
    GUID_ALTO_DESEMPENHO = "powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    GUID_EQUILIBRADO = "powercfg", "/setactive", "381b4222-f694-41f0-9685-ff5bb260df2e"
    GUID_ECONOMIA = "powercfg", "/setactive", "a1841308-3541-4fab-bc81-f71556f20b4a"
    
    limpar_tela()
    print("Bem vindo a Alteração de Modo de Energia!")
    time.sleep(1)
    choice = int(input("Escolha o modo de energia que vc deseja: "))
    if choice == 1:
        os.system(GUID_ALTO_DESEMPENHO)
        print("Modo Desempenho Ativado!")
        
    elif choice == 2:
        os.system(GUID_EQUILIBRADO)
        print("Modo Equilibrado Ativado!")
    
    elif choice == 3:
        os.system(GUID_ECONOMIA)
        print("Modo economia Ativado!")
        
    else:
        print("Numero Invalido")
    
        
    
        

        
    #FUNÇÃO 11
def verificar_plano_energia():
    limpar_tela() 
        
    GUID_ALTO_DESEMPENHO = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
    GUID_EQUILIBRADO = "381b4222-f694-41f0-9685-ff5bb260df2e"
    GUID_ECONOMIA = "a1841308-3541-4fab-bc81-f71556f20b4a"

    print(f"\n{Style.BRIGHT}Verificando plano de energia ativo...{Style.RESET_ALL}")
    time.sleep(0.5)
    print(f"\n{Style.BRIGHT}Verificando ajustes....{Style.RESET_ALL}")
    time.sleep(1)
    try:
        comando = ["powercfg", "/getactivescheme"]
        
        resultado = subprocess.run(comando, capture_output=True,text=True, check= True)
        
        saida_do_texto = resultado.stdout
        
        if GUID_ALTO_DESEMPENHO in saida_do_texto:
            print(f"Status: {Fore.GREEN}MODO ALTO DESEMPENHO ATIVADO{Style.RESET_ALL}")

        elif GUID_EQUILIBRADO in saida_do_texto:
            print(f"Status: {Fore.YELLOW}Modo Equilibrado ativado.{Style.RESET_ALL}")
            
        elif GUID_ECONOMIA in saida_do_texto:
            print(f"Status: {Fore.YELLOW}Modo Economia ativado.{Style.RESET_ALL}")
            
        else:
            print(f"Status: {Fore.CYAN}Outro plano de energia está ativo.{Style.RESET_ALL}")
    
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
         print(f"{Fore.RED}Não foi possível verificar o plano de energia. Erro: {e}{Style.RESET_ALL}")
         print(f"{Fore.YELLOW}Isso pode acontecer se o script não for executado como Administrador.{Style.RESET_ALL}")

    #FUNÇÃO 10
def limpar_pasta_temp():
    
    arquivos_apagados = 0
    pastas_apagadas = 0
    erros = 0
    
    caminho_temp = tempfile.gettempdir()
    
    try:
        itens = list(os.scandir(caminho_temp))
        
    except FileNotFoundError:
        print(f"{Fore.RED}ERRO! Pasta não encontrada. {Style.RESET_ALL}")
        return
    except PermissionError:
        print(f"{Fore.RED} ERRO! Permissão negada para acessar a pasta temporária.  {Style.RESET_ALL}")
        return

    if not itens:
        print(f"{Fore.GREEN}A pasta temporária já está limpa! Nada a fazer.{Style.RESET_ALL}")
        return
    
    limpar_tela()
    print(f"\n{Fore.GREEN} INICIANDO LIMPEZA DE {len(itens)} ITENS EM '{caminho_temp}'...")
    
    time.sleep(2)
    for item in tqdm(itens, desc="Limpando", ncols=100, unit=" item"):

        try:
             if item.is_file() or item.is_symlink():
                 os.remove(item.path)
                 time.sleep(0.5)
                 arquivos_apagados += 1
                 print(f"  {Fore.CYAN}Arquivo apagado:{Style.RESET_ALL} {item.name}")
             elif item.is_dir():
                shutil.rmtree(item.path)
                pastas_apagadas += 1

        except (PermissionError, OSError) as e:
            
            tqdm.write(f"  {Fore.RED}Erro ao apagar {item.name}: Em uso ou sem permissão.{Style.RESET_ALL}") 
            erros += 1
    print(f"\n{Fore.CYAN} {arquivos_apagados} - Arquivo(s) apagado(s) com sucesso ")
    print(f"\n {Fore.CYAN}{pastas_apagadas} - Pasta(s) apagada(s) com sucesso ")
    print(f"\n {Fore.RED}{erros} Pastas e arquivos que não foram possiveis deletar ")