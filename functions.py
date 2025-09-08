import os
import sys
import shutil
from colorama import Fore, Back, Style, init
from tqdm import tqdm
import time
import subprocess
import tempfile
import psutil
import ctypes
import winshell
import itertools

def is_admin():
    """Verifica se o script está rodando em modo administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def limpar_tela():
     os.system('cls' if os.name == 'nt' else 'clear')

def loading():
    for i in tqdm(range(100), desc="Otimizando Sistema"):
        time.sleep(0.0001)
         
    
    #FUNÇÃO 1   
def efeitos_visuais():
    CODIGO_EFEITOS_VISUAIS = 0x103F
    FLAG_SALVAR_PERFIL = 0x01
    FLAG_AVISAR_SISTEMA = 0x02
    
    
    limpar_tela()
    print(Fore.GREEN +"Iniciando otimização dos efeitos visuais....")
    time.sleep(2)
    
    limpar_tela()
    while True:
        print(Fore.GREEN +"""
              
                                                <---- Escolha uma das opções abaixo ------>
                                                
                                                ==========================================
                                                | [1] - Habilitar animações              |
                                                | [2] - Desabilitar animações            |
                                                | [3] - Voltar                           |
                                                ==========================================   
              
              
              """)
        escolha = None
        
        try:
            escolha = int(input(Fore.CYAN + "Escolha uma opção: "))
            
        except ValueError:
            
            print("Erro: Por favor, digite apenas um número.")
            continue
        
        if escolha == 1:
            
            try:
                ctypes.windll.user32.SystemParametersInfow(CODIGO_EFEITOS_VISUAIS 1, None, FLAG_SALVAR_PERFIL | FLAG_AVISAR_SISTEMA)
                print("animações habilitadas!")
                
            except Exception as e:
                print(f"Houve um erro ao habilitar animações {e}")
                
        elif escolha == 2:
            try:
                ctypes.windll.user32.SystemParametersInfow(CODIGO_EFEITOS_VISUAIS, 0, None, FLAG_SALVAR_PERFIL | FLAG_AVISAR_SISTEMA)
                print("Animações desabilitadas!")
            except Exception as e:
                print(f"Houve um erro ao desabilitar animações {e}")
        
        elif escolha == 3:
            print("Voltando para o menu...")
            time.sleep(0.7)
            break
        
        else:
            print("Digite apenas os números Válidos!")
            continue
                
            
        
    
    
        
        #FUNÇÃO 3
def limpeza_disco():
    limpar_tela()   
    print("Começando a limpeza de Disco Avançada")
    time.sleep(1)
    
    while True:
        limpar_tela()
        print(Fore.GREEN + """       
                                                <---- Escolha uma das opções abaixo ------>
                                                
                                                ==========================================
                                                | [1] - limpar pastas temps              |
                                                | [2] - Esvaziar Lixeira automaticamente |
                                                | [3] - Voltar                           |
                                                ==========================================   
                                                """)
        
        escolha = int(input("Digite sua opção: "))
        
        if escolha == 1:
            limpar_tela()
            print(Fore.MAGENTA +"\n--- Etapa 1: Limpando Arquivos Temporários ---")
            limpar_pasta_temp()
            time.sleep(1)
            input("Aperte Enter para voltar a escolha de Opções: ")
        
        elif escolha == 2:
            
            print(Fore.MAGENTA + "\n------ Etapa 2: Esvaziando lixeira------\n")
            try:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
                print(f"{Fore.GREEN}Limpando a sujeira..{Style.RESET_ALL}")
                time.sleep(1)
                print(f"{Fore.GREEN}juntando o lixo...{Style.RESET_ALL}")
                time.sleep(1)
                print(f"{Fore.GREEN}Jogando o lixo fora....{Style.RESET_ALL}")
                time.sleep(1)
                print(f"{Fore.GREEN}SUCESSO LIXEIRA ESVAZIADA COM SUCESSO.{Style.RESET_ALL}\n")
                input("Aperte Enter para voltar a escolha de Opções: ")
                
            except Exception as e:
                time.sleep(1)
                print(f"{Fore.RED}ERRO ao esvaziar a lixeira: sua lixeira já pode estar vazia. {Style.RESET_ALL}\n")
                print(f"{Fore.YELLOW}Isso pode exigir que o script seja executado como Administrador.{Style.RESET_ALL}\n")
                input("Aperte Enter para voltar a escolha de Opções: ")
        elif escolha == 3:
            print(Fore.CYAN + "\nVoltando...")
            print(f"{Fore.GREEN}\nFim da Limpeza Avançada {Style.RESET_ALL}")
            break
            
        else:
            print("Digite apenas os numeros das opções de escolhas listadas!")
            time.sleep(1)
    
    
    
    #FUNÇÃO 4
    
def conexao_rede():
    
    if os.name != 'nt': 
        print(f"{Fore.RED}ERRO: Esta função só é compatível com o Windows.{Style.RESET_ALL}")
        time.sleep(3)
        return
    
    comando_1 = ["ipconfig /release"]
    comando_2 = ["ipconfig /renew"]
    comando_3 = ["ipconfig", "/flushdns"]
    comando_4 = ["ping", "8.8.8.8"]
    limpar_tela()

    print(" Escolha uma opção\n")
    print(" [1] Renovar o Endereço IP")
    print(" [2] Limpar o Cache DNS ")
    print(" [3] Testar a Conexão\n ")
        
    escolher = int(input("DIGITE AQUI!: "))
        
    if escolher == 1:
        try:
            subprocess.run( comando_1,capture_output=True,text=True, check=True)
            print("você devolveu o seu IP ao roteador!")
            time.sleep(1)
            print("agora ele te dará um IP novo ou o mesmo.")
            subprocess.run(comando_2,capture_output=True,text=True, check=True)
            time.sleep(1)
            print("\nProntinho IP renovado!")
            
        except Exception as e:
            print(f"\nocorreu um erro ao Renovar IP! | ERRO [{e}] ")
            print("Dica: Execute o painel como Administrador.")
    
    elif escolher == 2:
        try:
            print("Limpando seu Cache DNS!")
            subprocess.run(comando_3,capture_output=True,text=True, check=True)
            print("\nCache DNS Limpo!")
            
        except Exception as e:
            print(f"\nHouve um erro ao tentar limpeza do Cache DNS! | ERRO: [{e}]")
            
    elif escolher == 3:
        try:
            print("Testando sua Conexão...")
            subprocess.run(comando_4, capture_output=True,text=True, check=True)
            print("Conexão Testada e sem nenhum problema!!!")
        
        except Exception as e:
            print(f"\nocorreu um erro ao Testar conexão! | ERRO [{e}] ")
            print("Dica: Execute o painel como Administrador.")
    else:
        print(f"\n{Fore.RED}ERRO: Opção inválida. Escolha 1, 2 ou 3.{Style.RESET_ALL}")
        

def obter_memorias_rss(processo):
    
    return processo.info['memory_info'].rss        
        
def exibir_processos():
    
    limite_atencao = 200
    limite_ciritco = 300
    
    
    listas_processos = list(psutil.process_iter(['pid','name', 'memory_info']))
    processos_ordenados = sorted(listas_processos, key=obter_memorias_rss, reverse=False)

    for item in processos_ordenados:
        try:
            memoria_mb = item.info['memory_info'].rss / (1024 * 1024)
            
            if memoria_mb >=limite_ciritco:
                cor_status = Fore.RED 
            elif memoria_mb >=limite_atencao:
               cor_status = Fore.YELLOW 
                
            else:
               cor_status = Fore.GREEN 
            
            print(f"nome: {Fore.GREEN}{item.info['name']:<30}{Style.RESET_ALL}  |  memoria: {cor_status}{memoria_mb:.2f}{Style.RESET_ALL}")
            
        except ValueError as e:
            print(f"Ocorreu um Erro: {e}")
            

    #FUNÇÃO 7  
def finalizar_tarefa():
    limpar_tela()
    processos_apagados = 0
    processos_nao_apagados = 0
    print(Fore.GREEN + "Iniciando Finalizador de Tarefas...")
    time.sleep(1)
    while True:
        escolha = input("\nDeseja visualizar os processos ativos antes de finalizar um? [s/n]: ").lower()
        
        if escolha in ["s", "n"]:
            break   
        
        else:
            print(f"{Fore.RED}Opção inválida. Por favor, digite apenas 's' para sim ou 'n' para não.{Style.RESET_ALL}")
            
        
    if escolha == 's':
            print("\nExibindo processos...")
            exibir_processos()             
                    
            print("\n" + "="*50)


                
    print(f"{Fore.YELLOW +"CUIDADO! - "} {"Não finalize processos que você não conheça"}\n")
    nome_do_processo = input("Digite o nome do processo (com o '.exe' no final) que quer encerrar (ou deixe em branco para cancelar): ")
    
    if not nome_do_processo:
        print("\nOperação cancelada. Voltando ao menu principal.")
        time.sleep(2)
        return
    print("\n" + "="*50)
    
    for processo in psutil.process_iter(['pid', 'name']):
        
        if processo.info['name'].lower() == nome_do_processo.lower():
            try:
                processo.kill()
                print(f"{Fore.GREEN}Processo '{processo.info['name']}' (PID: {processo.info['pid']}) finalizado com sucesso!{Style.RESET_ALL}")
                processos_apagados += 1
            except psutil.Error as e:
                print(f"{Fore.RED}ERRO! Ocorreu um erro ao finalizar o processo '{processo.info['name']}' | {e}{Style.RESET_ALL}")
                processos_nao_apagados += 1
    
    print(f"\n{Fore.GREEN}{processos_apagados} - processo(s) finalizado(s).")
    print(f"{Fore.RED}{processos_nao_apagados} - processo(s) não puderam ser finalizados (protegidos).")
    input("Aprete ENTER para voltar: ")
    

    #FUNÇÃO 8
def limpar_cache_windows():
    print(f"{Fore.GREEN}Iniciando a limpeza de cache e atualizações...")
    time.sleep(1)
    print(is_admin())
    

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
                 time.sleep(0.02)
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

    #FUNÇÃO 11
def verificar_plano_energia():
    limpar_tela() 
        

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
    input(Fore.YELLOW + "\nAperte ENTER para voltar: ")


GUID_ALTO_DESEMPENHO = "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"
GUID_EQUILIBRADO = "381b4222-f694-41f0-9685-ff5bb260df2e"
GUID_ECONOMIA = "a1841308-3541-4fab-bc81-f71556f20b4a"

     
        #FUNÇÃO 2
def ativar_modo_desempenho():

    limpar_tela()
    print("Bem vindo a Alteração de Modo de Energia!")
    time.sleep(1)
    print("\n[1] - Alto Desempenho")
    print("[2] - Equilibrado")
    print("[3] - Economia de Energia")
    print("[4] - voltar para o menu Principal\n")
    print("Para verificar em que plano de energia seu computador está, experimente a opção 11!\n")
    
    choice = int(input("Escolha o modo de energia que vc deseja: "))
    if choice == 1:
        os.system(f"powercfg /setactive {GUID_ALTO_DESEMPENHO}")
        print(Fore.GREEN + "Modo Desempenho Ativado!")
        
    elif choice == 2:
        os.system(f"powercfg /setactive {GUID_EQUILIBRADO}")
        print(Fore.YELLOW +"Modo Equilibrado Ativado!") 
    
    elif choice == 3:
        os.system(f"powercfg /setactive {GUID_ECONOMIA}")
        print(Fore.RED +"Modo economia Ativado!")
    
    elif choice == 4:
        limpar_tela()
        print("")
    else:
        print("Numero Invalido")

      
        

    
