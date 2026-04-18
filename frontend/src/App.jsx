import { useState, useEffect, useRef } from "react";

const API = "http://localhost:5000/api";

// ── Wikipedia Summary Card ────────────────────────────────────────────────
function WikiSummaryCard({ summary, topic, dark, border, muted }) {
  const [open, setOpen] = useState(true);
  return (
    <div style={{
      background: dark ? "#0f2d1f" : "#f0fdf4",
      border: `1.5px solid ${dark ? "#166534" : "#86efac"}`,
      borderRadius: 14, marginBottom: 22, overflow: "hidden",
      transition: "all 0.3s",
    }}>
      {/* Header row */}
      <button onClick={() => setOpen(!open)} style={{
        width: "100%", display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "12px 18px", background: "transparent", border: "none", cursor: "pointer",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 20 }}>📖</span>
          <div style={{ textAlign: "left" }}>
            <div style={{ fontWeight: 700, fontSize: 14, color: dark ? "#86efac" : "#166534" }}>
              Study Note: {topic}
            </div>
            <div style={{ fontSize: 11, color: muted }}>Wikipedia summary · Read before answering</div>
          </div>
        </div>
        <span style={{ fontSize: 18, color: dark ? "#86efac" : "#166534", transition: "transform 0.2s", transform: open ? "rotate(180deg)" : "rotate(0deg)" }}>▾</span>
      </button>

      {/* Collapsible body */}
      {open && (
        <div style={{
          padding: "0 18px 16px 18px",
          fontSize: 13.5, lineHeight: 1.75,
          color: dark ? "#bbf7d0" : "#14532d",
          borderTop: `1px solid ${dark ? "#166534" : "#bbf7d0"}`,
          paddingTop: 14,
          animation: "fadeIn 0.2s ease",
        }}>
          {summary}
        </div>
      )}
    </div>
  );
}

const AGENTS = [
  { id: "coordinator",    name: "Coordinator",    student: "Student A", icon: "🎓", color: "#6366f1", role: "Validates topic & fetches Wikipedia summary",      tool: "wikipedia_topic_fetcher" },
  { id: "quiz_generator", name: "Quiz Generator", student: "Student B", icon: "✏️", color: "#0891b2", role: "Generates 5 MCQ questions from topic summary",       tool: "save_quiz_to_file"       },
  { id: "grader",         name: "Grader",         student: "Student C", icon: "📊", color: "#059669", role: "Scores student answers against the answer key",      tool: "score_student_answers"   },
  { id: "report_writer",  name: "Report Writer",  student: "Student D", icon: "📄", color: "#d97706", role: "Compiles final graded report to disk",               tool: "write_final_report"      },
];

// ── Theme hook ──────────────────────────────────────────────────────────────
function useTheme() {
  const [dark, setDark] = useState(() => window.matchMedia("(prefers-color-scheme: dark)").matches);
  useEffect(() => {
    const mq = window.matchMedia("(prefers-color-scheme: dark)");
    const h = (e) => setDark(e.matches);
    mq.addEventListener("change", h);
    return () => mq.removeEventListener("change", h);
  }, []);
  return [dark, setDark];
}

// ── Agent card ───────────────────────────────────────────────────────────────
function AgentCard({ agent, status, dark }) {
  const statusColor = status === "done" ? "#22c55e" : status === "running" ? agent.color : "#94a3b8";
  const statusLabel = status === "done" ? "Complete" : status === "running" ? "Running…" : "Waiting";
  return (
    <div style={{
      background: dark ? "#1e293b" : "#fff",
      border: `1.5px solid ${status === "running" ? agent.color : dark ? "#334155" : "#e2e8f0"}`,
      borderRadius: 14, padding: "18px 20px", display: "flex", alignItems: "center", gap: 16,
      transition: "border-color 0.3s, box-shadow 0.3s",
      boxShadow: status === "running" ? `0 0 0 3px ${agent.color}28` : "none",
      position: "relative", overflow: "hidden",
    }}>
      {status === "running" && (
        <div style={{ position: "absolute", top: 0, left: 0, height: 3, background: agent.color, animation: "progressBar 2s ease-in-out infinite", borderRadius: "14px 0 0 0", width: "60%" }} />
      )}
      <div style={{ fontSize: 28, lineHeight: 1 }}>{agent.icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 2 }}>
          <span style={{ fontWeight: 700, fontSize: 15, color: dark ? "#f1f5f9" : "#0f172a" }}>{agent.name}</span>
          <span style={{ fontSize: 11, color: dark ? "#94a3b8" : "#64748b", background: dark ? "#334155" : "#f1f5f9", borderRadius: 99, padding: "1px 8px" }}>{agent.student}</span>
        </div>
        <div style={{ fontSize: 12, color: dark ? "#94a3b8" : "#64748b", marginBottom: 4 }}>{agent.role}</div>
        <div style={{ fontSize: 11, color: agent.color, fontFamily: "monospace", background: dark ? "#0f172a" : "#f8fafc", borderRadius: 6, padding: "2px 8px", display: "inline-block" }}>
          🔧 {agent.tool}
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 4 }}>
        <div style={{ width: 10, height: 10, borderRadius: "50%", background: statusColor, boxShadow: status === "running" ? `0 0 6px ${statusColor}` : "none", transition: "background 0.3s" }} />
        <span style={{ fontSize: 11, color: statusColor, fontWeight: 600 }}>{statusLabel}</span>
      </div>
    </div>
  );
}

