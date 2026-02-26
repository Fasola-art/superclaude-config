import { useEffect, useMemo, useRef, useState } from 'react'
import './App.css'

type Mode = 'quiz' | 'health' | 'news'
type Direction = 'up' | 'down' | 'side'
type NewsMove = 'dump' | 'accumulate'
type Difficulty = 'easy' | 'normal' | 'hard'

interface QuizItem {
  id: number
  type: '클러스터 델타' | '볼륨프로파일' | '풋프린트'
  title: string
  truth: Direction
  points: number[]
}

interface HealthMetrics {
  longShortSplit: number
  maAlignment: number
  footprintCvd: number
  clusterDelta: number
  volumeProfile: number
  tpo: number
  vwap: number
}

interface NewsItem {
  id: number
  headline: string
  tone: 'good' | 'bad'
  realMove: NewsMove
}

interface CropRect {
  x: number
  y: number
  w: number
  h: number
}

interface OverlayComment {
  x: number
  y: number
  label: string
  tone: 'bull' | 'bear' | 'warn'
}

const modeTitle: Record<Mode, string> = {
  quiz: '차트 이미지 퀴즈',
  health: '차트 종합건강검진',
  news: '개미를 흔들어라',
}

const quizItems: QuizItem[] = [
  { id: 1, type: '클러스터 델타', title: '고점 델타 피로', truth: 'down', points: [35, 38, 43, 48, 50, 52, 51, 47, 44, 39, 33] },
  { id: 2, type: '볼륨프로파일', title: '밸류 상단 이탈 후 안착', truth: 'up', points: [22, 23, 24, 26, 30, 35, 38, 41, 45, 49, 54] },
  { id: 3, type: '풋프린트', title: '흡수 이후 박스 횡보', truth: 'side', points: [58, 57, 59, 60, 59, 58, 59, 60, 59, 58, 59] },
  { id: 4, type: '클러스터 델타', title: '저점 양봉 누적', truth: 'up', points: [28, 27, 29, 31, 34, 36, 40, 44, 47, 49, 53] },
  { id: 5, type: '볼륨프로파일', title: '밸류 하단 재진입 실패', truth: 'down', points: [62, 60, 58, 57, 55, 53, 50, 47, 45, 41, 38] },
  { id: 6, type: '풋프린트', title: '체결 균형 박스권', truth: 'side', points: [44, 45, 44, 46, 45, 44, 45, 46, 45, 44, 45] },
]

const newsDeckByDifficulty: Record<Difficulty, NewsItem[]> = {
  easy: [
    { id: 1, headline: '금리 인하 기대 뉴스 확산', tone: 'good', realMove: 'dump' },
    { id: 2, headline: '규제 강화 루머 확대', tone: 'bad', realMove: 'accumulate' },
    { id: 3, headline: '기관 매수 보도', tone: 'good', realMove: 'dump' },
  ],
  normal: [
    { id: 1, headline: 'ETF 승인 기대감 급등', tone: 'good', realMove: 'dump' },
    { id: 2, headline: '해킹 사고 속보', tone: 'bad', realMove: 'accumulate' },
    { id: 3, headline: '대형 거래소 상장', tone: 'good', realMove: 'dump' },
    { id: 4, headline: '국세청 조사 뉴스', tone: 'bad', realMove: 'accumulate' },
    { id: 5, headline: '파트너십 체결 발표', tone: 'good', realMove: 'dump' },
  ],
  hard: [
    { id: 1, headline: '호재 뉴스 + 거래량 급감', tone: 'good', realMove: 'dump' },
    { id: 2, headline: '악재 뉴스 + 저점 흡수 증가', tone: 'bad', realMove: 'accumulate' },
    { id: 3, headline: '호재 연속 기사 도배', tone: 'good', realMove: 'dump' },
    { id: 4, headline: '악재 헤드라인 뒤 대량 체결', tone: 'bad', realMove: 'accumulate' },
    { id: 5, headline: '시총 상위 코인 호재 인터뷰', tone: 'good', realMove: 'dump' },
    { id: 6, headline: '규제 불확실성 확대', tone: 'bad', realMove: 'accumulate' },
  ],
}

