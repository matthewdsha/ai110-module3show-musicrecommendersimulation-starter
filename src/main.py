"""
Command line runner for the Music Recommender Simulation.

This file runs the recommender against a battery of user profiles:
  - 3 "normal" profiles that describe coherent tastes.
  - Several "adversarial" / edge-case profiles designed to probe the
    scoring logic in recommender.py and see if it can be tricked.

You implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Normal profiles: coherent tastes a real listener might have.
# ---------------------------------------------------------------------------
NORMAL_PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.85},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}


# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles: designed to trick or stress the scorer.
# Each note explains WHAT the profile is probing for.
# ---------------------------------------------------------------------------
ADVERSARIAL_PROFILES = {
    # Conflicting axes: "sad" mood but "high energy". The scorer treats mood
    # and energy independently, so it happily rewards BOTH — it never notices
    # that a loud, high-energy sad song is contradictory. Expect an incoherent
    # mix at the top (aggressive/intense songs that merely happen to be sad-ish,
    # or sad songs that lose on energy) with no single dominant vibe.
    "Conflicted: Sad but Hyped": {"mood": "sad", "energy": 0.9},

    # No genre, no mood, only energy. Tests whether energy alone can drive the
    # ranking. Everything is scored purely on distance-to-0.5, so the top 5
    # should be whatever songs cluster near energy 0.5 regardless of style.
    "Energy-Only Middle": {"energy": 0.5},

    # Empty profile: zero preferences. score_song returns 0.0 for every song,
    # so ranking is arbitrary (stable sort => original CSV order). Checks the
    # "no matching preferences" fallback path and degenerate ties.
    "Empty Preferences": {},

    # Out-of-range energy (1.5). abs(song.energy - 1.5) is always >= ~0.5, and
    # `1 - dist` is clamped at 0 via max(0.0, ...). Verifies the clamp holds and
    # nobody scores negative energy points from a target outside [0, 1].
    "Impossible Energy 1.5": {"genre": "metal", "mood": "aggressive", "energy": 1.5},

    # Unknown labels that exist nowhere in the dataset. No genre/mood match can
    # fire, so only the energy term contributes. Confirms the scorer degrades
    # gracefully instead of crashing on values it has never seen.
    "Nonexistent Tastes": {"genre": "polka", "mood": "ecstatic", "energy": 0.7},
}


def run_profile(name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Run the recommender for a single profile and print the top k."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 60)
    print(f"  {name}")
    print(f"  For: {user_prefs}")
    print("=" * 60 + "\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']}   [score: {score:.2f}]")
        for reason in explanation.split("; "):
            print(f"     • {reason}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n" + "#" * 60)
    print("#  NORMAL PROFILES")
    print("#" * 60)
    for name, prefs in NORMAL_PROFILES.items():
        run_profile(name, prefs, songs, k=5)

    print("\n" + "#" * 60)
    print("#  ADVERSARIAL / EDGE-CASE PROFILES")
    print("#" * 60)
    for name, prefs in ADVERSARIAL_PROFILES.items():
        run_profile(name, prefs, songs, k=5)


if __name__ == "__main__":
    main()
