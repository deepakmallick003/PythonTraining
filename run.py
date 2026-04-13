#!/usr/bin/env python3
"""
Main entry point for the Coding Practice UI
"""
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path
import signal

# Add the app directory to the path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / 'app'))

from app import create_app


def _is_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError:
            return False
    return True


def _list_listener_pids(port: int) -> list[int]:
    """Return PIDs listening on the given TCP port."""
    try:
        result = subprocess.run(
            ['lsof', '-n', '-P', '-ti', f'tcp:{port}', '-sTCP:LISTEN'],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return []

    pids = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return pids


def _project_root_for_pid(pid: int) -> str | None:
    try:
        result = subprocess.run(
            ['lsof', '-a', '-p', str(pid), '-d', 'cwd', '-Fn'],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except (FileNotFoundError, subprocess.SubprocessError):
        return None

    for line in result.stdout.splitlines():
        if line.startswith('n'):
            return line[1:]
    return None


def _terminate_stale_project_servers(port: int) -> list[int]:
    """Stop older run.py instances from this same workspace using the target port."""
    killed: list[int] = []
    current_pid = os.getpid()

    for pid in _list_listener_pids(port):
        if pid == current_pid:
            continue

        if _project_root_for_pid(pid) != str(BASE_DIR):
            continue

        try:
            os.kill(pid, signal.SIGTERM)
            killed.append(pid)
        except ProcessLookupError:
            continue

    if not killed:
        return killed

    deadline = time.time() + 3
    while time.time() < deadline:
        remaining = [pid for pid in killed if pid in _list_listener_pids(port)]
        if not remaining:
            return killed
        time.sleep(0.1)

    for pid in list(killed):
        if pid in _list_listener_pids(port):
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass

    return killed


def _open_browser(host: str, port: int) -> None:
    display_host = '127.0.0.1' if host == '0.0.0.0' else host
    url = f'http://{display_host}:{port}'

    try:
        subprocess.Popen([
            'open', '-a', 'Google Chrome', url
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        try:
            webbrowser.open_new_tab(url)
        except Exception:
            print(f'Open this URL manually: {url}')


if __name__ == '__main__':
    app = create_app()
    host = os.getenv('HOST', '127.0.0.1')
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    port = int(os.getenv('PORT', '5000'))

    killed = _terminate_stale_project_servers(port)
    if killed:
        print(f"Replaced older app process(es) on port {port}: {', '.join(str(pid) for pid in killed)}")

    if not _is_port_available(host, port):
        print(
            f"ERROR: Port {port} is already in use by another process.\n"
            f"The app stays fixed on port {port}, so please stop that other service and run again."
        )
        sys.exit(1)

    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        threading.Timer(1.0, _open_browser, args=(host, port)).start()

    app.run(debug=debug, host=host, port=port)
