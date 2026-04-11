"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


# ============================================================================
# User Preference Profiles
# ============================================================================

# Profile 1: The Indie Enthusiast
# Indie pop lover with relaxed vibes, prefers acoustic warmth
PROFILE_INDIE_ENTHUSIAST = {
    "favorite_genre": "indie pop",
    "favorite_mood": "chill",
    "target_energy": 0.75,
    "target_valence": 0.70,
    "target_tempo_bpm": 110,
    "likes_acoustic": True,
    "preferred_activities": ["driving", "studying"],
}

# Profile 2: The Lofi Scholar
# Calm, focused listener preferring mellow study vibes
PROFILE_LOFI_SCHOLAR = {
    "favorite_genre": "lofi",
    "favorite_mood": "focused",
    "target_energy": 0.38,      # Low energy for concentration
    "target_valence": 0.55,     # Neutral/slightly positive emotional tone
    "target_tempo_bpm": 80,     # Slower pace for focus
    "likes_acoustic": True,
    "preferred_activities": ["studying", "relaxing", "working"],
}

# Profile 3: The Gym Enthusiast
# High-energy listener seeking motivation for workouts
PROFILE_GYM_ENTHUSIAST = {
    "favorite_genre": "pop",
    "favorite_mood": "intense",
    "target_energy": 0.90,      # Very high energy for motivation
    "target_valence": 0.75,     # Positive/uplifting
    "target_tempo_bpm": 130,    # Fast tempo for cardio
    "likes_acoustic": False,
    "preferred_activities": ["working out", "driving"],
}


# ============================================================================
# System Evaluation: Adversarial & Edge Case Profiles
# ============================================================================

ADVERSARIAL_PROFILES = [
    {
        "name": "🚩 Conflicting: High Energy + Peaceful Mood",
        "description": "Tests if scorer handles contradictory preferences gracefully",
        "prefs": {
            "favorite_genre": "ambient",
            "favorite_mood": "peaceful",
            "target_energy": 0.95,        # ← Conflict: peaceful songs are usually low energy
            "target_valence": 0.50,
            "target_tempo_bpm": 140,      # ← Fast tempo contradicts peaceful mood
            "likes_acoustic": True,
            "preferred_activities": ["relaxing"],
        },
    },
    {
        "name": "🚩 Contradiction: Intense Mood + Low Energy",
        "description": "Tests preference contradiction (intense songs are usually high-energy)",
        "prefs": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.25,        # ← Conflict: intense is high-energy by nature
            "target_valence": 0.30,
            "target_tempo_bpm": 60,       # ← Slow tempo contradicts intense
            "likes_acoustic": True,
            "preferred_activities": ["relaxing", "sleeping"],  # ← Contradicts intense mood
        },
    },
    {
        "name": "🚩 Extreme Values: All Maxed Out",
        "description": "Tests if scorer degrades gracefully with all extreme preferences",
        "prefs": {
            "favorite_genre": "synthwave",
            "favorite_mood": "intense",
            "target_energy": 0.99,        # Nearly maximum
            "target_valence": 0.99,       # Nearly maximum
            "target_tempo_bpm": 200,      # Unrealistically fast
            "likes_acoustic": False,
            "preferred_activities": ["working out", "driving", "studying"],  # Contradictory
        },
    },
    {
        "name": "🚩 Extreme Values: All Minimized",
        "description": "Tests if scorer works with minimal/neutral preferences",
        "prefs": {
            "favorite_genre": "ambient",
            "favorite_mood": "chill",
            "target_energy": 0.01,        # Unrealistically low
            "target_valence": 0.01,       # Nearly zero valence (sad)
            "target_tempo_bpm": 30,       # Unrealistically slow
            "likes_acoustic": False,
            "preferred_activities": ["sleeping"],
        },
    },
    {
        "name": "🚩 Empty Activity List vs. Genre Mismatch",
        "description": "Tests if scorer handles missing/empty preferred_activities gracefully",
        "prefs": {
            "favorite_genre": "jazz",
            "favorite_mood": "relaxed",
            "target_energy": 0.50,
            "target_valence": 0.50,
            "target_tempo_bpm": 90,
            "likes_acoustic": True,
            "preferred_activities": [],    # Empty activities list
        },
    },
    {
        "name": "🚩 Happiness + High Danceability with Sad Valence",
        "description": "Tests if scorer weights contradictory numeric attributes correctly",
        "prefs": {
            "favorite_genre": "techno",
            "favorite_mood": "happy",
            "target_energy": 0.85,
            "target_valence": 0.15,       # ← Contradiction: 'happy' mood but sad valence (0.15)
            "target_tempo_bpm": 120,
            "likes_acoustic": False,
            "preferred_activities": ["working out"],
        },
    },
    {
        "name": "🚩 Moody + Energetic + Danceability Confusion",
        "description": "Tests if moody songs can score well despite contradictory energy settings",
        "prefs": {
            "favorite_genre": "electronic",
            "favorite_mood": "moody",
            "target_energy": 0.88,        # High energy
            "target_valence": 0.25,       # Dark/sad
            "target_tempo_bpm": 95,       # Medium-slow tempo
            "likes_acoustic": False,
            "preferred_activities": ["driving"],
        },
    },
]


