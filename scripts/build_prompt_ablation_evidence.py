"""Reconcile saved prompt arms and judge decisions; make no model calls."""
import hashlib
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
WORKSPACE = PAPER.parent
BACKEND = WORKSPACE / 'stego-side-wing'
BASE = BACKEND / 'metrics/experiments/wren'
sources = {}

def read(path, lines=False):
    raw = path.read_bytes()
    sources[str(path.relative_to(WORKSPACE))] = hashlib.sha256(raw).hexdigest()
    text = raw.decode('utf-8')
    return [json.loads(s) for s in text.splitlines() if s.strip()] if lines else json.loads(text)

primary = BASE / 'g0_g3/g0_g3_live_20260919'
extension = BASE / 'g4_g5_barb/g4_g5_barb_screen48_20260919'
manifests = [read(p / 'manifest.json') for p in (primary, extension)]
post_ids = set(manifests[0]['post_ids'])
assert len(post_ids) == 48 and post_ids == set(manifests[1]['post_ids'])
historical = read(Path(manifests[0]['j1_data']) / 'codex_judgments/standout_judgments.jsonl', lines=True)
historical_by_post = {}
for row in historical:
    historical_by_post.setdefault(row['post_id'], {})[row['method']] = row['result']['inserted_index'] == row['answer']['inserted_index']
assert len(historical_by_post) == 244 and post_ids <= set(historical_by_post)
strata = {}
for post in post_ids:
    results = historical_by_post[post]
    key = f"ours_{int(results['our_method'])}_zlg_{int(results['zlg'])}"
    strata[key] = strata.get(key, 0) + 1
assert sorted(strata.values()) == [12, 12, 12, 12]
attempts = [r for p in (primary, extension) for r in read(p / 'attempts.jsonl', lines=True)]
by_key = {(r['post_id'], r['arm']): r for r in attempts}
assert len(attempts) == len(by_key) == 336
for post in post_ids:
    rows = [r for r in attempts if r['post_id'] == post]
    assert len({r['selected_parent_id'] for r in rows}) == 1
    assert len({r['selected_angle_idx'] for r in rows}) == 1
judgments = []
for directory in (BASE / 'g0_g3_j1/j1_screen48_20260919', BASE / 'g4_g5_barb/j1_screen48_20260919'):
    tasks = read(directory / 'standout_tasks.jsonl', lines=True)
    saved = read(directory / 'standout_judgments.jsonl', lines=True)
    tasks_by_id = {r['task_id']: r for r in tasks}
    assert len(tasks_by_id) == len(tasks) == len(saved)
    assert {r['task_id'] for r in saved} == set(tasks_by_id)
    for row in saved:
        assert not row.get('error') and isinstance(row.get('result'), dict)
        task = tasks_by_id[row['task_id']]
        assert (task['post_id'], task['arm']) == (row['post_id'], row['arm'])
        attempt = by_key[(row['post_id'], row['arm'])]
        assert row['carrier_text'].strip() == attempt['accepted_text'].strip()
        assert len(row['candidates']) == 10
        inserted = row['answer']['inserted_index']
        carrier = next(c['text'] for c in row['candidates'] if c['index'] == inserted)
        assert carrier.strip() == row['carrier_text'].strip()
        row['_hit'] = row['result']['inserted_index'] == inserted
        judgments.append(row)
assert len(judgments) == 236
assert len({(r['post_id'], r['arm']) for r in judgments}) == len(judgments)

arms = []
for name in ('G0', 'G1', 'G2', 'G3', 'G4', 'G5', 'BARB'):
    rows = [r for r in attempts if r['arm'] == name]
    judged = [r for r in judgments if r['arm'] == name]
    assert len(rows) == 48 and {r['post_id'] for r in rows} == post_ids
    targeted = {r['payload_bearing'] for r in rows}
    assert len(targeted) == 1
    payload = targeted.pop()
    accepted = [r for r in rows if r['accepted_text'].strip()]
    assert {r['post_id'] for r in accepted} == {r['post_id'] for r in judged}
    if payload:
        assert all(r['accepted_exact'] is True for r in accepted)
    else:
        assert all(r['accepted_exact'] is None for r in rows)
    arms.append({'arm': name, 'targeted': payload, 'assigned': len(rows),
                 'produced': sum(bool(r['first_draft_text'].strip()) for r in rows),
                 'topic_verified': len(accepted) if payload else None,
                 'judged': len(judged), 'detected': sum(r['_hit'] for r in judged),
                 'generation_failures': sum(r['outcome'] == 'generation_failure' for r in rows),
                 'validation_failures': sum(r['outcome'] == 'receiver_failure' for r in rows)})

