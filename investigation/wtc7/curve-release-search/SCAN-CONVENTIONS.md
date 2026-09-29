# Prospective byte-locator conventions

These conventions supplement PROTOCOL.md before either new historical body
scan. Independent method design prompted clarification, not a result mismatch.

- Physical lines are separated only by byte LF (`0a`); a terminal LF does
  not add an empty line. Empty bytes have zero lines. A line's length/cap
  includes its LF when present. Counts are byte-oriented, not Unicode lines.
- Preserve one-based physical line, zero-based byte column and zero-based
  absolute byte offset for every literal hit. Search uppercased bytes for
  each ASCII, UTF16LE and UTF16BE family stem at any byte alignment. Overlapping
  encoding-pattern matches, if present, stay separate; they do not authenticate
  that the file uses that encoding. UTF32, compressed subpayloads and dynamic
  generation are not evaluated.
- A suffix is present only when the next character in the matched encoding
  is an ASCII letter, digit or underscore. Otherwise mark the literal as base.
  This lexical label does not establish a syntactically valid definition.
- Line-leading means that the bytes between this LF-based line start and
  the hit are solely space/tab/CR in the hit's encoding. Only an initial
  UTF8 BOM at absolute offset zero may be removed before this test. No UTF16
  BOM or unmatched NUL is silently stripped. Odd-length UTF16 prefixes cannot
  pass the encoded-whitespace test. Thus the LF-based leading flag is not
  a general Unicode keyword parser; literal opportunity-to-detect remains
  the full-byte marker search, not the narrower leading flag.
- Per-body NUL count and bytes with value above127 are separate. Preserve
  an all-NUL flag and initial UTF8-BOM flag, without interpreting binary data
  as source code. Commented/quoted hits remain in the literal output; their
  runtime status is not inferred.

Both readers must pin this supplement as well as the base protocol. Subsequent
comparison may adapt schemas but must compare all declared common locators
and flags, rather than changing these conventions to fit the results.
