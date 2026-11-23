# UI quality rules

Ten rules for every screen and every piece of user-facing text in this repository: the register, receipt print view, operator panel, refund lookup, cash-up screen and the head-office summary page. Rules 1 and 2 were stated by the owner; rules 3 to 10 were proposed and approved by the owner on 2026-11-22. All ten are binding. Changing one needs the owner ([owner-decisions.md](owner-decisions.md), entry 12).

Colours, type, spacing and radii come from the shared tokens in [design-tokens.md](design-tokens.md); new UI uses them and adds no colour literal.

No UI source exists yet, so nothing has been checked against these rules. The tickets that build screens (#2, #5, #6 and the register-depth ticket, planned as #9) name this file in their acceptance criteria.

1. No thick accent border on one side of a card, callout, alert, list item or quote (for example `border-left: 4px solid <accent>`). Use spacing, type weight, an icon or a full hairline border instead.
2. No soft tinted background with a thin border of the same hue as the default way to mark a status, tag, callout or card. One neutral surface and one clear signal (text, icon or a solid chip) is enough.
3. No gradient text and no purple-to-blue gradient as a default accent.
4. No blur or glass panels, and no drop shadow plus large radius on every card.
5. No emoji used as icons or bullets, and no sparkle marks.
6. No pill or badge on things that are not states. No all-caps, letter-spaced micro labels as section decoration.
7. No centred hero with a slogan in an application screen. Screens open on the user's task.
8. One accent colour, used for the primary action and the current selection. Status colours only for status.
9. Dense, aligned layouts on a consistent spacing scale. No card grid where a table or a list is the right form.
10. User-facing copy is plain and specific: no filler, no exclamation marks, and the same word for the same thing everywhere.

## How they are applied

- A UI ticket starts with the `ui-ux-pro-max` skill (`.claude/skills/ui-ux-pro-max/`, design-system search for a retail point of sale) and ends with a check of every changed screen against the ten rules. The check is recorded in the pull request.
- Copy, documentation and pull request text go through the `unslop` skill (`.claude/skills/unslop/`) before the pull request is opened.
- Code Reviewer checks the rules on every ticket that touches `static/` or user-facing text; Frontend Developer and Accessibility Auditor name this file in their checklists.
- Rule 1 can be searched for in CSS (a `border-left` or `border-inline-start` wider than 1px next to an accent colour). Rule 2 cannot be detected reliably by a script, so review enforces it.
- This product is keyboard first and prints receipts: status must also read in plain text, not by colour alone.
