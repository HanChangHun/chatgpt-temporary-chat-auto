# ChatGPT Temporary Chat Auto

ChatGPT 새 대화를 자동으로 Temporary Chat 모드로 열어 주는 Chrome Manifest V3 확장입니다.

This is an unofficial extension and is not affiliated with OpenAI.

## Features

- Automatically opens new ChatGPT chats with `temporary-chat=true`.
- Patches New chat links on `chatgpt.com` and `chat.openai.com`.
- Adds a small in-page toggle near ChatGPT's Temporary Chat indicator.
- Stores only the single on/off preference in Chrome sync storage.

## 설치

1. Chrome에서 `chrome://extensions`를 엽니다.
2. 오른쪽 위 `Developer mode`를 켭니다.
3. `Load unpacked`를 누르고 이 폴더를 선택합니다.

## 동작 방식

- `https://chatgpt.com/`과 `https://chat.openai.com/`에서만 동작합니다.
- 새 채팅 URL과 New chat 링크에 `temporary-chat=true` 파라미터를 붙입니다.
- 화면에 Temporary Chat 토글이 보이고 꺼진 상태가 명확할 때만 클릭합니다.
- 팝업에서는 자동 적용을 하나의 체크박스로 켜고 끌 수 있습니다.
- ChatGPT 화면 안의 작은 토글로도 자동 적용을 바로 켜고 끌 수 있습니다.

## 메모

ChatGPT 화면 구조는 바뀔 수 있어서 URL 보정을 우선 사용합니다. UI가 바뀌어 토글 클릭이 동작하지 않아도 새 채팅 링크 보정은 비교적 오래 버틸 가능성이 높습니다.

## Privacy

The extension does not collect, transmit, sell, or share user data. It does not read or send ChatGPT conversation content to any server. See [PRIVACY.md](PRIVACY.md).

Public privacy policy URL: https://github.com/HanChangHun/chatgpt-temporary-chat-auto/blob/main/PRIVACY.md

## Chrome Web Store

Store listing copy, privacy answers, and review notes are in [store/STORE_LISTING.md](store/STORE_LISTING.md).
