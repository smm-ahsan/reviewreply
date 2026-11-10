#!/usr/bin/env python3
"""ReviewReply - draft polite, human replies to customer reviews.

A tiny, dependency-free tool for local businesses. Owners of restaurants,
cafes, salons and shops are expected to reply to every Google review, and
writing a fresh, gracious reply every day is harder than it sounds -
especially to the unfair ones. ReviewReply prints ready-to-edit reply
drafts matched to the star rating: grateful for five stars, warm for
four, balanced for three, and calmly apologetic for one and two, without
ever arguing with the reviewer.

Usage:
    python3 reviewreply.py --stars 5 --business "Cafe Example" --reviewer "Maria"
    python3 reviewreply.py --stars 2 --business "Cafe Example" --issue "slow service" --tone professional
"""

import argparse
import random
import sys

# ---------------------------------------------------------------------------
# Template banks. Placeholders: {greeting}, {business}, {issue_line}.
# ---------------------------------------------------------------------------

FIVE = {
    "warm": [
        "{greeting} thank you so much for the five stars! It honestly makes "
        "our day to hear you had a great experience at {business}. We will "
        "pass your kind words on to the whole team, and we hope to welcome "
        "you back again very soon.",
        "{greeting} what a lovely review - thank you! Guests like you are "
        "exactly why we love what we do at {business}. Come back soon; the "
        "welcome will be just as warm.",
        "{greeting} thank you for taking the time to leave us five stars. "
        "We are so glad everything hit the mark at {business}, and we "
        "cannot wait to have you back.",
        "{greeting} you have made our whole team smile with this one. "
        "Thank you for choosing {business} and for the five stars - it "
        "really does mean the world to a small business like ours.",
    ],
    "professional": [
        "{greeting} thank you for your five-star review of {business}. We "
        "are delighted that your visit met your expectations, and we look "
        "forward to welcoming you again.",
        "{greeting} thank you for rating {business} five stars. Feedback "
        "like yours confirms we are on the right track, and we appreciate "
        "you taking the time to share it.",
        "{greeting} we sincerely appreciate your five-star review. The "
        "team at {business} works hard to keep standards high, and your "
        "words are a real encouragement to them.",
    ],
}

FOUR = {
    "warm": [
        "{greeting} thank you for the four stars and for visiting "
        "{business}! We are really glad you enjoyed it. Next time you are "
        "in, tell us what would make it a five for you - we would love to "
        "earn that last star.",
        "{greeting} thanks so much for the kind review of {business}. It "
        "is great to hear you had a good time with us. We hope to see you "
        "again soon, and we will be aiming for five stars on your next "
        "visit.",
        "{greeting} four stars - thank you! We are happy you chose "
        "{business} and even happier that you left pleased. Do come back "
        "soon; there is always something new to try.",
    ],
    "professional": [
        "{greeting} thank you for your four-star review of {business}. We "
        "are pleased your experience was a positive one. If anything could "
        "have been better, we would genuinely value the detail - it helps "
        "us improve. We hope to welcome you again.",
        "{greeting} thank you for taking the time to review {business}. "
        "We are glad your visit went well, and we will keep working on the "
        "details that turn a good visit into a great one.",
        "{greeting} we appreciate your four-star rating and your visit to "
        "{business}. Your feedback is noted, and we look forward to "
        "serving you again soon.",
    ],
}

THREE = {
    "warm": [
        "{greeting} thank you for the honest three stars and for giving "
        "{business} a try. We are glad some of it worked for you, and we "
        "are sorry other parts fell short.{issue_line} We are working on "
        "it, and we would love the chance to do better on your next visit.",
        "{greeting} thanks for reviewing {business} - a mixed review is "
        "the most useful kind, so we really do appreciate it.{issue_line} "
        "We have shared your comments with the team, and we hope you will "
        "give us another chance to get it fully right.",
        "{greeting} thank you for stopping by {business} and for the fair "
        "review. Not perfect is not good enough for us.{issue_line} Your "
        "feedback is how we improve, so thank you for being straight with "
        "us.",
    ],
    "professional": [
        "{greeting} thank you for your three-star review of {business}. "
        "We are sorry your experience was not consistently at the standard "
        "we aim for.{issue_line} Your comments have been passed to the "
        "team, and we are addressing them. We hope to serve you better on "
        "a future visit.",
        "{greeting} thank you for your balanced feedback on {business}. "
        "We take both the positives and the shortcomings seriously."
        "{issue_line} If you would like to share more detail, we would "
        "welcome it - it directly informs the changes we make.",
        "{greeting} we appreciate your review of {business} and your "
        "honesty about where we fell short.{issue_line} Consistent quality "
        "is our goal, and your feedback helps us close the gap. Thank you "
        "for giving us the opportunity to improve.",
    ],
}

