(() => {
  "use strict";

  const TEMPORARY_PARAM = "temporary-chat";
  const DEFAULT_OPTIONS = {
    enabled: true,
    redirectNewChats: true,
    patchNewChatLinks: true,
    clickVisibleToggle: true,
    debug: false
  };

  const NEW_CHAT_TEXT = [
    "new chat",
    "새 채팅",
    "새로운 채팅",
    "新建聊天",
    "新しいチャット"
  ];

  const TEMPORARY_CHAT_TEXT = [
    "temporary chat",
    "임시 채팅",
    "臨時聊天",
    "临时聊天",
    "一時チャット"
  ];

  let options = { ...DEFAULT_OPTIONS };
  let lastHref = location.href;
  let lastApplyAt = 0;

  const log = (...args) => {
    if (options.debug) {
      console.debug("[Temporary Chat Auto]", ...args);
    }
  };

  const storageGet = (defaults) =>
    new Promise((resolve) => {
      if (!chrome?.storage?.sync) {
        resolve(defaults);
        return;
      }

      chrome.storage.sync.get(defaults, resolve);
    });

  const isSupportedOrigin = (url) =>
    url.origin === "https://chatgpt.com" || url.origin === "https://chat.openai.com";

  const hasTemporaryParam = (url) =>
    url.searchParams.get(TEMPORARY_PARAM) === "true";

  const isConversationOrUtilityPath = (pathname) => {
    const utilityPrefixes = [
      "/api",
      "/auth",
      "/backend-api",
      "/c/",
      "/gpts",
      "/logout",
      "/pricing",
      "/public-api",
      "/search",
      "/share/",
      "/signin",
      "/settings"
    ];

    if (utilityPrefixes.some((prefix) => pathname.startsWith(prefix))) {
      return true;
    }

    return /\/c\/[0-9a-f-]{8,}/i.test(pathname);
  };

  const isLikelyNewChatPath = (url) => {
    if (!isSupportedOrigin(url) || isConversationOrUtilityPath(url.pathname)) {
      return false;
    }

    return url.pathname === "/" || url.pathname === "" || /^\/g\/[^/]+\/?$/.test(url.pathname);
  };

  const withTemporaryParam = (href) => {
    try {
      const url = new URL(href, location.href);

      if (!isLikelyNewChatPath(url)) {
        return null;
      }

      url.searchParams.set(TEMPORARY_PARAM, "true");
      return url.href;
    } catch {
      return null;
    }
  };

  const containsAny = (value, needles) => {
    const normalized = value.replace(/\s+/g, " ").trim().toLowerCase();
    return needles.some((needle) => normalized.includes(needle));
  };

  const getElementText = (element) => {
    const parts = [
      element.getAttribute("aria-label"),
      element.getAttribute("title"),
      element.textContent
    ];

    return parts.filter(Boolean).join(" ");
  };

  const isVisible = (element) => {
    if (!element || !(element instanceof Element)) {
      return false;
    }

    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);

    return (
      rect.width > 0 &&
      rect.height > 0 &&
      style.visibility !== "hidden" &&
      style.display !== "none" &&
      Number(style.opacity || "1") > 0
    );
  };

  const getExplicitCheckedState = (element) => {
    const ariaChecked = element.getAttribute("aria-checked");
    const ariaPressed = element.getAttribute("aria-pressed");
    const dataState = element.getAttribute("data-state");

    if (ariaChecked === "true" || ariaPressed === "true" || dataState === "checked") {
      return true;
    }

    if (ariaChecked === "false" || ariaPressed === "false" || dataState === "unchecked") {
      return false;
    }

    if (element instanceof HTMLInputElement && element.type === "checkbox") {
      return element.checked;
    }

    return null;
  };

  const dispatchTrustedLikeClick = (element) => {
    element.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, pointerId: 1 }));
    element.dispatchEvent(new MouseEvent("mousedown", { bubbles: true }));
    element.dispatchEvent(new PointerEvent("pointerup", { bubbles: true, pointerId: 1 }));
    element.dispatchEvent(new MouseEvent("mouseup", { bubbles: true }));
    element.click();
  };

  const findVisibleTemporaryToggle = () => {
    const controls = Array.from(
      document.querySelectorAll(
        [
          "button",
          "input[type='checkbox']",
          "[role='checkbox']",
          "[role='menuitemcheckbox']",
          "[role='switch']"
        ].join(",")
      )
    );

    for (const control of controls) {
      if (!isVisible(control)) {
        continue;
      }

      const label = [
        getElementText(control),
        control.closest("label")?.textContent,
        control.closest("[role='menuitem'], [role='menuitemcheckbox'], li, div")?.textContent
      ]
        .filter(Boolean)
        .join(" ");

      if (!containsAny(label, TEMPORARY_CHAT_TEXT)) {
        continue;
      }

      if (getExplicitCheckedState(control) === false) {
        return control;
      }
    }

    return null;
  };

  const clickTemporaryToggleIfClearlyOff = () => {
    if (!options.clickVisibleToggle) {
      return false;
    }

    const toggle = findVisibleTemporaryToggle();

    if (!toggle) {
      return false;
    }

    log("Clicking visible temporary chat toggle");
    dispatchTrustedLikeClick(toggle);
    return true;
  };

  const patchAnchor = (anchor) => {
    const temporaryHref = withTemporaryParam(anchor.href);

    if (!temporaryHref || anchor.href === temporaryHref) {
      return false;
    }

    if (!anchor.dataset.temporaryChatAutoOriginalHref) {
      anchor.dataset.temporaryChatAutoOriginalHref = anchor.getAttribute("href") || anchor.href;
    }

    anchor.href = temporaryHref;
    return true;
  };

  const restorePatchedLinks = () => {
    for (const anchor of document.querySelectorAll("a[data-temporary-chat-auto-original-href]")) {
      anchor.setAttribute("href", anchor.dataset.temporaryChatAutoOriginalHref);
      delete anchor.dataset.temporaryChatAutoOriginalHref;
    }
  };

  const patchNewChatLinks = () => {
    if (!options.patchNewChatLinks) {
      return 0;
    }

    let patched = 0;

    for (const anchor of document.querySelectorAll("a[href]")) {
      const text = getElementText(anchor);
      const href = anchor.getAttribute("href") || "";
      const looksLikeRootNewChat = href === "/" || href.startsWith("/?") || href.startsWith("https://chatgpt.com/?");

      if ((looksLikeRootNewChat || containsAny(text, NEW_CHAT_TEXT)) && patchAnchor(anchor)) {
        patched += 1;
      }
    }

    if (patched) {
      log("Patched new chat links", patched);
    }

    return patched;
  };

  const shouldIgnoreModifiedClick = (event) =>
    event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey;

  const navigateToTemporaryChat = () => {
    const temporaryHref = withTemporaryParam(location.origin + "/");

    if (temporaryHref) {
      location.assign(temporaryHref);
    }
  };

  const onCapturedClick = (event) => {
    if (!options.enabled) {
      return;
    }

    const anchor = event.target.closest?.("a[href]");

    if (anchor && options.patchNewChatLinks) {
      const patched = patchAnchor(anchor);

      if (patched && !shouldIgnoreModifiedClick(event)) {
        event.preventDefault();
        event.stopImmediatePropagation();
        location.assign(anchor.href);
      }

      return;
    }

    const button = event.target.closest?.("button, [role='button']");

    if (!button || shouldIgnoreModifiedClick(event)) {
      return;
    }

    if (containsAny(getElementText(button), NEW_CHAT_TEXT)) {
      event.preventDefault();
      event.stopImmediatePropagation();
      navigateToTemporaryChat();
    }
  };

  const applyTemporaryChatMode = (reason = "apply") => {
    if (!options.enabled) {
      restorePatchedLinks();
      return;
    }

    const now = Date.now();

    if (now - lastApplyAt < 250) {
      return;
    }

    lastApplyAt = now;
    patchNewChatLinks();

    try {
      const currentUrl = new URL(location.href);
      const temporaryHref = withTemporaryParam(currentUrl.href);

      if (
        options.redirectNewChats &&
        temporaryHref &&
        temporaryHref !== currentUrl.href &&
        isLikelyNewChatPath(currentUrl) &&
        !hasTemporaryParam(currentUrl)
      ) {
        log("Redirecting to temporary chat URL", reason, temporaryHref);
        location.replace(temporaryHref);
        return;
      }
    } catch {
      return;
    }

    clickTemporaryToggleIfClearlyOff();
  };

  const watchLocationChanges = () => {
    window.setInterval(() => {
      if (location.href !== lastHref) {
        lastHref = location.href;
        applyTemporaryChatMode("url-change");
      }
    }, 500);
  };

  const watchDomChanges = () => {
    const observer = new MutationObserver(() => {
      applyTemporaryChatMode("dom-change");
    });

    observer.observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  };

  const installMessageHandler = () => {
    chrome.runtime?.onMessage?.addListener((message, _sender, sendResponse) => {
      if (message?.type !== "TEMPORARY_CHAT_AUTO_APPLY") {
        return false;
      }

      applyTemporaryChatMode("popup");
      sendResponse({ ok: true });
      return false;
    });
  };

  const installStorageHandler = () => {
    chrome.storage?.onChanged?.addListener((changes, area) => {
      if (area !== "sync") {
        return;
      }

      let changed = false;

      for (const key of Object.keys(DEFAULT_OPTIONS)) {
      if (changes[key]) {
          options[key] = changes[key].newValue;
          changed = true;
        }
      }

      if (changed) {
        if (!options.enabled) {
          restorePatchedLinks();
          return;
        }

        applyTemporaryChatMode("settings-change");
      }
    });
  };

  const init = async () => {
    options = await storageGet(DEFAULT_OPTIONS);

    document.addEventListener("click", onCapturedClick, true);
    installMessageHandler();
    installStorageHandler();
    watchLocationChanges();
    watchDomChanges();
    applyTemporaryChatMode("init");
  };

  init().catch((error) => {
    console.warn("[Temporary Chat Auto] Failed to initialize", error);
  });
})();
