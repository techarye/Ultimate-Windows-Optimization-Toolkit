# install_python.ps1
# Automatically downloads and installs the latest Python 3.x for Windows (64-bit)

$pythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$installerPath = "$env:TEMP\python-installer.exe"

Write-Host "Downloading Python installer..."
Invoke-WebRequest -Uri $pythonInstallerUrl -OutFile $installerPath

Write-Host "Installing Python silently..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0" -Wait

Write-Host "Cleaning up..."
Remove-Item $installerPath

Write-Host "Python installation complete. Please restart your terminal or command prompt."
