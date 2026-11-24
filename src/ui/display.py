from __future__ import annotations

import os

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def show_banner() -> None:
    banner_text = Text()
    banner_text.append("  ____   ____   ___        _   _           _              \n", style="bold green")
    banner_text.append(" |  _ \\ / ___| / _ \\ _ __ | |_(_)_ __ ___ (_)_______ _ __ \n", style="bold green")
    banner_text.append(" | |_) | |    | | | | '_ \\| __| | '_ ` _ \\| |_  / _ \\ '__|\n", style="bold green")
    banner_text.append(" |  __/| |___ | |_| | |_) | |_| | | | | | | |/ /  __/ |   \n", style="bold green")
    banner_text.append(" |_|    \\____| \\___/| .__/ \\__|_|_| |_| |_|_/___\\___|_|   \n", style="bold green")
    banner_text.append("                    |_|                                    \n", style="bold green")
    banner_text.append("          PC Optimizer Pro", style="bold bright_green")
    banner_text.append("  v2.0", style="dim green")
    banner_text.append("  |  ", style="dim white")
    banner_text.append("github.com/FelpsCodee", style="dim cyan")

    panel = Panel(
        Align.center(banner_text),
        border_style="green",
        box=box.DOUBLE_EDGE,
        padding=(1, 2),
    )
    console.print(panel)


def show_main_menu() -> None:
    table = Table(
        title="Menu Principal",
        title_style="bold bright_green",
        box=box.ROUNDED,
        border_style="green",
        show_header=True,
        header_style="bold cyan",
        padding=(0, 2),
    )
    table.add_column("Opção", style="bold yellow", justify="center", width=8)
    table.add_column("Descrição", style="white", min_width=30)

    options = [
        ("1", "📊  Dashboard do Sistema"),
        ("2", "🧹  Limpeza de Disco"),
        ("3", "🌐  Otimizar Rede"),
        ("4", "⚡  Plano de Energia"),
        ("5", "🎨  Efeitos Visuais"),
        ("6", "📋  Gerenciar Processos"),
        ("7", "🚀  Programas de Inicialização"),
        ("8", "🔧  Reparar Sistema"),
        ("9", "📄  Relatório Completo"),
        ("0", "🚪  Sair"),
    ]

    for key, desc in options:
        style = "dim red" if key == "0" else ""
        table.add_row(key, desc, style=style)

    console.print()
    console.print(Align.center(table))
    console.print()


