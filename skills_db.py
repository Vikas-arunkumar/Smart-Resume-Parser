# ══════════════════════════════════════════════════════════════════════════════
# skills_db.py — Data backbone for TalentScan NLP Parser
# IT23602 — Natural Language & Image Processing
# MIT Anna University
# ══════════════════════════════════════════════════════════════════════════════

# ── STOPWORDS ─────────────────────────────────────────────────────────────────
# Common English words that carry no meaningful signal for skill/entity extraction
STOPWORDS = {
    "a","an","the","and","or","but","if","in","on","at","to","for","of","with",
    "by","from","as","is","was","are","were","be","been","being","have","has",
    "had","do","does","did","will","would","could","should","may","might","shall",
    "can","need","dare","ought","used","able","i","me","my","myself","we","our",
    "ours","ourselves","you","your","yours","yourself","yourselves","he","him",
    "his","himself","she","her","hers","herself","it","its","itself","they","them",
    "their","theirs","themselves","what","which","who","whom","this","that","these",
    "those","am","into","through","during","before","after","above","below","between",
    "each","both","few","more","most","other","some","such","no","not","only","own",
    "same","so","than","too","very","just","because","while","although","however",
    "therefore","thus","hence","also","well","about","up","out","there","here",
    "when","where","how","all","any","both","each","many","much","more","most",
    "other","some","such","over","under","again","further","once","within","without",
    "during","including","across","behind","across","despite","towards","upon",
    "working","work","works","worked","use","using","used","uses","make","makes",
    "making","made","help","helps","helped","helping","get","gets","getting","got",
    "take","takes","taking","took","give","gives","giving","gave","good","great",
    "new","old","high","low","large","small","long","short","strong","able","major",
}

# ── SKILLS DATABASE ───────────────────────────────────────────────────────────
# Organised by domain. All lowercase for easy matching.

SKILLS = {

    # ── Programming Languages ──
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go",
    "golang", "rust", "ruby", "php", "swift", "kotlin", "scala", "r",
    "matlab", "perl", "bash", "shell", "powershell", "lua", "dart",
    "objective-c", "assembly", "cobol", "fortran", "haskell", "elixir",
    "clojure", "groovy", "vba", "visual basic",

    # ── Web Frontend ──
    "html", "css", "html5", "css3", "sass", "scss", "less", "bootstrap",
    "tailwind", "tailwindcss", "react", "reactjs", "react.js", "angular",
    "angularjs", "vue", "vuejs", "vue.js", "svelte", "jquery", "next.js",
    "nextjs", "nuxt.js", "gatsby", "webpack", "babel", "vite", "parcel",
    "figma", "sketch", "adobe xd", "responsive design", "pwa",

    # ── Web Backend ──
    "node.js", "nodejs", "express", "express.js", "django", "flask",
    "fastapi", "spring", "spring boot", "laravel", "rails", "ruby on rails",
    "asp.net", ".net", "dotnet", "graphql", "rest", "rest api", "restful",
    "soap", "grpc", "websocket", "microservices", "api", "web services",

    # ── Databases ──
    "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle", "sql server",
    "mssql", "mongodb", "mongoose", "redis", "cassandra", "dynamodb",
    "firebase", "firestore", "elasticsearch", "neo4j", "mariadb", "couchdb",
    "influxdb", "hbase", "nosql", "database design", "orm",

    # ── Data Science & ML ──
    "machine learning", "deep learning", "neural network", "artificial intelligence",
    "ai", "ml", "nlp", "natural language processing", "computer vision",
    "data science", "data analysis", "data analytics", "data mining",
    "statistics", "probability", "linear regression", "logistic regression",
    "decision tree", "random forest", "svm", "support vector machine",
    "k-means", "clustering", "classification", "regression", "time series",
    "feature engineering", "model evaluation", "cross validation",
    "hyperparameter tuning", "transfer learning", "reinforcement learning",
    "generative ai", "llm", "transformers", "bert", "gpt",

    # ── ML / Data Libraries ──
    "numpy", "pandas", "matplotlib", "seaborn", "plotly", "scipy",
    "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch", "torch",
    "huggingface", "xgboost", "lightgbm", "catboost", "spacy", "nltk",
    "gensim", "opencv", "pillow", "pil", "statsmodels",

    # ── Cloud & DevOps ──
    "aws", "amazon web services", "azure", "microsoft azure", "gcp",
    "google cloud", "heroku", "digitalocean", "docker", "kubernetes", "k8s",
    "jenkins", "github actions", "gitlab ci", "travis ci", "ci/cd",
    "terraform", "ansible", "puppet", "chef", "nginx", "apache",
    "linux", "unix", "ubuntu", "centos", "debian", "windows server",

    # ── Version Control & Tools ──
    "git", "github", "gitlab", "bitbucket", "svn", "jira", "confluence",
    "trello", "slack", "postman", "swagger", "vs code", "visual studio",
    "intellij", "eclipse", "pycharm", "vim", "emacs", "terminal",

    # ── Mobile ──
    "android", "ios", "react native", "flutter", "xamarin", "ionic",
    "mobile development", "app development",

    # ── Cybersecurity ──
    "cybersecurity", "network security", "penetration testing", "ethical hacking",
    "cryptography", "firewall", "vpn", "ssl", "tls", "owasp", "siem",
    "vulnerability assessment", "security audit",

    # ── Networking ──
    "networking", "tcp/ip", "http", "https", "dns", "dhcp", "ftp",
    "socket programming", "network protocols", "lan", "wan",

    # ── Embedded & Hardware ──
    "embedded systems", "arduino", "raspberry pi", "iot", "rtos",
    "microcontroller", "fpga", "verilog", "vhdl", "pcb design",

    # ── Testing ──
    "unit testing", "integration testing", "selenium", "pytest", "junit",
    "jest", "mocha", "cypress", "test driven development", "tdd",
    "quality assurance", "qa", "manual testing", "automation testing",

    # ── Soft Skills (detectable from resume text) ──
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "project management",
    "agile", "scrum", "kanban", "waterfall",

    # ── Data Engineering ──
    "apache spark", "spark", "hadoop", "kafka", "airflow", "etl",
    "data pipeline", "data warehouse", "snowflake", "bigquery",
    "redshift", "dbt", "tableau", "power bi", "looker", "excel",

    # ── Other Tools ──
    "latex", "markdown", "json", "xml", "yaml", "csv",
    "jupyter", "jupyter notebook", "google colab", "streamlit",
}

