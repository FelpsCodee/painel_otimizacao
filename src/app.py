from __future__ import annotations

import time
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich import box

from src.core.system_info import (
    get_system_summary,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_gpu_info,
    get_network_info,
    get_startup_programs,
)
from src.core.optimizer import (
    check_admin,
    clean_temp_files,
    clean_windows_update_cache,
    disable_startup_item,
    disable_visual_effects,
    empty_recycle_bin,
    enable_visual_effects,
    flush_dns_cache,
    get_active_power_plan,
    get_running_processes,
    get_system_health_score,
    kill_process_by_name,
    optimize_startup,
    ping_test,
    renew_ip_address,
    restart_explorer,
    run_dism_repair,
    run_sfc_scan,
    set_power_plan,
)
from src.core.report import generate_text_report, generate_report_filename
from src.ui.display import (
    clear_screen,
    confirm,
    prompt_choice,
    show_banner,
    show_error,
    show_health_score,
    show_info,
    show_main_menu,
    show_process_table,
    show_success,
    show_system_dashboard,
    show_warning,
)


class PCOptimizerApp:
    def __init__(self) -> None:
        self.running = True
        self.console = Console()

    def run(self) -> None:
        clear_screen()
        while self.running:
            show_banner()
            show_main_menu()
            choice = prompt_choice("Escolha uma opção")
            self._handle_choice(choice)

    def _handle_choice(self, choice: str) -> None:
        handlers = {
            "1": self._show_dashboard,
            "2": self._disk_cleanup,
            "3": self._network_tools,
            "4": self._power_plan,
            "5": self._visual_effects,
            "6": self._process_manager,
            "7": self._startup_manager,
            "8": self._system_repair,
            "9": self._full_report,
            "0": self._exit,
        }
        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except KeyboardInterrupt:
                show_warning("Operação cancelada pelo usuário.")
            except Exception as e:
                show_error(f"Erro inesperado: {e}")
                time.sleep(2)
        else:
            show_error("Opção inválida! Escolha um número do menu.")
            time.sleep(1)
        if self.running:
            clear_screen()

    def _show_dashboard(self) -> None:
        clear_screen()
        show_info("Coletando informações do sistema...")

        system = get_system_summary()
        cpu = get_cpu_info()
        memory = get_memory_info()
        disks = get_disk_info()
        gpus = get_gpu_info()

        show_system_dashboard(system, cpu, memory, disks, gpus)

        health = get_system_health_score()
        show_health_score({
            "pontuacao": health["score"],
            "pontuacao_maxima": 100,
            "detalhes": {
                "Disco": health["details"]["disk"]["score"],
                "Memória": health["details"]["memory"]["score"],
                "Arquivos temporários": health["details"]["temp_files"]["score"],
                "Inicialização": health["details"]["startup"]["score"],
            },
        })

        prompt_choice("Pressione ENTER para voltar")

    def _disk_cleanup(self) -> None:
        while True:
            clear_screen()
            show_banner()
            self.console.print()

            table = Table(
                title="🧹 Limpeza de Disco",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "🗑️  Limpar arquivos temporários")
            table.add_row("2", "♻️  Esvaziar lixeira")
            table.add_row("3", "🔄  Limpar cache do Windows Update")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                show_info("Limpando arquivos temporários...")
                result = clean_temp_files()
                show_success(
                    f"{result['files_deleted']} arquivo(s) e {result['dirs_deleted']} pasta(s) removidos. "
                    f"Espaço liberado: {result['space_freed_mb']} MB. "
                    f"Erros de permissão/bloqueio: {result['errors']}"
                )
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "2":
                show_info("Esvaziando lixeira...")
                if empty_recycle_bin():
                    show_success("Lixeira verificada e limpa com sucesso!")
                else:
                    show_warning("Não foi possível esvaziar a lixeira no momento.")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "3":
                if not check_admin():
                    show_error("Esta operação requer privilégios de administrador.")
                    prompt_choice("Pressione ENTER para continuar")
                    continue
                show_info("Limpando cache do Windows Update...")
                success, message = clean_windows_update_cache()
                if success:
                    show_success(message)
                else:
                    show_error(message)
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "0":
                break

    def _network_tools(self) -> None:
        while True:
            clear_screen()
            show_banner()
            self.console.print()

            table = Table(
                title="🌐 Ferramentas de Rede",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "🔄  Limpar cache DNS")
            table.add_row("2", "🔧  Renovar endereço IP")
            table.add_row("3", "📡  Teste de conectividade (Ping)")
            table.add_row("4", "📊  Interfaces e IPs de rede")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                show_info("Limpando cache DNS...")
                success, message = flush_dns_cache()
                if success:
                    show_success(f"Cache DNS liberado com êxito! {message}")
                else:
                    show_error(message)
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "2":
                show_info("Renovando endereço IP no roteador...")
                success, message = renew_ip_address()
                if success:
                    show_success("Endereço IP renovado com sucesso!")
                else:
                    show_error(f"Erro ao renovar IP: {message}")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "3":
                host = prompt_choice("Host para teste (padrão: 8.8.8.8)") or "8.8.8.8"
                show_info(f"Testando latência com {host}...")
                result = ping_test(host)
                self.console.print()
                self.console.print(f"  Destino: {result['host']}")
                self.console.print(f"  Pacotes enviados: {result['packets_sent']}")
                self.console.print(f"  Pacotes recebidos: {result['packets_received']}")
                self.console.print(f"  Perda de pacotes: {result['packet_loss_percent']}%")
                self.console.print(f"  Latência média: {result['avg_latency_ms']} ms")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "4":
                clear_screen()
                interfaces = get_network_info()
                net_table = Table(
                    title="📊 Interfaces de Rede Detectadas",
                    box=box.ROUNDED,
                    border_style="green",
                )
                net_table.add_column("Interface", style="bold cyan")
                net_table.add_column("IP IPv4", style="green")
                net_table.add_column("Endereço Físico (MAC)", style="yellow")
                for iface in interfaces:
                    if iface["ip_address"]:
                        net_table.add_row(
                            iface["interface_name"],
                            iface["ip_address"],
                            iface["mac_address"],
                        )
                self.console.print(net_table)
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "0":
                break

    def _power_plan(self) -> None:
        while True:
            clear_screen()
            show_banner()
            current = get_active_power_plan()
            show_info(f"Plano de energia ativo no momento: {current}")
            self.console.print()

            table = Table(
                title="⚡ Planos de Energia do Windows",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "🚀  Desempenho Máximo (Ultimate Performance)")
            table.add_row("2", "🔥  Alto Desempenho")
            table.add_row("3", "⚖️  Equilibrado")
            table.add_row("4", "🔋  Economia de Energia")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                if set_power_plan("ultimate_performance"):
                    show_success("Plano de Desempenho Máximo ativado com sucesso!")
                else:
                    show_error("Falha ao ativar o plano de Desempenho Máximo.")
                time.sleep(1.5)

            elif choice == "2":
                if set_power_plan("high_performance"):
                    show_success("Plano de Alto Desempenho ativado!")
                else:
                    show_error("Falha ao alterar para Alto Desempenho.")
                time.sleep(1.5)

            elif choice == "3":
                if set_power_plan("balanced"):
                    show_success("Plano Equilibrado ativado!")
                else:
                    show_error("Falha ao alterar para Equilibrado.")
                time.sleep(1.5)

            elif choice == "4":
                if set_power_plan("power_saver"):
                    show_success("Plano de Economia de Energia ativado!")
                else:
                    show_error("Falha ao alterar para Economia.")
                time.sleep(1.5)

            elif choice == "0":
                break

    def _visual_effects(self) -> None:
        while True:
            clear_screen()
            show_banner()
            self.console.print()

            table = Table(
                title="🎨 Efeitos Visuais e Animações",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "⚡  Desabilitar animações (foco em desempenho e resposta)")
            table.add_row("2", "🎨  Habilitar animações (padrão estético do Windows)")
            table.add_row("3", "🔄  Reiniciar Windows Explorer (aplicar alterações)")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                if disable_visual_effects():
                    show_success("Efeitos visuais desabilitados no registro.")
                    if confirm("Deseja reiniciar o Windows Explorer agora para aplicar?"):
                        restart_explorer()
                        show_success("Windows Explorer reiniciado.")
                else:
                    show_error("Falha ao desabilitar efeitos visuais.")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "2":
                if enable_visual_effects():
                    show_success("Efeitos visuais restaurados no registro.")
                    if confirm("Deseja reiniciar o Windows Explorer agora para aplicar?"):
                        restart_explorer()
                        show_success("Windows Explorer reiniciado.")
                else:
                    show_error("Falha ao habilitar efeitos visuais.")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "3":
                show_info("Reiniciando explorer.exe...")
                restart_explorer()
                show_success("Windows Explorer reiniciado com sucesso.")
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "0":
                break

    def _process_manager(self) -> None:
        while True:
            clear_screen()
            show_banner()
            self.console.print()

            processes = get_running_processes()[:25]
            formatted = []
            for p in processes:
                formatted.append({
                    "pid": p["pid"],
                    "nome": p["name"],
                    "cpu_percent": p["cpu_percent"],
                    "memoria_mb": p["memory_mb"],
                    "status": p["status"],
                })
            show_process_table(formatted)

            self.console.print()
            table = Table(box=box.ROUNDED, border_style="green")
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "🔪  Finalizar um processo por nome")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                name = prompt_choice("Digite o nome do executável (ex: chrome.exe)")
                if name:
                    if confirm(f"Confirma o encerramento de todas as instâncias de '{name}'?"):
                        result = kill_process_by_name(name)
                        show_success(f"{result['killed']} processo(s) finalizado(s).")
                        if result["failed"] > 0:
                            show_warning(f"{result['failed']} processo(s) protegidos pelo sistema.")
                        time.sleep(2)

            elif choice == "0":
                break

    def _startup_manager(self) -> None:
        while True:
            clear_screen()
            show_banner()
            self.console.print()

            items = optimize_startup()
            table = Table(
                title="🚀 Programas de Inicialização com o Windows",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("#", style="bold yellow", justify="center", width=5)
            table.add_column("Nome", style="bold white", min_width=20)
            table.add_column("Caminho do Executável", style="dim")
            table.add_column("Registro", style="cyan", justify="center")

            for idx, item in enumerate(items, 1):
                table.add_row(str(idx), item["name"], item["command"], item["location"])

            self.console.print(table)
            show_info(f"Total de {len(items)} programa(s) configurado(s) para iniciar com o sistema.")
            self.console.print()

            sub_table = Table(box=box.ROUNDED, border_style="green")
            sub_table.add_column("Opção", style="bold yellow", justify="center", width=8)
            sub_table.add_column("Descrição", style="white", min_width=30)
            sub_table.add_row("1", "🗑️  Desabilitar um programa da inicialização")
            sub_table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(sub_table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                try:
                    idx = int(prompt_choice("Digite o número (#) do programa para desabilitar"))
                    if 1 <= idx <= len(items):
                        item = items[idx - 1]
                        if confirm(f"Remover '{item['name']}' da inicialização automática?"):
                            if disable_startup_item(item["name"], item["location"]):
                                show_success(f"'{item['name']}' removido com sucesso!")
                            else:
                                show_error(f"Falha ao remover '{item['name']}' (permissão insuficiente).")
                            time.sleep(1.5)
                    else:
                        show_error("Número de item inexistente.")
                except ValueError:
                    show_error("Entrada inválida. Digite apenas números.")
                time.sleep(1)

            elif choice == "0":
                break

    def _system_repair(self) -> None:
        while True:
            clear_screen()
            show_banner()

            if not check_admin():
                show_warning("As ferramentas de reparo do Windows exigem privilégios de Administrador.")
            self.console.print()

            table = Table(
                title="🔧 Reparo de Integridade do Windows",
                title_style="bold bright_green",
                box=box.ROUNDED,
                border_style="green",
                show_header=True,
                header_style="bold cyan",
            )
            table.add_column("Opção", style="bold yellow", justify="center", width=8)
            table.add_column("Descrição", style="white", min_width=30)
            table.add_row("1", "🔍  Verificação SFC (System File Checker / scannow)")
            table.add_row("2", "🛠️  Reparo DISM (Deployment Image Servicing and Management)")
            table.add_row("0", "↩️  Voltar", style="dim")
            self.console.print(table)

            choice = prompt_choice("Escolha uma opção")

            if choice == "1":
                show_info("Executando sfc /scannow. Isso pode levar alguns minutos...")
                success, output = run_sfc_scan()
                if success:
                    show_success("Verificação SFC concluída!")
                else:
                    show_error("Falha ou aviso na verificação SFC.")
                self.console.print(output[:500] if len(output) > 500 else output)
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "2":
                show_info("Executando DISM RestoreHealth. Aguarde a conclusão...")
                success, output = run_dism_repair()
                if success:
                    show_success("Reparo DISM concluído com sucesso!")
                else:
                    show_error("Falha na execução do DISM.")
                self.console.print(output[:500] if len(output) > 500 else output)
                prompt_choice("Pressione ENTER para continuar")

            elif choice == "0":
                break

    def _full_report(self) -> None:
        clear_screen()
        show_banner()
        show_info("Gerando diagnóstico completo do sistema...")

        report = generate_text_report()
        self.console.print()
        self.console.print(report)

        if confirm("Deseja exportar e salvar este relatório em disco?"):
            reports_dir = Path("reports")
            reports_dir.mkdir(exist_ok=True)
            filename = generate_report_filename()
            filepath = reports_dir / filename
            generate_text_report(str(filepath))
            show_success(f"Relatório exportado com sucesso em: {filepath}")

        prompt_choice("Pressione ENTER para voltar")

    def _exit(self) -> None:
        clear_screen()
        show_banner()
        show_info("Obrigado por usar o PC Optimizer Pro!")
        self.running = False
        time.sleep(1)
