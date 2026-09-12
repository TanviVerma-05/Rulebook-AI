import { useState } from "react";
import "./App.css";

const API_URL = "http://localhost:5000/api/ask";

function App() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setResult(data);
    } catch (error) {
      setResult({
        state: "ERROR",
        answer: error.message,
        citations: [],
        conflicts: [],
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && e.ctrlKey) {
      askQuestion();
    }
  };

  const getStateInfo = () => {
    if (!result) return null;

    switch (result.state) {
      case "ANSWER":
        return {
          icon: "✓",
          title: "Answer",
          subtitle: "Grounded in the rulebook",
          className: "answer",
        };

      case "CONTRADICTION":
        return {
          icon: "!",
          title: "Contradiction Detected",
          subtitle: "Conflicting rules found",
          className: "contradiction",
        };

      case "NO_EVIDENCE":
        return {
          icon: "−",
          title: "No Evidence",
          subtitle: "Not covered by the rulebook",
          className: "no-evidence",
        };

      default:
        return {
          icon: "!",
          title: "Error",
          subtitle: "Something went wrong",
          className: "error",
        };
    }
  };

  const stateInfo = getStateInfo();

  return (
    <div className="app">

      {/* HEADER */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">▱</div>
          <div>
            <h1>Rulebook AI</h1>
            <span>University Rulebook Assistant</span>
          </div>
        </div>

        <div className="institution">
          <span>⌂</span>
          SGSITS, Indore
        </div>
      </header>


      <div className="layout">

        {/* SIDEBAR */}
        <aside className="sidebar">

          <div className="nav-item active">
            <span>⌕</span>
            Ask Rulebook
          </div>

          <div className="nav-item">
            <span>▤</span>
            View Sources
          </div>

          <div className="nav-item">
            <span>◷</span>
            Chat History
          </div>

          <div className="nav-item">
            <span>ⓘ</span>
            About
          </div>

          <div className="sidebar-bottom">
            <div className="coffee-cup"></div>
            <p>Better answers.</p>
            <p>From the right rules.</p>
          </div>

        </aside>


        {/* MAIN */}
        <main className="main">

          {/* HERO / SEARCH */}
          <section className="hero">

            <div className="hero-decoration">
              ▱
            </div>

            <div className="hero-content">
              <h2>Ask the Rulebook</h2>

              <p>
                Get answers grounded exclusively in the university
                rulebook.
              </p>

              <div className="search-box">

                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask a question about university rules..."
                  rows="2"
                />

                <button
                  className="ask-button"
                  onClick={askQuestion}
                  disabled={loading || !question.trim()}
                >
                  {loading ? "..." : "➤"}
                </button>

              </div>

              <div className="example">
                ✦ Example: What is the minimum attendance requirement?
              </div>

            </div>
          </section>


          {/* EMPTY STATE */}
          {!result && !loading && (
            <section className="welcome-card">

              <div className="welcome-icon">▱</div>

              <h3>Ask about university regulations</h3>

              <p>
                Rulebook AI searches the provided rulebook and identifies
                whether the evidence supports an answer, contains a
                contradiction, or does not cover your question.
              </p>

              <div className="state-preview">

                <div className="mini-state answer">
                  <strong>✓</strong>
                  <div>
                    <b>Answer</b>
                    <span>Evidence found</span>
                  </div>
                </div>

                <div className="mini-state contradiction">
                  <strong>!</strong>
                  <div>
                    <b>Contradiction</b>
                    <span>Conflicting evidence</span>
                  </div>
                </div>

                <div className="mini-state no-evidence">
                  <strong>−</strong>
                  <div>
                    <b>No Evidence</b>
                    <span>Question not covered</span>
                  </div>
                </div>

              </div>

            </section>
          )}


          {/* LOADING */}
          {loading && (
            <section className="result-card loading-card">

              <div className="loading-icon">
                ✦
              </div>

              <h3>Searching the rulebook...</h3>

              <p>
                Retrieving relevant passages and checking the evidence.
              </p>

              <div className="loading-line">
                <div></div>
              </div>

            </section>
          )}


          {/* RESULT */}
          {result && !loading && stateInfo && (

            <section className={`result-card ${stateInfo.className}`}>

              {/* RESULT HEADER */}
              <div className="result-header">

                <div className={`state-icon ${stateInfo.className}`}>
                  {stateInfo.icon}
                </div>

                <div>
                  <div className="result-state">
                    {stateInfo.title}
                  </div>

                  <div className="result-subtitle">
                    {stateInfo.subtitle}
                  </div>
                </div>

              </div>


              {/* ANSWER */}
              <div className="answer-section">

                <h3>
                  {result.state === "CONTRADICTION"
                    ? "What we found"
                    : "Response"}
                </h3>

                <p className="answer-text">
                  {result.answer}
                </p>

              </div>


              {/* CONTRADICTIONS */}
              {result.state === "CONTRADICTION" &&
                result.conflicts?.length > 0 && (

                  <div className="evidence-section">

                    <div className="section-title">
                      <span>⚠</span>
                      Conflicting Evidence
                    </div>

                    <div className="conflict-grid">

                      {result.conflicts.map((conflict, index) => (

                        <div
                          className="conflict-card"
                          key={index}
                        >

                          <div className="source-top">
                            <span className="document-icon">
                              ▤
                            </span>

                            <div>
                              <strong>
                                {conflict.source || "Rulebook"}
                              </strong>

                              <span>
                                {conflict.section ||
                                  conflict.page ||
                                  "Source passage"}
                              </span>
                            </div>
                          </div>

                          <div className="conflict-text">
                            {conflict.quote ||
                              conflict.text ||
                              conflict.claim ||
                              JSON.stringify(conflict)}
                          </div>

                        </div>

                      ))}

                    </div>

                  </div>
                )}


              {/* CITATIONS */}
              {result.citations?.length > 0 && (

                <div className="evidence-section">

                  <div className="section-title">
                    <span>▤</span>
                    Sources
                  </div>

                  <div className="citation-list">

                    {result.citations.map((citation, index) => (

                      <div className="citation" key={index}>

                        <div className="citation-icon">
                          ▤
                        </div>

                        <div className="citation-info">

                          <strong>
                            {citation.source ||
                              citation.document ||
                              "Rulebook"}
                          </strong>

                          <span>
                            {citation.section ||
                              citation.page ||
                              "Source passage"}
                          </span>

                        </div>

                        {citation.page && (
                          <span className="page-badge">
                            Page {citation.page}
                          </span>
                        )}

                      </div>

                    ))}

                  </div>

                </div>
              )}


              {/* RETRIEVED EVIDENCE */}
              {result.state === "ANSWER" &&
                result.retrieved?.length > 0 && (

                  <details className="retrieved">

                    <summary>
                      <span>
                        Retrieved evidence
                      </span>

                      <span className="retrieved-count">
                        {result.retrieved.length}
                      </span>
                    </summary>

                    <div className="retrieved-list">

                      {result.retrieved.map((item, index) => (

                        <div
                          className="retrieved-item"
                          key={index}
                        >

                          <div>
                            <strong>
                              {item.source}
                            </strong>

                            <span>
                              {item.section ||
                                `Page ${item.page || "-"}`}
                            </span>
                          </div>

                          <span className="score">
                            {Number(item.score).toFixed(2)}
                          </span>

                        </div>

                      ))}

                    </div>

                  </details>
                )}

            </section>
          )}


          {/* BOTTOM QUESTION */}
          {result && !loading && (
            <div className="ask-again">

              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask another question..."
              />

              <button
                onClick={askQuestion}
                disabled={!question.trim()}
              >
                ➤
              </button>

            </div>
          )}

        </main>


        {/* RIGHT PANEL */}
        <aside className="right-panel">

          <div className="panel-card">

            <h3>Query Status</h3>

            {!stateInfo ? (
              <div className="status-idle">
                <div className="idle-icon">?</div>

                <div>
                  <strong>Ready</strong>
                  <span>Waiting for your question</span>
                </div>
              </div>
            ) : (
              <div className={`status-display ${stateInfo.className}`}>

                <div className="status-icon">
                  {stateInfo.icon}
                </div>

                <div>
                  <strong>{stateInfo.title}</strong>
                  <span>{stateInfo.subtitle}</span>
                </div>

              </div>
            )}

          </div>


          <div className="panel-card">

            <h3>What it checks</h3>

            <div className="check-item">
              <span className="check green">✓</span>
              Grounded answers
            </div>

            <div className="check-item">
              <span className="check red">!</span>
              Contradictions
            </div>

            <div className="check-item">
              <span className="check yellow">−</span>
              Missing evidence
            </div>

          </div>


          <div className="panel-card about-card">

            <div className="about-icon">
              ▱
            </div>

            <h3>About Rulebook AI</h3>

            <p>
              A checkable RAG system designed to answer questions
              using only the supplied university rulebook.
            </p>

            <div className="tech-tags">
              <span>RAG</span>
              <span>Python</span>
              <span>Gemini</span>
              <span>React</span>
            </div>

          </div>

        </aside>

      </div>

    </div>
  );
}

export default App;