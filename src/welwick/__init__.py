import argparse
import logging
import sys
from typing import List

from welwick.welwick import get_version, run

# calculate what version of this program we are running
__version__ = get_version()


def parse_arguments(arguments: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="welwick")

    token_input_group = parser.add_mutually_exclusive_group(required=False)
    token_input_group.add_argument(
        "--token",
        metavar="TOKEN",
        dest="token",
        help="your Mastodon API token",
    )
    token_input_group.add_argument(
        "--token-stdin",
        action="store_true",
        help="your Mastodon API token from stdin",
    )

    parser.add_argument(
        "--api-url",
        metavar="URL",
        help="url of the Mastodon API server",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="send verbose output to the console",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="return the version number and exit",
    )
    return parser.parse_args(arguments)


def main() -> None:
    args = parse_arguments(sys.argv[1:])

    logging.basicConfig(
        format="[%(asctime)s] %(levelname)-8s - %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
        stream=sys.stdout,
    )

    run(
        args.token,
        args.token_stdin,
        args.api_url,
    )


if __name__ == "__main__":
    main()
