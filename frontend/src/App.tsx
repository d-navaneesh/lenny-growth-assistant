import { useEffect, useMemo, useState } from 'react'
import { AlertCircle, ArrowUpRight, BookText, BrainCircuit, LayoutPanelTop, MessageSquareText, Plus, SendHorizonal, Sparkles, Wand2 } from 'lucide-react'
import { marked } from 'marked'
import './App.css'

const API_BASE = 'http://localhost:8000/api/v1'

type Session = {
  id: number
  title: string
  owner: string | null
  updated_at: string
}

type Message = {
  id: number
  role: string
  content: string
  provider?: string
  model?: string
  timestamp?: string
}

type Evidence = {
  source_title: string
  excerpt: string
  score?: number
  url?: string
  chunk_id?: number
}

type Artifact = {
  id: number
  title: string
  type: string
  content: string
}

function buildSafeArtifactHtml(body: string) {
  return `<!doctype html><html><head><meta charset="utf-8" /><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline';" /><style>body{font-family:ui-sans-serif,system-ui,sans-serif;background:#f7f5f1;color:#1c1b1a;line-height:1.6;padding:32px;max-width:720px;margin:0 auto} h1,h2,h3{color:#1b2a1d} a{color:#2a6d4f} code{background:#edead8;padding:2px 6px;border-radius:4px} pre{background:#1b1b1b;color:#f6f5f3;padding:16px;border-radius:12px;overflow:auto}</style></head><body>${body}</body></html>`
}

