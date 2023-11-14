import sys
from signal import (
    SIG_DFL,
    SIGPIPE,
    signal,
)
from typing import (
    Callable,
    Dict,
    List,
    Optional,
)

signal(SIGPIPE, SIG_DFL)

_sum = sum
_min = min
_max = max


def read(column: Optional[int] = None) -> List[str]:
    """Read lines from stdin."""
    lines = str(sys.stdin.read()).splitlines()

    if column is None or column == 0:
        return lines

    # Return only N - 1 column (index starts from 1, like awk)
    return [line.split()[column - 1] for line in lines]


def out(column: Optional[int] = None) -> None:
    """Display output."""
    print("\n".join(read(column)))


def sum(column: Optional[int] = None) -> None:
    """Sum numbers."""
    print(_sum([int(v) for v in read(column)]))


def sort(column: Optional[int] = None, num: bool = False) -> None:
    """Sort lines."""
    print("\n".join(sorted(read(column), key=int if num else str)))


def min(column: Optional[int] = None) -> None:
    """Show min."""
    print(_min([int(v) for v in read(column)]))


def max(column: Optional[int] = None) -> None:
    """Show max."""
    print(_max([int(v) for v in read(column)]))


def size(from_size: str, to_size: str) -> None:
    """Convert sizes like kb to mb and so on."""
    value = read()
    if len(value) != 1:
        print(f'pepe size: too many input values ({len(value)}), expected 1')
        sys.exit(1)

    from_size = from_size.lower()
    to_size = to_size.lower()
    sizes = {
        'b': 1,
        'kb': 1024,
        'mb': 1024 * 1024,
        'gb': 1024 * 1024 * 1024,
    }
    if from_size not in sizes:
        print(f'pepe size: wrong size ({from_size}), expected one of {list(sizes.keys())}')
        sys.exit(1)
    if to_size not in sizes:
        print(f'pepe size: wrong size ({to_size}), expected one of {list(sizes.keys())}')
        sys.exit(1)

    print(round(int(value[0]) * sizes[from_size] / sizes[to_size], 3))


def count() -> None:
    """Count lines."""
    print(len(read()))


def _help() -> None:
    print('''
\033[1m========= PEPE - pipeline helper =========\033[0m

\033[92mpepe out <column>\033[0m - print lines
    pepe out - print whole line
    pepe out 1 - print first column only

\033[92mpepe sum <column>\033[0m - sum numbers (only!)
    pepe sum - sum whole line
    pepe sum 1 - sum first column only

\033[92mpepe sort <column> <numeric>\033[0m - sort lines
    pepe sort 1 - select first column, sort like string
    pepe sort 0 true - select whole line, sort like numberic

\033[92mpepe min <column>\033[0m - show min of numbers
    pepe min - show min of whole line
    pepe min 1 - show min of first column

\033[92mpepe max <column>\033[0m - show max of numbers
    pepe max - show max of whole line
    pepe max 1 - show max of first column

\033[92mpepe size <from> <to>\033[0m - convert size
    pepe kb gb - convert KB to GB

\033[92mpepe count\033[0m - count lines

=============================================

Also you can use pepe as a library from python code. For example:

    ps ux | python -c "import pepe; pepe.sum(6)"

More examples here: https://github.com/deniskrumko/py-pepe/blob/master/README.md''')
    sys.exit(1)


def _cli(override_args: Optional[List[str]] = None) -> None:
    """Command line interface.

    Example of use:

        # Show RAM usage of Chrome processes
        ps ux | grep Chrome | pepe sum 6

        # Count lines in file
        cat main.py | pepe count
    """
    args = sys.argv[1:] if override_args is None else override_args

    if len(args) == 0:
        _help()

    command = args[0]
    args = args[1:]

    commands_map: Dict[str, Callable] = {
        'count': count,
        'max': max,
        'min': min,
        'out': out,
        'size': size,
        'sort': sort,
        'sum': sum,
    }

    if command not in commands_map:
        print(f'pepe: unknown command ({command})')
        _help()

    for i, arg in enumerate(args[:]):  # Because we need to modify args
        if arg.isdigit():
            args[i] = int(arg)  # type: ignore
        if arg.lower() == 'true':
            args[i] = True  # type: ignore
        if arg.lower() == 'false':
            args[i] = False  # type: ignore

    try:
        commands_map[command](*args)
    except Exception as e:
        print(f'pepe: error while executing command {command}:\n{e!r}')
        _help()
