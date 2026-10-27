"""
Semantic Text Similarity Application.
REST API and Web Interface.
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import PyPDF2

import database
from chunker import chunk_text
from engine import (
    similarity_index,
    compute_pair_similarity,
    EMBED_MODEL_NAME,
    EMB_DIM
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Initialize database schema on startup
database.init_db()

# Rebuild / sync FAISS index if index is empty but database has chunks
if similarity_index.index.ntotal == 0:
    all_chunks = database.get_all_chunks()
    if all_chunks:
        print("[App] Syncing FAISS index from existing database chunks...")
        similarity_index.rebuild_from_db()

def extract_text_from_pdf(file_storage) -> str:
    """Extracts text content from an uploaded PDF file."""
    reader = PyPDF2.PdfReader(file_storage)
    text_parts = []
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text.strip())
    return "\n\n".join(text_parts).strip()

# ----------------- Web UI -----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Docker and monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "semantic-similarity-studio",
        "faiss_total": similarity_index.index.ntotal if similarity_index.index else 0
    }), 200

# ----------------- System Stats -----------------
@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Returns system and corpus statistics."""
    db_stats = database.get_db_stats()
    engine_stats = similarity_index.get_stats()
    return jsonify({
        "status": "healthy",
        "model": EMBED_MODEL_NAME,
        "embedding_dim": EMB_DIM,
        "corpus": db_stats,
        "engine": engine_stats
    })

# ----------------- Corpus Management -----------------
@app.route("/api/texts", methods=["GET"])
def list_texts():
    """Returns list of stored texts with metadata."""
    texts = database.get_texts()
    return jsonify({
        "total": len(texts),
        "texts": texts
    })

@app.route("/api/texts/<int:text_id>", methods=["GET"])
def get_single_text(text_id):
    """Returns a specific document with its chunks."""
    doc = database.get_text(text_id)
    if not doc:
        return jsonify({"error": f"Document with ID {text_id} not found."}), 404
    return jsonify(doc)

@app.route("/api/texts", methods=["POST"])
def add_document():
    """
    Adds a new text or PDF to the corpus.
    Accepts:
    - JSON: { "label": "...", "content": "..." }
    - Multipart form: 'file' (PDF or TXT) and optional 'label'
    """
    content = ""
    label = ""
    source_type = "text"

    if request.is_json:
        payload = request.get_json() or {}
        label = payload.get("label", "").strip()
        content = payload.get("content", "").strip()
        source_type = "text"
    elif "file" in request.files:
        file = request.files["file"]
        if not file or file.filename == "":
            return jsonify({"error": "No file selected."}), 400
        
        filename = file.filename
        label = request.form.get("label", "").strip() or filename

        if filename.lower().endswith(".pdf"):
            source_type = "pdf"
            try:
                content = extract_text_from_pdf(file)
            except Exception as e:
                return jsonify({"error": f"Failed to parse PDF file: {str(e)}"}), 400
        else:
            source_type = "text"
            try:
                content = file.read().decode("utf-8", errors="replace").strip()
            except Exception as e:
                return jsonify({"error": f"Failed to read file: {str(e)}"}), 400
    else:
        # Check form-data with text
        label = request.form.get("label", "").strip()
        content = request.form.get("content", "").strip()
        source_type = "text"

    if not content:
        return jsonify({"error": "Content cannot be empty."}), 400

    if not label:
        label = f"Document ({content[:30]}...)"

    # Structural chunking
    chunks = chunk_text(content)
    if not chunks:
        chunks = [content]

    # Save to SQLite
    doc_info = database.add_text(
        label=label,
        content=content,
        chunks=chunks,
        source_type=source_type
    )

    # Embed and add to FAISS
    similarity_index.add_document(
        text_id=doc_info["id"],
        doc_label=label,
        chunks=chunks
    )

    return jsonify({
        "message": "Document successfully indexed.",
        "document": doc_info,
        "sample_chunks": chunks[:3]
    }), 201

@app.route("/api/texts/<int:text_id>", methods=["DELETE"])
def delete_document(text_id):
    """Deletes a text and rebuilds the FAISS index."""
    existing = database.get_text(text_id)
    if not existing:
        return jsonify({"error": f"Document with ID {text_id} not found."}), 404

    deleted = database.delete_text(text_id)
    if deleted:
        similarity_index.rebuild_from_db()
        return jsonify({
            "message": f"Document {text_id} deleted and FAISS index synchronized.",
            "deleted_id": text_id,
            "remaining_chunks": similarity_index.index.ntotal
        })
    else:
        return jsonify({"error": "Could not delete document."}), 500

