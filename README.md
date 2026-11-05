# Research repo (ARIS)

Research workspace built on [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) (Claude Code research skills)
plus our additions: state files (`research/`), custom skills (`/stage-summarizer`, `/related-work-matrix`, `/weekly-report`, `/help-aris`),
results-to-LaTeX macros, and a GitHub LaTeX workflow.

**Start here: [docs/GUIDE.md](docs/GUIDE.md)**: setup, how STATUS / backlog / the knowledge wiki work, and examples.

Quick start (after setup):

```bash
claude
> "Where are we?"                       # reads research/STATUS.md + research-wiki/query_pack.md
> /research-lit "your specific topic"   # fills the knowledge wiki
> /related-work-matrix                  # papers × dimensions, exposes the gap
> /idea-discovery "your direction"      # checks backlog first, parks unselected ideas
> /stage-summarizer                     # end of session
> /weekly-report                        # Fridays
> /help-aris <skill | goal>             # how to use any skill
```
