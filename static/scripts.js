/**
 * Semantic Similarity Studio - Interactive Application Logic
 * Supports: Pair Comparison, Query Search, Corpus Management, FAISS Synchronization.
 */

// Preset Text Pairs for instant testing
const PRESETS = {
  paraphrase: {
    t1: "The quick brown fox jumps over the lazy dog.",
    t2: "A fast brown fox leaps over a sleepy canine."
  },
  technical: {
    t1: "Transformers utilize multi-head self-attention mechanisms to process sequence data in parallel without recurrent connections.",
    t2: "Self-attention layers in modern deep learning models enable tokens to compute contextual representations across all sequence positions simultaneously."
  },
  contrast: {
    t1: "The central bank announced an immediate decrease in benchmark interest rates to stimulate economic borrowing and expansion.",
    t2: "The monetary committee decided to raise benchmark lending rates aggressively to curb escalating consumer price inflation."
  },
  unrelated: {
    t1: "Quantum computing harnesses superposition and entanglement to solve discrete optimization problems exponentially faster than classical computers.",
    t2: "Authentic Neapolitan pizza crust requires high-protein flour, slow cold fermentation for 48 hours, and baking in a wood-fired oven at 900 degrees Fahrenheit."
  }
};

const SAMPLE_DOCS = [
  {
    label: "Neural Networks & Transformer Architecture",
    content: `# Deep Learning Foundations
Deep learning algorithms use multi-layered artificial neural networks to model complex nonlinear representations from large-scale data.

# Transformer Architecture & Attention
The Transformer architecture, introduced in 'Attention Is All You Need', replaces recurrent neural networks with multi-head self-attention.
Each attention head computes scaled dot-product attention over query, key, and value vectors, allowing parallel training on GPUs.

# Positional Encoding & Feed-Forward Layers
Because Transformers contain no recurrent or convolutional operations, positional encodings are injected into the input embeddings to preserve token order.
Each sub-layer is followed by layer normalization and residual connections to stabilize gradient propagation.`
  },
  {
    label: "Quantum Computing Principles",
    content: `# Principles of Quantum Mechanics
Quantum computation is rooted in the fundamental laws of quantum mechanics, specifically superposition, entanglement, and quantum interference.

# Qubits and Quantum Superposition
Unlike classical binary bits that exist in state 0 or 1, a quantum bit (qubit) exists in a continuous linear superposition |ψ⟩ = α|0⟩ + β|1⟩.
When measured, the wave function collapses to a basis state according to Born's probability rule.

# Quantum Algorithms and Quantum Supremacy
Shor's algorithm achieves polynomial-time integer factorization, posing a threat to RSA cryptography.
Grover's search algorithm provides a quadratic speedup for unstructured database queries.`
  },
  {
    label: "Artisan Bread Baking & Fermentation Science",
    content: `# The Microbiology of Sourdough
Sourdough bread relies on a symbiotic culture of wild yeasts (such as Candida humilis) and lactic acid bacteria (such as Lactobacillus sanfranciscensis).

# Fermentation and Gluten Development
During bulk fermentation, amylase enzymes break down starch into simple sugars, which are fermented into carbon dioxide and organic acids.
Hydration and gentle stretching align glutenin and gliadin proteins into an elastic gluten matrix that traps fermentation gases.

# Baking and Crust Caramelization
Baking sourdough with steam gelatinizes surface starches, delaying crust formation to maximize oven spring.
High oven temperatures promote Maillard reactions and caramelization, producing a crisp, dark, flavorful crust.`
  }
];

// ----------------- State & Utilities -----------------
let activeIngestMode = "text";
let selectedUploadFile = null;

async function api(path, method = "GET", body = null) {
  const opts = { method, headers: {} };
  if (body instanceof FormData) {
    opts.body = body;
  } else if (body) {
    opts.headers["Content-Type"] = "application/json";
    opts.body = JSON.stringify(body);
  }

  const res = await fetch(path, opts);
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const errorMsg = data.error || `HTTP ${res.status}: ${res.statusText}`;
    throw new Error(errorMsg);
  }
  return data;
}

