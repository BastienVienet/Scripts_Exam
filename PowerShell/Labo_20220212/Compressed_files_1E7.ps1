Import-Module ActiveDirectory

New-Item -Path "C:\" -Name "Workspace" -ItemType "directory"
New-Item -Path "C:\Workspace" -Name "Compressed_Files" -ItemType "directory"

Get-ADUser -Filter 'Company -like "SoftDev"' -Properties * | Select-Object SamAccountName,UserPrincipalName,Name,GivenName,Surname,Initials,DisplayName,Path,Company,EmailAddress,Title,Department,AccountPassword,ExpirationDate | export-csv -path C:\Workspace\Users_exported.csv

Compress-Archive C:\Workspace\Users_exported.csv -DestinationPath ('C:\Workspace\Compressed_Files\' + (Get-Date -Format dd/MM/yyy) + '.zip')