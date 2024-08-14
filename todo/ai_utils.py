import google.generativeai as genai
from local_settings import API_KEY


genai.configure(api_key=API_KEY)


model = genai.GenerativeModel('gemini-1.5-flash')

def summarize_text(paragraph):
    PROMPT = f"""
    explain what is
    "{paragraph}"
    
    in 3 detailed sentences. If you do not have enough infomation about it, just say :"I don't have enough information"
    """
    
    
    response = model.generate_content(PROMPT)
    
    
    return response.text.strip()

def analyze_task_content(title, content):
    PROMPT = f"""
    You are given a task with the title: "{title}" and the content: "{content}".
    1. Check if the content aligns with the task title. If the content is consistent and reasonable for the given title, respond with "The content is appropriate for the title."
    2. If the content does not align with the title, or is insufficient or vague, respond with "The content does not match the title" and explain why in 1-2 sentences. Then, provide a specific suggestion on how to rewrite the content to better match the title.
    Make sure your suggestions are actionable and easy to follow.
    """
    # Call the API to analyze the content
    response = model.generate_content(PROMPT)
    # Return the analysis result
    return response.text.strip()