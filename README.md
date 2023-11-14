[![pypi](https://img.shields.io/pypi/v/py-pepe.svg)](https://pypi.org/project/py-pepe/)
[![pypi](https://img.shields.io/pypi/pyversions/py-pepe.svg)](https://pypi.org/project/py-pepe/)
[![pypi](https://img.shields.io/pypi/l/py-pepe.svg)](https://raw.githubusercontent.com/deniskrumko/py-pepe/master/LICENSE)

# py-pepe

Super simple pipeline helper on Python. Works like `awk` but easier to remember (and also less posibilities...).

PEPE can work in 2 different ways:

### 1. As python module

Don't remember `awk` commands? Not a problem! Just insert python script here and read result of previous
command using `pepe.read()`. Additionally, you can select N column (like column 6 in example):

```bash
# Show max usage RAM from process
ps ux | python -c "import pepe; x=pepe.read(6); print(max(x[1:]))"
```

### 2. As CLI

Don't want to call python scripts like that? We got you a CLI tool too!

CLI interface totally mimics python functions usage:

```bash
# Show total RAM usage of Visual Studio Code process
ps ux | grep "Visual Studio Code" | pepe sum 6
```

Here you add `pepe sum 6` in pipe. That's identical to `import pepe; pepe.sum(6)`. Same args and same positions.
That's why if you want to sort lines as numbers, you need to add 0 positional arg: `pepe sort 0 true`,
because that's identical to `pepe.sort(0, True)`.

CLI doesn't have any flags, only positional args. That's for simplicity.

# Installation

```bash
pip install py-pepe
```

# Functions/Example of usage

## help
To show help just call `pepe` command in terminal.
Also on each error in input you probably will see pepe help.

## `pepe.read`

Python-code only function (no cli). Reads all stdin and returns list of lines.

**NOTE:** This is the only function in pepe that returns a value. All other function just print their results.

Optional positional params:
    - `<column>` - select only N column
```bash
# Show max usage RAM from process
ps ux | python -c "import pepe; x=pepe.read(6); print(max(x[1:]))"
```

## `pepe.out`

Display result. Works like `cat` or `echo`, but can select column.

Optional positional params:
    - `<column>` - select only N column

```bash
# Display only 1 column of ps ux
ps ux | head -n 10 | pepe out 1

# Same, but using python code
ps ux | head -n 10 | python -c "import pepe; pepe.out(1)"

# Without pepe
ps ux | head -n 10 | awk '{ print $1 }'
```

## `pepe.sum`

Command `sum` allows to sum lines as numbers.

Optional positional params:
    - `<column>` - select only N column

Let's count RAM usage of all VSCode processes (on mac). Column 6 of "ps ux" output contains info about RAM:
```bash
# Select column 6 and sum
ps ux | grep "Visual Studio Code" | pepe sum 6

# Select column 6 using awk and sum all lines
ps ux | grep "Visual Studio Code" | awk '{ print $6 }' | pepe sum

# Same, but using python code
ps ux | grep "Visual Studio Code" | python -c "import pepe; pepe.sum(6)"

# Without pepe
ps ux | grep "Visual Studio Code" | awk '{sum+=$6} END {print sum}'
```

## `pepe.sort`
## `pepe.min`
## `pepe.max`
## `pepe.size`
## `pepe.count`
