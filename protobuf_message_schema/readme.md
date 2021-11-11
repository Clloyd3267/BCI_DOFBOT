# Setup Google Protobuf Installation
# For aarch64 Raspberry Pi

# Get Protobuf Compiler
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-aarch_64.zip

# Compile the .proto File
./bin/protoc --python_out=./ ./bci_dofbot_interface.proto

# Install Protobuf using pip
pip install protobuf

# Windows

# Download and extract the compiler to the "BCI_DOFBOT/protobuf_message_schema/" folder
https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-win64.zip

# Open a command prompt in the extracted folder "protoc-3.19.1-win64/" and run the following command
# Replace <SRC_FOLDER> with either "headset_server_src" or "dofbot_client_src" depending on whether on the server or client
./bin/protoc.exe --python_out=../../<SRC_FOLDER>/ --proto_path=../ ../bci_dofbot_interface.proto