def show_system_dashboard(
    system_info: dict,
    cpu_info: dict,
    memory_info: dict,
    disk_info: list,
    gpu_info: list,
) -> None:
    labels_sys = {
        "os_name": "Sistema Operacional",
        "os_version": "Versão do SO",
        "os_build": "Compilação / Build",
        "architecture": "Arquitetura",
        "hostname": "Nome da Máquina",
        "username": "Usuário Atual",
        "boot_time": "Última Inicialização",
    }
    sys_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    sys_table.add_column("Campo", style="bold cyan", min_width=20)
    sys_table.add_column("Valor", style="white")
    for key, value in system_info.items():
        field_label = labels_sys.get(key, key)
        sys_table.add_row(field_label, str(value))
    sys_panel = Panel(sys_table, title="💻 Sistema", border_style="blue", box=box.ROUNDED)

    labels_cpu = {
        "name": "Processador",
        "physical_cores": "Núcleos Físicos",
        "logical_cores": "Threads / Lógicos",
        "frequency_mhz": "Frequência Atual",
        "usage_percent": "Uso de CPU",
    }
    cpu_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    cpu_table.add_column("Campo", style="bold cyan", min_width=20)
    cpu_table.add_column("Valor", style="white")
    for key, value in cpu_info.items():
        field_label = labels_cpu.get(key, key)
        display_val = f"{value} MHz" if key == "frequency_mhz" else f"{value}%" if key == "usage_percent" else str(value)
        cpu_table.add_row(field_label, display_val)
    cpu_panel = Panel(cpu_table, title="🔲 Processador", border_style="yellow", box=box.ROUNDED)

    labels_mem = {
        "total_gb": "Memória Total",
        "used_gb": "Memória em Uso",
        "available_gb": "Memória Disponível",
        "usage_percent": "Uso de RAM",
    }
    mem_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    mem_table.add_column("Campo", style="bold cyan", min_width=20)
    mem_table.add_column("Valor", style="white")
    for key, value in memory_info.items():
        field_label = labels_mem.get(key, key)
        display_val = f"{value}%" if key == "usage_percent" else f"{value} GB"
        mem_table.add_row(field_label, display_val)
    mem_panel = Panel(mem_table, title="🧠 Memória", border_style="magenta", box=box.ROUNDED)

    disk_table = Table(box=box.SIMPLE, show_header=True, padding=(0, 1))
    disk_table.add_column("Unidade", style="bold white", justify="center")
    disk_table.add_column("Total", style="cyan", justify="right")
    disk_table.add_column("Usado", style="yellow", justify="right")
    disk_table.add_column("Livre", style="green", justify="right")
    disk_table.add_column("Uso %", style="bold", justify="center")
    for disk in disk_info:
        usage_pct = disk.get("usage_percent", disk.get("uso_percentual", 0))
        if usage_pct >= 90:
            pct_style = "bold red"
        elif usage_pct >= 70:
            pct_style = "bold yellow"
        else:
            pct_style = "bold green"

        device = disk.get("device") or disk.get("unidade", "")
        total_val = f"{disk['total_gb']} GB" if "total_gb" in disk else str(disk.get("total", ""))
        used_val = f"{disk['used_gb']} GB" if "used_gb" in disk else str(disk.get("usado", ""))
        free_val = f"{disk['free_gb']} GB" if "free_gb" in disk else str(disk.get("livre", ""))

        disk_table.add_row(
            device,
            total_val,
            used_val,
            free_val,
            Text(f"{usage_pct}%", style=pct_style),
        )
    disk_panel = Panel(disk_table, title="💾 Discos", border_style="cyan", box=box.ROUNDED)

    gpu_table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    gpu_table.add_column("Campo", style="bold cyan", min_width=20)
    gpu_table.add_column("Valor", style="white")
    if gpu_info:
        for idx, gpu in enumerate(gpu_info, 1):
            if len(gpu_info) > 1:
                gpu_table.add_row(f"GPU #{idx}", "")
            gpu_table.add_row("Modelo", str(gpu.get("name", gpu.get("nome", ""))))
            vram = gpu.get("vram_mb", 0)
            if vram:
                gpu_table.add_row("VRAM Estimada", f"{vram} MB")
            driver = gpu.get("driver_version", "")
            if driver:
                gpu_table.add_row("Versão do Driver", str(driver))
    else:
        gpu_table.add_row("Status", "Nenhum adaptador de vídeo identificado")
    gpu_panel = Panel(gpu_table, title="🎮 GPU", border_style="red", box=box.ROUNDED)

    console.print()
    console.print(Panel(
        Columns([sys_panel, cpu_panel], equal=True, expand=True),
        title="📊 Dashboard do Sistema",
        border_style="bright_green",
        box=box.DOUBLE_EDGE,
        subtitle="PC Optimizer Pro",
        subtitle_align="right",
    ))
    console.print(Columns([mem_panel, disk_panel], equal=True, expand=True))
    console.print(gpu_panel)
    console.print()


