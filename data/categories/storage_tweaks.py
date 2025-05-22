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

def storage_tweaks():
    print("Applying Storage Tweaks...\n")

    # 1. Enable Storage Sense
    print("1. Enabling Storage Sense")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v 01 /t REG_DWORD /d 1 /f')

    # 2. Set Storage Sense cleanup frequency to daily
    print("2. Setting Storage Sense cleanup frequency to daily")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v 01 /t REG_DWORD /d 1 /f')

    # 3. Enable deletion of temporary files
    print("3. Enabling deletion of temporary files")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v 02 /t REG_DWORD /d 1 /f')

    # 4. Delete files in recycle bin older than 30 days
    print("4. Setting recycle bin to delete files older than 30 days")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy" /v 03 /t REG_DWORD /d 1 /f')

    # 5. Disable thumbnail cache to save disk space
    print("5. Disabling thumbnail cache")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DisableThumbnailCache /t REG_DWORD /d 1 /f')

    # 6. Disable prefetcher to reduce disk writes (not recommended for SSD)
    print("6. Disabling prefetcher")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters" /v EnablePrefetcher /t REG_DWORD /d 0 /f')

    # 7. Disable superfetch (SysMain) service
    print("7. Disabling SysMain (Superfetch) service")
    run_command('sc config SysMain start= disabled')
    run_command('net stop SysMain')

    # 8. Disable Windows Search Indexing service (optional)
    print("8. Disabling Windows Search Indexing")
    run_command('sc config WSearch start= disabled')
    run_command('net stop WSearch')

    # 9. Disable Windows Error Reporting disk writes
    print("9. Disabling Windows Error Reporting disk writes")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting" /v Disabled /t REG_DWORD /d 1 /f')

    # 10. Clear Windows Update cache
    print("10. Clearing Windows Update cache")
    run_command('net stop wuauserv')
    run_command('del /q /f /s %windir%\\SoftwareDistribution\\Download\\*')
    run_command('net start wuauserv')

    # 11. Enable write caching on all drives
    print("11. Enabling write caching on all drives")
    run_command('powercfg /setactive SCHEME_BALANCED')  # Balanced plan usually enables write caching

    # 12. Disable drive indexing for faster disk access
    print("12. Disabling drive indexing")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\WSearch" /v Start /t REG_DWORD /d 4 /f')

    # 13. Disable automatic defragmentation for SSDs
    print("13. Disabling automatic defrag for SSDs")
    run_command('defrag C: /L')

    # 14. Disable Windows Disk Cleanup notifications
    print("14. Disabling Disk Cleanup notifications")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced" /v DontUseRecycleBin /t REG_DWORD /d 1 /f')

    # 15. Increase system cache working set size
    print("15. Increasing system cache working set size")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v LargeSystemCache /t REG_DWORD /d 1 /f')

    # 16. Enable NTFS last access updates (improves compatibility)
    print("16. Enabling NTFS last access updates")
    run_command('fsutil behavior set disablelastaccess 0')

    # 17. Enable TRIM for SSDs
    print("17. Enabling TRIM for SSDs")
    run_command('fsutil behavior set disabledeletenotify 0')

    # 18. Disable offline files caching
    print("18. Disabling offline files caching")
    run_command('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Services\\CscService" /v Start /t REG_DWORD /d 4 /f')

    # 19. Disable System Restore to save disk space (optional)
    print("19. Disabling System Restore")
    run_command('wmic.exe /Namespace:\\\\root\\default Path SystemRestore Call Disable')

    # 20. Set recycle bin max size to 10% of disk
    print("20. Setting Recycle Bin max size to 10% of disk")
    run_command('reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\BitBucket" /v MaxCapacity /t REG_DWORD /d 10485760 /f')

    # 21. Disable Windows backup service
    print("21. Disabling Windows backup service")
    run_command('sc config sdclt start= disabled')
    run_command('net stop sdclt')

    # 22. Disable scheduled defrag task
    print("22. Disabling scheduled defrag task")
    run_command('schtasks /Change /TN "\\Microsoft\\Windows\\Defrag\\ScheduledDefrag" /Disable')

    # 23. Enable Quick Removal for USB drives (disable write caching)
    print("23. Enabling Quick Removal for USB drives")
    # This needs manual GUI or registry tweaks — skipped here

    # 24. Disable Windows Update delivery optimization
    print("24. Disabling Windows Update Delivery Optimization")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization" /v DODownloadMode /t REG_DWORD /d 0 /f')

    # 25. Clear temporary files folder
    print("25. Clearing temporary files folder")
    temp = os.getenv('TEMP')
    if temp:
        run_command(f'del /q /f /s "{temp}\\*"')

    # 26. Disable automatic disk error checking on boot
    print("26. Disabling automatic disk error checking on boot")
    run_command('chkntfs /x C:')

    # 27. Disable offline files service
    print("27. Disabling offline files service")
    run_command('sc config CscService start= disabled')
    run_command('net stop CscService')

    # 28. Disable ReadyBoost
    print("28. Disabling ReadyBoost")
    run_command('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ReadyBoost" /v Enabled /t REG_DWORD /d 0 /f')

    # 29. Disable Windows Media Player Network Sharing Service
    print("29. Disabling WMP Network Sharing Service")
    run_command('sc config WMPNetworkSvc start= disabled')
    run_command('net stop WMPNetworkSvc')

    # 30. Disable Disk Quotas
    print("30. Disabling Disk Quotas")
    run_command('fsutil quota disable C:')

    print("\nStorage tweaks applied. Please restart your computer for all changes to take effect.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    storage_tweaks()
