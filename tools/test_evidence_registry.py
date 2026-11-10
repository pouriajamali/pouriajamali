import copy, unittest, json, tempfile
from pathlib import Path
from evidence_registry import load, render_readme

class RegistryChecks(unittest.TestCase):
    def test_current_profile_and_repeat_render(self):
        data=load();sample='[Current preview][execution-release]'
        rendered=render_readme(sample,data)
        self.assertEqual(rendered,render_readme(rendered,data))
        self.assertIn('/releases/tag/v0.5.2-preview.1',rendered)

    def test_main_links_and_unrelated_repositories_stay(self):
        data=load();sample='https://github.com/pouriajamali/trading-execution-lab/blob/main/README.md https://github.com/other/other/releases/tag/v0.0.0-preview.1'
        self.assertTrue(render_readme(sample,data).startswith(sample))

    def test_historical_tagged_links_are_never_promoted(self):
        data=load();sample='Historical source: https://github.com/pouriajamali/trading-execution-lab/blob/v0.5.1-preview.1/docs/decisions/0002-transactional-control-plane.md'
        self.assertTrue(render_readme(sample,data).startswith(sample))

    def test_incomplete_or_unsigned_release_evidence_is_rejected(self):
        for field in ['ci','signature','assets','hash','coverage','count']:
            with self.subTest(field=field),tempfile.TemporaryDirectory() as tmp:
                data=load();r=data['projects']['execution']['recommended_verified_release']
                if field=='ci':r['ci']['status']='in_progress'
                if field=='signature':r['downloads']['signature']['verified']=False
                if field=='assets':r['downloads']['assets']=[]
                if field=='hash':r['downloads']['assets'][0]['sha256']='incorrect'
                if field=='coverage':r['downloads']['signature']['scope']=[]
                if field=='count':r['downloads']['sha256_verified_assets']=999
                path=Path(tmp)/'projects.json';path.write_text(json.dumps(data),encoding='utf8')
                with self.assertRaises(AssertionError):load(path)

    def test_resume_issuance_is_not_silently_promoted(self):
        data=load();snapshot=copy.deepcopy(data['resume_editions'])
        render_readme('test',data)
        self.assertEqual(snapshot,data['resume_editions'])
        self.assertEqual('v0.5.1-preview.1',data['resume_editions']['showcase-20261106']['release_tags']['execution'])

    def test_wrong_commit_ci_is_rejected(self):
        data=load();data['projects']['execution']['recommended_verified_release']['ci']['head_sha']='0'*40
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'projects.json';path.write_text(json.dumps(data),encoding='utf8')
            with self.assertRaises(AssertionError):load(path)

    def test_unknown_resume_release_is_rejected(self):
        data=load();data['resume_editions']['showcase-20261106']['release_tags']['execution']='v9.9.9-preview.1'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'projects.json';path.write_text(json.dumps(data),encoding='utf8')
            with self.assertRaises(AssertionError):load(path)

    def test_active_edition_and_original_snapshot_are_distinct(self):
        data=load()
        self.assertEqual('review-repairs-20261110-final',data['active_resume_edition'])
        self.assertEqual('v0.1.0-preview.1',data['resume_editions']['senior-evidence-20261110']['release_tags']['contracts'])
        self.assertEqual('v0.1.0-preview.2',data['resume_editions'][data['active_resume_edition']]['release_tags']['contracts'])
        self.assertEqual(4,len(data['resume_editions']['showcase-20261106']['release_tags']))
        self.assertEqual(14,len(data['resume_editions'][data['active_resume_edition']]['release_tags']))
        self.assertEqual(6,len(data['resume_editions'][data['active_resume_edition']]['public_pdfs']))

    def test_unknown_active_edition_is_rejected(self):
        data=load();data['active_resume_edition']='missing'
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'projects.json';path.write_text(json.dumps(data),encoding='utf8')
            with self.assertRaises(AssertionError):load(path)

if __name__=='__main__':unittest.main()
