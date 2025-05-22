import os
import ctypes
import subprocess

# Aggressive bloatware list for Windows 10/11
BLOATWARE_APPS = [
    # Microsoft/Windows Apps
    "Microsoft.3DBuilder",
    "Microsoft.BingNews",
    "Microsoft.BingWeather",
    "Microsoft.GetHelp",
    "Microsoft.Getstarted",
    "Microsoft.Microsoft3DViewer",
    "Microsoft.MicrosoftOfficeHub",
    "Microsoft.MicrosoftSolitaireCollection",
    "Microsoft.MicrosoftStickyNotes",
    "Microsoft.MixedReality.Portal",
    "Microsoft.OneConnect",
    "Microsoft.People",
    "Microsoft.Print3D",
    "Microsoft.SkypeApp",
    "Microsoft.Wallet",
    "Microsoft.WindowsAlarms",
    "Microsoft.WindowsCamera",
    "Microsoft.WindowsFeedbackHub",
    "Microsoft.WindowsMaps",
    "Microsoft.WindowsSoundRecorder",
    "Microsoft.Xbox.TCUI",
    "Microsoft.XboxApp",
    "Microsoft.XboxGameOverlay",
    "Microsoft.XboxGamingOverlay",
    "Microsoft.XboxIdentityProvider",
    "Microsoft.XboxSpeechToTextOverlay",
    "Microsoft.YourPhone",
    "Microsoft.ZuneMusic",
    "Microsoft.ZuneVideo",
    "MicrosoftTeams",
    "Microsoft.OneDrive",
    "Microsoft.GamingApp",
    "Microsoft.Todos",
    "Microsoft.PowerAutomateDesktop",
    "Microsoft.MSPaint",
    "Microsoft.ScreenSketch",
    "Microsoft.HEIFImageExtension",
    "Microsoft.HEVCVideoExtension",
    "Microsoft.WebMediaExtensions",
    "Microsoft.WebpImageExtension",
    "Microsoft.VP9VideoExtensions",
    "Microsoft.PeopleExperienceHost",
    "Microsoft.549981C3F5F10",  # Cortana
    "Microsoft.BingFinance",
    "Microsoft.BingSports",
    "Microsoft.BingTravel",
    "Microsoft.Office.OneNote",
    "Microsoft.Office.Sway",
    "Microsoft.MinecraftUWP",
    "Microsoft.MicrosoftEdge.Stable",
    "Microsoft.MicrosoftEdgeDevToolsClient",
    "Microsoft.MicrosoftEdgeBeta",
    "Microsoft.MicrosoftEdgeCanary",
    "Microsoft.MicrosoftEdgeWebView",
    "Microsoft.WindowsReadingList",
    "Microsoft.WindowsTerminal",
    "Microsoft.WindowsStore",
    "Microsoft.Windows.Photos",
    "Microsoft.WindowsCalculator",
    "Microsoft.WindowsCommunicationsApps",  # Mail & Calendar
    # Third-party and OEM
    "SpotifyAB.SpotifyMusic",
    "Disney.37853FC22B2CE",
    "DolbyLaboratories.DolbyAccess",
    "Facebook.Facebook",
    "king.com.CandyCrushSaga",
    "king.com.CandyCrushSodaSaga",
    "king.com.FarmHeroesSaga",
    "A278AB0D.MarchofEmpires",
    "GAMELOFTSA.Asphalt8Airborne",
    "KeeperSecurityInc.Keeper",
    "PandoraMediaInc.29680B314EFC2",
    "SlingTVLLC.SlingTV",
    "Twitter.Twitter",
    "Flipboard.Flipboard",
    "ShazamEntertainmentLtd.Shazam",
    "AdobeSystemsIncorporated.AdobePhotoshopExpress",
    "Duolingo-LearnLanguagesforFree",
    "EclipseManager",
    "ActiproSoftwareLLC.562882FEEB491",
    "D5EA27B7.Duolingo-LearnLanguagesforFree",
]

# Remove duplicates, just in case
BLOATWARE_APPS = list(set(BLOATWARE_APPS))

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def remove_bloatware():
    print("Starting BIG Bloatware Remover for Windows 10/11...")
    for app in BLOATWARE_APPS:
        print(f"  Removing {app}...")
        cmd = f'powershell -Command "Get-AppxPackage *{app}* | Remove-AppxPackage"'
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            print(f"    Could not remove {app} (may not be installed or already removed).")
    # Remove provisioned apps for new users
    print("Removing provisioned apps for new users...")
    for app in BLOATWARE_APPS:
        cmd = f'powershell -Command "Get-AppxProvisionedPackage -Online | Where-Object {{$_.PackageName -like \'*{app}*\'}} | Remove-AppxProvisionedPackage -Online"'
        try:
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    print("Bloatware removal complete!")

def main():
    if not is_admin():
        print("This script requires administrator privileges. Please run as admin.")
        return

    print("WARNING: This will attempt to remove most pre-installed Windows apps for all users.")
    confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Operation cancelled.")
        return

    remove_bloatware()
    print("Tweak applied. Please restart your PC for full effect.")

    while True:
        restart = input("Do you want to restart now to apply all changes? (yes/no): ").strip().lower()
        if restart == "yes":
            print("Restarting your computer...")
            os.system("shutdown /r /t 3")
            break
        elif restart == "no":
            print("Returning to main script. Please restart later for full effect.")
            break
        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()