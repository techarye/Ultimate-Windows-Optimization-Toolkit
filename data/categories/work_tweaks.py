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

def work_tweaks():
    print("Applying Work Tweaks...\n")

    # 1. Set power plan to Balanced
    print("1. Setting power plan to Balanced")
    run_command('powercfg /setactive SCHEME_BALANCED')

    # 2. Disable lock screen timeout
    print("2. Disabling lock screen timeout")
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v ScreenSaveTimeOut /t REG_SZ /d 0 /f')

    # 3. Enable Night Light
    print("3. Enabling Night Light")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\CloudStore\\Store\\Cache\\DefaultAccount" /v Data /t REG_BINARY /d 0300000001000000 /f')

    # 4. Disable Focus Assist notifications
    print("4. Disabling Focus Assist notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings" /v NOC_GLOBAL_SETTING_TOASTS_ENABLED /t REG_DWORD /d 0 /f')

    # 5. Set Taskbar to auto-hide
    print("5. Setting Taskbar to auto-hide")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\StuckRects3" /v Settings /t REG_BINARY /d 2800000003000000000000000000000000000000000000000000000000000000 /f')

    # 6. Disable animations to speed up UI
    print("6. Disabling animations")
    run_command('reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f')

    # 7. Disable Windows Tips
    print("7. Disabling Windows Tips")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')

    # 8. Disable Sticky Keys popup
    print("8. Disabling Sticky Keys popup")
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d 506 /f')

    # 9. Disable Windows Ink Workspace
    print("9. Disabling Windows Ink Workspace")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsInkWorkspace" /v AllowWindowsInkWorkspace /t REG_DWORD /d 0 /f')

    # 10. Disable Cortana SearchBox on Taskbar
    print("10. Disabling Cortana SearchBox")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f')

    # 11. Enable Clipboard History
    print("11. Enabling Clipboard History")
    run_command('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 1 /f')

    # 12. Disable Automatic Restart after updates
    print("12. Disabling Automatic Restart after updates")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f')

    # 13. Disable Windows Notification Center
    print("13. Disabling Windows Notification Center")
    run_command('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableNotificationCenter /t REG_DWORD /d 1 /f')

    # 14. Disable Taskbar Thumbnails preview
    print("14. Disabling Taskbar Thumbnails preview")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ExtendedUIHoverTime /t REG_DWORD /d 9000 /f')

    # 15. Disable Windows Game Bar
    print("15. Disabling Windows Game Bar")
    run_command('reg add "HKCU\\System\\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f')

    # 16. Set Default Save Location to Documents
    print("16. Setting Default Save Location to Documents")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders" /v Personal /t REG_EXPAND_SZ /d "%USERPROFILE%\\Documents" /f')

    # 17. Disable Windows Spotlight on Lock Screen
    print("17. Disabling Windows Spotlight")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v RotatingLockScreenEnabled /t REG_DWORD /d 0 /f')

    # 18. Disable automatic driver updates
    print("18. Disabling automatic driver updates")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DriverSearching" /v SearchOrderConfig /t REG_DWORD /d 0 /f')

    # 19. Disable Windows Store notifications
    print("19. Disabling Windows Store notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f')

    # 20. Disable app suggestions on Start Menu
    print("20. Disabling app suggestions on Start Menu")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v Start_NotifyNewApps /t REG_DWORD /d 0 /f')

    # 21. Disable Windows Defender Offline scan notifications
    print("21. Disabling Windows Defender Offline scan notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows Defender\\Real-Time Protection" /v DisableBehaviorMonitoring /t REG_DWORD /d 1 /f')

    # 22. Disable automatic sync of settings
    print("22. Disabling automatic sync of settings")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\SettingSync\\Groups\\Personalization" /v Enabled /t REG_DWORD /d 0 /f')

    # 23. Disable Windows Error Reporting
    print("23. Disabling Windows Error Reporting")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

    # 24. Disable feedback notifications
    print("24. Disabling feedback notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f')

    # 25. Disable Customer Experience Improvement Program
    print("25. Disabling CEIP")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\SQMClient\\Windows" /v CEIPEnable /t REG_DWORD /d 0 /f')

    # 26. Disable Search Indexing service
    print("26. Disabling Search Indexing")
    disable_service("WSearch")

    # 27. Disable Xbox Game Monitoring Service
    print("27. Disabling Xbox Game Monitoring Service")
    disable_service("XboxGipSvc")

    # 28. Disable Windows Media Player Network Sharing Service
    print("28. Disabling WMP Network Sharing Service")
    disable_service("WMPNetworkSvc")

    # 29. Disable Sync Host
    print("29. Disabling Sync Host")
    disable_service("SyncHost")

    # 30. Disable Remote Registry Service
    print("30. Disabling Remote Registry Service")
    disable_service("RemoteRegistry")

    print("\nWork tweaks applied. Please restart your computer for all changes to take effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    work_tweaks()
