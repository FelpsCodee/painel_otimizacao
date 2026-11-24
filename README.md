# PC Optimizer Pro 🚀

<div align="center">

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-Modular%20MVC-orange)
![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen)

**Uma suíte completa e profissional de diagnóstico, limpeza e otimização para sistemas Windows via terminal moderno.**

[Recursos](#-recursos) • [Arquitetura](#-arquitetura-do-projeto) • [Instalação](#-instalação-e-uso) • [Tecnologias](#-tecnologias-utilizadas) • [Autor](#-autor)

</div>

---

## 📌 Sobre o Projeto

O **PC Optimizer Pro** é uma aplicação desktop CLI desenvolvida em Python voltada para manutenção preventiva, ganho de performance e diagnóstico avançado em sistemas operacionais Windows. 

Reformulado a partir de uma arquitetura modular com separação de responsabilidades (Core Engine, UI Renderer e Controller), o projeto adota tipagem estática moderna, tratamento robusto de exceções e integração direta com APIs nativas do Windows (`ctypes`, `winreg`, `psutil` e subprocessos do sistema).

---

## ✨ Recursos

### 1. 📊 Dashboard do Sistema e Diagnóstico
- Monitoramento em tempo real de hardware e sistema operacional.
- Detecção detalhada de CPU (núcleos físicos, threads, frequência e consumo).
- Análise de memória RAM (total, disponível e percentual em uso).
- Mapeamento de todas as partições de disco ativas com cálculo de espaço livre.
- Detecção de adaptadores gráficos (GPU, VRAM e versão do driver).
- **Cálculo de Health Score (0 a 100)**: algoritmo ponderado avaliando integridade de disco, pressão de memória, volume de arquivos temporários e programas na inicialização.

### 2. 🧹 Limpeza Avançada de Disco
- Varredura e exclusão recursiva de arquivos temporários (`%TEMP%`, `C:\Windows\Temp`).
- Esvaziamento programático da Lixeira do Windows utilizando Win32 API (`SHEmptyRecycleBinW`).
- Limpeza do cache de downloads do Windows Update (`SoftwareDistribution\Download`) com controle de serviço (`wuauserv`).

### 3. 🌐 Otimização e Reparo de Rede
- Liberação e renovação do cache do resolvedor DNS (`ipconfig /flushdns`).
- Liberação e renovação de leases DHCP (`ipconfig /release` e `/renew`).
- Teste de conectividade e cálculo de perda de pacotes / latência média via ICMP Ping.
- Mapeamento de interfaces de rede ativas com seus respectivos endereços IPv4 e MAC.

### 4. ⚡ Gerenciamento de Planos de Energia
- Desbloqueio e ativação do plano **Desempenho Máximo (Ultimate Performance)** via GUID nativo.
- Alternância rápida entre planos: Alto Desempenho, Equilibrado e Economia de Energia.
- Identificação em tempo real do esquema de energia atualmente ativo no Windows.

### 5. 🎨 Efeitos Visuais e Latência
- Modificação direta do registro do Windows (`UserPreferencesMask`) para desativação de animações e transições.
- Reinicialização sob demanda do processo `explorer.exe` para aplicação imediata dos ajustes.

### 6. 📋 Gerenciador de Processos
- Listagem em tempo real dos processos ordenados por consumo de memória RAM.
- Destaque visual por faixas de consumo (verde, amarelo e alerta vermelho).
- Encerramento forçado de árvores de processos por nome de executável com confirmação de segurança.

### 7. 🚀 Gerenciador de Programas de Inicialização
- Leitura automatizada das chaves do Registro do Windows (`Run` em `HKCU` e `HKLM`).
- Identificação de softwares configurados para inicializar automaticamente com o sistema.
- Remoção segura de entradas para acelerar o tempo de boot.

### 8. 🔧 Reparo de Integridade do Sistema
- Execução assistida do **System File Checker** (`sfc /scannow`) para restaurar arquivos corrompidos.
- Execução do **DISM** (`DISM /Online /Cleanup-Image /RestoreHealth`) para recuperação da imagem do Windows.

### 9. 📄 Exportação de Relatórios de Diagnóstico
- Geração de relatório técnico completo em formato `.txt` com data e hora.
- Armazenamento estruturado na pasta `reports/` para auditoria ou suporte técnico.

---

## 🏗️ Arquitetura do Projeto

O projeto foi estruturado seguindo as melhores práticas de engenharia de software:

```
painel_otimizacao/
│
├── main.py                  # Ponto de entrada (Entrypoint com checagem de SO e privilégios)
├── requirements.txt         # Dependências do projeto
├── pyproject.toml           # Metadados do pacote Python
├── setup.bat                # Script de automação: cria venv e instala dependências
├── run.bat                  # Script de execução rápida
├── LICENSE                  # Licença MIT
├── README.md                # Documentação técnica do projeto
│
└── src/
    ├── __init__.py
    ├── app.py               # Controller principal (Orquestração do ciclo de vida da aplicação)
    │
    ├── core/                # Módulo Core (Regras de negócio e integração com SO)
    │   ├── __init__.py
    │   ├── optimizer.py     # Motor de otimização (disco, energia, registro, processos)
    │   ├── system_info.py   # Coleta de métricas e hardware (psutil, winreg, platform)
    │   └── report.py        # Gerador e exportador de relatórios técnicos
    │
    └── ui/                  # Módulo de Interface (Renderização e CLI)
        ├── __init__.py
        └── display.py       # Renderização de tabelas, painéis, menus e estilos com Rich
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**: Linguagem base utilizando type hints, pattern matching e PEP 8.
- **Rich**: Renderização de interface de terminal profissional, tabelas responsivas e painéis coloridos.
- **psutil**: Mapeamento de CPU, memória, partições de disco e processos do sistema.
- **ctypes / Win32 API**: Interação direta com bibliotecas nativas do Windows (`shell32.dll`).
- **winreg**: Leitura e manipulação segura de chaves do Registro do Windows.
- **subprocess**: Execução controlada de utilitários de sistema (`powercfg`, `ipconfig`, `sfc`, `dism`).

---

## 🚀 Instalação e Uso

### Pré-requisitos
- Sistema Operacional: **Windows 10** ou **Windows 11**
- **Python 3.10** ou superior instalado com adição ao `PATH`
- Recomendado: Executar o terminal como **Administrador** para acesso a todos os recursos de sistema.

---

### Método 1: Configuração Automática (Recomendado)

1. Clone o repositório:
   ```cmd
   git clone https://github.com/FelpsCodee/painel_otimizacao.git
   cd painel_otimizacao
   ```

2. Execute o assistente de configuração automática:
   ```cmd
   setup.bat
   ```
   *O script cria automaticamente o ambiente virtual (`venv`) e instala todas as dependências.*

3. Inicie o painel:
   ```cmd
   run.bat
   ```

---

### Método 2: Configuração Manual

1. Crie o ambiente virtual:
   ```cmd
   python -m venv venv
   ```

2. Ative o ambiente virtual:
   ```cmd
   venv\Scripts\activate
   ```

3. Instale as dependências:
   ```cmd
   pip install -r requirements.txt
   ```

4. Execute o programa:
   ```cmd
   python main.py
   ```

---

## 🔒 Permissões e Segurança

Algumas operações (como limpeza de cache do Windows Update, desativação de programas em HKLM e comandos SFC/DISM) exigem permissões elevadas. Caso a aplicação seja executada sem privilégios de Administrador, o sistema emitirá um aviso na inicialização e protegerá as funções sensíveis contra encerramentos inesperados.

---

## 📄 Licença

Este projeto é distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

## 👨‍💻 Autor

Desenvolvido por **Felipe Correia (FelpsCodee)**.

- **GitHub**: [@FelpsCodee](https://github.com/FelpsCodee)
- **Repositório**: [painel_otimizacao](https://github.com/FelpsCodee/painel_otimizacao)
