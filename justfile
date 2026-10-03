default: build
[linux]
set shell := ["sh", "-cu"]

[windows]
set shell := ["powershell.exe","-c"]

[macos]
set shell := ["zsh", "-cu"]

ci profile:
  @echo "Creating Required Directories"
  mkdir -p Lib Include Build/{{ profile }}

  @echo "Generating C Header with cbindgen."
  cd Core && cbindgen --lang c --output ../Include/HermesCore.h
  
  @echo "Building For Windows x86_64"
  cd Core && cargo build --target="x86_64-pc-windows-msvc" {{ if profile == "Release" { "--release" } else { "" } }}
  cp Core/target/x86_64-pc-windows-msvc/debug/Hermes_Core.lib Lib/
  GOOS=windows GOARCH=amd64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-windows-amd64.exe main.go
  rm Lib/Hermes_Core.lib

  @echo "Building For Windows x86"
  cd Core && cargo build --target="i686-pc-windows-msvc" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/i686-pc-windows-msvc/debug/Hermes_Core.lib Lib/
  GOOS=windows GOARCH=386 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-windows-x86.exe main.go
  rm Lib/Hermes_Core.lib

  @echo "Building For Windows armv8"
  cd Core && cargo build --target="aarch64-pc-windows-msvc" {{ if profile == "Release" { "--release" } else {""} }} 
  cp Core/target/aarch64-pc-windows-msvc/debug/Hermes_Core.lib Lib/
  GOOS=windows GOARCH=arm64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-windows-arm64.exe main.go
  rm Lib/Hermes_Core.lib

  @echo "Building For Linux x86_64"
  cd Core && cargo build --target="x86_64-unknown-linux-gnu" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/x86_64-unknown-linux-gnu/debug/libHermes_Core.a Lib/
  GOOS=linux GOARCH=amd64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-linux-amd64 main.go
  rm Lib/libHermes_Core.a
 
  @echo "Building For Linux x86"
  cd Core && cargo build --target="i686-unknown-linux-gnu" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/i686-unknown-linux-gnu/debug/libHermes_Core.a Lib/
  GOOS=linux GOARCH=386 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-linux-x86 main.go
  rm Lib/libHermes_Core.a

  @echo "Building For Linux armv8"
  cd Core && cargo build --target="aarch64-unknown-linux-gnu" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/aarch64-unknown-linux-gnu/debug/libHermes_Core.a Lib/
  GOOS=linux GOARCH=arm64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-linux-arm64 main.go
  rm Lib/libHermes_Core.a

  @echo "Building For Linux armv7"
  cd Core && cargo build --target="armv7-unknown-linux-gnueabihf" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/armv7-unknown-linux-gnueabihf/debug/libHermes_Core.a Lib/
  GOOS=linux GOARCH=arm GOARM=7 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-linux-armv7 main.go
  rm Lib/libHermes_Core.a

  @echo "Building For Macos x86_64"
  cd Core && cargo build --target="x86_64-apple-darwin" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/x86_64-apple-darwin/debug/libHermes_Core.a Lib/
  GOOS=darwin GOARCH=amd64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-darwin-amd64 main.go
  rm Lib/libHermes_Core.a

  @echo "Building For Macos armv8"
  cd Core && cargo build --target="aarch64-apple-darwin" {{ if profile == "Release" { "--release" } else {""} }}
  cp Core/target/aarch64-apple-darwin/debug/libHermes_Core.a Lib/
  GOOS=darwin GOARCH=arm64 go build -o Build/{{ profile }}/HermesKit-{{ profile }}-darwin-arm64 main.go
  rm Lib/libHermes_Core.a
  @echo "{{ profile }} build completed"

