from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

from src.core.system_info import (
    get_system_summary,
    get_cpu_info,
    get_memory_info,
    get_disk_info,
    get_gpu_info,
    get_network_info,
    get_startup_programs,
)
from src.core.optimizer import get_active_power_plan, get_system_health_score


def generate_report_filename() -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return f"relatorio_sistema_{timestamp}.txt"


def generate_text_report(output_path: str | None = None) -> str:
    separator = "=" * 60
    lines: list[str] = []

    lines.append(separator)
    lines.append("  PC OPTIMIZER PRO - RELATÓRIO DO SISTEMA")
    lines.append(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    lines.append(separator)

    system = get_system_summary()
    lines.append("\n[SISTEMA OPERACIONAL]")
    lines.append(f"  Sistema:       {system['os_name']}")
    lines.append(f"  Versão:        {system['os_version']}")
    lines.append(f"  Build:         {system['os_build']}")
    lines.append(f"  Arquitetura:   {system['architecture']}")
    lines.append(f"  Hostname:      {system['hostname']}")
    lines.append(f"  Usuário:       {system['username']}")
    lines.append(f"  Último boot:   {system['boot_time']}")

    cpu = get_cpu_info()
    lines.append(f"\n[PROCESSADOR]")
    lines.append(f"  Processador:    {cpu['name']}")
    lines.append(f"  Núcleos físicos: {cpu['physical_cores']}")
    lines.append(f"  Núcleos lógicos: {cpu['logical_cores']}")
    lines.append(f"  Frequência:     {cpu['frequency_mhz']} MHz")
    lines.append(f"  Uso atual:      {cpu['usage_percent']}%")

    memory = get_memory_info()
    lines.append(f"\n[MEMÓRIA RAM]")
    lines.append(f"  Total:       {memory['total_gb']} GB")
    lines.append(f"  Em uso:      {memory['used_gb']} GB")
    lines.append(f"  Disponível:  {memory['available_gb']} GB")
    lines.append(f"  Uso:         {memory['usage_percent']}%")

    disks = get_disk_info()
    lines.append(f"\n[ARMAZENAMENTO]")
    for disk in disks:
        lines.append(f"  Unidade: {disk['device']}")
        lines.append(f"    Sistema de arquivos: {disk['filesystem']}")
        lines.append(f"    Total:  {disk['total_gb']} GB")
        lines.append(f"    Usado:  {disk['used_gb']} GB")
        lines.append(f"    Livre:  {disk['free_gb']} GB")
        lines.append(f"    Uso:    {disk['usage_percent']}%")

    gpus = get_gpu_info()
    lines.append(f"\n[GPU]")
    if gpus:
        for gpu in gpus:
            lines.append(f"  Nome:    {gpu['name']}")
            lines.append(f"  VRAM:    {gpu['vram_mb']} MB")
            lines.append(f"  Driver:  {gpu['driver_version']}")
    else:
        lines.append("  Nenhuma GPU detectada via WMI.")

    network = get_network_info()
    lines.append(f"\n[REDE]")
    for iface in network:
        if iface["ip_address"]:
            lines.append(f"  Interface: {iface['interface_name']}")
            lines.append(f"    IP:  {iface['ip_address']}")
            lines.append(f"    MAC: {iface['mac_address']}")

    power_plan = get_active_power_plan()
    lines.append(f"\n[PLANO DE ENERGIA]")
    lines.append(f"  Plano ativo: {power_plan}")

    startup = get_startup_programs()
    lines.append(f"\n[PROGRAMAS DE INICIALIZAÇÃO] ({len(startup)} itens)")
    for item in startup:
        lines.append(f"  [{item['location']}] {item['name']}")
        lines.append(f"    Caminho: {item['path']}")

    health = get_system_health_score()
    lines.append(f"\n[SAÚDE DO SISTEMA]")
    lines.append(f"  Pontuação geral: {health['score']}/100")
    for category, data in health["details"].items():
        lines.append(f"  {category}: {data['score']}/100")

    lines.append(f"\n{separator}")
    lines.append("  Fim do relatório - PC Optimizer Pro v2.0")
    lines.append(separator)

    report_text = "\n".join(lines)

    if output_path:
        reports_dir = Path(output_path).parent
        reports_dir.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)

    return report_text
