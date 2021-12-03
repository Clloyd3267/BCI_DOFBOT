# Setup Google Protobuf Installation

# Install Protobuf using pip
```bash
pip install protobuf
```

# For aarch64 Raspberry Pi Linux

```bash
# Change dir to the protobuf folder
cd BCI_DOFBOT/protobuf_message_schema/

# Get the compiler zip file and unzip it
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-aarch_64.zip
unzip protoc-3.19.1-linux-aarch_64.zip -d protoc-3.19.1-linux-aarch_64

# Compile protobuf file to client folder
cd protoc-3.19.1-linux-aarch_64
./bin/protoc --python_out=../../dofbot_client_src/ --proto_path=../ ../bci_dofbot_interface.proto
```

# Windows

# Download and extract the compiler to the "BCI_DOFBOT/protobuf_message_schema/" folder
https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-win64.zip

# Open a command prompt in the extracted folder "protoc-3.19.1-win64/" and run the following command
```bash
./bin/protoc.exe --python_out=../../headset_server_src/ --proto_path=../ ../bci_dofbot_interface.proto
```
