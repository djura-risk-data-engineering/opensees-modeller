from typing import Union, List
from pathlib import Path
import multiprocessing as mp
from .msa import MSA


class MSA_MP:
    def __init__(
        self,
        analysis_options: Union[int, List[int]] = None,
        export_dir: Union[Path, str] = None,
        gm_folder: Path = None,
        gm_filenames: List[Union[Path, str]] = None,
        im_type: int = 2,
        analysis_time_step: float = None,
        dt_record: float = None,
        eq_name_x: str = None,
        eq_name_y: str = None,
        dcap: float = 10.,
        multiprocess: bool = True,
        damping=None,
        omegas=None,
        bnode=None,
        tnode=None,
    ) -> None:
        self.analysis_options = analysis_options
        self.export_dir = export_dir
        self.gm_folder = gm_folder
        self.gm_filenames = gm_filenames
        self.im_type = im_type
        self.analysis_time_step = analysis_time_step
        self.dt_record = dt_record
        self.eq_name_x = eq_name_x
        self.eq_name_y = eq_name_y
        self.dcap = dcap
        self.multiprocess = multiprocess
        self.damping = damping
        self.omegas = omegas
        self.bnode = bnode
        self.tnode = tnode

    def start(self, records, workers=0):
        """
        Start the parallel computation
        :param records: dict
        :param workers: int
        :return: None
        """
        # Get number of CPUs available
        if workers == 0:
            workers = mp.cpu_count()
        if workers > 0:
            workers = workers + 1

        with mp.Pool(workers - 1, maxtasksperchild=1) as pool:
            outputs = pool.imap(self.run_msa, list(records.items()))

            for _ in outputs:
                print("[SUCCESS]")

    def run_msa(self, batch):

        msa = MSA(
            self.gm_folder,
            self.export_dir,
            self.damping,
            self.omegas,
            self.dcap,
            analysis_time_step=self.analysis_time_step,
            bnode=self.bnode,
            tnode=self.tnode,
        )
        msa.use_multiprocess = True

        msa.analyze(batch)
