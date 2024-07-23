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

cat_parser = commands_parser.add_parser("cat-file")
cat_parser.add_argument("type", metavar="type", choices=["blob", "commit", "tag", "tree"])
cat_parser.add_argument("object", metavar="object")

if __name__ == "__main__":
    args = parser.parse_args(sys.argv[1:])
    match args.command:
        case "init":
            GitRepo(args.path, create=True)
        case "add":
            pass
        case "cat-file":
            repo = GitRepo(".")
            repo.cat_file(args.object, args.type.encode())
        case _:
            print(f"Unrecognized git command '{args.commands}'")