# ── SKILL SYNONYMS ────────────────────────────────────────────────────────────
# Maps abbreviations / alternate names → canonical skill name
# Used to normalise extracted tokens before matching

SKILL_SYNONYMS = {
    "js"           : "javascript",
    "ts"           : "typescript",
    "py"           : "python",
    "rb"           : "ruby",
    "ml"           : "machine learning",
    "ai"           : "artificial intelligence",
    "dl"           : "deep learning",
    "nlp"          : "natural language processing",
    "cv"           : "computer vision",
    "ds"           : "data science",
    "sql server"   : "mssql",
    "postgres"     : "postgresql",
    "react.js"     : "react",
    "reactjs"      : "react",
    "node"         : "node.js",
    "nodejs"       : "node.js",
    "vue.js"       : "vue",
    "vuejs"        : "vue",
    "next.js"      : "nextjs",
    "angular.js"   : "angular",
    "angularjs"    : "angular",
    "sklearn"      : "scikit-learn",
    "tf"           : "tensorflow",
    "torch"        : "pytorch",
    "k8s"          : "kubernetes",
    "gcp"          : "google cloud",
    "aws"          : "amazon web services",
    "azure"        : "microsoft azure",
    "rest api"     : "rest",
    "restful api"  : "rest",
    "restful"      : "rest",
    "oop"          : "object oriented programming",
    "oops"         : "object oriented programming",
    "dsa"          : "data structures",
    "c plus plus"  : "c++",
    "dot net"      : ".net",
    "dotnet"       : ".net",
    "msql"         : "mysql",
    "mongo"        : "mongodb",
    "postgres"     : "postgresql",
    "tailwind css" : "tailwindcss",
    "scss"         : "sass",
    "colab"        : "google colab",
    "jupyter nb"   : "jupyter notebook",
    "vsc"          : "vs code",
    "gh"           : "github",
    "gl"           : "gitlab",
}

# ── MULTI-WORD SKILLS ─────────────────────────────────────────────────────────
# Skills that are phrases — checked via substring match in full text
# Ordered longest first to avoid partial matches

