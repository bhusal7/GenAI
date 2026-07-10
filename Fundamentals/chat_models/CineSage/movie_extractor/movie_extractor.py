from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-large-latest", temperature=0.9)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an information-extraction engine for movie summaries.
 
TASK:
Read the movie title and the summary paragraph provided by the user, and
extract only the useful, factual information from it. Do not invent details
that are not stated or clearly implied in the summary.
 
RULES:
1. Use only the information present in the given summary — never use outside
   knowledge about the real movie, even if you recognize the title.
2. If a field cannot be determined from the summary, set its value to null
   (for strings) or an empty list (for lists). Never guess.
3. Keep every value concise — no full sentences copied verbatim from the
   summary, rephrase in your own words.
4. "genres" and "themes" must be short lowercase tags (e.g. "revenge",
   "sci-fi"), not sentences.
5. "main_characters" should list only characters explicitly named or clearly
   referred to in the summary, with a short (<=8 word) description each.
6. Do not include any commentary, explanation, or text outside the required
   output format.
 
OUTPUT:
Respond with ONLY a valid JSON object, no markdown fences, matching exactly
this schema:
{{
  "movie_title": string,
  "genres": [string, ...],
  "main_characters": [{{"name": string, "description": string}}, ...],
  "setting": string | null,
  "plot_summary": string,
  "themes": [string, ...],
  "mood": string | null,
  "target_audience": string | null
}}""",
        ),
        (
            "human",
            "Movie Title: {movie_title}\n\nSummary:\n{summary}",
        ),
    ]
)

# ----------------------------------------------------------------------------
# Example run
# ----------------------------------------------------------------------------
movie_title = "Interstellar"
summary = (
    "A former pilot named Cooper leaves his family on a dying Earth to join "
    "a space mission searching for a new habitable planet. Guided by a "
    "scientist named Brand, he travels through a wormhole near Saturn, "
    "faces time dilation on a distant water planet, and ultimately sacrifices "
    "his place on the crew to save the mission, ending up trapped near a "
    "black hole where he discovers a way to communicate with his daughter "
    "across time."
)


paragraph = input("Give your paragraph : ")

chain = prompt | model

 
response = chain.invoke({"movie_title": movie_title, "summary": summary})

print(response.content)
