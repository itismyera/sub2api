param(
    [string]$OutputPath = ".env",
    [string]$AdminEmail = "admin@sub2api.local",
    [string]$AdminPassword = "",
    [string]$Sub2ApiImage = "",
    [int]$HostServerPort = 18080,
    [string]$CaddyDataVolume = "",
    [string]$CaddyConfigVolume = ""
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$templatePath = Join-Path $scriptDir ".env.example"

if (-not (Test-Path -LiteralPath $templatePath)) {
    throw "Template not found: $templatePath"
}

function New-HexSecret([int]$Bytes = 32) {
    $requiredLength = $Bytes * 2
    $value = ""
    while ($value.Length -lt $requiredLength) {
        $value += [guid]::NewGuid().ToString("N")
    }
    return $value.Substring(0, $requiredLength)
}

function Set-OrAppendEnvValue {
    param(
        [string[]]$Lines,
        [string]$Key,
        [string]$Value
    )

    $prefix = "$Key="
    $updated = $false
    for ($i = 0; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i].StartsWith($prefix)) {
            $Lines[$i] = "$prefix$Value"
            $updated = $true
        }
    }

    if (-not $updated) {
        $Lines += "$prefix$Value"
    }

    return ,$Lines
}

$outputFullPath = if ([System.IO.Path]::IsPathRooted($OutputPath)) {
    $OutputPath
} else {
    Join-Path $scriptDir $OutputPath
}

$lines = Get-Content -LiteralPath $templatePath
$lines = Set-OrAppendEnvValue -Lines $lines -Key "POSTGRES_PASSWORD" -Value (New-HexSecret)
$lines = Set-OrAppendEnvValue -Lines $lines -Key "JWT_SECRET" -Value (New-HexSecret)
$lines = Set-OrAppendEnvValue -Lines $lines -Key "TOTP_ENCRYPTION_KEY" -Value (New-HexSecret)
$lines = Set-OrAppendEnvValue -Lines $lines -Key "ADMIN_EMAIL" -Value $AdminEmail
$lines = Set-OrAppendEnvValue -Lines $lines -Key "ADMIN_PASSWORD" -Value $AdminPassword
$lines = Set-OrAppendEnvValue -Lines $lines -Key "HOST_SERVER_PORT" -Value $HostServerPort
if ($Sub2ApiImage) {
    $lines = Set-OrAppendEnvValue -Lines $lines -Key "SUB2API_IMAGE" -Value $Sub2ApiImage
}

if ($CaddyDataVolume) {
    $lines = Set-OrAppendEnvValue -Lines $lines -Key "CADDY_DATA_VOLUME" -Value $CaddyDataVolume
}

if ($CaddyConfigVolume) {
    $lines = Set-OrAppendEnvValue -Lines $lines -Key "CADDY_CONFIG_VOLUME" -Value $CaddyConfigVolume
}

$outputDir = Split-Path -Parent $outputFullPath
if ($outputDir -and -not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

Set-Content -LiteralPath $outputFullPath -Value $lines -Encoding ascii

foreach ($dirName in @("data", "postgres_data", "redis_data")) {
    $dirPath = Join-Path $scriptDir $dirName
    if (-not (Test-Path -LiteralPath $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath | Out-Null
    }
}

Write-Output "Generated $outputFullPath"
Write-Output "Created/verified data directories under $scriptDir"
