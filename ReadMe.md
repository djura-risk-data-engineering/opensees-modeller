# Step-by-step
You need to create this only once
```shell
conda create --name venv
conda activate venv
conda install --file requirements.txt
```

To deactivate virutal environment
```shell
conda deactivate
```

To run the MSA WITHOUT multiprocessor
```shell
python main.py
```

To run the MSA with multiprocessor
```shell
python main_mp.py
```

To run the MSA postprocessor
```shell
python postprocess.py
```
