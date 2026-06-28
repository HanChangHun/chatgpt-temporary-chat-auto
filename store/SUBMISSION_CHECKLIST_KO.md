# Chrome Web Store 제출 체크리스트

## 1. 개발자 계정 설정

- 사업자 선언: `비판매자 계정`
- 이유: 현재 확장은 무료 배포이며 광고, 구독, 유료 기능, 어필리에이트, 데이터 판매가 없습니다.
- 나중에 수익화하거나 사업자/회사 명의로 운영하면 `판매자 계정`으로 변경하는 편이 안전합니다.

## 2. 새 항목 생성

- Chrome Web Store Developer Dashboard에서 `새 항목` 또는 `New item`을 선택합니다.
- 업로드 파일:
  - `C:\Users\ehwjs\workspaces\chatgpt-temporary-chat-auto-0.1.0-store.zip`

## 3. 스토어 등록정보

- 이름: `ChatGPT Temporary Chat Auto`
- 간단한 설명:
  - `Automatically opens new ChatGPT chats with Temporary Chat enabled. Unofficial extension; no data collection.`
- 카테고리: `Productivity`
- 언어: `English`
- 자세한 설명:

```text
ChatGPT Temporary Chat Auto keeps new ChatGPT conversations in Temporary Chat mode by default.

It works on chatgpt.com and chat.openai.com, updates New chat links to include the Temporary Chat URL parameter, and can enable a visible Temporary Chat toggle when the page clearly shows it as off.

The popup lets users turn the automation on or off and control each behavior separately.

Privacy-first behavior:

- No analytics
- No remote code
- No external network requests from the extension
- No collection or transmission of ChatGPT conversation content
- Only extension preferences are stored with Chrome storage

This is an unofficial extension and is not affiliated with OpenAI.
```

## 4. 이미지

- 아이콘: 패키지 안의 `icons/icon-128.png`
- 스크린샷:
  - `C:\Users\ehwjs\workspaces\chatgpt-temporary-chat-auto\store\assets\screenshot-1280x800.png`
- Small promo tile:
  - `C:\Users\ehwjs\workspaces\chatgpt-temporary-chat-auto\store\assets\promo-small-440x280.png`

## 5. 개인정보

- Privacy policy URL:
  - `https://github.com/HanChangHun/chatgpt-temporary-chat-auto/blob/main/PRIVACY.md`
- 데이터 수집:
  - 사용자 데이터 수집 안 함
- Remote code:
  - 없음
- 전용 목적 설명:

```text
Automatically open new ChatGPT chats in Temporary Chat mode. The extension updates ChatGPT new chat URLs and New chat links so they include the Temporary Chat URL parameter, and it stores only the user's extension preferences.
```

## 6. 권한 설명

### storage

Stores the user's extension preferences, such as whether automatic Temporary Chat mode and optional link/toggle behaviors are enabled.

### https://chatgpt.com/*

Allows the extension to run on ChatGPT pages so it can add the Temporary Chat URL parameter to new chat links and apply the user's Temporary Chat preference.

### https://chat.openai.com/*

Supports the older ChatGPT domain for users who are still routed through chat.openai.com.

### 호스트 권한 사용 근거 칸이 하나만 있는 경우

```text
Required to run only on chatgpt.com and chat.openai.com so the extension can update New chat links with the Temporary Chat URL parameter and apply the user's Temporary Chat preference. The extension does not collect, transmit, or store ChatGPT conversation content.
```

## 6.1 게시자 연락처 이메일

- 왼쪽 `설정` > `프로필`에서 연락처 이메일을 추가하고 인증합니다.
- 개인 이메일을 공개하고 싶지 않다면 GitHub용 별도 이메일이나 새 Gmail alias를 쓰는 편이 좋습니다.
- 이 항목은 이메일 인증이 완료되어야 제출 가능 상태가 됩니다.

## 7. 심사자 테스트 안내

```text
1. Install the extension from the submitted package.
2. Open https://chatgpt.com/.
3. Confirm that opening a new chat routes to a URL with temporary-chat=true.
4. Open the extension popup and turn automation off.
5. Confirm New chat links are no longer modified by the extension.

No test credentials are required. The reviewer can test with any ChatGPT account.
```

## 8. 제출 전 확인

- 확장은 무료입니다.
- 확장은 OpenAI 공식 확장이 아닙니다.
- 확장은 ChatGPT 대화 내용, 계정 정보, 프롬프트, 응답을 외부 서버로 전송하지 않습니다.
- 확장은 원격 코드를 불러오지 않습니다.
