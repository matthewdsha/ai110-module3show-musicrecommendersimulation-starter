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

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



