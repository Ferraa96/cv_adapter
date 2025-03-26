import json
import os
import sys
from loading_anim import loading_animation
from dotenv import load_dotenv
import yaml
from llm_service import LLMService
import subprocess


class AdaptCV:
    
    @loading_animation
    def adapt(self):
        """
        Adapt the CV based on the job description.
        Reads the job description from the 'data/job_description.txt' file and the CV from the 'data/cv.yaml' file.
        Queries the LLM model to analyze the job description and rewrite the CV sections based on the job description.
        Writes the modified CV to the 'data/cv_modified.yaml' file.
        """
        job_description_file = 'data/job_description.txt'
        cv_file = 'data/cv.yaml'
        queries_file = 'cv_queries.yaml'
        
        try:
            with open(job_description_file, 'r') as file:
                job_description = file.read()
            
            with open(cv_file, 'r') as file:
                cv_content = file.read()
                cv_content = yaml.safe_load(cv_content)
            
            with open(queries_file, "r") as file:
                queries = file.read()
                queries = yaml.safe_load(queries)
        
        except FileNotFoundError:
            raise FileNotFoundError("Please make sure that the 'job_description.txt' and 'cv.yaml' files exist in the 'data' directory.")
            
        
        load_dotenv()
        llm_service = LLMService(
            provider=os.getenv("AI_PROVIDER"),
            api_key=os.getenv("API_KEY"),
            model_name=os.getenv("OLLAMA_MODEL")
        )
        
        print("Processing the job description...")
        job_analyzer = queries["analyze_jd"]
        cv_writer = queries["rewrite_sections"]
        
        keywords = llm_service.query_llm(job_analyzer, {'job_description': job_description})
        print("Keywords extracted from the job description:")
        print(keywords)
        
        print("Rewriting the CV sections based on the job description...")
        valid_output = False
        failed_runs = 0
        while not valid_output:
            modified_sections = llm_service.query_llm(
                cv_writer, 
                {
                    'sections_text': cv_content['cv']['sections'], 
                    'keywords': keywords
                }
            ).replace("'", "\"")
            
            # fix malformed json output
            if modified_sections.startswith('`'):
                modified_sections = '\n'.join(modified_sections.splitlines()[1:]).rstrip('`')
            
            try:
                modified_sections = json.loads(modified_sections)
            except json.decoder.JSONDecodeError:
                failed_runs += 1
                print(f'Failed to decode the modified CV sections, retrying (attempt {failed_runs+1})')
                if failed_runs > 1:
                    print("Failed to decode the modified CV sections. Please try again.")
                    print(modified_sections)
                    sys.exit()
        
        cv_content['cv']['sections'] = modified_sections
        
        with open('data/cv_modified.yaml', 'w') as file:
            yaml.dump(cv_content, file, default_flow_style=False, sort_keys=False)
    
    
    @loading_animation
    def run_render_cv(self):
        """
        Run the 'rendercv render' command to render the modified CV.
        render_cv creates the cv files from the CV data in the 'rendercv_output' folder.
        """
        cv_file = 'data/cv_modified.yaml'
        
        with subprocess.Popen(["rendercv", "render", cv_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True) as process:
            for line in process.stdout:
                print(line, end='')

            for line in process.stderr:
                print(line, end='', file=sys.stderr)


def main():
    adapt_cv = AdaptCV()
    adapt_cv.adapt()
    adapt_cv.run_render_cv()


if __name__ == "__main__":
    main()
    