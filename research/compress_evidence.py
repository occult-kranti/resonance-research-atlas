#!/usr/bin/env python3
"""Losslessly compress completed-round CSVs and bind exact decompressed hashes.

Usage: python research/compress_evidence.py round1 round2
Omit round names to process every round directory. Reproduction solvers regenerate
the raw CSVs; run this script afterward to refresh the deterministic archives.
"""
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
targets=[ROOT/name for name in sys.argv[1:]] if len(sys.argv)>1 else sorted(ROOT.glob("round[0-9]*"))
for folder in targets:
    entries=[]
    for path in sorted(folder.glob("*.csv")):
        raw=path.read_bytes();buffer=io.BytesIO()
        with gzip.GzipFile(filename="",fileobj=buffer,mode="wb",mtime=0,compresslevel=9) as stream:stream.write(raw)
        packed=buffer.getvalue()
        if gzip.decompress(packed)!=raw:raise RuntimeError("Lossless round-trip verification failed")
        archive=path.with_suffix(".csv.gz");archive.write_bytes(packed)
        entries.append(dict(raw_filename=path.name,gzip_filename=archive.name,raw_bytes=len(raw),gzip_bytes=len(packed),
                            raw_sha256=hashlib.sha256(raw).hexdigest(),gzip_sha256=hashlib.sha256(packed).hexdigest()))
        path.unlink()
    if entries or any(folder.glob("*.csv.gz")):
        # Include already archived CSVs, so partial reruns never discard provenance.
        regenerated={entry["gzip_filename"]:entry for entry in entries}
        for archive in sorted(folder.glob("*.csv.gz")):
            packed=archive.read_bytes();raw=gzip.decompress(packed)
            regenerated[archive.name]=dict(raw_filename=archive.name[:-3],gzip_filename=archive.name,
                raw_bytes=len(raw),gzip_bytes=len(packed),raw_sha256=hashlib.sha256(raw).hexdigest(),
                gzip_sha256=hashlib.sha256(packed).hexdigest())
        entries=[regenerated[name] for name in sorted(regenerated)]
        manifest=folder/"csv-manifest.json"
        manifest.write_text(json.dumps(dict(method="gzip, mtime=0, empty original filename; verified exact decompression",
                                             reproduce="Run solver.py, then python research/compress_evidence.py "+folder.name,
                                             files=entries),indent=2)+"\n")
        for document in folder.glob("*.md"):
            content=document.read_text()
            for item in entries:
                name=item["raw_filename"]
                content=content.replace("]("+name+")", "]("+name+".gz)")
            # Frozen contracts mention raw output semantics, not compressed storage links.
            if content!=document.read_text():document.write_text(content)
        print(folder.name+": "+str(len(entries))+" exact CSV archives, manifest verified")
