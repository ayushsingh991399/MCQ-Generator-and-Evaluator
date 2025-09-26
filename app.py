import streamlit as st
import json
import traceback
import pandas as pd
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from utility import read_file, safe_json_parse, get_table_data

st.title("MCQ Generator and Evaluator")

# User inputs
api_key = st.text_input("Enter your Google Gemini API Key", type="password")
uploaded_file = st.file_uploader("Upload your PDF or TXT file", type=["pdf", "txt"])
number_of_mcqs = st.number_input("Number of MCQs", min_value=1, max_value=50, value=5)
subject = st.text_input("Subject", value="General Knowledge")
tone = st.selectbox("Tone of the MCQs", ["Formal", "Casual", "Fun", "Challenging"])
generate_button = st.button("Generate Quiz")

# --------------------------
# Async function for quiz
# --------------------------
async def generate_quiz_async(text, number, subject, tone, api_key):
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=api_key.strip()
    )

    # Quiz template
    response_json_template = json.dumps({
        "q1": {
            "mcq": "Question text",
            "options": {"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"},
            "correct": "A"
        }
    }, indent=2)

    quiz_template = """
Text:{text}
You are an expert MCQ maker. Given the above text, create {number} multiple choice questions for {subject} students in {tone} tone. 

Rules:
- Return ONLY valid JSON.
- Do not add any text outside the JSON.
- Follow exactly the format in RESPONSE_JSON.
- Ensure there are {number} questions.

### RESPONSE_JSON
{response_json}
"""
    quiz_prompt = PromptTemplate(
        input_variables=["text", "number", "subject", "tone", "response_json"],
        template=quiz_template
    )
    quiz_chain = LLMChain(llm=llm, prompt=quiz_prompt, output_key="quiz", verbose=False)

    # Review template
    review_template = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for {subject} students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
If the quiz is not at par with the cognitive and analytical abilities of the students,
update the quiz questions which need to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}
Just do the analysis.
Dont send the updated quiz. 
Check from an expert English Writer of the above quiz:
"""
    review_prompt = PromptTemplate(input_variables=["subject", "quiz"], template=review_template)
    review_chain = LLMChain(llm=llm, prompt=review_prompt, output_key="review", verbose=False)

    # Combine chains
    overall_chain = SequentialChain(
        chains=[quiz_chain, review_chain],
        input_variables=["text", "number", "subject", "tone", "response_json"],
        output_variables=["quiz", "review"],
        verbose=False
    )

    # Run the chain asynchronously
    result = await asyncio.to_thread(
        overall_chain.run,
        {
            "text": text,
            "number": number,
            "subject": subject,
            "tone": tone,
            "response_json": response_json_template
        }
    )
    return result

# --------------------------
# Streamlit button click
# --------------------------
if generate_button:
    if not api_key.strip():
        st.error("Please enter your Google Gemini API key.")
    elif not uploaded_file:
        st.error("Please upload a PDF or TXT file.")
    else:
        with st.spinner("Generating quiz... This may take a moment."):
            try:
                text = read_file(uploaded_file)
                # Run async function
                result = asyncio.run(generate_quiz_async(text, number_of_mcqs, subject, tone, api_key))

                st.success("Quiz Generated!")
                parsed_quiz = safe_json_parse(result["quiz"])

                if parsed_quiz:
                    st.subheader("Quiz Table")
                    quiz_table = get_table_data(parsed_quiz)
                    if quiz_table:
                        df = pd.DataFrame(quiz_table).set_index("No.")
                        st.dataframe(df, use_container_width=True)

                        # Download buttons
                        st.download_button(
                            "Download Quiz as JSON",
                            data=json.dumps(parsed_quiz, indent=2),
                            file_name=f"{subject}_quiz.json",
                            mime="application/json"
                        )

                        st.download_button(
                            "Download Quiz as CSV",
                            data=df.to_csv(index=False),
                            file_name=f"{subject}_quiz.csv",
                            mime="text/csv"
                        )
                    else:
                        st.warning("Could not parse quiz to table.")
                else:
                    st.error("Quiz output is not valid JSON. No table generated.")

                st.subheader("Evaluation & Review")
                st.info(result["review"])

            except Exception:
                st.error("Error generating quiz:")
                st.text(traceback.format_exc())
