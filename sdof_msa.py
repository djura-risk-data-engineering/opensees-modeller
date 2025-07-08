from pathlib import Path
import numpy as np
from src.sdof.msa import run_sdof
from src.utilities import export_results
import json
import zipfile

__filepath__ = Path(__file__).resolve().parent
path = __filepath__.parents[0] / "DJURA/.applications/FF-converter"
records_path = path / "records"
out_path = path / "msa-outputs"
sdof = json.load(open(path / "model.json"))
groups = [
    # records_path / "0.5",
    # records_path / "1.0",
    records_path / "0.1",
]


def run_msa(gm_path: Path):
    gm_id = gm_path.name

    out = {}

    for json_file in gm_path.glob("Records*.json"):
        records_lvl = json_file.stem
        print(records_lvl)

        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        filenames = data["selected_scaled_best"]["rec_filenames"]
        dts = data["selected_scaled_best"]["dt"]

        file_x, file_y = zip(*(name.split(", ") for name in filenames))

        records_path = gm_path.parents[0] / f"gms{gm_id}/{records_lvl}.zip"

        out[records_lvl] = {
            "file_x": file_x,
            "file_y": file_y,
            "dts": dts,
            "max_disp": []
        }

        for _fx, _fy, _dt in zip(file_x, file_y, dts):
            with zipfile.ZipFile(records_path, "r") as zip_ref:
                with zip_ref.open(f"{_fx}_scaled.txt") as f:
                    record_x = np.loadtxt(f).transpose()
                with zip_ref.open(f"{_fy}_scaled.txt") as f:
                    record_y = np.loadtxt(f).transpose()

            # hysteretic model
            f = sdof["F"]
            d = sdof["D"]

            pars_pos = []
            pars_neg = []
            for _f, _d in zip(f, d):
                pars_pos.append(_f)
                pars_pos.append(_d)
                pars_neg.append(-_f)
                pars_neg.append(-_d)

            pars_pos += pars_neg + [0.8, 0.5, 0.0, 0.0, 0.0]

            sdof_out = run_sdof(pars_pos, record_x, _dt, sdof["mass"],
                                sdof["damping"])

            out[records_lvl]["max_disp"].append(sdof_out)

    export_results(
        out_path /
        f"msa-{gm_path.name}", out, "json")


def run_msa1(gm_path: Path):
    gm_id = gm_path.name

    out = {}

    for json_file in gm_path.glob("Records*.json"):
        records_lvl = json_file.stem
        print(records_lvl)

        with json_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        file_x = data["selected_scaled_best"]["rec_filenames"]
        dts = data["selected_scaled_best"]["dt"]

        records_path = gm_path.parents[0] / f"gms{gm_id}/{records_lvl}.zip"

        out[records_lvl] = {
            "file_x": file_x,
            "dts": dts,
            "max_disp": []
        }

        for _fx, _dt in zip(file_x, dts):
            with zipfile.ZipFile(records_path, "r") as zip_ref:
                with zip_ref.open(f"{_fx}_scaled.txt") as f:
                    record_x = np.loadtxt(f).transpose()

            # hysteretic model
            f = sdof["F"]
            d = sdof["D"]

            pars_pos = []
            pars_neg = []
            for _f, _d in zip(f, d):
                pars_pos.append(_f)
                pars_pos.append(_d)
                pars_neg.append(-_f)
                pars_neg.append(-_d)

            pars_pos += pars_neg + [0.8, 0.5, 0.0, 0.0, 0.0]

            sdof_out = run_sdof(pars_pos, record_x, _dt, sdof["mass"],
                                sdof["damping"])

            out[records_lvl]["max_disp"].append(sdof_out)

    export_results(
        out_path /
        f"msa-{gm_path.name}", out, "json")


if __name__ == "__main__":

    import multiprocessing as mp

    # workers = mp.cpu_count()
    workers = 2

    with mp.Pool(workers - 1) as pool:
        outs = pool.imap(run_msa1, groups)

        for _ in outs:
            print("Success")
