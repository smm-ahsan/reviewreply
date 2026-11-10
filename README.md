# ReviewReply

A tiny, dependency-free command line tool that drafts polite, human replies
to customer reviews for local businesses.

Tell it the star rating, your business name, and optionally the reviewer's
name and what went wrong. It prints ready-to-edit reply drafts in the right
register for the rating: grateful for five stars, warm with a gentle invite
back for four, balanced and improvement-minded for three, and calmly
apologetic for one and two - acknowledging the specific issue and offering
to make it right privately, never arguing with the reviewer.

## Why

Restaurants, cafes, salons and shops are expected to reply to every Google
review, every day. The five-star ones are easy. The one-star review written
at midnight by someone who had a bad day is not - and a defensive reply
posted in anger stays on the internet forever. ReviewReply covers the
blank-page moment and the hot-head moment at once: it gives you a gracious
first draft in one second, which you calm down, personalise, and post.

## Features

- Zero dependencies - pure Python 3 standard library
- Template banks per star band, each in a warm and a professional tone
- Reviewer name personalises the greeting
- A specific issue ("slow service", "cold food") is acknowledged
  gracefully in one to three star replies
- Low-star drafts always apologise, never argue, and move the
  conversation to a private channel
- Print several distinct drafts and pick the one that sounds most like you

## Install

No installation needed. Clone the repo and run it with Python 3:

```bash
git clone https://github.com/ahsanhani/reviewreply.git
cd reviewreply
python3 reviewreply.py --help
```

## Usage

```bash
python3 reviewreply.py --stars 5 --business "Cafe Example" --reviewer "Maria"
python3 reviewreply.py --stars 4 --business "Bloom Salon" --count 3
python3 reviewreply.py --stars 3 --business "Pizza Corner" --issue "long wait at lunch"
python3 reviewreply.py --stars 2 --business "Cafe Example" --issue "slow service" --tone professional
python3 reviewreply.py --stars 1 --business "City Barbers" --reviewer "Joe"
```

Sample output for a five-star review:

```
--- Draft 1 ---
Hi Maria, thank you so much for the five stars! It honestly makes our
day to hear you had a great experience at Cafe Example. We will pass
your kind words on to the whole team, and we hope to welcome you back
again very soon.

With thanks,
The Cafe Example team
```

See [examples.md](examples.md) for full sample runs.

## Roadmap

- More tones: playful, formal, super-short (for platforms with limits)
- Industry flavour packs: restaurants, salons, clinics, retail
- Read custom template banks from a JSON file
- Optional "reply to all" worksheet mode for a week of reviews

## Contributing

Issues and pull requests are welcome. If you run a local business and a
reply style is missing - or a draft reads wrong to you - open an issue and
share the kind of review you struggle to answer. Real examples make the
templates better.

## License

MIT - see [LICENSE](LICENSE).
