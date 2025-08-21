import os
import sys
import shutil
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import time
import subprocess
import tempfile




def loading():
    for i in tqdm(range(100), desc="Otimizando Sistema"):
        time.sleep(0.001)
        
        
def otimizar_ram():
    loading()
    
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
    
    for item in itens:
        loading()
        try:
             if item.is_file() or item.is_symlink():
                 os.remove(item.path)
                 time.sleep(0.5)
                 arquivos_apagados += 1
                 print(f"  {Fore.CYAN}Arquivo apagado:{Style.RESET_ALL} {item.name}")
             elif item.is_dir():
                shutil.rmtree(item.path)
                time.sleep(0.5)# Apaga a pasta e tudo dentro dela
                pastas_apagadas += 1

        except (PermissionError, OSError) as e:
            
            print(f"  {Fore.RED}Erro ao apagar {item.name}: Em uso ou sem permissão.{Style.RESET_ALL}") # Descomente para ver detalhes dos erros
            erros += 1
            tqdm.write(f"  {Fore.RED}Erro ao apagar:{Style.RESET_ALL} {item.name[:50]}") # tqdm.write para não quebrar a barra
    time.sleep(2)
    print(f"\n{Fore.CYAN} {arquivos_apagados} - Arquivo(s) apagado(s) com sucesso ")
    print(f"\n {Fore.CYAN}{pastas_apagadas} - Pasta(s) apagada(s) com sucesso ")
    print(f"\n {Fore.RED}{erros} Pastas e arquivos que não foram possiveis deletar ")