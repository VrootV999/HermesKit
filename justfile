default: build
[linux]
set shell := ["sh", "-cu"]

[windows]
set shell := ["powershell.exe","-c"]

[macos]
set shell := ["zsh", "-cu"]

setup:
  go mod download
  go install gotest.tools/gotestsum@latest

  @echo ""
  @echo "Setup Done"

# Build Release Version for Darwin Systems
[linux]
[unix]
[macos]
build:
  @just setup
  @echo "Creating Required Directories"
  mkdir -p Lib Build/Release

  @echo "Building Rust Library (Release)"
  cd Core && cargo build --release

  @echo "Copying static library artifacts"
  cp Core/target/release/libHermes_Core.a Lib/

  @echo "Building Go Binary (Release)"
  go build -o Build/Release/HermesKit main.go
  @echo "Release build complete!"

# Build Release Version for Windows Systems
[windows]
build:
  @just setup
  @Write-Host "Creating Required Directories"
  if (!(Test-Path "Lib")) { New-Item -ItemType Directory -Force -Path "Lib" | Out-Null }
  if (!(Test-Path "Build\Release")) { New-Item -ItemType Directory -Force -Path "Build\Release" | Out-Null }

  @Write-Host "Building Rust Static Library (Release)"
  Set-Location Core; cargo build --release

  Copy-Item "Core\target\release\Hermes_Core.lib" "Lib" -Force

  @Write-Host "Building Go Binary (Release)"
  go build -o Build/Release/HermesKit.exe main.go
  
  @Write-Host "Release build complete!" -ForegroundColor Green
