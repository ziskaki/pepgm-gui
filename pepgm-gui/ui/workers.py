from pathlib import Path
import numpy as np


def get_absolute_file_path(*path_components):
    """ Get absolute file path, given the script path."""
    script_dir = Path(__file__).resolve().parent
    absolute_path = script_dir.parent / Path(*path_components)
    return absolute_path.as_posix()


def get_float_range(start, end, step):
    """ Generate a list of numbers with a given range and step size."""
    return np.round(np.arange(start, end + step, step), 2).tolist()


def get_form_value(request, field_name, default_value=str()):
    """ Get form value from a text input field. """
    value = request.form.get(field_name)
    return value if value else default_value


def get_file_path_from_form(request, field_name):
    """ Get form value from a file upload field. """
    file_name = request.files[field_name].filename
    search_directory = Path(__file__).resolve().parents[1]
    matching_files = str(list(search_directory.glob('**/' + file_name))[0])

    return matching_files