# Build Debug Version for Darwin Systems
[linux]
[unix]
[macos]
debug:
  @echo "Creating Required Directories"
  mkdir -p Lib Include Build/Debug

  @echo "Generating C Header with cbindgen"
  cd Core && cbindgen --lang c --output ../Include/HermesCore.h

  @echo "Building Rust Library (Debug)"
  cd Core && cargo build

  @echo "Copying static library artifacts"
  cp Core/target/debug/libHermes_Core.a Lib/

  @echo "Building Go Binary (Debug)"
  go build -o Build/Debug/HermesKit main.go
  @echo "Debug build complete!"

# Build Debug Version for Windows Systems
[windows]
debug:
  @Write-Host "Creating Required Directories"
  if (!(Test-Path "Lib")) { New-Item -ItemType Directory -Force -Path "Lib" | Out-Null }
  if (!(Test-Path "Include")) { New-Item -ItemType Directory -Force -Path "Include" | Out-Null }
  if (!(Test-Path "Build\Debug")) { New-Item -ItemType Directory -Force -Path "Build\Debug" | Out-Null }

  @Write-Host "Generating C Header with cbindgen"
  Set-Location Core; cbindgen --lang c --output "..\Include\HermesCore.h"
  
  @Write-Host "Building Rust Static Library (Debug)"
  Set-Location Core; cargo build

  Copy-Item "Core\target\debug\Hermes_Core.lib" "Lib" -Force

  @Write-Host "Building Go Binary (Debug)"
  go build -o Build/Debug/HermesKit.exe main.go
  
  @Write-Host "Debug build complete!" -ForegroundColor Green

# Build Release Version for Darwin Systems
[linux]
[unix]
[macos]
build:
  @just setup
  @echo "Creating Required Directories"
  mkdir -p Lib Include Build/Release

  @echo "Generating C Header with cbindgen"
  cd Core && cbindgen --lang c --output ../Include/HermesCore.h

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
  if (!(Test-Path "Include")) { New-Item -ItemType Directory -Force -Path "Include" | Out-Null }
  if (!(Test-Path "Build\Release")) { New-Item -ItemType Directory -Force -Path "Build\Release" | Out-Null }

  @Write-Host "Generating C Header with cbindgen"
  Set-Location Core; cbindgen --lang c --output "..\Include\HermesCore.h"
  
  @Write-Host "Building Rust Static Library (Release)"
  Set-Location Core; cargo build --release

  Copy-Item "Core\target\release\Hermes_Core.lib" "Lib" -Force

  @Write-Host "Building Go Binary (Release)"
  go build -o Build/Release/HermesKit.exe main.go
  
  @Write-Host "Release build complete!" -ForegroundColor Green

# Test the Code for Darwin Systems
[linux]
[unix]
[macos]
test gofile="":
  @echo "Testing"
  cd Core/ && cargo check
  gotestsum {{gofile}}

# Test the Code for Windows Systems
[windows]
test gofile="":
  @Write-Host "Testing"
  Set-Location Core
  cargo check
  Set-Location ..
  gotestsum {{gofile}}

# Clean Build Artifacts for Darwin Systems
[linux]
[unix]
[macos]
clean:
  cd Core && cargo clean
  rm -rf Build Lib Include

# Clean Build Artifacts for Windows Systems
[windows]
clean:
  Set-Location Core && cargo clean
  Remove-Item -Path Build, Lib, Include -Recurse -Force -ErrorAction SilentlyContinue

# Setup for installation
setup:
  @echo "Setup Rust"
  rustup target add x86_64-pc-windows-msvc
  rustup target add i686-pc-windows-msvc
  rustup target add aarch64-pc-windows-msvc
  rustup target add x86_64-unknown-linux-gnu
  rustup target add i686-unknown-linux-gnu
  rustup target add aarch64-unknown-linux-gnu
  rustup target add armv7-unknown-linux-gnueabihf
  rustup target add x86_64-apple-darwin
  rustup target add aarch64-apple-darwin

  @echo "Setup GO"
  go mod download
  go install gotest.tools/gotestsum@latest

  @echo ""
  @echo "Setup Done"

