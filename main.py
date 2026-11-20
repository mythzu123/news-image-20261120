from pathlib import Path
import hashlib
import shutil


source = Path(__file__).with_name("entry.png")
destination = Path("/output/entry.png")
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, destination)

source_size = source.stat().st_size
destination_size = destination.stat().st_size
source_hash = hashlib.sha256(source.read_bytes()).digest()
destination_hash = hashlib.sha256(destination.read_bytes()).digest()
if source_size != destination_size or source_hash != destination_hash:
    raise SystemExit("Copy verification failed: source and output sizes or SHA-256 hashes differ.")
print(f"Copied and verified {destination_size} bytes.")
