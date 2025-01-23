param (
    [switch]$build
)

function Copy-FilesToScratchpad {
    $source = Join-Path $PSScriptRoot "addon" "globalPlugins" "voicemeeter"
    $target = Join-Path $env:appdata "nvda" "scratchpad" "globalPlugins" "voicemeeter"
    Robocopy $source $target | Out-Null
}

function Build-Addon {
    "Building add-on" | Write-Host
    scons
}

function Main {
    "Copying updated files to Scratchpad" | Write-Host
    Copy-FilesToScratchpad

    if ($build) {
        Build-Addon
    }
}

if ($MyInvocation.InvocationName -ne '.') { Main }