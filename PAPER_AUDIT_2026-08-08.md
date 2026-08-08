# Paper audit log — 2026-08-08

## Scope

This audit updates only `project_paper`. The sibling code repositories were read as evidence sources and were not modified.

## Evidence checked

1. `stego-side-wing/docs/reports/2026-08-08-current-research-state.md` — authoritative status: current LUCID runs are sampler/smoke artifacts with post reuse, and the latest ZLG artifact is not paired with a clean symmetric manifest.
2. `stego-side-wing/.agents/method-and-zlg-benchmark.md` — method contract, capacity accounting, baseline protocol, and reporting cautions.
3. Sender/receiver pipelines, the shared codec, workflow prompts, and benchmark reports — implementation behavior and provenance.
4. Both English and Arabic LaTeX trees — terminology, numerical claims, and translation consistency.

## Findings and actions

| Paper area | Finding | Action |
|---|---|---|
| Abstract/introduction | The historical 627/554/304 artifact was too easy to read as current publication evidence. | Recast it as an audited historical configuration comparison. |
| Synchronization | The temporal window is an operational precondition; the current receiver does not enforce the timestamp cutoff itself. | State that the caller/acquisition layer must supply or enforce it. |
| Decoding | Semantic shortlist ranking plus a discriminator is configurable and not inherently deterministic. | Qualify deterministic-reconstruction language and separate audit-assisted recovery. |
| Capacity | Only uniquely decodable states count. | Retain the floor formula and its non-power-of-two caveat. |
| Evaluation/conclusion | Current-state documentation says no clean, symmetric, decision-grade paired result exists yet. | Remove final/superiority framing and preserve failure accounting. |
| Arabic paper | The same factual qualifications must appear in corresponding sections. | Synchronize abstract, methodology, evaluation, and conclusion. |

## Verification record

- `stego_paper_ar/main_ar.xdv` was already untracked and was left untouched.
- No files outside `project_paper` are in scope for edits.
- Both paper variants will be rebuilt if the local TeX toolchain is available.

## Commit plan

1. Update English and Arabic factual scope and method caveats.
2. Build/check both variants and inspect the diff.
3. Commit with an evidence-alignment message.
