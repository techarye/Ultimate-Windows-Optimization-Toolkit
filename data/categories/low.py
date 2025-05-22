import subprocess
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip()

def disable_visual_effects():
    # Disable animations and shadows
    cmds = [
        r'reg add "HKCU\Control Panel\Desktop\WindowMetrics" /v MinAnimate /t REG_SZ /d 0 /f',
        r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" /v VisualFXSetting /t REG_DWORD /d 2 /f',
        r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v ListviewShadow /t REG_DWORD /d 0 /f',
        r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" /v TaskbarAnimations /t REG_DWORD /d 0 /f'
    ]
    for cmd in cmds:
        run_cmd(cmd)
    print("[*] Visual effects disabled")

def disable_sysmain_service():
    # Stop and disable SysMain (Superfetch)
    run_cmd("sc stop SysMain")
    run_cmd("sc config SysMain start= disabled")
    print("[*] SysMain service stopped and disabled")

def set_high_performance_power_plan():
    # Set power plan to High Performance
    run_cmd('powercfg -setactive SCHEME_MIN')
    print("[*] Power plan set to High Performance")

def disable_windows_tips():
    # Disable Windows Tips
    run_cmd(r'reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager" /v SystemPaneSuggestionsEnabled /t REG_DWORD /d 0 /f')
    print("[*] Windows tips disabled")

def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as admin.")
        return

    print("Starting low performance boost tweak...")
    disable_visual_effects()
    disable_sysmain_service()
    set_high_performance_power_plan()
    disable_windows_tips()
    print("Tweak applied. Please restart your PC for full effect.")

    # Prompt for restart
    while True:
        restart = input("Do you want to restart now to apply all changes? (yes/no): ").strip().lower()
        if restart == "yes":
            print("Restarting your computer...")
            import os
            os.system("shutdown /r /t 3")
            break
        elif restart == "no":
            print("Returning to main script. Please restart later for full effect.")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
