import contextlib
from sys import stdin

import pytest

import pepe


@pytest.mark.parametrize('column, expected', (
    (None, ["hello world"]),
    (0, ["hello world"]),
    (1, ["hello"]),
))
def test_read(monkeypatch, column, expected):
    def mock_read():
        return "hello world"

    monkeypatch.setattr(stdin, "read", mock_read)
    assert pepe.read(column) == expected


def test_out(monkeypatch, capsys):
    def mock_read():
        return "hello world"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.out()
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"


def test_sum(monkeypatch, capsys):
    def mock_read():
        return "1\n2\n3"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.sum()
    captured = capsys.readouterr()
    assert captured.out == "6\n"


def test_sort(monkeypatch, capsys):
    def mock_read():
        return "3\n1\n2"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.sort()
    captured = capsys.readouterr()
    assert captured.out == "1\n2\n3\n"


def test_min(monkeypatch, capsys):
    def mock_read():
        return "3\n1\n2"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.min()
    captured = capsys.readouterr()
    assert captured.out == "1\n"


def test_max(monkeypatch, capsys):
    def mock_read():
        return "3\n1\n2"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.max()
    captured = capsys.readouterr()
    assert captured.out == "3\n"


@pytest.mark.parametrize('retval, args, expected', (
    ("1", ["kb", "b"], "1024.0\n"),
    ("1\n2", ["kb", "b"], SystemExit),
    ("1", ["xxx", "b"], SystemExit),
    ("1", ["b", "xxx"], SystemExit),
))
def test_size(monkeypatch, capsys, retval, args, expected):
    monkeypatch.setattr(stdin, "read", lambda: retval)

    try:
        pepe.size(*args)
    except SystemExit:
        captured = capsys.readouterr()
        assert expected == SystemExit
    else:
        captured = capsys.readouterr()
        assert captured.out == expected


def test_count(monkeypatch, capsys):
    def mock_read():
        return "1\n1\n1"

    monkeypatch.setattr(stdin, "read", mock_read)
    pepe.count()
    captured = capsys.readouterr()
    assert captured.out == "3\n"


def test_help(capsys):
    from pepe.main import _help

    with contextlib.suppress(SystemExit):
        _help()

    captured = capsys.readouterr()
    assert 'pipeline helper' in captured.out


@pytest.mark.parametrize('override_args, expected_out', (
    ([], 'pipeline helper'),
    (['wrong'], 'pipeline helper'),
    (['count'], '3'),
    (['sort', '0', 'true'], '1\n1\n1'),
    (['sort', '0', 'false'], '1\n1\n1'),
    (['sort', 'xxx'], 'pipeline helper'),  # means error
))
def test_cli(monkeypatch, capsys, override_args, expected_out):
    from pepe.main import _cli

    monkeypatch.setattr(stdin, "read", lambda: "1\n1\n1")

    with contextlib.suppress(SystemExit):
        _cli(override_args=override_args)

    captured = capsys.readouterr()
    assert expected_out in captured.out
