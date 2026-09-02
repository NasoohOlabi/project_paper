# Project paper

Glossary for the English and Arabic writeup of the selection-channel steganography method. Implementation details live in `stego-side-wing`, not here.

## Language

**Selection channel**:
A covert channel that hides bits by choosing among ordinary visible options, not by editing tokens or inserting invisible characters.
_Avoid_: token embedding, steganographic sampling (for this method)

**Angle**:
One candidate communicative intent in a shared ordered list: a category, a source quote, and a tangent.
_Avoid_: topic, prompt, idea, theme (when the list item is meant)

**Tangent**:
The thematic direction field of an Angle: what the reply should talk about.
_Avoid_: angle (the whole triplet), topic

**Reply target**:
The post or comment the sender replies to. Index 0 is a top-level reply to the post; any other index is a specific comment.
_Avoid_: parent (unless walking the thread), location, spatial embedding (in reader-facing prose)

**Stego comment**:
The published visible reply that carries the selected choices. A reader sees ordinary comment text.
_Avoid_: covertext (unless contrasting with literature), stegotext as the primary term in running prose

**Recoverable capacity**:
The number of uniquely decodable bits in one frame: floor(log2 of comment choices) plus floor(log2 of Angle choices).
_Avoid_: physical width, embedding rate, bits per word (unless that metric is actually being reported)

**Physical width**:
The field size written into the bitstream, which can be wider than the recoverable capacity when a choice count is not a power of two.
_Avoid_: capacity (when aliasing is the point)

**Frame**:
One published reply under one post that carries a slice of the bitstream. A longer payload needs more frames.
_Avoid_: sample, trial, comment (when the transport unit is meant)

**Temporal window**:
The agreed duration between the sender's thread snapshot and publication, so the receiver can ignore comments that arrived while the sender was still working.
_Avoid_: timeout, latency, sync key

**Blind recovery**:
Payload recovery from public thread state plus shared operational parameters, with no sender audit file.
_Avoid_: decode (too broad)

**Audit-assisted recovery**:
Payload recovery that uses sender-side metadata. Valid as an engineering check, not as evidence of a working covert receiver.
_Avoid_: ground truth decode, oracle decode

**Intention-to-treat**:
A reliability rate counted over every attempted sample, including failures.
_Avoid_: success rate (when failures were dropped)

**Successful-output-only**:
A quality or capacity number counted only on accepted generations, usually then averaged per source post.
_Avoid_: the headline result (when the attempt rate is the reliability claim)

**LLM judge**:
A fixed-text, post-clustered evaluation in which a language model scores paired outputs on named criteria. It is not a human reader study.
_Avoid_: G-Eval (unless that exact protocol is in use), human evaluation, naturalness proof

**Context-weighted Angle set**:
An Angle list that depends on which comment was chosen as the reply target, rebuilt after that choice is known.
_Avoid_: shared angle set (when the reported run used parent-conditioned lists)

**ZLG**:
The official zero-shot generative linguistic steganography baseline: bits hidden in generated-token sampling, served by the local hide/reveal API.
_Avoid_: our method, selection channel, LLM-Stega
