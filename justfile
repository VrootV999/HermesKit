# Build the Project
build:
  @echo "Building Debug Build"
  @go build -o Build/Debug/HermesKit

# Build the Release Version
release:
  @echo "Building Release Build"
  @go build -ldflags="-s -w" -o Build/Release/HermesKit

# Run Tests
test file="":
  @echo "Testing"
  @gotestsum {{file}}

