# general_tweaks.py
import os
import subprocess

def disable_startup_sound():
    # Disable Windows startup sound via registry
    cmd = r'reg add "HKCU\AppEvents\EventLabels\SystemStart" /v ExcludeFromCPL /t REG_DWORD /d 1 /f'
    subprocess.run(cmd, shell=True)
    print("✔ Disabled Windows startup sound.")

def show_file_extensions():
    # Show file extensions in Explorer
    cmd = r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v HideFileExt /t REG_DWORD /d 0 /f'
    subprocess.run(cmd, shell=True)
    print("✔ Enabled showing file extensions.")

def enable_dark_mode():
    # Enable dark mode for apps
    cmd1 = r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v AppsUseLightTheme /t REG_DWORD /d 0 /f'
    cmd2 = r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" /v SystemUsesLightTheme /t REG_DWORD /d 0 /f'
    subprocess.run(cmd1, shell=True)
    subprocess.run(cmd2, shell=True)
    print("✔ Enabled dark mode.")

def menu():
    while True:
        os.system('cls')
        print("=== General System Tweaks ===")
        print("1. Disable Windows startup sound")
        print("2. Show file extensions in Explorer")
        print("3. Enable dark mode")
        print("0. Return to main menu")
        choice = input("Enter choice: ")

        if choice == "1":
            disable_startup_sound()
        elif choice == "2":
            show_file_extensions()
        elif choice == "3":
            enable_dark_mode()
        elif choice == "0":
            break
        else:
            print("Invalid choice, try again.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    menu()
