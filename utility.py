import PyPDF2
import json



def read_file(file):
    
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise Exception(f"Error reading the PDF file: {e}")
    
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    
    else:
        raise Exception("Unsupported file format. Only PDF and TXT supported")
    
def safe_json_parse(quiz_str):

    try:
        return json.loads(quiz_str)
    except json.JSONDecodeError:
        import re
        
        match = re.search(r"\{.*\}", quiz_str, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return None
        return None

def get_table_data(quiz_dict):
    
    quiz_table_data = []
    for i, (key, value) in enumerate(quiz_dict.items(), start=1):
        mcq = value.get("mcq", "N/A")
        options_dict = value.get("options", {})
        if isinstance(options_dict, dict):
            # Format choices with newlines for better spacing in the table
            options = " || ".join([f"{opt} -> {opt_val}" for opt, opt_val in options_dict.items()])
        else:
            options = "N/A"
        
        correct = value.get("correct", "N/A")

        quiz_table_data.append({
            "No.": i,
            "MCQ": mcq,
            "Choices": options,
            "Correct": correct
        })
    
    return quiz_table_data
