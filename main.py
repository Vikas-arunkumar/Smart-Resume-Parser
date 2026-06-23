import streamlit as st
import json
import os
import time
from datetime import date
from resume_parser import parse_resume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RESUMES_DIR = os.path.join(DATA_DIR, "resumes")
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")

DEFAULT_JOBS = [
    {
        "id": "J001", "title": "Python Backend Developer",
        "department": "Engineering", "location": "Chennai / Remote",
        "type": "Full-time",
        "description": "We are looking for a skilled Python developer to build and maintain scalable backend systems. You will design RESTful APIs, optimise database queries, write clean tested code, and collaborate closely with the product team.",
        "skills": ["Python", "Flask", "REST API", "SQL", "Git"],
        "posted": "2025-03-01", "status": "open", "applicants": 0,
    },
    {
        "id": "J002", "title": "Data Science Intern",
        "department": "Analytics", "location": "Chennai",
        "type": "Internship",
        "description": "Join our data team to build ML models, analyse datasets, and create visualisations that drive business decisions. Ideal for final-year students with solid Python and machine learning fundamentals.",
        "skills": ["Python", "Machine Learning", "Pandas", "Scikit-learn", "Matplotlib"],
        "posted": "2025-03-05", "status": "open", "applicants": 0,
    },
    {
        "id": "J003", "title": "Frontend Developer",
        "department": "Product", "location": "Remote",
        "type": "Full-time",
        "description": "Build beautiful, responsive interfaces for our recruitment platform. You will work closely with designers to bring Figma mocks to life using React, write accessible HTML/CSS, and keep performance sharp.",
        "skills": ["React", "JavaScript", "CSS", "Tailwind", "Figma"],
        "posted": "2025-03-08", "status": "open", "applicants": 0,
    },
]

DEFAULT_APPLICATIONS = []

# ── Page config (MUST be first) ───────────────────────────────────────────────
st.set_page_config(
    page_title="TalentScan – Intelligent Recruitment",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: #060912;
    color: #E2E8F8;
}
.stApp { background: #060912; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem !important; max-width: 1300px !important; margin: 0 auto !important; }


::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: #1E2D4A; border-radius: 4px; }

.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 9px !important;
    transition: all 0.22s ease !important;
    border: none !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(56,189,248,0.18) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #0F1524 !important;
    border: 1px solid #1E2D4A !important;
    border-radius: 9px !important;
    color: #E2E8F8 !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.12) !important;
}

[data-testid="stFileUploader"] > div {
    background: #0F1524 !important;
    border: 2px dashed #1E2D4A !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] > div:hover {
    border-color: #38BDF8 !important;
}

[data-testid="stSidebar"] {
    background: #080C18 !important;
    border-right: 1px solid #1A2238 !important;
}
[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    background: transparent !important;
    border: 1px solid transparent !important;
    color: #64748B !important;
    text-align: left !important;
    padding: 10px 14px !important;
    margin-bottom: 2px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(56,189,248,0.06) !important;
    border-color: rgba(56,189,248,0.2) !important;
    color: #38BDF8 !important;
    transform: none !important;
    box-shadow: none !important;
}

.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px !important;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}

.anim-1 { animation: fadeUp 0.6s ease 0.05s both; }
.anim-2 { animation: fadeUp 0.6s ease 0.15s both; }
.anim-3 { animation: fadeUp 0.6s ease 0.25s both; }
.anim-4 { animation: fadeUp 0.6s ease 0.35s both; }

