import gradio as gr
import requests

BACKEND_URL = "http://localhost:8000"  # Change to your backend URL

def analyze_resume(pdf_file):
    with open(pdf_file, "rb") as f:
        pdf_bytes = f.read()

    files = {"resume": ("resume.pdf", pdf_bytes, "application/pdf")}
    response = requests.post(f"{BACKEND_URL}/match/", files=files)
    response.raise_for_status()

    data = response.json()
    
    # Format job matches nicely
    matches_text = ""
    for job in data.get("matches", []):
        matches_text += (
            f"{job['Job Title']} at {job['Company']} in {job['location']}, {job['Country']} "
            f"(Score: {round(job['match_score'], 2)})\n"
            f"Work Type: {job['Work Type']}, Salary: {job['Salary Range']}, Role: {job['Role']}\n"
            f"Skills: {job['skills']}\n"
            f"Qualifications: {job['Qualifications']}\n"
            f"Responsibilities: {job['Responsibilities'][:200]}...\n\n"
        )
    analysis_text = data.get("hf_model_reply", "No analysis available.")
    return matches_text, analysis_text


with gr.Blocks() as app:
    gr.Markdown("# Resume Matcher\nUpload your resume PDF to get job matches and professional analysis.")
    
    resume_input = gr.File(file_types=[".pdf"], label="Upload your resume (PDF)")
    
    gr.Markdown("## Closest Job Matches")
    job_matches = gr.Textbox(lines=15, interactive=False)
    
    gr.Markdown("## Professional Analysis & Suggestions")
    analysis = gr.Textbox(lines=15, interactive=False)
    
    resume_input.change(
        fn=analyze_resume,
        inputs=resume_input,
        outputs=[job_matches, analysis]
    )

if __name__ == "__main__":
    app.launch()
