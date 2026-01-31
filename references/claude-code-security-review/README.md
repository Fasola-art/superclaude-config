# 코드 보안 검토 가이드

> 코드 보안 검토 체크리스트 및 가이드

## OWASP Top 10

1. **Injection** - SQL, NoSQL, OS 명령어 인젝션
2. **Broken Authentication** - 인증 취약점
3. **Sensitive Data Exposure** - 민감 데이터 노출
4. **XML External Entities (XXE)** - XML 외부 엔티티
5. **Broken Access Control** - 접근 제어 취약점
6. **Security Misconfiguration** - 보안 설정 오류
7. **Cross-Site Scripting (XSS)** - 크로스 사이트 스크립팅
8. **Insecure Deserialization** - 안전하지 않은 역직렬화
9. **Using Components with Known Vulnerabilities** - 알려진 취약점
10. **Insufficient Logging & Monitoring** - 부족한 로깅

## 검토 체크리스트

- [ ] 입력 검증 및 sanitization
- [ ] 인증/권한 검사
- [ ] 민감 정보 암호화
- [ ] SQL 파라미터화
- [ ] XSS 방지 (escape/encode)
- [ ] CSRF 토큰 사용
- [ ] 에러 메시지 정보 노출 최소화
- [ ] 의존성 취약점 검사
