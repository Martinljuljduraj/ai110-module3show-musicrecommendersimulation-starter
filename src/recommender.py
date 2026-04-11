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

# ---------------------------------------------------------------------------
# Scoring helpers
# ---------------------------------------------------------------------------

# Genres considered "indie family" for partial credit
_INDIE_FAMILY = {"indie pop", "indie rock", "indie folk"}

# Moods considered "chill family" for partial credit
_MOOD_FAMILIES: Dict[str, set] = {
    "chill":    {"chill", "relaxed", "peaceful", "focused"},
    "relaxed":  {"relaxed", "chill", "peaceful"},
    "peaceful": {"peaceful", "chill", "relaxed"},
    "focused":  {"focused", "chill"},
    "happy":    {"happy", "energetic"},
    "energetic":{"energetic", "happy", "intense"},
    "intense":  {"intense", "energetic", "angry"},
    "moody":    {"moody", "melancholic", "romantic"},
    "melancholic": {"melancholic", "moody"},
    "romantic": {"romantic", "moody"},
    "angry":    {"angry", "intense"},
}


def score_song(song: Dict, user_prefs: Dict) -> Tuple[float, str]:
    """
    Score a single song against user preferences using seven weighted rules.

    Returns (score, explanation_string).

    Scoring recipe (max ≈ 13.5 points):
      Rule 1 – Genre logic       : exact +1.0 | indie-family +0.5  (halved)
      Rule 2 – Mood match        : exact +1.5 | mood-family  +0.75
      Rule 3 – Energy proximity  : up to +4.0  (linear decay over [0, 1], doubled)
      Rule 4 – Valence proximity : up to +1.5  (linear decay over [0, 1])
      Rule 5 – Tempo proximity   : up to +1.5  (linear decay over ±80 BPM)
      Rule 6 – Danceability zone : +1.0 if in [0.55, 0.85], +0.5 if near-miss
      Rule 7 – Acousticness      : up to +1.0  (proportional to preference)
    """
    score = 0.0
    reasons: List[str] = []

    song_genre = song.get("genre", "").lower().strip()
    fav_genre  = user_prefs.get("favorite_genre", "").lower().strip()

    # ------------------------------------------------------------------
    # Rule 1: Genre logic (+1.0 exact, +0.5 indie-family) — halved weight
    # ------------------------------------------------------------------
    if song_genre == fav_genre:
        score += 1.0
        reasons.append(f"genre match ({song_genre}) +1.0")
    elif song_genre in _INDIE_FAMILY and fav_genre in _INDIE_FAMILY:
        score += 0.5
        reasons.append(f"indie-family genre ({song_genre}) +0.5")

    # ------------------------------------------------------------------
    # Rule 2: Mood match (+1.5 exact, +0.75 mood-family)
    # ------------------------------------------------------------------
    song_mood = song.get("mood", "").lower().strip()
    fav_mood  = user_prefs.get("favorite_mood", "").lower().strip()

    if song_mood == fav_mood:
        score += 1.5
        reasons.append(f"mood match ({song_mood}) +1.5")
    elif song_mood in _MOOD_FAMILIES.get(fav_mood, set()):
        score += 0.75
        reasons.append(f"mood family ({song_mood}≈{fav_mood}) +0.75")

    # ------------------------------------------------------------------
    # Rule 3: Energy proximity (up to +4.0) — doubled weight
    # ------------------------------------------------------------------
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_delta  = abs(float(song.get("energy", 0.5)) - target_energy)
    energy_points = 4.0 * max(0.0, 1.0 - energy_delta)
    score += energy_points
    reasons.append(f"energy proximity +{energy_points:.2f}")

    # ------------------------------------------------------------------
    # Rule 4: Valence proximity (up to +1.5)
    # ------------------------------------------------------------------
    target_valence = user_prefs.get("target_valence", 0.5)
    valence_delta  = abs(float(song.get("valence", 0.5)) - target_valence)
    valence_points = 1.5 * max(0.0, 1.0 - valence_delta)
    score += valence_points
    reasons.append(f"valence proximity +{valence_points:.2f}")

    # ------------------------------------------------------------------
    # Rule 5: Tempo proximity (up to +1.5, decays over ±80 BPM)
    # ------------------------------------------------------------------
    target_tempo = user_prefs.get("target_tempo_bpm", 110)
    tempo_delta  = abs(float(song.get("tempo_bpm", 100)) - target_tempo)
    tempo_points = 1.5 * max(0.0, 1.0 - tempo_delta / 80.0)
    score += tempo_points
    reasons.append(f"tempo proximity +{tempo_points:.2f}")

    # ------------------------------------------------------------------
    # Rule 6: Danceability sweet spot (+1.0 in zone, +0.5 near-miss)
    # ------------------------------------------------------------------
    danceability = float(song.get("danceability", 0.5))
    if 0.55 <= danceability <= 0.85:
        score += 1.0
        reasons.append(f"danceability sweet spot ({danceability:.2f}) +1.0")
    elif 0.45 <= danceability < 0.55 or 0.85 < danceability <= 0.95:
        score += 0.5
        reasons.append(f"danceability near-miss ({danceability:.2f}) +0.5")

    # ------------------------------------------------------------------
    # Rule 7: Acousticness (up to +1.0, proportional to preference)
    # ------------------------------------------------------------------
    acousticness = float(song.get("acousticness", 0.5))
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acoustic_points = 1.0 * acousticness
    else:
        acoustic_points = 1.0 * (1.0 - acousticness)
    score += acoustic_points
    reasons.append(f"acousticness +{acoustic_points:.2f}")

    # ------------------------------------------------------------------
    # Rule 8: Activity match (+1.0 per matching activity, max +2.0)
    # ------------------------------------------------------------------
    preferred_activities = set(user_prefs.get("preferred_activities", []))
    song_activities = set(
        a.strip() for a in song.get("activities", "").split(",") if a.strip()
    )
    matched = preferred_activities & song_activities
    activity_points = min(len(matched) * 1.0, 2.0)
    if activity_points > 0:
        score += activity_points
        reasons.append(f"activity match ({', '.join(sorted(matched))}) +{activity_points:.1f}")

    explanation = " | ".join(reasons)
    return round(score, 2), explanation


