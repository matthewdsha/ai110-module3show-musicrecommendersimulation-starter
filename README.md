# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real-world recommenders blend several signals at once using content-based filtering that matches items by their attributes, collaborative filtering that learns from what similar users listened to, and behavioral signals like skips, replays, and time-of-day that are all continuously retrained on massive datasets and tuned to maximize engagement. My version is deliberately simpler and more transparent as it's purely content-based, scoring each song by how closely its numerical features (energy, valence, danceability, acousticness) match a stated user preference. It prioritizes matching the requested "vibe" over popularity or novelty. The trade-off is that it can't discover the surprising, cross-genre picks that collaborative filtering excels at, but in exchange every result is predictable and easy to reason about.

My recommender uses a Song object with genre and mood (categorical, scored), energy and acousticness (numeric, scored for closeness), valence/danceability/tempo_bpm (reserved in the data), plus id/title/artist for identity only. The UserProfile holds favorite_genre, favorite_mood, target_energy, and likes_acoustic, which map onto the four scored features. The dataflow is straightforward: input is a single UserProfile, the process loops over every song in songs.csv and scores it independently against those preferences (attaching a short reason for each), and the output sorts by score and returns the Top-K recommendations with explanations. My finalized Algorithm Recipe (max 6.0 points) awards +2.0 for a genre match, +1.0 for a mood match, up to +2.0 for energy closeness (2.0 * (1 - |song.energy - target_energy|)), and up to +1.0 for acousticness closeness (target 0.8 if likes_acoustic else 0.2). Genre and energy act as co-equal anchors while mood and acousticness serve as tie-breakers, and crucially the numeric features reward closeness in both directions rather than higher-is-better, so a too-intense song is penalized just like a too-mellow one.

I do expect some built-in biases. Because it's purely content-based, it has a diversity blind spot — it keeps serving the user's stated genre and never surprises them with a strong cross-genre pick, and the heavy 2.0 genre weight makes genre lock-in likely even when an off-genre song is a perfect vibe match. The small dataset means genres and moods aren't evenly represented, so some preferences have many more candidates than others, and since mood is partly derivable from energy the two axes double-count "vibe" a little (which is why mood is kept lighter at 1.0). Finally, the point weights are assumptions as they encode my own view of what defines a musical vibe.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

Loading songs from data/songs.csv...
Loaded songs: 19

================================================
  TOP RECOMMENDATIONS
  For: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
================================================

1. Sunrise City — Neon Echo   [score: 4.96]
     • genre match: pop (+2.0)
     • mood match: happy (+1.0)
     • energy close to 0.80 (song 0.82) (+1.96)

2. Gym Hero — Max Pulse   [score: 3.74]
     • genre match: pop (+2.0)
     • energy close to 0.80 (song 0.93) (+1.74)

3. Rooftop Lights — Indigo Parade   [score: 2.92]
     • mood match: happy (+1.0)
     • energy close to 0.80 (song 0.76) (+1.92)

4. Concrete Kings — Blockprint   [score: 2.00]
     • energy close to 0.80 (song 0.80) (+2.00)

5. Night Drive Loop — Neon Echo   [score: 1.90]
     • energy close to 0.80 (song 0.75) (+1.90)





Loading songs from data/songs.csv...
Loaded songs: 19

############################################################
#  NORMAL PROFILES
############################################################

============================================================
  High-Energy Pop
  For: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85}
============================================================

1. Sunrise City — Neon Echo   [score: 4.94]
     • genre match: pop (+2.0)
     • mood match: happy (+1.0)
     • energy close to 0.85 (song 0.82) (+1.94)

2. Gym Hero — Max Pulse   [score: 3.84]
     • genre match: pop (+2.0)
     • energy close to 0.85 (song 0.93) (+1.84)

3. Rooftop Lights — Indigo Parade   [score: 2.82]
     • mood match: happy (+1.0)
     • energy close to 0.85 (song 0.76) (+1.82)

