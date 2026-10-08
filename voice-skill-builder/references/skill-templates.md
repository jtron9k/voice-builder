# Templates for the two generated skills

Fill in `<name>` (lowercase, used in the skill names), `<Name>` (as they write it), and the register list. Copy the hard rules that hold across every register into the SKILL.md itself; leave register-specific detail in the reference files.

Replace every placeholder before saving: a skill description cannot contain angle brackets, so a leftover `<Name>` will fail validation.

Both skills ship with the same `references/` folder: one `profile-<register>.md` and one `samples-<register>.md` per register.

---

## Template 1: `write-like-<name>/SKILL.md`

```markdown
---
name: write-like-<name>
description: Draft emails, chat messages, posts, and other text in <Name>'s own voice. Use whenever <Name> asks for a draft of anything they will send or publish as themselves (an email, a reply, a Slack or Teams message, a LinkedIn post, a text), or says "write this like me", "in my voice", or "sound like me", even if they do not mention this skill.
---

# Write like <Name>

Drafts text that <Name> can send without editing the voice. The profiles in `references/` were built from <Name>'s own sent messages; trust them over your instincts about what good writing sounds like.

## Before writing

1. Pick the register from what is being written and who it is for:
   - Work email or chat: `references/profile-work.md`, `references/samples-work.md`
   - Public post: `references/profile-public.md`, `references/samples-public.md`
   - Personal: `references/profile-personal.md`, `references/samples-personal.md`
2. Read that profile and its samples. Find the two or three samples closest to this situation and write toward them.
3. If the request does not say who it is for or what it needs to achieve, and guessing wrong would waste the draft, ask one question. Otherwise draft.

## Rules that hold everywhere

<Paste the cross-register hard rules here, each with a one-line reason. Typical entries: dash habits, greeting and sign-off habits, phrases that never appear, typical length.>

## Calibration

- Match their length. If their median reply is short, a long draft is wrong even if every sentence sounds like them.
- Use rare habits rarely. A phrase that shows up in 3% of their messages belongs in about 3% of drafts. Overusing a signature phrase reads as parody.
- Leave it a little rough where they would. Do not add polish, transitions, or a closing line they would not write.
- Content comes from the request. Never invent facts, names, numbers, or commitments to make a draft sound complete; leave a bracketed gap instead.

## Output

Give the draft alone, ready to copy. For email, include a subject line in their style. Add a note only if you had to guess at something that changes the meaning.
```

---

## Template 2: `<name>ify/SKILL.md`

```markdown
---
name: <name>ify
description: Rewrite existing text so it sounds like <Name> wrote it. Use whenever <Name> pastes or points to a draft (their own rough notes, something a colleague wrote, or AI-written text) and asks to "<name>ify" it, make it sound like them, put it in their voice, or make it sound less like AI.
---

# <Name>ify

Converts text that already exists into <Name>'s voice. This is an edit, not a rewrite from scratch: the meaning, the facts, and the order of ideas stay put unless they get in the way of sounding like <Name>.

## Steps

1. Work out the register (work, public, personal) from the text and where it is going. Read the matching `references/profile-<register>.md` and `references/samples-<register>.md`.
2. Strip what <Name> never writes: <list the "never appears" items from the profile, for example stock openers, stacked adjectives, summary closers>.
3. Bring length toward their normal range for this kind of message. This usually means cutting.
4. Swap in their habits where they fit naturally: openers, closers, punctuation, contractions, how they ask for things. At the rate they actually use them.
5. Read it against the two closest samples. If a sentence could not sit next to those samples, fix that sentence.

## Guardrails

- Keep every fact, name, number, date, and commitment from the original. If something looks wrong, flag it rather than changing it.
- Do not add content, jokes, or opinions that were not in the original.
- If the source is already close to their voice, change little and say so.

## Rules that hold everywhere

<Same cross-register hard rules as in write-like-<name>.>

## Output

Return the rewritten text alone. If you cut or changed anything that affects meaning, list it in one line underneath.
```

---

## Samples file format

`references/samples-<register>.md`:

```markdown
# <Name>: <register> samples

Verbatim, lightly redacted. Typos are original and intentional to keep.

## 1. <Situation, for example "Quick yes to a meeting request">
<message text>

## 2. <Situation>
<message text>
```

Choose samples for range over quantity: a one-liner, a scheduling note, a decline, a request, a longer explanation, something funny. Label each with its situation so the writing skill can find the closest match.
