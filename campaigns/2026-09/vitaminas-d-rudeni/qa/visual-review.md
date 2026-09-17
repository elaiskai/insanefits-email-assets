# Current HTML review

Date: 2026-09-17

HTML SHA256: `13df64f2ef854b39bf1fcc36ea8263a09e8e4bb9d99159e3ba2c738550b8de6e`

Version: V5 compact quantity pricing and single-line hero headline. Supersedes the V4 QA record.

All screenshots and `../desktop-preview.jpg` rendered fresh from this HTML. Automated measurements are in `automated.json`.

| Viewport | Normal | Head styles and font links removed |
| --- | --- | --- |
| 600 px | PASS | PASS |
| 320 px | PASS | PASS |
| 390 px | PASS | PASS |
| 430 px | PASS | PASS |

All eight fresh full-page previews visually inspected. One font family, readable body widths, intact headings and product names, preserved square hero, 4:5 infographic and 3:2 bundle proportions, correct image and text order, product photos associated with their CTA, no empty columns. The hero headline stays on one line at 600, 320, 390 and 430 px, also without head styles. Desktop falls back from 36 px to a readable 28 px when styles are stripped. Three compact pricing rows fit side by side within each row even at 320 px, no broken amounts or clipped quantity names. Current prices and crossed-out totals match the supplied screenshot: 10,63 / 12,50 EUR, 19,78 / 25,00 EUR, 28,08 / 37,50 EUR. Savings 5,22 and 9,42 EUR verified arithmetically against regular totals. Image callouts remain intact; infographic uses full width. All three CTA have full clickable rectangles and measure 56 px high. No horizontal overflow or missing images. No dash punctuation in customer-facing text, title, alt text or added infographic text. Detailed alt preserves benefit content when images are unavailable.

Direct product URLs checked successfully, linking to the matching product and bundle. Source packaging discrepancy remains an editorial verification item, see README.

Scope: local Chromium browser and importer-style simulation only. Real Gmail/Omnisend delivery NOT verified. Browser layout QA passed for the GitHub review package. Not approved for sending until the README pre-send items are resolved.