4. Concrete Kings — Blockprint   [score: 1.90]
     • energy close to 0.85 (song 0.80) (+1.90)

5. Storm Runner — Voltline   [score: 1.88]
     • energy close to 0.85 (song 0.91) (+1.88)


============================================================
  Chill Lofi
  For: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
============================================================

1. Library Rain — Paper Lanterns   [score: 5.00]
     • genre match: lofi (+2.0)
     • mood match: chill (+1.0)
     • energy close to 0.35 (song 0.35) (+2.00)

2. Midnight Coding — LoRoom   [score: 4.86]
     • genre match: lofi (+2.0)
     • mood match: chill (+1.0)
     • energy close to 0.35 (song 0.42) (+1.86)

3. Focus Flow — LoRoom   [score: 3.90]
     • genre match: lofi (+2.0)
     • energy close to 0.35 (song 0.40) (+1.90)

4. Spacewalk Thoughts — Orbit Bloom   [score: 2.86]
     • mood match: chill (+1.0)
     • energy close to 0.35 (song 0.28) (+1.86)

5. Coffee Shop Stories — Slow Stereo   [score: 1.96]
     • energy close to 0.35 (song 0.37) (+1.96)


============================================================
  Deep Intense Rock
  For: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
============================================================

1. Storm Runner — Voltline   [score: 4.98]
     • genre match: rock (+2.0)
     • mood match: intense (+1.0)
     • energy close to 0.90 (song 0.91) (+1.98)

2. Gym Hero — Max Pulse   [score: 2.94]
     • mood match: intense (+1.0)
     • energy close to 0.90 (song 0.93) (+1.94)

3. Neon Overdrive — Pulsewave   [score: 1.90]
     • energy close to 0.90 (song 0.95) (+1.90)

4. Iron Verdict — Ashfall   [score: 1.86]
     • energy close to 0.90 (song 0.97) (+1.86)

5. Sunrise City — Neon Echo   [score: 1.84]
     • energy close to 0.90 (song 0.82) (+1.84)


############################################################
#  ADVERSARIAL / EDGE-CASE PROFILES
############################################################

============================================================
  Conflicted: Sad but Hyped
  For: {'mood': 'sad', 'energy': 0.9}
============================================================

1. Three A.M. Blues — Deltona Hart   [score: 2.00]
     • mood match: sad (+1.0)
     • energy close to 0.90 (song 0.40) (+1.00)

2. Storm Runner — Voltline   [score: 1.98]
     • energy close to 0.90 (song 0.91) (+1.98)

3. Gym Hero — Max Pulse   [score: 1.94]
     • energy close to 0.90 (song 0.93) (+1.94)

4. Neon Overdrive — Pulsewave   [score: 1.90]
     • energy close to 0.90 (song 0.95) (+1.90)

5. Iron Verdict — Ashfall   [score: 1.86]
     • energy close to 0.90 (song 0.97) (+1.86)


============================================================
  Energy-Only Middle
  For: {'energy': 0.5}
============================================================

1. Velvet Hours — Soraya Lane   [score: 2.00]
     • energy close to 0.50 (song 0.50) (+2.00)

2. Backroad Goodbye — Marlowe Creek   [score: 1.90]
     • energy close to 0.50 (song 0.45) (+1.90)

3. Midnight Coding — LoRoom   [score: 1.84]
     • energy close to 0.50 (song 0.42) (+1.84)

4. Focus Flow — LoRoom   [score: 1.80]
     • energy close to 0.50 (song 0.40) (+1.80)

5. Island Time — Sunwave Collective   [score: 1.80]
     • energy close to 0.50 (song 0.60) (+1.80)


============================================================
  Empty Preferences
  For: {}
============================================================

1. Sunrise City — Neon Echo   [score: 0.00]
     • no matching preferences

2. Midnight Coding — LoRoom   [score: 0.00]
     • no matching preferences

3. Storm Runner — Voltline   [score: 0.00]
     • no matching preferences

4. Library Rain — Paper Lanterns   [score: 0.00]
     • no matching preferences

