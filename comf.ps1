$cpp_file = $args[0]
$file_path_no_extensions = [System.IO.Path]::GetFileNameWithoutExtension($cpp_file)
$target = $file_path_no_extensions +".exe"
g++ -std=c++17 -Wshadow -Wall -o $target -g $cpp_file

$command = "type D:\devel\algorithm\in.txt | .\$($target)"
$starttime = Get-Date
$output = Invoke-Expression $command
$endtime = Get-Date
$executetime = $endtime - $starttime
echo $output
Write-Host "time: $($executetime.TotalMilliseconds) ms."
