# ══════════════════════════════════════════════════════════════════════════════
# parser.py — NLP Resume Parser & Skill Extractor
# IT23602 — Natural Language & Image Processing
# MIT Anna University
# ══════════════════════════════════════════════════════════════════════════════
#
# NLP Pipeline:
#   1. Text Extraction     — PDF / DOCX → raw text
#   2. Preprocessing       — lowercase, clean special chars
#   3. Tokenization        — split into word tokens
#   4. Stopword Removal    — filter noise words
#   5. Lemmatization       — reduce to base form (rule-based)
#   6. Section Detection   — split resume into logical sections
#   7. Regex Extraction    — email, phone, dates
#   8. NER (manual)        — name, education, experience
#   9. Skill Matching      — token + phrase matching vs skills_db
#  10. Match Score         — compute % match against job requirements
# ══════════════════════════════════════════════════════════════════════════════

import re
import io
import string
from skills_db import (
    STOPWORDS, SKILLS, SKILL_SYNONYMS, MULTI_WORD_SKILLS,
    DEGREE_KEYWORDS, INSTITUTION_KEYWORDS, ROLE_KEYWORDS,
    MONTHS, STRONG_ACTION_VERBS, WEAK_ACTION_VERBS, SECTION_HEADERS,
)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1 — TEXT EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract raw text from a PDF file.
    Tries PyPDF2 first, falls back to pdfplumber.
    """
    text = ""

    # Try PyPDF2
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            except Exception:
                continue
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: pdfplumber
    if not text.strip():
        try:
            import pdfplumber
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception:
                        continue
        except ImportError:
            pass
        except Exception:
            pass

    return text.strip()


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract raw text from a DOCX file using python-docx.
    Reads all paragraphs in order.
    """
    text = ""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text.strip() + "\n"
    except Exception as e:
        text = f"[Error reading DOCX: {e}]"
    return text.strip()


def extract_text(uploaded_file) -> str:
    """
    Main entry: detect file type and dispatch to correct extractor.
    uploaded_file — Streamlit UploadedFile object.
    Returns plain text string.
    """
    try:
        uploaded_file.seek(0)          # always reset stream position
    except Exception:
        pass

    file_bytes = uploaded_file.read()
    filename   = uploaded_file.name.lower()

    if not file_bytes:
        return ""

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    else:
        return ""


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2 — PREPROCESSING
# ══════════════════════════════════════════════════════════════════════════════

def preprocess(text: str) -> str:
    """
    Clean raw resume text:
    - Lowercase
    - Collapse multiple newlines / spaces
    - Remove special characters except those needed for emails / phones
    """
    # Lowercase
    text = text.lower()
    # Normalise newlines
    text = re.sub(r'\r\n|\r', '\n', text)
    # Remove non-ASCII characters
    text = text.encode('ascii', errors='ignore').decode()
    # Remove URLs
    text = re.sub(r'http\S+|www\.\S+', '', text)
    # Collapse multiple spaces
    text = re.sub(r' {2,}', ' ', text)
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3 — TOKENIZATION
# ══════════════════════════════════════════════════════════════════════════════

def tokenize(text: str) -> list:
    """
    Split cleaned text into individual word tokens.
    Keeps alphanumeric + hyphen/dot for compound words like 'c++', 'node.js'.
    """
    # Split on whitespace and punctuation (keep - and . for compound terms)
    tokens = re.findall(r"[a-z][a-z0-9\.\+\#\-]*", text)
    return tokens


# ══════════════════════════════════════════════════════════════════════════════
# STEP 4 — STOPWORD REMOVAL
# ══════════════════════════════════════════════════════════════════════════════

def remove_stopwords(tokens: list) -> list:
    """
    Filter out common English stopwords that carry no signal.
    Also removes very short tokens (1 char) except 'c' and 'r' (languages).
    """
    kept = []
    for tok in tokens:
        if tok in STOPWORDS:
            continue
        if len(tok) == 1 and tok not in ('c', 'r'):
            continue
        kept.append(tok)
    return kept


# ══════════════════════════════════════════════════════════════════════════════
# STEP 5 — LEMMATIZATION (Rule-based)
# ══════════════════════════════════════════════════════════════════════════════

