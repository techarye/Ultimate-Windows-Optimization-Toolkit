import os
import subprocess
import ctypes
import sys

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

def cpu_network_security_tweaks():
    print("Applying CPU, Network, and Security Tweaks...\n")

    # CPU Tweaks

    # 1. Set power plan to High Performance
    print("1. Setting power plan to High Performance")
    run_command('powercfg /setactive SCHEME_MIN')

    # 2. Disable CPU throttling
    print("2. Disabling CPU throttling")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\be337238-0d82-4146-a960-4f3749d470c7" /v Attributes /t REG_DWORD /d 2 /f')

    # 3. Disable C-states (CPU idle states)
    print("3. Disabling CPU C-states")
    # Usually BIOS setting, no direct Windows tweak - skip here

    # 4. Enable Processor Performance Increase Mode
    print("4. Enabling Processor Performance Increase Mode")
    run_command('powercfg /setacvalueindex SCHEME_MIN SUB_PROCESSOR PERFBOOSTMODE 1')
    run_command('powercfg /setactive SCHEME_MIN')

    # Network Tweaks

    # 5. Disable Large Send Offload (LSO) on all network adapters
    print("5. Disabling Large Send Offload (LSO)")
    run_command('powershell -Command "Get-NetAdapter | ForEach-Object { Disable-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Large Send Offload (IPv4)\' -NoRestart }"')
    run_command('powershell -Command "Get-NetAdapter | ForEach-Object { Disable-NetAdapterAdvancedProperty -Name $_.Name -DisplayName \'Large Send Offload (IPv6)\' -NoRestart }"')

    # 6. Enable TCP Auto-Tuning
    print("6. Enabling TCP Auto-Tuning")
    run_command('netsh interface tcp set global autotuninglevel=normal')

    # 7. Enable TCP Chimney Offload
    print("7. Enabling TCP Chimney Offload")
    run_command('netsh int tcp set global chimney=enabled')

    # 8. Enable Receive Side Scaling (RSS)
    print("8. Enabling Receive Side Scaling")
    run_command('netsh int tcp set global rss=enabled')

    # 9. Enable Dead Gateway Detection
    print("9. Enabling Dead Gateway Detection")
    run_command('netsh int tcp set global deadgwdetect=enabled')

    # 10. Disable SMBv1 for security
    print("10. Disabling SMBv1 for security")
    run_command('dism /online /norestart /disable-feature /featurename:SMB1Protocol')

    # 11. Enable Windows Defender real-time protection
    print("11. Enabling Windows Defender real-time protection")
    run_command('powershell Set-MpPreference -DisableRealtimeMonitoring $false')

    # 12. Enable Windows Firewall
    print("12. Enabling Windows Firewall")
    run_command('netsh advfirewall set allprofiles state on')

    # 13. Disable Remote Desktop (security)
    print("13. Disabling Remote Desktop")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 1 /f')

    # 14. Disable Windows Remote Management
    print("14. Disabling Windows Remote Management")
    run_command('sc config WinRM start= disabled')
    run_command('net stop WinRM')

    # 15. Disable unnecessary network protocols (e.g., NetBIOS over TCP/IP)
    print("15. Disabling NetBIOS over TCP/IP")
    run_command('wmic nicconfig where "IPEnabled=true" call SetTcpipNetbios 2')

    # 16. Disable IPv6 if unused
    print("16. Disabling IPv6")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip6\\Parameters" /v DisabledComponents /t REG_DWORD /d 0xFFFFFFFF /f')

    # 17. Enable Windows Defender Exploit Protection
    print("17. Enabling Windows Defender Exploit Protection")
    run_command('powershell Start-Process "ms-settings:windowsdefender-exploitguard"')

    # 18. Enable Credential Guard (requires restart)
    print("18. Enabling Credential Guard")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v EnableVirtualizationBasedSecurity /t REG_DWORD /d 1 /f')
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\DeviceGuard" /v RequirePlatformSecurityFeatures /t REG_DWORD /d 1 /f')

    # 19. Enable Secure Boot (BIOS setting, skip here)

    # 20. Disable guest account
    print("20. Disabling Guest Account")
    run_command('net user guest /active:no')

    # 21. Enable User Account Control (UAC)
    print("21. Enabling User Account Control")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v EnableLUA /t REG_DWORD /d 1 /f')

    # 22. Disable auto-run for removable drives
    print("22. Disabling AutoRun on removable drives")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer" /v NoDriveTypeAutoRun /t REG_DWORD /d 0x000000FF /f')

    # 23. Enable Windows Update service
    print("23. Enabling Windows Update service")
    run_command('sc config wuauserv start= auto')
    run_command('net start wuauserv')

    # 24. Disable unused services (Telnet, FTP, etc.)
    print("24. Disabling Telnet service")
    run_command('sc config TlntSvr start= disabled')
    run_command('net stop TlntSvr')

    # 25. Enable Windows Defender Firewall logging
    print("25. Enabling Windows Firewall logging")
    run_command('netsh advfirewall set currentprofile logging filename %windir%\\system32\\logfiles\\firewall\\pfirewall.log')
    run_command('netsh advfirewall set currentprofile logging maxfilesize 4096')

    # 26. Disable Windows Messenger service
    print("26. Disabling Messenger service")
    run_command('sc config messenger start= disabled')
    run_command('net stop messenger')

    # 27. Enable Network Level Authentication for Remote Desktop
    print("27. Enabling Network Level Authentication")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 1 /f')

    # 28. Set minimum password length to 12 characters
    print("28. Setting minimum password length to 12")
    run_command('net accounts /minpwlen:12')

    # 29. Enable account lockout policy (lock after 5 invalid attempts)
    print("29. Enabling account lockout policy")
    run_command('net accounts /lockoutthreshold:5')
    run_command('net accounts /lockoutduration:30')
    run_command('net accounts /lockoutwindow:30')

    # 30. Disable SMBv1 Client driver (extra safety)
    print("30. Disabling SMBv1 Client driver")
    run_command('sc config mrxsmb10 start= disabled')

    print("\nCPU, Network, and Security tweaks applied. Please restart your computer for full effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    cpu_network_security_tweaks()
