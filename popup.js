(() => {
  "use strict";

  const DEFAULT_OPTIONS = {
    enabled: true,
    redirectNewChats: true,
    patchNewChatLinks: true,
    clickVisibleToggle: true,
    debug: false
  };

  const optionIds = [
    "enabled",
    "redirectNewChats",
    "patchNewChatLinks",
    "clickVisibleToggle"
  ];

  const status = document.querySelector("#status");
  const applyNow = document.querySelector("#applyNow");

  const setStatus = (message) => {
    status.textContent = message;
  };

  const loadOptions = () => {
    chrome.storage.sync.get(DEFAULT_OPTIONS, (items) => {
      for (const id of optionIds) {
        document.querySelector(`#${id}`).checked = Boolean(items[id]);
      }
    });
  };

  const saveOption = (event) => {
    const input = event.currentTarget;
    chrome.storage.sync.set({ [input.id]: input.checked }, () => {
      setStatus("저장됨");
    });
  };

  const sendApplyMessage = async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    if (!tab?.id) {
      setStatus("활성 탭 없음");
      return;
    }

    chrome.tabs.sendMessage(tab.id, { type: "TEMPORARY_CHAT_AUTO_APPLY" }, () => {
      if (chrome.runtime.lastError) {
        setStatus("ChatGPT 탭에서 사용 가능");
        return;
      }

      setStatus("적용됨");
    });
  };

  for (const id of optionIds) {
    document.querySelector(`#${id}`).addEventListener("change", saveOption);
  }

  applyNow.addEventListener("click", sendApplyMessage);
  loadOptions();
})();
