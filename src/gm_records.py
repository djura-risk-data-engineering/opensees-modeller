from pathlib import Path
from typing import List, Tuple
import os
from .utilities import create_path
import numpy as np


def get_ground_motion(path: Path, filenames: List[Path]) -> Tuple[np.array]:
    """Get ground motions

    Parameters
    ----------
    path : Path
        Path of ground motion files
    filenames : List[Path]
        List of length 2 or 3 (2 for 2D analysis, 3 for 3D analysis)
            List contains path to the following:
                File containing the names of the ground motion files in
                1st direction
                Optional, file containing the names of the ground motion files
                in 2nd direction
                File containing the time steps of the ground motion records

    Returns
    -------
    Tuple containing
        np.arrays of
            Names of ground motions in 1st direction
            Names of ground motions in 2nd direction
            Time steps of ground motions
    """
    names_y = None

    if len(filenames) == 2:
        # 2D modelling, a single direction of a
        # ground motion record is provided
        names_x = np.loadtxt(path / filenames[0], dtype="str", ndmin=1)
        dts_list = np.loadtxt(path / filenames[1], ndmin=1)
    else:
        names_x = np.loadtxt(path / filenames[0], dtype="str", ndmin=1)
        names_y = np.loadtxt(path / filenames[1], dtype="str", ndmin=1)
        dts_list = np.loadtxt(path / filenames[2], ndmin=1)

    try:
        dts_list = [float(dts_list)]
    except Exception:
        dts_list = list(dts_list)

    return names_x, names_y, dts_list


def get_ground_motion_batches(gm_folder: Path) -> List[str]:
    """Inside the main ground motion directory associated with MSA
    look for subdirectories associated with each intensity level
    (return period)

    Parameters
    ----------
    gm_folder : Path
        Main directory

    Returns
    -------
    List[str]
        Names of ground motion subdirectories
    """
    return next(os.walk(gm_folder))[1]


def get_records(gm_folder: Path, filenames: List[Path],
                output_dir: Path = None):
    """Gets records for multiprocessing and creates directories for exporting
    analysis results at a later stage

    Parameters
    ----------
    gm_folder : Path
        Path of ground motion records
    filenames : List[Path]
        Filenames of ground motion records
    output_dir : Path, optional
        Output directory for MSA results, by default None

    Returns
    -------
    RecordBatchModel (TODO)
        Ground Motion record sets for MSA
    """
    # Get the ground motion set information
    gm_paths = get_ground_motion_batches(gm_folder)

    # Records in batches for multiprocessing
    records = {}

    # Set up directories to export MSA outputs for each batch of records
    for sub_path in gm_paths:
        if output_dir is not None:
            create_path(output_dir / sub_path)

        # Get the ground motion information
        names_x, names_y, dts_list = get_ground_motion(
            gm_folder / sub_path, filenames)
        records[sub_path] = {"X": list(names_x), "Y": list(
            names_y), "dt": list(dts_list)}

    return records
