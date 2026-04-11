# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

BamBam is a music recommender that scores songs based on how well they match a user's taste profile. It uses eight rules — genre, mood, energy, valence, tempo, danceability, acousticness, and activity match — to give every song a score and return the top picks. I ran it against three realistic user profiles and seven adversarial edge cases to see where it holds up and where it breaks.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
Each `Song` has an id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. 
- What information does your `UserProfile` store
The `UserProfile` uses favorite_genre, favorite_mood, target_energy which is the system measuring how close a song's energy is to a specific target value, and likes_acoustic which if true, the acousticness score contributes positively as in my design I have raw and warm sounding music to score high.
- How does your `Recommender` compute a score for each song
In my design algorithm, a score is computed for each song with seven scoring rules: Mood match, valence match, popularity, danceability sweet spot, beat strength, acousticness, and genre logic. I added an 8th rule which is activity matching based on if they are for preferred_activities ["driving", "studying"]. I believe a potential bias I expect will be the popularity factor based on how I planned and set the rules.
- How do you choose which songs to recommend
First, based on my design, every song is given a score independently. Second, we rank the scored list and pick the top.

### Data Flow

```mermaid
flowchart TD
    A([🎵 data/songs.csv\n18 songs]) --> B[load_songs\nparse CSV → list of dicts]
    P([👤 user_prefs\ngenre · mood · energy\nvalence · tempo · acoustic\nactivities]) --> C

    B --> LOOP

    subgraph LOOP["🔁 recommend_songs — loops over every song"]
        C[pick one song dict] --> D

        subgraph SCORE["score_song(song, user_prefs)"]
            D[Rule 1: Genre match\nexact +2.0 · family +1.0]
            D --> E[Rule 2: Mood match\nexact +1.5 · family +0.75]
            E --> F[Rule 3: Energy proximity\nup to +2.0]
            F --> G[Rule 4: Valence proximity\nup to +1.5]
            G --> H[Rule 5: Tempo proximity\nup to +1.5]
            H --> I[Rule 6: Danceability zone\n+1.0 sweet spot · +0.5 near-miss]
            I --> J[Rule 7: Acousticness\nup to +1.0]
            J --> K[Rule 8: Activity match\n+1.0 per match · max +2.0]
        end

        K --> L["return (song, score, explanation)"]
        L --> M{More songs?}
        M -- yes --> C
    end

    M -- no, 18 songs scored --> N["sort by score descending\nscored.sort(reverse=True)"]
    N --> O["slice top-k\nscored[:5]"]
    O --> R

    subgraph R["📋 Output — main.py prints top 5"]
        R1["#1 Rooftop Lights     8.90"]
        R2["#2 Midnight Coding    7.74"]
        R3["#3 Library Rain       7.70"]
        R4["#4 Broken Compass     7.54"]
        R5["#5 Focus Flow         7.10"]
    end
```

### Sample Output

![Recommendation Output](recommendation_output.png)

### User Profile Recommendations

#### Indie Enthusiast Profile
![Indie Enthusiast Recommendations](indie_enthusiast.png)

#### Lofi Scholar Profile
![Lofi Scholar Recommendations](lofi_scholar.png)

#### Gym Enthusiast Profile
![Gym Enthusiast Recommendations](gym_enthusiast.png)

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

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I ran a weight shift experiment — I doubled the energy weight from 2.0 to 4.0 and halved the genre weight from 2.0 to 1.0 to test how sensitive the system was to a single change. The result was more dramatic than I expected. The Lofi Scholar started getting mid-energy songs that had nothing to do with lofi, just because their energy value was close to the target. That told me energy was already the dominant signal before the shift, and the genre weight wasn't doing as much work as I thought. I also tested seven adversarial profiles with contradictory preferences — like wanting a peaceful mood but a very high energy level — to see if the system would crash or return something reasonable. It handled all of them without breaking, though the results for those profiles weren't always meaningful.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- The catalog only has 18 songs, so niche users like jazz or classical fans have almost no real options
- Energy now controls about 30% of the score, which means it can overpower everything else and lock users into a narrow range of songs
- The danceability sweet spot is hardcoded, so ambient and classical songs always get penalized even if the user loves that style
- The system has no way to say "I don't know" — it always returns something, even when nothing fits well
- It does not understand lyrics, language, culture, or any context outside of the numeric features

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> BamBam

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

