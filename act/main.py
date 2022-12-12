import sys
import os
import argparse

from act.logging.logger import information_logger, error_logger
from act.requests.User import User


def exists(filepath: str):
    return os.path.isfile(filepath)


def parse_options():
    """Parser argument options."""
    parser = argparse.ArgumentParser(
        description="act requires config.toml with -f argument"
    )
    parser.add_argument(
        "-f", dest="file", action="store", required=False, help="Login email"
    )

    parser.add_argument("--v", action="version", version="0.1")
    return parser


def main():
    """started act"""
    try:
        parser = parse_options()
        argvs = sys.argv
        if len(argvs) <= 1:
            parser.print_help()
            sys.exit(1)
        args = parser.parse_args()
        if not exists(args.file):
            error_logger("file not found")
            return

        victim = User("victim", args.file)
        victim.login()
        attacker = User("attacker", args.file)
        attacker.login()
        attacker.request_target()
        victim.request_target()

    except (RuntimeError, KeyboardInterrupt) as ex:
        sys.stderr.write(f"{ex}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
