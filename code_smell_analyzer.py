import csv

def get_data_list(path):
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        return [row for row in reader]

def get_snippet(file_content, start_line, end_line):
    lines = file_content.split("\n")
    return "\n".join(lines[start_line-1:end_line])


class CodeSmellAnalyzer:
    def __init__(self, repository):
        self.repository = repository

    def get_code_smells(self, data_list, limit=None):
        code_smells = []
        for i, data in enumerate(data_list):
            if limit is not None and i >= limit:
                break
            file_content = self.repository.get_file_content(
                data["repository"], data["commit_hash"], data["path"]
            )
            snippet = get_snippet(file_content, int(data["start_line"]), int(data["end_line"]))
            code_smells.append({
                "id": data["id"],
                "smell": data["smell"],
                "severity": data["severity"],
                "type": data["type"],
                "snippet": snippet
            })
        return code_smells