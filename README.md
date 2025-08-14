<div align="center">

# 📝 ResumeCrafter  

ResumeCrafter is an **LLM-powered resume builder** that transforms your **rough skill/experience notes** into a **professionally formatted, rich LaTeX CV**.  
Saving $100+ on Professional Resume Writers
<br>

[🔗 GitHub Repo](https://github.com/Abhaikumar007/ResumeCrafter) | [▶ Run Instructions](#how-to-run)

</div>


---

## 🚀 Features

- **📜 Structured Input Prompt**  
  Works with a `resume_outline.txt` and a `resume_generator_prompt.txt` that guide the LLM on exactly how to interpret and organize your CV data.

- **🖋 Dynamic LaTeX Generation**  
  Generates a LaTeX file that is **professionally styled** using a pre-selected resume template.

- **🛠 Manual Edit Stage**  
  After AI generation, you can manually fine-tune the LaTeX before final PDF export.

- **📄 PDF Export**  
  Converts the polished LaTeX into a **print-ready PDF**.

- **🔄 Auto-updating Resume**  
  Any time you update your skills or experience in `resume_outline.txt`, ResumeCrafter can **re-generate** your CV with the latest data.

---

## 📂 How It Works

1. **Prepare your data**  
   - Write your raw career information in `resume_outline.txt` (skills, experience, projects, etc.).
   - Write your **resume structuring prompt** in `resume_generator_prompt.txt`.

2. **Run ResumeCrafter**  
   - The LLM takes your outline and prompt to generate a **rich, well-structured LaTeX CV**.

3. **Manual Edit Stage (Optional)**  
   - Before compiling, review and tweak the LaTeX file for any final adjustments.

4. **Generate PDF**  
   - ResumeCrafter compiles your final LaTeX into a PDF using your chosen template.

---


---

## ⚠️ Template Warning
We **recommend not changing** the default template unless you know LaTeX well.  
Changing templates may cause formatting issues or LaTeX errors.  

---

## 📦 Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Abhaikumar007/ResumeCrafter
cd ResumeCrafter
```
### Install dependencies
Make sure you have Python 3.8+ installed.
Install required packages:

```bash
pip install -r requirements.txt
```
### Prepare your resume outline
Open input.txt and add your details in this format:

```yaml
Name: John Doe
Email: john@example.com
Phone: +1 234 567 890
Education:
    - B.Sc. Computer Science, XYZ University, 2020-2024
Experience:
    - Software Engineer Intern, ABC Corp, 2023
Skills:
    - Python, Machine Learning, Git
Projects:
    - ResumeCrafter: AI-powered resume builder
```
## ▶️ Running the Application
### Run the main program:
```bash
python app.py
```
---
# STILL IN DEVELOPMENT
---