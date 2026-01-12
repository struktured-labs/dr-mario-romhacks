#!/bin/bash
# Wrapper script to run Mesen with .NET in PATH
export PATH="$HOME/.dotnet:$PATH"
export DOTNET_ROOT="$HOME/.dotnet"
exec "$(dirname "$0")/mesen2/bin/linux-x64/Release/Mesen" "$@"
