# CLAUDE.md — Claude Code Project Instructions

This repository uses the same constitution for Claude Code and Codex-style agents.

**Authoritative rules are in `AGENTS.md`.**

Claude Code must read and follow `AGENTS.md` before editing files, running commands, adding dependencies, changing API behavior, or producing a final report.

Summary of the most important constraints:

- CPU-only.
- Single image only.
- Object detection only.
- No tracking.
- No video.
- No segmentation.
- No masks.
- No background jobs.
- No queues.
- No remote image URL fetching in MVP.
- Fixed bearer API key from environment.
- OpenAI-compatible `/v1/chat/completions` surface.
- Base64 data URL image input only.
- Tests required for behavior changes.
- Final report required after every run.
- After bootstrap, do not commit or push directly to `main`; use a named branch and PR for every change.
- Every future work order must state the branch name, whether a PR is required, and whether merging is forbidden.

If any requested task conflicts with `AGENTS.md`, stop and report the conflict.
