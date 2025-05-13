# WRITTEN BY GYRO-XD
# FOLLOW MY GITHUB : https://github.com/GYRO-XD
import os
import sys
import time 
from time import sleep
import subprocess
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
import importlib.util

console = Console()

# Core Requirements
REQUIREMENTS = [
    ("cython", "3.0.0"),
    ("rich", "13.0.0"),
    ("pycryptodome", "3.20.0"),
    ("uncompyle6", "3.9.0"),
    ("decompyle3", "3.9.1")
]

TERMUX_PACKAGES = [
    "clang",
    "make",
    "upx"
]

def is_package_installed(package, min_version=None):
    try:
        spec = importlib.util.find_spec(package)
        if spec is None:
            return False
        
        if min_version:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package],
                capture_output=True,
                text=True
            )
            installed_version = None
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    installed_version = line.split(':')[1].strip()
                    break
            
            if installed_version and installed_version < min_version:
                console.print(f"[yellow]⚠ {package} version {installed_version} needs upgrade (required: {min_version})[/]")
                return False
        
        return True
    except Exception:
        return False

def install_missing_packages():
    with Progress() as progress:
        # Python packages
        py_task = progress.add_task("[cyan]Checking Python packages...", total=len(REQUIREMENTS))
        
        to_install = []
        for package, version in REQUIREMENTS:
            if not is_package_installed(package, version):
                to_install.append(f"{package}=={version}")
            progress.advance(py_task)
        
        if to_install:
            progress.print("[yellow]Installing missing Python packages...[/]")
            subprocess.run(
                [sys.executable, "-m", "pip", "install"] + to_install,
                check=True
            )
        
        # Termux packages
        if is_termux():
            tx_task = progress.add_task("[blue]Checking Termux packages...", total=len(TERMUX_PACKAGES))
            
            to_install = []
            for package in TERMUX_PACKAGES:
                result = subprocess.run(
                    ["dpkg", "-s", package],
                    capture_output=True,
                    text=True
                )
                if "Status: install ok installed" not in result.stdout:
                    to_install.append(package)
                progress.advance(tx_task)
            
            if to_install:
                progress.print("[yellow]Installing missing Termux packages...[/]")
                subprocess.run(
                    ["pkg", "install", "-y"] + to_install,
                    check=True
                )

def is_termux():
    return os.path.exists("/data/data/com.termux/files/usr")

def show_installation_report():
    os.system('clear')
    table = Table(title="Installation Report", show_header=True, header_style="bold magenta")
    table.add_column("Package", style="cyan")
    table.add_column("Status", justify="right")
    
    # Python packages
    for package, version in REQUIREMENTS:
        if is_package_installed(package, version):
            table.add_row(package, "[green]✓ Installed[/]")
        else:
            table.add_row(package, "[red]✖ Missing[/]")
    
    # Termux packages
    if is_termux():
        for package in TERMUX_PACKAGES:
            result = subprocess.run(
                ["dpkg", "-s", package],
                capture_output=True,
                text=True
            )
            if "Status: install ok installed" in result.stdout:
                table.add_row(f"Termux/{package}", "[green]✓ Installed[/]")
            else:
                table.add_row(f"Termux/{package}", "[red]✖ Missing[/]")
    
    console.print(table)

if __name__ == "__main__":
    console.print("[bold]🔍 Scanning installed packages...[/]")
    show_installation_report()
    
    if "--auto" in sys.argv:
        install_missing_packages()
        console.print("[bold green]✅ Installation complete![/]")
        time.sleep(1)
        os.system("python ENC-PRO.py")
    else:
        console.print("\nRun with [bold green]python requirements.py --auto[/] to install missing packages")
# WRITTEN BY GYRO-XD
# FOLLOW MY GITHUB : https://github.com/GYRO-XD