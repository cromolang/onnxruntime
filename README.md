# ONNX Runtime for Cromo

Run models in the [ONNX](https://onnx.ai) format from a [Cromo](https://cromolang.org) program, with [ONNX Runtime](https://onnxruntime.ai).

```sh
cromo get github.com/cromolang/onnxruntime
```

```cromo
import onnxruntime

i32 main() {
    onnxruntime.Session model = onnxruntime.load("linear.onnx")
    list<f32> x = [1.0, 2.0, 3.0, 4.0]
    list<onnxruntime.Tensor> out = model.run([onnxruntime.Tensor([1, 4], x)])
    println("{:?} {:?}", out[0].shape, out[0].data)   // [1, 3] [4.85, 3.8, 4.55]
    ret 0
}
```

There is nothing else to install. The library of ONNX Runtime is the one that Microsoft publishes: `cromo` downloads it the first time the program is built, checks it by its hash, and puts it next to the executable, `onnxruntime.dll` on Windows and `libonnxruntime.so.1` on Linux. A program is given to others with that file next to it.

## What it has

- `onnxruntime.load(path)` reads a model from a file, and `onnxruntime.Session(bytes)` from its bytes, as those of `embed("model.onnx")`, which puts the model inside the program.
- `session.inputNames()` and `session.outputNames()` are the names of the inputs and of the outputs of the model, in their order.
- `session.run(inputs)` takes a tensor for each input and gives one for each output.
- `onnxruntime.Tensor(shape, data)` is numbers with a shape: `shape` the size of each dimension, `data` the numbers row after row.
- `onnxruntime.version()` is the version of ONNX Runtime in use.

What ONNX Runtime refuses, as a file that is not a model or an input of the wrong shape, is an `Error` with its message.

## Limits of this version

- The tensors are of `f32`. A model with an input or an output of another type is refused.
- The models run on the processor: no GPU.
- Windows and Linux on x86-64. Android, Linux on ARM64 and macOS come later.
- Linux needs glibc 2.29 or later, and the C++ library of the system (`libstdc++`), which the distributions have.

## The versions

| This package | ONNX Runtime | Cromo |
|---|---|---|
| v0.1.0 | 1.32.0 | 0.90 or later |

## Developing it

```sh
cromo test onnxruntime.cro          # its tests
python tools/model.py testdata/linear.onnx   # writes the model of the tests again
python tools/table.py <onnxruntime_c_api.h>  # the places of the functions in the table of the C API
```

The module calls the C API of ONNX Runtime through its table of functions, each by its place in the table, which only grows at its end from one version to the next. `tools/table.py` reads the places from the header of a version.

## License

MIT, as ONNX Runtime: see `LICENSE`. ONNX Runtime is a work of Microsoft and of its contributors; its license and its notices are in the archives that it publishes.