const rewardByDifficulty: Record<Difficulty, number> = { easy: 2, normal: 3, hard: 5 }
const preRoundsByDifficulty: Record<Difficulty, number> = { easy: 3, normal: 5, hard: 6 }
const QUIZ_TARGET = 10

function linePath(points: number[]) {
  return points.map((p, i) => `${(i / (points.length - 1)) * 100},${100 - p}`).join(' ')
}

function metricLabel(key: keyof HealthMetrics) {
  const map: Record<keyof HealthMetrics, string> = {
    longShortSplit: '4분할 장기/단기',
    maAlignment: '이평선 장기/단기',
    footprintCvd: '풋프린트 + CVD',
    clusterDelta: '클러스터 델타',
    volumeProfile: '볼륨프로파일',
    tpo: 'TPO',
    vwap: 'VWAP',
  }
  return map[key]
}

function cropImageToDataUrl(source: string, crop: CropRect): Promise<string> {
  return new Promise((resolve, reject) => {
    const img = new Image()
    img.onload = () => {
      const sx = (crop.x / 100) * img.width
      const sy = (crop.y / 100) * img.height
      const sw = Math.max(10, (crop.w / 100) * img.width)
      const sh = Math.max(10, (crop.h / 100) * img.height)
      const canvas = document.createElement('canvas')
      canvas.width = Math.max(120, Math.round(sw))
      canvas.height = Math.max(80, Math.round(sh))
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        reject(new Error('canvas context 없음'))
        return
      }
      ctx.drawImage(img, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height)
      resolve(canvas.toDataURL('image/png'))
    }
    img.onerror = reject
    img.src = source
  })
}

function clamp(n: number, min: number, max: number) {
  return Math.max(min, Math.min(max, n))
}

function randomQuizIndex(prev: number) {
  if (quizItems.length <= 1) return 0
  let next = prev
  while (next === prev) {
    next = Math.floor(Math.random() * quizItems.length)
  }
  return next
}