function showToast(message, type = "info") {
  const container = document.getElementById("toast-container");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `<span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(40px)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// ----------------- Navigation Tabs -----------------
function initTabs() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => {
        t.classList.remove("active");
        t.setAttribute("aria-selected", "false");
      });
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));

      tab.classList.add("active");
      tab.setAttribute("aria-selected", "true");
      const targetPane = document.getElementById(tab.dataset.tab);
      if (targetPane) targetPane.classList.add("active");

      // Auto-load corpus data when switching to corpus tab
      if (tab.dataset.tab === "tab-corpus") {
        loadCorpusRegistry();
      }
    });
  });
}

// ----------------- Stats & Header -----------------
async function refreshStats() {
  try {
    const stats = await api("/api/stats");
    const docCount = stats.corpus ? stats.corpus.total_texts : 0;
    const chunkCount = stats.engine ? stats.engine.total_indexed_chunks : 0;

    document.getElementById("header-doc-count").innerText = `${docCount} docs`;
    document.getElementById("header-chunk-count").innerText = `${chunkCount} chunks`;
    document.getElementById("nav-corpus-count").innerText = docCount;
  } catch (err) {
    console.warn("Could not refresh system stats:", err);
  }
}

// ----------------- Pair Comparison -----------------
function initPairEditors() {
  const t1 = document.getElementById("text1");
  const t2 = document.getElementById("text2");

  function updateCounts(el, wordId, charId) {
    const val = el.value;
    const words = val.trim() ? val.trim().split(/\s+/).length : 0;
    document.getElementById(wordId).innerText = `${words} words`;
    document.getElementById(charId).innerText = `${val.length} chars`;
  }

  t1.addEventListener("input", () => updateCounts(t1, "t1-word-count", "t1-char-count"));
  t2.addEventListener("input", () => updateCounts(t2, "t2-word-count", "t2-char-count"));

  // Hotkey: Ctrl+Enter or Cmd+Enter to compare
  [t1, t2].forEach(area => {
    area.addEventListener("keydown", e => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        runPairComparison();
      }
    });
  });
}

function loadPreset(key) {
  const preset = PRESETS[key];
  if (!preset) return;
  const t1 = document.getElementById("text1");
  const t2 = document.getElementById("text2");
  t1.value = preset.t1;
  t2.value = preset.t2;
  t1.dispatchEvent(new Event("input"));
  t2.dispatchEvent(new Event("input"));
  runPairComparison();
}

function clearText(target) {
  const area = target === "t1" ? document.getElementById("text1") : document.getElementById("text2");
  area.value = "";
  area.dispatchEvent(new Event("input"));
  area.focus();
}

function swapTexts() {
  const t1 = document.getElementById("text1");
  const t2 = document.getElementById("text2");
  const temp = t1.value;
  t1.value = t2.value;
  t2.value = temp;
  t1.dispatchEvent(new Event("input"));
  t2.dispatchEvent(new Event("input"));
  if (t1.value.trim() && t2.value.trim()) {
    runPairComparison();
  }
}

async function runPairComparison() {
  const text1 = document.getElementById("text1").value.trim();
  const text2 = document.getElementById("text2").value.trim();

  if (!text1 || !text2) {
    showToast("Please provide both Text A and Text B to compare.", "error");
    return;
  }

  const btn = document.getElementById("btn-compare");
  const spinner = document.getElementById("compare-spinner");
  const label = document.getElementById("btn-compare-label");

  btn.disabled = true;
  spinner.style.display = "inline-block";
  label.innerText = "Encoding & Scoring...";

  try {
    const result = await api("/api/similarity/pair", "POST", { text1, text2 });
    renderPairResult(result);
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
    label.innerText = "Calculate Similarity";
  }
}

function renderPairResult(data) {
  const resultCard = document.getElementById("pair-result-card");
  resultCard.style.display = "block";

  // Circular gauge animation
  const circle = document.getElementById("pair-meter-circle");
  const circumference = 314.159; // 2 * PI * 50
  const offset = circumference * (1 - (data.score || 0));
  circle.style.strokeDashoffset = offset;
  circle.style.stroke = data.color || "#6366f1";

  // Score texts
  document.getElementById("pair-score-pct").innerText = `${data.score_pct}%`;
  document.getElementById("pair-score-raw").innerText = `Cosine Score: ${data.score.toFixed(4)}`;
  
  // Tier badge & description
  const badge = document.getElementById("pair-tier-badge");
  badge.innerText = data.label;
  badge.style.color = data.color;
  badge.style.borderColor = data.color;
  badge.style.backgroundColor = `${data.color}15`;

  document.getElementById("pair-tier-desc").innerText = data.description;

  // Linear bar
  const progressBar = document.getElementById("pair-progress-bar");
  progressBar.style.width = `${data.score_pct}%`;
  progressBar.style.background = `linear-gradient(90deg, #6366f1, ${data.color})`;

  // Stats
  document.getElementById("pair-t1-stat").innerText = `${data.text1_words} words`;
  document.getElementById("pair-t1-chars").innerText = `${data.text1_chars} characters`;
  document.getElementById("pair-t2-stat").innerText = `${data.text2_words} words`;
  document.getElementById("pair-t2-chars").innerText = `${data.text2_chars} characters`;
  document.getElementById("pair-common-count").innerText = `${data.common_words_count} overlapping words`;

  // Tokens chips
  const tokensWrap = document.getElementById("pair-common-tokens");
  tokensWrap.innerHTML = "";
  if (data.common_words_sample && data.common_words_sample.length > 0) {
    data.common_words_sample.forEach(token => {
      const chip = document.createElement("span");
      chip.className = "common-chip";
      chip.innerText = token;
      tokensWrap.appendChild(chip);
    });
  } else {
    tokensWrap.innerHTML = `<span style="font-size:0.75rem; color:var(--text-tertiary);">No shared lexical words</span>`;
  }

  document.getElementById("pair-time").innerText = `Computed at ${new Date().toLocaleTimeString()}`;
  resultCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

// ----------------- Query Search -----------------
function initQuerySearch() {
  const input = document.getElementById("query-input");
  input.addEventListener("keydown", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      runQuerySearch();
    }
  });
}

