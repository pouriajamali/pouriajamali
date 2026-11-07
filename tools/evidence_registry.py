"""Validate public release evidence and render its README links. Standard library only."""
from pathlib import Path
import argparse, json, re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'evidence/projects.json'

def load(path=MANIFEST):
    data = json.loads(Path(path).read_text(encoding='utf8'))
    assert data['schema_version'] == 1
    assert set(data['projects']) == {'execution', 'reliability', 'integrity', 'replay'}
    for project in data['projects'].values():
        assert re.fullmatch(r'https://github.com/pouriajamali/[a-z0-9-]+', project['repository'])
        release = project['recommended_verified_release']
        assert re.fullmatch(r'v[0-9]+\.[0-9]+\.[0-9]+-preview\.[0-9]+', release['tag'])
        assert re.fullmatch(r'[0-9a-f]{40}', release['commit'])
        assert release['ci']['conclusion'] == 'success'
        assert release['ci']['status'] == 'completed'
        assert release['ci']['head_sha'] == release['commit']
        assert release['ci']['url'].startswith(project['repository'] + '/actions/runs/')
        downloads=release['downloads'];assets=downloads['assets'];signature=downloads['signature']
        assert len(assets)>0 and downloads['sha256_verified_assets']==len(assets)
        assert downloads['execution_performed'] is False
        assert signature['verified'] is True and signature['namespace']=='file'
        assert signature['trusted_key_fingerprint']=='SHA256:AgU5bZlJSjUu0KsWMmVEEr+BfXpcMVNroTA33bHcQdU'
        assert len({a['name'] for a in assets})==len(assets)
        for asset in assets:
            assert re.fullmatch(r'[A-Za-z0-9_.-]+',asset['name'])
            assert re.fullmatch(r'[0-9a-f]{64}',asset['sha256'])
            assert asset['url']==project['repository']+'/releases/download/'+release['tag']+'/'+asset['name']
            assert type(asset['covered_by_signed_checksums']) is bool
        covered={a['name'] for a in assets if a['covered_by_signed_checksums']}
        assert covered and covered==set(signature['scope']) and len(covered)==len(signature['scope'])
        assert project['site_page'].startswith('https://pouriajamali.site/work/')
    for edition in data['resume_editions'].values():
        assert set(edition['release_tags']) == set(data['projects'])
        for key, tag in edition['release_tags'].items():
            project = data['projects'][key]
            assert tag in [project['recommended_verified_release']['tag'], *project['historical_evidence_tags']]
        for row in edition['public_pdfs'].values():
            assert re.fullmatch(r'[0-9a-f]{64}', row['sha256'])
            assert row['language'] in ('en', 'nl', 'es')
    return data

def render_readme(text, data):
    start='<!-- evidence-release-links:begin -->';end='<!-- evidence-release-links:end -->'
    definitions=[]
    for key,p in data['projects'].items():
        tag=p['recommended_verified_release']['tag'];repo=p['repository']
        definitions += [f'[{key}-release]: {repo}/releases/tag/{tag}',
          f'[{key}-case]: {repo}/blob/{tag}/{p["documents"]["case_study"]}',
          f'[{key}-design]: {repo}/blob/{tag}/{p["documents"]["design"]}']
    block=start+'\n'+'\n'.join(definitions)+'\n'+end
    if start not in text and end not in text:return text.rstrip()+'\n\n'+block+'\n'
    assert text.count(start)==1 and text.count(end)==1,'Ambiguous managed release-link block'
    before,rest=text.split(start);_,after=rest.split(end)
    return before+block+after

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    data=load();path=ROOT/'README.md';old=path.read_text(encoding='utf8');new=render_readme(old,data)
    if args.write:path.write_text(new,encoding='utf8',newline='\n')
    else:assert old==new,'README release links drifted; run python tools/evidence_registry.py --write'
    print('PASS: four release contracts and profile links; immutable resume edition registered')

if __name__=='__main__':main()