function App() {
  const [mode, setMode] = useState<Mode>('quiz')

  const [quizIndex, setQuizIndex] = useState(0)
  const [guess, setGuess] = useState<Direction | null>(null)
  const [reveal, setReveal] = useState(false)
  const [quizScore, setQuizScore] = useState(0)
  const [quizSolved, setQuizSolved] = useState(0)
  const [bestAccuracy, setBestAccuracy] = useState(0)
  const [quizSessionDone, setQuizSessionDone] = useState(false)

  const [uploadSrc, setUploadSrc] = useState<string | null>(null)
  const [croppedSrc, setCroppedSrc] = useState<string | null>(null)
  const [crop, setCrop] = useState<CropRect>({ x: 8, y: 8, w: 84, h: 72 })
  const [draggingCrop, setDraggingCrop] = useState(false)
  const [dragStart, setDragStart] = useState<{ x: number; y: number } | null>(null)
  const cropStageRef = useRef<HTMLDivElement | null>(null)

  const [healthFee] = useState(3)
  const [metrics, setMetrics] = useState<HealthMetrics>({
    longShortSplit: 58,
    maAlignment: 62,
    footprintCvd: 55,
    clusterDelta: 50,
    volumeProfile: 64,
    tpo: 59,
    vwap: 61,
  })

  const [difficulty, setDifficulty] = useState<Difficulty>('normal')
  const [newsRound, setNewsRound] = useState(1)
  const [newsScore, setNewsScore] = useState(0)
  const [newsCoins, setNewsCoins] = useState(0)
  const [bestCoins, setBestCoins] = useState(0)
  const [newsResult, setNewsResult] = useState('')
  const [newsEnded, setNewsEnded] = useState(false)
  const [combo, setCombo] = useState(0)
  const [bossHp, setBossHp] = useState(6)
  const [bossTurns, setBossTurns] = useState(7)
  const [newsSessions, setNewsSessions] = useState(0)
  const [newsCompleted, setNewsCompleted] = useState(0)

  const currentQuiz = quizItems[quizIndex]
  const cut = Math.floor(currentQuiz.points.length * 0.65)
  const visiblePoints = reveal ? currentQuiz.points : currentQuiz.points.slice(0, cut)

  const quizAccuracy = quizSolved ? Math.round((quizScore / quizSolved) * 100) : 0

  const healthScore = useMemo(() => {
    const values = Object.values(metrics)
    return Math.round(values.reduce((acc, v) => acc + v, 0) / values.length)
  }, [metrics])

  const healthAction = useMemo(() => {
    const trend = metrics.maAlignment + metrics.vwap - metrics.clusterDelta
    if (healthScore >= 70 && trend > 70) return '매수 우선'
    if (healthScore < 45 || trend < 40) return '매도 우선'
    return '관망/짧은 스캘프'
  }, [healthScore, metrics])

  const healthOverlays = useMemo<OverlayComment[]>(() => {
    const items: OverlayComment[] = []
    if (metrics.maAlignment >= 60) items.push({ x: 22, y: 28, label: '장단기 이평 정배열', tone: 'bull' })
    if (metrics.maAlignment < 45) items.push({ x: 20, y: 28, label: '이평 역배열 경고', tone: 'bear' })
    if (metrics.footprintCvd >= 60) items.push({ x: 58, y: 24, label: 'CVD 유입 증가', tone: 'bull' })
    if (metrics.clusterDelta < 40) items.push({ x: 62, y: 52, label: '델타 매도 압력', tone: 'bear' })
    if (metrics.vwap < 45) items.push({ x: 30, y: 62, label: 'VWAP 하회', tone: 'warn' })
    if (metrics.volumeProfile >= 65) items.push({ x: 70, y: 70, label: '밸류 수용 구간', tone: 'bull' })
    return items.slice(0, 4)
  }, [metrics])

  const healthChecklist = useMemo(() => {
    const checks = [
      { label: '장단기 밸런스', value: metrics.longShortSplit },
      { label: '이평 정렬', value: metrics.maAlignment },
      { label: '풋프린트/CVD', value: metrics.footprintCvd },
      { label: '클러스터 델타', value: metrics.clusterDelta },
      { label: '볼륨프로파일', value: metrics.volumeProfile },
      { label: 'TPO', value: metrics.tpo },
      { label: 'VWAP', value: metrics.vwap },
    ]
    return checks.map((c) => ({ ...c, state: c.value >= 60 ? 'PASS' : c.value >= 45 ? 'WARN' : 'RISK' }))
  }, [metrics])

  const preRounds = preRoundsByDifficulty[difficulty]
  const isBossRound = newsRound > preRounds
  const newsDeck = newsDeckByDifficulty[difficulty]
  const currentNews = isBossRound
    ? { id: 999, headline: '보스: 노이즈 뉴스 폭격 구간', tone: 'bad' as const, realMove: 'accumulate' as NewsMove }
    : newsDeck[(newsRound - 1) % newsDeck.length]

  const completionRate = newsSessions ? Math.round((newsCompleted / newsSessions) * 100) : 0

  useEffect(() => {
    const acc = Number(localStorage.getItem('odf_best_acc') ?? '0')
    const coins = Number(localStorage.getItem('odf_best_coins') ?? '0')
    const sessions = Number(localStorage.getItem('odf_news_sessions') ?? '0')
    const completed = Number(localStorage.getItem('odf_news_completed') ?? '0')
    setBestAccuracy(acc)
    setBestCoins(coins)
    setNewsSessions(sessions)
    setNewsCompleted(completed)
  }, [])

  useEffect(() => {
    if (!uploadSrc) {
      setCroppedSrc(null)
      return
    }
    let cancelled = false
    cropImageToDataUrl(uploadSrc, crop)
      .then((data) => {
        if (!cancelled) setCroppedSrc(data)
      })
      .catch(() => {
        if (!cancelled) setCroppedSrc(uploadSrc)
      })
    return () => {
      cancelled = true
    }
  }, [uploadSrc, crop])

  function onUploadFile(file: File | null) {
    if (!file) return
    const reader = new FileReader()
    reader.onload = () => {
      if (typeof reader.result === 'string') setUploadSrc(reader.result)
    }
    reader.readAsDataURL(file)
  }

  function setCropValue(key: keyof CropRect, value: number) {
    setCrop((prev) => ({ ...prev, [key]: value }))
  }

  function handleCropStart(e: React.PointerEvent<HTMLDivElement>) {
    if (!uploadSrc || !cropStageRef.current) return
    const rect = cropStageRef.current.getBoundingClientRect()
    const px = clamp(((e.clientX - rect.left) / rect.width) * 100, 0, 100)
    const py = clamp(((e.clientY - rect.top) / rect.height) * 100, 0, 100)
    setDragStart({ x: px, y: py })
    setDraggingCrop(true)
    setCrop({ x: px, y: py, w: 1, h: 1 })
    e.currentTarget.setPointerCapture(e.pointerId)
  }

  function handleCropMove(e: React.PointerEvent<HTMLDivElement>) {
    if (!draggingCrop || !dragStart || !cropStageRef.current) return
    const rect = cropStageRef.current.getBoundingClientRect()
    const px = clamp(((e.clientX - rect.left) / rect.width) * 100, 0, 100)
    const py = clamp(((e.clientY - rect.top) / rect.height) * 100, 0, 100)
    const x = Math.min(dragStart.x, px)
    const y = Math.min(dragStart.y, py)
    const w = Math.max(4, Math.abs(px - dragStart.x))
    const h = Math.max(4, Math.abs(py - dragStart.y))
    const clampedW = clamp(w, 4, 100 - x)
    const clampedH = clamp(h, 4, 100 - y)
    setCrop({ x, y, w: clampedW, h: clampedH })
  }

  function handleCropEnd(e: React.PointerEvent<HTMLDivElement>) {
    setDraggingCrop(false)
    setDragStart(null)
    if (e.currentTarget.hasPointerCapture(e.pointerId)) {
      e.currentTarget.releasePointerCapture(e.pointerId)
    }
  }

  function submitQuiz(direction: Direction) {
    if (reveal || quizSessionDone) return
    const ok = direction === currentQuiz.truth
    const nextSolved = quizSolved + 1
    const nextScore = ok ? quizScore + 1 : quizScore
    const nextAcc = Math.round((nextScore / nextSolved) * 100)

    setGuess(direction)
    setReveal(true)
    setQuizScore(nextScore)
    setQuizSolved(nextSolved)

    if (nextAcc > bestAccuracy) {
      setBestAccuracy(nextAcc)
      localStorage.setItem('odf_best_acc', String(nextAcc))
    }

    if (nextSolved >= QUIZ_TARGET) {
      setQuizSessionDone(true)
    }
  }

  function nextQuiz() {
    setReveal(false)
    setGuess(null)
    if (quizSolved >= QUIZ_TARGET) {
      setQuizSessionDone(true)
      return
    }
    setQuizIndex((i) => randomQuizIndex(i))
  }

  function resetQuizSession() {
    setQuizScore(0)
    setQuizSolved(0)
    setGuess(null)
    setReveal(false)
    setQuizSessionDone(false)
    setQuizIndex(Math.floor(Math.random() * quizItems.length))
  }

  function updateMetric(key: keyof HealthMetrics, value: number) {
    setMetrics((prev) => ({ ...prev, [key]: value }))
  }

  async function downloadHealthReport() {
    const { jsPDF } = await import('jspdf')
    const doc = new jsPDF({ unit: 'mm', format: 'a4' })
    let y = 12
    doc.setFontSize(16)
    doc.text('Chart Health Report', 14, y)
    y += 8
    doc.setFontSize(11)
    doc.text(`Health Score: ${healthScore}/100`, 14, y)
    y += 6
    doc.text(`Action: ${healthAction}`, 14, y)
    y += 8
    doc.text('Checklist', 14, y)
    y += 6
    healthChecklist.forEach((item) => {
      doc.text(`- ${item.label}: ${item.value} (${item.state})`, 16, y)
      y += 5
    })
    y += 6
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, y)
    doc.save(`chart-health-report-${Date.now()}.pdf`)
  }

  function applyNewsDelta(ok: boolean, comboValue: number) {
    const delta = ok ? rewardByDifficulty[difficulty] + comboValue : -1
    const nextCoins = Math.max(0, newsCoins + delta)
    setNewsCoins(nextCoins)
    if (nextCoins > bestCoins) {
      setBestCoins(nextCoins)
      localStorage.setItem('odf_best_coins', String(nextCoins))
    }
  }

  function closeNewsSession(success: boolean, message: string) {
    setNewsEnded(true)
    setNewsResult(message)
    const nextSessions = newsSessions + 1
    const nextCompleted = newsCompleted + (success ? 1 : 0)
    setNewsSessions(nextSessions)
    setNewsCompleted(nextCompleted)
    localStorage.setItem('odf_news_sessions', String(nextSessions))
    localStorage.setItem('odf_news_completed', String(nextCompleted))
  }

  function playNews(move: NewsMove) {
    if (newsEnded) return
    const ok = move === currentNews.realMove

    if (!isBossRound) {
      const nextCombo = ok ? combo + 1 : 0
      if (ok) {
        setNewsScore((v) => v + 1)
        setNewsResult(`정답: 콤보 x${nextCombo}`)
      } else {
        setNewsResult('오답: 군중심리 추격')
      }
      setCombo(nextCombo)
      applyNewsDelta(ok, nextCombo)

      if (newsRound >= preRounds) {
        setNewsRound(preRounds + 1)
        setNewsResult('보스 라운드 진입! 콤보로 보스를 무너뜨려라')
        return
      }
      setNewsRound((v) => v + 1)
      return
    }

    const nextCombo = ok ? combo + 1 : 0
    const damage = ok ? (nextCombo >= 3 ? 3 : nextCombo >= 2 ? 2 : 1) : 0
    const nextHp = ok ? Math.max(0, bossHp - damage) : bossHp
    const nextTurns = bossTurns - 1

    if (ok) {
      setNewsScore((v) => v + 1)
      setNewsResult(`보스 타격 ${damage} 데미지!`)
    } else {
      setNewsResult('보스 패턴 실패!')
    }

    setCombo(nextCombo)
    setBossHp(nextHp)
    setBossTurns(nextTurns)
    applyNewsDelta(ok, nextCombo)

    if (nextHp <= 0) {
      closeNewsSession(true, '보스 격파 성공!')
      return
    }

    if (nextTurns <= 0) {
      closeNewsSession(false, '보스전 시간 종료!')
    }
  }

  function restartNews() {
    setNewsRound(1)
    setNewsScore(0)
    setNewsCoins(0)
    setNewsResult('')
    setNewsEnded(false)
    setCombo(0)
    setBossHp(6)
    setBossTurns(7)
  }

  return (
    <div className="shell">
      <header className="hero pixelCard" data-testid="hero">
        <div className="mascots">
          <div className="pixel doctor" aria-hidden="true" />
          <div className="pixel ant" aria-hidden="true" />
        </div>
        <div>
          <h1>Orderflow Doctor Arena</h1>
          <p>도트 감성 오더플로우 트레이딩 게임</p>
        </div>
      </header>

      <nav className="tabs" data-testid="mode-tabs">
        {(['quiz', 'health', 'news'] as Mode[]).map((m) => (
          <button key={m} data-testid={`tab-${m}`} className={mode === m ? 'tab active' : 'tab'} onClick={() => setMode(m)}>
            {modeTitle[m]}
          </button>
        ))}
      </nav>

      {mode === 'quiz' && (
        <section className="card pixelCard" data-testid="quiz-mode">
          <div className="row between">
            <h2>{currentQuiz.type} 퀴즈</h2>
            <strong data-testid="quiz-accuracy">정확도 {quizAccuracy}% (최고 {bestAccuracy}%)</strong>
          </div>
          <p className="sub">{currentQuiz.title}</p>
          <p className="subtle" data-testid="quiz-progress">문항 진행 {quizSolved}/{QUIZ_TARGET} (목표 정확도 60% 이상)</p>

          <div className="uploader pixelPanel">
            <label>
              차트 이미지 업로드
              <input type="file" accept="image/*" onChange={(e) => onUploadFile(e.target.files?.[0] ?? null)} />
            </label>
            {uploadSrc && (
              <div className="cropGrid">
                <label>X <input type="range" min={0} max={60} value={crop.x} onChange={(e) => setCropValue('x', Number(e.target.value))} /></label>
                <label>Y <input type="range" min={0} max={60} value={crop.y} onChange={(e) => setCropValue('y', Number(e.target.value))} /></label>
                <label>W <input type="range" min={30} max={100} value={crop.w} onChange={(e) => setCropValue('w', Number(e.target.value))} /></label>
                <label>H <input type="range" min={30} max={100} value={crop.h} onChange={(e) => setCropValue('h', Number(e.target.value))} /></label>
              </div>
            )}
            {croppedSrc && (
              <div className="previewWrap">
                <span>크롭 미리보기</span>
                <img src={croppedSrc} alt="크롭 미리보기" className="previewImage" />
              </div>
            )}
          </div>

          <div
            ref={cropStageRef}
            className="chartBox pixelPanel cropStage"
            onPointerDown={handleCropStart}
            onPointerMove={handleCropMove}
            onPointerUp={handleCropEnd}
            onPointerLeave={handleCropEnd}
          >
            {uploadSrc ? (
              <img src={uploadSrc} alt="업로드 차트" className="quizImage" />
            ) : (
              <svg viewBox="0 0 100 100" preserveAspectRatio="none">
                <polyline points={linePath(reveal ? currentQuiz.points : visiblePoints)} fill="none" stroke="#1e9d64" strokeWidth="2.2" />
              </svg>
            )}
            {uploadSrc && (
              <div
                className={`cropRect ${draggingCrop ? 'dragging' : ''}`}
                style={{ left: `${crop.x}%`, top: `${crop.y}%`, width: `${crop.w}%`, height: `${crop.h}%` }}
              />
            )}
            {!reveal && <div className="fog">뒷부분 방향 예측</div>}
          </div>

          <div className="row">
            <button data-testid="quiz-up" disabled={quizSessionDone} onClick={() => submitQuiz('up')}>상승</button>
            <button data-testid="quiz-down" disabled={quizSessionDone} onClick={() => submitQuiz('down')}>하락</button>
            <button data-testid="quiz-side" disabled={quizSessionDone} onClick={() => submitQuiz('side')}>횡보</button>
            {quizSessionDone && <button data-testid="quiz-reset" onClick={resetQuizSession}>10문제 다시 시작</button>}
          </div>

          {reveal && (
            <div className="result pixelPanel">
              <p>예측: {guess} / 정답: {currentQuiz.truth}</p>
              <p>{guess === currentQuiz.truth ? '정답입니다.' : '오답입니다.'}</p>
              <button data-testid="quiz-next" onClick={nextQuiz}>다음 문제</button>
            </div>
          )}

          {quizSessionDone && (
            <div className="result pixelPanel" data-testid="quiz-session-result">
              <p>10문제 세션 종료</p>
              <p>최종 정확도 {quizAccuracy}% ({quizAccuracy >= 60 ? '목표 달성' : '재도전 필요'})</p>
            </div>
          )}
        </section>
      )}

      {mode === 'health' && (
        <section className="card pixelCard" data-testid="health-mode">
          <div className="row between">
            <h2>차트 종합건강검진</h2>
            <div className="row">
              <div className="badge">검진비 {healthFee}코인</div>
              <button data-testid="health-pdf" onClick={downloadHealthReport}>PDF 리포트 저장</button>
            </div>
          </div>

          <div className="grid">
            {(Object.keys(metrics) as (keyof HealthMetrics)[]).map((key) => (
              <label key={key} className="metric pixelPanel">
                <span>{metricLabel(key)}</span>
                <input type="range" min={0} max={100} value={metrics[key]} onChange={(e) => updateMetric(key, Number(e.target.value))} />
                <em>{metrics[key]}</em>
              </label>
            ))}
          </div>

          <div className="healthChart pixelPanel">
            <div className="baseline" />
            {healthOverlays.map((item, i) => (
              <div key={i} className={`overlay ${item.tone}`} style={{ left: `${item.x}%`, top: `${item.y}%` }}>
                {item.label}
              </div>
            ))}
          </div>

          <div className="doctorBox pixelPanel">
            <div className="pixel doctor" aria-hidden="true" />
            <div>
              <h3>차트 검진 의사 소견</h3>
              <p data-testid="health-score">종합 건강도: <strong>{healthScore}</strong>/100</p>
              <p data-testid="health-action">권고 포지션: <strong>{healthAction}</strong></p>
              <p className="subtle">
                {healthScore >= 76
                  ? '혈액순환 양호. 눌림 매수 우선.'
                  : healthScore >= 56
                    ? '중립. VWAP 회복 확인 뒤 진입.'
                    : '혈액순환 저하. 반등 매도 우세.'}
              </p>
            </div>
          </div>

          <div className="checklist pixelPanel">
            {healthChecklist.map((item) => (
              <div key={item.label} className="checkItem">
                <span>{item.label}</span>
                <strong className={item.state.toLowerCase()}>{item.state}</strong>
              </div>
            ))}
          </div>
        </section>
      )}

      {mode === 'news' && (
        <section className="card pixelCard" data-testid="news-mode">
          <div className="row between">
            <h2>개미를 흔들어라</h2>
            <div className="row">
              <label className="selectWrap">
                난이도
                <select value={difficulty} onChange={(e) => { setDifficulty(e.target.value as Difficulty); restartNews() }}>
                  <option value="easy">easy</option>
                  <option value="normal">normal</option>
                  <option value="hard">hard</option>
                </select>
              </label>
              <strong data-testid="news-round">라운드 {newsRound}/{preRounds + 1}</strong>
              <strong data-testid="news-combo">콤보 x{combo}</strong>
              <strong data-testid="news-coins">코인 {newsCoins}</strong>
              <strong data-testid="news-best-coins">최고 {bestCoins}</strong>
            </div>
          </div>

          <article className="headline pixelPanel">
            <h3>{currentNews.headline}</h3>
            <p>뉴스 톤: {currentNews.tone === 'good' ? '호재' : '악재'}</p>
            <p className="hint">규칙: 호재→덤핑, 악재→매집</p>
            {isBossRound && (
              <p className="bossLine">BOSS HP {bossHp} / TURN {bossTurns}</p>
            )}
          </article>

          <div className="row">
            <button data-testid="news-dump" disabled={newsEnded} onClick={() => playNews('dump')}>덤핑</button>
            <button data-testid="news-accumulate" disabled={newsEnded} onClick={() => playNews('accumulate')}>매집</button>
            {newsEnded && <button data-testid="news-restart" onClick={restartNews}>새 세션</button>}
          </div>

          <p className="resultLine" data-testid="news-result">{newsResult}</p>
          <p className="subtle" data-testid="news-completion-rate">세션 완료율 {completionRate}% ({newsCompleted}/{newsSessions})</p>
          {newsEnded && <p className="subtle">세션 종료: 정답 {newsScore}</p>}
        </section>
      )}
    </div>
  )
}

export default App
