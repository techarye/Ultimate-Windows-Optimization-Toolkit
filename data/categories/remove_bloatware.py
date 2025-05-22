import subprocess
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_powershell(cmd):
    try:
        completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True, text=True, check=True)
        print(completed.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {cmd}\n{e}")

def remove_bloatware():
    print("Removing common Windows bloatware apps...")

    # 1. Remove Xbox app
    print("1. Removing Xbox App")
    run_powershell("Get-AppxPackage *xboxapp* | Remove-AppxPackage")

    # 2. Remove Candy Crush
    print("2. Removing Candy Crush")
    run_powershell("Get-AppxPackage *candycrush* | Remove-AppxPackage")

    # 3. Remove Microsoft Solitaire Collection
    print("3. Removing Microsoft Solitaire Collection")
    run_powershell("Get-AppxPackage *solitairecollection* | Remove-AppxPackage")

    # 4. Remove Microsoft People app
    print("4. Removing People app")
    run_powershell("Get-AppxPackage *people* | Remove-AppxPackage")

    # 5. Remove Microsoft Sticky Notes
    print("5. Removing Sticky Notes")
    run_powershell("Get-AppxPackage *stickynotes* | Remove-AppxPackage")

    # 6. Remove Microsoft Photos
    print("6. Removing Microsoft Photos")
    run_powershell("Get-AppxPackage *photos* | Remove-AppxPackage")

    # 7. Remove Groove Music
    print("7. Removing Groove Music")
    run_powershell("Get-AppxPackage *zunemusic* | Remove-AppxPackage")

    # 8. Remove Movies & TV
    print("8. Removing Movies & TV")
    run_powershell("Get-AppxPackage *zunevideo* | Remove-AppxPackage")

    # 9. Remove Weather app
    print("9. Removing Weather app")
    run_powershell("Get-AppxPackage *bingweather* | Remove-AppxPackage")

    # 10. Remove News app
    print("10. Removing News app")
    run_powershell("Get-AppxPackage *bingnews* | Remove-AppxPackage")

    # 11. Remove Microsoft Office Hub
    print("11. Removing Office Hub")
    run_powershell("Get-AppxPackage *officehub* | Remove-AppxPackage")

    # 12. Remove Skype app
    print("12. Removing Skype")
    run_powershell("Get-AppxPackage *skypeapp* | Remove-AppxPackage")

    # 13. Remove 3D Builder
    print("13. Removing 3D Builder")
    run_powershell("Get-AppxPackage *3dbuilder* | Remove-AppxPackage")

    # 14. Remove Mixed Reality Portal
    print("14. Removing Mixed Reality Portal")
    run_powershell("Get-AppxPackage *mixedrealityportal* | Remove-AppxPackage")

    # 15. Remove People app (duplicate check)
    print("15. Removing People app (duplicate)")
    run_powershell("Get-AppxPackage *people* | Remove-AppxPackage")

    # 16. Remove Feedback Hub
    print("16. Removing Feedback Hub")
    run_powershell("Get-AppxPackage *feedbackhub* | Remove-AppxPackage")

    # 17. Remove Maps
    print("17. Removing Maps app")
    run_powershell("Get-AppxPackage *windowsmaps* | Remove-AppxPackage")

    # 18. Remove OneNote
    print("18. Removing OneNote")
    run_powershell("Get-AppxPackage *onenote* | Remove-AppxPackage")

    # 19. Remove Paint 3D
    print("19. Removing Paint 3D")
    run_powershell("Get-AppxPackage *paint3d* | Remove-AppxPackage")

    # 20. Remove Xbox Game Overlay
    print("20. Removing Xbox Game Overlay")
    run_powershell("Get-AppxPackage *gamingoverlay* | Remove-AppxPackage")

    # 21. Remove Xbox Game Speech Window
    print("21. Removing Xbox Game Speech Window")
    run_powershell("Get-AppxPackage *gamingservices* | Remove-AppxPackage")

    # 22. Remove Cortana
    print("22. Removing Cortana")
    run_powershell("Get-AppxPackage *cortana* | Remove-AppxPackage")

    # 23. Remove Microsoft Store (optional, be cautious)
    print("23. Removing Microsoft Store (optional)")
    run_powershell("Get-AppxPackage *windowsstore* | Remove-AppxPackage")

    # 24. Remove Mixed Reality Services
    print("24. Removing Mixed Reality Services")
    run_powershell("Get-AppxPackage *windowscommunicationsapps* | Remove-AppxPackage")

    # 25. Remove Voice Recorder
    print("25. Removing Voice Recorder")
    run_powershell("Get-AppxPackage *soundrecorder* | Remove-AppxPackage")

    # 26. Remove Alarms & Clock
    print("26. Removing Alarms & Clock")
    run_powershell("Get-AppxPackage *windowsalarms* | Remove-AppxPackage")

    # 27. Remove Messaging
    print("27. Removing Messaging")
    run_powershell("Get-AppxPackage *messaging* | Remove-AppxPackage")

    # 28. Remove Mail and Calendar
    print("28. Removing Mail and Calendar")
    run_powershell("Get-AppxPackage *windowscommunicationsapps* | Remove-AppxPackage")

    # 29. Remove Xbox Identity Provider
    print("29. Removing Xbox Identity Provider")
    run_powershell("Get-AppxPackage *xboxidentityprovider* | Remove-AppxPackage")

    # 30. Remove People Experience Host
    print("30. Removing People Experience Host")
    run_powershell("Get-AppxPackage *peopleexperiencehost* | Remove-AppxPackage")

    print("\nBloatware removal completed. Restart your PC to finalize.")

if __name__ == "__main__":
    if not is_admin():
        print("Please run this script as Administrator!")
        sys.exit(1)
    remove_bloatware()