# ---------------------------------------------------------------------------
# Public API used by src/main.py
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file and return a list of dicts.
    Numeric columns are cast to float; id is cast to int.
    """
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "activities":   row.get("activities", ""),
            })
    return songs


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Score every song, rank by score, return top-k as (song, score, explanation).
    """
    scored = [(song, *score_song(song, user_prefs)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]


# ---------------------------------------------------------------------------
# OOP wrapper (required by tests/test_recommender.py)
# ---------------------------------------------------------------------------

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Store the catalog of Song dataclass instances."""
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        """Convert a Song dataclass to a plain dict for score_song."""
        return {
            "id": song.id, "title": song.title, "artist": song.artist,
            "genre": song.genre, "mood": song.mood, "energy": song.energy,
            "tempo_bpm": song.tempo_bpm, "valence": song.valence,
            "danceability": song.danceability, "acousticness": song.acousticness,
        }

    def _user_to_dict(self, user: UserProfile) -> Dict:
        """Convert a UserProfile dataclass to a plain dict for score_song."""
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood":  user.favorite_mood,
            "target_energy":  user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score all songs for this user and return the top-k Song objects."""
        user_dict  = self._user_to_dict(user)
        song_dicts = [self._song_to_dict(s) for s in self.songs]
        results    = recommend_songs(user_dict, song_dicts, k)
        id_map     = {s.id: s for s in self.songs}
        return [id_map[r[0]["id"]] for r in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return the scoring explanation string for a single song and user."""
        _, explanation = score_song(self._song_to_dict(song), self._user_to_dict(user))
        return explanation
