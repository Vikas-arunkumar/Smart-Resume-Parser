# 🔍 TalentScan – Intelligent Resume Screening System

<p align="center">
  <h3 align="center">AI-Powered Resume Parsing & Candidate Matching Platform</h3>
  <p align="center">
    Built using Python, Streamlit and Natural Language Processing (NLP)
  </p>
</p>

---

## 📖 About The Project

TalentScan is an intelligent recruitment platform that automates resume screening and candidate evaluation using Natural Language Processing techniques.

The system extracts important information from uploaded resumes, identifies technical skills, analyzes candidate qualifications, and matches applicants against available job openings.

Instead of manually reviewing hundreds of resumes, recruiters can quickly identify the most suitable candidates through automated skill matching and ranking.

---

## ✨ Features

### 👨‍💼 Candidate Features

* Upload resumes in PDF format
* Automatic resume parsing
* Skill extraction
* Job matching based on qualifications
* Application submission

### 🏢 Recruiter Features

* View available candidates
* Manage job openings
* Track applications
* Review candidate profiles
* Compare match scores

### 🤖 NLP Features

* Resume text extraction
* Tokenization
* Stopword removal
* Lemmatization
* Entity extraction
* Skill detection
* Education detection
* Experience extraction
* Job-role matching

---

## 🧠 NLP Pipeline

```text
Resume Upload
      │
      ▼
Text Extraction
(PDF / DOCX)
      │
      ▼
Preprocessing
      │
      ├─ Cleaning
      ├─ Tokenization
      ├─ Stopword Removal
      └─ Lemmatization
      │
      ▼
Information Extraction
      │
      ├─ Name
      ├─ Email
      ├─ Phone
      ├─ Education
      └─ Experience
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

## 🛠 Technologies Used

### Frontend

* Streamlit

### Backend

* Python

### Resume Processing

* PyPDF2
* pdfplumber
* python-docx

### NLP Techniques

* Tokenization
* Stopword Removal
* Lemmatization
* Regex-Based Entity Extraction
* Skill Matching
* Resume Scoring

### Data Storage

* JSON Files

---

## 📂 Project Structure

```text
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
└── README.md
```

---

## 🎯 How It Works

### Step 1

Recruiters create job openings with required skills.

### Step 2

Candidates upload their resumes.

### Step 3

The NLP engine extracts:

* Contact Information
* Education
* Experience
* Technical Skills

### Step 4

Extracted skills are compared against job requirements.

### Step 5

A match score is generated.

### Step 6

Recruiters can review and shortlist candidates efficiently.

---

## 📊 Skills Database

TalentScan contains an extensive skill database covering:

* Programming Languages
* Frontend Technologies
* Backend Technologies
* Databases
* Cloud Computing
* Machine Learning
* Artificial Intelligence
* DevOps Tools
* Data Analytics
* Software Engineering

---

## 🚀 Future Improvements

* Machine Learning based ranking
* Semantic skill matching using embeddings
* MongoDB / PostgreSQL integration
* Authentication system
* Email notifications
* Interview scheduling
* Recruiter analytics dashboard
* Generative AI resume analysis

---

## 🎓 Academic Context

Developed as part of:

**IT23602 – Natural Language & Image Processing**

**Madras Institute of Technology (MIT)**

**Anna University**

---

## 👨‍💻 Author

**Vikas Arunkumar**

B.Tech Information Technology

Madras Institute of Technology (MIT)

Anna University

---

## ⭐ If You Like This Project

Give this repository a ⭐ and support the project.

---

<p align="center">
Built with ❤️ using Python, Streamlit and NLP
</p>

