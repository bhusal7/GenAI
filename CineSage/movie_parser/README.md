# 🎥 Movie Information Parser

A LangChain project that demonstrates **structured output parsing** using **PydanticOutputParser**.

Instead of manually requesting JSON, this project defines a Pydantic schema and lets LangChain automatically instruct the language model to generate output that matches the schema.

## Features

* Structured output using Pydantic
* Automatic output validation
* Uses `PydanticOutputParser`
* Powered by LangChain and Mistral AI
* Available as both a Python script and a Streamlit application

## Technologies Used

* Python
* LangChain
* Pydantic
* Mistral AI
* Streamlit
* python-dotenv

## Project Structure

```
movie_parser/
│── app.py              # Streamlit application
│── movie_parser.py     # Python script
│── requirements.txt
│── .gitignore
│── README.md
```

## Installation

```bash
git clone <repository-url>

cd movie_parser

pip install -r requirements.txt
```

Create a `.env` file.

```
MISTRAL_API_KEY=your_api_key_here
```

## Run the Python Version

```bash
python movie_parser.py
```

## Run the Streamlit Version

```bash
streamlit run app.py
```

## Output Schema

```python
class Movie(BaseModel):
    title: str
    release_year: Optional[int]
    genre: List[str]
    director: Optional[str]
    cast: List[str]
    rating: Optional[float]
    summary: str
```

## Example Output

```json
{
  "title": "Interstellar",
  "release_year": 2014,
  "genre": [
    "Science Fiction",
    "Adventure"
  ],
  "director": "Christopher Nolan",
  "cast": [
    "Matthew McConaughey",
    "Anne Hathaway",
    "Jessica Chastain"
  ],
  "rating": 8.7,
  "summary": "A former pilot joins a mission to find a new home for humanity."
}
```

## License

This project is created for learning and educational purposes.
