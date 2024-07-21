import sys
import argparse
from repo import GitRepo

parser = argparse.ArgumentParser(
    prog="Pygit", description="A simple git client written in Python"
)
commands_parser = parser.add_subparsers(title="Commands", dest="command")
commands_parser.required = True

init_parser = commands_parser.add_parser("init")
init_parser.add_argument("path", metavar="directory", nargs="?", default=".")

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    match args.command:
        case "init":
            GitRepo(args.path, create=True)
            pass
        case "add":
            pass
        case _:
            print(f"Unrecognized git command '{args.commands}'")
