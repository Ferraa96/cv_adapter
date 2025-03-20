# CV Adapter

CV Adapter is a tool designed to adapt your CV based on a job description. It leverages large language models (LLMs) to analyze job descriptions and rewrite CV sections to optimize them for applicant tracking systems (ATS).

## Features

- Analyzes job descriptions to extract relevant keywords.
- Rewrites CV sections using the extracted keywords.
- Supports multiple LLM providers (OpenAI, Ollama, Groq).
- Generates CVs in multiple formats (e.g., LaTeX, Markdown, HTML).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/cv_adapter.git
    cd cv_adapter
    ```

2. Install dependencies using Poetry:
    ```sh
    poetry install
    ```

3. Edit the file `edit.env` file in the root directory and add your API keys:
    ```env
    AI_PROVIDER=your_provider
    GROQ_API_KEY=your_groq_api_key
    OLLAMA_MODEL=your_ollama_model_name
    ```
    Modify the name of the file in `.env`

## Usage

1. Place your job description in the `data/job_description.txt` file.
2. Place your CV data in the `data/cv.yaml` file.
3. Run the CV Adapter:
    ```sh
    poetry run start
    ```

4. The modified CV will be saved to `data/cv_modified.yaml`.
5. To render the modified CV, run:
    ```sh
    poetry run python adapt_cv.py
    ```

## Project Structure

- `data/`: Directory containing job descriptions, CV data, and rendered CVs.
- `rendercv_output/`: Directory containing the output of the rendered CVs.
