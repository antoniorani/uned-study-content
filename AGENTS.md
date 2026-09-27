# Instructions for LLMs and automated content authors

This repository contains academic study content consumed by **UNED Study for Home Assistant**. Treat the JSON files as durable data, not disposable generated text. A careless ID change can disconnect a user's long-term study progress from an item.

## Repository contract

- Each real subject lives in `subjects/<subject_id>/`.
- The subject definition is `subjects/<subject_id>/subject.json`.
- `subject.json.id` **must exactly equal** the folder name.
- Optional images and diagrams belong in `subjects/<subject_id>/assets/`.
- The current content schema is `schema/subject.schema.json`.
- Current `schema_version` is **1**.
- A subject has one study type: `test` or `flashcards`.
- User progress is not stored here and must never be added to this repository.

## The most important rule: IDs are permanent

Topic IDs and item IDs are durable identifiers.

**Never change an existing ID merely because wording, formatting, an explanation or a legal citation is improved.**

Keep the same item ID when:
- correcting spelling;
- improving Markdown;
- clarifying the wording without changing what is being tested;
- improving distractors while the tested concept remains the same;
- correcting or expanding an explanation;
- updating a source reference for the same concept.

Create a **new** item ID when:
- the question tests a materially different proposition;
- a flashcard is split into several atomic cards;
- two items are merged into a different learning item;
- the correct proposition changes so much that old progress would be misleading.

Do not recycle an ID from a deleted item for unrelated content.

## Content versions

Every content change to a subject must increment `content_version`.

Recommended form:

`YYYY.MM.N`

Example: `2026.09.1`, then `2026.09.2`.

`schema_version` changes only when the application contract changes. Do not increment it for ordinary content edits.

## Importance scale

Every item has `importance` from 1 to 5. This value affects how often it is selected for study.

- **1 — Low:** peripheral detail; unlikely to justify frequent repetition.
- **2 — Secondary:** useful but clearly below core material.
- **3 — Normal:** default importance when there is no strong evidence otherwise.
- **4 — Important:** central concept, recurring distinction or clearly exam-relevant material.
- **5 — Essential:** exceptionally central or repeatedly evidenced in examinations.

Do not mark everything 4 or 5. If evidence is weak, use 3.

Where past examinations or official guidance support a higher importance, preserve that evidence in `exam_history` and/or `source`. Never fabricate exam frequency.

## Source fidelity and legal content

This repository may contain law material where wording and temporal validity matter.

When source material is supplied:
- stay faithful to it;
- distinguish verbatim legal propositions from summaries;
- retain article numbers and references when they are known;
- do not silently invent missing article numbers, case numbers, dates, page numbers or quotations;
- do not claim that something appeared in an exam unless there is evidence;
- if the applicable law may have changed, verify the version requested by the user or flag the item for human review rather than guessing;
- do not manufacture a legal rule to make a distractor or explanation sound plausible.

If the source is ambiguous or internally inconsistent, prefer a review note in the pull request over fabricated certainty.

## Test-question quality

A test item must have:
- one clear prompt in `question_md`;
- at least two answer options;
- exactly one `correct_answer`, referencing an answer ID;
- plausible distractors;
- an `explanation_md` whenever useful;
- one valid topic;
- an importance value.

Authoring rules:
- Test one meaningful proposition at a time.
- Avoid accidental clues such as one answer being much longer or more precise solely because it is correct.
- Avoid leaking the correct answer in bold text, headings, hints or wording.
- Avoid trick wording unless it mirrors documented exam style.
- Avoid `all of the above` / `none of the above` unless the source or exam style specifically warrants it.
- Distractors should be wrong for a defensible reason, not nonsense.
- Explanations should teach the distinction, not merely say “B is correct”.
- When practical, explain why tempting distractors fail.
- If a source passage does not support a reliable multiple-choice question, do not force one.

Answer IDs should normally be stable short values such as `a`, `b`, `c`, `d`. Reordering display order in the future must not silently change which ID is correct.

