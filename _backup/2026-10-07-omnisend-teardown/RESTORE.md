# Insane Fits - Omnisend teardown 2026-10-07

Visos 7 įjungtos automatizacijos ir gyvas 10 % popup'as **ištrinti** iš Omnisend
paskyros 2026-10-07 (Luko sprendimas, komandos susitarimas). Čia yra viskas, ko
reikia atkūrimui.

## Kas ištrinta

| Objektas | ID | Trigger | Laiškų | Last 30d |
|---|---|---|---|---|
| [IF] Welcome serija (eLaiškai 2026-06) | `6a20877a8ac35d6deb9dc574` | subscribed to marketing | 3 | 828 send / 3 703 € |
| Abandoned Checkout Trigger | `64e86ff13f32f55d16ae2d3d` | started checkout | 6 (A/B) | 918 send / 2 345 € |
| Product Abandonment Engagement Split | `6a212c84de553f01826b7d26` | viewed product | 2 (A/B) | 1 641 send / 1 389 € |
| Abandoned Cart Trigger | `6a2137f38305508380599481` | added product to cart | 6 (A/B) | 545 send / 858 € |
| Customer Reactivation | `66d585db069079e2f07b3424` | placed order | 3 | 1 309 send / 281 € |
| Product Reviews | `6a212aec5e898a73f9a36e49` | order fulfilled | 1 | 600 send / 0 € |
| [IF] Nupirko proteiną -> receptų knyga | `6abcd88b2c2ab323fbfa0710` | ordered product | 1 | 30 send / 0 € |
| 10% Popup MOBILE (forma) | `6a2139701a67df459ff5b39c` | popup, device mobile, 15 s, 6 h | - | - |
| 10% Popup DESKTOP (forma) | `6a21394afb74517726d259a2` | popup, device desktop, 10 s, 6 h | - | - |

## Kas NEIŠTRINTA (sąmoningai palikta)

8 jau išjungtos automatizacijos (tarp jų `Copy of: Abandoned Cart Trigger` ir
`Copy of: Product Abandonment Engagement Split` - 2026-09-14 pre-A/B snapshot'ai,
gyvos ištrintų srautų replikos), `Branded Email capture` (embedded),
`Black friday email form` (landingPage), `Main pop-up` + `Insanefits 10% popup`
(seniai disabled), `Signup box No.1` (draft). Kampanijos, draftai, segmentai ir
kontaktai nepaliesti.

## Kaip atkurti

Automatizacijai:

1. `automations/<id>-<pavadinimas>/automation.json` - pilnas objektas: `trigger`
   (su `condition`, `filterGroups`, `inactivitySettings`), `blocks[]` (delay'ai,
   `abTesting` su `aBlocks`/`bBlocks`/`aBlocksPercentage`), `exitConditions[]`,
   `settings` (`frequencyLimiter`, `sendingThresholds`).
2. Kiekvienam laiškui `content-<contentID>.json` = pilnas `email-content` objektas
   (`generalSettings` + `sections`). `POST /api/email-templates` su tuo turiniu →
   naujas `templateID`.
3. `POST /api/automations` su `trigger` + `blocks[]`, kur kiekvienas `sendEmail`
   blokas gauna `temporaryID` + ką tik gautą `templateID` (senų `contentID`
   nebeatkursi - jie mirė kartu su srautais).
4. `POST /api/automations/{id}/enable`.

⚠️ `templateID` suvartojamas tik kuriant bloką. Jau esamo bloko turinio per
`PATCH` nepakeisi - tam `PUT /api/email-content/{contentID}`.

Formai: `forms/<id>-<pavadinimas>.json` turi pilną `content`, `targeting`,
`contactTags`, `doubleOptIn`. `POST /api/forms` su tuo pačiu objektu →
`POST /api/forms/{id}/enable`.

## Ko atkurti NEBEIŠEIS

- Visa srautų statistika ir pajamų atribucija (Omnisende jos nebėra)
- Kontaktai, kurie teardown momentu buvo srautų viduryje (išėjo per
  `contactsInWorkflow: exit`)
- Originalūs `contentID` / `automationID` - atkūrus bus nauji

## Techninės pastabos

- `DELETE /api/automations/{id}` ir `DELETE /api/forms/{id}` **egzistuoja** ir
  grąžina `204`, nors docs puslapyje jų lengvai nerasi. Idempotent: `204` net su
  neegzistuojančiu ID.
- Įjungto srauto trinti **nereikia** pirma išjungti - `DELETE` suveikė iškart,
  be `409`.
- `POST /api/forms/{id}/disable` taip pat yra (nedokumentuota); `/pause` - ne.
- Eksportas: `clients/insanefits/_backup_flows.py`, push: `_push_backup.py`,
  teardown: `_teardown_1007.py`, logas: `_teardown_1007_log.json`.
