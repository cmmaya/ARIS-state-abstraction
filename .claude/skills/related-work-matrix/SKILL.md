---
name: related-work-matrix
description: "Builds and updates the related-work matrix (papers x dimensions: formulation, state space, reward, evaluation) in research/related_work_matrix.md, exposes the research gap, and drafts hooks for the related-work section. Uses the research wiki as the source of paper facts. Use when the user says \"related work matrix\", \"compare papers\", \"where is the gap\", \"update the matrix\", or during the formulation stage."
argument-hint: "[optional: topic, paper slugs/arXiv ids to add, or \"refresh\"]"
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep
---

# Related-Work Matrix

Request: $ARGUMENTS   (empty or `refresh` = rebuild from the wiki for the project topic)

Output file: `research/related_work_matrix.md` (keep its section layout).

## Step 0 — Resolve the wiki helper

```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)" || exit 1
PY=python3; $PY -c "" 2>/dev/null || PY=python
ARIS_REPO="${ARIS_REPO:-$(awk -F'\t' '$1=="repo_root"{print $2; exit}' .aris/installed-skills.txt 2>/dev/null)}"
WIKI_SCRIPT=".aris/tools/research_wiki.py"
[ -f "$WIKI_SCRIPT" ] || WIKI_SCRIPT="tools/research_wiki.py"
[ -f "$WIKI_SCRIPT" ] || { [ -n "${ARIS_REPO:-}" ] && WIKI_SCRIPT="$ARIS_REPO/tools/research_wiki.py"; }
[ -d research-wiki ] || echo "WARN: research-wiki/ missing — run /research-wiki init"
```

## Step 1 — Find the papers (query discipline)

1. Read the `## Dimensions` list in `research/related_work_matrix.md` — these are the columns (default: Formulation,
   State space, Reward, Evaluation; the user may have edited them).
2. Run `/research-wiki query "<topic from $ARGUMENTS or RESEARCH_BRIEF.md>"` (or, if the skill can't be invoked,
   `"$PY" "$WIKI_SCRIPT" rebuild_query_pack research-wiki/` and read `research-wiki/query_pack.md`).
3. Candidate papers = those named in the query pack + those in `research-wiki/index.md` tagged with the topic
   + any paper explicitly listed in `$ARGUMENTS`.
4. Open **only** those paper pages (`research-wiki/papers/<slug>.md`). Read: one-line thesis, Problem/Gap, Method,
   Key Results, Assumptions, Limitations. Do not open unrelated pages.
5. Paper requested in `$ARGUMENTS` but not in the wiki → ingest it first
   (`"$PY" "$WIKI_SCRIPT" ingest_paper research-wiki/ --arxiv-id <id>` or `/research-wiki ingest "<title>" — arxiv: <id>`),
   then read its page. If you cannot get the paper's content, add the row with `?` cells and note it.

## Step 2 — Fill the matrix

- One row per paper, sorted by year then by formulation. First column = `[Short name](../research-wiki/papers/<slug>.md)`
  plus `` `paper:<slug>` ``.
- Each cell ≤ 12 words, factual, taken from the paper page. Unknown → `?` (never guess).
- `Key limitation` = the limitation most relevant to **our** problem.
- Keep the final row `**Ours (planned)**` filled from `research/STATUS.md` "Current idea" (or leave blank if none).
- Preserve existing rows the user wrote by hand; update cells only if the wiki page contradicts them, and say so.

## Step 3 — Expose the gap

Under `## Gaps exposed`:
- Look for **empty or rare combinations** across dimensions (e.g. "no paper uses partial observability with dense reward
  and >5-seed evaluation"), and for shared limitations.
- Each gap: one line, the rows that show it, and a G-id. Reuse ids from `research-wiki/gap_map.md` if the gap exists;
  otherwise add the gap to `gap_map.md` with the next free G-id.
- Mark which gap our idea targets with **← ours**.

## Step 4 — Narrative hooks

Under `## Narrative hooks for the related-work section`: 3–6 bullets, each a paragraph topic grouping rows by a dimension
(e.g. "Reward design: A, B shape rewards by …; unlike them we …"), citing `paper:<slug>` ids so `/paper-write` can turn
them into `\cite{}` paragraphs.

## Step 5 — Record and report

- Append one line to `research/log/<today>.md`: "Related-work matrix updated: N papers, gaps G#, G#."
- If a gap suggests a new idea not being pursued now, append it to `research/backlog.md` (entry format there).
- Reply with: number of rows, the gaps found, and which papers had `?` cells.