.card {
    background: linear-gradient(135deg,rgba(255,255,255,0.035),rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 18px;
    transition: all 0.3s ease;
}
.card:hover {
    border-color: rgba(56,189,248,0.28);
    box-shadow: 0 16px 40px rgba(56,189,248,0.07);
    transform: translateY(-3px);
}
.card-flat {
    background: #0C1220;
    border: 1px solid #1A2238;
    border-radius: 14px;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.badge-pending     { background:rgba(251,191,36,0.12);  color:#FBBF24; border:1px solid rgba(251,191,36,0.25); }
.badge-shortlisted { background:rgba(52,211,153,0.12);  color:#34D399; border:1px solid rgba(52,211,153,0.25); }
.badge-rejected    { background:rgba(248,113,113,0.12); color:#F87171; border:1px solid rgba(248,113,113,0.25); }
.badge-open        { background:rgba(56,189,248,0.12);  color:#38BDF8; border:1px solid rgba(56,189,248,0.25); }
.badge-closed      { background:rgba(100,116,139,0.12); color:#64748B; border:1px solid rgba(100,116,139,0.25); }

.pill {
    display: inline-block;
    padding: 4px 13px;
    border-radius: 20px;
    font-size: 12px;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
}
.pill-blue   { background:rgba(56,189,248,0.1);  color:#38BDF8; border:1px solid rgba(56,189,248,0.2); }
.pill-indigo { background:rgba(129,140,248,0.1); color:#818CF8; border:1px solid rgba(129,140,248,0.2); }
.pill-green  { background:rgba(52,211,153,0.1);  color:#34D399; border:1px solid rgba(52,211,153,0.2); }
.pill-amber  { background:rgba(251,191,36,0.1);  color:#FBBF24; border:1px solid rgba(251,191,36,0.2); }

.grad {
    background: linear-gradient(135deg,#E2E8F8 20%,#38BDF8 65%,#818CF8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.grad2 {
    background: linear-gradient(90deg,#38BDF8,#818CF8,#38BDF8);
    background-size: 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 4s linear infinite;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    letter-spacing: -0.8px;
    color: #E2E8F8;
}
.divider {
    height: 1px;
    background: linear-gradient(90deg,transparent,#1E2D4A,transparent);
    margin: 18px 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
def init_state():
    defaults = {
        "page": "home",
        "admin_logged_in": False,
        "admin_tab": "overview",
        "apply_job": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    if "applications" not in st.session_state:
        st.session_state.applications = load_json_data(APPLICATIONS_FILE, DEFAULT_APPLICATIONS)

    if "jobs" not in st.session_state:
        st.session_state.jobs = sync_job_applicant_counts(
            load_json_data(JOBS_FILE, DEFAULT_JOBS),
            st.session_state.applications,
        )
        save_json_data(JOBS_FILE, st.session_state.jobs)


def load_json_data(path, fallback):
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(path):
        save_json_data(path, fallback)
        return json.loads(json.dumps(fallback))

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (OSError, json.JSONDecodeError):
        pass

    save_json_data(path, fallback)
    return json.loads(json.dumps(fallback))


def save_json_data(path, payload):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def save_uploaded_resume(uploaded_file, application_id):
    os.makedirs(RESUMES_DIR, exist_ok=True)
    original_name = uploaded_file.name or f"{application_id}.pdf"
    _, ext = os.path.splitext(original_name)
    ext = ext.lower() if ext else ".pdf"
    safe_name = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in application_id)
    stored_name = f"{safe_name}{ext}"
    stored_path = os.path.join(RESUMES_DIR, stored_name)

    uploaded_file.seek(0)
    with open(stored_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    uploaded_file.seek(0)

    return {
        "resume_filename": original_name,
        "resume_path": stored_path,
        "resume_type": uploaded_file.type or "application/octet-stream",
    }


def sync_job_applicant_counts(jobs, applications):
    app_counts = {}
    for app in applications:
        job_id = app.get("job_id")
        if job_id:
            app_counts[job_id] = app_counts.get(job_id, 0) + 1

    synced_jobs = []
    for job in jobs:
        synced_job = dict(job)
        synced_job["applicants"] = app_counts.get(job.get("id"), 0)
        synced_jobs.append(synced_job)
    return synced_jobs

init_state()


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def nav(page):
    st.session_state.page = page
    st.rerun()

def skill_pills(skills, color="#38BDF8", bg="rgba(56,189,248,0.08)", border="rgba(56,189,248,0.18)"):
    return "".join([
        f'<span style="display:inline-block;padding:3px 11px;border-radius:6px;'
        f'font-size:12px;font-family:Syne,sans-serif;font-weight:600;'
        f'color:{color};background:{bg};border:1px solid {border};margin:2px;">{s}</span>'
        for s in skills
    ])

def score_ring(score):
    color = "#34D399" if score >= 80 else "#FBBF24" if score >= 60 else "#F87171"
    deg   = score * 3.6
    return f"""
    <div style="width:68px;height:68px;border-radius:50%;flex-shrink:0;
        background:conic-gradient({color} {deg}deg,#1A2238 0deg);
        display:flex;align-items:center;justify-content:center;">
        <div style="width:52px;height:52px;border-radius:50%;background:#0C1220;
            display:flex;align-items:center;justify-content:center;
            font-family:'Syne',sans-serif;font-weight:800;font-size:14px;color:{color};">
            {score}%
        </div>
    </div>"""

def navbar():
    st.markdown("""
    <div style="position:sticky;top:0;z-index:200;
        background:rgba(6,9,18,0.92);backdrop-filter:blur(18px);
        border-bottom:1px solid rgba(255,255,255,0.06);
        padding:14px 0;display:flex;align-items:center;justify-content:space-between;">
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="width:32px;height:32px;border-radius:9px;
                background:linear-gradient(135deg,#38BDF8,#818CF8);
                display:flex;align-items:center;justify-content:center;font-size:15px;">🔍</div>
            <span style="font-family:'Syne',sans-serif;font-weight:800;
                font-size:17px;color:#E2E8F8;letter-spacing:-0.2px;">TalentScan</span>
        </div>
        <div style="display:flex;align-items:center;gap:4px;">
            <span style="color:#64748B;font-size:13px;padding:6px 14px;">Home</span>
            <span style="color:#64748B;font-size:13px;padding:6px 14px;">Jobs</span>
            <span style="color:#64748B;font-size:13px;padding:6px 14px;">Track Status</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — HOME
# ══════════════════════════════════════════════════════════════════════════════
def page_home():
    navbar()

    st.markdown("""
    <div style="min-height:86vh;padding:72px 0 48px;position:relative;overflow:hidden;">
        <div style="position:absolute;inset:0;
            background-image:linear-gradient(rgba(56,189,248,0.032) 1px,transparent 1px),
            linear-gradient(90deg,rgba(56,189,248,0.032) 1px,transparent 1px);
            background-size:54px 54px;pointer-events:none;"></div>
        <div style="position:absolute;top:-120px;right:-100px;width:620px;height:620px;border-radius:50%;
            background:radial-gradient(circle,rgba(129,140,248,0.1) 0%,transparent 65%);pointer-events:none;"></div>
        <div style="position:absolute;bottom:-80px;left:-80px;width:500px;height:500px;border-radius:50%;
            background:radial-gradient(circle,rgba(56,189,248,0.07) 0%,transparent 65%);pointer-events:none;"></div>
        <div style="position:relative;max-width:880px;">
            <div class="anim-1" style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:28px;">
                <span class="pill pill-blue">NLIP Mini Project</span>
                <span class="pill pill-indigo">IT23602</span>
                <span class="pill pill-green">MIT Anna University</span>
            </div>
            <h1 class="anim-2" style="font-family:'Syne',sans-serif;
                font-size:clamp(44px,6vw,80px);font-weight:800;
                line-height:1.04;letter-spacing:-2.5px;margin-bottom:26px;">
                <span class="grad">Intelligent</span><br>
                <span style="color:#E2E8F8;">Resume Parser</span><br>
                <span style="color:#E2E8F8;">&amp; </span>
                <span class="grad2">Skill Extractor</span>
            </h1>
            <p class="anim-3" style="font-size:17px;color:#94A3B8;max-width:520px;
                line-height:1.85;font-weight:300;margin-bottom:0;">
                An NLP-powered recruitment platform that parses resumes, extracts
                structured data, and matches candidates to job requirements — with
                <strong style="color:#E2E8F8;font-weight:500;">human oversight</strong>
                at every decision.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, _ = st.columns([1.3, 1.3, 6])
    with c1:
        if st.button("Browse Jobs →", use_container_width=True, type="primary"):
            nav("jobs")
    with c2:
        if st.button("Admin Login", use_container_width=True):
            nav("admin_login")

    st.markdown("""
    <div style="background:#080D1A;border-top:1px solid #121C30;
        border-bottom:1px solid #121C30;padding:28px 0;
        display:flex;gap:48px;flex-wrap:wrap;align-items:center;margin-top:16px;">
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;color:#38BDF8;">7+</div>
            <div style="font-size:13px;color:#475569;margin-top:2px;">NLP Techniques</div>
        </div>
        <div style="width:1px;height:40px;background:#1A2238;"></div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;color:#818CF8;">3</div>
            <div style="font-size:13px;color:#475569;margin-top:2px;">Open Positions</div>
        </div>
        <div style="width:1px;height:40px;background:#1A2238;"></div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;color:#34D399;">100%</div>
            <div style="font-size:13px;color:#475569;margin-top:2px;">Human Verified Decisions</div>
        </div>
        <div style="width:1px;height:40px;background:#1A2238;"></div>
        <div>
            <div style="font-family:'Syne',sans-serif;font-size:34px;font-weight:800;color:#FBBF24;">0</div>
            <div style="font-size:13px;color:#475569;margin-top:2px;">Score Shown to Candidate</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # How it works
    st.markdown("""
    <div style="padding:60px 0 40px;">
        <div style="text-align:center;margin-bottom:48px;">
            <div class="section-label" style="color:#38BDF8;margin-bottom:12px;">WORKFLOW</div>
            <h2 class="section-title" style="font-size:clamp(28px,4vw,44px);">How it works</h2>
            <p style="color:#64748B;font-size:15px;margin-top:12px;max-width:420px;
                margin-left:auto;margin-right:auto;line-height:1.75;">
                Two roles. Five steps. NLP does the analysis — humans make the call.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(5)
    steps = [
        ("#38BDF8","01","📤","Post & Browse","Recruiter posts jobs. Candidates browse and apply with just their email."),
        ("#818CF8","02","🧠","NLP Parsing","Resume text is tokenized, cleaned, lemmatized, NER and regex applied."),
        ("#34D399","03","⚖️","Skill Matching","Extracted skills matched against job requirements. Score computed silently."),
        ("#FBBF24","04","🔐","Admin Review","Score visible only to recruiter. They review and make the final decision."),
        ("#F472B6","05","📬","Status Update","Candidate checks status by email — sees only Pending/Shortlisted/Rejected."),
    ]
    for col, (color, num, icon, title, desc) in zip(cols, steps):
        with col:
            st.markdown(f"""
            <div class="card" style="padding:26px 16px;text-align:center;min-height:240px;">
                <div style="font-family:'Syne',sans-serif;font-size:10px;font-weight:700;
                    letter-spacing:3px;color:{color};opacity:0.35;margin-bottom:12px;">{num}</div>
                <div style="width:48px;height:48px;border-radius:12px;margin:0 auto 14px;
                    background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                    display:flex;align-items:center;justify-content:center;font-size:22px;">{icon}</div>
                <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
                    color:#E2E8F8;margin-bottom:9px;">{title}</div>
                <div style="font-size:12px;color:#64748B;line-height:1.7;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # NLP Techniques
    st.markdown("""
    <div style="padding:24px 0 60px;">
        <div style="background:linear-gradient(135deg,rgba(129,140,248,0.05),rgba(56,189,248,0.03));
            border:1px solid rgba(255,255,255,0.07);border-radius:24px;padding:48px 44px;">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:44px;align-items:start;">
                <div>
                    <div class="section-label" style="color:#818CF8;margin-bottom:16px;">CORE NLIP CONCEPTS</div>
                    <h2 class="section-title" style="font-size:clamp(24px,3vw,36px);margin-bottom:16px;">
                        Built on real<br/>NLP fundamentals
                    </h2>
                    <p style="color:#64748B;font-size:14px;line-height:1.85;max-width:360px;">
                        Every extraction step maps directly to concepts from IT23602.
                        No black-box models — pure NLP logic you can trace and explain.
                    </p>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
    """, unsafe_allow_html=True)

    for icon, title, desc in [
        ("🔤","Tokenization","Split text into word tokens"),
        ("🚫","Stopword Removal","Filter 'the', 'and', 'is'"),
        ("📖","Lemmatization","Reduce to base root form"),
        ("🏷️","NER","Extract names, orgs, degrees"),
        ("🔡","POS Tagging","Label nouns, verbs, adjectives"),
        ("🔍","Regex","Match emails, phones, dates"),
        ("🧩","Phrase Chunking","Group tokens into phrases"),
        ("⚖️","Skill Matching","Compare against skills dict"),
    ]:
        st.markdown(f"""
        <div class="card-flat" style="padding:13px 15px;">
            <div style="display:flex;align-items:flex-start;gap:10px;">
                <div style="width:30px;height:30px;border-radius:7px;flex-shrink:0;
                    background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.06);
                    display:flex;align-items:center;justify-content:center;font-size:13px;">{icon}</div>
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:12px;font-weight:700;
                        color:#CBD5E1;margin-bottom:2px;">{title}</div>
                    <div style="font-size:11px;color:#475569;line-height:1.4;">{desc}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div></div></div>", unsafe_allow_html=True)

    # Team
    st.markdown("""
    <div style="padding:0 0 60px;">
        <div style="text-align:center;margin-bottom:36px;">
            <div class="section-label" style="color:#FBBF24;margin-bottom:12px;">THE TEAM</div>
            <h2 class="section-title" style="font-size:clamp(26px,4vw,40px);">Built by</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, tc, _ = st.columns([1.5, 3, 1.5])
    with tc:
        for initials, color, name, reg, role in [
            ("AV","#38BDF8","A. Vikas","2023506122","Backend & NLP Pipeline"),
            ("MA","#818CF8","M. Aswin Kumar","2023506310","Frontend & Integration"),
        ]:
            st.markdown(f"""
            <div class="card" style="padding:20px 24px;margin-bottom:10px;
                display:flex;align-items:center;gap:14px;">
                <div style="width:46px;height:46px;border-radius:11px;flex-shrink:0;
                    background:{color}14;border:1px solid {color}32;
                    display:flex;align-items:center;justify-content:center;
                    font-family:'Syne',sans-serif;font-weight:800;font-size:15px;color:{color};">
                    {initials}</div>
                <div style="flex:1;">
                    <div style="font-family:'Syne',sans-serif;font-weight:700;
                        font-size:15px;color:#E2E8F8;">{name}</div>
                    <div style="font-size:11px;color:#475569;margin-top:2px;">Reg: {reg}</div>
                </div>
                <span style="font-size:11px;color:{color};background:{color}10;
                    border:1px solid {color}26;padding:4px 11px;border-radius:14px;
                    font-family:'Syne',sans-serif;font-weight:700;">{role}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align:center;margin-top:8px;font-size:12px;color:#1A2E48;">
            Dept. of Information Technology &nbsp;·&nbsp; MIT Anna University &nbsp;·&nbsp; Chennai 600044
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style="border-top:1px solid #0D1626;padding:20px 0;
        display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
        <div style="display:flex;align-items:center;gap:7px;">
            <div style="width:22px;height:22px;border-radius:5px;
                background:linear-gradient(135deg,#38BDF8,#818CF8);
                display:flex;align-items:center;justify-content:center;font-size:10px;">🔍</div>
            <span style="font-family:'Syne',sans-serif;font-weight:700;color:#1A2E48;font-size:13px;">TalentScan</span>
        </div>
        <span style="font-size:11px;color:#172030;">IT23602 · Natural Language &amp; Image Processing · MIT Anna University</span>
        <span style="font-size:11px;color:#172030;">A. Vikas &nbsp;·&nbsp; M. Aswin Kumar</span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — JOB LISTINGS
# ══════════════════════════════════════════════════════════════════════════════
def page_jobs():
    navbar()

    st.markdown("""
    <div style="padding:40px 0 24px;">
        <h1 style="font-family:'Syne',sans-serif;font-size:36px;font-weight:800;
            color:#E2E8F8;letter-spacing:-1px;margin-bottom:6px;">Open Positions</h1>
        <p style="color:#64748B;font-size:15px;margin:0;">
            Apply with your resume — no account required.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cb, _ = st.columns([1, 9])
    with cb:
        if st.button("← Home"):
            nav("home")

    st.markdown("<div style='padding:8px 0 0;'>", unsafe_allow_html=True)
    with st.expander("📋 Track your application status"):
        t1, t2 = st.columns([3, 1])
        with t1:
            track_email = st.text_input("Your email", placeholder="you@example.com",
                                        label_visibility="collapsed", key="track_email_input")
        with t2:
            track_btn = st.button("Check", use_container_width=True, key="track_btn")
        if track_btn and track_email:
            matches = [a for a in st.session_state.applications
                       if a["email"].lower().strip() == track_email.lower().strip()]
            if matches:
                for app in matches:
                    st.markdown(f"""
                    <div class="card-flat" style="padding:14px 18px;margin-top:10px;
                        display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                        <div>
                            <div style="font-family:'Syne',sans-serif;font-weight:700;
                                color:#E2E8F8;font-size:14px;">{app['job_title']}</div>
                            <div style="font-size:12px;color:#475569;margin-top:2px;">Applied: {app['applied']}</div>
                        </div>
                        <span class="badge badge-{app['status']}">{app['status']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No applications found for this email.")
        elif track_btn:
            st.warning("Please enter your email address.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='padding:20px 0 60px;'>", unsafe_allow_html=True)
    open_jobs = [j for j in st.session_state.jobs if j["status"] == "open"]

    if not open_jobs:
        st.markdown("""
        <div style="text-align:center;padding:80px;color:#475569;">
            <div style="font-size:40px;margin-bottom:14px;">🗂️</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:700;color:#334155;">
                No open positions right now
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for job in open_jobs:
            st.markdown(f"""
            <div class="card" style="padding:26px 30px;margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;
                    align-items:flex-start;flex-wrap:wrap;gap:14px;">
                    <div style="flex:1;min-width:260px;">
                        <div style="display:flex;align-items:center;gap:9px;margin-bottom:7px;flex-wrap:wrap;">
                            <span style="font-family:'Syne',sans-serif;font-size:19px;
                                font-weight:800;color:#E2E8F8;">{job['title']}</span>
                            <span class="badge badge-open">{job['type']}</span>
                        </div>
                        <div style="font-size:12px;color:#475569;margin-bottom:14px;">
                            🏢 {job['department']} &nbsp;·&nbsp;
                            📍 {job['location']} &nbsp;·&nbsp;
                            📅 Posted {job['posted']}
                        </div>
                        <p style="font-size:14px;color:#94A3B8;line-height:1.75;
                            margin-bottom:14px;max-width:680px;">
                            {job['description'][:180]}...
                        </p>
                        <div style="display:flex;flex-wrap:wrap;gap:5px;">
                            {skill_pills(job['skills'])}
                        </div>
                    </div>
                    <div style="text-align:right;min-width:80px;">
                        <div style="font-family:'Syne',sans-serif;font-size:22px;
                            font-weight:800;color:#38BDF8;">{job['applicants']}</div>
                        <div style="font-size:11px;color:#475569;">applicants</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            _, ab = st.columns([6, 1])
            with ab:
                if st.button("Apply →", key=f"apply_{job['id']}", use_container_width=True):
                    st.session_state.apply_job = job
                    nav("apply")

    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — APPLY
# ══════════════════════════════════════════════════════════════════════════════
def page_apply():
    navbar()
    job = st.session_state.apply_job
    if not job:
        nav("jobs")
        return

    st.markdown(f"""
    <div style="padding:32px 0 20px;">
        <h1 style="font-family:'Syne',sans-serif;font-size:30px;font-weight:800;
            color:#E2E8F8;letter-spacing:-0.8px;margin-bottom:6px;">
            Apply — {job['title']}
        </h1>
        <p style="color:#64748B;font-size:14px;margin:0;">
            Fill in your details and upload your resume.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("← Back to Jobs", key="apply_back"):
        nav("jobs")

    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)

    # ── Form fields — all at top level (no nesting inside columns) ──
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#38BDF8;letter-spacing:1.5px;text-transform:uppercase;
        margin-bottom:12px;">📝 Your Details</div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        name  = st.text_input("Full Name *",  placeholder="e.g. Vikas A",    key="app_name")
        phone = st.text_input("Phone Number", placeholder="+91 98765 43210", key="app_phone")
    with col_b:
        email = st.text_input("Email Address *", placeholder="you@example.com", key="app_email")

    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
        color:#38BDF8;letter-spacing:1.5px;text-transform:uppercase;
        margin:20px 0 10px;">📄 Resume Upload</div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload your resume (PDF or DOCX)",
        type=["pdf", "docx"],
        key="app_file"
    )

    if uploaded:
        st.success(f"✓  {uploaded.name}  ready to submit")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    # ── Submit button at top level — NOT inside any column ──
    submit = st.button(
        "🚀  Submit Application",
        type="primary",
        key="submit_app"
    )

    if submit:
        # Validation
        errors = []
        if not name.strip():     errors.append("Full name is required.")
        if not email.strip():    errors.append("Email address is required.")
        if uploaded is None:     errors.append("Please upload your resume.")
        if errors:
            for e in errors:
                st.error(e)
            st.stop()

        # Duplicate check
        already = any(
            a["email"].lower().strip() == email.lower().strip()
            and a["job_id"] == job["id"]
            for a in st.session_state.applications
        )
        if already:
            st.warning("You have already applied for this position with this email.")
            st.stop()

        # NLP Parsing — always continues even if parser errors
        parsed = {
            "name"       : name.strip(),
            "email"      : email.strip(),
            "phone"      : phone.strip() or "Not provided",
            "skills"     : [],
            "education"  : "Not extracted",
            "experience" : "Not extracted",
            "match_score": 0,
        }
        parse_error = None
        with st.spinner("🧠 Analysing resume with NLP engine..."):
            try:
                uploaded.seek(0)
                result = parse_resume(uploaded, job)
                # Keep typed name/email as the source of truth for tracking.
                parsed["skills"]      = result.get("skills", [])
                parsed["education"]   = result.get("education", "Not extracted")
                parsed["experience"]  = result.get("experience", "Not extracted")
                parsed["match_score"] = result.get("match_score", 0)
                if not phone.strip() and result.get("phone"):
                    parsed["phone"] = result["phone"]
            except Exception as e:
                parse_error = str(e)

        # Save to session state
        application_id = f"A{len(st.session_state.applications)+1:03d}"
        resume_meta = save_uploaded_resume(uploaded, application_id)
        new_app = {
            "id"         : application_id,
            "job_id"     : job["id"],
            "job_title"  : job["title"],
            "name"       : parsed["name"],
            "email"      : parsed["email"],
            "phone"      : parsed["phone"],
            "skills"     : parsed["skills"],
            "education"  : parsed["education"],
            "experience" : parsed["experience"],
            "match_score": parsed["match_score"],
            "status"     : "pending",
            "applied"    : str(date.today()),
            **resume_meta,
        }
        st.session_state.applications.append(new_app)
        save_json_data(APPLICATIONS_FILE, st.session_state.applications)

        for i, j in enumerate(st.session_state.jobs):
            if j["id"] == job["id"]:
                st.session_state.jobs[i]["applicants"] += 1
                break
        save_json_data(JOBS_FILE, st.session_state.jobs)

        if parse_error:
            st.warning(f"⚠️ Resume saved — parser note: {parse_error}")

        st.markdown("""
        <div style="background:linear-gradient(135deg,rgba(52,211,153,0.08),
            rgba(56,189,248,0.08));border:1px solid rgba(52,211,153,0.25);
            border-radius:14px;padding:28px;text-align:center;margin-top:16px;">
            <div style="font-size:40px;margin-bottom:10px;">✅</div>
            <div style="font-family:'Syne',sans-serif;font-size:18px;font-weight:800;
                color:#34D399;margin-bottom:8px;">Application Submitted!</div>
            <div style="color:#64748B;font-size:13px;line-height:1.8;">
                Your resume has been received and is being reviewed.<br/>
                Use your email on the Jobs page to track your status.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Job info panel ──
    st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card-flat" style="padding:24px;">
        <div style="display:flex;justify-content:space-between;
            align-items:flex-start;flex-wrap:wrap;gap:16px;">
            <div>
                <div class="section-label" style="color:#38BDF8;margin-bottom:10px;">
                    APPLYING FOR
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:18px;
                    font-weight:800;color:#E2E8F8;margin-bottom:5px;">
                    {job['title']}
                </div>
                <div style="font-size:13px;color:#475569;">
                    🏢 {job['department']} &nbsp;·&nbsp;
                    📍 {job['location']} &nbsp;·&nbsp;
                    🕒 {job['type']}
                </div>
            </div>
            <div style="display:flex;flex-wrap:wrap;gap:6px;max-width:480px;">
                {skill_pills(job['skills'])}
            </div>
        </div>
        <div style="margin-top:16px;font-size:13px;color:#94A3B8;line-height:1.8;">
            {job['description']}
        </div>
    </div>
    <div style="background:rgba(251,191,36,0.06);border:1px solid rgba(251,191,36,0.14);
        border-radius:10px;padding:14px 16px;margin-top:10px;">
        <div style="color:#FBBF24;font-family:'Syne',sans-serif;
            font-weight:700;font-size:12px;margin-bottom:5px;">ℹ️ What happens next?</div>
        <div style="color:#64748B;font-size:12px;line-height:1.75;">
            Your resume is automatically parsed by our NLP engine. The recruiter
            reviews all applications and makes decisions manually.
            Expect a status update within 3–5 business days.
        </div>
    </div>
    """, unsafe_allow_html=True)


# PAGE 4 — ADMIN LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def page_admin_login():
    navbar()
    _, mid, _ = st.columns([1.5, 2, 1.5])
    with mid:
        st.markdown("""
        <div style="padding:68px 0 28px;text-align:center;">
            <div style="width:56px;height:56px;border-radius:14px;margin:0 auto 18px;
                background:linear-gradient(135deg,rgba(56,189,248,0.14),rgba(129,140,248,0.1));
                border:1px solid rgba(56,189,248,0.2);
                display:flex;align-items:center;justify-content:center;font-size:24px;">🔐</div>
            <h2 style="font-family:'Syne',sans-serif;font-size:26px;font-weight:800;
                color:#E2E8F8;margin-bottom:5px;">Recruiter Login</h2>
            <p style="color:#64748B;font-size:14px;">Admin access only</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#0C1220;border:1px solid #1A2238;border-radius:16px;padding:30px;">
        """, unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="admin",       key="login_user")
        password = st.text_input("Password", type="password",
                                 placeholder="••••••••",                 key="login_pass")
        st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        if st.button("Login to Dashboard →", use_container_width=True,
                     type="primary", key="login_btn"):
            if username == "admin" and password == "admin123":
                st.session_state.admin_logged_in = True
                st.session_state.admin_tab = "overview"
                nav("admin_dashboard")
            else:
                st.error("Invalid credentials.")

        st.markdown("""
        <div style="text-align:center;margin-top:16px;">
            <span style="font-size:12px;color:#1E3A5F;">
                Demo: &nbsp;<strong style="color:#38BDF8;">admin</strong>
                &nbsp;/&nbsp;
                <strong style="color:#38BDF8;">admin123</strong>
            </span>
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("← Back to Home", use_container_width=True, key="login_back"):
            nav("home")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_admin_dashboard():
    if not st.session_state.admin_logged_in:
        nav("admin_login")
        return

    with st.sidebar:
        st.markdown("""
        <div style="padding:18px 2px 10px;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:3px;">
                <div style="width:26px;height:26px;border-radius:6px;
                    background:linear-gradient(135deg,#38BDF8,#818CF8);
                    display:flex;align-items:center;justify-content:center;font-size:12px;">🔍</div>
                <span style="font-family:'Syne',sans-serif;font-weight:800;
                    font-size:14px;color:#E2E8F8;">TalentScan</span>
            </div>
            <div style="font-size:10px;color:#334155;padding-left:34px;">Admin Panel</div>
        </div>
        <div style="height:1px;background:#121C30;margin:8px 0 10px;"></div>
        """, unsafe_allow_html=True)

        for key, icon, label in [
            ("overview",     "📊","Overview"),
            ("applications", "📋","Applications"),
            ("jobs",         "💼","Job Posts"),
            ("post_job",     "➕","Post New Job"),
        ]:
            if st.button(f"{icon}  {label}", key=f"sb_{key}", use_container_width=True):
                st.session_state.admin_tab = key
                st.rerun()

        st.markdown("<div style='height:1px;background:#121C30;margin:10px 0;'></div>",
                    unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True, key="sb_logout"):
            st.session_state.admin_logged_in = False
            nav("home")

    tab = st.session_state.admin_tab
    tab_labels = {
        "overview":"Overview","applications":"Applications",
        "jobs":"Job Posts","post_job":"Post New Job",
    }

    st.markdown(f"""
    <div style="background:#080D1A;border-bottom:1px solid #121C30;
        padding:20px 0;display:flex;align-items:center;justify-content:space-between;">
        <h1 style="font-family:'Syne',sans-serif;font-size:21px;font-weight:800;
            color:#E2E8F8;margin:0;">{tab_labels.get(tab,'Dashboard')}</h1>
        <div style="background:#0C1220;border:1px solid #1A2238;border-radius:7px;
            padding:6px 13px;font-size:12px;color:#475569;">👤 Admin Recruiter</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Overview ──
    if tab == "overview":
        apps = st.session_state.applications
        jobs = st.session_state.jobs
        total     = len(apps)
        pending   = len([a for a in apps if a["status"]=="pending"])
        shortlist = len([a for a in apps if a["status"]=="shortlisted"])
        open_j    = len([j for j in jobs if j["status"]=="open"])

        st.markdown("<div style='padding:26px 0;'>", unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        for col,val,label,clr in [
            (m1,total,    "Total Applications","#38BDF8"),
            (m2,pending,  "Pending Review",    "#FBBF24"),
            (m3,shortlist,"Shortlisted",       "#34D399"),
            (m4,open_j,   "Open Positions",    "#818CF8"),
        ]:
            with col:
                st.markdown(f"""
                <div class="card-flat" style="padding:20px;text-align:center;">
                    <div style="font-family:'Syne',sans-serif;font-size:34px;
                        font-weight:800;color:{clr};line-height:1;">{val}</div>
                    <div style="font-size:12px;color:#475569;margin-top:5px;">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""
        <div style="height:24px;"></div>
        <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;
            color:#E2E8F8;margin-bottom:14px;">🕐 Recent Applications</div>
        """, unsafe_allow_html=True)

        for app in list(reversed(apps))[:5]:
            st.markdown(f"""
            <div class="card-flat" style="padding:16px 20px;margin-bottom:9px;
                display:flex;align-items:center;justify-content:space-between;
                flex-wrap:wrap;gap:10px;">
                <div style="flex:1;min-width:200px;">
                    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
                        <span style="font-family:'Syne',sans-serif;font-weight:700;
                            color:#E2E8F8;font-size:14px;">{app['name']}</span>
                        <span class="badge badge-{app['status']}">{app['status']}</span>
                    </div>
                    <div style="font-size:12px;color:#475569;">
                        {app['job_title']} &nbsp;·&nbsp; {app['applied']}
                    </div>
                    <div style="margin-top:7px;display:flex;flex-wrap:wrap;gap:4px;">
                        {skill_pills(app['skills'][:4]) if app['skills'] else
                         '<span style="color:#F87171;font-size:11px;">⚠ No skills extracted — check resume format</span>'}
                    </div>
                </div>
                {score_ring(app['match_score'])}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Applications ──
    elif tab == "applications":
        st.markdown("<div style='padding:26px 0;'>", unsafe_allow_html=True)
        fc, _ = st.columns([2,5])
        with fc:
            sf = st.selectbox("Filter","All,pending,shortlisted,rejected".split(","),
                              label_visibility="collapsed", key="app_filter")
        apps = st.session_state.applications
        if sf != "All":
            apps = [a for a in apps if a["status"]==sf]

        if not apps:
            st.markdown("""
            <div style="text-align:center;padding:60px;color:#475569;">
                <div style="font-size:36px;margin-bottom:10px;">📭</div>
                <div style="font-family:'Syne',sans-serif;font-size:15px;
                    font-weight:700;color:#334155;">No applications found</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for app in apps:
                orig_idx = st.session_state.applications.index(app)
                st.markdown(f"""
                <div class="card-flat" style="padding:20px 24px;margin-bottom:10px;">
                    <div style="display:flex;justify-content:space-between;
                        align-items:flex-start;flex-wrap:wrap;gap:14px;">
                        <div style="flex:1;min-width:220px;">
                            <div style="display:flex;align-items:center;gap:8px;
                                margin-bottom:5px;flex-wrap:wrap;">
                                <span style="font-family:'Syne',sans-serif;font-size:16px;
                                    font-weight:800;color:#E2E8F8;">{app['name']}</span>
                                <span class="badge badge-{app['status']}">{app['status']}</span>
                            </div>
                            <div style="font-size:12px;color:#475569;margin-bottom:8px;">
                                📧 {app['email']} &nbsp;·&nbsp;
                                📞 {app['phone']} &nbsp;·&nbsp;
                                💼 {app['job_title']}
                            </div>
                            <div style="font-size:12px;color:#94A3B8;margin-bottom:3px;">
                                🎓 {app['education']}
                            </div>
                            <div style="font-size:12px;color:#94A3B8;margin-bottom:10px;">
                                💼 {app['experience']}
                            </div>
                            <div style="display:flex;flex-wrap:wrap;gap:4px;">
                                {skill_pills(app['skills']) if app['skills'] else
                                 '<span style="color:#F87171;font-size:11px;">⚠ No skills extracted — check resume format</span>'}
                            </div>
                        </div>
                        <div style="text-align:center;">
                            {score_ring(app['match_score'])}
                            <div style="font-size:10px;color:#475569;margin-top:5px;">NLP Match</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                resume_path = app.get("resume_path")
                if resume_path and os.path.exists(resume_path):
                    with open(resume_path, "rb") as resume_file:
                        st.download_button(
                            "📄 Download Resume",
                            data=resume_file.read(),
                            file_name=app.get("resume_filename", os.path.basename(resume_path)),
                            mime=app.get("resume_type", "application/octet-stream"),
                            key=f"resume_{app['id']}",
                        )
                    st.caption(f"Attached resume: {app.get('resume_filename', os.path.basename(resume_path))}")
                else:
                    st.caption("Resume file not available for this application.")

                _, b1, b2, b3 = st.columns([4,1,1,1])
                with b1:
                    if st.button("✅ Shortlist", key=f"sl_{app['id']}", use_container_width=True):
                        st.session_state.applications[orig_idx]["status"] = "shortlisted"
                        save_json_data(APPLICATIONS_FILE, st.session_state.applications)
                        st.rerun()
                with b2:
                    if st.button("❌ Reject",    key=f"rj_{app['id']}", use_container_width=True):
                        st.session_state.applications[orig_idx]["status"] = "rejected"
                        save_json_data(APPLICATIONS_FILE, st.session_state.applications)
                        st.rerun()
                with b3:
                    if st.button("⏸ Hold",       key=f"hd_{app['id']}", use_container_width=True):
                        st.session_state.applications[orig_idx]["status"] = "pending"
                        save_json_data(APPLICATIONS_FILE, st.session_state.applications)
                        st.rerun()
                st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Job Posts ──
    elif tab == "jobs":
        st.markdown("<div style='padding:26px 0;'>", unsafe_allow_html=True)
        for i, job in enumerate(st.session_state.jobs):
            app_count = len([a for a in st.session_state.applications if a["job_id"]==job["id"]])
            st.markdown(f"""
            <div class="card-flat" style="padding:20px 24px;margin-bottom:10px;">
                <div style="display:flex;justify-content:space-between;
                    align-items:flex-start;flex-wrap:wrap;gap:14px;">
                    <div style="flex:1;min-width:220px;">
                        <div style="display:flex;align-items:center;gap:8px;
                            margin-bottom:6px;flex-wrap:wrap;">
                            <span style="font-family:'Syne',sans-serif;font-size:17px;
                                font-weight:800;color:#E2E8F8;">{job['title']}</span>
                            <span class="badge badge-{'open' if job['status']=='open' else 'closed'}">
                                {job['status']}</span>
                            <span style="display:inline-block;padding:4px 12px;border-radius:20px;
                                font-size:11px;font-family:'Syne',sans-serif;font-weight:700;
                                background:rgba(129,140,248,0.1);color:#818CF8;
                                border:1px solid rgba(129,140,248,0.2);">{job['type']}</span>
                        </div>
                        <div style="font-size:12px;color:#475569;margin-bottom:10px;">
                            🏢 {job['department']} &nbsp;·&nbsp;
                            📍 {job['location']} &nbsp;·&nbsp;
                            📅 {job['posted']}
                        </div>
                        <p style="font-size:13px;color:#94A3B8;line-height:1.7;
                            max-width:580px;margin-bottom:10px;">
                            {job['description'][:150]}...
                        </p>
                        <div style="display:flex;flex-wrap:wrap;gap:4px;">
                            {skill_pills(job['skills'])}
                        </div>
                    </div>
                    <div style="text-align:center;min-width:56px;">
                        <div style="font-family:'Syne',sans-serif;font-size:26px;
                            font-weight:800;color:#38BDF8;">{app_count}</div>
                        <div style="font-size:10px;color:#475569;">applicants</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            _, t1, t2 = st.columns([5,1,1])
            with t1:
                lbl = "🔒 Close" if job["status"]=="open" else "🔓 Reopen"
                if st.button(lbl, key=f"tg_{job['id']}", use_container_width=True):
                    st.session_state.jobs[i]["status"] = (
                        "closed" if job["status"]=="open" else "open")
                    save_json_data(JOBS_FILE, st.session_state.jobs)
                    st.rerun()
            with t2:
                if st.button("🗑 Delete", key=f"dl_{job['id']}", use_container_width=True):
                    st.session_state.jobs.pop(i)
                    st.session_state.applications = [
                        app for app in st.session_state.applications
                        if app["job_id"] != job["id"]
                    ]
                    st.session_state.jobs = sync_job_applicant_counts(
                        st.session_state.jobs,
                        st.session_state.applications,
                    )
                    save_json_data(APPLICATIONS_FILE, st.session_state.applications)
                    save_json_data(JOBS_FILE, st.session_state.jobs)
                    st.rerun()
            st.markdown("<div style='height:2px;'></div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Post New Job ──
    elif tab == "post_job":
        fc, tc = st.columns([3,2], gap="large")

        with fc:
            st.markdown("<div style='padding:26px 0 0 0;'>", unsafe_allow_html=True)
            title    = st.text_input("Job Title *",       placeholder="e.g. Python Developer",   key="nj_title")
            dept     = st.text_input("Department",         placeholder="e.g. Engineering",        key="nj_dept")
            location = st.text_input("Location",           placeholder="e.g. Chennai / Remote",   key="nj_loc")
            jtype    = st.selectbox("Employment Type",
                                    ["Full-time","Part-time","Internship","Contract"],            key="nj_type")
            desc     = st.text_area("Job Description *",  height=140,
                                    placeholder="Describe the role and responsibilities...",      key="nj_desc")
            skills_r = st.text_input("Required Skills (comma-separated) *",
                                     placeholder="Python, Flask, SQL, Git",                       key="nj_skills")

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if st.button("📢 Publish Job", use_container_width=True,
                         type="primary", key="publish_btn"):
                if not title.strip() or not desc.strip() or not skills_r.strip():
                    st.error("Please fill in Title, Description, and Required Skills.")
                else:
                    st.session_state.jobs.append({
                        "id"         : f"J{len(st.session_state.jobs)+1:03d}",
                        "title"      : title.strip(),
                        "department" : dept.strip() or "General",
                        "location"   : location.strip() or "TBD",
                        "type"       : jtype,
                        "description": desc.strip(),
                        "skills"     : [s.strip() for s in skills_r.split(",") if s.strip()],
                        "posted"     : str(date.today()),
                        "status"     : "open",
                        "applicants" : 0,
                    })
                    save_json_data(JOBS_FILE, st.session_state.jobs)
                    st.success(f"✅ '{title}' published!")
                    time.sleep(1)
                    st.session_state.admin_tab = "jobs"
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        with tc:
            st.markdown("""
            <div style="padding:26px 0 0 0;">
                <div class="card-flat" style="padding:22px;">
                    <div style="font-family:'Syne',sans-serif;font-size:13px;font-weight:700;
                        color:#38BDF8;margin-bottom:12px;">💡 Tips for better matching</div>
            """, unsafe_allow_html=True)
            for tip, body in [
                ("Be specific",   "List exact skill names — the NLP matches against these"),
                ("Use commas",    "Separate each skill with a comma for best accuracy"),
                ("Mention level", "Include seniority e.g. '2+ years Python'"),
                ("Keep it clear", "Clear descriptions help candidates self-assess fit"),
            ]:
                st.markdown(f"""
                <div style="display:flex;align-items:flex-start;gap:9px;margin-bottom:12px;">
                    <div style="width:5px;height:5px;border-radius:50%;background:#38BDF8;
                        flex-shrink:0;margin-top:5px;"></div>
                    <div>
                        <div style="font-family:'Syne',sans-serif;font-size:12px;
                            font-weight:700;color:#CBD5E1;">{tip}</div>
                        <div style="font-size:11px;color:#475569;line-height:1.5;margin-top:2px;">{body}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div></div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
_page = st.session_state.page

if   _page == "home":            page_home()
elif _page == "jobs":            page_jobs()
elif _page == "apply":           page_apply()
elif _page == "admin_login":     page_admin_login()
elif _page == "admin_dashboard": page_admin_dashboard()
else:                            page_home()
