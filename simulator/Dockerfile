FROM ubuntu:20.04

# Install cmake, g++, Qt, libssl, protobuf, git, curl
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq \
        cmake protobuf-compiler libprotobuf-dev qtbase5-dev libqt5opengl5-dev \
        g++ libusb-1.0-0-dev libsdl2-dev libqt5svg5-dev libssl-dev git curl unzip tar

WORKDIR /app

# Clone the simulator
RUN git clone https://github.com/robotics-erlangen/framework.git && \
    cd framework && \
    git checkout b342652846464c4dc789079f5ddb468d8ba3595f

WORKDIR /app/framework

# Build the simulator
RUN export LANG=C.UTF-8 && mkdir build && cd build && LANG=C.UTF-8 cmake .. && LANG=C.UTF-8 make

# Run the simulator
CMD ["./build/bin/simulator-cli", "-g", "2018", "--realism", "None"]