@app.route("/api/rebuild", methods=["POST"])
def rebuild_index_endpoint():
    """Explicitly rebuilds FAISS index from SQLite database."""
    similarity_index.rebuild_from_db()
    return jsonify({
        "message": "FAISS index rebuilt successfully.",
        "total_chunks": similarity_index.index.ntotal,
        "metadata_count": len(similarity_index.metadata)
    })

# ----------------- Similarity Endpoints -----------------
@app.route("/api/similarity/pair", methods=["POST"])
def similarity_pair():
    """
    Computes pairwise semantic similarity between two texts.
    Accepts: { "text1": str, "text2": str }
    Returns: { score, score_pct, label, color, description, text1_words, ... }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body provided."}), 400

    text1 = data.get("text1", "")
    text2 = data.get("text2", "")

    if not isinstance(text1, str) or not isinstance(text2, str):
        return jsonify({"error": "Both 'text1' and 'text2' must be string values."}), 400

    if not text1.strip() or not text2.strip():
        return jsonify({"error": "Both text1 and text2 must be non-empty."}), 400

    result = compute_pair_similarity(text1, text2)
    return jsonify(result)

@app.route("/api/similarity/query", methods=["POST"])
def similarity_query():
    """
    Searches the indexed corpus for chunks most semantically similar to query.
    Accepts: { "query": str, "top_k": int (default 5) }
    Returns: { query, total_matches, results: [...] }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON body provided."}), 400

    query = data.get("query", "")
    if not isinstance(query, str) or not query.strip():
        return jsonify({"error": "Query parameter must be a non-empty string."}), 400

    try:
        top_k = int(data.get("top_k", 5))
        top_k = max(1, min(top_k, 20))
    except (ValueError, TypeError):
        top_k = 5

    if similarity_index.index.ntotal == 0:
        return jsonify({
            "query": query,
            "total_matches": 0,
            "results": [],
            "message": "Corpus is currently empty. Please add or upload documents to search."
        })

    results = similarity_index.search(query=query, top_k=top_k)
    return jsonify({
        "query": query,
        "total_matches": len(results),
        "results": results
    })

# ----------------- Domain Packs Endpoints -----------------
@app.route("/api/datasets/domains", methods=["GET"])
def get_domain_packs():
    """Returns metadata, presets, and sample queries for all custom domain packs."""
    from datasets.domain_packs import DOMAIN_PACKS
    summary = {}
    for key, pack in DOMAIN_PACKS.items():
        summary[key] = {
            "title": pack["title"],
            "badge_color": pack["badge_color"],
            "document_title": pack["document"]["label"],
            "presets": pack["presets"],
            "queries": pack["queries"]
        }
    return jsonify({
        "total_domains": len(summary),
        "domains": summary
    })

@app.route("/api/datasets/seed", methods=["POST"])
def seed_domain_pack():
    """Seeds one or all curated domain packs into SQLite and FAISS."""
    from datasets.domain_packs import DOMAIN_PACKS
    data = request.get_json(silent=True) or {}
    domain_key = data.get("domain", "all")

    seeded = []
    keys_to_seed = DOMAIN_PACKS.keys() if domain_key == "all" else [domain_key]

    for k in keys_to_seed:
        if k not in DOMAIN_PACKS:
            continue
        pack = DOMAIN_PACKS[k]
        doc = pack["document"]
        raw_text = doc["content"]
        chunks = chunk_text(raw_text)
        doc_record = database.add_text(
            label=f"[{pack['title']}] {doc['label']}",
            content=raw_text,
            chunks=chunks,
            source_type="text"
        )
        similarity_index.add_document(
            text_id=doc_record["id"],
            doc_label=doc_record["label"],
            chunks=chunks
        )
        seeded.append({
            "domain": k,
            "title": pack["title"],
            "doc_id": doc_record["id"],
            "chunk_count": len(chunks)
        })

    return jsonify({
        "status": "success",
        "message": f"Successfully seeded {len(seeded)} domain dataset(s) into SQLite and FAISS.",
        "seeded": seeded,
        "total_indexed_chunks": similarity_index.index.ntotal
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
