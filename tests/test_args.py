import welwick


def test_valid_values():
    x = welwick.parse_arguments(
        [
            "--token-stdin",
            "--api-url",
            "https://uncontrollablegas.com/",
        ],
    )
    assert not x.verbose
    assert x.api_url == "https://uncontrollablegas.com/"
    assert x.token_stdin
    assert x.token is None

    x = welwick.parse_arguments(
        [
            "--token",
            "asdf",
            "--api-url",
            "https://uncontrollablegas.com/",
        ],
    )
    assert not x.verbose
    assert x.api_url == "https://uncontrollablegas.com/"
    assert not x.token_stdin
    assert x.token == "asdf"  # noqa: S105
