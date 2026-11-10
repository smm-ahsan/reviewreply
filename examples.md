# Examples

Real output from ReviewReply, captured from actual runs.

## Five stars, warm tone, named reviewer

Command:

```bash
python3 reviewreply.py --stars 5 --business "Cafe Example" --reviewer "Maria"
```

Output:

```
--- Draft 1 ---
Hi Maria, thank you for taking the time to leave us five stars. We are so glad everything hit the mark at Cafe Example, and we cannot wait to have you back.

With thanks,
The Cafe Example team

--- Draft 2 ---
Hi Maria, you have made our whole team smile with this one. Thank you for choosing Cafe Example and for the five stars - it really does mean the world to a small business like ours.

With thanks,
The Cafe Example team
```

## Two stars, professional tone, with an issue

Command:

```bash
python3 reviewreply.py --stars 2 --business "Cafe Example" --issue "slow service" --tone professional
```

Output:

```
--- Draft 1 ---
Hi there, thank you for bringing this to our attention. We apologise unreservedly for your experience at Cafe Example. You mentioned the slow service, and you are right to expect better from us on that. Reviews like yours are taken seriously and shared with the whole team. We would welcome the chance to speak with you privately and put things right.

Kind regards,
The Cafe Example team

--- Draft 2 ---
Hi there, thank you for your review, and please accept our sincere apologies. Your experience at Cafe Example fell below the standard we set for ourselves. You mentioned the slow service, and you are right to expect better from us on that. We would appreciate the opportunity to discuss this privately and resolve it properly - please contact us directly at your convenience.

Kind regards,
The Cafe Example team
```
