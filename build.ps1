param(
    [switch]$build
)

function Copy-FilestoScratchpad {
    $source = Join-Path $PSScriptRoot "addon" "globalPlugins" "voicemeeter"
    $target = Join-Path $env:appdata "nvda" "scratchpad" "globalPlugins" "voicemeeter"
    Robocopy $source $target | Out-Null
}

function main {
    "Copying files to Scratchpad" | Write-Host
    Copy-FilestoScratchpad

    if ($build) {
        Invoke-Expression ".venv/Scripts/Activate.ps1"

        "Building add-on" | Write-Host
        scons

        deactivate
    }
}

if ($MyInvocation.InvocationName -ne '.') { main }