import sys
import argparse

parser = argparse.ArgumentParser(
    prog="Pygit", description="A simple git client written in Python"
)
parser.add_argument("command", choices=["init", "add"])

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    match args.command:
        case "init":
            pass
        case "add":
            pass
        case _:
            print(f"Unrecognized git command '{args.commands}'")
