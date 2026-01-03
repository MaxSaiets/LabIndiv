async function postJSON(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const msg = data && data.error ? data.error : "request_failed";
    throw new Error(msg);
  }
  return data;
}

function $(id) {
  return document.getElementById(id);
}

function setResult(text, muted = false) {
  const el = $("result");
  if (!el) return;
  el.textContent = text;
  el.classList.toggle("muted", muted);
}

function setMeta(text) {
  const el = $("meta");
  if (!el) return;
  el.textContent = text || "";
}

function enableCopy(enabled) {
  const btn = $("copyBtn");
  if (!btn) return;
  btn.disabled = !enabled;
}

document.addEventListener("DOMContentLoaded", () => {
  const genBtn = $("genBtn");
  const clearBtn = $("clearBtn");
  const copyBtn = $("copyBtn");
  const postText = $("postText");

  if (!genBtn || !clearBtn || !copyBtn || !postText) return;

  clearBtn.addEventListener("click", () => {
    postText.value = "";
    setResult("Поки що порожньо…", true);
    setMeta("");
    enableCopy(false);
  });

  copyBtn.addEventListener("click", async () => {
    const txt = $("result")?.textContent || "";
    if (!txt || txt.includes("порожньо")) return;
    await navigator.clipboard.writeText(txt);
    setMeta("Скопійовано в буфер обміну.");
    setTimeout(() => setMeta(""), 1800);
  });

  genBtn.addEventListener("click", async () => {
    const text = postText.value.trim();
    if (!text) {
      setResult("Введіть текст поста.", true);
      enableCopy(false);
      return;
    }

    genBtn.disabled = true;
    setResult("Генерую…", true);
    setMeta("");
    enableCopy(false);

    try {
      const data = await postJSON("/api/generate", { text });
      const tags = (data.hashtags || []).join(" ");
      if (!tags) {
        setResult("Не вдалося виділити ключові слова. Спробуйте інший текст.", true);
        enableCopy(false);
      } else {
        setResult(tags, false);
        enableCopy(true);
      }
      if (data.saved) {
        setMeta("Збережено в історії (БД PostgreSQL).");
      } else {
        setMeta("Підказка: увійдіть, щоб зберігати історію в БД.");
      }
    } catch (e) {
      setResult("Помилка запиту: " + (e?.message || "unknown"), true);
      enableCopy(false);
    } finally {
      genBtn.disabled = false;
    }
  });
});


