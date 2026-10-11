# OEM followup acquisition and review record

October 4, 2026. Research only. The prospective [protocol](PROTOCOL.md) was
saved before retrieval, SHA256
`bef0e57dc5993c8c1061235f97987aa57b2b77f022ec6139724d895bb08296e6`
(`7e8a72`, exit0). Its target URLs came from the existing September 16 lead
memo, not guessed adjacent Bates identifiers. Root read that complete memo
again (`5ff2db`, exit0). Catalog labels remained unverified contents.

## Retrieval and preservation

The capture window was 13:52:47-13:53:40 UTC. One direct GET per exact URL,
concurrently dispatched, no repeats. curl 8.7.1 was the same runtime verified
in the parent acquisition. Each command used:

```sh
curl -q --silent --show-error --proto '=https' --no-location --retry 0 \
  --connect-timeout 10 --max-time 40 --max-filesize 10485760 \
  --output /private/tmp/wtc7-oem-followup.FDbgsl/<ID>.response \
  --write-out '{"http_code":"%{http_code}","url_effective":"%{url_effective}","content_type":"%{content_type}","size_download":%{size_download}}\n' \
  https://sept11documents.cityofnewyork.us/apps/content/September11_MD/<ID>.pdf
```

The literal IDs were NYC-WTC_000173199 and NYC-WTC_000172166. No response
headers, cookies or credentials were captured or sent; user curl config was
disabled. Each effective URL equaled its requested URL.

| Preserved source | Actual response and terminal status | SHA256 |
| --- | --- | --- |
| [NYC-WTC_000173199.pdf](NYC-WTC_000173199.pdf) | HTTP200, application/pdf,333388bytes; initial handle90208, polled to exit0 (`0c7ec3`). | `37b65cb843cd81716df26af8780627e27bed6d0557eb4b3419945ef742495903` |
| [NYC-WTC_000172166.pdf](NYC-WTC_000172166.pdf) | HTTP200, application/pdf,147759bytes; exit0 (`205a2b`). | `362ad11e3e7b5ac89183be9fa0095f2b0803518e3c854a77ae34f8e626012193` |

`file` and `shasum` confirmed PDF1.5 and captured bytes (`04da8e`, exit0).
`pdfinfo` independently found6/2pages, no forms/JavaScript, unencrypted,
ABBYY/iText/Nuix processing metadata (`500e3e`/`cd81a5`, exit0). The August12,
2026 modification dates are not historical issue or release dates. Properties
are not a security or historical-authentication certification.
Approved `cp -n` commands preserved both files without overwriting (`a1185d`,
exit0); later source hashes matched (`8e39fd`, exit0). Official portal headers,
consecutive Bates and body identity were checked in the subsequent full reading.

## Page derivation and root coverage

Root created only the temporary render directory (`066510`, exit0) and ran:

```sh
pdftoppm -f 1 -l 6 -r 150 -png /private/tmp/wtc7-oem-followup.FDbgsl/NYC-WTC_000173199.response /private/tmp/wtc7-oem-followup.FDbgsl/render/173199
pdftoppm -f 1 -l 2 -r 150 -png /private/tmp/wtc7-oem-followup.FDbgsl/NYC-WTC_000172166.response /private/tmp/wtc7-oem-followup.FDbgsl/render/172166
```

Poppler26.05.0, same runtime as the parent. Both handles were polled, not
restarted:85831 to `f8a560`,12157 to `866fbf`, both terminal exit0 without
renderer warnings. Eight expected files were enumerated (`42e1be`, exit0),
then copied unchanged with approved `cp -R -n` (`730181`, exit0). The complete
saved set was hashed (`8e39fd`, exit0):

| PNG in render | SHA256 |
| --- | --- |
| 173199-1.png | `0801d39df1b19903c6bbe469d7f96ea90ac547571394e5468932c9b01a048f62` |
| 173199-2.png | `32f93b41f342789be67762b146052aa4e156053db28e6637d453ac61f5dd59b6` |
| 173199-3.png | `9c74ec79024f7e23b50e022f7797f3a5d03ebbe940cbbfa9f0cc6ceb106de1a1` |
| 173199-4.png | `cd721595feb50da44709c482040f2c1299e19322adc2204f01c1705b392e2553` |
| 173199-5.png | `01821bed2c8209a0bd12de3a85c1a874a8c509cf5d65552c4dab266f5d025907` |
| 173199-6.png | `623e27eed964881f62003a50a8f8e69c3b4fea9042eba1dd562b4f31b4d4e12d` |
| 172166-1.png | `128e33b4d14e6a8cdaf27b5e2fbf7caecbe7ccac16c5635d7a7a874e836f6812` |
| 172166-2.png | `08fd0c5c4deece650e673a046ae573d9785eb859864b4af2c4ce71054b6c866e` |

Root displayed every full page once at original detail, in the protocol order,
with no retries, crop, enhancement or OCR. [root-observations.md](root-observations.md)
froze at SHA256 `f7a55784f03e5a646ba811b97c9364623dcc0853e54946a477305bce26197e78`
(`f4739b`, exit0) before receiving substantive peer findings. The initial
routing overlay, fax context and small product-diagram text remain qualified;
no missing text was manufactured. Historical contact details and author paths
are not proposed for external disclosure. Separate review and derivative
checks have their own attributable records; their completion is not inferred
from delegation.

## Independent completion and corrections

The separate reader completed all eight first-view displays and froze
[review.md](review.md), SHA256
`454c8d7c297bb1e05ae78bada52f9c8e8476e4dab1b7cbd3196b2e2ce5cbf618`
(`15acec`, exit0), before reading root's findings. Its source-pin check passed
(`947bc6`, exit0). After both freezes, the reader read root's note (`9507f7`,
exit0) and confirmed both note hashes unchanged (`41e2ba`, exit0), finding no
material disagreement. Root read the complete peer record (`48aefb`, exit0).
Total source interpretation: sixteen full first-page views, zero repeats,
shared sources and no claim of independent historical corroboration.

The separate [derivative check](derivative-check.md), SHA256
`005f7302f3bf5221afb5ebed476e3a47ff055c0f8a5d5d020ec8d8833b6eea8c`,
re-rendered each PDF once into a fresh temporary directory and compared all
eight PNGs. Both renders reached exit0 without warnings; all eight byte and
hash comparisons matched. No failed source acquisition or render occurred in
this follow-up; the parent web-reader failures remain preserved separately.

A final complete text-only peer check (`5a2f3f`, exit0; reviewed draft
SHA256 `da36e34353e091565c22825cf6c32fe6c5e62d78bdc5f5ddf2ab7991155139be`)
identified one wording correction: "earlier deficiencies" might imply proven
installed defects. Root changed the question to whether the earlier review
comments were resolved and requested corrections completed. The frozen reading
record remained unchanged (`9626f8`, exit0). The report otherwise preserved
date, issuance, project-link and acceptance distinctions. No second source
reading was performed for this text review.

Root read the complete independent derivative receipt (`35706f`, exit0).
The [parent completion receipt](../source-log.md) records the final thirteen
frozen-file, nineteen-render and thirty-eight-link checks across both units,
the successful diff check, preserved WIP and final report hashes. Those checks
do not promote the source statements to engineering or historical findings.
