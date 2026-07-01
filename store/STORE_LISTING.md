# Chrome Web Store Listing Draft

## Name

ChatGPT Temporary Chat Auto

## Short Description

Automatically opens new ChatGPT chats with Temporary Chat enabled. Unofficial extension.

## Detailed Description

ChatGPT Temporary Chat Auto makes Temporary Chat the default for new ChatGPT conversations.

When you open ChatGPT or click New chat, the extension keeps the Temporary Chat URL parameter in place so new chats start in Temporary Chat mode. It works on `chatgpt.com` and `chat.openai.com`.

Use the popup to turn automatic Temporary Chat on or off. On the ChatGPT page, a compact Auto toggle can appear near the Temporary Chat indicator for quick control.

This is an unofficial extension and is not affiliated with OpenAI.

## Category

Productivity

## Language

English

## Single Purpose

Automatically open new ChatGPT chats in Temporary Chat mode.

## Permission Justifications

### storage

Stores the user's extension preference, specifically whether automatic Temporary Chat mode is enabled.

### Host permission: https://chatgpt.com/*

Allows the extension to run on ChatGPT pages so it can add the Temporary Chat URL parameter to new chat links and apply the user's Temporary Chat preference.

### Host permission: https://chat.openai.com/*

Supports the older ChatGPT domain for users who are still routed through `chat.openai.com`.

## Remote Code

No. The extension does not load or execute remote code.

## Data Usage

The extension does not collect user data.

Recommended Chrome Web Store data disclosure:

- Do not select any user data collection categories.
- Certify that data is not sold or used for unrelated purposes.
- Privacy policy URL: `https://github.com/HanChangHun/chatgpt-temporary-chat-auto/blob/main/PRIVACY.md`

## Test Instructions

1. Install the extension from the submitted package.
2. Open `https://chatgpt.com/`.
3. Confirm that opening a new chat routes to a URL with `temporary-chat=true`.
4. Open the extension popup and turn automation off.
5. Confirm New chat links are no longer modified by the extension.

No test credentials are required. The reviewer can test with any ChatGPT account.

## Store Assets

- Icon: `icons/icon-128.png`
- Small promotional image: `store/assets/promo-small-440x280.png`
- Marquee promotional image: `store/assets/promo-marquee-1400x560.png`
- Screenshot: `store/assets/screenshot-1280x800.png`

## Korean Submission Checklist

See `store/SUBMISSION_CHECKLIST_KO.md`.
