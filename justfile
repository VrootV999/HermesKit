default: build
[linux]
set shell := ['sh', '-cu']

[windows]
set shell := ["powershell.exe","-c"]

# Build the Project for darwin
[linux]
[macos]
build:
  @echo "Generating C Header with cbindgen..."
  cd Core && cbindgen --lang c --output ../Include/HermesCore.h

  @echo "Building Rust Library (Debug)..."
  cd Core && cargo build

  @echo "Copying static library artifacts..."
  mkdir -p Lib Include
  cp Core/target/debug/libhermes_core.a Lib/

  @echo "Building Go Binary (Debug)..."
  mkdir -p Build/Debug
  go build -o Build/Debug/HermesKit main.go
  @echo "Debug build complete!"

# Build the Project for Windows
[windows]
build:
  @Write-Host "Generating C Header with cbindgen..."
  Set-Location Core
  cbindgen --lang c --output "..\Include\HermesCore.h"
  
  @Write-Host "Building Rust Static Library (Debug)..."
  cargo build
  Set-Location ..

  @Write-Host "Copying static library artifacts..."
  if (!(Test-Path "Lib")) { New-Item -ItemType Directory -Force -Path "Lib" | Out-Null }
  if (!(Test-Path "Include")) { New-Item -ItemType Directory -Force -Path "Include" | Out-Null }

  # Copy-Item "Core\target\debug\hermes_core.lib" "Lib\" -Force

  @Write-Host "Creating build directory..."
  if (!(Test-Path "Build\Debug")) {
    New-Item -ItemType Directory -Force -Path "Build\Debug" | Out-Null
  }

  @Write-Host "Building Go Binary (Debug)..."
  go build -o Build/Debug/HermesKit.exe main.go
  
  @Write-Host "Debug build complete!" -ForegroundColor Green

# Build the Release Version
[linux]
[macos]
release:
  @echo "Generating C Header with cbindgen..."
  cd Core && cbindgen --lang c --output ../Include/HermesCore.h

  @echo "Building Rust Library (Release)..."
  cd Core && cargo build --release

  @echo "Copying static library artifacts..."
  mkdir -p Lib Include
  cp Core/target/release/libhermes_core.a Lib/

  @echo "Building Go Binary (Release)..."
  mkdir -p Build/Release
  go build -o Build/Release/HermesKit main.go
  @echo "Release build complete!"

# Build the Release Version
[windows]
release:
  @Write-Host "Generating C Header with cbindgen..."
  Set-Location Core
  cbindgen --lang c --output "..\Include\HermesCore.h"
  
  @Write-Host "Building Rust Static Library (Release)..."
  cargo build --release
  Set-Location ..

  @Write-Host "Copying static library artifacts..."
  if (!(Test-Path "Lib")) { New-Item -ItemType Directory -Force -Path "Lib" | Out-Null }
  if (!(Test-Path "Include")) { New-Item -ItemType Directory -Force -Path "Include" | Out-Null }

  # Copy-Item "Core\target\debug\hermes_core.lib" "Lib\" -Force

  @Write-Host "Creating build directory..."
  if (!(Test-Path "Build\Release")) { 
      New-Item -ItemType Directory -Force -Path "Build\Release" | Out-Null 
  }

  @Write-Host "Building Go Binary (Release)..."
  go build -o Build/Release/HermesKit.exe main.go
  
  @Write-Host "Release build complete!" -ForegroundColor Green

# Run Tests on Darwin
[linux]
[macos]
test gofile="":
  @echo "Testing"
  cd Core/ && cargo check
  gotestsum {{gofile}}

# Run Tests on Windows
[windows]
test gofile="":
  @Write-Host "Testing"
  Set-Location Core
  cargo check
  Set-Location ..
  gotestsum {{gofile}}
# Clean build artifacts darwin
[linux]
[macos]
clean:
  cd Core && cargo clean
  rm -rf Build Lib Include

# Clean Build artifacts Windows
[windows]
clean:
  Set-Location Core && cargo clean
  Remove-Item -Path Build, Lib, Include -Recurse -Force -ErrorAction SilentlyContinue
