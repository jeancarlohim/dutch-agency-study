# Coverage report — the mapping run

Aug 7, 2026. What the seven approved category lists could and could not
place, how accurate the placement is, and what JC needs to know about it.

Two passes were used. First a keyword rule pass, written straight off the
membership rules in each approved list. Then Sonnet agents on whatever the
rules could not place with a clear winner. Anything neither pass could place
is written as "unknown" — never guessed.

## 1. How much landed

"Mass" = case occurrences, not distinct phrasings. The focus scores are
computed per case, so mass is the number that matters.

| Focus type | Cases stating it | In a real bucket | Unknown | Placed by rules | Placed by the model pass |
|---|---|---|---|---|---|
| what the client's business is | 8727 | 8264 (95%) | 463 (5%) | 64% | 31% |
| what they sell | 23863 | 20719 (87%) | 3144 (13%) | 77% | 10% |
| the problem they fix | 5096 | 4153 (81%) | 943 (19%) | 31% | 50% |
| platform or channel | 6799 | 6603 (97%) | 196 (3%) | 90% | 7% |
| the client's money model | 1876 | 1756 (94%) | 120 (6%) | 78% | 16% |
| the client's size | 1335 | 1231 (92%) | 104 (8%) | 63% | 30% |
| where the clients are | 4525 | 4350 (96%) | 175 (4%) | 85% | 11% |

Across all seven: **47076 of 52221 stated values (90%) landed in a
real bucket.**

## 2. How accurate it is

For every focus type, 80 phrasings the KEYWORD RULES had placed were sampled
(weighted by case mass, so the phrasings carrying the most cases were the most
likely to be checked) and re-read from scratch by a separate Sonnet agent that
was told not to defer to the rule. Agreement is the honest accuracy floor for
the rule half of the run.

| Focus type | Agreement of an independent second read |
|---|---|
| what the client's business is | 69/80 |
| what they sell | 71/80 |
| the problem they fix | 66/80 |
| platform or channel | 64/80 |
| the client's money model | 69/80 → 68/80 (after the rule fix) |
| the client's size | 71/80 → 75/80 (after the rule fix) |
| where the clients are | 64/80 → 69/80 (after the rule fix) |

Where the first audit exposed a systematic rule bug, the rule was fixed and
the audit re-run on a fresh sample. Three focus types went through that loop:
where the clients are, the client's size, the client's money model.

The disagreements that remain are mostly genuine judgement calls on text that
names several things at once ("branding & website", "seo sea"), not clear
errors. The rules break those ties by taking whichever bucket the text leads
with; a human reader would sometimes take the one that dominates instead.

## 3. Findings JC needs to decide on

### The platform-or-channel list contradicts itself

Bucket 2 says paid ads on a named social platform "go to bucket 3". Bucket 3
is the ORGANIC social bucket; bucket 4 is the paid one. The cross-reference is
a leftover from the 13-bucket draft, before the social bucket was split into
paid and organic. This run followed bucket 4's own definition — a paid marker
on a named social platform files under "Social media paid". **The list should
be corrected before it is quoted anywhere.**

### "Zakelijke afnemers" and "Dienstverleners" overlap by construction

A consultancy sells services (bucket 6) to businesses (bucket 1). The approved
tie-break ("webshop form > software-as-product > explicit both > audience")
does not say which of those two wins. This run checks the audience first, so
service sellers with business customers land in bucket 1. An independent read
preferred bucket 6 in those cases. No test runs on this focus type — the
approved list already marks it descriptive-only — so it was left as is rather
than re-run.

### No new buckets were needed

Per the handoff, no category was invented. Nothing in the data formed a large
cluster with no home in the approved lists. What falls to unknown is not a
missing category — it is text that states nothing about that focus type.

## 4. What "unknown" actually is

The biggest unknown group by far is text that carries no value for that focus
type at all: taglines, campaign titles, testimonials, bare client names, result
claims. A sample of the largest unknowns per focus type:

