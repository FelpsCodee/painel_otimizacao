from __future__ import annotations

import ctypes
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import psutil
import winreg


def clean_temp_files() -> dict:
    temp_dirs: set[str] = set()
    temp_dirs.add(tempfile.gettempdir())
    env_temp = os.environ.get("TEMP")
    if env_temp:
        temp_dirs.add(env_temp)
    win_temp = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "Temp"
    if win_temp.exists():
        temp_dirs.add(str(win_temp))

    files_deleted = 0
    dirs_deleted = 0
    errors = 0
    space_freed = 0

    for temp_dir in temp_dirs:
        if not os.path.isdir(temp_dir):
            continue
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                try:
                    space_freed += os.path.getsize(file_path)
                    os.remove(file_path)
                    files_deleted += 1
                except OSError:
                    errors += 1
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    os.rmdir(dir_path)
                    dirs_deleted += 1
                except OSError:
                    errors += 1

    return {
        "files_deleted": files_deleted,
        "dirs_deleted": dirs_deleted,
        "errors": errors,
        "space_freed_mb": round(space_freed / (1024 * 1024), 2),
    }


def empty_recycle_bin() -> bool:
    flags = 0x00000001 | 0x00000002 | 0x00000004
    try:
        result = ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, flags)
        return result in (0, -2147418113, 0x80041001, 0x80070002)
    except Exception:
        return False