function clearQueryInput() {
  const input = document.getElementById("query-input");
  input.value = "";
  input.focus();
}

function runQuickQuery(text) {
  const input = document.getElementById("query-input");
  input.value = text;
  runQuerySearch();
}

async function runQuerySearch() {
  const query = document.getElementById("query-input").value.trim();
  if (!query) {
    showToast("Please enter a query string.", "error");
    return;
  }

  const topK = parseInt(document.getElementById("topk-slider").value) || 5;
  const btn = document.getElementById("btn-run-query");
  const spinner = document.getElementById("query-spinner");

  btn.disabled = true;
  spinner.style.display = "inline-block";

  const startTime = performance.now();

  try {
    const data = await api("/api/similarity/query", "POST", { query, top_k: topK });
    const elapsed = Math.round(performance.now() - startTime);
    renderQueryResults(data, elapsed);
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
  }
}

function renderQueryResults(data, elapsedMs) {
  const emptyState = document.getElementById("query-empty-state");
  const summaryRow = document.getElementById("query-results-summary");
  const resultsList = document.getElementById("query-results-list");

  resultsList.innerHTML = "";

  if (!data.results || data.results.length === 0) {
    summaryRow.style.display = "none";
    emptyState.style.display = "block";
    document.getElementById("empty-state-title").innerText = "No matching chunks found";
    document.getElementById("empty-state-desc").innerText = data.message || "Your corpus might be empty or no documents matched your query.";
    return;
  }

  emptyState.style.display = "none";
  summaryRow.style.display = "flex";
  document.getElementById("results-count").innerText = data.results.length;
  document.getElementById("query-meta-time").innerText = `Query evaluated in ${elapsedMs}ms across FAISS index`;

  data.results.forEach(res => {
    const card = document.createElement("div");
    card.className = "result-item-card";

    card.innerHTML = `
      <div class="result-item-top">
        <div class="result-badges-group">
          <span class="rank-badge">#${res.rank} Rank</span>
          <span class="source-badge">${escapeHtml(res.doc_label)}</span>
          <span class="chunk-badge">Chunk ${res.chunk_index + 1}</span>
        </div>
        <span class="score-badge" style="color: ${res.color}; border-color: ${res.color}; background: ${res.color}15;">
          ${res.score_pct}% Match · ${res.label}
        </span>
      </div>
      <div class="result-snippet">${escapeHtml(res.snippet)}</div>
    `;

    resultsList.appendChild(card);
  });
}