# Irregular verb forms → base form
IRREGULAR_VERBS = {
    "ran":"run","built":"build","wrote":"write","made":"make",
    "led":"lead","taught":"teach","gave":"give","took":"take",
    "developed":"develop","designed":"design","managed":"manage",
    "implemented":"implement","analysed":"analyse","analyzed":"analyze",
    "optimised":"optimise","optimized":"optimize","improved":"improve",
    "created":"create","deployed":"deploy","integrated":"integrate",
    "tested":"test","debugged":"debug","maintained":"maintain",
    "refactored":"refactor","launched":"launch","delivered":"deliver",
    "published":"publish","documented":"document","contributed":"contribute",
    "participated":"participate","achieved":"achieve","reduced":"reduce",
    "increased":"increase","established":"establish","initiated":"initiate",
    "proposed":"propose","reviewed":"review","validated":"validate",
    "verified":"verify","monitored":"monitor","configured":"configure",
    "administered":"administer","secured":"secure","collaborated":"collaborate",
    "mentored":"mentor","trained":"train","presented":"present",
    "researched":"research","investigated":"investigate","evaluated":"evaluate",
}

def lemmatize_token(token: str) -> str:
    """
    Rule-based lemmatizer:
    1. Check irregular verbs lookup
    2. Strip common suffixes: -ing, -ed, -er, -ly, -tion, -s
    Avoids over-stemming by requiring minimum stem length.
    """
    if token in IRREGULAR_VERBS:
        return IRREGULAR_VERBS[token]

    # -ing: running → run, working → work (stem >= 3 chars)
    if token.endswith("ing") and len(token) > 6:
        stem = token[:-3]
        # Handle double consonant: running → run
        if len(stem) > 3 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem

    # -ed: worked → work
    if token.endswith("ed") and len(token) > 5:
        stem = token[:-2]
        if len(stem) > 3 and stem[-1] == stem[-2]:
            stem = stem[:-1]
        return stem

    # -er: developer → develop
    if token.endswith("er") and len(token) > 5:
        return token[:-2]

    # -ly: quickly → quick
    if token.endswith("ly") and len(token) > 5:
        return token[:-2]

    # -tion: implementation → implement
    if token.endswith("tion") and len(token) > 7:
        return token[:-4]

    # -ment: management → manage
    if token.endswith("ment") and len(token) > 7:
        return token[:-4]

    # Plural -s (conservative — only if > 4 chars and not already a skill)
    if token.endswith("s") and len(token) > 4 and not token.endswith("ss"):
        return token[:-1]

    return token


def lemmatize(tokens: list) -> list:
    """Apply lemmatization to all tokens."""
    return [lemmatize_token(t) for t in tokens]


# ══════════════════════════════════════════════════════════════════════════════
# STEP 6 — SECTION DETECTION
# ══════════════════════════════════════════════════════════════════════════════

def detect_sections(text: str) -> dict:
    """
    Split resume text into logical sections by detecting header keywords.
    Returns a dict: { 'education': '...', 'experience': '...', ... }
    """
    sections = {key: "" for key in SECTION_HEADERS}
    sections["other"] = ""

    lines          = text.split('\n')
    current_section = "other"

    for line in lines:
        stripped = line.strip().lower()

        # Check if this line is a section header
        matched_section = None
        for section_name, keywords in SECTION_HEADERS.items():
            for kw in keywords:
                # Header lines are usually short (< 40 chars) and match a keyword
                if kw in stripped and len(stripped) < 40:
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            current_section = matched_section
        else:
            sections[current_section] += line + "\n"

    return sections


# ══════════════════════════════════════════════════════════════════════════════
# STEP 7 — REGEX EXTRACTION (Email, Phone, Dates)
# ══════════════════════════════════════════════════════════════════════════════

def extract_email(text: str) -> str:
    """Extract first email address found using regex."""
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""


def extract_phone(text: str) -> str:
    """
    Extract first phone number.
    Handles Indian formats: +91 XXXXX XXXXX, 9XXXXXXXXX, 0XX-XXXX-XXXX
    """
    patterns = [
        r'\+91[\s\-]?[6-9]\d{9}',          # +91 9XXXXXXXXX
        r'\+91[\s\-]?\d{5}[\s\-]?\d{5}',   # +91 XXXXX XXXXX
        r'[6-9]\d{9}',                       # 10-digit Indian mobile
        r'\d{3}[\s\-]\d{3}[\s\-]\d{4}',     # XXX-XXX-XXXX
        r'\(\d{3}\)[\s\-]?\d{3}[\s\-]?\d{4}',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0].strip()
    return ""


