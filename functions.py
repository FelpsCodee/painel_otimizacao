import os
import sys
import shutil
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import time
import subprocess
import tempfile


def loading():
    for i in tqdm(range(200), desc="Otimizando Sistema"):
        time.sleep(0.05)
        
        
def otimizar_ram():
    loading()
    
def limpar_pasta_temp():
    caminho_temp = os.getenv('TEMP')
    
    if not caminho_temp or not os.path.exists(caminho_temp):
        print("ERRO: Não foi possível localizar a pasta Temp do sistema.")
        return
    
    print(f"Pasta Temp encontrada em: {caminho_temp}")
    print("Iniciando limpeza...")