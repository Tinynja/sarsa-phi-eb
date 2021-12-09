$OldPwd = Get-Location

Set-Location "${PSScriptRoot}"

# Make a copy of Pipfile and remove Colab-expluded packages
Copy-Item "..\Pipfile" "."
(Get-Content "..\Pipfile_Colab_exclude") | ForEach-Object {(Get-Content ".\Pipfile") -replace "$_.*","" | Set-Content ".\Pipfile"}

# Generate requirements file
pipenv lock -r > ..\requirements_Colab.txt

# Cleanup
Remove-Item @("Pipfile", "Pipfile.lock")
Set-Location $OldPwd