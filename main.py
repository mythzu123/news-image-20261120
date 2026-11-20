from pathlib import Path
import shutil


source = Path(__file__).with_name("entry.png")
destination = Path("/output/entry.png")
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, destination)
