const tabs = document.querySelectorAll(".tab");
const form = document.getElementById("form");
const fileInput = document.getElementById("file");
const drop = document.getElementById("drop");
const dropText = document.getElementById("drop-text");
const submit = document.getElementById("submit");
const status = document.getElementById("status");

let mode = "encrypt";

function setMode(next) {
  mode = next;
  tabs.forEach((t) => t.classList.toggle("active", t.dataset.mode === next));
  submit.textContent = next === "encrypt" ? "Encrypt PDF" : "Decrypt PDF";
  clearStatus();
}

function showStatus(msg, kind) {
  status.textContent = msg;
  status.className = `status ${kind}`;
  status.hidden = false;
}

function clearStatus() {
  status.hidden = true;
  status.className = "status";
}

function setFile(file) {
  if (!file) return;
  fileInput.files = createFileList(file);
  dropText.textContent = file.name;
  drop.classList.add("has-file");
  clearStatus();
}

function createFileList(file) {
  const dt = new DataTransfer();
  dt.items.add(file);
  return dt.files;
}

tabs.forEach((t) => t.addEventListener("click", () => setMode(t.dataset.mode)));

fileInput.addEventListener("change", () => setFile(fileInput.files[0]));

["dragenter", "dragover"].forEach((e) =>
  drop.addEventListener(e, (ev) => {
    ev.preventDefault();
    drop.classList.add("dragover");
  })
);
["dragleave", "drop"].forEach((e) =>
  drop.addEventListener(e, (ev) => {
    ev.preventDefault();
    drop.classList.remove("dragover");
  })
);
drop.addEventListener("drop", (ev) => setFile(ev.dataTransfer.files[0]));

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const file = fileInput.files[0];
  if (!file) return showStatus("Choose a PDF first.", "error");

  const body = new FormData();
  body.append("file", file);
  body.append("password", document.getElementById("password").value);

  submit.disabled = true;
  showStatus("Processing…", "");

  try {
    const res = await fetch(`/api/${mode}`, { method: "POST", body });
    if (!res.ok) {
      const { detail } = await res.json().catch(() => ({}));
      throw new Error(detail || "Something went wrong.");
    }
    const blob = await res.blob();
    downloadBlob(blob, res.headers.get("Content-Disposition"));
    showStatus("Done — your download has started.", "success");
  } catch (err) {
    showStatus(err.message, "error");
  } finally {
    submit.disabled = false;
  }
});

function downloadBlob(blob, disposition) {
  const match = disposition && disposition.match(/filename="(.+?)"/);
  const name = match ? match[1] : "output.pdf";
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}

setMode("encrypt");
