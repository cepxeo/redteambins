
### Connect to Global Catalog and setup searcher for the entire forest

[ADSI] $RootDSE = “LDAP://RootDSE”
[Object] $RootDomain = New-Object System.DirectoryServices.DirectoryEntry “GC://$($RootDSE.rootDomainNamingContext)”
[Object] $Searcher = New-Object System.DirectoryServices.DirectorySearcher
$Searcher.SearchRoot = $RootDomain
$Searcher.PageSize = 1000

### Clear all properties and add properties to load, adjust with additional properties if needed

$Searcher.PropertiesToLoad.Clear()
$Searcher.PropertiesToLoad.Add("Name") > $Null
$Searcher.PropertiesToLoad.Add("UserprincipalName") > $Null
$Searcher.PropertiesToLoad.Add("proxyAddresses") > $Null 
$Searcher.PropertiesToLoad.Add("sAMAccountName") > $Null 
$Searcher.PropertiesToLoad.Add("displayName") > $Null 
$Searcher.CacheResults = $false

### Filter for any user object in the forest

$Searcher.Filter = “(&(objectCategory=User))”

### Initiate search and collect results in the results variable

$Results = $Searcher.FindAll()

### Go through the results and store each result in a PSobject in the UserArray variable

$UserArray = @()
ForEach ($User In $Results){

    $Addresses = $User.Properties.Item("proxyAddresses")
    [string] $upn = $User.Properties.Item("UserprincipalName")
    [string] $sam = $User.Properties.Item("sAMAccountName")
    [string] $name = $User.Properties.Item("Name")
    [string] $displayname = $User.Properties.Item("displayName")

    $Properties = @{'UPN' = $upn; 'Name'= $name ; 'DisplayName' = $displayname; 'SAM' = $sam; 'Addresses' = $Addresses}

    $UserArray += New-Object -TypeName PSObject -Property $Properties            

}

$Results.Dispose()
$Searcher.Dispose()

### Select properties in the right order and output to GridView

$UserArray | select UPN,SAM,Name,DisplayName,Addresses | Out-GridView -Title 'AD Forest User List'
