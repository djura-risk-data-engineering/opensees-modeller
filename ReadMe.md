# Step-by-step
To install python, visit https://www.python.org/downloads/release/python-3127/

To install git, visit https://git-scm.com/install/

Make sure install the correct version matching your system (64-bit, Windows, macOS etc.)

To clone the repository (do this only once)
```shell
git clone https://github.com/djura-risk-data-engineering/opensees-modeller.git
```

To create the virtual environment (do this only once):
```shell
py -3.12 -m venv .venv
```

To activate the virtual environment:
```shell
.venv\Scripts\activate
```

To upgrade pip (do this only once):
```shell
python -m pip install --upgrade pip
```

To test if all installed correctly, run:
```shell
python build_model.py
```