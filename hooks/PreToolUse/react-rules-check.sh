#!/bin/bash
# React/Next.js 파일 수정 시 규칙 상기
# Hook Type: PreToolUse | Matcher: Write|Edit

# stdin에서 JSON 읽기
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

if [[ "$FILE" == *.tsx ]] || [[ "$FILE" == *.jsx ]]; then
    echo "React rules: Promise.all | No barrel import | Server Component default | next/image"
fi