// ----------------- Corpus Management -----------------
function switchIngestMode(mode) {
  activeIngestMode = mode;
  const textBtn = document.getElementById("subtab-btn-text");
  const fileBtn = document.getElementById("subtab-btn-file");
  const textGroup = document.getElementById("ingest-text-group");
  const fileGroup = document.getElementById("ingest-file-group");

  if (mode === "text") {
    textBtn.classList.add("active");
    fileBtn.classList.remove("active");
    textGroup.style.display = "block";
    fileGroup.style.display = "none";
  } else {
    fileBtn.classList.add("active");
    textBtn.classList.remove("active");
    fileGroup.style.display = "block";
    textGroup.style.display = "none";
  }
}

function handleFileSelect(input) {
  if (input.files && input.files[0]) {
    selectedUploadFile = input.files[0];
    document.getElementById("dropzone-label").innerText = `Selected: ${selectedUploadFile.name} (${Math.round(selectedUploadFile.size / 1024)} KB)`;
    const labelInput = document.getElementById("doc-label");
    if (!labelInput.value.trim()) {
      labelInput.value = selectedUploadFile.name.replace(/\.[^/.]+$/, "");
    }
  }
}

// Setup drag and drop on dropzone
function initDropzone() {
  const dropzone = document.getElementById("file-dropzone");
  if (!dropzone) return;

  ["dragenter", "dragover"].forEach(event => {
    dropzone.addEventListener(event, e => {
      e.preventDefault();
      dropzone.style.borderColor = "var(--accent-primary)";
      dropzone.style.background = "rgba(99, 102, 241, 0.1)";
    });
  });

  ["dragleave", "drop"].forEach(event => {
    dropzone.addEventListener(event, e => {
      e.preventDefault();
      dropzone.style.borderColor = "var(--border-strong)";
      dropzone.style.background = "var(--bg-input)";
    });
  });

  dropzone.addEventListener("drop", e => {
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const input = document.getElementById("doc-file-input");
      input.files = e.dataTransfer.files;
      handleFileSelect(input);
    }
  });
}

async function handleIngest(e) {
  e.preventDefault();
  const label = document.getElementById("doc-label").value.trim();
  const spinner = document.getElementById("ingest-spinner");
  const btn = document.getElementById("btn-ingest");

  btn.disabled = true;
  spinner.style.display = "inline-block";

  try {
    if (activeIngestMode === "text") {
      const content = document.getElementById("doc-content").value.trim();
      if (!content) {
        throw new Error("Please enter text content to chunk and index.");
      }
      await api("/api/texts", "POST", { label, content });
      document.getElementById("doc-content").value = "";
    } else {
      if (!selectedUploadFile) {
        throw new Error("Please select a PDF or TXT file to upload.");
      }
      const formData = new FormData();
      formData.append("file", selectedUploadFile);
      formData.append("label", label);
      await api("/api/texts", "POST", formData);
      selectedUploadFile = null;
      document.getElementById("dropzone-label").innerText = "Click or Drag & Drop PDF here";
      document.getElementById("doc-file-input").value = "";
    }

    document.getElementById("doc-label").value = "";
    showToast(`Document "${label}" successfully chunked & indexed!`, "success");
    await loadCorpusRegistry();
    await refreshStats();
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
  }
}

