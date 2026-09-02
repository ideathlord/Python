const SERVER = "http://127.0.0.1:5005";

const titleEl = document.getElementById("video-title");
const statusEl = document.getElementById("status");
const btn = document.getElementById("download-btn");
const qualitySelect = document.getElementById("quality");
const audioOnlyCheckbox = document.getElementById("audio-only");

let currentUrl = null;
let pollTimer = null;

function isYouTubeUrl(url) {
  return /^https?:\/\/(www\.)?(youtube\.com\/watch|youtu\.be\/|m\.youtube\.com\/watch)/.test(
    url
  );
}

function setStatus(text, type) {
  statusEl.textContent = text;
  statusEl.className = type || "";
}

// Detect the current tab's URL
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const tab = tabs[0];
  if (tab && tab.url && isYouTubeUrl(tab.url)) {
    currentUrl = tab.url;
    titleEl.textContent = tab.title || currentUrl;
  } else {
    titleEl.textContent = "Not a YouTube video page.";
    btn.disabled = true;
  }
});

// Check the local server is reachable, warn early if not
fetch(`${SERVER}/ping`)
  .then((r) => r.ok || Promise.reject())
  .catch(() => {
    setStatus(
      "Local server not running. Start server.py first.",
      "error"
    );
    btn.disabled = true;
  });

btn.addEventListener("click", () => {
  if (!currentUrl) return;

  btn.disabled = true;
  setStatus("Starting download…");

  fetch(`${SERVER}/download`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: currentUrl,
      audio_only: audioOnlyCheckbox.checked,
      quality: parseInt(qualitySelect.value, 10),
    }),
  })
    .then((r) => r.json())
    .then((data) => {
      if (data.error) {
        setStatus(data.error, "error");
        btn.disabled = false;
        return;
      }
      pollStatus(data.job_id);
    })
    .catch(() => {
      setStatus("Couldn't reach local server.", "error");
      btn.disabled = false;
    });
});

function pollStatus(jobId) {
  clearInterval(pollTimer);
  pollTimer = setInterval(() => {
    fetch(`${SERVER}/status/${jobId}`)
      .then((r) => r.json())
      .then((job) => {
        if (job.status === "downloading") {
          setStatus(`Downloading… ${job.percent || ""}`);
        } else if (job.status === "done") {
          clearInterval(pollTimer);
          setStatus(`Done: ${job.title || "saved"}`, "success");
          btn.disabled = false;
        } else if (job.status === "error") {
          clearInterval(pollTimer);
          setStatus(`Failed: ${job.error}`, "error");
          btn.disabled = false;
        }
      })
      .catch(() => {
        clearInterval(pollTimer);
        setStatus("Lost connection to server.", "error");
        btn.disabled = false;
      });
  }, 1000);
}