## Flashcard quality

A flashcard must have:
- `front_md`: a focused recall prompt;
- `back_md`: the answer;
- a valid topic;
- an importance value.

Optional fields:
- `hint_md`;
- `mnemonic_md`;
- tags;
- source;
- exam history.

Prefer **atomic recall**. A card asking for ten unrelated points is usually worse than several smaller cards.

The back can be structured with Markdown, including headings, lists, tables and quotations, but should remain suitable for active recall rather than becoming an entire textbook page.

Hints must help retrieval without simply revealing the complete answer.

Mnemonics should be genuinely useful; do not invent awkward mnemonics just to fill the field.

## Markdown

Fields ending in `_md` contain Markdown.

Use:
- headings;
- bold / italic;
- lists;
- tables;
- blockquotes;
- inline code when appropriate;
- relative images in the subject's `assets/` directory.

Do not use:
- `<script>`;
- event-handler HTML;
- arbitrary active HTML;
- external tracking content;
- content that depends on executing JavaScript.

The application will sanitize/render Markdown. Keep source Markdown portable.

## Assets

Store subject-specific media under:

`subjects/<subject_id>/assets/`

Use stable filenames and relative paths.

Do not rename an asset without updating every reference. Prefer SVG/PNG/WebP for diagrams and images when appropriate. Do not add copyrighted material unless the user has the right to store it.

## Topics and tags

Topics represent the subject's durable syllabus structure. Keep topic IDs stable even if their display titles improve.

Tags are optional and may cross topic boundaries. Use lowercase, concise, reusable tags. Do not create near-duplicate tags just because wording differs.

## Sources

When known, use a source object such as:

```json
{
  "type": "official_material",
  "reference": "Tema 3, epígrafe 2",
  "page": 41
}
```

Other useful `type` values can include `law`, `exam`, `notes` or `case`.

Only record fields actually supported by evidence.

## Exam history

`exam_history` is a list of documented exam occurrences, for example:

```json
["2025-02", "2025-06"]
```

Do not infer or fabricate entries. If the provenance is unknown, omit the field.

## Creating a new subject

1. Choose a stable lowercase `subject_id` using letters, numbers, underscores or hyphens.
2. Create `subjects/<subject_id>/subject.json`.
3. Set `schema_version` to 1.
4. Define metadata and topics before generating items.
5. Choose exactly one type: `test` or `flashcards`.
6. Create stable, unique item IDs.
7. Validate the JSON against `schema/subject.schema.json`.
8. Review duplicates and near-duplicates.
9. Check source fidelity.
10. Increment `content_version` for every later edit.

## Updating an existing subject

Before editing:
1. Read the existing `subject.json`.
2. Preserve existing topic and item IDs unless the learning item itself is replaced.
3. Inspect existing tags and naming conventions.
4. Avoid duplicating an already covered proposition.
5. Increment `content_version`.
6. Validate the complete file after changes.

Never regenerate an entire subject from scratch merely to add a few items. That can destroy ID stability and therefore continuity of user progress.

## Required review before committing generated content

For test subjects:
- unique item IDs;
- valid topic references;
- one valid correct answer per item;
- no duplicate answer IDs;
- plausible distractors;
- no answer leakage;
- importance values justified;
- sources/exam history not invented.

For flashcards:
- unique item IDs;
- valid topic references;
- atomic prompts;
- answers appropriate for recall;
- hints do not give the answer away;
- importance values justified;
- sources/exam history not invented.

For every subject:
- valid JSON;
- schema validation passes;
- folder ID matches subject ID;
- `content_version` was incremented;
- existing IDs were preserved where required.

## When information is missing

Do not fill factual gaps by guessing.

If an LLM lacks the source needed to create reliable content, it should:
- create only what is supported;
- clearly state what could not be completed;
- request or flag missing source material in the work summary.

Accuracy and durable identifiers are more important than maximizing the number of generated questions.
