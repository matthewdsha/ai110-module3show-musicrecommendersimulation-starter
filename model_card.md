# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

Music Musician 1.0

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

This recommender suggests songs that match a user's stated taste — their preferred genre, mood, and target energy level. It assumes the user can describe those three preferences and that a song's fit can be scored by matching them. It's built for classroom exploration, not real users — a small simulation for learning how scoring and ranking work.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The recommender looks at three things about each song: its genre, its mood, and its energy level (how calm or intense it is). It compares those to what the user asked for — a favorite genre, a mood, and a target energy. Then it gives each song points: a genre match is worth the most, a mood match a bit less, and energy adds points based on how close the song is to the user's target. It adds up the points and ranks the songs from highest to lowest, showing the top five with a short reason for each. I tried an experiment — making energy count more and genre count less — but after testing I changed it back, so the final version keeps the original balance.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog has 19 songs. It covers a wide range of genres — pop, lofi, rock, jazz, classical, edm, metal, hip hop, folk, r&b, country, reggae, blues, and more — with matching moods like happy, chill, intense, sad, and romantic. I didn't add or remove any songs; I used the dataset as given. It's small, though, so some tastes are thin or missing — only one or two songs per genre, a lean toward high-energy tracks, and no real coverage of things like world music, kids' music, or very long/experimental styles.

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

One weak is an energy "filter bubble." The energy score uses a linear gap (2.0 × max(0, 1 − |song − target|)), so a mid-energy user (target ~0.5), where every song is within 0.5 distance, gets a flat list whose top picks differ by hundredths of a point, making the ranking almost arbitrary. And because the dataset skews high-energy, the same few loud tracks keep topping the lists, quietly funneling everyone toward the same popular cluster instead of showing variety. The result is a bias that under-serves any listener whose taste falls outside the catalog's center.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested eight profiles. Three were normal tastes: High-Energy Pop (pop, happy, 0.85), Chill Lofi (lofi, chill, 0.35), and Deep Intense Rock (rock, intense, 0.9). Five were adversarial edge cases: Sad but Hyped (sad, 0.9), Energy-Only (0.5), Empty ({}), Impossible Energy (1.5), and Nonexistent Tastes (labels not in the dataset).

I checked three things for each profile: whether the #1 pick actually matched the request (a pop/happy/high-energy user should get a loud pop song, not a quiet ballad), whether the explanation lines added up to the printed score, and whether the top five showed real variety or just repeated the same few tracks. For the adversarial profiles I also looked for graceful failure — no crashes, no bad scores, and a sensible fallback when nothing matched. In short, I wanted the results to be faithful to the request, explainable from the math, and robust against odd input.

The biggest surprise was that Sad but Hyped returned a slow, sad song instead of a loud one — the +1.0 mood match beat everyone's energy score. I was also surprised nothing broke on the impossible 1.5 energy (the clamp held), and how tightly the energy-only picks clustered (a near-tie in the 1.80–2.00 range).

Comparing the normal profiles, Pop and Lofi were mirror images — Pop pulled loud songs, Lofi pulled quiet ones — because their opposite energy targets sweep opposite ends of the catalog. Pop and Rock shared a high-energy band but had different winners, since genre and mood bonuses broke the tie. Lofi and Rock overlapped in nothing at all, confirming energy is the main axis separating listeners.

Comparing normal vs. adversarial, Rock and Sad but Hyped both wanted energy 0.9, so their lists were nearly identical except #1 — showing the mood label was the only wildcard. Pop and Nonexistent Tastes showed what labels add: Pop's matches lifted a clear winner, while Nonexistent collapsed into a flat energy-only ranking. Among the edge cases, Energy-Only vs. Impossible Energy were opposite failures — 0.5 hit a perfect bullseye, while 1.5 could never score on energy and leaned on genre/mood instead.

Every result was valid — no crashes or bad scores — and each comparison traces back to one part of the scoring: energy separates the profiles, and genre/mood bonuses break ties.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

A few ways I'd improve it next. I'd use more of the song data that's already there, like danceability and how acoustic a song is, so the matches feel more personal. I'd make the explanations friendlier, saying something like "picked because it's upbeat and matches your energy" instead of showing raw points. I'd add a way to keep the top five varied, so the list doesn't repeat the same few loud songs. And I'd let the system handle trickier tastes — users who like more than one genre, or who give contradictory preferences like "sad but high-energy" — instead of treating every preference as all-or-nothing.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I always thought recommender systems were a lot more complex or complicated, but then I learned that its more of a simple formula that calculates what things to recommend over others. This was very interesting to find out when I had to research YouTube and Spotify as well as working on this recommender. I also found it interesting how some systems use multiple recommender systems. This made me appreciate recommenders a lot more and understand where these recommendations come from.