import { useState } from "react";
import "./styles.css";

function App() {
  const [text, setText] = useState("");      // <-- for input text
  const [query, setQuery] = useState("");    // <-- question
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [file, setFile] = useState(null);

  const handleQuery = async () => {
    if (!query.trim()) return alert("Please enter a question.");

    const formData = new FormData();
    formData.append("q", query);

    // If text is provided, send it too
    if (text.trim()) {
      formData.append("text", text);
    }

    // If a file is uploaded, send it too
    if (file) {
      formData.append("file", file);
    }

    const res = await fetch(`${__BACKEND_URL__}/query`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setAnswer(data.answer);
    setSources(data.sources || []);
  };

  const handleUpload = () => {
    if (!file) return alert("No file selected.");
    alert("File will be sent along with your query. You can also input text manually.");
  };

  return (
    <div className="app">
      <h1>Mini RAG</h1>
      <p className="subtitle">Provide text or upload file, then ask a question</p>

      {/* Optional text input */}
      <textarea
        placeholder="Paste text here (optional)..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      {/* Optional file upload */}
      <div className="upload-section">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />
        <button className="btn" onClick={handleUpload}>Attach File</button>
      </div>

      {/* Query input */}
      <textarea
        placeholder="Ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button className="btn" onClick={handleQuery}>Ask Question</button>

      {/* Answer display */}
      {answer && (
        <div className="answer">
          <h2>Answer</h2>
          <p>{answer}</p>
          {sources.length > 0 && (
            <>
              <h3>Sources</h3>
              <ul>
                {sources.map((s, i) => (
                  <li key={i}>{s.content}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
