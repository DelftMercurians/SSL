#!/bin/sh
protoc --plugin=protoc-gen-mypy=$(poetry env info -p)/bin/protoc-gen-mypy --python_out=../protobuf/ --mypy_out=../protobuf/ *.proto

