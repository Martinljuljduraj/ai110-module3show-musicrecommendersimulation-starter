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
    print("🎵 Music Recommender Simulation")
    print("=" * 50)

    # Taste profile — values reflect the algorithm recipe scoring rules
    user_prefs = {
        # --- Genre & Mood ---
        # Primary genre: indie pop sits in the indie scoring path (uniqueness-weighted)
        # rather than the popularity-gated mainstream path
        "favorite_genre": "indie pop",

        # Rewarded moods from the recipe: chill, intense, relaxed score highest
        "favorite_mood": "chill",

        # --- Numerical targets (proximity-scored, not raw-value scored) ---
        # target_energy: 0.75 — high-energy feel without crossing into aggressive territory.
        # Songs close to this value score well; very low (0.28) or very high (0.97) score poorly.
        "target_energy": 0.75,

        # target_valence: 0.70 — positive and uplifting but not aggressively cheerful.
        # Sad/dark songs (valence < 0.30) will lose points against this target.
        "target_valence": 0.70,

        # target_danceability: 0.75 — sits in the sweet-spot range (0.55–0.85) from the recipe.
        # Rewards groovy tracks without over-indexing on pure dance music.
        "target_danceability": 0.75,

        # target_tempo_bpm: 110 — mid-to-uptempo. Pairs with target_energy for beat score.
        # Slow tracks (< 70 BPM) and very fast tracks (> 155 BPM) drift away from this.
        "target_tempo_bpm": 110,

        # --- Boolean flags ---
        # likes_acoustic: True — raw, warm, intimate sounds score higher via acousticness rule.
        "likes_acoustic": True,

        # --- Activity context ---
        # Songs tagged for these contexts earn bonus points in the activity score rule.
        "preferred_activities": ["driving", "studying"],
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"\n  User Profile")
    print(f"  {'─' * 46}")
    print(f"  Genre: {user_prefs['favorite_genre'].title():<20} Mood: {user_prefs['favorite_mood'].title()}")
    print(f"  Energy: {user_prefs['target_energy']:<19} Valence: {user_prefs['target_valence']}")
    print(f"  Tempo: {user_prefs['target_tempo_bpm']} BPM{'':<15} Acoustic: {'Yes' if user_prefs['likes_acoustic'] else 'No'}")
    print(f"  Activities: {', '.join(user_prefs['preferred_activities'])}")

    print(f"\n{'═' * 52}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"{'═' * 52}")

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        bar_len = int((score / 13.5) * 20)
        bar = "█" * bar_len + "░" * (20 - bar_len)
        print(f"\n  #{i}  {song['title']} — {song['artist']}")
        print(f"       Score: {score:>5.2f}  [{bar}]")
        print(f"       Genre: {song['genre'].title():<18} Mood: {song['mood'].title()}")
        reasons = explanation.split(" | ")
        for reason in reasons:
            print(f"         • {reason}")

    print(f"\n{'═' * 52}\n")


if __name__ == "__main__":
    main()
