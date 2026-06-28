(() => {
  "use strict";

  const enabled = document.querySelector("#enabled");
  const status = document.querySelector("#status");
  const applyNow = document.querySelector("#applyNow");

  const setStatus = (message) => {
    status.textContent = message;
  };

  const loadOptions = () => {
    chrome.storage.sync.get({ enabled: true }, (items) => {
      const value = chrome.runtime.lastError ? true : items.enabled;
      enabled.checked = Boolean(value);
    });
  };

  const saveOption = (event) => {
    const input = event.currentTarget;
    chrome.storage.sync.set({ enabled: input.checked }, () => {
      if (chrome.runtime.lastError) {
        enabled.checked = !input.checked;
        setStatus("저장 실패");
        return;
      }

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

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === "sync" && changes.enabled) {
      enabled.checked = Boolean(changes.enabled.newValue);
      setStatus("저장됨");
    }
  });

  enabled.addEventListener("change", saveOption);
  applyNow.addEventListener("click", sendApplyMessage);
  loadOptions();
})();