// ── Quiz Question ────────────────────────────────────────────────────────────
function QuizQuestion({ q, idx, selected, onSelect, showAnswer, dark }) {
  return (
    <div style={{ marginBottom: 22 }}>
      <div style={{ fontWeight: 600, fontSize: 14, color: dark ? "#e2e8f0" : "#1e293b", marginBottom: 10 }}>
        Q{idx + 1}. {q.question}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
        {Object.entries(q.options).map(([key, val]) => {
          const isSelected = selected === key;
          const isCorrect  = key === q.answer;
          let bg     = dark ? "#1e293b" : "#f8fafc";
          let border = dark ? "#334155" : "#e2e8f0";
          let color  = dark ? "#cbd5e1" : "#475569";
          if (isSelected && !showAnswer) { bg = "#6366f128"; border = "#6366f1"; color = "#6366f1"; }
          if (showAnswer && isCorrect)    { bg = "#22c55e18"; border = "#22c55e"; color = "#16a34a"; }
          if (showAnswer && isSelected && !isCorrect) { bg = "#ef444418"; border = "#ef4444"; color = "#dc2626"; }
          return (
            <button key={key} onClick={() => !showAnswer && onSelect(idx, key)}
              style={{ background: bg, border: `1.5px solid ${border}`, borderRadius: 10, padding: "10px 14px", cursor: showAnswer ? "default" : "pointer", textAlign: "left", transition: "all 0.2s", display: "flex", alignItems: "center", gap: 8 }}>
              <span style={{ fontWeight: 700, fontSize: 13, color: border, minWidth: 20 }}>{key}</span>
              <span style={{ fontSize: 13, color }}>{val}</span>
              {showAnswer && isCorrect && <span style={{ marginLeft: "auto", fontSize: 14 }}>✅</span>}
              {showAnswer && isSelected && !isCorrect && <span style={{ marginLeft: "auto", fontSize: 14 }}>❌</span>}
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ── Score Ring ───────────────────────────────────────────────────────────────
function ScoreRing({ pct, dark }) {
  const r = 52, c = 2 * Math.PI * r;
  const offset = c - (pct / 100) * c;
  const color  = pct >= 60 ? "#22c55e" : "#ef4444";
  return (
    <svg width={130} height={130} viewBox="0 0 130 130">
      <circle cx={65} cy={65} r={r} fill="none" stroke={dark ? "#334155" : "#e2e8f0"} strokeWidth={10} />
      <circle cx={65} cy={65} r={r} fill="none" stroke={color} strokeWidth={10}
        strokeDasharray={c} strokeDashoffset={offset}
        strokeLinecap="round" transform="rotate(-90 65 65)"
        style={{ transition: "stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)" }} />
      <text x={65} y={60} textAnchor="middle" fontSize={22} fontWeight={800} fill={dark ? "#f1f5f9" : "#0f172a"}>{pct}%</text>
      <text x={65} y={80} textAnchor="middle" fontSize={11} fill={color} fontWeight={700}>{pct >= 60 ? "PASS" : "FAIL"}</text>
    </svg>
  );
}

// ── Log Viewer ───────────────────────────────────────────────────────────────
function LogViewer({ logs, dark }) {
  const ref = useRef(null);
  useEffect(() => { if (ref.current) ref.current.scrollTop = ref.current.scrollHeight; }, [logs]);
  const getColor = (line) => {
    if (line.includes("[START]"))    return "#6366f1";
    if (line.includes("[END]"))      return "#22c55e";
    if (line.includes("[TOOL]"))     return "#f59e0b";
    if (line.includes("[RESULT]"))   return "#0891b2";
    if (line.includes("[STATE]"))    return "#a855f7";
    if (line.includes("[ERROR]"))    return "#ef4444";
    if (line.includes("[PIPELINE"))  return "#f1f5f9";
    if (line.includes("✅"))          return "#22c55e";
    if (line.includes("❌"))          return "#ef4444";
    return dark ? "#94a3b8" : "#64748b";
  };
  return (
    <div ref={ref} style={{ background: dark ? "#0f172a" : "#1e293b", borderRadius: 12, padding: "14px 16px", height: 220, overflowY: "auto", fontFamily: "monospace", fontSize: 11.5, lineHeight: 1.8 }}>
      {logs.length === 0 && <span style={{ color: "#475569" }}>// Waiting for pipeline to start…</span>}
      {logs.map((line, i) => (
        <div key={i} style={{ color: getColor(line), wordBreak: "break-all" }}>
          <span style={{ color: "#475569", marginRight: 8 }}>{String(i + 1).padStart(3, "0")}</span>
          {line}
        </div>
      ))}
    </div>
  );
}

// ── Main App ─────────────────────────────────────────────────────────────────
export default function App() {
  const [dark, setDark] = useTheme();

  // Pipeline config
  const [topic,       setTopic]       = useState("Photosynthesis");
  const [difficulty,  setDifficulty]  = useState("medium");
  const [studentName, setStudentName] = useState("Alice Fernando");

  // Pipeline state
  const [phase,         setPhase]         = useState("idle"); // idle | fetching_quiz | quiz_ready | running | done | error
  const [agentStatuses, setAgentStatuses] = useState(["idle","idle","idle","idle"]);
  const [logs,          setLogs]          = useState([]);
  const [errorMsg,      setErrorMsg]      = useState("");

  // Quiz + answers
  const [quiz,        setQuiz]        = useState(null);
  const [wikiSummary, setWikiSummary] = useState("");  // Wikipedia summary
  const [answers,     setAnswers]     = useState({});
  const [showAnswer,  setShowAnswer]  = useState(false);

  // Results
  const [score,  setScore]  = useState(null);
  const [report, setReport] = useState(null);

  // Tabs
  const [activeTab, setActiveTab] = useState("pipeline");

  const addLog = (msg) => setLogs((l) => [...l, msg]);

  // ── Step 1: Fetch quiz from backend ────────────────────────────────────────
  const fetchQuiz = async () => {
    if (!topic.trim()) { alert("Please enter a topic."); return; }
    setPhase("fetching_quiz");
    setQuiz(null);
    setWikiSummary("");
    setAnswers({});
    setShowAnswer(false);
    setScore(null);
    setReport(null);
    setLogs([]);
    setErrorMsg("");
    setAgentStatuses(["running","idle","idle","idle"]);
    addLog("[PIPELINE] Generating quiz from backend…");
    addLog(`[CONFIG] Topic="${topic}" | Difficulty="${difficulty}" | Student="${studentName}"`);

    try {
      // Step 1: Fetch Wikipedia summary immediately (fast, no LLM)
      addLog(`[TOOL]  Tool=wikipedia_topic_fetcher | Fetching summary for "${topic}"…`);
      const wikiRes = await fetch(`${API}/wiki?topic=${encodeURIComponent(topic)}`);
      if (wikiRes.ok) {
        const wikiData = await wikiRes.json();
        setWikiSummary(wikiData.summary || "");
        addLog(`[RESULT] Tool=wikipedia_topic_fetcher | Fetched ${(wikiData.summary || "").length} chars.`);
      }
      addLog(`[STATE] Coordinator → QuizGenerator | Keys=['topic_summary']`);
      const res = await fetch(`${API}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, difficulty, student_name: studentName, answers: "A,A,A,A,A" }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Backend error");
      }

      const data = await res.json();
      setQuiz(data.quiz);
      if (data.wiki_summary) setWikiSummary(data.wiki_summary);
      setAgentStatuses(["done","done","idle","idle"]);
      addLog("[RESULT] Quiz generated: 5 questions ready.");
      addLog("[STATE] → Waiting for student answers…");
      setPhase("quiz_ready");
      setActiveTab("quiz");

    } catch (e) {
      setAgentStatuses(["idle","idle","idle","idle"]);
      setErrorMsg(e.message);
      setPhase("error");
      addLog(`[ERROR] ${e.message}`);
    }
  };

  // ── Step 2: Submit answers → run grader + report writer ────────────────────
  const submitAnswers = async () => {
    if (!quiz) return;
    const answered = Object.keys(answers).length;
    if (answered < quiz.length) {
      alert(`Please answer all ${quiz.length} questions. (${answered}/${quiz.length} done)`);
      return;
    }

    const answerStr = quiz.map((_, i) => answers[i] || "A").join(",");

    setPhase("running");
    setAgentStatuses(["done","done","running","idle"]);
    setLogs([]);
    addLog("[PIPELINE START] ======================================");
    addLog(`[CONFIG] Topic="${topic}" | Student="${studentName}" | Answers="${answerStr}"`);
    addLog("[TOOL]  Tool=score_student_answers | Running…");

    try {
      const res = await fetch(`${API}/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic, difficulty, student_name: studentName, answers: answerStr }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.error || "Backend error");
      }

      const data = await res.json();

      // Update quiz with freshly generated one (may differ from placeholder run)
      setQuiz(data.quiz);
      if (data.wiki_summary) setWikiSummary(data.wiki_summary);

      const pct     = data.score.score_percentage;
      const correct = data.score.correct_count;
      const total   = data.score.total_questions;
      const pass    = pct >= 60;

      addLog(`[RESULT] Tool=score_student_answers | Score=${pct}% (${correct}/${total})`);
      setAgentStatuses(["done","done","done","running"]);

      addLog(`[TOOL]  Tool=write_final_report | Args={topic:"${topic}", student:"${studentName}"}`);
      addLog(`[RESULT] Report saved to output/${data.report_file} | Status=${pass ? "PASS" : "FAIL"}`);
      addLog(`[PIPELINE END] Score=${pct}% | Status=${pass ? "PASS" : "FAIL"}`);
      addLog(`[PIPELINE END] ======================================`);
      addLog(`✅ Pipeline complete!`);

      setAgentStatuses(["done","done","done","done"]);
      setScore({ pct, correct, total, pass, reportFile: data.report_file });
      setReport(data.report);
      setShowAnswer(true);
      setPhase("done");
      setActiveTab("results");

    } catch (e) {
      setAgentStatuses(["done","done","idle","idle"]);
      setErrorMsg(e.message);
      setPhase("error");
      addLog(`[ERROR] ${e.message}`);
    }
  };

  const reset = () => {
    setPhase("idle"); setAgentStatuses(["idle","idle","idle","idle"]);
    setLogs([]); setAnswers({}); setShowAnswer(false);
    setScore(null); setReport(null); setQuiz(null); setWikiSummary(""); setErrorMsg("");
    setActiveTab("pipeline");
  };

  // ── Theme tokens ─────────────────────────────────────────────────────────
  const bg      = dark ? "#0f172a" : "#f8fafc";
  const surface = dark ? "#1e293b" : "#fff";
  const border  = dark ? "#334155" : "#e2e8f0";
  const text    = dark ? "#f1f5f9" : "#0f172a";
  const muted   = dark ? "#94a3b8" : "#64748b";

  const tabs = ["pipeline", "quiz", "results", "logs"];

  return (
    <div style={{ minHeight: "100vh", background: bg, fontFamily: "'Inter','Segoe UI',system-ui,sans-serif", color: text }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        button, input, select { font-family: inherit; cursor: pointer; }
        ::-webkit-scrollbar { width: 6px; } ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #475569; border-radius: 3px; }
        @keyframes progressBar { 0%{width:10%} 50%{width:70%} 100%{width:95%} }
        @keyframes spin { to{transform:rotate(360deg)} }
        @keyframes fadeIn { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
      `}</style>

      {/* ── Header ── */}
      <div style={{ background: surface, borderBottom: `1px solid ${border}`, padding: "16px 24px", display: "flex", alignItems: "center", justifyContent: "space-between", position: "sticky", top: 0, zIndex: 10 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 36, height: 36, borderRadius: 10, background: "linear-gradient(135deg,#6366f1,#0891b2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 18 }}>🧠</div>
          <div>
            <div style={{ fontWeight: 800, fontSize: 17, letterSpacing: -0.3 }}>EduMAS</div>
            <div style={{ fontSize: 11, color: muted }}>Educational Multi-Agent System · SE4010 CTSE</div>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {/* Backend status */}
          <BackendBadge dark={dark} muted={muted} />
          <button onClick={() => setDark(!dark)} style={{ background: dark ? "#334155" : "#f1f5f9", border: "none", borderRadius: 8, padding: "6px 10px", fontSize: 16, color: text }}>
            {dark ? "☀️" : "🌙"}
          </button>
        </div>
      </div>

      <div style={{ maxWidth: 920, margin: "0 auto", padding: "24px 16px" }}>

        {/* ── Tabs ── */}
        <div style={{ display: "flex", gap: 4, marginBottom: 24, background: dark ? "#1e293b" : "#f1f5f9", borderRadius: 12, padding: 4 }}>
          {tabs.map((t) => (
            <button key={t} onClick={() => setActiveTab(t)} style={{
              flex: 1, padding: "8px 0", borderRadius: 9, border: "none", fontWeight: 600, fontSize: 13,
              transition: "all 0.2s", textTransform: "capitalize",
              background: activeTab === t ? (dark ? "#0f172a" : "#fff") : "transparent",
              color: activeTab === t ? text : muted,
              boxShadow: activeTab === t ? "0 1px 4px rgba(0,0,0,0.1)" : "none",
            }}>
              {t === "pipeline" ? "🔄 Pipeline" : t === "quiz" ? "✏️ Quiz" : t === "results" ? "📊 Results" : "🔍 Logs"}
            </button>
          ))}
        </div>

        {/* ══ PIPELINE TAB ══ */}
        {activeTab === "pipeline" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>

            {/* Config */}
            <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 16, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>Pipeline Configuration</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
                <div>
                  <label style={{ fontSize: 12, fontWeight: 600, color: muted, display: "block", marginBottom: 6 }}>Topic</label>
                  <input id="input-topic" value={topic} onChange={(e) => setTopic(e.target.value)} disabled={phase === "running" || phase === "fetching_quiz"}
                    placeholder="e.g. Photosynthesis, Birds, Gravity…"
                    style={{ width: "100%", padding: "9px 12px", borderRadius: 9, border: `1.5px solid ${border}`, background: dark ? "#0f172a" : "#f8fafc", color: text, fontSize: 14 }} />
                </div>
                <div>
                  <label style={{ fontSize: 12, fontWeight: 600, color: muted, display: "block", marginBottom: 6 }}>Difficulty</label>
                  <select id="select-difficulty" value={difficulty} onChange={(e) => setDifficulty(e.target.value)} disabled={phase === "running" || phase === "fetching_quiz"}
                    style={{ width: "100%", padding: "9px 12px", borderRadius: 9, border: `1.5px solid ${border}`, background: dark ? "#0f172a" : "#f8fafc", color: text, fontSize: 14 }}>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
              </div>
              <div>
                <label style={{ fontSize: 12, fontWeight: 600, color: muted, display: "block", marginBottom: 6 }}>Student Name</label>
                <input id="input-student" value={studentName} onChange={(e) => setStudentName(e.target.value)} disabled={phase === "running" || phase === "fetching_quiz"}
                  style={{ width: "100%", padding: "9px 12px", borderRadius: 9, border: `1.5px solid ${border}`, background: dark ? "#0f172a" : "#f8fafc", color: text, fontSize: 14 }} />
              </div>
            </div>

            {/* Error banner */}
            {phase === "error" && (
              <div style={{ background: "#ef444418", border: "1.5px solid #ef4444", borderRadius: 12, padding: "12px 16px", marginBottom: 16, color: "#ef4444", fontSize: 13 }}>
                ❌ <strong>Error:</strong> {errorMsg}
              </div>
            )}

            {/* Agent cards */}
            <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 16, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>Agent Swarm</div>
              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {AGENTS.map((agent, i) => (
                  <AgentCard key={agent.id} agent={agent} status={agentStatuses[i]} dark={dark} />
                ))}
              </div>
            </div>

            {/* State flow */}
            <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20, marginBottom: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 16, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>State Flow</div>
              <div style={{ display: "flex", alignItems: "center", gap: 0, overflowX: "auto" }}>
                {["topic\ndifficulty\nstudent", "topic_summary", "quiz_file_path\nquiz_questions", "scores\nscore_pct", "final_report_path"].map((label, i) => (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 0, flex: i < 4 ? 1 : 0 }}>
                    <div style={{ background: dark ? "#0f172a" : "#f8fafc", border: `1.5px solid ${border}`, borderRadius: 10, padding: "8px 12px", fontSize: 11, fontFamily: "monospace", color: muted, whiteSpace: "pre", minWidth: 100, textAlign: "center" }}>
                      {label}
                    </div>
                    {i < 4 && <div style={{ flex: 1, height: 1.5, background: `linear-gradient(90deg,${AGENTS[i].color},${AGENTS[Math.min(i+1,3)].color})`, margin: "0 4px", position: "relative" }}>
                      <div style={{ position: "absolute", right: -4, top: "50%", transform: "translateY(-50%)", fontSize: 12, color: AGENTS[Math.min(i+1,3)].color }}>▶</div>
                    </div>}
                  </div>
                ))}
              </div>
            </div>

            {/* Action buttons */}
            <div style={{ display: "flex", gap: 12 }}>
              {(phase === "idle" || phase === "error") && (
                <button id="btn-generate-quiz" onClick={fetchQuiz}
                  style={{ flex: 1, padding: "14px 0", borderRadius: 12, border: "none", background: "linear-gradient(135deg,#6366f1,#0891b2)", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                  🚀 Generate Quiz
                </button>
              )}
              {(phase === "fetching_quiz") && (
                <button disabled style={{ flex: 1, padding: "14px 0", borderRadius: 12, border: "none", background: "#475569", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                  ⏳ Generating Quiz via AI…
                </button>
              )}
              {(phase === "quiz_ready") && (
                <button id="btn-go-quiz" onClick={() => setActiveTab("quiz")}
                  style={{ flex: 1, padding: "14px 0", borderRadius: 12, border: "none", background: "linear-gradient(135deg,#059669,#0891b2)", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                  ✏️ Answer Quiz →
                </button>
              )}
              {(phase === "running") && (
                <button disabled style={{ flex: 1, padding: "14px 0", borderRadius: 12, border: "none", background: "#475569", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                  ⏳ Grading & Writing Report…
                </button>
              )}
              {(phase === "done") && (
                <>
                  <button id="btn-view-results" onClick={() => setActiveTab("results")}
                    style={{ flex: 2, padding: "14px 0", borderRadius: 12, border: "none", background: "linear-gradient(135deg,#6366f1,#0891b2)", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                    📊 View Results
                  </button>
                  <button id="btn-reset" onClick={reset}
                    style={{ flex: 1, padding: "14px 0", borderRadius: 12, border: "1.5px solid #ef4444", background: "transparent", color: "#ef4444", fontWeight: 700, fontSize: 15 }}>
                    ↺ Reset
                  </button>
                </>
              )}
            </div>
          </div>
        )}

        {/* ══ QUIZ TAB ══ */}
        {activeTab === "quiz" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            {!quiz ? (
              <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 48, textAlign: "center" }}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>✏️</div>
                <div style={{ fontWeight: 700, fontSize: 17, marginBottom: 8 }}>No quiz generated yet</div>
                <div style={{ color: muted, fontSize: 14, marginBottom: 20 }}>Go to Pipeline tab and click "Generate Quiz" first.</div>
                <button onClick={() => setActiveTab("pipeline")}
                  style={{ padding: "10px 24px", borderRadius: 10, border: "none", background: "linear-gradient(135deg,#6366f1,#0891b2)", color: "#fff", fontWeight: 700 }}>
                  ← Go to Pipeline
                </button>
              </div>
            ) : (
              <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
                  <div>
                    <div style={{ fontWeight: 800, fontSize: 18 }}>Quiz: {topic}</div>
                    <div style={{ fontSize: 13, color: muted, marginTop: 2 }}>Difficulty: {difficulty} · {quiz.length} questions · {studentName}</div>
                  </div>
                  <div style={{ fontSize: 13, color: Object.keys(answers).length === quiz.length ? "#22c55e" : muted, fontWeight: 600 }}>
                    {Object.keys(answers).length}/{quiz.length} answered
                  </div>
                </div>

                {/* Wikipedia summary study note */}
                {wikiSummary && (
                  <WikiSummaryCard summary={wikiSummary} topic={topic} dark={dark} border={border} muted={muted} />
                )}

                {quiz.map((q, i) => (
                  <QuizQuestion key={i} q={q} idx={i}
                    selected={answers[i]}
                    onSelect={(idx, key) => setAnswers({ ...answers, [idx]: key })}
                    showAnswer={showAnswer}
                    dark={dark} />
                ))}

                {!showAnswer && (
                  <button id="btn-submit-answers" onClick={submitAnswers}
                    style={{
                      width: "100%", marginTop: 8, padding: "13px 0", borderRadius: 12, border: "none",
                      background: Object.keys(answers).length === quiz.length
                        ? "linear-gradient(135deg,#6366f1,#0891b2)"
                        : (dark ? "#334155" : "#e2e8f0"),
                      color: Object.keys(answers).length === quiz.length ? "#fff" : muted,
                      fontWeight: 700, fontSize: 15,
                    }}>
                    {phase === "running" ? "⏳ Grading…" : `🎯 Submit & Grade (${Object.keys(answers).length}/${quiz.length})`}
                  </button>
                )}
                {showAnswer && (
                  <button onClick={() => setActiveTab("results")}
                    style={{ width: "100%", marginTop: 8, padding: "13px 0", borderRadius: 12, border: "none", background: "linear-gradient(135deg,#059669,#22c55e)", color: "#fff", fontWeight: 700, fontSize: 15 }}>
                    📊 View Results →
                  </button>
                )}
              </div>
            )}
          </div>
        )}

        {/* ══ RESULTS TAB ══ */}
        {activeTab === "results" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            {!score ? (
              <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 48, textAlign: "center" }}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>📊</div>
                <div style={{ fontWeight: 700, fontSize: 17, marginBottom: 8 }}>No results yet</div>
                <div style={{ color: muted, fontSize: 14 }}>Complete the quiz and submit answers first.</div>
              </div>
            ) : (
              <>
                {/* Score summary card */}
                <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 24, marginBottom: 16, display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" }}>
                  <ScoreRing pct={score.pct} dark={dark} />
                  <div style={{ flex: 1, minWidth: 200 }}>
                    <div style={{ fontWeight: 800, fontSize: 22, marginBottom: 4 }}>{studentName}</div>
                    <div style={{ color: muted, fontSize: 14, marginBottom: 14 }}>Topic: {topic} · {difficulty}</div>
                    <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
                      {[
                        { label: "Correct",  val: `${score.correct}/${score.total}`, color: "#22c55e" },
                        { label: "Score",    val: `${score.pct}%`,                   color: score.pass ? "#22c55e" : "#ef4444" },
                        { label: "Status",   val: score.pass ? "PASS" : "FAIL",      color: score.pass ? "#22c55e" : "#ef4444" },
                        { label: "Threshold",val: "60%",                             color: muted },
                      ].map((s) => (
                        <div key={s.label} style={{ background: dark ? "#0f172a" : "#f8fafc", border: `1.5px solid ${border}`, borderRadius: 10, padding: "8px 16px" }}>
                          <div style={{ fontSize: 11, color: muted, marginBottom: 2 }}>{s.label}</div>
                          <div style={{ fontWeight: 800, fontSize: 18, color: s.color }}>{s.val}</div>
                        </div>
                      ))}
                    </div>
                    <div style={{ marginTop: 14, fontSize: 12, color: muted, fontFamily: "monospace", background: dark ? "#0f172a" : "#f8fafc", borderRadius: 8, padding: "6px 10px", display: "inline-block" }}>
                      📁 output/{score.reportFile}
                    </div>
                  </div>
                </div>

                {/* Question breakdown */}
                {report && (
                  <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 24, marginBottom: 16 }}>
                    <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 16, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>Question Breakdown</div>
                    {report.question_feedback.map((fb, i) => {
                      const ok = fb.result === "Correct";
                      return (
                        <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 14, padding: "12px 0", borderBottom: i < report.question_feedback.length - 1 ? `1px solid ${border}` : "none" }}>
                          <div style={{ width: 28, height: 28, borderRadius: "50%", background: ok ? "#22c55e18" : "#ef444418", border: `1.5px solid ${ok ? "#22c55e" : "#ef4444"}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, flexShrink: 0 }}>
                            {ok ? "✅" : "❌"}
                          </div>
                          <div style={{ flex: 1 }}>
                            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>Q{fb.question_no}. {fb.question}</div>
                            <div style={{ fontSize: 12, color: muted }}>
                              Your answer: <span style={{ color: ok ? "#22c55e" : "#ef4444", fontWeight: 700 }}>{fb.student_answer}</span>
                              {!ok && <> · Correct: <span style={{ color: "#22c55e", fontWeight: 700 }}>{fb.correct_answer}</span></>}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Raw report JSON */}
                {report && (
                  <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20 }}>
                    <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 12, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>Raw Report JSON</div>
                    <pre style={{ background: dark ? "#0f172a" : "#1e293b", color: "#94a3b8", borderRadius: 10, padding: 16, fontSize: 11, overflowX: "auto", fontFamily: "monospace", lineHeight: 1.7 }}>
                      {JSON.stringify(report, null, 2)}
                    </pre>
                  </div>
                )}
              </>
            )}
          </div>
        )}

        {/* ══ LOGS TAB ══ */}
        {activeTab === "logs" && (
          <div style={{ animation: "fadeIn 0.3s ease" }}>
            <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20, marginBottom: 16 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
                <div style={{ fontWeight: 700, fontSize: 13, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>LLMOps / AgentOps Trace Log</div>
                <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                  {[["#6366f1","START"],["#22c55e","END/✅"],["#f59e0b","TOOL"],["#0891b2","RESULT"],["#a855f7","STATE"],["#ef4444","ERROR"]].map(([c,l]) => (
                    <span key={l} style={{ fontSize: 10, padding: "2px 7px", borderRadius: 99, background: `${c}20`, color: c, fontWeight: 700 }}>{l}</span>
                  ))}
                </div>
              </div>
              <LogViewer logs={logs} dark={dark} />
              <div style={{ marginTop: 12, fontSize: 12, color: muted }}>
                📁 Full server-side trace: <code style={{ fontFamily: "monospace", background: dark ? "#0f172a" : "#f8fafc", padding: "2px 6px", borderRadius: 4 }}>logs/agent_trace.log</code>
              </div>
            </div>

            {/* Observability functions legend */}
            <div style={{ background: surface, border: `1px solid ${border}`, borderRadius: 16, padding: 20 }}>
              <div style={{ fontWeight: 700, fontSize: 13, marginBottom: 14, color: muted, textTransform: "uppercase", letterSpacing: 0.5 }}>Observability Functions</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10 }}>
                {[
                  { fn: "log_pipeline_start()", desc: "Marks the start of a full pipeline run" },
                  { fn: "log_agent_start()",    desc: "Logs agent name and input data" },
                  { fn: "log_tool_call()",       desc: "Logs tool name and arguments" },
                  { fn: "log_tool_result()",     desc: "Logs output returned by each tool" },
                  { fn: "log_state_transition()", desc: "Logs state keys passed between agents" },
                  { fn: "crewai_step_callback()", desc: "Auto-hooked into CrewAI step events" },
                ].map((item) => (
                  <div key={item.fn} style={{ background: dark ? "#0f172a" : "#f8fafc", borderRadius: 10, padding: "10px 14px" }}>
                    <div style={{ fontFamily: "monospace", fontSize: 12, color: "#6366f1", fontWeight: 700, marginBottom: 4 }}>{item.fn}</div>
                    <div style={{ fontSize: 12, color: muted }}>{item.desc}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Backend health badge ──────────────────────────────────────────────────────
function BackendBadge({ dark, muted }) {
  const [status, setStatus] = useState("checking"); // checking | ok | error
  useEffect(() => {
    let cancelled = false;
    const check = async () => {
      try {
        const r = await fetch(`${API}/health`, { signal: AbortSignal.timeout(3000) });
        if (!cancelled) setStatus(r.ok ? "ok" : "error");
      } catch { if (!cancelled) setStatus("error"); }
    };
    check();
    const interval = setInterval(check, 10000);
    return () => { cancelled = true; clearInterval(interval); };
  }, []);

  const color = status === "ok" ? "#22c55e" : status === "error" ? "#ef4444" : "#f59e0b";
  const label = status === "ok" ? "API Connected" : status === "error" ? "API Offline" : "Checking…";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 7, fontSize: 11, padding: "4px 12px", borderRadius: 99, background: `${color}18`, color, fontWeight: 600 }}>
      <div style={{ width: 7, height: 7, borderRadius: "50%", background: color, animation: status === "checking" ? "pulse 1s infinite" : "none" }} />
      {label}
    </div>
  );
}
