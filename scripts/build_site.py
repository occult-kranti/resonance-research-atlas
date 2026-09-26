#!/usr/bin/env python3
"""Assemble the atlas and immutable public project snapshots without running imported code."""
from pathlib import Path
import argparse, json, shutil, subprocess, tempfile, html, os

ROOT = Path(__file__).resolve().parents[1]

def git(*args, cwd=None):
    return subprocess.check_output(['git', *args], cwd=cwd, text=True).strip()

def build(output, source_root=None, skip_projects=False):
    output=Path(output).resolve()
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError('Output must not contain the authored source directory')
    output.mkdir(parents=True,exist_ok=True)
    allow=['index.html','styles.css','app.js','models.js','assets','data','docs','research','archive','integrations','README.md','LICENSE']
    for name in allow:
        src=ROOT/name
        if not src.exists(): continue
        dst=output/name
        if src.is_dir(): shutil.copytree(src,dst,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        else: shutil.copy2(src,dst)
    manifest=json.loads((ROOT/'integrations/manifest.json').read_text())
    imported=[]
    if not skip_projects:
        for spec in manifest['projects']:
            if spec.get('mode')!='snapshot': continue
            local=(Path(source_root)/spec['name']) if source_root else None
            with tempfile.TemporaryDirectory(prefix='atlas-import-') as tmp:
                if local and local.exists():
                    actual=git('rev-parse','HEAD',cwd=local)
                    if actual != spec['commit']:
                        raise ValueError(f"{spec['name']}: local HEAD differs from pinned revision")
                    # Only committed content is assembled; never publish unrelated local files.
                    archive=Path(tmp)/'source.tar'
                    subprocess.run(['git','archive','--format=tar','-o',str(archive),spec['commit']],cwd=local,check=True)
                else:
                    clone=Path(tmp)/'repo'
                    subprocess.run(['git','clone','--quiet','--no-checkout','--filter=blob:none',spec['url']+'.git',str(clone)],check=True)
                    archive=Path(tmp)/'source.tar'
                    subprocess.run(['git','archive','--format=tar','-o',str(archive),spec['commit']],cwd=clone,check=True)
                import tarfile
                dest=output/'projects'/spec['name']
                if dest.exists(): shutil.rmtree(dest)
                dest.mkdir(parents=True)
                with tarfile.open(archive) as tar: tar.extractall(dest,filter='data')
                for directory in ['.github','.git']:
                    shutil.rmtree(dest/directory,ignore_errors=True)
                for file in dest.rglob('*.html'):
                    rel=file.parent.relative_to(output)
                    back='../'*len(rel.parts)+'index.html#projects'
                    correction='../'*len(file.parent.relative_to(dest).parts)+'research-corrections.html' if spec['name']=='resonant-vessels' else None
                    note='Historical and proposed interpretations retain their own evidence limits.'
                    if spec['name']=='resonant-vessels':
                        note='Corrected first-draft exhibit. Generated plates are concepts; inherited numerical claims need their cited artifacts.'
                    banner='<aside style="position:relative;z-index:10000;background:#eee8db;color:#183a39;padding:10px 18px;font:14px/1.5 system-ui;border-bottom:1px solid #b4c0b7"><a style="color:#145c5a;font-weight:700" href="'+back+'">← Research Atlas</a> · '+html.escape(note)
                    if correction: banner+=' <a style="color:#145c5a" href="'+correction+'">Read source corrections</a>'
                    banner+='</aside>'
                    text=file.read_text()
                    import re
                    text=re.sub(r'(<body\b[^>]*>)',lambda m:m.group(1)+banner,text,count=1,flags=re.I)
                    file.write_text(text)
                imported.append({'name':spec['name'],'commit':spec['commit'],'path':'projects/'+spec['name']+'/'})
    (output/'.nojekyll').touch()
    source_sha=os.environ.get('GITHUB_SHA')
    if not source_sha and subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:
        source_sha=git('rev-parse','HEAD',cwd=ROOT)
    (output/'build-manifest.json').write_text(json.dumps({'atlas_source':source_sha,'projects':imported,'assembly':'Source snapshots, only navigation banners added'},indent=2)+'\n')
    print(json.dumps({'output':str(output),'projects':imported,'files':sum(p.is_file() for p in output.rglob('*'))}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--source-root');p.add_argument('--skip-projects',action='store_true');a=p.parse_args()
    build(a.output,a.source_root,a.skip_projects)
