import sqlite3

class CodeSample:
    def __init__(self, sample_id, repository, commit_hash, path, start_line, end_line, link):
        self.id = sample_id
        self.repository = repository
        self.commit_hash = commit_hash
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.link = link

    def save(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO CodeSample(id, repository, commit_hash, path, start_line, end_line, link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.id, self.repository, self.commit_hash, self.path, self.start_line, self.end_line, self.link))
        conn.commit()

    def __str__(self):
        return f'{self.repository} {self.commit_hash} {self.path} {self.start_line} {self.end_line}'

class CodeScope:
    def __init__(self, sample_id, scope_type, code_segment=None):
        self.id = None
        self.sample_id = sample_id
        self.scope_type = scope_type
        self.code_segment = code_segment

    def save(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO CodeScope(sample_id, scope_type, code_segment)
            VALUES (?, ?, ?)
        ''', (self.sample_id, self.scope_type, self.code_segment))
        conn.commit()
        cursor.execute('''
            SELECT id FROM CodeScope WHERE sample_id = ? AND scope_type = ? 
        ''', (self.sample_id, self.scope_type))
        result = cursor.fetchone()
        if result:
            self.id = result[0]
            return True
        return False

    def __str__(self):
        return f'{self.sample_id} {self.scope_type}'

class CodeSmell:
    def __init__(self, smell_id, code_sample_id, smell_type, severity, reviewer_id, review_timestamp):
        self.id = smell_id
        self.code_sample_id = code_sample_id
        self.smell_type = smell_type
        self.severity = severity
        self.reviewer_id = reviewer_id
        self.review_timestamp = review_timestamp

    def save(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO CodeSmell(id, code_sample_id, smell_type, severity, reviewer_id, review_timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.id, self.code_sample_id, self.smell_type, self.severity, self.reviewer_id, self.review_timestamp))
        conn.commit()

    def __str__(self):
        return f'{self.code_sample_id} {self.smell_type} {self.severity}'

def initialize_database():
    conn = sqlite3.connect('../data/code_smell_analysis.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CodeSample(
            id INTEGER PRIMARY KEY,
            repository TEXT,
            commit_hash TEXT,
            path TEXT,
            start_line INTEGER,
            end_line INTEGER,
            link TEXT,
            UNIQUE(repository, commit_hash, path, start_line, end_line)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CodeScope (
            id INTEGER PRIMARY KEY,
            sample_id INTEGER,
            scope_type TEXT,
            code_segment TEXT,
            FOREIGN KEY (sample_id) REFERENCES CodeSample(id)
            UNIQUE(sample_id, scope_type)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CodeSmell (
            id INTEGER PRIMARY KEY,
            code_sample_id INTEGER,
            smell_type TEXT,
            severity TEXT,
            reviewer_id INTEGER,
            review_timestamp TEXT,
            FOREIGN KEY (code_sample_id) REFERENCES CodeSample(id)
        )
    ''')
    conn.commit()
    return conn