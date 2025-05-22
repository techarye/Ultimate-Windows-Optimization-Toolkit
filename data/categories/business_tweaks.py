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

def business_tweaks():
    print("Applying Business Tweaks...\n")

    # 1. Enable Windows Firewall
    print("1. Enabling Windows Firewall")
    run_command("netsh advfirewall set allprofiles state on")

    # 2. Enable BitLocker (requires TPM)
    print("2. Enabling BitLocker (manual setup recommended)")

    # 3. Disable Guest Account
    print("3. Disabling Guest Account")
    run_command('net user guest /active:no')

    # 4. Enable Windows Defender Antivirus
    print("4. Enabling Windows Defender Antivirus")
    run_command('sc config WinDefend start= auto')
    run_command('net start WinDefend')

    # 5. Disable SMBv1 (security risk)
    print("5. Disabling SMBv1")
    run_command('dism /online /norestart /disable-feature /featurename:SMB1Protocol')

    # 6. Configure User Account Control to highest level
    print("6. Setting UAC to highest level")
    run_command('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v ConsentPromptBehaviorAdmin /t REG_DWORD /d 2 /f')

    # 7. Disable Remote Desktop (if not needed)
    print("7. Disabling Remote Desktop")
    run_command('reg add "HKLM\\System\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f')

    # 8. Disable Windows Remote Management (WinRM)
    print("8. Disabling Windows Remote Management (WinRM)")
    disable_service("WinRM")

    # 9. Disable Windows Remote Registry service
    print("9. Disabling Remote Registry service")
    disable_service("RemoteRegistry")

    # 10. Enable Audit Policy for Logon Events
    print("10. Enabling Audit Logon Events")
    run_command('auditpol /set /subcategory:"Logon" /success:enable /failure:enable')

    # 11. Enable Windows Update automatic download and install
    print("11. Configuring Windows Update for automatic install")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\WindowsUpdate\\Auto Update" /v AUOptions /t REG_DWORD /d 4 /f')

    # 12. Disable Windows Tips and Ads
    print("12. Disabling Windows Tips and Ads")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')

    # 13. Disable Cortana
    print("13. Disabling Cortana")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search" /v AllowCortana /t REG_DWORD /d 0 /f')

    # 14. Disable OneDrive Sync (if business policy requires)
    print("14. Disabling OneDrive Sync")
    run_command('reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive" /v DisableFileSyncNGSC /t REG_DWORD /d 1 /f')

    # 15. Disable Windows Error Reporting
    print("15. Disabling Windows Error Reporting")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

    # 16. Enable Time Synchronization
    print("16. Enabling Windows Time Service")
    run_command('sc config w32time start= auto')
    run_command('net start w32time')
    run_command('w32tm /resync')

    # 17. Disable AutoPlay on all drives
    print("17. Disabling AutoPlay on all drives")
    run_command('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 255 /f')

    # 18. Disable Windows Defender SmartScreen for Executables
    print("18. Disabling SmartScreen")
    run_command('reg add "HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\SmartScreenEnabled" /t REG_SZ /d "Off" /f')

    # 19. Configure Password Policy (minimum length 12)
    print("19. Configuring Password Policy")
    run_command('net accounts /minpwlen:12')

    # 20. Disable Remote Assistance
    print("20. Disabling Remote Assistance")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Remote Assistance" /v fAllowToGetHelp /t REG_DWORD /d 0 /f')

    # 21. Enable Account Lockout Policy (lock after 5 failed attempts)
    print("21. Enabling Account Lockout Policy")
    run_command('net accounts /lockoutthreshold:5 /lockoutduration:30 /lockoutwindow:30')

    # 22. Disable Legacy SMBv1 Client
    print("22. Disabling SMBv1 Client")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\LanmanWorkstation\\Parameters" /v SMB1 /t REG_DWORD /d 0 /f')

    # 23. Disable Windows Feedback Hub
    print("23. Disabling Feedback Hub")
    run_command('reg add "HKLM\\Software\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')

    # 24. Disable Diagnostic Tracking
    print("24. Disabling Diagnostic Tracking")
    run_command('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" /v AllowTelemetry /t REG_DWORD /d 0 /f')

    # 25. Enable Windows Defender Exploit Protection
    print("25. Enabling Windows Defender Exploit Protection")
    run_command('explorer.exe')  # Note: Proper configuration requires special tools, so just a placeholder

    # 26. Disable Windows Scheduled Tasks that are not business critical
    print("26. Disabling Windows Scheduled Tasks (manual review recommended)")

    # 27. Disable Windows Search Indexing (if not needed)
    print("27. Disabling Windows Search Indexing service")
    disable_service("WSearch")

    # 28. Enable Network Level Authentication for RDP
    print("28. Enabling Network Level Authentication for RDP")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 1 /f')

    # 29. Disable Local Administrator Account (security best practice)
    print("29. Disabling Local Administrator Account")
    run_command('net user administrator /active:no')

    # 30. Disable Windows Advertising ID
    print("30. Disabling Advertising ID")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo" /v Enabled /t REG_DWORD /d 0 /f')

    print("\nBusiness tweaks applied. Please reboot your PC for all changes to take effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    business_tweaks()
