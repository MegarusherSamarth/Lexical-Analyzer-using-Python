# Lexical Analyzer using Python

A modular lexical analyzer built with Python and React, designed to tokenize and classify input strings for compiler design and language processing tasks. This project demonstrates clean separation of concerns, with a Python backend for lexical logic and a React-based frontend for user interaction.

---

## 📚 Table of Contents
- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [How It Works](#how-it-works)
- [Folder Structure](#folder-structure)
- [Use Cases](#use-cases)
- [Screenshots](#screenshots)
- [License](#license)
- [Author](#author)

---

## 🔍 Features
- Tokenizes input into:
  - Keywords (e.g., `if`, `while`, `return`)
  - Identifiers (e.g., variable names)
  - Operators (`+`, `-`, `*`, `/`, `=`)
  - Literals (e.g., numbers, strings)
  - Delimiters (`;`, `{}`, `()`)
- Modular folder structure: React frontend and Python backend
- Interactive web interface for input/output
- Easily extendable for new token types or grammar rules
- Educational and beginner-friendly design

---

## 🧠 Architecture Overview

This project follows a **modular, decoupled architecture**:

- **Backend**: Python script (`main.py`) performs lexical analysis.
- **Frontend**: Built with React, provides a responsive UI for input and output.
- **Communication**: Currently independent; future versions may integrate via REST API or WebSocket.

---

## 🛠️ Tech Stack

| Layer     | Technology         | Purpose                          |
|-----------|--------------------|----------------------------------|
| Backend   | Python             | Lexical analysis logic           |
| Frontend  | React (JSX, CSS)   | User interface and interaction   |
| Execution | Local (CLI + Browser) | Simple, no server required    |

---

## 🚀 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/MegarusherSamarth/Lexical-Analyzer-using-Python
cd Lexical-Analyzer-using-Python
```

### 2. Run the backend analyzer
```bash
cd Backend
python main.py
```

### 3. Launch the frontend
```bash
cd Frontend
npm install
npm start
```

> This will start the React development server and open the app in your browser.

---

## ⚙️ How It Works

1. **Input**: User enters a string of code via the React UI.
2. **Processing**:
   - Python script reads the input.
   - Applies regex and string parsing to identify tokens.
   - Classifies each token into its type.
3. **Output**:
   - Tokens are displayed in the React UI.
   - Backend prints results to console (for debugging).

---

## 📁 Folder Structure

```
Lexical-Analyzer-using-Python/
├── Backend/
│   └── main.py          # Core lexical analysis logic
├── Frontend/
│   ├── public/          # Static assets
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   ├── index.js     # Entry point
│   │   └── styles.css   # Custom styling
├── README.md            # Project documentation
└── LICENSE              # Open-source license
```

---

## 🧪 Use Cases
- Compiler design coursework and demos
- Tokenization for NLP preprocessing
- Educational tool for understanding lexical analysis
- Base for building interpreters or parsers

---

## 🖼️ Screenshots

> Add screenshots of:
> - React UI with sample input/output
> - Console output from backend

---

## 📄 License

This project is licensed under the MIT License. You are free to use, modify, and distribute it with attribution.

See the [LICENSE](LICENSE) file for full details.

---

## 🙌 Author

**MegarusherSamarth**  
Visionary technologist focused on modular, multi-tenant systems for real-world impact.  
GitHub: [@MegarusherSamarth](https://github.com/MegarusherSamarth)

---

## 💡 Future Improvements
- Integrate backend and frontend via Flask or FastAPI
- Add support for more languages and token types
- Export tokenized output to CSV or JSON
- Add unit tests and CI/CD pipeline

---

## 🗣️ Feedback & Contributions

Feel free to fork, raise issues, or submit pull requests.  
For suggestions or collaboration, reach out via GitHub Issues or Discussions.

---

Let me know if you want help generating screenshots, writing a LICENSE file, or integrating the backend with React via API. I can also help you scaffold a README for your HFT simulator next.