5. Gym Hero — Max Pulse   [score: 0.00]
     • no matching preferences


============================================================
  Impossible Energy 1.5
  For: {'genre': 'metal', 'mood': 'aggressive', 'energy': 1.5}
============================================================

1. Iron Verdict — Ashfall   [score: 3.94]
     • genre match: metal (+2.0)
     • mood match: aggressive (+1.0)
     • energy close to 1.50 (song 0.97) (+0.94)

2. Neon Overdrive — Pulsewave   [score: 0.90]
     • energy close to 1.50 (song 0.95) (+0.90)

3. Gym Hero — Max Pulse   [score: 0.86]
     • energy close to 1.50 (song 0.93) (+0.86)

4. Storm Runner — Voltline   [score: 0.82]
     • energy close to 1.50 (song 0.91) (+0.82)

5. Sunrise City — Neon Echo   [score: 0.64]
     • energy close to 1.50 (song 0.82) (+0.64)


============================================================
  Nonexistent Tastes
  For: {'genre': 'polka', 'mood': 'ecstatic', 'energy': 0.7}
============================================================

1. Night Drive Loop — Neon Echo   [score: 1.90]
     • energy close to 0.70 (song 0.75) (+1.90)

2. Rooftop Lights — Indigo Parade   [score: 1.88]
     • energy close to 0.70 (song 0.76) (+1.88)

3. Island Time — Sunwave Collective   [score: 1.80]
     • energy close to 0.70 (song 0.60) (+1.80)

4. Concrete Kings — Blockprint   [score: 1.80]
     • energy close to 0.70 (song 0.80) (+1.80)

5. Sunrise City — Neon Echo   [score: 1.76]
     • energy close to 0.70 (song 0.82) (+1.76)


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

 I halved genre (2.0 → 1.0) and doubled energy (2.0 → 4.0). For normal profiles the top picks barely moved — mostly just bigger scores. But the contradictory "sad but high-energy" profile changed its #1 from a slow sad song to a genuinely loud one, since energy now outweighed the mood label. The downside was that genre stopped mattering much, so I changed the weights back to the original.

Tested different user types: I ran eight profiles — three normal (pop, lofi, rock) and five odd ones (contradictory, energy-only, empty, impossible energy, and made-up labels). Normal profiles gave sensible, on-target lists. The odd ones never crashed: unmatched labels fell back to ranking by energy, an empty profile scored everything zero, and an out-of-range energy value was safely capped.

I learned energy is the main thing separating one listener from another, genre and mood mostly break ties, and the small high-energy dataset makes the same few songs repeat across lists.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- It only works on a tiny 19-song catalog, so the same few songs repeat.
- It doesn't understand lyrics, language, or how a song actually sounds.
- It leans toward high-energy songs, since most of the catalog is high-energy.
- It treats preferences as all-or-nothing, so a genre either matches fully or not at all.
- It can't handle contradictory tastes well, like "sad but high-energy."

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

My biggest learning moment about this project was truly just understand how these recommender systems work. Understanding how different systems work together to give users personalized recommendations gave me a lot of clarity on how these systems works.

AI helped a lot in adjusting the scoring rules, explaining systems, and analyzings results. It helped figure out things I did right, like the scoring rule, and things I did wrong, like analyzing my results. I would need to double check once in a while to see if it messed up the scoring rule a little though.

I was very surprised by seeing this simple algorithm recommend decently well. It matched songs very well to user profiles, and it was awesome to see it at work.

I'd definitely look into working on more trickier tastes that have mixed tastes. They can really bring this system to the next level if it works well.

Overall, building this showed me a recommender is just math on data as it turns songs and user preferences into numbers, scores how well they match, and ranks them. The "prediction" is whatever scores highest. 

It also showed how bias sneaks in. If the data leans one way, like ours skewing high-energy, the system quietly favors those songs and ignores other tastes. And the weights I choose decide whose preferences matter most — so unfairness can come straight from the data and settings, not bad intentions.