/**
 * 클로바노트 자동 요약 시스템
 * Google Apps Script - 24시간 자동 실행
 */

// ✅ 설정 완료
const CLAUDE_API_KEY = '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';
const FOLDER_ID = '17qWrHGYQbuikn_psh-zru7kMEbCyOWc8';

// 처리된 파일 추적용
const PROCESSED_KEY = 'processedFiles';

/**
 * 메인 함수 - 트리거로 실행
 */
function processNewFiles() {
  const folder = DriveApp.getFolderById(FOLDER_ID);
  const files = folder.getFilesByType(MimeType.PLAIN_TEXT);

  const processedFiles = getProcessedFiles();

  while (files.hasNext()) {
    const file = files.next();
    const fileName = file.getName();
    const fileId = file.getId();

    // 요약 파일은 건너뛰기
    if (fileName.includes('_요약')) continue;

    // 이미 처리된 파일 건너뛰기
    if (processedFiles.includes(fileId)) continue;

    // 요약 파일이 이미 있는지 확인
    const summaryName = fileName.replace('.txt', '_요약.md');
    if (fileExists(folder, summaryName)) {
      markAsProcessed(fileId);
      continue;
    }

    try {
      Logger.log('처리 중: ' + fileName);

      const content = file.getBlob().getDataAsString('UTF-8');

      if (content.length < 100) {
        markAsProcessed(fileId);
        continue;
      }

      const summary = summarizeWithClaude(content);

      if (summary) {
        const date = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd');
        const markdownContent = formatMarkdown(summary, date);
        folder.createFile(summaryName, markdownContent, MimeType.PLAIN_TEXT);
        Logger.log('요약 생성 완료: ' + summaryName);
      }

      markAsProcessed(fileId);

    } catch (error) {
      Logger.log('오류: ' + fileName + ' - ' + error.message);
    }
  }
}

/**
 * Claude API 호출
 */
function summarizeWithClaude(transcript) {
  const prompt = `당신은 수업 내용을 학생이 복습하기 좋게 정리하는 전문가입니다.

다음 수업 녹음 텍스트를 분석하여 구조화된 요약을 작성해주세요.

## 지침

### 1. 중요 개념 (key_concepts)
- 단어가 아닌 **문장형**으로 작성
- 선생님이 강조한 핵심 멘트를 그대로 살려서 작성

### 2. 개념별 상세 설명 (concept_details)
- 수업에서 **실제 언급된 구체적인 예시, 비유, 설명**을 최대한 포함
- 딱딱한 교과서 문체가 아닌, 선생님이 설명하듯 **친절하고 구어체**로 작성
- 각 설명은 **3-5문장 이상**으로 충분히 길게 작성

### 3. 암기용 요약 (memorization_summary)
- 핵심만 불릿 포인트로 정리

## 출력 형식 (JSON)
{
    "title": "수업 제목",
    "key_concepts": ["문장형 핵심 멘트1", "문장형 핵심 멘트2"],
    "concept_details": [
        {"name": "개념명", "explanation": "구체적이고 친절한 설명"}
    ],
    "memorization_summary": "• 핵심1\\n• 핵심2",
    "full_summary": "전체 요약"
}

## 수업 녹음 텍스트
${transcript}`;

  const payload = {
    model: 'claude-3-5-haiku-20241022',
    max_tokens: 4096,
    messages: [
      { role: 'user', content: prompt }
    ]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'x-api-key': CLAUDE_API_KEY,
      'anthropic-version': '2023-06-01'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch('https://api.anthropic.com/v1/messages', options);
  const result = JSON.parse(response.getContentText());

  if (result.error) {
    throw new Error(result.error.message);
  }

  const text = result.content[0].text;

  let jsonStr = text;
  if (text.includes('{')) {
    const start = text.indexOf('{');
    const end = text.lastIndexOf('}') + 1;
    jsonStr = text.substring(start, end);
  }

  return JSON.parse(jsonStr);
}

/**
 * 마크다운 형식으로 변환
 */
function formatMarkdown(data, date) {
  let md = `# ${data.title}\n\n`;
  md += `**날짜**: ${date}\n\n`;

  if (data.key_concepts && data.key_concepts.length > 0) {
    md += `## 📌 중요 개념\n`;
    data.key_concepts.forEach(concept => {
      md += `- ${concept}\n`;
    });
    md += '\n';
  }

  if (data.concept_details && data.concept_details.length > 0) {
    md += `## 📖 개념별 상세 설명\n\n`;
    data.concept_details.forEach(detail => {
      md += `### ${detail.name}\n`;
      md += `${detail.explanation}\n\n`;
    });
  }

  if (data.memorization_summary) {
    md += `## 🧠 암기용 요약\n\n`;
    md += `${data.memorization_summary}\n\n`;
  }

  if (data.full_summary) {
    md += `---\n*${data.full_summary}*\n`;
  }

  return md;
}

/**
 * 파일 존재 확인
 */
function fileExists(folder, fileName) {
  const files = folder.getFilesByName(fileName);
  return files.hasNext();
}

/**
 * 처리된 파일 목록 가져오기
 */
function getProcessedFiles() {
  const props = PropertiesService.getScriptProperties();
  const data = props.getProperty(PROCESSED_KEY);
  return data ? JSON.parse(data) : [];
}

/**
 * 처리 완료 표시
 */
function markAsProcessed(fileId) {
  const props = PropertiesService.getScriptProperties();
  const processed = getProcessedFiles();
  if (!processed.includes(fileId)) {
    processed.push(fileId);
    if (processed.length > 100) {
      processed.shift();
    }
    props.setProperty(PROCESSED_KEY, JSON.stringify(processed));
  }
}

/**
 * 테스트 함수
 */
function testRun() {
  Logger.log('테스트 시작...');
  processNewFiles();
  Logger.log('테스트 완료!');
}

/**
 * 트리거 설정 (한 번만 실행)
 */
function createTrigger() {
  const triggers = ScriptApp.getProjectTriggers();
  triggers.forEach(trigger => ScriptApp.deleteTrigger(trigger));

  ScriptApp.newTrigger('processNewFiles')
    .timeBased()
    .everyMinutes(5)
    .create();

  Logger.log('트리거 설정 완료! 5분마다 자동 실행됩니다.');
}
