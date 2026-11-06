# Biederman’s 2005 and 2006 WPI steel presentations

An attachment encountered while looking for Sisson and Biederman’s October 2006 case history contains a separate 89-page presentation. Its title slide identifies Ronald R. Biederman and the Higgins Armory/WPI MCSI Symposium on **June 5, 2006**. The WPI-hosted copy of the presentation names **June 8, 2005**. Both versions and their dates are preserved. The 2006 copy is publicly accessible through a forum attachment, with no institutional delivery or native slide file verified. [WPI PDF](https://web.wpi.edu/Images/CMS/MCSI/2005biederman2.pdf#page=1) · [2006 PDF attachment](https://www.metabunk.org/attachments/2006biederman-pdf.2412/) · [Upload context, post 683](https://www.metabunk.org/threads/wtc-7-building-7.1094/post-38917)

## Observations

| Physical PDF page | WPI-hosted 2005 copy | 2006 attachment |
|---|---|---|
| 1, extracted text line 9 | `June 8, 2005` | `June 5, 2006` |
| 20, second image occurrence | 1,500 × 1,167 pixels. One dimension of the placed image extends past both slide edges. | 1,500 × 1,125 pixels. The image placement differs. A 200 μm scale bar is visible in both. The recognizable features overlap, with framing differences. |
| 33, 37, 38, 39, 43 and 61 | Six differing page renders, with the image digests preserved in the comparison record. | Each corresponding image has the same pixel dimensions as in the 2005 copy. The corresponding fields and visible scale bars appear alike in side-by-side review. Pages 37–39 reuse one changed image in each copy. |

At a fixed 718 × 538 RGB render in PyMuPDF 1.27.2.2, **eight of 89 pages differ**. Page 20 has 33,244 pixels with at least one channel differing by more than 16 on the 0–255 scale. Among the six other image pages, the corresponding counts range from **2 to 45**. This cutoff describes the rendered differences and has no calibrated significance for microscopy. The comparison covers all pages for extracted text, page size and rotation, raster pixels, and decoded embedded image digests. Visual inspection covers the seven image pages in a paired contact sheet. The files have different hashes and sizes. [Comparison code](compare_decks.py) · [Per-page results and embedded PDF metadata](COMPARISON.json) · [Source pins](SOURCE-PINS.json)

Page 1 is the only page with changed extracted text. Pages 79–83, covering the furnace run, its micrograph, and its labeled EDS spots, have identical renders in this comparison. Page 79 calls the tested material **A36**, and page 80 labels the field **A36 Steel**. The separate proceedings candidate describes an **A36** run in its text and uses **HSLA column material** in its Figure 13 caption. The 2006 deck repeats the 2005 presentation at these locators. The section of the earlier study that preserved the grade discrepancy remains open. [WPI deck, pp. 79–83](https://web.wpi.edu/Images/CMS/MCSI/2005biederman2.pdf#page=79) · [Earlier figure and specimen-label comparison](https://github.com/AveLyra/911-conspiracy-investigation/blob/82a53d4d244740c32b6b8d56bb88ea35c09fa0ec/investigation/broader-evidence/steel-wpi-furnace-paper-candidate-2026-11-06/README.md)

## Interpretation and limits

The matching fields and labels across both presentations make them useful for tracing figure versions. The image differences matter if someone wants to measure grain sizes or areas using a particular slide version, especially page 20, where the raster size and placement differ. Re-export, compression and reframing are untested explanations. The cause of the differences, the original image acquisition settings and the physical specimen mapping remain unverified. Both decks come from the same line of work and supply no independent specimen identification.

The October 2006 journal case history remains a separate source. Its publisher identifies it as a five-page article and its public abstract reports localized temperatures above **940 °C** and proposes material loss during exposure to post-collapse rubble fire. The abstract gives the authors’ interpretation. This review did not examine the article’s full reasoning or verify the separate recovery-location account quoted in a later appeal. [Publisher record and abstract](https://link.springer.com/article/10.1361/154770206X129006) · [Appeal, printed p. 69, quotation attributed to the case history](https://ic911.org/wp-content/uploads/2023/08/appeal-of-nist-initial-decision-wtc-7-rfc-09-28-20_public.pdf#page=69)

## Open records

- [ ] Locate the exact October 2006 journal article through a publicly available authorized copy. Check its pages 17–21 for the specimen identifier, recovery account, figures, and basis for dating the corrosion.
- [ ] Locate an institutional copy or archive capture of the 2006 presentation, plus the native slide deck and original micrograph and scale calibration for page 20. Test whether the same source field and quantitative scale were used.
- [ ] Locate the furnace-run notebook, specimen and mount IDs, and native image/EDS data. Trace the A36 and HSLA labels to the physical coupon before assigning a grade to Figure 13.
- [ ] Keep the earlier steel recovery and accession records outstanding. A title date, a PDF timestamp, or repetition of the image cannot supply custody.
