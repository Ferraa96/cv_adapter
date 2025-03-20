import os
from dotenv import load_dotenv
from tqdm import tqdm
import yaml
from llm_service import LLMService
import subprocess


class AdaptCV:
    
    def transform_cv(self, data, transform_func, cv_writer, keywords=None):
        progress_bar = tqdm(desc="Processed elements", unit=" items")
        
        def traverse_dict(data, transform_func, cv_writer, keywords):
            progress_bar.update(1)
            if isinstance(data, dict):
                return {k: traverse_dict(v, transform_func, cv_writer, keywords) for k, v in data.items()}
            elif isinstance(data, list):
                return [traverse_dict(v, transform_func, cv_writer, keywords) for v in data]
            elif isinstance(data, str):
                return transform_func(cv_writer, {'section_text': data, 'keywords': keywords})
            else:
                return data
        
        transformed_data = traverse_dict(data, transform_func, cv_writer, keywords)
        progress_bar.close()
        
        return transformed_data

    
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
        cv_writer = queries["rewrite_section"]
        
        keywords = llm_service.query_llm(job_analyzer, {'job_description': job_description})
        print("Keywords extracted from the job description:")
        print(keywords)
        
        print("Rewriting the CV sections based on the job description...")
        cv_content['cv']['sections'] = self.transform_cv(
            cv_content['cv']['sections'], 
            llm_service.query_llm,
            cv_writer,
            keywords
        )
        
        with open('data/cv_modified.yaml', 'w') as file:
            yaml.dump(cv_content, file, default_flow_style=False, sort_keys=False)
    
    
    def run_render_cv(self):
        """
        Run the 'rendercv render' command to render the modified CV.
        render_cv creates the cv files from the CV data in the 'rendercv_output' folder.
        """
        cv_file = 'data/cv_modified.yaml'
        result = subprocess.run(["rendercv", "render", cv_file], capture_output=True, text=True, shell=True)
        
        if not result.returncode == 0:
            print('An error occurred while running the command.')
            print('Error in rendering the CV.')
        


def main():
    adapt_cv = AdaptCV()
    adapt_cv.adapt()
    adapt_cv.run_render_cv()


if __name__ == "__main__":
    main()
    