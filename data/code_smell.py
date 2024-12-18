MAX_CODE_SEGMENT_LENGTH = 256000

class CodeSmell:
    def __init__(self, smell_id, code_sample_id, smell, severity, scope, code_name, start_line, end_line, link):
        self.id = smell_id
        self.code_sample_id = code_sample_id
        self.smell = smell
        self.severity = severity
        self.scope = scope
        self.code_name = code_name
        self.start_line = start_line
        self.end_line = end_line
        self.link = link

    def save(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO CodeSmell(id, code_sample_id, smell, severity, scope, code_name, start_line, end_line, link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.id, self.code_sample_id, self.smell, self.severity, self.scope, self.code_name, self.start_line, self.end_line,
            self.link))
        conn.commit()

    def get_name(self):
        # If code_name contains hashtag, return the first word after the hashtag
        if '#' in self.code_name:
            return self.code_name.split('#')[1].split(' ')[0]
        else:
            # Otherwise, return the first word after the last dot
            return self.code_name.split('.')[-1].split(' ')[0]

    @staticmethod
    def get_ids(conn, smell, severity, amount, min_id=None):
        if min_id is None: min_id = 0
        cursor = conn.cursor()
        cursor.execute('''
            SELECT CodeSmell.id FROM CodeSmell INNER JOIN CodeSample on CodeSample.id = CodeSmell.code_sample_id WHERE smell = ? AND severity = ? AND CodeSmell.id >= ? AND CodeSmell.id <= 10224 and length(code_segment) < ? LIMIT ?;
        ''', (smell, severity, min_id, MAX_CODE_SEGMENT_LENGTH, amount))
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    @staticmethod
    def get_code_sample_ids(conn, ids):
        cursor = conn.cursor()
        query = '''
                    SELECT DISTINCT code_sample_id 
                    FROM CodeSmell 
                    WHERE id IN ({})
                '''.format(','.join('?' * len(ids)))
        cursor.execute(query, ids)
        rows = cursor.fetchall()
        return [row[0] for row in rows]

    def __str__(self):
        return f'{self.id} {self.smell} {self.severity} {self.code_name}'
