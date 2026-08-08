# CLAUDE.md — standing instructions for every Claude Code session in this repo

## Touchdown rule

At the end of every prompt session in this repo, before finishing, write one touchdown file:

    touchdowns/TD-<YYYY-MM-DD>-<short-name>.md

(e.g. TD-2026-08-08-manifest-1.md; if a second session same day shares the name, suffix -b.)

A touchdown is a journal record, distinct from handover files. Handovers signal the next
manifest; touchdowns exist so a future journal-writer can reconstruct what happened. Format:

    # Touchdown: <short-name>
    date:
    window: <manifest number, scout, or ad-hoc description>
    prompt-received: <the full text of the prompt this session was given, verbatim>
    what-happened: <2-6 sentences: what was actually done, in plain English>
    files-touched: <created / changed, one line each>
    decisions: <calls made in this session, each with one-line reasoning>
    friction: <anything that stalled, errored, or cost time, however small>
    state-left: <what the repo state is now, what the next session should know>

Write it even for small or failed sessions. Failed sessions especially: friction entries are
the raw material for future diagnosis.

## Safety rule

Before any commit or push: run `git status` and confirm no raw export files appear
(conversations.json, users.json, projects/, login_history.json, any *.zip). These must never
enter version control. If one appears, stop and fix .gitignore before committing.