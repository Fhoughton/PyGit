import os


class GitRepo:
    """Represents a git repository (working tree and git directory)"""

    def __init__(self, path, create=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if create:
            # Make the git paths if not already present
            if not os.path.exists(self.worktree):
                os.makedirs(self.worktree)

            if not os.path.exists(self.gitdir):
                os.makedirs(self.gitdir)

            # Make the key .git paths
            self.gitdir_path("branches", mkdir=True)
            self.gitdir_path("objects", mkdir=True)
            self.gitdir_path("refs", mkdir=True)
            self.gitdir_path("refs", "tags", mkdir=True)
            self.gitdir_path("refs", "heads", mkdir=True)

            # Add the git description
            with open(self.gitdir_path("description"), "w") as desc:
                desc.write(
                    "Unnamed repository; edit this file 'description' to name the repository.\n"
                )

            # Establish the head
            with open(self.gitdir_path("HEAD"), "w") as head:
                head.write("ref: refs/heads/master\n")

            # Write the default config
            with open(self.gitdir_path("config"), "w") as config:
                config_data = """[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
"""
                config.write(config_data)

    def gitdir_path(self, *path, mkdir=False):
        """Gets a path relative to .git (for finding objects), *path is variadic so can handle multiple path elements, if mkdir creates path"""
        resolved_path = os.path.join(self.gitdir, *path)

        if mkdir:
            os.mkdir(resolved_path)

        return resolved_path
