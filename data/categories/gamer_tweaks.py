import os
import subprocess
import ctypes
import sys
import winreg

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}\n{e}")

def disable_service(service_name):
    run_command(f"sc config {service_name} start= disabled")
    run_command(f"net stop {service_name}")

def gamer_tweaks():
    print("Applying Gamer Tweaks...\n")

    # 1. Set High Performance Power Plan
    print("1. Setting High Performance Power Plan")
    run_command("powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")

    # 2. Disable Xbox Game Bar
    print("2. Disabling Xbox Game Bar")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\GameDVR" /v DVR_Enabled /t REG_DWORD /d 0 /f')

    # 3. Disable Xbox Services
    print("3. Disabling Xbox services")
    disable_service("XblAuthManager")
    disable_service("XblGameSave")
    disable_service("XboxGipSvc")
    disable_service("XboxNetApiSvc")

    # 4. Disable Fullscreen Optimizations (manual notice)
    print("4. Disabling Fullscreen Optimizations (manual - requires user action)")

    # 5. Disable Game Mode
    print("5. Disabling Game Mode")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 0 /f')

    # 6. Disable Windows Update during gaming hours (disable service example)
    print("6. Disabling Windows Update service")
    disable_service("wuauserv")

    # 7. Disable Background Apps
    print("7. Disabling Background Apps")
    run_command('powershell "Get-AppxPackage | Remove-AppxPackage"')

    # 8. Disable Nagle's Algorithm (improve network latency)
    print("8. Disabling Nagle's Algorithm")
    interfaces_key_path = r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, interfaces_key_path) as interfaces_key:
            for i in range(0, winreg.QueryInfoKey(interfaces_key)[0]):
                subkey_name = winreg.EnumKey(interfaces_key, i)
                subkey_path = f"{interfaces_key_path}\\{subkey_name}"
                try:
                    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_ALL_ACCESS) as subkey:
                        winreg.SetValueEx(subkey, "TcpAckFrequency", 0, winreg.REG_DWORD, 1)
                        winreg.SetValueEx(subkey, "TCPNoDelay", 0, winreg.REG_DWORD, 1)
                except PermissionError:
                    print(f"Permission error setting Nagle's Algorithm on interface {subkey_name}")
    except Exception as e:
        print(f"Error setting Nagle's Algorithm: {e}")

    # 9. Disable Windows Animations for Performance
    print("9. Disabling Windows Animations")
    run_command('reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f')

    # 10. Disable Visual Effects for Best Performance
    print("10. Setting Visual Effects for Best Performance")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f')

    # 11. Disable Windows Tips and Notifications
    print("11. Disabling Windows Tips and Notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f')

    # 12. Disable Windows Defender Real-Time Protection (temporary - risky)
    print("12. Disabling Windows Defender Real-Time Protection (risky!)")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableRealtimeMonitoring /t REG_DWORD /d 1 /f')

    # 13. Set Network Throttling Index to Max
    print("13. Setting Network Throttling Index to Max")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d ffffffff /f')

    # 14. Increase Process Priority for Games (Manual guidance)
    print("14. You can increase process priority manually in Task Manager for best performance.")

    # 15. Disable Background Intelligent Transfer Service (BITS)
    print("15. Disabling BITS Service")
    disable_service("BITS")

    # 16. Enable TCP/IP Auto-Tuning Level (Improves network performance)
    print("16. Enabling TCP/IP Auto-Tuning")
    run_command('netsh interface tcp set global autotuninglevel=normal')

    # 17. Disable Superfetch (SysMain)
    print("17. Disabling SysMain (Superfetch)")
    disable_service("SysMain")

    # 18. Disable Windows Search indexing service
    print("18. Disabling Windows Search indexing")
    disable_service("WSearch")

    # 19. Disable Remote Differential Compression (RDC)
    print("19. Disabling RDC")
    run_command('dism /online /disable-feature /featurename:RemoteDifferentialCompression')

    # 20. Disable Windows Error Reporting
    print("20. Disabling Windows Error Reporting")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

    # 21. Disable OneDrive (if installed)
    print("21. Disabling OneDrive")
    run_command('reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /t REG_DWORD /d 1 /f')
    disable_service("OneSyncSvc")

    # 22. Clear Prefetch Data (improve performance)
    print("22. Clearing Prefetch Data")
    prefetch_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Prefetch')
    try:
        for file in os.listdir(prefetch_path):
            file_path = os.path.join(prefetch_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except Exception as e:
        print(f"Error clearing prefetch: {e}")

    # 23. Enable Large System Cache
    print("23. Enabling Large System Cache")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v LargeSystemCache /t REG_DWORD /d 1 /f')

    # 24. Increase Max User Port (increase network port range)
    print("24. Increasing Max User Port")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v MaxUserPort /t REG_DWORD /d 65534 /f')

    # 25. Disable Windows Notification Center
    print("25. Disabling Action Center")
    run_command('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableNotificationCenter /t REG_DWORD /d 1 /f')

    # 26. Disable Clipboard History
    print("26. Disabling Clipboard History")
    run_command('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 0 /f')

    # 27. Disable Tips on Lock Screen
    print("27. Disabling Tips on Lock Screen")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-338388Enabled /t REG_DWORD /d 0 /f')

    # 28. Disable Windows Spotlight on Lock Screen
    print("28. Disabling Windows Spotlight")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-310093Enabled /t REG_DWORD /d 0 /f')

    # 29. Disable Automatic Driver Updates
    print("29. Disabling Automatic Driver Updates")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DriverSearching" /v SearchOrderConfig /t REG_DWORD /d 0 /f')

    # 30. Set CPU Priority for Games (manual)
    print("30. Set CPU priority for games manually in Task Manager for best performance.")

    print("\nGamer tweaks applied. Please reboot your PC for all changes to take effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    gamer_tweaks()
