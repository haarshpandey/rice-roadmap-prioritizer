# RICE Roadmap Prioritizer

A small CLI tool that scores a feature backlog with the **RICE framework** (Reach × Impact × Confidence ÷ Effort) and prints a ranked roadmap. The kind of thing I'd actually use in a roadmap review.

## Usage

```bash
python prioritize.py --demo          # bundled sample SaaS backlog
python prioritize.py features.csv   # your own backlog
python prioritize.py --demo --top 3 # just the top 3
```

CSV columns: `feature, reach, impact, confidence, effort`
Impact scale: 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal.

## Sample output

```
Rank  Feature                                R       I    C%     E      RICE
1     In-app onboarding checklist         5000       1    70     1    3500.0
2     Dark mode                           8000     0.5    90   1.5    2400.0
3     Admin audit log export               600       2    85     1    1020.0
4     AI triage agent for support         2000       3    50     4     750.0
...
```

Note what RICE surfaces here: the AI triage agent has *massive* impact but ranks 4th — low confidence and high effort drag it down. That's the framework doing its job: it forces the conversation toward "how do we de-risk this?" instead of "this feels important."
