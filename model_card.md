# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
**BamBam**

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

BamBam suggests songs from a small catalog based on a user's preferred genre, mood, energy level, and activities. It assumes the user can describe their taste with a few simple preferences — a favorite genre, a target energy, and what they are doing while listening. This is a classroom simulation, not a production tool. It is not connected to any real streaming service and is not meant for real users.

**Not intended for:** Real-world deployment, personalized health or wellness recommendations, or any context where a wrong recommendation could cause harm.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

Every song gets a score based on how well it matches what the user told us they like. The system checks eight things: whether the genre matches, whether the mood matches, how close the song's energy is to what the user wants, how close the emotional tone (valence) is, how close the tempo is, whether the song falls in a danceable range, whether the song is acoustic or electric, and whether it fits the user's activities like studying or working out. Each check adds points. The song with the most points wins.

I doubled the energy weight compared to the original design — so energy now has the biggest influence on the final score. I also halved the genre weight, meaning two songs with different genres but similar energy levels will rank closer together than before.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 18 songs. Genres include lofi, pop, rock, indie pop, indie rock, indie folk, jazz, ambient, synthwave, hip-hop, r&b, electronic, funk, heavy metal, and classical. Moods covered are chill, happy, intense, focused, relaxed, moody, melancholic, romantic, peaceful, energetic, and angry. I did not add or remove any songs from the starter data. The dataset skews toward Western genres and does not include Latin, K-pop, Afrobeats, country, or any non-English music traditions. It also has very few songs in some categories — there is only one classical song and one jazz song — so users who prefer those genres have almost nothing to match against.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

BamBam works best when the user has a clear, specific profile. The Lofi Scholar got near-perfect results — every top song was genuinely quiet, study-friendly, and matched the genre. The Gym Enthusiast also got consistently appropriate songs, all high-energy and activity-tagged for workouts. The system is also fully transparent: every score comes with a breakdown showing exactly why each song ranked where it did, which makes it easy to understand and debug.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The biggest bias is the dominance energy creates, which I will call an "energy tunnel". When I doubled the weight of energy from 2.0 to 4.0 and the max score a song can get is 13.5, this makes up about 30% of the total score. We hardcoded the danceability sweet spot. A user who explicitly prefers ambient and relaxing music will still get docked on every ambient song. The tempo window is too wide to discriminate. Almost every song earns some tempo credit from almost every user. The rule is so permissive it adds noise rather than signal. A user with a niche activity not in the catalog (e.g., "cooking", "meditating") gets 0 activity points for every song — effectively losing up to 2.0 points from their score ceiling relative to users with mainstream activities. Finally, there is no genre diversity constraint.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested three standard profiles — Indie Enthusiast, Lofi Scholar, and Gym Enthusiast — chosen because they sit far apart in energy, mood, and tempo, making it easy to spot whether the system was actually differentiating between them. For each, I checked that the top songs matched the stated genre and mood first, then verified the numeric attributes were trending in the right direction.

I also ran seven adversarial cases to stress-test the logic — contradictory inputs like a "peaceful" mood user with target_energy = 0.95, or an empty activities list — checking that the system degraded gracefully rather than producing nonsense rankings.

The most surprising result came from the weight-shift experiment. Doubling the energy weight had a bigger effect than expected: the Lofi Scholar started receiving mid-energy songs with no connection to lofi or chill moods, just because their energy value was numerically close. That revealed energy was already doing most of the ranking work before the shift.


---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

1. **Add a diversity rule.** Right now the top 5 results can all be the same genre. A simple fix would be to cap how many songs from the same genre can appear in one recommendation list.
2. **Make the danceability zone user-driven.** Instead of a hardcoded sweet spot at [0.55, 0.85], let the user set a preferred danceability range so classical and ambient listeners are not automatically penalized.
3. **Expand the catalog.** 18 songs is too small for niche users. A jazz fan or classical fan only has one option each — that is not a real recommendation, it is just the only match available.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

Building BamBam taught me that a recommender is only as smart as its weights. The system does not understand music but rather it just adds up numbers. When I doubled the energy weight, I expected a small shift, but the whole ranking changed in ways that felt wrong which surprised me. It also made me realize that Spotify or YouTube probably have hundreds of signals being weighted against each other, and small changes in those weights could mean the difference between a recommendation that feels personal and one that feels random. The part I found most interesting is that the system can look smart or dumb depending entirely on whether the catalog has enough songs to match a user's profile. When the data cooperated, the results felt great. When it did not, the system had no way to say "I don't know". The system just gave you whatever was closest.

---

### Profile Output Comparison

When I ran the three main profiles side by side, the differences were clear and made intuitive sense — but also revealed where the system is doing something sneaky.

The **Gym Enthusiast** (target energy 0.90, mood: intense, genre: pop) consistently pulled in songs like *Gym Hero*, *Voltage Drop*, and *Storm Runner*. That makes sense — those songs are loud, fast, and built for physical effort. But here is the interesting part: *Gym Hero* also showed up for the **Happy Pop** user. Why? Because *Gym Hero* has energy 0.93, valence 0.77, and tempo 132 BPM — it scores well on almost every numeric rule for a pop/happy listener too. The song is not wrong for that user, but it was not designed for them. The system does not know the difference between "high energy because you are running" and "high energy because you are happy" — it just sees a number close to the target and rewards it.

The **Lofi Scholar** (target energy 0.38, mood: focused, genre: lofi) got results that felt the most accurate — *Midnight Coding*, *Library Rain*, and *Focus Flow* all came up, which are genuinely quiet, studious songs. This profile worked well because the catalog actually has a small cluster of lofi songs that match on energy, mood, and activities all at once. The system looked smart here, but mostly because the data happened to cooperate.

The **Indie Enthusiast** (target energy 0.75, mood: chill, genre: indie pop) produced the most mixed results. Songs like *Rooftop Lights* fit perfectly, but the system also surfaced songs from other genres that simply had similar energy and valence values. That is the core lesson: the recommender does not truly understand genre or mood the way a person does — it matches numbers. When the numbers line up by coincidence, the result looks wrong even if the score was technically high.
