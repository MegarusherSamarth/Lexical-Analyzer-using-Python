import React, { useState } from "react";

function App() {
  const [code, setCode] = useState("");
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    const res = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();
    setResults(data);
  };

  const Section = ({ title, content }) => (
    <div>
      <h2 className="text-xl font-semibold">{title}</h2>
      <pre className="bg-gray-100 p-4 rounded overflow-auto font-mono whitespace-pre text-sm">
        {content}
      </pre>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50 px-6 py-8 relative w-screen">
      <div className="max-w-4xl mx-auto bg-white rounded shadow p-6">
        <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
          Lexical Analyzer
        </h1>
        <h2 className="fixed bottom-6 right-6 text-3xl text-red-600 outline-2 outline-amber-700 p-4 rounded-3xl">
          By: MegaRushers
        </h2>

        <textarea
          rows="10"
          className="w-full border rounded p-3 text-sm font-mono focus:outline-none focus:ring focus:border-blue-400"
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Paste your C code here..."
        />

        <div className="text-center mt-4">
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded transition duration-200"
            onClick={handleAnalyze}
          >
            Analyze
          </button>
        </div>

        {results && (
          <div className="mt-8 space-y-6">
            <Section title="🔤 Symbol Table" content={results.symbolTable} />
            <Section
              title="🔢 Constants Table"
              content={results.constantTable}
            />
            <Section title="🧩 Parsed Table" content={results.parsedTable} />
            <Section title="💬 Comments" content={results.comments} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
