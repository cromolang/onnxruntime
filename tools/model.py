"""Writes a small model of ONNX by hand, without the package onnx: y = Relu(x * W + b),
with x of 1 by 4 and y of 1 by 3, and scores = Softmax(y). Its bytes are the messages of
protobuf of onnx.proto, written here field by field.

    python model.py linear.onnx
"""
import struct
import sys


def varint(n):
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def field(number, wire, payload):
    return varint(number << 3 | wire) + payload


def integer(number, value):
    return field(number, 0, varint(value))


def text(number, value):
    data = value.encode() if isinstance(value, str) else value
    return field(number, 2, varint(len(data)) + data)


def tensor(name, dims, values):
    out = b''.join(integer(1, d) for d in dims)
    out += integer(2, 1)  # FLOAT
    out += text(8, name)
    out += text(9, struct.pack('<%df' % len(values), *values))  # raw_data
    return out


def value_info(name, dims):
    shape = b''.join(text(1, integer(1, d)) for d in dims)
    tensor_type = integer(1, 1) + text(2, shape)
    return text(1, name) + text(2, text(1, tensor_type))


def node(op, inputs, outputs, name):
    out = b''.join(text(1, i) for i in inputs)
    out += b''.join(text(2, o) for o in outputs)
    out += text(3, name) + text(4, op)
    return out


W = [0.5, -1.0, 0.25,
     1.0, 0.5, -0.5,
     -0.25, 2.0, 1.0,
     0.75, -0.5, 0.5]
B = [0.1, -0.2, 0.3]
graph = text(1, node('Gemm', ['x', 'W', 'b'], ['sum'], 'gemm'))
graph += text(1, node('Relu', ['sum'], ['y'], 'relu'))
graph += text(1, node('Softmax', ['y'], ['scores'], 'softmax'))
graph += text(2, 'linear')
graph += text(5, tensor('W', [4, 3], W))
graph += text(5, tensor('b', [3], B))
graph += text(11, value_info('x', [1, 4]))
graph += text(12, value_info('y', [1, 3]))
graph += text(12, value_info('scores', [1, 3]))
model = integer(1, 8) + text(2, 'cromo') + text(7, graph) + text(8, text(1, '') + integer(2, 13))
open(sys.argv[1], 'wb').write(model)
print(len(model), 'bytes')
