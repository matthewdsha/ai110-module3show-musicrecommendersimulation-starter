"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    # Header describing the profile we recommended for.
    print("\n" + "=" * 48)
    print("  TOP RECOMMENDATIONS")
    print(f"  For: {user_prefs}")
    print("=" * 48 + "\n")

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        # Title line: rank, song, artist, and the final score.
        print(f"{rank}. {song['title']} — {song['artist']}   [score: {score:.2f}]")
        # Show each reason on its own indented line for readability.
        for reason in explanation.split("; "):
            print(f"     • {reason}")
        print()


if __name__ == "__main__":
    main()
