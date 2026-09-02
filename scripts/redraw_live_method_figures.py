"""Redraw paper figures so labels match the live selection-channel writeup."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT_DIRS = [
    ROOT / "stego_paper" / "figures",
    ROOT / "stego_paper_ar" / "figures",
]

BG = "#F8FAFC"
SLATE = "#334155"
TEAL = "#0D9488"
AMBER = "#D97706"
CARD = "#FFFFFF"
BORDER = "#94A3B8"
MUTED = "#64748B"
LIGHT_TEAL = "#CCFBF1"
LIGHT_AMBER = "#FEF3C7"
LIGHT_ROSE = "#FFE4E6"
LIGHT_SLATE = "#E2E8F0"


def _save(fig, name: str) -> None:
    fig.patch.set_facecolor(BG)
    for out in OUT_DIRS:
        out.mkdir(parents=True, exist_ok=True)
        dest = out / name
        fig.savefig(dest, dpi=220, bbox_inches="tight", facecolor=BG, edgecolor="none")
        print(f"wrote {dest}")
    plt.close(fig)


def _box(ax, x, y, w, h, text, *, fc=CARD, ec=BORDER, tc=SLATE, size=9, weight="medium", lw=1.2, radius=0.08):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.02,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=2,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        color=tc,
        fontsize=size,
        fontweight=weight,
        zorder=3,
        wrap=True,
    )
    return patch


def _arrow(ax, x1, y1, x2, y2, color=SLATE):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=12,
            color=color,
            lw=1.4,
            zorder=1,
        )
    )


def draw_verify_and_decode() -> None:
    fig, ax = plt.subplots(figsize=(14.2, 7.4))
    ax.set_xlim(0, 14.2)
    ax.set_ylim(0, 7.4)
    ax.axis("off")
    ax.set_facecolor(BG)

    ax.text(0.35, 6.95, "Sender", fontsize=13, fontweight="bold", color=SLATE)
    ax.text(0.35, 3.35, "Receiver", fontsize=13, fontweight="bold", color=SLATE)
    ax.plot([0.3, 13.9], [3.7, 3.7], ls="--", color=BORDER, lw=1.1)
    ax.text(12.55, 3.82, "public channel", fontsize=8, color=MUTED, ha="center")

    _box(ax, 0.4, 5.15, 3.3, 1.35, "Synthesize 3 JSON\ncomments (T=0.7)", fc=LIGHT_AMBER, ec=AMBER)
    _box(ax, 4.5, 5.15, 3.5, 1.35, "Strict decode hits\nselected Angle?", fc=LIGHT_TEAL, ec=TEAL)
    _box(ax, 9.0, 5.15, 3.4, 1.35, "Write local artifact\n(does not post to Reddit)", fc=LIGHT_SLATE, ec=SLATE)
    _arrow(ax, 3.7, 5.82, 4.5, 5.82)
    _arrow(ax, 8.0, 5.82, 9.0, 5.82)
    ax.text(6.25, 6.62, "Yes", fontsize=8, color=TEAL, ha="center")

    # retry loop
    ax.annotate(
        "",
        xy=(2.05, 5.15),
        xytext=(6.25, 4.55),
        arrowprops=dict(arrowstyle="-|>", color=AMBER, lw=1.3, connectionstyle="arc3,rad=-0.25"),
    )
    ax.text(4.7, 4.55, "No  ·  retry same parent + Angle\nthen optional revision  ·  budget 6", fontsize=8, color=AMBER, ha="center")

    _box(ax, 0.4, 1.35, 2.7, 1.35, "Observe\nstego comment", fc=LIGHT_SLATE, ec=SLATE)
    _box(ax, 3.7, 1.35, 3.3, 1.35, "MiniLM cosine shortlist\ntop 20, then lexical rerank", fc=LIGHT_TEAL, ec=TEAL)
    _box(ax, 7.6, 1.35, 3.2, 1.35, "LLM discriminator\n(T=0.7):  idx: N", fc=LIGHT_AMBER, ec=AMBER)
    _box(ax, 11.3, 1.35, 2.5, 1.35, "Map to payload bits\naudit may override\nin non-strict mode", size=8)
    _arrow(ax, 3.1, 2.02, 3.7, 2.02)
    _arrow(ax, 7.0, 2.02, 7.6, 2.02)
    _arrow(ax, 10.8, 2.02, 11.3, 2.02)

    ax.plot([10.7, 10.7], [5.15, 2.7], ls=":", color=BORDER, lw=1.2)
    ax.text(10.85, 3.95, "artifact", fontsize=7.5, color=MUTED)

    ax.text(0.4, 0.35, "Sender acceptance requires a strict parse. Reported workloads decode non-strict and may trust the audit index.", fontsize=8, color=MUTED)
    _save(fig, "verify_and_decode_flow.png")


def draw_two_layer() -> None:
    fig, ax = plt.subplots(figsize=(15.2, 8.6))
    ax.set_xlim(0, 15.2)
    ax.set_ylim(0, 8.6)
    ax.axis("off")
    ax.set_facecolor(BG)

    ax.text(0.4, 8.2, "Layer 1 — reply target", fontsize=13, fontweight="bold", color=SLATE)
    ax.text(8.3, 8.2, "Layer 2 — shared Angle set", fontsize=13, fontweight="bold", color=SLATE)

    # tree
    nodes = [
        (2.6, 7.15, "POST", False),
        (1.15, 5.85, "c1", False),
        (2.6, 5.85, "c2", True),
        (4.05, 5.85, "c3", False),
        (1.9, 4.55, "c4", False),
        (3.3, 4.55, "c5", False),
    ]
    ax.plot([2.6, 1.15], [7.15, 6.35], color=BORDER, lw=1.2, zorder=1)
    ax.plot([2.6, 2.6], [7.15, 6.35], color=BORDER, lw=1.2, zorder=1)
    ax.plot([2.6, 4.05], [7.15, 6.35], color=BORDER, lw=1.2, zorder=1)
    ax.plot([2.6, 1.9], [5.85, 5.05], color=BORDER, lw=1.2, zorder=1)
    ax.plot([2.6, 3.3], [5.85, 5.05], color=BORDER, lw=1.2, zorder=1)
    for x, y, lab, sel in nodes:
        fc, ec, lw = (LIGHT_AMBER, AMBER, 2.2) if sel else (CARD, BORDER, 1.1)
        _box(ax, x - 0.55, y - 0.32, 1.1, 0.64, lab, fc=fc, ec=ec, lw=lw, size=8)
    ax.text(2.6, 3.95, "Selected reply parent (index k)\nindex 0 = top-level reply to post", fontsize=8.5, color=AMBER, ha="center")
    ax.text(0.4, 3.35, r"$w_1=\lceil\log_2(n+1)\rceil$   DFS order, not post dates", fontsize=8.5, color=MUTED)

    # angle list
    labels = [
        "0  category · quote · tangent",
        "1  category · quote · tangent",
        "2  category · quote · tangent",
        "3  selected Angle idx",
        "4  category · quote · tangent",
        "…",
        "31  cap used in reported runs",
    ]
    y0 = 7.35
    for i, lab in enumerate(labels):
        y = y0 - i * 0.48
        sel = i == 3
        _box(
            ax,
            8.3,
            y - 0.18,
            6.2,
            0.42,
            lab,
            fc=LIGHT_TEAL if sel else CARD,
            ec=TEAL if sel else BORDER,
            lw=1.8 if sel else 1.0,
            size=8,
        )
    ax.text(8.3, 3.35, r"Recoverable $w_2=\lfloor\log_2 A\rfloor$  ·  physical field may wrap with modulo", fontsize=8.5, color=MUTED)

    # bitstream
    _box(ax, 0.4, 2.15, 14.4, 0.95, "", fc="#F1F5F9", ec=BORDER)
    ax.text(0.7, 2.78, "payload bits", fontsize=8, color=MUTED, va="center")
    ax.add_patch(Rectangle((2.6, 2.35), 4.2, 0.55, facecolor=LIGHT_AMBER, edgecolor=AMBER))
    ax.add_patch(Rectangle((6.8, 2.35), 5.0, 0.55, facecolor=LIGHT_TEAL, edgecolor=TEAL))
    ax.text(4.7, 2.62, r"$w_1$ bits → Layer 1", fontsize=9, ha="center", color=SLATE)
    ax.text(9.3, 2.62, r"$w_2$ bits → Layer 2", fontsize=9, ha="center", color=SLATE)

    _box(ax, 0.4, 0.35, 5.6, 1.45, "LLM synthesis (temperature=0.7)", fc=LIGHT_SLATE, ec=SLATE)
    _box(ax, 6.4, 0.35, 2.6, 1.45, "Candidate A\nJSON", size=8)
    _box(ax, 9.2, 0.35, 2.6, 1.45, "Candidate B\nJSON", size=8)
    _box(ax, 12.0, 0.35, 2.6, 1.45, "Candidate C\nJSON", size=8)
    _arrow(ax, 6.0, 1.07, 6.4, 1.07)
    _save(fig, "two_layer_embedding.png")


def draw_temporal_sync() -> None:
    fig, ax = plt.subplots(figsize=(14.4, 6.8))
    ax.set_xlim(0, 14.4)
    ax.set_ylim(0, 6.8)
    ax.axis("off")
    ax.set_facecolor(BG)

    ax.text(0.4, 6.35, "Intended temporal window", fontsize=13, fontweight="bold", color=SLATE)
    ax.plot([0.8, 13.6], [4.15, 4.15], color=SLATE, lw=2.0)
    ax.text(0.8, 4.42, "thread history →", fontsize=8, color=MUTED)
    ax.text(13.6, 4.42, "later", fontsize=8, color=MUTED, ha="right")

    ax.plot([2.4, 2.4], [3.95, 5.35], color=TEAL, lw=1.4)
    ax.scatter([2.4], [4.15], s=40, color=TEAL, zorder=4)
    ax.text(2.4, 5.5, r"$t_{start}$: Alice snapshots thread", fontsize=9, ha="center", color=TEAL)

    ax.add_patch(Rectangle((2.4, 3.55), 6.2, 1.2, facecolor=LIGHT_AMBER, edgecolor=AMBER, alpha=0.9, zorder=1))
    ax.text(5.5, 4.15, "Sender pipeline\n(embedding + synthesis latency)", fontsize=9, ha="center", color=SLATE, zorder=3)

    ax.plot([8.6, 8.6], [3.95, 5.35], color=AMBER, lw=1.4)
    ax.scatter([8.6], [4.15], s=40, color=AMBER, zorder=4)
    ax.text(8.6, 5.5, r"$t_{publish}$: stego comment appears", fontsize=9, ha="center", color=AMBER)

    ax.plot([7.4, 7.4], [2.35, 3.55], color=SLATE, lw=1.1, ls="--")
    ax.annotate(
        "",
        xy=(7.4, 2.55),
        xytext=(0.8, 2.55),
        arrowprops=dict(arrowstyle="<->", color=SLATE, lw=1.3),
    )
    ax.text(4.1, 2.05, r"Intended: Bob keeps comments with time $\leq t_{publish}-T_{sync}$", fontsize=9, ha="center", color=SLATE)

    ax.scatter([5.2, 6.6], [4.75, 4.75], s=50, color="#E11D48", zorder=4)
    ax.text(5.9, 5.05, "excluded: arrived during Alice's run", fontsize=8, color="#E11D48", ha="center")

    _box(
        ax,
        0.6,
        0.35,
        13.2,
        1.35,
        "Live receiver does not apply this cutoff.\nIt deletes Alice's comment from a supplied post and rebuilds from that object.\nReported encode/decode workloads skip even that rebuild: they decode against the sender's already-angled post.",
        fc=LIGHT_SLATE,
        size=9,
    )
    _save(fig, "temporal_sync_window.png")


def draw_end_to_end() -> None:
    fig, ax = plt.subplots(figsize=(13.6, 7.0))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 7.0)
    ax.axis("off")
    ax.set_facecolor(BG)

    _box(ax, 0.35, 3.7, 3.3, 2.6, "Alice / sender agent\n\nencode\nverify\nwrite local artifact", fc=LIGHT_AMBER, ec=AMBER, size=9)
    _box(ax, 5.05, 3.55, 3.5, 2.9, "Public threaded forum\n(e.g. Reddit-style)\n\nPost\n  Comment thread\n    Reply chain\n    (selected parent)", fc=CARD, size=9)
    _box(ax, 9.95, 3.7, 3.3, 2.6, "Bob / receiver agent\n\nuse supplied snapshot\ndecode payload", fc=LIGHT_TEAL, ec=TEAL, size=9)
    _arrow(ax, 3.65, 5.0, 5.05, 5.0)
    ax.text(4.35, 5.18, "stego comment", fontsize=8, color=MUTED, ha="center")
    _arrow(ax, 8.55, 5.0, 9.95, 5.0)
    ax.text(9.25, 5.18, "reads thread", fontsize=8, color=MUTED, ha="center")

    _box(
        ax,
        0.35,
        0.45,
        8.3,
        2.55,
        "Shared\nsearch settings + Angle generation at temperature 0\nagreed wait $T_{sync}$ (operational)\n\nTemperature 0 rebuilds document and Angle lists.\nComment writing and Angle ID run at temperature 0.7.",
        fc=LIGHT_SLATE,
        size=9,
    )
    _box(
        ax,
        8.9,
        0.45,
        4.35,
        2.55,
        "Passive observer\n\nsees the public thread\ndoes not share\nsearch / Angle settings",
        fc="#F8FAFC",
        ec=MUTED,
        tc=MUTED,
        size=8.5,
    )
    _save(fig, "end_to_end_scenario.png")


def draw_research_pipeline() -> None:
    fig, ax = plt.subplots(figsize=(16.4, 5.2))
    ax.set_xlim(0, 16.4)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_facecolor(BG)

    stages = [
        (0.3, "1  Source inputs", "Post title, body, URL\nnot the comment section"),
        (3.5, "2  Search-term generator", "LLM (T=0)\nprompt asks 12–20\nbalanced keeps 8"),
        (6.7, "3  Fixed-shape search", "Google first, then fallbacks\nfirst=1, count=10"),
        (9.9, "4  Filtering and fetch", "Drop PDFs\nDedup links\nBatched fetch (3)"),
        (13.1, "5  Hashed corpus", "search-term hash\nsearch-results hash"),
    ]
    colors = [CARD, LIGHT_TEAL, CARD, LIGHT_AMBER, CARD]
    ecs = [BORDER, TEAL, BORDER, AMBER, BORDER]
    for (x, title, body), fc, ec in zip(stages, colors, ecs):
        _box(ax, x, 1.55, 2.95, 2.7, f"{title}\n\n{body}", fc=fc, ec=ec, size=8.5)
    for x in (3.25, 6.45, 9.65, 12.85):
        _arrow(ax, x, 2.9, x + 0.25, 2.9)
    ax.text(8.2, 0.55, "Reproducible preprocessing chain (Alice == Bob)", fontsize=11, ha="center", color=SLATE, fontweight="bold")
    _save(fig, "research_pipeline_deterministic.png")


def draw_implementation() -> None:
    fig, ax = plt.subplots(figsize=(14.8, 4.8))
    ax.set_xlim(0, 14.8)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    ax.set_facecolor(BG)

    stages = [
        (0.35, "Data load", "#DBEAFE", "#2563EB"),
        (3.2, "Research", LIGHT_AMBER, AMBER),
        (6.05, "Angle generation", LIGHT_TEAL, TEAL),
        (8.9, "Stego encoding", "#FCE7F3", "#DB2777"),
        (11.75, "Decode", "#DCFCE7", "#16A34A"),
    ]
    for x, title, fc, ec in stages:
        _box(ax, x, 1.7, 2.6, 2.1, title, fc=fc, ec=ec, size=11, weight="bold")
    for x in (2.95, 5.8, 8.65, 11.5):
        _arrow(ax, x, 2.75, x + 0.25, 2.75)
    ax.text(
        7.4,
        0.55,
        "Search-term and Angle stages replay at T=0 when inputs match.\nComment writing and Angle identification remain stochastic (T=0.7).",
        fontsize=9,
        ha="center",
        color=MUTED,
    )
    _save(fig, "implementation_pipelines.png")


def draw_token_vs_intent() -> None:
    fig, ax = plt.subplots(figsize=(14.8, 7.4))
    ax.set_xlim(0, 14.8)
    ax.set_ylim(0, 7.4)
    ax.axis("off")
    ax.set_facecolor(BG)
    ax.text(7.4, 7.0, "Embedding domain: token vs communicative intent", fontsize=13, fontweight="bold", color=SLATE, ha="center")

    _box(ax, 0.35, 0.4, 5.6, 6.2, "", fc=CARD, ec=BORDER, lw=1.0)
    ax.text(3.15, 6.2, "Token / distribution embedding (typical)", fontsize=10, fontweight="bold", color=SLATE, ha="center")
    for i, tok in enumerate(["tok", "a", "the", "[x]", "bit", "y"]):
        _box(ax, 0.6 + i * 0.85, 5.15, 0.75, 0.55, tok, size=7.5, fc=LIGHT_SLATE)
    _box(ax, 0.7, 3.55, 4.9, 1.2, "next-token distribution / logits", fc=LIGHT_SLATE, size=9)
    _box(ax, 0.7, 2.05, 4.9, 1.15, "sampling", fc=LIGHT_SLATE, size=9)
    _box(ax, 0.7, 0.65, 4.9, 1.1, "often needs white-box logits\nfragile in a threaded social context", fc=LIGHT_ROSE, ec="#E11D48", tc="#9F1239", size=8)

    ax.annotate("", xy=(8.55, 3.6), xytext=(6.15, 3.6), arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2.2))
    ax.text(7.35, 3.95, "shift to\nsemantic layer", fontsize=8.5, color=TEAL, ha="center")

    _box(ax, 8.85, 0.4, 5.55, 6.2, "", fc=CARD, ec=TEAL, lw=1.3)
    ax.text(11.62, 6.2, "Semantic / intent embedding (this work)", fontsize=10, fontweight="bold", color=TEAL, ha="center")
    _box(ax, 9.15, 5.15, 4.95, 0.7, "Original post", size=8.5)
    _box(ax, 9.55, 4.25, 4.15, 0.55, "Comment", size=8)
    _box(ax, 9.55, 3.35, 4.15, 0.7, "Layer 1: reply target", fc=LIGHT_AMBER, ec=AMBER, size=8.5)
    for i, lab in enumerate(["Angle 0", "Angle 1", "Angle k", "Angle n"]):
        sel = lab == "Angle k"
        _box(
            ax,
            9.15 + (i % 2) * 2.55,
            1.95 - (i // 2) * 0.7,
            2.4,
            0.55,
            lab,
            fc=LIGHT_TEAL if sel else CARD,
            ec=TEAL if sel else BORDER,
            size=8,
        )
    _box(ax, 9.15, 0.6, 4.95, 0.7, "Stego reply (visible comment)", fc=LIGHT_TEAL, ec=TEAL, size=8.5)
    _save(fig, "token_vs_intent_embedding.png")


def main() -> None:
    draw_verify_and_decode()
    draw_two_layer()
    draw_temporal_sync()
    draw_end_to_end()
    draw_research_pipeline()
    draw_implementation()
    draw_token_vs_intent()


if __name__ == "__main__":
    main()
