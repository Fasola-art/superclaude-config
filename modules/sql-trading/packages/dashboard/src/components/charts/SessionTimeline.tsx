'use client';

interface Session {
  name: string;
  start: number;
  end: number;
  color: string;
}

const SESSIONS: Session[] = [
  { name: '아시아', start: 9, end: 15.5, color: 'bg-blue-500/30' },
  { name: '런던 Open', start: 16, end: 22.5, color: 'bg-green-500/30' },
  { name: '뉴욕 Open', start: 22.5, end: 24, color: 'bg-purple-500/30' },
];

export function SessionTimeline() {
  const currentHour = new Date().getHours() + new Date().getMinutes() / 60;

  return (
    <div className="space-y-3">
      <div className="relative h-12 bg-card border border-border rounded-lg overflow-hidden">
        {SESSIONS.map((session) => {
          const left = (session.start / 24) * 100;
          const width = ((session.end - session.start) / 24) * 100;

          return (
            <div
              key={session.name}
              className={`absolute inset-y-0 ${session.color} border-l border-border`}
              style={{ left: `${left}%`, width: `${width}%` }}
            >
              <span className="absolute inset-0 flex items-center justify-center text-xs font-medium">
                {session.name}
              </span>
            </div>
          );
        })}

        {/* 현재 시각 마커 */}
        <div
          className="absolute inset-y-0 w-0.5 bg-accent z-10"
          style={{ left: `${(currentHour / 24) * 100}%` }}
        />
      </div>

      <div className="flex justify-between text-xs text-muted">
        <span>00:00</span>
        <span>09:00</span>
        <span>16:00</span>
        <span>22:30</span>
      </div>
    </div>
  );
}
