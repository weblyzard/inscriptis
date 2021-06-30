from inscriptis.metadata import (__author__, __author_email__, __copyright__,
                                 __license__, __version__)


def test_metadata():
    """Test inscriptis package metadata."""
    assert 'Albert Weichselbraun' in __author__
    assert 'Fabian Odoni' in __author__

    assert '@' in __author_email__

    assert '2016-' in __copyright__
    assert 'Albert Weichselbraun' in __copyright__
    assert 'Fabian Odoni' in __copyright__

    assert __license__ == 'Apache 2.0'

    assert __version__[0].isnumeric()
    assert '.' in __version__
