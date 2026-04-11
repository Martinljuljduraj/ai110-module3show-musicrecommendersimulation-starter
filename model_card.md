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

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

---

### Profile Output Comparison

When I ran the three main profiles side by side, the differences were clear and made intuitive sense — but also revealed where the system is doing something sneaky.

The **Gym Enthusiast** (target energy 0.90, mood: intense, genre: pop) consistently pulled in songs like *Gym Hero*, *Voltage Drop*, and *Storm Runner*. That makes sense — those songs are loud, fast, and built for physical effort. But here is the interesting part: *Gym Hero* also showed up for the **Happy Pop** user. Why? Because *Gym Hero* has energy 0.93, valence 0.77, and tempo 132 BPM — it scores well on almost every numeric rule for a pop/happy listener too. The song is not wrong for that user, but it was not designed for them. The system does not know the difference between "high energy because you are running" and "high energy because you are happy" — it just sees a number close to the target and rewards it.

The **Lofi Scholar** (target energy 0.38, mood: focused, genre: lofi) got results that felt the most accurate — *Midnight Coding*, *Library Rain*, and *Focus Flow* all came up, which are genuinely quiet, studious songs. This profile worked well because the catalog actually has a small cluster of lofi songs that match on energy, mood, and activities all at once. The system looked smart here, but mostly because the data happened to cooperate.

The **Indie Enthusiast** (target energy 0.75, mood: chill, genre: indie pop) produced the most mixed results. Songs like *Rooftop Lights* fit perfectly, but the system also surfaced songs from other genres that simply had similar energy and valence values. That is the core lesson: the recommender does not truly understand genre or mood the way a person does — it matches numbers. When the numbers line up by coincidence, the result looks wrong even if the score was technically high.
