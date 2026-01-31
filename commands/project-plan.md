---
description: "프로젝트 계획 수립 (Create project plan)"
argument-hint: "[project_name or PRD_path]"
---

# 프로젝트 계획

PRD(Product Requirements Document)를 기반으로 프로젝트 실행 계획을 수립합니다.

## 동작

1. PRD 파일 또는 프로젝트 요구사항 분석
2. 단계별 마일스톤 설정
3. Steel Thread 식별
4. 태스크 분해 및 의존성 정의
5. `.planning/` 폴더에 계획 문서 생성

## 생성 문서

```
.planning/
├── PROJECT.md      # 프로젝트 개요
├── ROADMAP.md      # 마일스톤 및 일정
├── STATE.md        # 현재 진행 상태
├── ARCHITECTURE.md # 아키텍처 설계
└── TASKS.md        # 세부 태스크 목록
```

## 사용 예시

```
/project-plan my-app
/project-plan ./docs/PRD.md
```

## 출력 형식

```
📋 프로젝트 계획 수립

프로젝트: [프로젝트명]
예상 단계: [N]개 마일스톤
Steel Thread: [핵심 기능 목록]

마일스톤:
M1: [기초 설정] - 태스크 N개
M2: [핵심 기능] - 태스크 N개
M3: [통합/테스트] - 태스크 N개

.planning/ 폴더에 계획 문서가 생성되었습니다.
```
