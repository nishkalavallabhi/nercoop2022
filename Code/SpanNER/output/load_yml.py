import yaml
from pathlib import Path
from yaml.loader import Loader

conf = yaml.load(Path('hparams.yaml').read_text(), Loader=Loader)
print(conf.keys())