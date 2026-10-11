# Interpreter correction before batch inference

October 5, 2026. The first B/C/D launch exited 1 before conversion or inference:
`python3` resolved to `/usr/bin/python3` version 3.9.6, which lacks
`hashlib.file_digest`. The runner created an empty `run03-bcd` directory before
this exception, with no receipt or model output. Tool receipt `e69e6f` preserves
the exception. The interrupted turn had not launched a replacement process.

Fresh inspection confirms the directory is empty. Preserve it as
`run03-bcd-launch01-empty`, then execute the unchanged runner explicitly with
`/Users/admin/.pyenv/versions/3.13.7/bin/python3 -B`. This is the installed
interpreter family used for the prior successful trial. The new self-test
passes three valid and ten invalid invented cases and confirms decoding
arguments match A. No dependency installation, model, speech setting, source
or acceptance rule changes. No inference attempt was consumed by the failure.

Unchanged runner SHA-256:
`4f948cd9b7acefdc1b053ce3e1666595195bd9c9a486f5ac46ddb88f0fc0b7de`.
Unchanged batch protocol SHA-256:
`83e4818b319cba277875229280d1b7351cf0b15e81376be1af416fc251122549`.

The earlier self-test passed on Python 3.9 because it did not exercise the
hashing helper. That test therefore did not establish interpreter readiness.
Future invocations should name the verified interpreter rather than rely on
the ambient `python3` command. The failed launch remains part of the record.
