# 🎬 Movie Information Extractor

A LangChain project that extracts structured movie information from a movie summary using the **Mistral Large** language model.

The application reads a movie title and its summary, then returns the extracted information as a JSON object.

## Features

* Extracts structured information from movie summaries
* Returns data in JSON format
* Uses prompt engineering for reliable extraction
* Powered by LangChain and Mistral AI
* Available as both a Python script and a Streamlit application

## Technologies Used

* Python
* LangChain
* Mistral AI
* Streamlit
* python-dotenv

## Project Structure

```
movie_extractor/
│── app.py                 # Streamlit application
│── movie_extractor.py     # Python script
│── requirements.txt
│── .gitignore
│── README.md
```

## Installation

```bash
git clone <repository-url>

cd movie_extractor

pip install -r requirements.txt
```

Create a `.env` file and add your API key.

```
MISTRAL_API_KEY=your_api_key_here
```

## Run the Python Version

```bash
python movie_extractor.py
```

## Run the Streamlit Version

```bash
streamlit run app.py
```

## Example Output

```json
{
  "movie_title": "Interstellar",
  "genres": [
    "science fiction",
    "adventure"
  ],
  "main_characters": [
    {
      "name": "Cooper",
      "description": "Former pilot"
    },
    {
      "name": "Brand",
      "description": "Scientist"
    }
  ],
  "setting": "Earth and outer space",
  "plot_summary": "A former pilot joins a space mission to find a habitable planet.",
  "themes": [
    "survival",
    "family",
    "space exploration"
  ],
  "mood": "hopeful",
  "target_audience": "science fiction fans"
}
```

## License

This project is created for learning and educational purposes.
