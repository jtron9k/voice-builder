# Voice Skill Builder

A Claude skill that builds two more skills for you, from your own writing:

- `write-like-<you>` drafts new emails, messages, and posts in your voice.
- `<you>ify` rewrites existing text so it sounds like you wrote it.

Most "write like me" prompts describe a voice in adjectives ("casual but professional"). This one measures it. It pulls a corpus of things you actually sent, counts your habits (length, dashes, greetings, sign-offs, contractions, pet phrases), reads for how you say no or ask for things, and writes rules that cite the evidence.

## Install

**Claude (web or desktop)**

1. Download [`voice-skill-builder.zip`](voice-skill-builder.zip).
2. In Claude, go to Customize > Skills, click "+", then "Create skill" and "Upload a skill".
3. Upload the ZIP.

Skills need code execution turned on (Settings > Capabilities > "Code execution and file creation"). On Team and Enterprise plans your admin may need to allow user-created skills. Details: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

**Claude Code**

```bash
git clone https://github.com/jtron9k/voice-builder
cp -r voice-builder/voice-skill-builder ~/.claude/skills/
```

## Use

Start a chat and say:

> Build me a "write like me" skill.

Claude will ask what to call the skills, which kinds of writing matter (work, public, personal), and where your writing lives. It works best with your mail and chat connected so it can read your sent items. Without connectors, paste or upload exports.

Aim for 200+ messages per kind of writing. Under 50 it still works, and the profile will say it is thin.

## What it does

1. **Scope.** Name, registers, sources, and anything you already know you hate in writing.
2. **Collect.** Sent items only, saved in full before analysis. Automated mail, AI-drafted mail, credentials, and sensitive threads (medical, legal, finance, HR) are left out unless you add them back.
3. **Measure.** `scripts/voice_stats.py` counts the habits a writer can act on.
4. **Read for patterns.** Openers, closers, how you decline, ask, apologize, joke, and what never appears.
5. **Write the profile and samples.** Hard rules and soft defaults, each with its evidence, plus 10 to 25 redacted real samples.
6. **Review.** You correct the profile.
7. **Generate.** The two skills are built from templates.
8. **Test and tune.** Real drafts, with misses fed back into the profile.

## What's in here

```
voice-skill-builder/
  SKILL.md                         the workflow
  scripts/voice_stats.py           corpus statistics, standard library only
  references/profile-template.md   skeleton for each voice profile
  references/skill-templates.md    templates for the two generated skills
voice-skill-builder.zip            the same folder, ready to upload
```

You can run the stats script on its own against any folder of `.txt` or `.md` files, one message per file:

```bash
python voice-skill-builder/scripts/voice_stats.py corpus/work --label work --json work.json
```

## Privacy

Your corpus, profile, and samples stay in your own Claude account and the skills you generate. Nothing in this repo collects or sends anything. The generated skills contain real samples of your writing, so look them over before sharing those skills with anyone.

Build a voice skill only for your own writing, or with the clear say-so of the person whose writing it is.

## License

[MIT](LICENSE)
