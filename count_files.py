from pathlib import Path

from lib import g

folder = Path(f"{g.website_folderpath}/herbs")

files = sum(p.is_file() for p in folder.rglob("*"))
folders = sum(p.is_dir() for p in folder.rglob("*"))

print(files, folders, files + folders)
