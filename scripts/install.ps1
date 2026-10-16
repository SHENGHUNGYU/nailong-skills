# Windows entry point; forwards arguments and the installer's exit code.
if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$PSScriptRoot/install.py" @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$PSScriptRoot/install.py" @args
} else {
    Write-Error "Python 3 is required. Install Python and try again."
    exit 1
}
exit $LASTEXITCODE
