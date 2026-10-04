import { useRef, useState } from 'react'
import { api, ApiError } from '../api.js'
import Button from '../components/Button.jsx'
import ErrorNote from '../components/ErrorNote.jsx'
import Spinner from '../components/Spinner.jsx'

// Turn "[1]" markers in the answer into interactive pill buttons that jump to the matching source.
function AnswerText({ text, count, onPick }) {
  const parts = text.split(/(\[\d+\])/g)
  return (
    <p className="whitespace-pre-wrap font-serif text-[1.05rem] leading-relaxed text-ink">
      {parts.map((part, i) => {
        const m = part.match(/^\[(\d+)\]$/)
        const n = m ? Number(m[1]) : 0
        if (n >= 1 && n <= count) {
          return (
            <button
              key={i}
              type="button"
              onClick={() => onPick(n)}
              className="inline-flex items-center justify-center mx-1 px-1.5 py-0.2 rounded font-mono text-xs font-semibold bg-accent-soft text-accent hover:bg-accent hover:text-white transition-all cursor-pointer shadow-2xs"
              aria-label={`Jump to source ${n}`}
              title={`Jump to source ${n}`}
            >
              [{n}]
            </button>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </p>
  )
}

export default function Chat() {
  const [question, setQuestion] = useState('')
  const [asked, setAsked] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [active, setActive] = useState(null)
  const [copied, setCopied] = useState(false)
  const sourceRefs = useRef({})

  async function ask(e) {
    e?.preventDefault()
    const q = question.trim()
    if (!q || loading) return
    setLoading(true)
    setError('')
    setResult(null)
    setActive(null)
    setAsked(q)
    setCopied(false)
    try {
      setResult(await api('/api/chat', { method: 'POST', json: { question: q } }))
    } catch (err) {
      setError(
        err instanceof ApiError && err.status === 429
          ? 'You have asked a lot of questions in a short time. Wait about a minute, then ask again.'
          : err.message,
      )
    } finally {
      setLoading(false)
    }
  }

  function copyAnswer() {
    if (!result?.answer) return
    navigator.clipboard.writeText(result.answer)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  function pick(n) {
    setActive(n)
    const el = sourceRefs.current[n]
    if (el) {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
      el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'nearest' })
    }
  }

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6 text-center">
        <h1 className="text-3xl font-serif tracking-tight text-ink">Ask your documents</h1>
        <p className="mt-1.5 text-sm text-muted">
          Answers use only the documents your role is allowed to see.
        </p>
      </div>

      <form onSubmit={ask} className="rounded-lg border border-rule bg-panel p-5 shadow-xs text-left">
        <label htmlFor="question" className="mb-1.5 block text-sm font-medium">
          Your question
        </label>
        <textarea
          id="question"
          rows={3}
          maxLength={1000}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) ask(e)
          }}
          placeholder="For example: How many vacation days do I get?"
          className="w-full rounded border border-rule bg-paper/60 px-3.5 py-2.5 text-sm transition-colors focus:bg-panel focus:border-accent"
        />

        <div className="mt-4 flex items-center justify-between border-t border-rule/60 pt-3">
          <Button type="submit" disabled={loading || !question.trim()}>
            {loading ? 'Searching & answering...' : 'Ask question'}
          </Button>
          <span className="text-xs text-muted font-mono hidden sm:inline">Ctrl + Enter to send</span>
        </div>
      </form>

      <div className="mt-6" aria-live="polite">
        {loading && <Spinner label="Searching vector & text indexes and synthesizing answer" />}
        <ErrorNote>{error}</ErrorNote>

        {result && !result.found && (
          <section className="rounded-lg border border-rule bg-panel p-5 shadow-xs">
            <div className="flex items-center gap-2 text-ink">
              <span className="inline-block h-2.5 w-2.5 rounded-full bg-[#A8741A]"></span>
              <h2 className="text-lg font-serif font-medium">No answer found in your documents</h2>
            </div>
            <p className="mt-2 text-sm text-ink leading-relaxed">
              Nothing in the documents you have access to matches <span className="font-semibold italic">“{asked}”</span>.
            </p>
            <p className="mt-2 text-xs text-muted leading-relaxed border-t border-rule/60 pt-2.5">
              The answer may exist in a document restricted to higher roles, or it may not be present. The LLM was intentionally not called to prevent hallucinations.
            </p>
          </section>
        )}

        {result && result.found && (
          <section className="space-y-5">
            <div className="rounded-lg border border-rule bg-panel p-5 shadow-xs">
              <div className="flex items-center justify-between border-b border-rule/60 pb-3 mb-3">
                <div className="flex items-center gap-2">
                  <span className="inline-block h-2 w-2 rounded-full bg-accent animate-pulse"></span>
                  <span className="font-mono text-xs uppercase tracking-wider text-muted">Answer</span>
                </div>
                <button
                  type="button"
                  onClick={copyAnswer}
                  className="text-xs font-mono text-accent hover:text-accent-dark transition-colors px-2 py-0.5 rounded border border-rule hover:border-accent bg-paper/60 cursor-pointer"
                >
                  {copied ? '✓ Copied' : 'Copy'}
                </button>
              </div>

              <AnswerText text={result.answer} count={result.sources.length} onPick={pick} />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <h2 className="text-lg font-serif font-medium">Cited sources ({result.sources.length})</h2>
                <span className="text-xs text-muted font-mono">Ranked by Hybrid RRF</span>
              </div>
              
              <ol className="space-y-2">
                {result.sources.map((s, i) => (
                  <li
                    key={s.chunk_id}
                    ref={(el) => (sourceRefs.current[i + 1] = el)}
                    className={`rounded-md border p-3 text-sm transition-all ${
                      active === i + 1 
                        ? 'border-accent bg-accent-soft/40 shadow-xs ring-1 ring-accent' 
                        : 'border-rule bg-panel hover:border-muted'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="font-mono text-xs font-semibold text-accent bg-accent-soft px-1.5 py-0.5 rounded">
                          [{i + 1}]
                        </span>
                        <span className="font-medium text-ink truncate">{s.title}</span>
                      </div>
                      <div className="flex items-center gap-2 font-mono text-xs text-muted shrink-0">
                        <span className="bg-paper px-1.5 py-0.5 rounded border border-rule text-[0.7rem]">
                          chunk #{s.chunk_id}
                        </span>
                        <span className="text-accent text-[0.7rem] font-medium">
                          score {s.score.toFixed(4)}
                        </span>
                      </div>
                    </div>
                  </li>
                ))}
              </ol>
            </div>
          </section>
        )}
      </div>
    </div>
  )
}
