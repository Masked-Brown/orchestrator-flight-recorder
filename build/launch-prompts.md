# launch-prompts.md — Copy-paste per Claude Code window

Not part of the repo deliverable. Keep in build/ or delete after launch.

---

## Prompt M1 (first window — no polling)

```
You are Manifest 1 of the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

FIRST, before anything else: confirm .gitignore exists at repo root and covers the raw
conversation export (the unzipped export files/folders and any *.zip). Run `git status` and
confirm no export file appears as tracked or untracked-to-be-added. If the export is exposed,
stop and fix .gitignore before proceeding. This repo will become public; the export must
never be committed.

Then read, in order:
  build/communitycompetitions.md
  build/spec.md
  build/plan.md
  build/brainwave.md

Execute Manifest M1 exactly as specified in build/plan.md (Scaffold and parser). The real
export is already unzipped inside this repo folder; locate it, inspect its schema by script
only (never load the raw JSON into your context), and build parse.py against what is actually
there.

Finish by writing build/handover/MANIFEST-1-COMPLETE.md in the format plan.md defines.
Commit and push your work (verify git status shows no export files first).
```

## Prompt M2

```
You are Manifest 2 of the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

Poll for build/handover/MANIFEST-1-COMPLETE.md. If absent, wait 60 seconds and check again;
loop until present. When present, read it first, then the four seed files in build/
(communitycompetitions.md, spec.md, plan.md, brainwave.md).

Execute Manifest M2 exactly as specified in build/plan.md (Substance: rules, taxonomy,
report schema). Plain English throughout; the reader must be able to evaluate the system
without the system's vocabulary.

List every rule you author with its justification in your handover. Flag disagreements with
the seed files; never silently override.

Finish by writing build/handover/MANIFEST-2-COMPLETE.md. Commit and push (verify git status
shows no export files first).
```

## Prompt M3

```
You are Manifest 3 of the orchestrator-flight-recorder build.

Working directory: C:\Users\alexa\github_repos\orchestrator-flight-recorder

Poll for build/handover/MANIFEST-2-COMPLETE.md. If absent, wait 60 seconds and check again;
loop until present. When present, read it first, then the four seed files in build/.

Execute Manifest M3 exactly as specified in build/plan.md (Enforcement): check.py, the test
cases, the negative fixtures that verify the verifier, tests/verify.py, and CI. Every
negative fixture must fail on its named check; assert N/N in verify.py.

Finish by writing build/handover/MANIFEST-3-COMPLETE.md. Commit and push (verify git status
shows no export files first).
```

## M4 and M5

M4's prompt is issued after the human writes build/handover/M4-INTAKE.md (incidents chosen
from the scout report, sensitivity ruled). M5's prompt after M4 review. Drafted at the halt,
so intake decisions are baked in rather than patched around.
