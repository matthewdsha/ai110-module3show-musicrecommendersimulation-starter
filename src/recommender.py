import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts, converting numeric columns to numbers."""
    print(f"Loading songs from {csv_path}...")
    float_fields = {"energy", "valence", "danceability", "acousticness"}
    int_fields = {"id", "tempo_bpm"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip fully blank lines that some CSVs end with.
            if not any((value or "").strip() for value in row.values()):
                continue
            song: Dict = {}
            for key, value in row.items():
                if key in float_fields:
                    song[key] = float(value)
                elif key in int_fields:
                    song[key] = int(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    # Genre match: hard label match, worth +2.0
    if song.get("genre") == user_prefs.get("genre"):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match: softer vibe match, worth +1.0 (half of genre)
    if song.get("mood") == user_prefs.get("mood"):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # Energy closeness: reward songs near the target, up to +2.0.
    # 1 - abs(distance) means too-high is penalized as much as too-low.
    if "energy" in user_prefs:
        target = user_prefs["energy"]
        points = 2.0 * max(0.0, 1.0 - abs(song["energy"] - target))
        score += points
        reasons.append(
            f"energy close to {target:.2f} (song {song['energy']:.2f}) (+{points:.2f})"
        )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), highest first."""
    # Judge every song with score_song, pairing each with its score + reasons.
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # Rank highest score first, then keep only the top k.
    scored.sort(key=lambda item: item[1], reverse=True)

    # Turn each song's reason list into a single explanation string for display.
    return [
        (song, score, "; ".join(reasons) if reasons else "no matching preferences")
        for song, score, reasons in scored[:k]
    ]
