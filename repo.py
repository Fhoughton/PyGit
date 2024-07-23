import os
import zlib
import hashlib


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

    def read_object(self, hash):
        """Reads a git object from its hash and returns it"""
        object_path = self.gitdir_path(
            "objects", hash[0:2], hash[2:]
        )  # sha [0:2] as first 2 characters of hash are folder name, then rest file name

        with open(object_path, "rb") as object_bin:
            object_data = zlib.decompress(
                object_bin.read()
            )  # By default git objects are compressed

            # Git object headers begin with the name e.g. blob and then a space, so we find the space first
            space_index = object_data.find(b" ")
            object_type = object_data[0:space_index]

            # After the space is the object size followed by a null byte (0x00)
            null_index = object_data.find(
                b"\x00", space_index
            )  # Start searching after the space, technically not needed

            object_size = int(object_data[space_index:null_index].decode("ascii"))

            # Construct a class based upon what object type it is
            match object_type:
                case b"commit":
                    pass
                case b"blob":
                    pass
                case b"tree":
                    pass
                case b"tag":
                    pass
                case _:
                    raise Exception(
                        f"Unrecognized object type for {hash}, found '{object_type}' not commit, blob, tree or tag"
                    )

    def write_object(self, obj):
        """Writes a GitObject's data to the correct path and file, formatted correctly"""
        # Get the object as useable bytes
        object_data = obj.serialize()

        # Construct the object header
        object_data = (
            obj.get_name()
            + b" "
            + str(len(object_data)).encode()
            + b"\x00"
            + object_data
        )

        # Hash the object
        object_hash = hashlib.sha1(object_data).hexdigest()

        # Resolve the path for the object to be stored in
        object_path = self.gitdir_path(
            "objects", object_hash[0:2], object_hash[2:], mkdir=True
        )

        # Write the object data to the file
        with open(object_path, "wb") as object_file:
            object_file.write(zlib.compress(object_data))

        # Return the hash to expose a reference for the new object
        return object_hash
    
    def find_object(self, name, fmt=None, follow=True):
        return name

    def cat_file(self, obj, fmt):
        obj = self.read_object(self.find_object(obj, fmt=fmt))
        sys.stdout.buffer.write(obj.serialize())
