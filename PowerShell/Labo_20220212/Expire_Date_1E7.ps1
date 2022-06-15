Import-Module ActiveDirectory

$csvfile = Import-Csv Users_1E7.csv -Delimiter ","

ForEach ($User in $csvfile)
{
    $ExpiryDate = $User.ExpirationDate
    $username = $User.Username

    
    if (Get-ADUser -F {SamAccountName -eq $Username})
    {
        Set-ADAccountExpiration -Identity $username -DateTime $ExpiryDate
    } 
}
