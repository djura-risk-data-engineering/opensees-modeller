import pickle
from pathlib import Path

path = Path(__file__).resolve().parent

with open(path / "out2/POE-0.0001-in-50-years/Record1.pickle", "rb") as f:
    data = pickle.load(f)


print(data[0].shape)
print(data[1].shape)
print(data[2].shape)
