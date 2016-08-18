"""Contains helper methods to create tempfiles for tests."""
import tempfile


def create_temp_file(content, extension):
    """
    Create a temp file with some content and extension.

    params:
        content (obj): file content to write
        extension (str): file extension preceded by a dot

    returns:
        file's name

    """
    temp_file = declare_temp_file(extension)
    with open(temp_file, mode='wb') as f:
        f.write(content)

    return temp_file


def declare_temp_file(extension):
    """
    Create an empty temp file.

    params: see self.create_temp_file
    returns: see self.create_temp_file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    return temp_file.name
