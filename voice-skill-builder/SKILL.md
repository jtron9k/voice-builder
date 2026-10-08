---
name: voice-skill-builder
description: Build a personal "write like me" skill and a matching "me-ify" rewrite skill from someone's own sent emails, chat messages, and posts. Use whenever the user wants Claude to write in their voice, sound like them, stop sounding like AI, clone or capture their writing style, build a voice profile or style guide from their own writing, or asks for a "write like me", "meify", or "(their name)-ify" skill, even if they never say the word skill.
---

# Voice skill builder

Builds two skills for one person, from evidence:

- `write-like-<name>`: drafts new emails, messages, and posts in their voice.
- `<name>ify`: rewrites existing text into their voice.

The idea that makes this work: measure first, describe second. "Casual but professional" is useless as an instruction. "Median reply is 18 words, three out of four replies skip the greeting, zero semicolons in 900 messages" is something a model can actually follow. So the job is to collect a real corpus of the person's own words, count things, read for patterns, and write rules that cite the evidence.

Work through the steps in order. Tell the user what you found at each stage. Do not skip the review in step 6: the person is the only one who can say whether the profile is right.

## 1. Scope it

Ask, in one round:

- What first name or handle should the skills use? (`write-like-sam`, `samify`)
- Which registers matter? Typical set: **work** (email and chat), **public** (LinkedIn, blog, newsletter), **personal** (personal email, texts). One is fine to start.
- Where does their writing live, and which of those can you reach right now? Check your connected tools before asking (mail, chat, drive, browser). If nothing is connected, ask them to paste or upload exports.
- Is there anything they already know they hate in writing? Write these down word for word. Stated dislikes are the strongest signal you will get.

## 2. Collect the corpus

You want text the person typed themselves. Nothing else.

Pull from **sent** items only. For each register aim for 200+ messages; 50 is a workable floor; under 50, build it anyway and say plainly that it is thin.

Keep each register in its own folder, one message per file, saved to disk in full **before** you analyze anything. Reassembling messages from memory or tool output later corrupts the exact wording and typos, which are part of the voice.

```
corpus/
  work/      0001.txt 0002.txt ...
  public/    ...
  personal/  ...
```

Clean each message down to their words:

- Cut quoted reply chains, forwarded content, and legal footers.
- Keep their sign-off and any signature line they clearly typed or chose ("Sent from my phone, pardon typos" is voice; a corporate address block is not).
- For posts, drop plain reshares and any text quoted from someone else.

Leave out entirely:

- Automated mail, calendar responses, forwards with no words of theirs.
- Anything that reads as AI-drafted or ghostwritten. Ask the user which recurring items those are (weekly updates and newsletters often are). Including them teaches the skill to sound like the AI they are trying to get away from.
- Anything containing passwords, keys, account numbers, or booking codes.
- Sensitive threads by default: medical, therapy, legal, tax and finance, HR and payroll, bereavement, anything about their kids. These are often where a person writes longest, so tell the user they were skipped and let them choose what to add back. Do not read them without a yes.

Note for the record: date range, count per source, what was excluded, and what was never sampled. This goes in the profile so that later readers know how far to trust it.

## 3. Measure

Run the bundled script on each register folder:

```bash
python scripts/voice_stats.py corpus/work --label work
python scripts/voice_stats.py corpus/public --label public
```

It reports length medians, sentence length, dash and punctuation habits, contractions, exclamation and question rates, emoji, bullets, apostrophe style, greeting and sign-off frequencies, and casual-spelling counts. It prints JSON you can paste into the profile.

If the corpus spans years, also split by period and compare. People change. Weight the most recent 12 months and note where older writing differs (it is common to find far more emoji, hashtags, and exclamation points three years back).

Be careful with comparisons across registers. If two numbers were counted differently, say "similar", not "equal".

## 4. Read for patterns

