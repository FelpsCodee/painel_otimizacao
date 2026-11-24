from __future__ import annotations

import json
import os
import platform
import subprocess
import winreg
from datetime import datetime

import psutil


def get_system_summary() -> dict:
    uname = platform.uname()
    boot_timestamp = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_timestamp).strftime("%d/%m/%Y %H:%M:%S")
    return {
        "os_name": uname.system,
        "os_version": uname.version,
        "os_build": uname.release,
        "architecture": platform.machine(),
        "hostname": uname.node,
        "username": os.getlogin(),
        "boot_time": boot_time,
    }


def get_cpu_info() -> dict:
    freq = psutil.cpu_freq()
    return {
        "name": platform.processor(),
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "frequency_mhz": round(freq.current, 2) if freq else 0.0,
        "usage_percent": psutil.cpu_percent(interval=0.2),
    }


def get_memory_info() -> dict:
    mem = psutil.virtual_memory()
    return {
        "total_gb": round(mem.total / (1024 ** 3), 2),
        "used_gb": round(mem.used / (1024 ** 3), 2),
        "available_gb": round(mem.available / (1024 ** 3), 2),
        "usage_percent": mem.percent,
    }


def get_disk_info() -> list[dict]:
    disks = []
    for partition in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        disks.append({
            "device": partition.device,
            "mountpoint": partition.mountpoint,
            "filesystem": partition.fstype,
            "total_gb": round(usage.total / (1024 ** 3), 2),
            "used_gb": round(usage.used / (1024 ** 3), 2),
            "free_gb": round(usage.free / (1024 ** 3), 2),
            "usage_percent": usage.percent,
        })
    return disks


def get_gpu_info() -> list[dict]:
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name,adapterram,driverversion"],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
        if len(lines) >= 2:
            gpus = []
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        adapter_ram = int(parts[0])
                        vram_mb = round(adapter_ram / (1024 ** 2))
                    except (ValueError, IndexError):
                        vram_mb = 0
                    driver_version = parts[1]
                    name = " ".join(parts[2:])
                    gpus.append({
                        "name": name,
                        "vram_mb": vram_mb,
                        "driver_version": driver_version,
                    })
            if gpus:
                return gpus
    except Exception:
        pass

    try:
        ps_cmd = "Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=8,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout.strip())
            if isinstance(data, dict):
                data = [data]
            gpus = []
            for item in data:
                ram = item.get("AdapterRAM") or 0
                gpus.append({
                    "name": item.get("Name", "Adaptador Gráfico"),
                    "vram_mb": round(ram / (1024 ** 2)) if ram else 0,
                    "driver_version": item.get("DriverVersion", ""),
                })
            return gpus
    except Exception:
        pass

    return []


def get_network_info() -> list[dict]:
    interfaces = []
    addrs = psutil.net_if_addrs()
    for interface_name, addr_list in addrs.items():
        ip_address = ""
        mac_address = ""
        for addr in addr_list:
            if addr.family.name == "AF_INET":
                ip_address = addr.address
            elif addr.family.name == "AF_LINK":
                mac_address = addr.address
        interfaces.append({
            "interface_name": interface_name,
            "ip_address": ip_address,
            "mac_address": mac_address,
        })
    return interfaces


def get_top_processes(limit: int = 10) -> list[dict]:
    processes = []
    for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent"]):
        try:
            info = proc.info
            memory_mb = round(info["memory_info"].rss / (1024 ** 2), 2) if info["memory_info"] else 0.0
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory_mb": memory_mb,
                "cpu_percent": info["cpu_percent"] or 0.0,
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    processes.sort(key=lambda p: p["memory_mb"], reverse=True)
    return processes[:limit]


def _read_startup_entries(hive: int, path: str, location: str) -> list[dict]:
    entries = []
    try:
        with winreg.OpenKey(hive, path) as key:
            index = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, index)
                    entries.append({
                        "name": name,
                        "path": value,
                        "location": location,
                    })
                    index += 1
                except OSError:
                    break
    except OSError:
        pass
    return entries


def get_startup_programs() -> list[dict]:
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    programs = []
    programs.extend(_read_startup_entries(winreg.HKEY_CURRENT_USER, reg_path, "HKCU"))
    programs.extend(_read_startup_entries(winreg.HKEY_LOCAL_MACHINE, reg_path, "HKLM"))
    return programs
