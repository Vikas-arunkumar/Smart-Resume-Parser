# 🚀 TalentScan - AI Powered Resume Screening System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-Web%20App-red?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/NLP-Resume%20Parsing-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge" />
</p>

<p align="center">
  An intelligent recruitment platform that automates resume screening, candidate evaluation, and job matching using Natural Language Processing (NLP).
</p>

---

## 📌 Overview

Recruiters often spend hours manually reviewing resumes to identify suitable candidates. TalentScan simplifies this process by automatically extracting candidate information, identifying skills, and calculating job-match scores.

The system enables recruiters to quickly shortlist applicants while providing candidates with an easy way to apply for relevant job openings.

---

## ✨ Key Features

### 👨‍💼 Candidate Portal

* Upload resumes in PDF/DOCX format
* Automatic resume parsing
* Candidate profile extraction
* Instant application submission
* Real-time job matching

### 🏢 Recruiter Dashboard

* Create and manage job postings
* View candidate applications
* Track application status
* Compare applicants using match scores
* Streamlined hiring workflow

### 🤖 AI & NLP Engine

* Resume text extraction
* Skill identification
* Contact information extraction
* Education detection
* Experience extraction
* Job-role matching
* Candidate ranking

---

## 🧠 NLP Pipeline

```text
Resume Upload
      │
      ▼
Text Extraction
      │
      ▼
Preprocessing
(Tokenization, Cleaning)
      │
      ▼
Information Extraction
(Name, Email, Phone)
      │
      ▼
Skill Detection
      │
      ▼
Job Matching
      │
      ▼
Candidate Ranking
```

---

## 🛠️ Tech Stack

| Category                | Technology                      |
| ----------------------- | ------------------------------- |
| Frontend                | Streamlit                       |
| Backend                 | Python                          |
| NLP                     | NLTK, Regex, Text Processing    |
| Data Storage            | JSON                            |
| Resume Parsing          | PyPDF2, pdfplumber, python-docx |
| Development Environment | VS Code                         |

---

## 📂 Project Structure

```bash
TalentScan/
│
├── main.py
├── resume_parser.py
├── skills_db.py
│
├── data/
│   ├── jobs.json
│   ├── applications.json
│   └── resumes/
│
├── assets/
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/TalentScan.git
cd TalentScan
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run Application

```bash
streamlit run main.py
```

Application will launch at:

```text
http://localhost:8501
```

---

## 🎯 How It Works

### Candidate Workflow

1. Upload Resume
2. Resume Parsed Automatically
3. Skills Extracted
4. Matching Jobs Displayed
5. Application Submitted

### Recruiter Workflow

1. Create Job Posting
2. Receive Applications
3. View Match Scores
4. Shortlist Candidates
5. Continue Recruitment Process

---

## 📊 Sample Information Extracted

The system can automatically identify:

✅ Candidate Name

✅ Email Address

✅ Phone Number

✅ Technical Skills

✅ Educational Qualifications

✅ Work Experience

✅ Resume Keywords

---

## 🔥 Future Enhancements

* Machine Learning Based Ranking
* Semantic Skill Matching
* Resume Recommendation Engine
* PostgreSQL / MongoDB Integration
* User Authentication
* Email Notifications
* Interview Scheduling
* AI-Powered Candidate Insights
* Generative AI Resume Analysis

---

## 📸 Screenshots

Add screenshots of your application here.

### Home Page

```text
assets/homepage.png
```

### Recruiter Dashboard

```text
assets/recruiter_dashboard.png
```

### Candidate View

```text
assets/candidate_portal.png
```

---

## 🎓 Academic Context

This project was developed as part of coursework and practical exploration in:

* Natural Language Processing
* Information Retrieval
* Software Engineering
* Full Stack Application Development

---

## 👨‍💻 Author

### Vikas Arunkumar

B.Tech Information Technology

Madras Institute of Technology (MIT)

Anna University

---

## ⭐ Support

If you found this project useful:

⭐ Star the repository

🍴 Fork the project

📢 Share it with others

---

<p align="center">
  Built with ❤️ using Python, Streamlit and NLP
</p>
