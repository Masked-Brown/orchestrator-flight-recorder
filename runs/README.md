# Runs

Real investigations, shipped whole. Written in build stage M4.

Each run gets a folder containing the incident statement as it was actually given, the message
manifest the investigator worked from, the report it produced, and the result of putting that
report through `check.py`.

Two rules govern what lands here:

**The runs are real.** They come from a genuine export of a genuine working session, not from
a scenario written to make the tool look good. Anything constructed to demonstrate a mechanism
is labelled as constructed, everywhere it appears.

**The excerpts are windowed and swept.** Only the stretch of conversation relevant to the
incident is shipped, and it is reviewed by a human before it is committed. The raw export
never enters version control.
