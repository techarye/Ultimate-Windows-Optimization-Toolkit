import os
import subprocess
import ctypes

def print_animation(message, duration=1.2):
    print(message, end='', flush=True)
    for _ in range(3):
        import time
        time.sleep(duration / 3)
        print('.', end='', flush=True)
    print('')

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(f"Command failed: {cmd}\n{e}")

def disable_service(service):
    run_command(f'sc config "{service}" start=disabled')
    run_command(f'net stop "{service}"')

def medium_performance_tweaks():
    print_animation("Applying Medium Performance Tweaks")

    # Power plan: Balanced (not High Performance, but better than Power Saver)
    print_animation("Setting Balanced Power Plan")
    run_command("powercfg -setactive 381b4222-f694-41f0-9685-ff5bb260df2e")

    # Disable some unnecessary services (not as aggressive as low.py)
    print_animation("Disabling select background services")
    for svc in [
        "DiagTrack", "MapsBroker", "WMPNetworkSvc", "Fax", "RetailDemo", "RemoteRegistry",
        "WerSvc", "WSearch", "Wecsvc", "WpnService", "WpnUserService"
    ]:
        print(f"  Disabling {svc}...")
        disable_service(svc)

    # Disable telemetry (medium level)
    print_animation("Reducing Telemetry")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 1 /f')

    # Disable Windows tips and suggestions
    print_animation("Disabling Windows Tips and Suggestions")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')

    # Disable Game Bar (but keep Game Mode)
    print_animation("Disabling Xbox Game Bar")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v DVR_Enabled /t REG_DWORD /d 0 /f')

    # Visual effects: Let Windows choose (not best performance, not best appearance)
    print_animation("Setting Visual Effects to Let Windows Choose")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 0 /f')

    # Keep Superfetch (SysMain) enabled for SSD/HDD caching
    print_animation("Keeping Superfetch (SysMain) enabled for better app launch times")

    # Clean temp files (safe)
    print_animation("Cleaning temp files")
    temp_dirs = [
        os.environ.get('TEMP', ''),
        os.environ.get('TMP', ''),
        os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
        os.path.expanduser('~\\AppData\\Local\\Temp')
    ]
    deleted = 0
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    fp = os.path.join(temp_dir, f)
                    if os.path.isfile(fp) or os.path.islink(fp):
                        os.remove(fp)
                        deleted += 1
                    elif os.path.isdir(fp):
                        subprocess.run(f'rmdir /s /q "{fp}"', shell=True)
                        deleted += 1
                except Exception:
                    pass
    print(f"Deleted {deleted} temp files/folders.")

    print_animation("Medium performance tweaks applied! Reboot recommended.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as admin.")
        return

    print("Starting medium performance tweaks...")
    medium_performance_tweaks()
    print("Tweak applied. Please restart your PC for full effect.")

    # Prompt for restart
    while True:
        restart = input("Do you want to restart now to apply all changes? (yes/no): ").strip().lower()
        if restart == "yes":
            print("Restarting your computer...")
            os.system("shutdown /r /t 3")
            break
        elif restart == "no":
            print("Returning to main script. Please restart later for full effect.")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()