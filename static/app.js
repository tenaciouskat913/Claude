let currentMode = "url";
let currentFactsheet = null;

const errorBanner = document.getElementById("error-banner");
const form = document.getElementById("generate-form");
const generateBtn = document.getElementById("generate-btn");
const spinner = document.getElementById("spinner");
const preview = document.getElementById("preview");

document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    currentMode = btn.dataset.mode;
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById("policy_url").classList.toggle("hidden", currentMode !== "url");
    document.getElementById("policy_text").classList.toggle("hidden", currentMode !== "text");
  });
});

function showError(message) {
  errorBanner.textContent = message;
  errorBanner.classList.remove("hidden");
}

function clearError() {
  errorBanner.classList.add("hidden");
  errorBanner.textContent = "";
}

function renderPreview(factsheet) {
  document.getElementById("preview-title").textContent = factsheet.title || "";
  document.getElementById("preview-subtitle").textContent = [factsheet.jurisdiction, factsheet.policy_reference]
    .filter(Boolean)
    .join(" — ");
  document.getElementById("preview-summary").textContent = factsheet.policy_summary || "";
  document.getElementById("preview-evidence").textContent = factsheet.evidence_section || "";
  document.getElementById("preview-scope").textContent = factsheet.scope_considerations || "";

  const list = document.getElementById("preview-alignment");
  list.innerHTML = "";
  (factsheet.alignment_points || []).forEach((point) => {
    const li = document.createElement("li");
    const strong = document.createElement("strong");
    strong.textContent = point.policy_requirement + " ";
    li.appendChild(strong);
    li.appendChild(document.createTextNode(`→ ${point.emp_feature}. ${point.explanation}`));
    list.appendChild(li);
  });

  preview.classList.remove("hidden");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  clearError();
  preview.classList.add("hidden");

  const payload = {
    mode: currentMode,
    policy_url: document.getElementById("policy_url").value.trim(),
    policy_text: document.getElementById("policy_text").value.trim(),
    jurisdiction_or_policy_name: document.getElementById("jurisdiction_or_policy_name").value.trim(),
    emp_description: document.getElementById("emp_description").value.trim(),
  };

  generateBtn.disabled = true;
  spinner.classList.remove("hidden");

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!data.ok) {
      showError(data.error || "Something went wrong.");
      return;
    }

    currentFactsheet = data.factsheet;
    renderPreview(currentFactsheet);
  } catch (err) {
    showError("Could not reach the server. Please try again.");
  } finally {
    generateBtn.disabled = false;
    spinner.classList.add("hidden");
  }
});

document.getElementById("download-btn").addEventListener("click", async () => {
  if (!currentFactsheet) return;
  clearError();

  try {
    const response = await fetch("/api/download", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ factsheet: currentFactsheet }),
    });

    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      showError(data.error || "Could not generate the document.");
      return;
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const disposition = response.headers.get("Content-Disposition") || "";
    const match = disposition.match(/filename="?([^"]+)"?/);
    const filename = match ? match[1] : "EMP_FactSheet.docx";

    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  } catch (err) {
    showError("Could not reach the server. Please try again.");
  }
});