async function loadCorpusRegistry() {
  const loading = document.getElementById("corpus-loading");
  const empty = document.getElementById("corpus-empty");
  const list = document.getElementById("corpus-items");

  loading.style.display = "block";
  empty.style.display = "none";
  list.innerHTML = "";

  try {
    const data = await api("/api/texts");
    loading.style.display = "none";

    if (!data.texts || data.texts.length === 0) {
      empty.style.display = "block";
      return;
    }

    data.texts.forEach(item => {
      const card = document.createElement("div");
      card.className = "corpus-item-card";

      const badgeClass = item.source_type === "pdf" ? "pdf" : "text";

      card.innerHTML = `
        <div class="item-left">
          <span class="item-source-badge ${badgeClass}">${item.source_type}</span>
          <div class="item-info">
            <div class="item-title" title="${escapeHtml(item.label)}">${escapeHtml(item.label)}</div>
            <div class="item-meta">
              ${item.chunk_count} chunks · ${item.word_count} words · Indexed ${item.created_at}
            </div>
          </div>
        </div>
        <div class="item-actions">
          <button class="btn btn-secondary btn-sm" onclick="inspectDocChunks(${item.id})">
            View Chunks
          </button>
          <button class="btn btn-secondary btn-sm" onclick="deleteDocument(${item.id}, '${escapeHtml(item.label)}')" style="color:var(--status-danger);">
            Delete
          </button>
        </div>
      `;
      list.appendChild(card);
    });
  } catch (err) {
    loading.style.display = "none";
    showToast(`Failed to load corpus: ${err.message}`, "error");
  }
}

async function inspectDocChunks(docId) {
  try {
    const doc = await api(`/api/texts/${docId}`);
    document.getElementById("modal-doc-title").innerText = doc.label;
    document.getElementById("modal-doc-meta").innerText = `${doc.chunk_count} structural chunks · ${doc.word_count} total words · ${doc.source_type.toUpperCase()}`;

    const list = document.getElementById("modal-chunks-list");
    list.innerHTML = "";

    doc.chunks.forEach(chunk => {
      const chunkCard = document.createElement("div");
      chunkCard.className = "modal-chunk-card";
      chunkCard.innerHTML = `
        <div class="modal-chunk-head">
          <span>Chunk ${chunk.chunk_index + 1}</span>
          <span>${chunk.word_count} words · ${chunk.char_count} chars</span>
        </div>
        <div class="modal-chunk-text">${escapeHtml(chunk.chunk_text)}</div>
      `;
      list.appendChild(chunkCard);
    });

    document.getElementById("chunks-modal").style.display = "flex";
  } catch (err) {
    showToast(`Could not fetch document chunks: ${err.message}`, "error");
  }
}

function closeChunksModal() {
  document.getElementById("chunks-modal").style.display = "none";
}

function closeModalOnOverlay(e) {
  if (e.target.id === "chunks-modal") {
    closeChunksModal();
  }
}

async function deleteDocument(docId, label) {
  if (!confirm(`Are you sure you want to delete "${label}" and rebuild the FAISS index?`)) {
    return;
  }

  try {
    await api(`/api/texts/${docId}`, "DELETE");
    showToast(`Document "${label}" deleted and index synced.`, "success");
    await loadCorpusRegistry();
    await refreshStats();
  } catch (err) {
    showToast(`Failed to delete document: ${err.message}`, "error");
  }
}

async function rebuildFaissIndex() {
  const btn = document.getElementById("btn-rebuild-index");
  const spinner = document.getElementById("rebuild-spinner");
  btn.disabled = true;
  spinner.style.display = "inline-block";

  try {
    const res = await api("/api/rebuild", "POST");
    showToast(`FAISS index rebuilt successfully! Total chunks: ${res.total_chunks}`, "success");
    await refreshStats();
  } catch (err) {
    showToast(`Rebuild error: ${err.message}`, "error");
  } finally {
    btn.disabled = false;
    spinner.style.display = "none";
  }
}

async function seedSampleDocs() {
  showToast("Seeding sample documents into corpus...", "info");
  for (const doc of SAMPLE_DOCS) {
    try {
      await api("/api/texts", "POST", doc);
    } catch (e) {
      console.warn("Seeding error:", e);
    }
  }
  showToast("3 Sample documents indexed into SQLite & FAISS!", "success");
  await refreshStats();
  await loadCorpusRegistry();
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
}

// ----------------- Initialization -----------------
window.addEventListener("DOMContentLoaded", async () => {
  initTabs();
  initPairEditors();
  initQuerySearch();
  initDropzone();
  await refreshStats();
  await loadCorpusRegistry();

  // Load initial preset into pair view for instant WOW
  loadPreset("paraphrase");
});