def print_recommendations(user_prefs, songs, profile_name="User Profile", k=5):
    """Helper function to print recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print(f"\n  {profile_name}")
    print(f"  {'─' * 50}")
    print(f"  Genre: {user_prefs['favorite_genre'].title():<18} Mood: {user_prefs['favorite_mood'].title()}")
    print(f"  Energy: {user_prefs['target_energy']:<17} Valence: {user_prefs['target_valence']}")
    print(f"  Tempo: {user_prefs['target_tempo_bpm']} BPM{'':<14} Acoustic: {'Yes' if user_prefs.get('likes_acoustic', False) else 'No'}")
    if user_prefs.get('preferred_activities'):
        print(f"  Activities: {', '.join(user_prefs['preferred_activities'])}")
    else:
        print(f"  Activities: (none)")

    print(f"\n  {'═' * 50}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"  {'═' * 50}")

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        bar_len = int((score / 13.5) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"\n    #{i}  {song['title']} — {song['artist']}")
        print(f"        Score: {score:>5.2f}  [{bar}]")
        print(f"        Genre: {song['genre'].title():<16} Mood: {song['mood'].title()}")
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"          • {reason}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print("🎵 Music Recommender Simulation")
    print("=" * 60)

    # ========================================================================
    # STANDARD EVALUATION: Three Distinct User Profiles
    # ========================================================================
    print("\n" + "=" * 60)
    print("STANDARD EVALUATION: Distinct User Profiles")
    print("=" * 60)

    print_recommendations(PROFILE_INDIE_ENTHUSIAST, songs, "Profile 1: Indie Enthusiast", k=5)
    print_recommendations(PROFILE_LOFI_SCHOLAR, songs, "Profile 2: Lofi Scholar", k=5)
    print_recommendations(PROFILE_GYM_ENTHUSIAST, songs, "Profile 3: Gym Enthusiast", k=5)

    # ========================================================================
    # SYSTEM EVALUATION: Adversarial & Edge Case Profiles
    # ========================================================================
    print("\n" + "=" * 60)
    print("SYSTEM EVALUATION: Adversarial & Edge Case Profiles")
    print("=" * 60)
    print("\n  Testing scoring robustness against contradictory/extreme preferences...\n")

    for i, adversarial in enumerate(ADVERSARIAL_PROFILES, 1):
        print(f"\n  [{i}] {adversarial['name']}")
        print(f"      → {adversarial['description']}")
        print_recommendations(adversarial['prefs'], songs, f"Adversarial Case {i}", k=3)

    print(f"\n{'═' * 60}")
    print("  System Evaluation Complete\n")


if __name__ == "__main__":
    main()
