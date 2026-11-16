param([string]$InputFile,[string]$OutputFile)
$ErrorActionPreference = 'Stop'
$documentPath = (Resolve-Path -LiteralPath $InputFile).Path
$pdfPath = [System.IO.Path]::GetFullPath($OutputFile)
$wordApplication = $null
$wordDocument = $null
try {
    $wordApplication = New-Object -ComObject Word.Application
    $wordApplication.Visible = $false
    $wordApplication.DisplayAlerts = 0
    $wordDocument = $wordApplication.Documents.Open($documentPath, $false, $true)
    $wordDocument.Repaginate()
    Write-Output ('Pages: ' + $wordDocument.ComputeStatistics(2))
    $wordDocument.ExportAsFixedFormat($pdfPath, 17)
    Write-Output $pdfPath
}
finally {
    if ($null -ne $wordDocument) { $wordDocument.Close(0) }
    if ($null -ne $wordApplication) { $wordApplication.Quit() }
}
