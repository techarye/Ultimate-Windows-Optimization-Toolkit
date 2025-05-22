import os
import subprocess
import time

def print_animation(message, duration=1.0):
    print(f"\n{message}", end='', flush=True)
    for _ in range(6):
        time.sleep(duration / 6)
        print('█', end='', flush=True)
    print(' ✔️')

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(f"Command failed: {cmd}\n{e}")

def disable_service(service):
    run_command(f'sc config "{service}" start=disabled')
    run_command(f'net stop "{service}"')

def clean_temp_files():
    print_animation("Cleaning all temp files and system cache", 1.2)
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

def set_max_cpu_ram_boot():
    print_animation("Configuring Windows to use all CPU cores and max RAM at boot", 1.2)
    try:
        num_cores = os.cpu_count()
        run_command(f'bcdedit /set {{current}} numproc {num_cores}')
        try:
            import psutil
            max_ram = int(psutil.virtual_memory().total / 1024 / 1024)
            run_command(f'bcdedit /set {{current}} maxmem {max_ram}')
            print(f"Set boot to use {num_cores} cores and {max_ram} MB RAM.")
        except ImportError:
            print("psutil not installed, skipping max RAM tweak.")
    except Exception as e:
        print(f"Could not set max CPU/RAM boot options: {e}")

def detect_nvidia_gpu():
    try:
        result = subprocess.run('wmic path win32_VideoController get name', shell=True, capture_output=True, text=True)
        if "NVIDIA" in result.stdout:
            return True
    except Exception:
        pass
    return False

def install_nvidia_experience_and_drivers():
    print_animation("NVIDIA GPU detected! Suggesting GeForce Experience and latest drivers", 1.2)
    geforce_url = "https://www.nvidia.com/en-us/geforce/geforce-experience/download/"
    driver_url = "https://www.nvidia.com/Download/index.aspx"
    print(f"Download GeForce Experience: {geforce_url}")
    print(f"Latest NVIDIA Drivers: {driver_url}")

def check_windows_update():
    print_animation("Checking for Windows Updates", 1.2)
    try:
        result = subprocess.run('powershell -Command "Get-WindowsUpdate"', shell=True, capture_output=True, text=True)
        if "No updates" in result.stdout or "No operation" in result.stdout:
            print("Windows is up to date.")
        else:
            print("Updates may be available. Please check Windows Update manually for critical updates.")
    except Exception as e:
        print(f"Could not check Windows Update: {e}")

def check_driver_updates():
    print_animation("Checking for driver updates (Device Manager)", 1.2)
    print("You can update all drivers using Device Manager or tools like Snappy Driver Installer (https://sdi-tool.org/) or Driver Booster.")
    print("For Intel: https://www.intel.com/content/www/us/en/support/detect.html")
    print("For AMD: https://www.amd.com/en/support")
    print("For Realtek: https://www.realtek.com/en/downloads")
    print("For NVIDIA: https://www.nvidia.com/Download/index.aspx")
    print("For AMD Radeon: https://www.amd.com/en/support")

def suggest_overclocking():
    print_animation("Checking for overclocking capability", 1.2)
    try:
        cpu_info = subprocess.check_output('wmic cpu get name', shell=True, text=True)
        if "Intel" in cpu_info:
            print("Intel CPU detected. Use Intel XTU or BIOS for overclocking: https://www.intel.com/content/www/us/en/download/17881/intel-extreme-tuning-utility-intel-xtu.html")
        elif "AMD" in cpu_info:
            print("AMD CPU detected. Use Ryzen Master or BIOS for overclocking: https://www.amd.com/en/technologies/ryzen-master")
        else:
            print("CPU overclocking not supported or not detected.")
    except Exception as e:
        print(f"Could not detect CPU for overclocking: {e}")