**what the client's business is** — "zakelijk" (23) · "marketing" (19) · "overig" (17) · "b2b" (12) · "ondernemer" (6) · "onderzoek" (6)

**what they sell** — "overig" (42) · "afval sorteren" (11) · "houd de lijn vrij!" (10) · "naamsbekendheid vergroten" (9) · "merkbekendheid" (9) · "verbindt ondernemers in ede" (8)

**the problem they fix** — "wil met haar afnemers en architecten duurzame ge" (6) · "als franchisegever maximaal impact maken met onl" (5) · "gaat u (ver)bouwen en bent u op zoek naar het be" (5) · "van hard schreeuwen naar verleiden" (5) · "hoe zorg je op een laagdrempelige manier dat íed" (4) · "slimme aanpak van onnodige armoede" (4)

**platform or channel** — "google" (41) · "online" (14) · "ai" (13) · "google only" (4) · "lokale marketing" (3) · "search" (3)

**the client's money model** — "leadgeneration" (6) · "super tevreden met onze nieuwe website. de samen" (5) · "marketplace" (4) · "everybody - regardless of their background - is " (2) · "het zijn voornamelijk vrouwen die zich met hart " (2) · "de samenwerking verliep soepel en het contact wa" (2)

**the client's size** — "webshop" (3) · "een makelaar met meerdere vestigingen" (2) · "als onderdeel van de mandemakers groep" (2) · "met een betrokken team van vrijwilligers" (2) · "multiple locations in london, uk" (2) · "landelijke vereniging zonder winstoogmerk" (2)

**where the clients are** — "dutch" (5) · "the dutch salvation army" (4) · "ish noviteitenbeurs" (4) · "een van de grootste nederlandstalige nieuwssites" (3) · "bestaande én nieuwe markten" (3) · "een vooraanstaand belgisch bedrijf" (2)

## 5. How much the tagging misses can move an answer

Measured, not assumed. Every client tag was knocked to a different bucket
with a 15% chance — worse than the measured miss rate — and the focus scores
were recomputed. 400 runs, on the real portfolios, on what they sell.

**One agency on its own.** Its focus score moves by more than 10 points in
16–36% of runs, at every portfolio size. A single agency's score is not
trustworthy and never will be. Do not build an example around one agency.

**One group on its own.** The middle score of a group drops by about 4 points
and stays there no matter how many agencies are added. That is because the
misses do not cancel out — a wrong tag almost always makes a portfolio look
more spread than it is. More agencies fix noise; they do not fix a lean.

**Two groups compared** — the thing actually reported. The lean hits both
sides equally, so most of it cancels in the subtraction:

| Agencies per group | Typical move in the gap | Worst in 100 runs |
|---|---|---|
| 10 | 5 pts | 17 pts |
| 20 | 4 pts | 13 pts |
| 30 | 4 pts | 13 pts |
| 40 | 3 pts | 10 pts |
| 50 | 3 pts | 10 pts |
| 75 | 3 pts | 10 pts |
| 100 | 3 pts | 8 pts |
| 150 | 3 pts | 8 pts |

Two rules follow, and they are what JC should hold onto:

1. **At least 40 agencies on each side of a comparison.** Below that the gap
   can swing 13–17 points on tagging misses alone.
2. **A gap under 10 points is not a finding**, at any group size. The floor
   does not go away by adding agencies — it is set by the tagging.

The 15-point narrowing threshold clears that floor. The groups available
clear the 40 (68 agencies that changed their message, 146 twins).

## 6. Two limits worth stating plainly

1. **The problem they fix is the weakest focus type**, and was always going to
   be. It is stated in only 16% of cases, it is written as free narrative
   rather than labels, and the approved list was locked knowing ~74% of
   phrasings would land cleanly. It came in at 81%. Treat any result resting
   mainly on this focus type as weaker than the others.
2. **Every focus score is about the published portfolio**, not the client
   base. That was already the study's standing rule; the mapping does not
   change it.