def extract_dates(text: str) -> list:
    """
    Extract date ranges from experience section.
    e.g. "Jun 2023 – Aug 2023", "2022 - present", "March 2021 to May 2022"
    Returns list of date-range strings found.
    """
    month_pat = r'(?:' + '|'.join(MONTHS) + r')'
    year_pat  = r'20\d{2}|19\d{2}'

    patterns = [
        # Jun 2023 – Aug 2023
        rf'{month_pat}\.?\s*{year_pat}\s*[-–—to]+\s*(?:{month_pat}\.?\s*)?(?:{year_pat}|present|current)',
        # 2022 – 2023
        rf'{year_pat}\s*[-–—to]+\s*(?:{year_pat}|present|current)',
        # June 2023
        rf'{month_pat}\.?\s+{year_pat}',
    ]

    found = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found.extend(matches)

    # Deduplicate while preserving order
    seen = set()
    result = []
    for d in found:
        if d not in seen:
            seen.add(d)
            result.append(d)
    return result


# ══════════════════════════════════════════════════════════════════════════════
# STEP 8 — NER: NAME, EDUCATION, EXPERIENCE (Manual heuristics)
# ══════════════════════════════════════════════════════════════════════════════

def extract_name(text: str) -> str:
    """
    Heuristic name extraction:
    - Look for "Name: ..." pattern first
    - Else take the first capitalised line at the top of the resume
      (typically the candidate's name)
    """
    # Pattern: Name: John Doe
    pattern = r'(?:name\s*[:\-]\s*)([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # Fallback: first non-empty line that looks like a proper name
    for line in text.split('\n')[:10]:
        line = line.strip()
        # A name: 2-4 words, each capitalised, no digits
        words = line.split()
        if 2 <= len(words) <= 4:
            if all(w[0].isupper() and w.isalpha() for w in words if w):
                return line

    return ""


def extract_education(sections: dict, raw_text: str) -> str:
    """
    Extract education information from the education section.
    Returns a human-readable string: "B.Tech IT — MIT Anna University (2021-2025)"
    """
    edu_text = sections.get("education", "") or raw_text

    found_degrees    = []
    found_institutes = []
    found_years      = []

    lines = edu_text.split('\n')
    for line in lines:
        lower = line.lower()

        # Check for degree keywords
        for deg in DEGREE_KEYWORDS:
            if deg in lower and line.strip():
                found_degrees.append(line.strip())
                break

        # Check for institution keywords
        for inst in INSTITUTION_KEYWORDS:
            if inst in lower and line.strip():
                found_institutes.append(line.strip())
                break

        # Extract years from education section
        years = re.findall(r'20\d{2}', line)
        found_years.extend(years)

    # Build a clean education string
    result_parts = []

    if found_degrees:
        result_parts.append(found_degrees[0])

    if found_institutes:
        inst = found_institutes[0]
        # Avoid duplicating if already in degree line
        if inst not in result_parts[0] if result_parts else True:
            result_parts.append(inst)

    if found_years:
        # Show year range e.g. 2021 - 2025
        years_sorted = sorted(set(found_years))
        if len(years_sorted) >= 2:
            result_parts.append(f"({years_sorted[0]} – {years_sorted[-1]})")
        else:
            result_parts.append(f"({years_sorted[0]})")

    if result_parts:
        return " — ".join(result_parts)

    # Last resort: return first 120 chars of education section
    if edu_text.strip():
        return edu_text.strip()[:120]

    return "Not found"


def extract_experience(sections: dict, raw_text: str) -> str:
    """
    Extract work experience / internship information.
    Returns a summary string of roles found.
    """
    exp_text = sections.get("experience", "") or ""
    if not exp_text.strip():
        exp_text = sections.get("other", "") or raw_text

    roles = []
    lines = exp_text.split('\n')

    for line in lines:
        lower = line.lower()
        for role_kw in ROLE_KEYWORDS:
            if role_kw in lower and len(line.strip()) > 5:
                roles.append(line.strip())
                break

    # Extract date ranges from experience
    dates = extract_dates(exp_text)

    if roles:
        # Return up to 2 most relevant roles
        summary = " | ".join(roles[:2])
        if dates:
            summary += f"  [{', '.join(dates[:2])}]"
        return summary[:200]  # cap at 200 chars

    # Fallback: return first meaningful lines
    meaningful = [l.strip() for l in lines if len(l.strip()) > 15]
    if meaningful:
        return meaningful[0][:150]

    return "No experience listed"


# ══════════════════════════════════════════════════════════════════════════════
# STEP 9 — SKILL EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

