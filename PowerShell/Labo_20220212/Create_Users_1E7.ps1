# Importer le module Active Directory pour exécuter les Commandes-let AD
Import-Module ActiveDirectory
  
# Stocker les données de Users_1E7.csv dans le variables $ADUsers
$ADUsers = Import-Csv Users_1E7.csv -Delimiter ","

# Définir l'UPN
$UPN = "@ad.private"

# Boucle sur chaque ligne contenant les détails de l'utilisateur dans le fichier CSV
foreach ($User in $ADUsers) {

    #Lire les données utilisateur de chaque champ de chaque ligne et assigner les données à u7ne variable comme ci-dessous
    $username = $User.username
    $password = $User.password
    $firstname = $User.firstname
    $lastname = $User.lastname
    $initials = $User.initials
    $OU = $User.ou #Ce champ fait  référence à l'OU dans lequel le compte utilisateur doit être créé
    $email = $User.email
    $jobtitle = $User.jobtitle
    $company = $User.company
    $department = $User.department

    # Vérifier si l'utilisateur existe déjà dans L'AD
    if (Get-ADUser -F { SamAccountName -eq $username }) {
        
        # Si l'utilisateur existe, donner un avertissement
        Write-Warning "A user account with username $username already exists in Active Directory."
    }
    else {

        # L'utilisateur n'existe pas, alors il faut créer le nouveau compte utilisateur.
        # Le compte sera créé dans l'OU fourni par la variable $OU lue dans le fichier CSV
        New-ADUser `
            -SamAccountName $username `
            -UserPrincipalName "$username@$UPN" `
            -Name "$firstname $lastname" `
            -GivenName $firstname `
            -Surname $lastname `
            -Initials $initials `
            -DisplayName "$lastname, $firstname" `
            -Path $OU `
            -Company $company `
            -EmailAddress $email `
            -Title $jobtitle `
            -Department $department `
            -AccountPassword (ConvertTo-secureString $password -AsPlainText -Force) -ChangePasswordAtLogon $True
            

        # Si l'utilisateur est créé, afficher le message.
        Write-Host "The user account $username is created." -ForegroundColor Cyan
    }
}

Read-Host -Prompt "Press Enter to exit"