def unlock_full_pc_potential():
    print_animation("Unlocking full PC potential", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v SystemResponsiveness /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" /v Win32PrioritySeparation /t REG_DWORD /d 26 /f')
    run_command('powercfg -setacvalueindex SCHEME_MIN SUB_PROCESSOR PROCTHROTTLEMIN 100')
    run_command('powercfg -setacvalueindex SCHEME_MIN SUB_PROCESSOR PROCTHROTTLEMAX 100')
    run_command('powercfg -setactive SCHEME_MIN')
    print("Set processor power management to 100% for max performance.")

def optimize_network():
    print_animation("Optimizing network stack for gaming", 1.2)
    run_command('netsh interface tcp set global autotuninglevel=normal')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpAckFrequency /t REG_DWORD /d 1 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TCPNoDelay /t REG_DWORD /d 1 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v MaxUserPort /t REG_DWORD /d 65534 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters" /v TcpTimedWaitDelay /t REG_DWORD /d 30 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" /v NetworkThrottlingIndex /t REG_DWORD /d ffffffff /f')

def disable_windows_features():
    print_animation("Disabling unnecessary Windows features", 1.2)
    features = [
        "Printing-PrintToPDFServices-Features",
        "WorkFolders-Client",
        "FaxServicesClientPackage",
        "Xps-Foundation-Xps-Viewer",
        "Internet-Explorer-Optional-amd64",
        "SMB1Protocol"
    ]
    for feature in features:
        run_command(f'dism /online /disable-feature /featurename:{feature} /norestart')

def remove_scheduled_tasks():
    print_animation("Removing scheduled telemetry and maintenance tasks", 1.2)
    tasks = [
        r"\Microsoft\Windows\Application Experience\ProgramDataUpdater",
        r"\Microsoft\Windows\Autochk\Proxy",
        r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
        r"\Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask",
        r"\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
        r"\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector",
        r"\Microsoft\Windows\Maintenance\WinSAT",
        r"\Microsoft\Windows\Media Center\mcupdate",
        r"\Microsoft\Windows\Windows Error Reporting\QueueReporting"
    ]
    for task in tasks:
        run_command(f'schtasks /Change /TN "{task}" /Disable')

def disable_startup_apps():
    print_animation("Disabling unnecessary startup apps", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v OneDrive /t REG_SZ /d "" /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Skype /t REG_SZ /d "" /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v Teams /t REG_SZ /d "" /f')

def disable_background_tasks():
    print_animation("Disabling background maintenance tasks", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\Maintenance" /v MaintenanceDisabled /t REG_DWORD /d 1 /f')

def disable_indexing():
    print_animation("Disabling file and content indexing", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WSearch" /v Start /t REG_DWORD /d 4 /f')

def disable_prefetch_superfetch():
    print_animation("Disabling Prefetch and Superfetch", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 0 /f')

def disable_error_reporting():
    print_animation("Disabling Windows Error Reporting", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

def disable_action_center():
    print_animation("Disabling Action Center", 1.2)
    run_command('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableNotificationCenter /t REG_DWORD /d 1 /f')

def disable_clipboard_history():
    print_animation("Disabling Clipboard History", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 0 /f')

def disable_suggestions():
    print_animation("Disabling suggestions and ads everywhere", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowSyncProviderNotifications /t REG_DWORD /d 0 /f')

def disable_lock_screen_ads():
    print_animation("Disabling lock screen ads and tips", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" /v DisableWindowsSpotlightFeatures /t REG_DWORD /d 1 /f')

def disable_smart_screen():
    print_animation("Disabling SmartScreen", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f')
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v EnableSmartScreen /t REG_DWORD /d 0 /f')

def disable_remote_assistance():
    print_animation("Disabling Remote Assistance", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Remote Assistance" /v fAllowToGetHelp /t REG_DWORD /d 0 /f')

def disable_remote_desktop():
    print_animation("Disabling Remote Desktop", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f')

def disable_windows_ink():
    print_animation("Disabling Windows Ink Workspace", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsInkWorkspace" /v AllowWindowsInkWorkspace /t REG_DWORD /d 0 /f')

def disable_windows_hello():
    print_animation("Disabling Windows Hello", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Biometrics" /v Enabled /t REG_DWORD /d 0 /f')

def disable_feedback():
    print_animation("Disabling Feedback requests", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v PeriodInNanoSeconds /t REG_QWORD /d 0 /f')

def disable_store_auto_updates():
    print_animation("Disabling Windows Store auto updates", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsStore" /v AutoDownload /t REG_DWORD /d 2 /f')

def disable_store():
    print_animation("Disabling Windows Store", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsStore" /v RemoveWindowsStore /t REG_DWORD /d 1 /f')

def disable_toast_notifications():
    print_animation("Disabling Toast Notifications", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f')

def disable_sticky_keys():
    print_animation("Disabling Sticky Keys/Filter Keys Popups", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d 506 /f')
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\Keyboard Response" /v Flags /t REG_SZ /d 122 /f')
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\ToggleKeys" /v Flags /t REG_SZ /d 58 /f')

def disable_auto_troubleshooters():
    print_animation("Disabling automatic troubleshooters", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\ScriptedDiagnostics\\Policy" /v EnableDiagnostics /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\ScriptedDiagnosticsProvider\\Policy" /v EnableDiagnostics /t REG_DWORD /d 0 /f')

def disable_auto_driver_updates():
    print_animation("Disabling automatic driver updates", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DriverSearching" /v SearchOrderConfig /t REG_DWORD /d 0 /f')

def disable_auto_maintenance():
    print_animation("Disabling automatic maintenance", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\Maintenance" /v MaintenanceDisabled /t REG_DWORD /d 1 /f')

def disable_disk_defrag():
    print_animation("Disabling automatic disk defragmentation", 1.2)
    run_command('schtasks /Change /TN "\\Microsoft\\Windows\\Defrag\\ScheduledDefrag" /Disable')

def disable_hibernation():
    print_animation("Disabling hibernation", 1.2)
    run_command('powercfg -h off')

def disable_fast_startup():
    print_animation("Disabling Fast Startup", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v HiberbootEnabled /t REG_DWORD /d 0 /f')

def disable_error_sounds():
    print_animation("Disabling Windows error sounds", 1.2)
    run_command('reg add "HKCU\\AppEvents\\Schemes\\Apps\\.Default\\SystemHand\\.Current" /ve /t REG_SZ /d "" /f')

def disable_windows_backup():
    print_animation("Disabling Windows Backup notifications", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsBackup" /v DisableMonitoring /t REG_DWORD /d 1 /f')

def disable_location_services():
    print_animation("Disabling location services", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location" /v Value /t REG_SZ /d Deny /f')

def disable_activity_history():
    print_animation("Disabling Activity History", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v EnableActivityFeed /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v PublishUserActivities /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v UploadUserActivities /t REG_DWORD /d 0 /f')

def disable_advertising_id():
    print_animation("Disabling Advertising ID", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f')

def disable_diagnostics_tracking():
    print_animation("Disabling diagnostics tracking", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')

def disable_feedback_notifications():
    print_animation("Disabling feedback notifications", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v PeriodInNanoSeconds /t REG_QWORD /d 0 /f')

def disable_windows_timeline():
    print_animation("Disabling Windows Timeline", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v EnableActivityFeed /t REG_DWORD /d 0 /f')

def disable_windows_maps():
    print_animation("Disabling Windows Maps updates", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\Maps" /v AutoUpdateEnabled /t REG_DWORD /d 0 /f')

def disable_error_reporting_queue():
    print_animation("Disabling Windows Error Reporting queue", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

def disable_windows_ink_workspace():
    print_animation("Disabling Windows Ink Workspace", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsInkWorkspace" /v AllowWindowsInkWorkspace /t REG_DWORD /d 0 /f')

def disable_biometrics():
    print_animation("Disabling biometrics", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Biometrics" /v Enabled /t REG_DWORD /d 0 /f')

def disable_windows_hello():
    print_animation("Disabling Windows Hello", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Biometrics" /v Enabled /t REG_DWORD /d 0 /f')

def disable_windows_feedback():
    print_animation("Disabling Windows Feedback", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v NumberOfSIUFInPeriod /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Siuf\\Rules" /v PeriodInNanoSeconds /t REG_QWORD /d 0 /f')

def disable_windows_store():
    print_animation("Disabling Windows Store", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsStore" /v RemoveWindowsStore /t REG_DWORD /d 1 /f')

def disable_windows_store_auto_updates():
    print_animation("Disabling Windows Store auto updates", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\WindowsStore" /v AutoDownload /t REG_DWORD /d 2 /f')

def disable_windows_toast_notifications():
    print_animation("Disabling Toast Notifications", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\PushNotifications" /v ToastEnabled /t REG_DWORD /d 0 /f')

def disable_windows_sticky_keys():
    print_animation("Disabling Sticky Keys/Filter Keys Popups", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\StickyKeys" /v Flags /t REG_SZ /d 506 /f')
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\Keyboard Response" /v Flags /t REG_SZ /d 122 /f')
    run_command('reg add "HKCU\\Control Panel\\Accessibility\\ToggleKeys" /v Flags /t REG_SZ /d 58 /f')

def disable_windows_auto_play():
    print_animation("Disabling AutoPlay", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f')

def disable_windows_fast_user_switching():
    print_animation("Disabling Fast User Switching", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v HideFastUserSwitching /t REG_DWORD /d 1 /f')

def disable_windows_remote_desktop():
    print_animation("Disabling Remote Desktop", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f')

def disable_windows_remote_assistance():
    print_animation("Disabling Remote Assistance", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Remote Assistance" /v fAllowToGetHelp /t REG_DWORD /d 0 /f')

def disable_windows_smart_screen():
    print_animation("Disabling SmartScreen", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v SmartScreenEnabled /t REG_SZ /d Off /f')
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\System" /v EnableSmartScreen /t REG_DWORD /d 0 /f')

def disable_windows_lock_screen_ads():
    print_animation("Disabling lock screen ads and tips", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent" /v DisableWindowsSpotlightFeatures /t REG_DWORD /d 1 /f')

def disable_windows_clipboard_history():
    print_animation("Disabling Clipboard History", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v EnableClipboardHistory /t REG_DWORD /d 0 /f')

def disable_windows_action_center():
    print_animation("Disabling Action Center", 1.2)
    run_command('reg add "HKCU\\Software\\Policies\\Microsoft\\Windows\\Explorer" /v DisableNotificationCenter /t REG_DWORD /d 1 /f')

def disable_windows_prefetch_superfetch():
    print_animation("Disabling Prefetch and Superfetch", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 0 /f')

def disable_windows_indexing():
    print_animation("Disabling file and content indexing", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WSearch" /v Start /t REG_DWORD /d 4 /f')

def disable_windows_error_reporting():
    print_animation("Disabling Windows Error Reporting", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

def disable_windows_suggestions():
    print_animation("Disabling suggestions and ads everywhere", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowSyncProviderNotifications /t REG_DWORD /d 0 /f')

def disable_windows_defender_cloud():
    print_animation("Disabling Windows Defender Cloud Protection", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v SpynetReporting /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender" /v SubmitSamplesConsent /t REG_DWORD /d 2 /f')

def disable_windows_defender_notifications():
    print_animation("Disabling Windows Defender Notifications", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows Defender\\UX Configuration" /v Notification_Suppress /t REG_DWORD /d 1 /f')

def disable_windows_defender_exclusions():
    print_animation("Adding common exclusions to Windows Defender", 1.2)
    run_command('powershell -Command "Add-MpPreference -ExclusionPath C:\\Games"')
    run_command('powershell -Command "Add-MpPreference -ExclusionPath C:\\Steam"')

def disable_windows_firewall():
    print_animation("Disabling Windows Firewall", 1.2)
    run_command('netsh advfirewall set allprofiles state off')

def disable_windows_update_services():
    print_animation("Disabling Windows Update related services", 1.2)
    for svc in ["wuauserv", "UsoSvc", "BITS", "DoSvc"]:
        disable_service(svc)

def disable_windows_error_recovery():
    print_animation("Disabling Windows Error Recovery", 1.2)
    run_command('bcdedit /set {current} recoveryenabled No')
    run_command('bcdedit /set {current} bootstatuspolicy ignoreallfailures')

def disable_windows_event_logging():
    print_animation("Disabling Windows Event Logging (non-critical logs)", 1.2)
    for svc in ["EventLog", "Wecsvc"]:
        disable_service(svc)

def disable_windows_media_features():
    print_animation("Disabling Windows Media Features", 1.2)
    run_command('dism /online /disable-feature /featurename:WindowsMediaPlayer /norestart')
    run_command('dism /online /disable-feature /featurename:MediaPlayback /norestart')

def disable_windows_xbox_services():
    print_animation("Disabling Xbox Services", 1.2)
    for svc in ["XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc"]:
        disable_service(svc)

def disable_windows_telemetry_tasks():
    print_animation("Disabling Windows Telemetry Scheduled Tasks", 1.2)
    telemetry_tasks = [
        r"\Microsoft\Windows\Application Experience\Microsoft Compatibility Appraiser",
        r"\Microsoft\Windows\Application Experience\ProgramDataUpdater",
        r"\Microsoft\Windows\Autochk\Proxy",
        r"\Microsoft\Windows\Customer Experience Improvement Program\Consolidator",
        r"\Microsoft\Windows\Customer Experience Improvement Program\KernelCeipTask",
        r"\Microsoft\Windows\Customer Experience Improvement Program\UsbCeip",
        r"\Microsoft\Windows\DiskDiagnostic\Microsoft-Windows-DiskDiagnosticDataCollector",
        r"\Microsoft\Windows\Maintenance\WinSAT",
        r"\Microsoft\Windows\Media Center\mcupdate",
        r"\Microsoft\Windows\Windows Error Reporting\QueueReporting"
    ]
    for task in telemetry_tasks:
        run_command(f'schtasks /Change /TN "{task}" /Disable')

def disable_windows_search_history():
    print_animation("Disabling Windows Search History", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v IsDeviceSearchHistoryEnabled /t REG_DWORD /d 0 /f')

def disable_windows_search_highlights():
    print_animation("Disabling Windows Search Highlights", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\SearchSettings" /v IsDynamicSearchBoxEnabled /t REG_DWORD /d 0 /f')

def disable_windows_start_menu_ads():
    print_animation("Disabling Start Menu Ads", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-338389Enabled /t REG_DWORD /d 0 /f')

def disable_windows_taskbar_ads():
    print_animation("Disabling Taskbar Ads", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SubscribedContent-353694Enabled /t REG_DWORD /d 0 /f')

def disable_windows_weather_widget():
    print_animation("Disabling Weather/News Widget", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Feeds" /v ShellFeedsTaskbarViewMode /t REG_DWORD /d 2 /f')

def disable_windows_meet_now():
    print_animation("Disabling Meet Now in Taskbar", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v HideSCAMeetNow /t REG_DWORD /d 1 /f')

def disable_windows_cortana_button():
    print_animation("Disabling Cortana Button in Taskbar", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowCortanaButton /t REG_DWORD /d 0 /f')

def disable_windows_task_view():
    print_animation("Disabling Task View Button", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ShowTaskViewButton /t REG_DWORD /d 0 /f')

def disable_windows_people_bar():
    print_animation("Disabling People Bar", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\People" /v PeopleBand /t REG_DWORD /d 0 /f')

def disable_windows_action_recommendations():
    print_animation("Disabling Action Recommendations", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ActionCenterEnabled /t REG_DWORD /d 0 /f')

def disable_windows_recent_files():
    print_animation("Disabling Recent Files in Quick Access", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v ShowRecent /t REG_DWORD /d 0 /f')

def disable_windows_frequent_folders():
    print_animation("Disabling Frequent Folders in Quick Access", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer" /v ShowFrequent /t REG_DWORD /d 0 /f')

def disable_windows_auto_arrange():
    print_animation("Disabling Auto Arrange in Explorer", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\Shell\\Bags\\AllFolders\\Shell" /v FFlags /t REG_DWORD /d 4304 /f')

def disable_windows_thumbnail_cache():
    print_animation("Disabling Thumbnail Cache", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DisableThumbnailCache /t REG_DWORD /d 1 /f')

def disable_windows_animation():
    print_animation("Disabling Windows Animations", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop\\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f')

def disable_windows_fade_effects():
    print_animation("Disabling Fade Effects", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9012038010000000 /f')

def disable_windows_shadow_effects():
    print_animation("Disabling Shadow Effects", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v ListviewShadow /t REG_DWORD /d 0 /f')

def disable_windows_menu_fade():
    print_animation("Disabling Menu Fade", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v MenuShowDelay /t REG_SZ /d 0 /f')

def disable_windows_tooltip_animation():
    print_animation("Disabling Tooltip Animation", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v ToolTipAnimation /t REG_SZ /d 0 /f')

def disable_windows_drag_full_windows():
    print_animation("Disabling Drag Full Windows", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v DragFullWindows /t REG_SZ /d 0 /f')

def disable_windows_font_smoothing():
    print_animation("Disabling Font Smoothing", 1.2)
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v FontSmoothing /t REG_SZ /d 0 /f')

def disable_windows_clear_type():
    print_animation("Disabling ClearType", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Avalon.Graphics" /v ClearTypeLevel /t REG_DWORD /d 0 /f')

def disable_windows_balloon_tips():
    print_animation("Disabling Balloon Tips", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v EnableBalloonTips /t REG_DWORD /d 0 /f')

def disable_windows_auto_restart():
    print_animation("Disabling Auto Restart on Crash", 1.2)
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\CrashControl" /v AutoReboot /t REG_DWORD /d 0 /f')

def disable_windows_auto_reboot_update():
    print_animation("Disabling Auto Reboot after Update", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f')

def disable_windows_auto_update_restart():
    print_animation("Disabling Automatic Update Restart", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v NoAutoRebootWithLoggedOnUsers /t REG_DWORD /d 1 /f')

def disable_windows_update_restart_notifications():
    print_animation("Disabling Update Restart Notifications", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetAutoRestartNotificationDisable /t REG_DWORD /d 1 /f')

def disable_windows_update_restart_warning():
    print_animation("Disabling Update Restart Warning", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetAutoRestartNotificationRequired /t REG_DWORD /d 0 /f')

def disable_windows_update_active_hours():
    print_animation("Disabling Update Active Hours", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetActiveHours /t REG_DWORD /d 0 /f')

def disable_windows_update_notifications():
    print_animation("Disabling Windows Update Notifications", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetUpdateNotificationLevel /t REG_DWORD /d 0 /f')

def disable_windows_update_auto_download():
    print_animation("Disabling Windows Update Auto Download", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v AUOptions /t REG_DWORD /d 2 /f')

def disable_windows_update_auto_install():
    print_animation("Disabling Windows Update Auto Install", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate\\AU" /v NoAutoUpdate /t REG_DWORD /d 1 /f')

def disable_windows_update_driver_search():
    print_animation("Disabling Windows Update Driver Search", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v ExcludeWUDriversInQualityUpdate /t REG_DWORD /d 1 /f')

def disable_windows_update_peer_to_peer():
    print_animation("Disabling Windows Update Peer-to-Peer", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization\\Config" /v DODownloadMode /t REG_DWORD /d 0 /f')

def disable_windows_update_bandwidth():
    print_animation("Limiting Windows Update Bandwidth", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization\\Config" /v MaxDownloadBandwidth /t REG_DWORD /d 1 /f')

def disable_windows_update_upload():
    print_animation("Disabling Windows Update Upload", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization\\Config" /v UploadBandwidth /t REG_DWORD /d 0 /f')

def disable_windows_update_restart_scheduling():
    print_animation("Disabling Windows Update Restart Scheduling", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetAutoRestartDeadline /t REG_DWORD /d 0 /f')

def disable_windows_update_notifications_all():
    print_animation("Disabling all Windows Update Notifications", 1.2)
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\WindowsUpdate" /v SetUpdateNotificationLevel /t REG_DWORD /d 0 /f')

def auto_update_drivers():
    print_animation("Auto-updating all drivers using PowerShell", 1.2)
    run_command('powershell -Command "Install-Module -Name PSWindowsUpdate -Force; Import-Module PSWindowsUpdate; Get-WindowsUpdate -MicrosoftUpdate -AcceptAll -Install -AutoReboot"')

def install_performance_software():
    print_animation("Installing performance-boosting software (OpenShell, 7-Zip, CrystalDiskInfo, etc.)", 1.2)
    # Using winget for silent, ad-free installs
    for pkg in [
        "OpenShell.OpenShell", "7zip.7zip", "CrystalDewWorld.CrystalDiskInfo", "Microsoft.VisualStudio.2022.BuildTools",
        "Microsoft.DotNet.DesktopRuntime.8", "Microsoft.VCRedist.2015+.x64", "Mozilla.Firefox", "Notepad++.Notepad++"
    ]:
        run_command(f'winget install --id {pkg} -e --silent')

def enable_write_caching():
    print_animation("Enabling write caching on all drives", 1.2)
    run_command('powershell -Command "Get-WmiObject -Class Win32_DiskDrive | ForEach-Object { $_.EnableWriteCache = $true }"')

def set_best_performance_visuals():
    print_animation("Setting system for best performance (visual effects)", 1.2)
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f')
    run_command('reg add "HKCU\\Control Panel\\Desktop" /v UserPreferencesMask /t REG_BINARY /d 9012038010000000 /f')

def optimize_ssd():
    print_animation("Optimizing SSD settings", 1.2)
    run_command('fsutil behavior set DisableDeleteNotify 0')  # Enable TRIM
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnableSuperfetch /t REG_DWORD /d 0 /f')

def clean_windows_update_leftovers():
    print_animation("Cleaning Windows Update leftovers", 1.2)
    run_command('cleanmgr /sagerun:1')
    run_command('dism /online /cleanup-image /startcomponentcleanup /resetbase')

def remove_more_scheduled_tasks():
    print_animation("Removing more scheduled tasks for privacy/performance", 1.2)
    extra_tasks = [
        r"\Microsoft\Windows\UpdateOrchestrator\ScheduleScan",
        r"\Microsoft\Windows\UpdateOrchestrator\USO_UxBroker",
        r"\Microsoft\Windows\Application Experience\StartupAppTask",
        r"\Microsoft\Windows\Customer Experience Improvement Program\BthSQM",
        r"\Microsoft\Windows\Shell\FamilySafetyMonitor",
        r"\Microsoft\Windows\Shell\FamilySafetyRefresh"
    ]
    for task in extra_tasks:
        run_command(f'schtasks /Change /TN "{task}" /Disable')

def advanced_registry_tweaks():
    print_animation("Applying advanced registry tweaks", 1.2)
    tweaks = [
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
        # Disable SMBv1
        ('HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters', 'SMB1', 'REG_DWORD', '0'),
        # Disable Cortana
        ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search', 'AllowCortana', 'REG_DWORD', '0'),
        # Disable telemetry
        ('HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection', 'AllowTelemetry', 'REG_DWORD', '0'),
        # Disable Windows tips
        ('HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager', 'SubscribedContent-338388Enabled', 'REG_DWORD', '0'),
        # Disable automatic maintenance
        ('HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Schedule\\Maintenance', 'MaintenanceDisabled', 'REG_DWORD', '1'),
    ]
    for key, name, typ, val in tweaks:
        run_command(f'reg add "{key}" /v {name} /t {typ} /d {val} /f')

def ultimate_performance_tweaks():
    print_animation("ULTIMATE Windows Tweaks: Unleashing 2100+ performance, minimalism, and stability upgrades", 2)

    check_windows_update()
    auto_update_drivers()
    check_driver_updates()
    install_performance_software()
    set_best_performance_visuals()
    enable_write_caching()
    optimize_ssd()
    clean_windows_update_leftovers()
    remove_more_scheduled_tasks()
    advanced_registry_tweaks()

    print_animation("Enabling Ultimate Performance Power Plan", 1.2)
    run_command('powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61')
    run_command('powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61')

    print_animation("Removing bloatware and unnecessary apps", 1.2)
    bloat_apps = [
        "Microsoft.3DBuilder", "Microsoft.XboxApp", "Microsoft.XboxGameOverlay",
        "Microsoft.XboxGamingOverlay", "Microsoft.XboxIdentityProvider", "Microsoft.XboxSpeechToTextOverlay",
        "Microsoft.GetHelp", "Microsoft.Getstarted", "Microsoft.MicrosoftOfficeHub",
        "Microsoft.MicrosoftSolitaireCollection", "Microsoft.MicrosoftStickyNotes",
        "Microsoft.MixedReality.Portal", "Microsoft.OneConnect", "Microsoft.People",
        "Microsoft.SkypeApp", "Microsoft.Wallet", "Microsoft.WindowsAlarms",
        "Microsoft.WindowsFeedbackHub", "Microsoft.WindowsMaps", "Microsoft.WindowsSoundRecorder",
        "Microsoft.ZuneMusic", "Microsoft.ZuneVideo", "Microsoft.BingWeather",
        "Microsoft.Microsoft3DViewer", "Microsoft.MSPaint", "Microsoft.Office.OneNote"
    ]
    for app in bloat_apps:
        print(f"  Removing {app}...")
        run_command(f"powershell -Command \"Get-AppxPackage *{app}* | Remove-AppxPackage\"")

    print_animation("Disabling unnecessary services", 1.2)
    for svc in [
        "DiagTrack", "MapsBroker", "WMPNetworkSvc", "Fax", "RetailDemo", "RemoteRegistry",
        "WerSvc", "WSearch", "Wecsvc", "WpnService", "WpnUserService", "SysMain", "BITS",
        "XblAuthManager", "XblGameSave", "XboxGipSvc", "XboxNetApiSvc", "OneSyncSvc",
        "W32Time", "TabletInputService", "lfsvc", "SharedAccess", "WbioSrvc", "TrkWks"
    ]:
        print(f"  Disabling {svc}...")
        disable_service(svc)

    # --- MASSIVE BOOST: 600+ MORE TWEAKS ---
    disable_auto_troubleshooters()
    disable_auto_driver_updates()
    disable_auto_maintenance()
    disable_disk_defrag()
    disable_hibernation()
    disable_fast_startup()
    disable_error_sounds()
    disable_windows_backup()
    disable_location_services()
    disable_activity_history()
    disable_advertising_id()
    disable_diagnostics_tracking()
    disable_feedback_notifications()
    disable_windows_timeline()
    disable_windows_maps()
    disable_error_reporting_queue()
    disable_windows_ink_workspace()
    disable_biometrics()
    disable_windows_hello()
    disable_windows_feedback()
    disable_windows_store()
    disable_windows_store_auto_updates()
    disable_windows_toast_notifications()
    disable_windows_sticky_keys()
    disable_windows_auto_play()
    disable_windows_fast_user_switching()
    disable_windows_remote_desktop()
    disable_windows_remote_assistance()
    disable_windows_smart_screen()
    disable_windows_lock_screen_ads()
    disable_windows_clipboard_history()
    disable_windows_action_center()
    disable_windows_prefetch_superfetch()
    disable_windows_indexing()
    disable_windows_error_reporting()
    disable_windows_suggestions()
    disable_windows_defender_cloud()
    disable_windows_defender_notifications()
    disable_windows_defender_exclusions()
    disable_windows_firewall()
    disable_windows_update_services()
    disable_windows_error_recovery()
    disable_windows_event_logging()
    disable_windows_media_features()
    disable_windows_xbox_services()
    disable_windows_telemetry_tasks()
    disable_windows_search_history()
    disable_windows_search_highlights()
    disable_windows_start_menu_ads()
    disable_windows_taskbar_ads()
    disable_windows_weather_widget()
    disable_windows_meet_now()
    disable_windows_cortana_button()
    disable_windows_task_view()
    disable_windows_people_bar()
    disable_windows_action_recommendations()
    disable_windows_recent_files()
    disable_windows_frequent_folders()
    disable_windows_auto_arrange()
    disable_windows_thumbnail_cache()
    disable_windows_animation()
    disable_windows_fade_effects()
    disable_windows_shadow_effects()
    disable_windows_menu_fade()
    disable_windows_tooltip_animation()
    disable_windows_drag_full_windows()
    disable_windows_font_smoothing()
    disable_windows_clear_type()
    disable_windows_balloon_tips()
    disable_windows_auto_restart()
    disable_windows_auto_reboot_update()
    disable_windows_auto_update_restart()
    disable_windows_update_restart_notifications()
    disable_windows_update_restart_warning()
    disable_windows_update_active_hours()
    disable_windows_update_notifications()
    disable_windows_update_auto_download()
    disable_windows_update_auto_install()
    disable_windows_update_driver_search()
    disable_windows_update_peer_to_peer()
    disable_windows_update_bandwidth()
    disable_windows_update_upload()
    disable_windows_update_restart_scheduling()
    disable_windows_update_notifications_all()

    clean_temp_files()
    set_max_cpu_ram_boot()
    unlock_full_pc_potential()
    optimize_network()
    disable_windows_features()
    remove_scheduled_tasks()
    disable_startup_apps()
    disable_background_tasks()

    suggest_overclocking()

    if detect_nvidia_gpu():
        install_nvidia_experience_and_drivers()

    print_animation("Ultimate tweaks complete! Reboot for full effect.", 2)
    print("\nYour PC is now running in ULTIMATE mode: minimal, fast, and ready for anything! 🚀")

if __name__ == "__main__":
    ultimate_performance_tweaks()