Numbers miss the moves. Read at least 50 messages per register, including the longest ten, and write down what you see with a real quoted example for each:

- **Openers and closers.** How do they start a new note versus a reply? How do they end?
- **Shape.** One-line paragraphs? Bullets or inline lists? Headers ever?
- **How they do the hard things.** Saying no. Pushing back. Apologizing for a late reply. Asking for something. Giving praise. These are the moments a generic draft sounds most fake.
- **Humor.** Deadpan, self-deprecating, absent? Set-up and punchline or a short aside?
- **Emphasis.** Caps on one word, italics, exclamation points, nothing?
- **Vocabulary.** Recurring phrases, abbreviations, pet words, regionalisms. Count them.
- **Absences.** What common phrases never appear? ("I hope this finds you well", "circle back", "let me know if you have questions".) Zero occurrences in hundreds of messages is evidence.
- **Imperfections.** Typos, missing commas, lowercase starts. These survive in real writing and should mostly survive in drafts.
- **Their own stated opinions on writing**, if any show up in the corpus.

## 5. Write the profile and samples

Create two reference files per register, using `references/profile-template.md` as the skeleton:

- `profile-<register>.md`: source set and limits, headline numbers, patterns with examples, then rules.
- `samples-<register>.md`: 10 to 25 verbatim messages chosen for range (one-liner, scheduling, a decline, a longer note, a joke). Samples do more than any rule, because the model can pattern-match on them directly.

Split the rules into two tiers and be honest about which is which:

- **Hard rules**: things the person told you, plus habits with essentially no exceptions in the data.
- **Soft defaults**: strong tendencies. Give the number so the model can calibrate ("skips the greeting on about three out of four replies").

Redact the samples: remove phone numbers, addresses, account details, and recipient email addresses. Swap third-party full names for first names or roles unless the user says otherwise. Samples live inside a skill file, and skill files get shared.

## 6. Review with the person

Show them the headline numbers, the pattern list, and the rules. Ask three things:

1. What here is wrong or surprising?
2. What is missing that you know you do?
3. Is anything in the samples something you would not want sitting in a file?

Fix the profile from their answers. Promote anything they feel strongly about to a hard rule.

## 7. Generate the two skills

Build from `references/skill-templates.md`, filling in the name and registers. Layout:

```
write-like-<name>/
  SKILL.md
  references/  profile-work.md  samples-work.md  (one pair per register)
<name>ify/
  SKILL.md
  references/  (same files)
```

Each SKILL.md should stay short: when to trigger, how to pick the register, the handful of hard rules that apply everywhere, and a pointer to read the matching profile and samples before writing. The detail belongs in the reference files so only the relevant register gets loaded.

Two things the generated skills need to say clearly, because they are where voice skills usually go wrong:

- **Do not exaggerate.** If a pet phrase shows up in 5% of messages, it belongs in roughly one draft in twenty, not every draft. A caricature is easier to spot than plain AI prose.
- **Do not polish them into someone else.** For the rewrite skill especially: keep their content and structure, change as little as needed, and leave a rough edge where they would.

Package each folder as a `.skill` file (a zip of the folder with a `.skill` extension) if you have a way to deliver files, so the user can install it.

## 8. Test and tune

Have the new skill write three things the person actually needs this week, one per register if there are several. Then:

- Run `voice_stats.py` on the drafts and compare against the profile. Length and punctuation should land near their medians.
- Ask the user to mark every phrase they would not have written. Each one becomes either a new rule or a correction to an old one.

Record the misses in the profile under "known gaps". A voice profile is never finished; the useful ones get corrected a few times in the first month.

## Honesty about limits

Put these in the profile, not in a footnote:

- How many messages, from when, and what was skipped.
- Which findings rest on fewer than about 20 examples.
- That text alone cannot prove a given message was not AI-assisted.

And one boundary: build this only for the person whose writing it is, or with their clear say-so. A voice skill for someone else's voice, built without them, is impersonation.
