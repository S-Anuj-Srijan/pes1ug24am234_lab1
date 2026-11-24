param([ValidateSet('coverage', 'fuzz', 'demo')][string]$Evidence = 'coverage')
$root = Split-Path $PSScriptRoot -Parent
$python = Join-Path $root '.venv/Scripts/python.exe'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONIOENCODING = 'utf-8'
$Host.UI.RawUI.WindowTitle = "S Anuj Srijan - $Evidence evidence"
Clear-Host
Write-Host 'S Anuj Srijan | PES1UG24AM234' -ForegroundColor Cyan
if ($Evidence -eq 'coverage') {
    Set-Location (Join-Path $root 'lab6')
    Write-Host "`nLAB 6 - CODE COVERAGE" -ForegroundColor Cyan
    Write-Host '> python -m coverage run --source=visa_application -m pytest CodeCoverageTest_visa_application.py -q'
    & $python -m coverage run --source=visa_application -m pytest CodeCoverageTest_visa_application.py -q
    Write-Host '> python -m coverage report -m'
    & $python -m coverage report -m
    Write-Host "`nLAB 6 - BRANCH COVERAGE" -ForegroundColor Cyan
    Write-Host '> python -m coverage run --branch --source=visa_application -m pytest BranchCoverageTest_visa_application.py -q'
    & $python -m coverage run --branch --source=visa_application -m pytest BranchCoverageTest_visa_application.py -q
    Write-Host '> python -m coverage report -m'
    & $python -m coverage report -m
} elseif ($Evidence -eq 'fuzz') {
    Set-Location (Join-Path $root 'lab7')
    Write-Host "`nLAB 7 - ORIGINAL: EXPECTED FAILURES" -ForegroundColor Cyan
    $env:LAB7_TARGET = 'baseline'
    Write-Host '> LAB7_TARGET=baseline python -m pytest test_processor.py -k no_crash -q --tb=no'
    & $python -m pytest test_processor.py -k no_crash -q --tb=no
    Write-Host "`nLAB 7 - FIXED: FULL TEST SUITE" -ForegroundColor Cyan
    $env:LAB7_TARGET = 'fixed'
    Write-Host '> LAB7_TARGET=fixed python -m pytest test_processor.py -q'
    & $python -m pytest test_processor.py -q
} else {
    Set-Location (Join-Path $root 'lab7')
    Write-Host "`nLAB 7 - ORIGINAL: EMPTY INPUT" -ForegroundColor Cyan
    Write-Host '> python baseline/visa_application.py [three empty input lines]'
    "`n`n`n" | & $python baseline/visa_application.py
    Write-Host "`nLAB 7 - FIXED: SAME EMPTY INPUT" -ForegroundColor Cyan
    Write-Host '> python visa_application.py [three empty input lines]'
    "`n`n`n" | & $python visa_application.py
    Write-Host "`nLAB 7 - FIXED: VALID INPUT" -ForegroundColor Cyan
    Write-Host '> python visa_application.py [tourist:2 / 5,10,21 / 6000|500]'
    "tourist:2`n5,10,21`n6000|500" | & $python visa_application.py
}
Write-Host "`nEvidence run complete." -ForegroundColor Green
