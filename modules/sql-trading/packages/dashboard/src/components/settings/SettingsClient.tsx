'use client';

import { useTheme } from '@/lib/theme-provider';
import { Badge } from '@/components/ui';
import { useSummary } from '@/hooks';

export function SettingsClient() {
  const { theme, toggle, senior, toggleSenior } = useTheme();
  const { data: summary, isLoading, error } = useSummary();

  return (
    <div className="space-y-6">
      {/* 테마 설정 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">테마</h2>
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-[var(--text)]">다크 모드</span>
            <button
              onClick={toggle}
              className="px-4 py-2 bg-[var(--accent)] text-white rounded-lg text-sm"
            >
              {theme === 'dark' ? '라이트로 전환' : '다크로 전환'}
            </button>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[var(--text)]">시니어 모드</span>
            <button
              onClick={toggleSenior}
              className={`px-4 py-2 rounded-lg text-sm ${
                senior
                  ? 'bg-[var(--accent)] text-white'
                  : 'bg-[var(--bg)] border border-[var(--border)] text-[var(--text)]'
              }`}
            >
              {senior ? '켜짐' : '꺼짐'}
            </button>
          </div>
        </div>
      </section>

      {/* API 상태 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">API 상태</h2>
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-[var(--text)]">연결 상태</span>
            {isLoading ? (
              <Badge variant="warning">확인 중...</Badge>
            ) : error ? (
              <Badge variant="error">오프라인</Badge>
            ) : (
              <Badge variant="success">온라인</Badge>
            )}
          </div>
          {summary && (
            <>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text)]">서버 시간</span>
                <span className="font-mono text-[var(--text-muted)] text-sm">
                  {summary.server_time}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-[var(--text)]">마지막 업데이트</span>
                <span className="font-mono text-[var(--text-muted)] text-sm">
                  {summary.last_update || 'N/A'}
                </span>
              </div>
            </>
          )}
        </div>
      </section>

      {/* 정보 */}
      <section>
        <h2 className="text-sm font-semibold text-[var(--text-muted)] mb-3">앱 정보</h2>
        <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-lg p-4 space-y-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="text-[var(--text)]">버전</span>
            <span className="text-[var(--text-muted)]">1.0.0</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[var(--text)]">API 주소</span>
            <span className="text-[var(--text-muted)] font-mono text-xs">
              {process.env.NEXT_PUBLIC_API_URL || 'localhost:8080'}
            </span>
          </div>
        </div>
      </section>
    </div>
  );
}
