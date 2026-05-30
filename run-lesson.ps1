param(
    [Parameter(Mandatory = $true)]
    [string]$Lesson
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$lessonFile = Join-Path $Lesson "lesson.py"
if (-not (Test-Path $lessonFile)) {
    Write-Error "Lesson not found: $lessonFile (example: .\run-lesson.ps1 -Lesson 01_basics)"
}

Write-Host "Running $lessonFile"
python $lessonFile

$practiceFile = Join-Path $Lesson "practice.py"
if (Test-Path $practiceFile) {
    Write-Host ""
    Write-Host "Running $practiceFile"
    python $practiceFile
}
