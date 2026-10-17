"""Reproduce the saved seven-comment example without fresh model or network calls.

Run with the backend's Python environment because this checks its actual codec.
Source records remain read-only; generated paper evidence goes to common/data.
"""

import argparse
import hashlib
import json
from pathlib import Path
import sys

PAPER = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--backend-root", type=Path, default=PAPER.parent / "stego-side-wing")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--diagnosis", type=Path, required=True)
    parser.add_argument("--sample-index", type=int, default=0)
    args = parser.parse_args()
    sys.path.insert(0, str(args.backend_root / "src"))
    from workflows.pipelines.receiver import build_pre_sender_post_all
    from workflows.utils.stego_codec import (
        MULTI_FRAME_MAGIC,
        MULTI_FRAME_VERSION,
        build_multi_frame_stream,
        build_shared_payload_dictionary,
        decompress_after_embed_prefix,
        encode_elias_gamma,
        parse_multi_frame_stream,
    )

    private_path = args.run_dir / "sender_private" / f"sample_{args.sample_index:04d}.json"
    public_path = args.run_dir / "public" / f"sample_{args.sample_index:04d}.json"
    private = json.loads(private_path.read_text(encoding="utf-8"))
    public = json.loads(public_path.read_text(encoding="utf-8"))
    diagnosis = json.loads(args.diagnosis.read_text(encoding="utf-8"))
    sample = next(s for s in diagnosis["samples"] if s["sample_index"] == args.sample_index)
    assert sample["stage"] == "exact_recovery" and sample["payload_match"]
    frames = private["frames"]
    payload_bits = private["prepared_payload"]["payload_bits"]
    count, length = len(frames), len(payload_bits)
    assert count == 7, "The paper example must remain the saved seven-comment message."
    built = build_multi_frame_stream(payload_bits, count)
    assert built["stream_bits"] == "".join(f["frame_bits"] for f in frames)
    rows = []
    received_parts = []
    for sent, received in zip(frames, sample["frames"], strict=True):
        assert sent["selected_angle_index"] == received["receiver_index"]
        assert received["bits_match"] and len(received["receiver_bits"]) == 1
        received_parts.append(received["receiver_bits"][0])
        rows.append({
            "comment": sent["frame_index"] + 1,
            "reply_index": sent["comment_selection_index"],
            "topic_index": sent["selected_angle_index"],
            "stream_bits": sent["bits_used"],
            "padding_bits": sent["padding_bits"],
        })
    parsed = parse_multi_frame_stream("".join(received_parts), count)
    assert parsed and parsed["integrity_verified"] and parsed["payload_bits"] == payload_bits
    dictionary = build_shared_payload_dictionary([
        build_pre_sender_post_all(post, public["sender_user_id"]) for post in public["posts"]
    ])
    recovered = decompress_after_embed_prefix(parsed["payload_bits"], dictionary, 0, 0)
    assert recovered == private["payload"]
    report = frames[0]["capacity_report"]
    reply_width = report["comment_recoverable_bits"]
    topic_width = report["tangent_recoverable_bits"]
    values = {
        "McPayloadBytes": len(private["payload"].encode("utf-8")),
        "McPayloadStorageBits": len(private["payload"].encode("utf-8")) * 8,
        "McCompressedBits": length,
        "McCount": count,
        "McMarkerBits": len(MULTI_FRAME_MAGIC),
        "McVersionBits": len(MULTI_FRAME_VERSION),
        "McCountBits": len(encode_elias_gamma(count)),
        "McLengthBits": len(encode_elias_gamma(length)),
        "McControlBits": len(built["control_bits"]),
        "McIntegrityBits": len(built["integrity_bits"]),
        "McStreamBits": len(built["stream_bits"]),
        "McPaddingBits": sum(f["padding_bits"] for f in frames),
        "McSlotBits": sum(f["capacity"] for f in frames),
        "McCommentChoices": report["comment_choices"],
        "McTopicChoices": report["tangent_choices"],
        "McCommentBits": reply_width,
        "McTopicBits": topic_width,
        "McFrameBits": reply_width + topic_width,
        "McDictionaryEntries": len(dictionary),
        "McReplyIndex": frames[0]["comment_selection_index"],
        "McTopicIndex": frames[0]["selected_angle_index"],
        "McFirstReplyBits": format(frames[0]["comment_selection_index"], f"0{reply_width}b"),
        "McFirstTopicBits": format(frames[0]["selected_angle_index"], f"0{topic_width}b"),
        "McMarkerString": MULTI_FRAME_MAGIC,
        "McVersionString": MULTI_FRAME_VERSION,
        "McGammaCount": encode_elias_gamma(count),
        "McGammaLength": encode_elias_gamma(length),
    }
    assert sum((values["McMarkerBits"], values["McVersionBits"], values["McCountBits"], values["McLengthBits"])) == values["McControlBits"]
    assert values["McControlBits"] + length + values["McIntegrityBits"] == values["McStreamBits"]
    assert values["McStreamBits"] + values["McPaddingBits"] == values["McSlotBits"]
    data = PAPER / "common/data"
    data.mkdir(exist_ok=True)
    source_paths = (private_path, public_path, args.diagnosis, args.backend_root / "src/workflows/utils/stego_codec.py")
    snapshot = {
        "scope": "One saved message across seven comments; prepared shared context and supplied carrier order; recorded classifier outputs, no fresh generation.",
        "sources": {str(p.resolve()): hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
        "sample_index": args.sample_index,
        "payload": private["payload"],
        "recovered_payload": recovered,
        "values": values,
        "frames": rows,
        "actual_codec_replay": "Stream rebuilt, recorded receiver bits parsed with CRC/padding checks, and payload decompressed exactly.",
    }
    (data / "multicomment_example.json").write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tex = "% Generated by scripts/build_multicomment_example.py.\n"
    tex += "".join(f"\\newcommand{{\\{key}}}{{{value}}}\n" for key, value in values.items())
    for language in ("En", "Ar"):
        cells = lambda row: [str(row[key]) for key in ("comment", "reply_index", "topic_index", "stream_bits", "padding_bits")]
        lines = [" & ".join(f"\\NUM{{{cell}}}" if language == "Ar" else cell for cell in cells(row)) + r" \\ \hline" for row in rows]
        tex += "\\newcommand{\\McFrameRows" + language + "}{%\n" + "\n".join(lines) + "\n}\n"
    (data / "multicomment_example_values.tex").write_text(tex, encoding="utf-8")
    print(f"Verified {count} comments: {length} payload bits + {len(built['control_bits'])} control + {len(built['integrity_bits'])} CRC; exact decompression to {len(recovered.encode('utf-8'))} bytes.")


if __name__ == "__main__":
    main()