function App() {
  const [sessions, setSessions] = useState<Session[]>([])
  const [selectedSessionId, setSelectedSessionId] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [evidence, setEvidence] = useState<Evidence[]>([])
  const [prompt, setPrompt] = useState('How should an early-stage startup find product-market fit?')
  const [status, setStatus] = useState('Local demo ready')
  const [config, setConfig] = useState({ provider: 'ollama', model: 'llama3.2:3b' })
  const [artifact, setArtifact] = useState<Artifact | null>(null)
  const [sourceList, setSourceList] = useState<any[]>([])

  const loadSessions = async () => {
    const response = await fetch(`${API_BASE}/sessions`)
    const payload = await response.json()
    setSessions(payload.items ?? [])
    if (!selectedSessionId && payload.items?.[0]) {
      setSelectedSessionId(payload.items[0].id)
    }
  }

  const loadSources = async () => {
    const response = await fetch(`${API_BASE}/sources`)
    const payload = await response.json()
    setSourceList(payload.items ?? [])
  }

  const loadConfig = async () => {
    const response = await fetch(`${API_BASE}/config/public`)
    const payload = await response.json()
    setConfig({ provider: payload.provider ?? 'ollama', model: payload.model ?? 'llama3.2:3b' })
  }

  useEffect(() => {
    void loadSessions()
    void loadConfig()
    void loadSources()
  }, [])

  useEffect(() => {
    if (!selectedSessionId) return
    const fetchMessages = async () => {
      const response = await fetch(`${API_BASE}/sessions/${selectedSessionId}/messages`)
      const payload = await response.json()
      setMessages(payload.items ?? [])
    }
    void fetchMessages()
  }, [selectedSessionId])

  const createNewSession = async () => {
    const response = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'New conversation', owner: 'demo-user' }),
    })
    const created = await response.json()
    await loadSessions()
    setSelectedSessionId(created.id)
  }

  const generateArtifact = async () => {
    const draft = messages.at(-1)?.content ?? 'Growth brief draft'
    const response = await fetch(`${API_BASE}/artifacts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: selectedSessionId,
        title: 'Growth Brief',
        artifact_type: 'markdown',
        content: `# Growth Brief\n\n${draft}\n\n## Evidence\n\n${evidence.map((item) => `- ${item.source_title}: ${item.excerpt}`).join('\n')}`,
      }),
    })
    const payload = await response.json()
    if (response.ok) {
      setArtifact({ id: payload.id, title: payload.title, type: payload.type, content: payload.content ?? '' })
      setStatus('Artifact generated and stored')
    }
  }

  const submitPrompt = async () => {
    if (!prompt.trim()) return
    setStatus('Generating response…')
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: selectedSessionId, prompt, provider: config.provider, model: config.model }),
    })
    const payload = await response.json()
    if (!response.ok) {
      setStatus(payload.detail ?? 'Request failed')
      return
    }
    setMessages((current) => [...current, { id: Date.now(), role: 'user', content: prompt }, { id: Date.now() + 1, role: 'assistant', content: payload.response, provider: payload.provider, model: payload.model }])
    setEvidence(payload.evidence ?? [])
    setPrompt('')
    setStatus(`Answer ready via ${payload.provider} / ${payload.model}`)
  }

  const previewHtml = useMemo(() => {
    if (!artifact) return ''
    const html = marked.parse(artifact.content || '') as string
    return buildSafeArtifactHtml(html)
  }, [artifact])

  return (
    <div className="workspace-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">LG</div>
          <div>
            <div className="brand-name">Lenny Growth Assistant</div>
            <div className="brand-tag">Growth Intelligence Workspace</div>
          </div>
        </div>

        <button className="new-chat" onClick={createNewSession}>
          <Plus size={16} />
          New conversation
        </button>

        <div className="side-section">
          <div className="section-label">Recent</div>
          <div className="session-list">
            {sessions.map((session) => (
              <button key={session.id} className={`session-item ${selectedSessionId === session.id ? 'active' : ''}`} onClick={() => setSelectedSessionId(session.id)}>
                <MessageSquareText size={14} />
                <span>{session.title}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="side-section status-grid">
          <div className="section-label">Knowledge base</div>
          <div className="mini-pill success">{sourceList.length} sources</div>
          <div className="section-label">Model status</div>
          <div className="mini-pill neutral">{config.provider}</div>
          <div className="mini-pill neutral">{config.model}</div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <div className="eyebrow">AI product + growth workspace</div>
            <h1>Ask grounded product questions</h1>
          </div>
          <div className="status-pill">
            <Sparkles size={14} />
            {status}
          </div>
        </header>

        <div className="content-grid">
          <section className="chat-panel">
            <div className="prompt-row">
              {['How should an early-stage startup find product-market fit?', 'What are the biggest mistakes when scaling a product?', 'Turn these insights into a Ship 30 for 30 essay.'].map((sample) => (
                <button key={sample} className="starter-prompt" onClick={() => setPrompt(sample)}>{sample}</button>
              ))}
            </div>

            <div className="message-list">
              {messages.length === 0 ? (
                <div className="empty-state">
                  <BrainCircuit size={28} />
                  <h3>Grounded answers, sources, and experiments.</h3>
                  <p>Use source-backed reasoning to turn product ideas into concrete next steps.</p>
                </div>
              ) : (
                messages.map((message) => (
                  <article key={message.id} className={`message ${message.role}`}>
                    <div className="author-label">{message.role === 'assistant' ? 'Assistant' : 'You'}</div>
                    <div className="message-body" dangerouslySetInnerHTML={{ __html: marked.parse(message.content) as string }} />
                  </article>
                ))
              )}
            </div>

            <div className="composer">
              <textarea value={prompt} onChange={(event) => setPrompt(event.target.value)} rows={3} placeholder="Ask a grounded product or growth question..." />
              <div className="composer-actions">
                <button className="secondary" onClick={generateArtifact}>Turn into artifact</button>
                <button className="primary" onClick={submitPrompt}>
                  <SendHorizonal size={16} />
                  Send
                </button>
              </div>
            </div>
          </section>

          <aside className="right-panel">
            <div className="panel-card">
              <div className="card-header">
                <BookText size={16} />
                <span>Evidence explorer</span>
              </div>
              <div className="evidence-list">
                {evidence.length === 0 ? <p className="faint">No retrieved passages yet.</p> : evidence.map((item, index) => (
                  <div key={`${item.source_title}-${index}`} className="evidence-item">
                    <div className="evidence-header">
                      <strong>{item.source_title}</strong>
                      <span>rank {index + 1}</span>
                    </div>
                    <p>{item.excerpt}</p>
                    {item.url ? <a href={item.url} target="_blank" rel="noreferrer">Source <ArrowUpRight size={12} /></a> : null}
                  </div>
                ))}
              </div>
            </div>

            <div className="panel-card">
              <div className="card-header">
                <LayoutPanelTop size={16} />
                <span>Model control center</span>
              </div>
              <div className="model-row">
                <span>Provider</span>
                <b>{config.provider}</b>
              </div>
              <div className="model-row">
                <span>Model</span>
                <b>{config.model}</b>
              </div>
              <div className="model-row">
                <span>State</span>
                <b>Local-first demo</b>
              </div>
            </div>

            <div className="panel-card">
              <div className="card-header">
                <Wand2 size={16} />
                <span>Artifact canvas</span>
              </div>
              {artifact ? (
                <div className="artifact-preview">
                  <iframe title="artifact-preview" sandbox="" srcDoc={previewHtml} />
                </div>
              ) : (
                <div className="empty-artifact">
                  <AlertCircle size={16} />
                  Generate a draft artifact from the latest answer.
                </div>
              )}
            </div>
          </aside>
        </div>
      </main>
    </div>
  )
}

export default App
