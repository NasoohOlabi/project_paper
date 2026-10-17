# Multi-comment transport and recorded example

The author requested a full dedicated large-payload explanation, clear single-comment versus multi-comment modes, and exact justification of the seven-comment example's control fields. This is an exposition revision; the backend transport is unchanged.

## Checked implementation

- `stego-side-wing/src/workflows/utils/stego_codec.py`: `build_multi_frame_stream`, `parse_multi_frame_stream`, gamma coding, CRC over the ASCII bit string, shared dictionary, and exact decompression.
- `stego-side-wing/src/workflows/pipelines/stego_multiframe.py`: planning over candidate carrier counts, invertible choice budgets, contextual topic construction, and final padding.
- `stego-side-wing/src/workflows/pipelines/receiver.py`: ordered frame collection, candidate joining, count/length checks, CRC rejection, unique payload selection, and decompression. Ordered carrier references are supplied; the header does not discover public comments automatically.

The current stream is `fixed_prefix || version || gamma(N) || gamma(L) || prepared_payload || CRC32`. Its 16-bit prefix `1010010110100101` is a fixed recognizer. It does not select among 65,536 registered formats. The receiver also accepts a legacy count/length stream, marked without integrity verification. UTF-8, character-span pointers and prefix-tree pointers are compression representations rather than transport-prefix format IDs.

Single-comment selection does not automatically receive the multi-comment assembly header. The selected transport mode determines overhead; even a one-carrier result from the multi-comment planner uses its own framing. Count and length information can be agreed differently in another protocol, and the exact marker length is not established as optimal. No backend redesign is claimed or applied.

## Recorded one-message example

Sample 0 of the saved source-excerpt batch contains one 40-byte message. It is a dictionary-source excerpt, which explains the exact compression match. The seven carriers share prepared inputs and supplied order; they are not seven independent messages. Recorded sender and receiver topic selections agree in all seven carriers.

The reproduced arithmetic is:

- Original text: 40 UTF-8 bytes / 320 storage bits, including one newline and a trailing space.
- Exact compressed representation: 31 bits, using the text-span codec.
- Prefix: 16 fixed bits + 2 version bits + 5 count bits for seven comments + 9 length bits for 31 prepared bits = 32 control bits for the whole message.
- Separate CRC: 32 bits. Total transport overhead: 64 bits. Complete stream: 95 bits.
- Seven 15-bit carriers: 105 bit positions. The last contains five remaining CRC bits and ten padding zeros.
- The first carrier holds recognition-prefix bits, demonstrating that header fields use the same linguistic choices and can cross comment boundaries.

The source trace and hashes are in `common/data/multicomment_example.json`; shared macros and row data are in `common/data/multicomment_example_values.tex`. No fresh language-model response or live-platform delivery was tested.

## Reproduce the accounting

From `stego-side-wing`, using its existing environment:

```powershell
uv run --no-sync python ../project_paper/scripts/build_multicomment_example.py `
  --run-dir metrics/e2e_runs/oppression25_fresh_20261003T113428Z `
  --diagnosis metrics/recovery_diagnosis/oppression25_20261003/report.json
```

The script rebuilds the actual framed stream, compares it with saved slices, parses the recorded receiver bits with CRC/padding checks, rebuilds the shared dictionary from public inputs, and verifies exact decompression. It writes only paper evidence files. Source records are read-only.

## Completed checks

Both XeLaTeX builds passed (English 50 pages; Arabic 77 pages). The dedicated methodology, example, tables, and adjoining pages were rendered and visually inspected in both languages. The Arabic receiver-input table was kept after its introducing subsection. Citation/reference checks passed; the four previously checked result-table bodies retain their numeric values. Both abstracts remain unchanged. The example replay passed with all seven saved receiver selections and exact recovery of the 40 original bytes, including whitespace. This replays saved outcomes rather than retesting model determinism or live delivery.
