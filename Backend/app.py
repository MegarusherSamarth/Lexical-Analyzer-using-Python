from flask import Flask, request, jsonify
from flask_cors import CORS
from lexical_analyzer import LexicalAnalyzer  # your class file

app = Flask(__name__)
CORS(app)  # allows requests from React

@app.route('/analyze', methods=['POST'])
def analyze_code():
    data = request.get_json()
    source_code = data.get('code', '')

    lexer = LexicalAnalyzer()
    lexer.analyze(source_code)
    reports = lexer.generate_reports()

    return jsonify({
        'symbolTable': reports['symbol_table'],
        'constantTable': reports['constants_table'],
        'parsedTable': reports['parsed_table'],
        'comments': reports['comments']
    })

if __name__ == '__main__':
    app.run(debug=True)