MULTI_WORD_SKILLS = sorted([
    "machine learning", "deep learning", "neural network", "natural language processing",
    "computer vision", "data science", "data analysis", "data analytics", "data mining",
    "data engineering", "data pipeline", "data warehouse", "feature engineering",
    "transfer learning", "reinforcement learning", "generative ai", "time series",
    "support vector machine", "random forest", "decision tree", "logistic regression",
    "linear regression", "k-means clustering", "cross validation", "hyperparameter tuning",
    "model evaluation", "amazon web services", "microsoft azure", "google cloud",
    "spring boot", "ruby on rails", "node.js", "react.js", "vue.js", "next.js",
    "express.js", "rest api", "restful api", "web services", "database design",
    "sql server", "power bi", "apache spark", "unit testing", "integration testing",
    "test driven development", "quality assurance", "automation testing", "manual testing",
    "penetration testing", "ethical hacking", "network security", "vulnerability assessment",
    "security audit", "embedded systems", "raspberry pi", "mobile development",
    "app development", "project management", "problem solving", "critical thinking",
    "time management", "object oriented programming", "data structures", "operating systems",
    "computer networks", "software engineering", "agile methodology", "version control",
    "responsive design", "ci/cd", "github actions", "gitlab ci", "google colab",
    "jupyter notebook", "vs code", "visual studio",
], key=len, reverse=True)

# ── DEGREE KEYWORDS ───────────────────────────────────────────────────────────
# Used to detect education section entries

DEGREE_KEYWORDS = [
    "b.tech", "b.e", "b.sc", "b.com", "b.a", "b.ca", "bca", "bsc", "bcom",
    "m.tech", "m.e", "m.sc", "m.com", "m.a", "mca", "msc", "mcom", "mba",
    "phd", "ph.d", "doctorate", "bachelor", "master", "bachelor's", "master's",
    "undergraduate", "postgraduate", "diploma", "associate", "engineering",
    "technology", "science", "arts", "commerce", "computer science", "information technology",
    "computer engineering", "electronics", "electrical", "mechanical", "civil",
]

# ── UNIVERSITY / INSTITUTION KEYWORDS ────────────────────────────────────────
INSTITUTION_KEYWORDS = [
    "university", "institute", "college", "school", "academy", "iit", "nit",
    "anna university", "mit", "bits", "vit", "srm", "sastra", "amrita",
    "psg", "coimbatore", "chennai", "bangalore", "mumbai", "delhi", "hyderabad",
]

# ── EXPERIENCE / ROLE KEYWORDS ────────────────────────────────────────────────
# Used to detect experience section and extract roles

ROLE_KEYWORDS = [
    "intern", "internship", "engineer", "developer", "programmer", "analyst",
    "scientist", "architect", "designer", "manager", "lead", "head", "director",
    "consultant", "associate", "senior", "junior", "fresher", "trainee",
    "full stack", "frontend", "backend", "devops", "data", "software",
    "project", "product", "research", "assistant",
]

# ── MONTH NAMES ───────────────────────────────────────────────────────────────
# For date / duration extraction

MONTHS = [
    "january","february","march","april","may","june",
    "july","august","september","october","november","december",
    "jan","feb","mar","apr","jun","jul","aug","sep","oct","nov","dec",
]

# ── ACTION VERBS ──────────────────────────────────────────────────────────────
# Strong resume action verbs — used for resume quality scoring

STRONG_ACTION_VERBS = {
    "developed","designed","built","implemented","created","engineered","architected",
    "optimised","optimized","improved","enhanced","automated","deployed","integrated",
    "led","managed","coordinated","collaborated","mentored","trained","presented",
    "analysed","analyzed","researched","investigated","evaluated","tested","debugged",
    "maintained","refactored","migrated","launched","delivered","published","wrote",
    "documented","contributed","participated","achieved","reduced","increased",
    "streamlined","accelerated","established","initiated","proposed","reviewed",
    "validated","verified","monitored","configured","administered","secured",
}

WEAK_ACTION_VERBS = {
    "helped","assisted","worked","did","made","tried","attempted","used","handled",
    "responsible","involved","participated","was","were","am","is",
}

# ── SECTION HEADERS ───────────────────────────────────────────────────────────
# Used to split resume into logical sections

SECTION_HEADERS = {
    "education"   : ["education", "academic", "qualification", "degree", "schooling"],
    "experience"  : ["experience", "work experience", "employment", "internship",
                     "professional experience", "career", "work history"],
    "skills"      : ["skills", "technical skills", "core skills", "key skills",
                     "competencies", "technologies", "tools", "expertise"],
    "projects"    : ["projects", "project work", "academic projects", "personal projects"],
    "certifications": ["certifications", "certificates", "courses", "training",
                       "achievements", "awards"],
    "contact"     : ["contact", "personal", "personal information", "profile"],
    "summary"     : ["summary", "objective", "profile", "about", "overview"],
}