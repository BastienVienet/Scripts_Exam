$datafromCSV = Import-Csv "Users_1E7.csv" -Delimiter ","

$department = $datafromCSV | Select-Object Department -Unique

for($i=0; $i -lt $department.Length ; $i++)
{
    New-ADOrganizationalUnit `    -Name $department[$i].Department `    -Path "DC=ad,DC=private" `
}