paired = {}
for a, b in [('G1', 'G3'), ('G3', 'G5'), ('G1', 'G5')]:
    left = {r['post_id']: r for r in judgments if r['arm'] == a}
    right = {r['post_id']: r for r in judgments if r['arm'] == b}
    common = set(left) & set(right)
    paired[f'{a}__{b}'] = {'common_judged_posts': len(common),
                          'left_detected': sum(left[p]['_hit'] for p in common),
                          'right_detected': sum(right[p]['_hit'] for p in common)}

# Preserve the trace-enabled rerun as separate evidence, never replacing primary rows.
traced = read(BASE / 'g0_g3/g0_g3_traced_screen48_20260920/summary.json')
for relative in ('src/workflows/utils/workflow_llm_prompts.py', 'docs/reports/project-wren/wren2_prompt_diffs.md', 'scripts/run_wren_g0_g3_pilot.py', 'scripts/run_wren_g4_g5_barb_pilot.py'):
    path = BACKEND / relative
    sources[str(path.relative_to(WORKSPACE))] = hashlib.sha256(path.read_bytes()).hexdigest()
snapshot = {'scope': 'Exploratory topic-validation and conditional standout screen; not full-message delivery.',
            'source_sha256': sources, 'post_ids': sorted(post_ids), 'selection_strata': strata, 'arms': arms,
            'paired_accepted_subsets': paired, 'judge_models': sorted({r['judge_model'] for r in judgments}),
            'judge_reasoning': sorted({r['reasoning_effort'] for r in judgments}),
            'generation_attempts': len(attempts), 'judge_tasks': len(judgments),
            'traced_rerun': {'n_posts': traced['n_posts'], 'n_attempts': traced['n_attempts'],
                            'G1_verified': traced['by_arm']['G1']['accepted_n'],
                            'G3_verified': traced['by_arm']['G3']['accepted_n']}}
values = {'PaPosts': len(post_ids), 'PaGenerationAttempts': len(attempts), 'PaJudgeTasks': len(judgments),
          'PaStratumPosts': 12, 'PaPrimaryAttempts': 192, 'PaExtensionAttempts': 144,
          'PaCommonGThreeGFive': paired['G3__G5']['common_judged_posts'],
          'PaCommonGThreeHits': paired['G3__G5']['left_detected'],
          'PaCommonGFiveHits': paired['G3__G5']['right_detected']}
names = {'G0': 'GZero', 'G1': 'GOne', 'G2': 'GTwo', 'G3': 'GThree', 'G4': 'GFour', 'G5': 'GFive', 'BARB': 'Argumentative'}
for arm in arms:
    for field, suffix in [('produced', 'Produced'), ('topic_verified', 'Verified'), ('detected', 'Detected'), ('judged', 'Judged')]:
        if arm[field] is not None: values['Pa' + names[arm['arm']] + suffix] = arm[field]
tex = '% Generated by scripts/build_prompt_ablation_evidence.py.\n'
tex += ''.join(f'\\newcommand{{\\{k}}}{{{v}}}\n' for k, v in values.items())
for language in ('En', 'Ar'):
    rows = []
    for a in arms:
        label = a['arm'] if a['arm'] != 'BARB' else ('Argumentative' if language == 'En' else 'الكتابة الجدلية')
        target = ('Yes' if a['targeted'] else 'No') if language == 'En' else ('نعم' if a['targeted'] else 'لا')
        def number(s):
            return str(s) if language == 'En' else f'\\NUM{{{s}}}'
        produced = number(f"{a['produced']}/{a['assigned']}")
        verified = number(f"{a['topic_verified']}/{a['assigned']}") if a['targeted'] else '--'
        detected = number(f"{a['detected']}/{a['judged']}")
        if language == 'Ar' and a['arm'] != 'BARB': label = f'\\EN{{{label}}}'
        rows.append(f'{label} & {target} & {produced} & {verified} & {detected} \\\\ \\hline')
    tex += f'\\newcommand{{\\PaRows{language}}}{{%\n' + '\n'.join(rows) + '\n}\n'
out = PAPER / 'common/data'
(out / 'prompt_ablation_evidence.json').write_text(json.dumps(snapshot, indent=2) + '\n', encoding='utf-8')
(out / 'prompt_ablation_values.tex').write_text(tex, encoding='utf-8')
print(json.dumps({'posts': len(post_ids), 'attempts': len(attempts), 'judge_tasks': len(judgments), 'arms': arms, 'paired': paired}, indent=2))
