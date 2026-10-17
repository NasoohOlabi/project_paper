"""Read saved experiment settings and reconcile the literature set; no model calls."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re

PAPER = Path(__file__).resolve().parents[1]
WORKSPACE = PAPER.parent
BACKEND = WORKSPACE / 'stego-side-wing'
SLR = Path('D:/Master/SLR draft')
sources = {}


def read(path, json_data=True):
    raw = path.read_bytes()
    sources[str(path)] = hashlib.sha256(raw).hexdigest()
    value = raw.decode('utf-8-sig')
    return json.loads(value) if json_data else value


excerpt = read(BACKEND / 'metrics/e2e_runs/oppression25_fresh_20261003T113428Z/manifest.json')
independent = read(BACKEND / 'metrics/recovery_development/luna10_20261003_v2/manifest.json')
assert excerpt['settings']['stego_default_max_retries'] == 6
assert excerpt['settings']['stego_llm_temperature'] == 0.7
assert '--max-frames-per-post 12' in excerpt['command']
assert independent['config']['max_retries'] == 1
assert independent['config']['max_frames'] == 20
assert independent['config']['payload_bytes'] == 8

archive = {}
for n in (5, 6):
    directory = WORKSPACE / f'AstrasReview/iterations/round-{n}'
    manifest = read(directory / 'manifest_private.json')
    quality = read(directory / 'quality_judge_freeze.json')
    settings = manifest['settings']
    assert settings['stego_llm_temperature'] == 0.7
    assert settings['decode_llm_temperature'] == 0
    assert manifest['max_frames'] == 20 and manifest['bits'] == 64
    model = next(m for m in manifest['models']['data'] if m['id'] == settings['lm_studio_model'])
    assert model['quantization'] == 'Q4_K_M' and model['loaded_context_length'] == 16384
    assert quality['model'] == 'openai/gpt-oss-20b' and quality['temperature'] == 0
    archive[str(n)] = {'settings': settings, 'model': model,
                       'max_frames': manifest['max_frames'],
                       'judge': {k: quality[k] for k in ('model', 'temperature')}}

campaign = BACKEND / 'metrics/evaluation_campaigns/lucid_fresh_6x_20260815'
quality_generation = read(campaign / 'runs/batch_0001/balanced/summary.json')['settings']
assert quality_generation['lm_studio_model'] == 'qwen/qwen3.5-9b'
assert quality_generation['stego_llm_temperature'] == 0.7
baseline = read(BACKEND / 'metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815/summary.json')
baseline_identity = baseline['zlg_server_identity']['health']
judge_dir = BACKEND / 'metrics/zlg_comparison_runs/zlg_lucid_fresh_6x_20260815_independent_unique_judge/comparison_dataset'
judgments = read(judge_dir / 'codex_judgments/register_judgments.jsonl', False)
judge = json.loads(judgments.splitlines()[0])
assert judge['judge_model'] == 'gpt-5.6-luna' and judge['reasoning_effort'] == 'high'

# The ID/key correspondence is documented with titles and source lines in the SLR report.
mapping = {
    25: 'hao2025robust', 43: 'wang2025contrastive', 44: 'kuznetsov2025deepstego',
    45: 'shi2025emotionally', 47: 'wozniak2025multicriteria', 48: 'lin2025positionagnostic',
    50: 'chen2025activetwo', 3: 'liao2024co', 6: 'wu2024generative', 8: 'lin2024zero',
    9: 'qi2024provably', 10: 'ji2024principled', 11: 'ding2023context',
    12: 'munyer2024deeptextmark', 13: 'wang2023hi', 15: 'steinebach2024natural',
    19: 'li2024imperceptible', 20: 'li2024semantic', 21: 'xu2024beyond',
    23: 'zhang2024controllable', 24: 'pang2024fremax', 4: 'ding2023joint',
    5: 'ding2023discop', 16: 'qiang2023natural', 17: 'li2023rewriting',
    22: 'xiang2023cpg', 2: 'zheng2022general', 18: 'yi2022alisa',
    7: 'kaptchuk2021meteor', 1: 'yang2020vae', 14: 'zhang2020linguistic',
}
rows = list(csv.DictReader(io.StringIO(read(SLR / 'data/SLR - SLR-Deep.csv', False))))
completed = [r for r in rows if r['Year'].strip()]
assert len(completed) == len(mapping) == 31
assert {int(r['#']) for r in completed} == set(mapping)
for language in ('stego_paper', 'stego_paper_ar'):
    text = read(PAPER / language / 'sections/related_work.tex', False)
    table = text.split('\\label{tab:app_distribution}', 1)[1].split('\\end{table}', 1)[0]
    keys = {k.strip() for group in re.findall(r'\\cite\{([^}]+)\}', table) for k in group.split(',')}
    assert keys == set(mapping.values()), (language, keys ^ set(mapping.values()))
for name in ('research_method', 'discussion', 'threats', 'conclusion'):
    read(SLR / f'sections/{name}.tex', False)

snapshot = {
    'source_sha256': sources,
    'source_excerpt': {'settings': excerpt['settings'], 'gpu': excerpt['gpu'], 'carrier_limit': 12},
    'independent_payload': independent['config'],
    'archive': archive,
    'quality_generation_settings': quality_generation,
    'quality_baseline_identity': baseline_identity,
    'quality_judge': {k: judge[k] for k in ('judge_backend', 'judge_model', 'reasoning_effort')},
    'slr_completed': [{'id': int(r['#']), 'title': r['title'], 'year': int(r['Year']),
                       'citation_key': mapping[int(r['#'])]} for r in completed],
    'slr_pending_records': sum(not r['Year'].strip() for r in rows),
    'scope': 'Saved configurations only; current defaults do not replace missing historical settings. '
             'SLR membership checks apply to the completed 31-study synthesis, not all draft counts.',
}
(PAPER / 'common/data/experiment_setup_evidence.json').write_text(
    json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print('Saved setup evidence; bilingual SLR membership: 31/31; archive model/sampling checks: passed.')
