import re
import sys

class LexicalAnalyzer:
    def __init__(self):
        self.line_number = 1
        self.cBrac = 0
        self.nc = 0
        self.flag = False
        self.cLine = 0
        self.var = 0
        self.symbol_table = []
        self.constants_table = []
        self.parsed_table = []
        self.comments = []
        self.single_line_comments = []
        self.in_multiline_comment = False
        self.current_multiline_comment = ""

        # Token patterns (comment patterns moved to top!)
        self.patterns = [
            (r'^#.*', 'd', "Preprocessor Statement"),
            (r'//.*', 'COMMENT', None),
            (r'/\*', 'MULTILINE_COMMENT_START', None),
            (r'\*/', 'MULTILINE_COMMENT_END', None),
            (r'\b(auto|break|case|char|const|continue|default|do|else|double|enum|extern|float|for|goto|if|int|long|register|return)\b', 'k', "Keyword"),
            (r'\b(signed|unsigned)?\s*(long|short)?\s*(int|char|void)\b', 'k', "Keyword"),
            (r'\b(signed|unsigned)?\s*(long|short)?\s*(int|char|void)\s*([a-zA-Z_]\w*)\s*\(.*\)', 'j', "Procedure"),
            (r'([a-zA-Z_]\w*)\s*\[\s*\d*\s*\]', 'a', "Array"),
            (r'\*\s*([a-zA-Z_]\w*)', 'q', "Pointer"),
            (r'[a-zA-Z_]\w*', 'i', "Identifier"),
            (r'[><]=?|!=|==', 'r', "Relational Op"),
            (r'[&|^~]', 'l', "Logical Op"),
            (r'[+\-*/%]', 'o', "Arithmetic Op"),
            (r'=', 'e', "Assignment Op"),
            (r'[(){}\[\];,.:]', 'p', "Punctuator"),
            (r'\d+', 'c', "Integer Constant"),
            (r'[-+]?\d*\.\d+([eE][-+]?\d+)?', 'f', "Float Constant"),
            (r'\'.\'', 'z', "Character Constant"),
            (r'\"(\\.|[^"\\])*\"', 's', "String Literal"),
            (r'\s+', None, None),
            (r'\n', 'NEWLINE', None)
        ]

        self.compiled_patterns = [(re.compile(pattern), token_type, token_name) for pattern, token_type, token_name in self.patterns]

    def analyze(self, code):
        self.code = code
        self.pos = 0
        self.length = len(code)
        while self.pos < self.length:
            self.match_patterns()

    def match_patterns(self):
        for pattern, token_type, token_name in self.compiled_patterns:
            match = pattern.match(self.code, self.pos)
            if match:
                # Handle if we're inside a multiline comment and not at the end yet
                if self.in_multiline_comment and token_type not in ['MULTILINE_COMMENT_END', 'MULTILINE_COMMENT_START']:
                    self.current_multiline_comment += match.group()
                    self.line_number += match.group().count('\n')
                    self.pos = match.end()
                    return

                self.handle_match(match, token_type, token_name)
                return
        char = self.code[self.pos]
        print(f"{self.input_file} : {self.line_number} : Invalid character '{char}'")
        self.pos += 1

    def handle_match(self, match, token_type, token_name):
        value = match.group()
        end_pos = match.end()

        if token_type == 'NEWLINE':
            self.line_number += 1
            self.pos = end_pos
            return

        if token_type == 'COMMENT':
            self.handle_single_line_comment(value)
            self.pos = end_pos
            return

        if token_type == 'MULTILINE_COMMENT_START':
            self.handle_multiline_comment_start()
            self.pos = end_pos
            return

        if token_type == 'MULTILINE_COMMENT_END':
            self.handle_multiline_comment_end()
            self.pos = end_pos
            return

        if token_type is None:
            self.line_number += value.count('\n')
            self.pos = end_pos
            return

        if value == '{':
            self.cBrac += 1
        elif value == '}':
            self.cBrac -= 1

        if self.nc <= 0:
            self.insert_to_tables(value, token_type, token_name)

        self.pos = end_pos

    def handle_single_line_comment(self, comment):
        content = comment[2:]
        self.single_line_comments.append(content)
        self.comments.append(comment)

    def handle_multiline_comment_start(self):
        self.nc += 1
        self.cLine += 1
        self.in_multiline_comment = True
        self.current_multiline_comment = "/*"

        if self.nc > 1:
            print(f"{self.input_file} : {self.line_number} : Nested Comment")
            self.flag = True

    def handle_multiline_comment_end(self):
        if self.nc > 0:
            self.nc -= 1
        else:
            print(f"{self.input_file} : {self.line_number} : */ found before /*")

        if self.in_multiline_comment:
            self.current_multiline_comment += "*/"
            self.comments.append(self.current_multiline_comment)
            self.current_multiline_comment = ""
            self.in_multiline_comment = False

    def insert_to_tables(self, value, token_type, token_name):
        existing_entry = next((entry for entry in self.symbol_table if entry['lexeme'] == value), None)

        if existing_entry is None:
            if token_type in ['i', 'a', 'q', 'j']:
                self.symbol_table.append({
                    'lexeme': value,
                    'type': token_name,
                    'attribute_value': self.var,
                    'line_number': self.line_number
                })
                self.var += 1

            if token_type in ['c', 'f', 'z']:
                const_type = {'c': 'int', 'f': 'float', 'z': 'char'}[token_type]
                self.constants_table.append({
                    'lexeme': value,
                    'type': const_type,
                    'attribute_value': self.var,
                    'line_number': self.line_number
                })
                self.var += 1

        self.parsed_table.append({
            'lexeme': value,
            'type': token_name,
            'attribute_value': self.var - 1 if existing_entry is None else existing_entry['attribute_value'],
            'line_number': self.line_number
        })

    def generate_reports(self):
        def table_to_str(title, entries):
            out = f"\n{title}:\n"
            out += f"{'Lexeme':20}{'Type':35}{'Attribute Value':30}{'Line Number':15}\n"
            for e in entries:
                out += f"{e['lexeme']:20}{e['type']:20}{e['attribute_value']:30}{e['line_number']:15}\n"
            return out

        symbol_report = table_to_str("Symbol Table", self.symbol_table)
        constants_report = table_to_str("Constants Table", self.constants_table)
        parsed_report = table_to_str("Parsed Table", self.parsed_table)

        comments_report = "\nComments:\n"
        if self.flag:
            comments_report += f"Nested Comments ({self.cLine} lines)\n"
        else:
            comments_report += f"Multi-line Comments ({self.cLine} lines):\n"
            comments_report += "\n".join(c for c in self.comments if c.startswith("/*")) + "\n"
            comments_report += "\nSingle-line Comments:\n"
            comments_report += "\n".join(self.single_line_comments) + "\n"

        return {
            'symbol_table': symbol_report,
            'constants_table': constants_report,
            'parsed_table': parsed_report,
            'comments': comments_report
        }

    def analyze_file(self, file_path):
        self.input_file = file_path
        with open(file_path, 'r') as f:
            code = f.read()
        self.analyze(code)
        if self.nc != 0:
            print(f"{self.input_file} : {self.line_number} : Comment Does Not End")
        if self.cBrac != 0:
            print(f"{self.input_file} : {self.line_number} : Unbalanced Parentheses")
        return self.generate_reports()


def main():
    if len(sys.argv) > 1:
        lexer = LexicalAnalyzer()
        reports = lexer.analyze_file(sys.argv[1])
        with open('symbolTable.txt', 'w') as f:
            f.write(reports['symbol_table'])
        with open('constantTable.txt', 'w') as f:
            f.write(reports['constants_table'])
        with open('parsedTable.txt', 'w') as f:
            f.write(reports['parsed_table'])
            f.write("\n\n" + reports['comments'])
        print("Lexical analysis completed. Reports generated in:")
        print("- symbolTable.txt")
        print("- constantTable.txt")
        print("- parsedTable.txt")
    else:
        print("Usage: python lexer.py <input_file>")


if __name__ == "__main__":
    main()
