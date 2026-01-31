#!/usr/bin/env python3
"""
React/Next.js 코드 검사기
49개 Vercel React Best Practices 규칙 검사
"""

import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Violation:
    rule: str
    priority: str
    file: str
    line: int
    message: str
    suggestion: str

class ReactChecker:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.violations: List[Violation] = []

    def check_all(self) -> List[Violation]:
        """모든 규칙 검사"""
        tsx_files = list(self.project_path.rglob("*.tsx"))
        ts_files = list(self.project_path.rglob("*.ts"))

        all_files = tsx_files + ts_files

        for file in all_files:
            if "node_modules" in str(file) or ".next" in str(file):
                continue
            self.check_file(file)

        return self.violations

    def check_file(self, file_path: Path):
        """파일별 검사"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')
        except Exception:
            return

        rel_path = str(file_path.relative_to(self.project_path))

        # BUNDLE-001: Barrel imports
        self._check_barrel_imports(rel_path, lines)

        # BUNDLE-003: Lodash 전체 import
        self._check_lodash_import(rel_path, lines)

        # ASYNC-001: Sequential await
        self._check_sequential_await(rel_path, content, lines)

        # RENDER-001: Client directive 위치
        self._check_use_client(rel_path, lines)

        # IMAGE-001: img 태그 사용
        self._check_img_tag(rel_path, lines)

        # RERENDER-009: Index as key
        self._check_index_key(rel_path, lines)

    def _check_barrel_imports(self, file: str, lines: List[str]):
        """BUNDLE-001: Barrel import 검사"""
        pattern = re.compile(r"from ['\"]@/(?:components|lib|utils)['\"]")
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                self.violations.append(Violation(
                    rule="BUNDLE-001",
                    priority="CRITICAL",
                    file=file,
                    line=i,
                    message="Barrel import 사용됨",
                    suggestion="직접 파일에서 import하세요: from '@/components/Button'"
                ))

    def _check_lodash_import(self, file: str, lines: List[str]):
        """BUNDLE-003: Lodash 전체 import 검사"""
        pattern = re.compile(r"import .* from ['\"]lodash['\"]")
        for i, line in enumerate(lines, 1):
            if pattern.search(line):
                self.violations.append(Violation(
                    rule="BUNDLE-003",
                    priority="CRITICAL",
                    file=file,
                    line=i,
                    message="Lodash 전체 import",
                    suggestion="import debounce from 'lodash/debounce' 형식으로 변경"
                ))

    def _check_sequential_await(self, file: str, content: str, lines: List[str]):
        """ASYNC-001: 연속 await 검사"""
        pattern = re.compile(r"await .+;\s*\n\s*(?:const|let|var)?.+await")
        matches = pattern.finditer(content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.violations.append(Violation(
                rule="ASYNC-001",
                priority="CRITICAL",
                file=file,
                line=line_num,
                message="순차적 await 감지 (Waterfall)",
                suggestion="Promise.all()로 병렬 처리하세요"
            ))

    def _check_use_client(self, file: str, lines: List[str]):
        """RENDER-001: 'use client' 검사"""
        if not lines:
            return

        has_use_client = any("'use client'" in line or '"use client"' in line for line in lines[:5])
        has_hooks = any(re.search(r"use(State|Effect|Memo|Callback|Ref|Context)\s*\(", line) for line in lines)

        if has_hooks and not has_use_client:
            self.violations.append(Violation(
                rule="RENDER-001",
                priority="HIGH",
                file=file,
                line=1,
                message="Hook 사용하지만 'use client' 없음",
                suggestion="파일 상단에 'use client' 추가"
            ))

    def _check_img_tag(self, file: str, lines: List[str]):
        """IMAGE-001: <img> 태그 검사"""
        for i, line in enumerate(lines, 1):
            if re.search(r"<img\s", line):
                self.violations.append(Violation(
                    rule="IMAGE-001",
                    priority="MEDIUM",
                    file=file,
                    line=i,
                    message="<img> 태그 사용됨",
                    suggestion="next/image의 <Image /> 사용"
                ))

    def _check_index_key(self, file: str, lines: List[str]):
        """JS-OPT-009: index를 key로 사용"""
        pattern = re.compile(r"\.map\s*\([^)]*,\s*(\w+)\s*\)[^}]*key\s*=\s*\{\s*\1\s*\}")
        for i, line in enumerate(lines, 1):
            if re.search(r"key\s*=\s*\{\s*(?:index|i|idx)\s*\}", line):
                self.violations.append(Violation(
                    rule="JS-OPT-009",
                    priority="LOW",
                    file=file,
                    line=i,
                    message="index를 key로 사용",
                    suggestion="고유 ID를 key로 사용하세요"
                ))

    def report(self) -> str:
        """검사 결과 리포트"""
        if not self.violations:
            return "✅ 모든 검사 통과! 위반 사항 없음."

        # 우선순위별 정렬
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_violations = sorted(
            self.violations,
            key=lambda v: (priority_order.get(v.priority, 4), v.file, v.line)
        )

        lines = [
            f"⚠️ {len(self.violations)}개 위반 발견\n",
            "=" * 60
        ]

        current_priority = None
        for v in sorted_violations:
            if v.priority != current_priority:
                current_priority = v.priority
                emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(v.priority, "⚪")
                lines.append(f"\n{emoji} {v.priority}")
                lines.append("-" * 40)

            lines.append(f"[{v.rule}] {v.file}:{v.line}")
            lines.append(f"  ❌ {v.message}")
            lines.append(f"  💡 {v.suggestion}")

        # 요약
        by_priority = {}
        for v in self.violations:
            by_priority[v.priority] = by_priority.get(v.priority, 0) + 1

        lines.append("\n" + "=" * 60)
        lines.append("요약:")
        for p in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if p in by_priority:
                lines.append(f"  {p}: {by_priority[p]}개")

        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("사용법: python react-checker.py <프로젝트_경로>")
        print("예시: python react-checker.py /path/to/nextjs-project")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.isdir(project_path):
        print(f"오류: '{project_path}'는 유효한 디렉토리가 아닙니다.")
        sys.exit(1)

    print(f"🔍 React 규칙 검사 중: {project_path}\n")

    checker = ReactChecker(project_path)
    checker.check_all()
    print(checker.report())


if __name__ == "__main__":
    main()
