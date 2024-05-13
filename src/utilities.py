import json
import pickle
import numpy as np
from pathlib import Path


def append_record(x, y):
    """Record selection issue related to the database of records
    whereby the two pairs of the records have different sizes
    To remedy the issue, the smallest of the records is appended with zeros

    Parameters
    ----------
    x : List
    y : List

    Returns
    -------
    List List
    """
    nx = len(x)
    ny = len(y)

    if nx < ny:
        x = np.append(x, np.zeros(ny - nx))
    if ny < nx:
        y = np.append(y, np.zeros(nx - ny))
    return x, y


def create_path(directory: Path):
    """Create a folder if it does not exist

    Parameters
    ----------
    directory : Path
        Directory to be created
    """
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        print("Error: Creating directory. ", directory)


def find_nearest(array, value: float):
    """Find index of nearest value in array

    Parameters
    ----------
    array : List
    value : float

    Returns
    -------
    List[int]
        Index of nearest value
    """
    value = np.asarray(value)
    array = np.asarray(array)
    idx = np.abs(array - value[:, np.newaxis]).argmin(axis=1)
    return idx


def read_text(name, usecols=None) -> np.array:
    """Reads a text file

    Parameters
    ----------
    name : str
        Filename
    usecols : sequence, optional
        Which columns to read, with 0 being the first.  For example,
        ``usecols = (1, 4, 5)`` will extract the 2nd, 5th and 6th columns.
        by default, None

    Returns
    -------
    np.array
        Content of file
    """
    return np.genfromtxt(name, invalid_raise=False, usecols=usecols)


def remove_directory_contents(directory: Path):
    if not directory.exists():
        return

    for item in directory.glob('*'):
        if item.is_file():
            item.unlink()
        else:
            item.rmdir()

    directory.rmdir()


def to_json_serializable(data):
    if isinstance(data, dict):
        for key, value in data.items():
            data[key] = to_json_serializable(value)
    elif isinstance(data, list):
        return [to_json_serializable(item) for item in data]
    elif isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, np.float_):
        return float(data)
    elif isinstance(data, np.float32):
        return float(data)
    elif isinstance(data, np.int32):
        return float(data)
    return data


def export_results(filepath: Path, data, filetype: str):
    """Exports results to file

    Parameters
    ----------
    filepath : Path
        Path where to export data to
    data : any
        Data to be stored
    filetype : str
        Filetype, e.g. npy, json, pkl, csv
    """
    if filetype == "json":
        data = to_json_serializable(data)

    if filetype == "npy":
        np.save(f"{filepath}.npy", data)
    elif filetype == "pkl" or filetype == "pickle":
        with open(f"{filepath}.pickle", 'wb') as handle:
            pickle.dump(data, handle)
    elif filetype == "json":
        with open(f"{filepath}.json", "w") as json_file:
            json.dump(data, json_file)
    elif filetype == "csv":
        data.to_csv(f"{filepath}.csv", index=False)


def read_pickle(path):
    with open(path, 'rb') as file:
        data = pickle.load(file)
    return data