def flush_dns_cache() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["ipconfig", "/flushdns"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, result.stderr.strip()
    except Exception as e:
        return False, f"Erro ao limpar cache DNS: {e}"


def renew_ip_address() -> tuple[bool, str]:
    try:
        release = subprocess.run(
            ["ipconfig", "/release"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        renew = subprocess.run(
            ["ipconfig", "/renew"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        success = release.returncode == 0 and renew.returncode == 0
        message = f"{release.stdout.strip()}\n{renew.stdout.strip()}"
        if not success:
            message = f"{release.stderr.strip()}\n{renew.stderr.strip()}"
        return success, message
    except Exception as e:
        return False, f"Erro ao renovar endereço IP: {e}"


def ping_test(host: str = "8.8.8.8", count: int = 4) -> dict:
    result_dict: dict = {
        "host": host,
        "packets_sent": count,
        "packets_received": 0,
        "packet_loss_percent": 100.0,
        "avg_latency_ms": 0.0,
    }
    try:
        result = subprocess.run(
            ["ping", "-n", str(count), host],
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout

        loss_match = re.search(r"(\d+)%\s+(?:loss|perda)", output, re.IGNORECASE)
        if loss_match:
            result_dict["packet_loss_percent"] = float(loss_match.group(1))

        received_match = re.search(
            r"(?:Received|Recebidos)\s*=\s*(\d+)", output, re.IGNORECASE
        )
        if received_match:
            result_dict["packets_received"] = int(received_match.group(1))

        avg_match = re.search(
            r"(?:Average|M[ée]dio|M[ée]dia)\s*=\s*(\d+)\s*ms", output, re.IGNORECASE
        )
        if avg_match:
            result_dict["avg_latency_ms"] = float(avg_match.group(1))
    except Exception:
        pass

    return result_dict


def set_power_plan(plan: str) -> bool:
    guids = {
        "ultimate_performance": "e9a42b02-d5df-448d-aa00-03f14749eb61",
        "high_performance": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
        "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
        "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a",
    }
    guid = guids.get(plan)
    if not guid:
        return False
    try:
        if plan == "ultimate_performance":
            subprocess.run(
                ["powercfg", "-duplicatescheme", guid],
                capture_output=True,
                timeout=10,
            )
        result = subprocess.run(
            ["powercfg", "/setactive", guid],
            capture_output=True,
            text=True,
            timeout=15,
        )
        return result.returncode == 0
    except Exception:
        return False


def get_active_power_plan() -> str:
    try:
        result = subprocess.run(
            ["powercfg", "/getactivescheme"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            match = re.search(r"\((.+)\)", result.stdout)
            if match:
                return match.group(1).strip()
        return "Desconhecido"
    except Exception:
        return "Erro ao obter plano de energia"


def disable_visual_effects() -> bool:
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Desktop",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(
            key,
            "UserPreferencesMask",
            0,
            winreg.REG_BINARY,
            b"\x90\x12\x03\x80\x10\x00\x00\x00",
        )
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def enable_visual_effects() -> bool:
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Control Panel\Desktop",
            0,
            winreg.KEY_SET_VALUE,
        )
        winreg.SetValueEx(
            key,
            "UserPreferencesMask",
            0,
            winreg.REG_BINARY,
            b"\x9e\x3e\x07\x80\x12\x00\x00\x00",
        )
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def restart_explorer() -> bool:
    try:
        subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True, timeout=10)
        subprocess.Popen(["explorer.exe"])
        return True
    except Exception:
        return False


def kill_process_by_name(name: str) -> dict:
    killed = 0
    failed = 0
    process_details: list[dict] = []
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == name.lower():
                pid = proc.info["pid"]
                proc_name = proc.info["name"]
                try:
                    proc.kill()
                    killed += 1
                    process_details.append({"pid": pid, "name": proc_name})
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    failed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return {"killed": killed, "failed": failed, "process_details": process_details}


def get_running_processes() -> list[dict]:
    processes: list[dict] = []
    for proc in psutil.process_iter(["pid", "name", "memory_info", "cpu_percent", "status"]):
        try:
            info = proc.info
            memory_mb = round(info["memory_info"].rss / (1024 * 1024), 2) if info["memory_info"] else 0.0
            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory_mb": memory_mb,
                "cpu_percent": info["cpu_percent"] or 0.0,
                "status": info["status"],
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    processes.sort(key=lambda p: p["memory_mb"], reverse=True)
    return processes


def run_sfc_scan() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["sfc", "/scannow"],
            capture_output=True,
            text=True,
            timeout=1800,
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Tempo limite excedido para verificação SFC."
    except Exception as e:
        return False, f"Erro ao executar SFC: {e}"


def run_dism_repair() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["DISM", "/Online", "/Cleanup-Image", "/RestoreHealth"],
            capture_output=True,
            text=True,
            timeout=3600,
        )
        return result.returncode == 0, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Tempo limite excedido para reparo DISM."
    except Exception as e:
        return False, f"Erro ao executar DISM: {e}"


def check_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def optimize_startup() -> list[dict]:
    startup_items: list[dict] = []
    locations = [
        (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM"),
    ]
    for hive, subkey, location_name in locations:
        try:
            key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ)
            i = 0
            while True:
                try:
                    name, value, _ = winreg.EnumValue(key, i)
                    startup_items.append({
                        "name": name,
                        "command": value,
                        "location": location_name,
                    })
                    i += 1
                except OSError:
                    break
            winreg.CloseKey(key)
        except Exception:
            continue
    return startup_items


def disable_startup_item(name: str, location: str = "HKCU") -> bool:
    hive = winreg.HKEY_CURRENT_USER if location == "HKCU" else winreg.HKEY_LOCAL_MACHINE
    subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        key = winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def clean_windows_update_cache() -> tuple[bool, str]:
    try:
        subprocess.run(
            ["net", "stop", "wuauserv"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        download_path = Path(r"C:\Windows\SoftwareDistribution\Download")
        if download_path.exists():
            for item in download_path.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception:
                    continue
        subprocess.run(
            ["net", "start", "wuauserv"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return True, "Cache do Windows Update limpo com sucesso."
    except Exception as e:
        try:
            subprocess.run(
                ["net", "start", "wuauserv"],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except Exception:
            pass
        return False, f"Erro ao limpar cache do Windows Update: {e}"


def get_system_health_score() -> dict:
    details: dict = {}

    system_drive = os.environ.get("SystemDrive", "C:") + "\\"
    try:
        disk = psutil.disk_usage(system_drive)
        disk_free_percent = 100 - disk.percent
    except Exception:
        disk_free_percent = 50.0

    if disk_free_percent >= 30:
        disk_score = 100
    elif disk_free_percent >= 10:
        disk_score = int(50 + (disk_free_percent - 10) * 2.5)
    else:
        disk_score = int(disk_free_percent * 5)
    details["disk"] = {
        "score": disk_score,
        "free_percent": round(disk_free_percent, 1),
    }

    memory = psutil.virtual_memory()
    mem_available_percent = 100 - memory.percent
    if mem_available_percent >= 50:
        mem_score = 100
    elif mem_available_percent >= 20:
        mem_score = int(30 + (mem_available_percent - 20) * (70 / 30))
    else:
        mem_score = int(mem_available_percent * 1.5)
    details["memory"] = {
        "score": mem_score,
        "used_percent": round(memory.percent, 1),
    }

    temp_count = 0
    temp_dir = tempfile.gettempdir()
    try:
        with os.scandir(temp_dir) as entries:
            for _ in entries:
                temp_count += 1
    except Exception:
        pass
    if temp_count <= 50:
        temp_score = 100
    elif temp_count <= 200:
        temp_score = int(100 - ((temp_count - 50) * 0.5))
    else:
        temp_score = max(0, int(25 - ((temp_count - 200) * 0.1)))
    details["temp_files"] = {
        "score": temp_score,
        "count": temp_count,
    }

    startup_items = optimize_startup()
    startup_count = len(startup_items)
    if startup_count <= 5:
        startup_score = 100
    elif startup_count <= 15:
        startup_score = int(100 - ((startup_count - 5) * 5))
    else:
        startup_score = max(0, int(50 - ((startup_count - 15) * 3)))
    details["startup"] = {
        "score": startup_score,
        "count": startup_count,
    }

    overall_score = int(
        disk_score * 0.30
        + mem_score * 0.30
        + temp_score * 0.20
        + startup_score * 0.20
    )
    overall_score = max(0, min(100, overall_score))

    return {"score": overall_score, "details": details}
