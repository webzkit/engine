from uuid import uuid4


def generate_unique_name(extension, desired_extension=False):
    unique = uuid4().hex
    # First goes original, second is thumbnail with desiredExtension
    return unique + '.' + extension, unique + '.' + desired_extension if desired_extension else desired_extension
