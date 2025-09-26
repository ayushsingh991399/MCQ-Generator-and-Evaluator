# 📘 MCQ Generator and Evaluator  

An interactive **Streamlit application** that generates **Multiple Choice Questions (MCQs)** from uploaded documents (PDF/TXT) using **Google Gemini (via LangChain)**.  
It also provides a **complexity review and analysis** to ensure the quiz fits the target learners.  

---

## ✨ Features
✅ Upload **PDF or TXT** documents  
✅ Generate **custom MCQs** (control number, subject, and tone)  
✅ Interactive **quiz table view**  
✅ Download quiz in **JSON** or **CSV** formats  
✅ Built-in **review & complexity analysis** from an expert English perspective  

---

## 🛠️ Tech Stack
- **Frontend/UI**: [Streamlit](https://streamlit.io/)  
- **LLM Orchestration**: [LangChain](https://www.langchain.com/)  
- **LLM Backend**: [Google Gemini](https://ai.google.dev/)  
- **Data Processing**: [Pandas](https://pandas.pydata.org/)  
- **File Handling**: [PyPDF2](https://pypi.org/project/PyPDF2/)  

---

## 📂 Project Structure
```
├── app.py                # Main Streamlit app
├── utility.py            # Helper functions (file reading, JSON parsing, table conversion)
├── requirements.txt      # Dependencies
└── README.md             # Documentation
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/mcq-generator.git
   cd mcq-generator
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 API Key Setup
You need a **Google Gemini API key** to run this project.  

1. Get your key from [Google AI Studio](https://aistudio.google.com/).  
2. Enter it directly in the app when prompted.  
   *(Optional: use `.env` + `python-dotenv` for local development.)*  

---

## 📊 How It Works
1. Upload a **PDF or TXT** file.  
2. Enter the **number of MCQs**, **subject**, and select a **tone** (Formal, Casual, Fun, Challenging).  
3. Click **Generate Quiz**.  
4. View questions in a clean, interactive **data table**.  
5. Download quiz as **JSON** or **CSV**.  
6. Read the **complexity review** to check difficulty and tone.  

---

## 📥 Example Output (JSON)
```json
{
  "q1": {
    "mcq": "What is the capital of France?",
    "options": {
      "A": "Paris",
      "B": "London",
      "C": "Berlin",
      "D": "Rome"
    },
    "correct": "A"
  }
}
```

---

## 📸 Demo (Screenshots)
> *(Add screenshots here when running the app for better presentation.)*  

---

## 📜 License
This project is licensed under the **MIT License**.  

---

## 🙌 Acknowledgements
- [Google Gemini](https://ai.google.dev/) – LLM capabilities  
- [LangChain](https://www.langchain.com/) – Prompt orchestration  
- [Streamlit](https://streamlit.io/) – UI framework  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF handling  
- [Pandas](https://pandas.pydata.org/) – Data formatting  

---
