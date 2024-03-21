from io import TextIOWrapper


class CsvDoc:
    title: str
    content: str
    
    def __init__(self, title: str, content: TextIOWrapper):
        self.title = title
        self.content = content.read()
        