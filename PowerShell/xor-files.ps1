param (
 [Parameter(Mandatory=$true)]
 [string] $file1, #First File
 [Parameter(Mandatory=$true)]
 [string] $file2, #Second file
 [Parameter(Mandatory=$true)]
 [string] $out #Output File
) #end param
$file1_b = [System.IO.File]::ReadAllBytes("$file1")
$file2_b = [System.IO.File]::ReadAllBytes("$file2")
$len = if ($file1_b.Count -lt $file2_b.Count) {$file1_b.Count} else {
$file2_b.Count}
$xord_byte_array = New-Object Byte[] $len
# XOR between the files
for($i=0; $i -lt $len ; $i++) {
 $xord_byte_array[$i] = $file1_b[$i] -bxor $file2_b[$i] }
[System.IO.File]::WriteAllBytes("$out", $xord_byte_array)
write-host "[*] $file1 XOR $file2`n[*] Saved to " -nonewline;
Write-host "$out" -foregroundcolor yellow -nonewline; Write-host ".";