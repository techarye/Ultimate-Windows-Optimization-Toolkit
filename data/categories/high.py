import os
import subprocess

def print_animation(message, duration=1.0):
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

def high_performance_tweaks():
    print_animation("Applying High Performance Tweaks")

    # Power plan: High Performance
    print_animation("Setting High Performance Power Plan")
    run_command("powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")

    # Disable more unnecessary services
    print_animation("Disabling background services")
    for svc in [
        "DiagTrack", "MapsBroker", "WMPNetworkSvc", "Fax", "RetailDemo", "RemoteRegistry",
        "WerSvc", "WSearch", "Wecsvc", "WpnService", "WpnUserService", "SysMain", "BITS",
        "XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc", "OneSyncSvc",
        "W32Time", "TabletInputService", "lfsvc", "SharedAccess", "WbioSrvc", "TrkWks"
    ]:
        print(f"  Disabling {svc}...")
        disable_service(svc)

    # Registry tweaks for performance
    print_animation("Applying registry tweaks for speed")
    reg_tweaks = [
        # Disable telemetry
        ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection', 'AllowTelemetry', 'REG_DWORD', '0'),
        # Disable Windows tips, suggestions, and ads
        ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SystemPaneSuggestionsEnabled', 'REG_DWORD', '0'),
        ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-338388Enabled', 'REG_DWORD', '0'),
        ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-310093Enabled', 'REG_DWORD', '0'),
        # Visual effects: Best Performance
        ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects', 'VisualFXSetting', 'REG_DWORD', '2'),
        ('HKCU\\Control Panel\\Desktop\\WindowMetrics', 'MinAnimate', 'REG_SZ', '0'),
        # Faster shutdown
        ('HKLM\\SYSTEM\\CurrentControlSet\\Control', 'WaitToKillServiceTimeout', 'REG_SZ', '2000'),
        ('HKCU\\Control Panel\\Desktop', 'WaitToKillAppTimeout', 'REG_SZ', '1000'),
        ('HKCU\\Control Panel\\Desktop', 'HungAppTimeout', 'REG_SZ', '1000'),
        # Disable Last Access Update
        ('HKLM\\SYSTEM\\CurrentControlSet\\Control\\FileSystem', 'NtfsDisableLastAccessUpdate', 'REG_DWORD', '1'),
        # Disable paging executive
        ('HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management', 'DisablePagingExecutive', 'REG_DWORD', '1'),
        # Large system cache
        ('HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management', 'LargeSystemCache', 'REG_DWORD', '1'),
        # Increase network throughput
        ('HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters', 'Size', 'REG_DWORD', '3'),
    ]
    for key, name, typ, val in reg_tweaks:
        run_command(f'reg add "{key}" /v {name} /t {typ} /d {val} /f')

    # Disable Game Bar and Game Mode
    print_animation("Disabling Xbox Game Bar and Game Mode")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v DVR_Enabled /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 0 /f')

    # Disable OneDrive
    print_animation("Disabling OneDrive")
    run_command('reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /t REG_DWORD /d 1 /f')
    disable_service("OneSyncSvc")

    # Disable Windows Search indexing
    print_animation("Disabling Windows Search Indexing")
    disable_service("WSearch")

    # Optimize SSD
    print_animation("Optimizing SSD settings")
    run_command('fsutil behavior set DisableDeleteNotify 0')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 0 /f')

    # Enable write caching
    print_animation("Enabling write caching on all drives")
    run_command('powershell -Command "Get-WmiObject -Class Win32_DiskDrive | ForEach-Object { $_.EnableWriteCache = $true }"')

    # Auto-update drivers (PowerShell)
    print_animation("Auto-updating all drivers")
    run_command('powershell -Command "Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -AutoReboot"')

    # Install performance software (ad-free)
    print_animation("Installing performance-boosting software")
    for pkg in [
        "OpenShell.OpenShell", "7zip.7zip", "CrystalDewWorld.CrystalDiskInfo"
    ]:
        run_command(f'winget install --id {pkg} -e --silent')

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

    print_animation("High performance tweaks applied! Reboot recommended.")

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
    high_performance_tweaks()