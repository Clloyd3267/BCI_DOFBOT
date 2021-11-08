# Setup Google Protobuf Installation
# For aarch64 Raspberry Pi

# Get Protobuf Compiler
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-aarch_64.zip

# Compile the .proto File
./bin/protoc --python_out=./ ./bci_dofbot_interface.proto

# Install Protobuf using pip
pip install protobuf