from flask import Flask, render_template, request, send_file
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure Gemini API Key
GEMINI_API_KEY = "Your API Key"
genai.configure(api_key=GEMINI_API_KEY)

# Function to generate MCQs
def generate_mcqs(unit_title, unit_content):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Generate 15 multiple-choice questions (MCQs) with 4 options each and correct answers from the following syllabus unit:\n\nUnit Title: {unit_title}\nContent:\n{unit_content}"
        
        response = model.generate_content(prompt)
        return response.text if response else "Error generating MCQs"
    
    except Exception as e:
        return f"Error generating MCQs: {str(e)}"

# Function to generate Internal Assessment Question Paper
def generate_internal_paper(units):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""Generate an Internal Assessment Question Paper with the following structure:

        Part A – 2 Mark Questions (Q1 to Q10)
        - Q1 to Q4: Short conceptual questions following the patterns of Unit I.
        - Q5 to Q8: Short conceptual questions following the patterns of Unit II.
        - Q9 & Q10: Short conceptual questions following the patterns of Unit III.

        Part B – 16 Mark Questions (Q11 & Q12)
        - Provide 4 questions in total.
        - Q11: Either-or question (2 questions based on concepts from Unit I).
        - Q12: Either-or question (2 questions based on concepts from Unit II).

        Part C – 8 Mark Question (Q13)
        - Provide 2 options for an either-or question from Unit III.

        Do not mention the syllabus units in the question paper. Just list the questions in the given format.
        Ensure that all questions are conceptually clear and structured appropriately for database concepts.
        """

        response = model.generate_content(prompt)
        return response.text if response else "Error generating IA question paper"

    except Exception as e:
        return f"Error generating IA question paper: {str(e)}"  

@app.route("/", methods=["GET", "POST"])
def index():
    units_mcq_data = {}
    ia_paper = ""
    selected_mode = ""

    if request.method == "POST":
        syllabus_text = request.form["syllabus"]
        selected_mode = request.form["mode"]
        units = syllabus_text.split("UNIT ")

        unit_list = []
        for unit in units:
            if unit.strip():
                unit_parts = unit.split("\n", 1)
                unit_title = "UNIT " + unit_parts[0].strip()
                unit_content = unit_parts[1].strip() if len(unit_parts) > 1 else ""
                unit_list.append({"title": unit_title, "content": unit_content})

        if selected_mode == "mcq":
            for unit in unit_list:
                mcqs = generate_mcqs(unit["title"], unit["content"])
                units_mcq_data[unit["title"]] = mcqs

        elif selected_mode == "ia":
            if len(unit_list) < 3:
                ia_paper = "Error: At least 3 units are required to generate an IA Question Paper."
            else:
                ia_paper = generate_internal_paper(unit_list[:3])

    return render_template("index.html", units_mcq_data=units_mcq_data, ia_paper=ia_paper, selected_mode=selected_mode)

@app.route("/download", methods=["POST"])
def download():
    try:
        unit_title = request.form["unit_title"]
        mcq_data = request.form["mcq_data"]
        filename = f"{unit_title.replace(' ', '_')}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"{unit_title}\n\n{mcq_data}")

        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return f"Error downloading file: {str(e)}"

@app.route("/download_ia", methods=["POST"])
def download_ia():
    try:
        ia_paper = request.form["ia_paper"]
        filename = "Internal_Assessment_Question_Paper.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(ia_paper)

        return send_file(filename, as_attachment=True)
    
    except Exception as e:
        return f"Error downloading IA question paper: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
