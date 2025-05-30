"""
Tests the Inscriptis CLI client.
"""

from io import StringIO
from json import loads
from pathlib import Path
from unittest.mock import Mock, call, mock_open, patch

import pytest

from inscriptis.cli.inscript import cli

INPUT_DATA = """<html><body>Hello <b>World</b>!</body></html>"""


def test_cli_read_from_stdin(monkeypatch, capsys):
    """Test converting HTML from standard input with the command line client."""
    # Use monkeypatch to replace the 'input' function
    monkeypatch.setattr("sys.argv", ["inscript"])
    monkeypatch.setattr("sys.stdin", StringIO(INPUT_DATA))
    cli()

    # Capture the printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World!"


def test_cli_read_from_stdin_write_to_file(monkeypatch, capsys):
    """Test converting HTML from standard input with the command line client and
    writing it to a file."""
    # Use monkeypatch to replace the 'input' function
    monkeypatch.setattr("sys.argv", ["inscript", "--output", "test.txt"])
    monkeypatch.setattr("sys.stdin", StringIO(INPUT_DATA))
    with patch("pathlib.Path.open", create=True) as mock_file:
        cli()

    # Capture the printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == ""
    # Capture the test written to the mock output file
    assert call().__enter__().write("Hello World!") in mock_file.mock_calls


def test_cli_read_from_file(monkeypatch, capsys):
    """Test converting HTML from a file with the command line client."""
    # Use monkeypatch to replace the 'input' function
    monkeypatch.setattr("sys.argv", ["inscript", "test.html"])
    monkeypatch.setattr("pathlib.Path.is_file", lambda _: True)
    monkeypatch.setattr("pathlib.Path.open", mock_open(read_data=INPUT_DATA))
    cli()

    # Capture the printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World!"


def test_cli_read_from_url(monkeypatch, capsys):
    """Test converting HTML from an URL with the command line client."""
    # Use monkeypatch to replace the 'input' function
    monkeypatch.setattr("sys.argv", ["inscript", "https://www.fhgr.ch/test.html"])

    mock_request = Mock()
    mock_request.content = INPUT_DATA.encode("utf8")
    mock_request.encoding = "utf-8"
    monkeypatch.setattr("requests.get", lambda url, timeout=0: mock_request)
    cli()

    # Capture the printed output
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World!"


def test_cli_annotations(monkeypatch, capsys):
    """Test annotation handling in the command line client."""
    # Prepare input data for the test
    annotation_rule_path = Path(__file__).parent / "data" / "annotation-profile-unittest.json"

    # Use monkeypatch to replace the 'input' function
    monkeypatch.setattr("sys.argv", ["inscript", "-p", "surface", "-r", str(annotation_rule_path)])
    monkeypatch.setattr("sys.stdin", StringIO(INPUT_DATA))
    cli()

    # Capture the printed json data and convert it to an object
    captured = loads(capsys.readouterr().out.strip())
    assert captured["text"].strip() == "Hello World!"
    assert captured["label"] == [[6, 11, "emphasis"]]
    assert captured["surface"] == [["emphasis", "World"]]


def test_help(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inscript", "--version"])

    # the cli should exit with exit code 0
    with pytest.raises(SystemExit) as exit_info:
        cli()
    assert exit_info.value.code == 0

    captured = capsys.readouterr().out
    assert captured.startswith("Inscript HTML to text conversion")
    assert "Inscript comes with ABSOLUTELY NO WARRANTY." in captured


def test_missing_input_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inscript", "test.html"])
    with pytest.raises(SystemExit) as exit_info:
        cli()

    captured = capsys.readouterr()
    assert exit_info.value.code == -1
    assert captured.out.strip().startswith("ERROR: Cannot open input file")


def test_missing_annotation_file(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["inscript", "--annotation-rules", "rules.json"])
    monkeypatch.setattr("sys.stdin", StringIO(INPUT_DATA))
    with pytest.raises(SystemExit) as exit_info:
        cli()

    captured = capsys.readouterr()
    assert exit_info.value.code == -1
    assert captured.out.strip().startswith("ERROR: Cannot open annotation rule file")