def show_process_table(processes: list[dict]) -> None:
    table = Table(
        title="📋 Processos em Execução",
        title_style="bold bright_green",
        box=box.ROUNDED,
        border_style="green",
        show_header=True,
        header_style="bold cyan",
        padding=(0, 1),
    )
    table.add_column("PID", style="bold white", justify="right", width=8)
    table.add_column("Nome", style="bold", min_width=25)
    table.add_column("CPU %", justify="right", width=8)
    table.add_column("Memória (MB)", justify="right", width=14)
    table.add_column("Status", justify="center", width=12)

    for proc in processes:
        mem_mb = proc.get("memoria_mb", 0)
        if mem_mb >= 300:
            mem_style = "bold red"
        elif mem_mb >= 100:
            mem_style = "bold yellow"
        else:
            mem_style = "green"

        cpu_val = proc.get("cpu_percent", 0)
        if cpu_val >= 50:
            cpu_style = "bold red"
        elif cpu_val >= 20:
            cpu_style = "yellow"
        else:
            cpu_style = "green"

        status = proc.get("status", "")
        if status == "running":
            status_text = Text("● Ativo", style="green")
        elif status == "sleeping":
            status_text = Text("● Espera", style="yellow")
        else:
            status_text = Text(f"● {status}", style="dim")

        table.add_row(
            str(proc.get("pid", "")),
            proc.get("nome", ""),
            Text(f"{cpu_val:.1f}", style=cpu_style),
            Text(f"{mem_mb:.1f}", style=mem_style),
            status_text,
        )

    console.print()
    console.print(table)
    console.print()


def show_progress(description: str, total: int) -> Progress:
    progress = Progress(
        SpinnerColumn(style="green"),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bold green"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    )
    progress.add_task(description, total=total)
    return progress


def show_health_score(score_data: dict) -> None:
    score = score_data.get("pontuacao", 0)
    max_score = score_data.get("pontuacao_maxima", 100)
    details = score_data.get("detalhes", {})

    if score >= 80:
        color = "green"
        status = "Excelente"
        emoji = "🟢"
    elif score >= 60:
        color = "yellow"
        status = "Bom"
        emoji = "🟡"
    elif score >= 40:
        color = "dark_orange"
        status = "Regular"
        emoji = "🟠"
    else:
        color = "red"
        status = "Crítico"
        emoji = "🔴"

    bar_length = 40
    filled = int((score / max_score) * bar_length)
    empty = bar_length - filled
    bar = Text()
    bar.append("█" * filled, style=f"bold {color}")
    bar.append("░" * empty, style="dim")

    score_text = Text()
    score_text.append(f"\n  {emoji} Saúde Geral do Sistema: ", style="bold white")
    score_text.append(f"{score}", style=f"bold {color}")
    score_text.append(f"/{max_score}", style="dim")
    score_text.append(f"  ({status})\n\n", style=f"bold {color}")
    score_text.append("  ")
    score_text.append_text(bar)
    score_text.append("\n")

    if details:
        score_text.append("\n")
        for category, value in details.items():
            if isinstance(value, (int, float)):
                cat_color = "green" if value >= 80 else "yellow" if value >= 60 else "red"
                score_text.append(f"  {category}: ", style="bold white")
                score_text.append(f"{value} pts\n", style=cat_color)
            else:
                score_text.append(f"  {category}: ", style="bold white")
                score_text.append(f"{value}\n", style="white")

    panel = Panel(
        score_text,
        title="🏥 Diagnóstico de Saúde",
        border_style=color,
        box=box.ROUNDED,
        padding=(0, 1),
    )
    console.print()
    console.print(panel)
    console.print()


def show_success(message: str) -> None:
    console.print(f"  [bold green]✔ {message}[/bold green]")


def show_error(message: str) -> None:
    console.print(f"  [bold red]✖ {message}[/bold red]")


def show_warning(message: str) -> None:
    console.print(f"  [bold yellow]⚠ {message}[/bold yellow]")


def show_info(message: str) -> None:
    console.print(f"  [bold blue]ℹ {message}[/bold blue]")


def prompt_choice(message: str, choices: list[str] | None = None, default: str = "") -> str:
    return Prompt.ask(
        f"[bold green]{message}[/bold green]",
        choices=choices,
        default=default,
        show_default=False,
        console=console,
    )


def confirm(message: str) -> bool:
    return Confirm.ask(f"[bold yellow]{message}[/bold yellow]", console=console)