def extract_skills(text: str, tokens_clean: list) -> list:
    """
    Two-pass skill extraction:

    Pass 1 — Multi-word phrase matching on full text
        Check if known multi-word skills appear as substrings in text.
        e.g. "machine learning", "node.js", "rest api"

    Pass 2 — Single-token matching on cleaned token list
        Check each token (after stopword removal + lemmatization)
        against the SKILLS set, applying synonyms first.

    Returns deduplicated list of matched skill names.
    """
    found = set()
    lower_text = text.lower()

    # ── Pass 1: Multi-word phrase matching ──
    for phrase in MULTI_WORD_SKILLS:
        if phrase in lower_text:
            found.add(phrase)

    # ── Pass 2: Single token matching ──
    for token in tokens_clean:
        # Apply synonym normalisation
        normalised = SKILL_SYNONYMS.get(token, token)
        if normalised in SKILLS:
            found.add(normalised)
        elif token in SKILLS:
            found.add(token)

    # ── Pass 3: Bigram / trigram matching on tokens ──
    # Catches skills like "react native", "power bi" not in multi-word list
    words = lower_text.split()
    for i in range(len(words) - 1):
        bigram = words[i] + " " + words[i+1]
        if bigram in SKILLS:
            found.add(bigram)
        if i < len(words) - 2:
            trigram = bigram + " " + words[i+2]
            if trigram in SKILLS:
                found.add(trigram)

    # Sort for consistent output
    return sorted(found)


# ══════════════════════════════════════════════════════════════════════════════
# STEP 10 — MATCH SCORE CALCULATION
# ══════════════════════════════════════════════════════════════════════════════

def calculate_match_score(extracted_skills: list, required_skills: list) -> int:
    """
    Compute how well the candidate's skills match the job requirements.

    Score breakdown:
    - Skill match  : 70% weight — # required skills found / total required
    - Bonus        : 30% — extra skills beyond the required set (shows breadth)

    Returns integer 0-100.
    """
    if not required_skills:
        return 0

    extracted_lower = {s.lower() for s in extracted_skills}
    required_lower  = [s.lower() for s in required_skills]

    # Count how many required skills the candidate has
    matched = sum(1 for req in required_lower if req in extracted_lower)

    # Core match percentage
    core_score = (matched / len(required_lower)) * 70

    # Bonus for extra skills (up to 30 points)
    extra_skills = len(extracted_lower) - matched
    bonus_score  = min(extra_skills * 4, 30)

    total = round(core_score + bonus_score)
    return min(total, 100)  # cap at 100


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT — parse_resume()
# ══════════════════════════════════════════════════════════════════════════════

def parse_resume(uploaded_file, job: dict) -> dict:
    """
    Full NLP pipeline. Called from app.py on resume upload.

    Args:
        uploaded_file : Streamlit UploadedFile object (PDF or DOCX)
        job           : dict with at least { 'skills': [...] }

    Returns:
        {
            'name'        : str,
            'email'       : str,
            'phone'       : str,
            'skills'      : list,
            'education'   : str,
            'experience'  : str,
            'match_score' : int,
            'raw_text'    : str,   # for debugging
            'tokens'      : list,  # for debugging
        }
    """

    # ── 1. Extract raw text ──
    raw_text = extract_text(uploaded_file)

    if not raw_text.strip():
        return {
            "name": "", "email": "", "phone": "",
            "skills": [], "education": "Could not extract text from resume.",
            "experience": "", "match_score": 0,
            "raw_text": "", "tokens": [],
        }

    # ── 2. Preprocess ──
    cleaned_text = preprocess(raw_text)

    # ── 3. Tokenize ──
    tokens = tokenize(cleaned_text)

    # ── 4. Remove stopwords ──
    tokens_no_stop = remove_stopwords(tokens)

    # ── 5. Lemmatize ──
    tokens_lemma = lemmatize(tokens_no_stop)

    # ── 6. Detect sections ──
    sections = detect_sections(cleaned_text)

    # ── 7. Regex extraction ──
    email = extract_email(raw_text)
    phone = extract_phone(raw_text)

    # ── 8. NER — name, education, experience ──
    name       = extract_name(raw_text)
    education  = extract_education(sections, cleaned_text)
    experience = extract_experience(sections, cleaned_text)

    # ── 9. Skill extraction ──
    skills = extract_skills(cleaned_text, tokens_lemma)

    # ── 10. Match score ──
    required_skills = job.get("skills", [])
    match_score     = calculate_match_score(skills, required_skills)

    return {
        "name"        : name,
        "email"       : email,
        "phone"       : phone,
        "skills"      : skills,
        "education"   : education,
        "experience"  : experience,
        "match_score" : match_score,
        "raw_text"    : raw_text,
        "tokens"      : tokens_lemma,
    }