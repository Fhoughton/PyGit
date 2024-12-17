# PyGit: A Git Client in Python
**PyGit** is a lightweight Git client written in Python. It was written to strengthen my understanding of how Git works under the hood by exploring its internals. You can read about its development [here](https://fhoughton.github.io/git/python/2024/07/27/week3-github-part1.html).

## Supported Commands
Currently, PyGit supports the following Git commands:

- `init`
- `log`
- `cat-file`
- `hash-object`

---

## How Git/PyGit Works Internally
### Git Init: The Core of a Git Repository
The `init` command creates a new Git repository, with the following structure:

- **The `.git` Folder**: Contains all repository files.
- **Key Folders**:
  - `branches`
  - `objects`
  - `refs`
- **Description File**: A description of the git repo (usually unused)
- **HEAD File**: Specifies the repository's head pathspec (e.g., `ref: refs/heads/master` by default).
- **Config File**: Specifies repository details such as the Git version format.

### Git Objects: Structure and Functionality
Git stores repository information using four types of objects:
1. **Blob**: Raw file data (e.g., the contents of `main.c`).
2. **Commit**: Metadata about a commit.
3. **Tag**: A named reference to a specific commit or object, including tag date and creator.
4. **Tree**: Relates files to directories.

Git objects are compressed using `zlib`. Once decompressed, they follow this format:
- **Header**: Identifies the object type (e.g., `blob`, `commit`).
- **Size**: Object size in ASCII text.
- **Data**: The actual object contents (e.g., file data, commit metadata).

---

## Learning Resources
Development of PyGit was guided by two key resources:

- [Official Git Documentation](https://git-scm.com/doc): An invaluable source for understanding Git's internals, including the structure of Git objects.
- [Write Yourself a Git](https://wyag.thb.lt/): A step-by-step guide for building your own Git client, particularly helpful for parsing Git objects.
