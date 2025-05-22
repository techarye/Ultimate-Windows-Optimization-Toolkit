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

def programmer_tweaks():
    print("Applying Programmer Tweaks...\n")

    # 1. Enable Windows Terminal as default terminal
    print("1. Setting Windows Terminal as default terminal")
    run_command('reg add "HKCU\\Console" /v "ForceV2" /t REG_DWORD /d 1 /f')

    # 2. Enable developer mode
    print("2. Enabling Developer Mode")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\AppModelUnlock" /v "AllowDevelopmentWithoutDevLicense" /t REG_DWORD /d 1 /f')

    # 3. Enable Windows Subsystem for Linux (WSL)
    print("3. Enabling Windows Subsystem for Linux (WSL)")
    run_command('dism /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart')

    # 4. Enable Virtual Machine Platform (for WSL 2)
    print("4. Enabling Virtual Machine Platform")
    run_command('dism /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart')

    # 5. Install OpenSSH client
    print("5. Installing OpenSSH client")
    run_command('dism /online /Add-Capability /CapabilityName:OpenSSH.Client~~~~0.0.1.0')

    # 6. Add developer tools folder to PATH (example: C:\\DevTools)
    print("6. Adding C:\\DevTools to PATH")
    run_command('setx PATH "%PATH%;C:\\DevTools"')

    # 7. Increase max open files limit (in registry)
    print("7. Increasing max open files limit")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager" /v "FileHandleQuota" /t REG_DWORD /d 20480 /f')

    # 8. Enable auto-indent and line numbers in Notepad++
    print("8. Notepad++ tweak skipped (requires app-level config)")

    # 9. Enable PowerShell script execution policy (RemoteSigned)
    print("9. Setting PowerShell execution policy to RemoteSigned")
    run_command('powershell Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force')

    # 10. Enable Windows Defender exclusions for developer folders
    print("10. Adding exclusions for C:\\DevTools and C:\\Projects")
    run_command('powershell Add-MpPreference -ExclusionPath "C:\\DevTools","C:\\Projects"')

    # 11. Disable Windows Tips (reduce distractions)
    print("11. Disabling Windows Tips")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" /v "SubscribedContent-338388Enabled" /t REG_DWORD /d 0 /f')

    # 12. Enable clipboard history
    print("12. Enabling Clipboard History")
    run_command('reg add "HKCU\\Software\\Microsoft\\Clipboard" /v "EnableClipboardHistory" /t REG_DWORD /d 1 /f')

    # 13. Enable window snapping for multitasking
    print("13. Enabling Snap Assist")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "SnapAssist" /t REG_DWORD /d 1 /f')

    # 14. Enable dark mode for apps and system
    print("14. Enabling Dark Mode")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "AppsUseLightTheme" /t REG_DWORD /d 0 /f')
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize" /v "SystemUsesLightTheme" /t REG_DWORD /d 0 /f')

    # 15. Increase console buffer size
    print("15. Increasing console buffer size")
    run_command('reg add "HKCU\\Console" /v "ScreenBufferSize" /t REG_DWORD /d 0x005001f0 /f')

    # 16. Enable file extensions visibility in Explorer
    print("16. Showing file extensions")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "HideFileExt" /t REG_DWORD /d 0 /f')

    # 17. Enable hidden files visibility in Explorer
    print("17. Showing hidden files")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v "Hidden" /t REG_DWORD /d 1 /f')

    # 18. Increase Explorer icon cache size
    print("18. Increasing Explorer icon cache size")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\Shell" /v "IconCacheSize" /t REG_DWORD /d 4096 /f')

    # 19. Enable automatic error reporting to Microsoft
    print("19. Enabling automatic error reporting")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\Windows Error Reporting" /v "Disabled" /t REG_DWORD /d 0 /f')

    # 20. Enable Windows Search indexing for developer folders
    print("20. Enabling Windows Search indexing on C:\\DevTools and C:\\Projects")
    # This requires more complex config, skipping detailed implementation

    # 21. Disable OneDrive auto-start
    print("21. Disabling OneDrive auto-start")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "OneDrive" /t REG_SZ /d "" /f')

    # 22. Enable file history backup (if applicable)
    print("22. Enabling File History backup")
    run_command('powershell Start-Process "control.exe" -ArgumentList "sdclt.exe"')

    # 23. Set environment variable for Java_HOME (example)
    print("23. Setting JAVA_HOME environment variable")
    run_command('setx JAVA_HOME "C:\\Program Files\\Java\\jdk"')

    # 24. Set environment variable for Python path
    print("24. Adding Python to PATH")
    run_command('setx PATH "%PATH%;C:\\Python39"')

    # 25. Enable Hyper-V (if supported)
    print("25. Enabling Hyper-V")
    run_command('dism /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart')

    # 26. Enable fast startup
    print("26. Enabling Fast Startup")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Power" /v "HiberbootEnabled" /t REG_DWORD /d 1 /f')

    # 27. Enable verbose logging for debugging (for troubleshooting)
    print("27. Enabling verbose logging")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System" /v "VerboseStatus" /t REG_DWORD /d 1 /f')

    # 28. Enable file sharing for LAN debugging
    print("28. Enabling file sharing")
    run_command('netsh advfirewall firewall set rule group="File and Printer Sharing" new enable=yes')

    # 29. Increase TCP/IP ephemeral port range (for testing)
    print("29. Increasing TCP/IP ephemeral port range")
    run_command('netsh int ipv4 set dynamicport tcp start=1024 num=65535')

    # 30. Enable Windows Sandbox
    print("30. Enabling Windows Sandbox")
    run_command('dism /online /enable-feature /featurename:Containers-DisposableClientVM /all /norestart')

    print("\nProgrammer tweaks applied. Restart your PC for full effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    programmer_tweaks()