LOW = {
    "warm": [
        "{greeting} we are really sorry. This is not the experience anyone "
        "should have at {business}, and we completely understand your "
        "frustration.{issue_line} Please message us directly so we can "
        "hear the full story and do our best to make it right - you "
        "deserve that from us.",
        "{greeting} thank you for telling us, even though we know it is "
        "not what you wanted to write. We got it wrong this time at "
        "{business}, and we are sorry.{issue_line} If you are open to it, "
        "reach out to us privately and we will do everything we can to "
        "put it right.",
        "{greeting} we are so sorry your visit to {business} left you "
        "feeling this way. That is on us, not you.{issue_line} We would "
        "genuinely like to fix this - please contact us directly and ask "
        "for the manager, and we will take it from there.",
    ],
    "professional": [
        "{greeting} thank you for your review, and please accept our "
        "sincere apologies. Your experience at {business} fell below the "
        "standard we set for ourselves.{issue_line} We would appreciate "
        "the opportunity to discuss this privately and resolve it properly "
        "- please contact us directly at your convenience.",
        "{greeting} we are sorry to read your review of {business}. Every "
        "guest should leave satisfied, and on this occasion we clearly "
        "failed to deliver that.{issue_line} Your feedback has been "
        "escalated to management. Please reach out to us directly so we "
        "can make amends.",
        "{greeting} thank you for bringing this to our attention. We "
        "apologise unreservedly for your experience at {business}."
        "{issue_line} Reviews like yours are taken seriously and shared "
        "with the whole team. We would welcome the chance to speak with "
        "you privately and put things right.",
    ],
}

BANDS = {5: FIVE, 4: FOUR, 3: THREE, 2: LOW, 1: LOW}

SIGNOFF = {
    "warm": "With thanks,\nThe {business} team",
    "professional": "Kind regards,\nThe {business} team",
}


def issue_line(issue, stars):
    """A graceful sentence acknowledging a specific complaint, or ''."""
    if not issue:
        return ""
    if stars <= 2:
        return (" You mentioned the {issue}, and you are right to expect "
                "better from us on that.").format(issue=issue)
    if stars == 3:
        return (" Thank you for flagging the {issue} - that is exactly "
                "the kind of detail that helps us improve.").format(issue=issue)
    return ""


def build_reply(template, greeting, business, issue, stars, tone):
    text = template.format(
        greeting=greeting,
        business=business,
        issue_line=issue_line(issue, stars),
    )
    return "{text}\n\n{signoff}".format(
        text=text, signoff=SIGNOFF[tone].format(business=business)
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Draft polite replies to customer reviews for local businesses."
    )
    parser.add_argument("--stars", required=True, type=int, choices=[1, 2, 3, 4, 5],
                        help="Star rating of the review (1 to 5)")
    parser.add_argument("--business", required=True,
                        help="Business name, e.g. 'Cafe Example'")
    parser.add_argument("--reviewer", default=None,
                        help="Reviewer's first name, to personalise the greeting")
    parser.add_argument("--issue", default=None,
                        help="Short note of what went wrong, used in 1-3 star "
                             "replies, e.g. 'slow service'")
    parser.add_argument("--tone", default="warm", choices=["warm", "professional"],
                        help="Reply tone (default: warm)")
    parser.add_argument("--count", type=int, default=2,
                        help="How many reply drafts to print (default: 2)")
    args = parser.parse_args(argv)

    if args.count < 1:
        print("--count must be at least 1", file=sys.stderr)
        return 2

    greeting = "Hi {name},".format(name=args.reviewer) if args.reviewer else "Hi there,"
    bank = BANDS[args.stars][args.tone]

    rng = random.Random()
    drafts = []
    pool = list(bank)
    while len(drafts) < args.count:
        rng.shuffle(pool)
        for template in pool:
            drafts.append(build_reply(template, greeting, args.business,
                                      args.issue, args.stars, args.tone))
            if len(drafts) >= args.count:
                break

    for i, draft in enumerate(drafts):
        if args.count > 1:
            print("--- Draft {} ---".format(i + 1))
        print(draft)
        if i < len(drafts) - 1:
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
