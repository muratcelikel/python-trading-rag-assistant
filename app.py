"""Streamlit portfolio demo for the end-to-end Trading RAG Assistant."""
from __future__ import annotations

# Project-local import bootstrap: allows direct execution before/without editable install.
import sys
from pathlib import Path as _BootstrapPath
_SRC_DIR = _BootstrapPath(__file__).resolve().parent / "src"
if _SRC_DIR.is_dir() and str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

import json
import time
from pathlib import Path

import streamlit as st

from trading_rag_assistant.config import OUTPUT_DIRECTORY, VECTOR_DB_DIRECTORY
from trading_rag_assistant.demo_mode import (
    get_demo_answer,
    get_demo_questions,
    load_packaged_evaluation_summary,
    load_packaged_evidence,
)
from trading_rag_assistant.document_types import EXTENSION_TO_TYPE
from trading_rag_assistant.embeddings import SentenceTransformerEmbedder
from trading_rag_assistant.indexer import index_document
from trading_rag_assistant.live_evaluation import export_live_evaluation_evidence, run_live_evaluation_with_evidence
from trading_rag_assistant.providers import build_answer_generator
from trading_rag_assistant.query_engine import GroundedQueryEngine
from trading_rag_assistant.retriever import SemanticRetriever
from trading_rag_assistant.vector_store import ChromaVectorStore

st.set_page_config(page_title="Trading RAG Assistant", page_icon="📚", layout="wide")
st.title("Trading RAG Assistant")
st.caption("Kaynak dayanaklı, yatırım tavsiyesi vermeyen eğitim ve portföy amaçlı uçtan uca RAG uygulaması")

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@st.cache_resource(show_spinner=False)
def get_embedder():
    return SentenceTransformerEmbedder()

@st.cache_resource(show_spinner=False)
def get_store():
    return ChromaVectorStore()


def build_engine(provider: str, top_k: int):
    retriever = SemanticRetriever(get_embedder(), get_store(), default_top_k=top_k)
    return GroundedQueryEngine(retriever, build_answer_generator(provider), default_top_k=top_k)

with st.sidebar:
    st.header("Çalışma modu")
    mode = st.radio(
        "İnceleme yöntemi",
        ["Demo (kurulumsuz)", "Groq (bulut)", "Ollama (yerel)"],
        help="Demo modu önceden üretilmiş örnekleri gösterir; Groq ve Ollama gerçek LLM çağrısı yapar.",
    )
    provider = "demo" if mode.startswith("Demo") else ("groq" if mode.startswith("Groq") else "ollama")
    top_k = st.slider("Kaynak parçası sayısı", 1, 8, 3, disabled=provider == "demo")
    max_distance = st.slider("Maksimum cosine distance", 0.10, 1.50, 0.85, 0.05, disabled=provider == "demo")
    if provider == "demo":
        indexed_chunks = "Gerekmez"
    else:
        try:
            indexed_chunks = get_store().count()
        except Exception:
            indexed_chunks = 0
    st.metric("İndeksli parça", indexed_chunks)
    if provider == "groq":
        st.info("Canlı bulut modu: GROQ_API_KEY ve internet gerekir.")
    elif provider == "ollama":
        st.info("Canlı yerel mod: Ollama servisi ve indirilmiş model gerekir.")
    else:
        st.success("Kurulumsuz inceleme: API anahtarı, Ollama ve vektör indeks gerekmez.")
        st.warning("Demo cevapları önceden üretilmiştir; canlı LLM sonucu değildir.")

ask_tab, docs_tab, eval_tab, system_tab = st.tabs(["Canlı Soru-Cevap", "Belge Yönetimi", "100 Soru Kanıtı", "Sistem Durumu"])

with ask_tab:
    if provider == "demo":
        selected = st.selectbox("Paketlenmiş demo sorusu", get_demo_questions())
        custom = st.text_input("Veya kendi sorunuzu yazın", placeholder="Demo dışında serbest soru için Groq/Ollama seçin")
        question = custom.strip() or selected
    else:
        question = st.text_area("Sorunuz", placeholder="Örneğin: Günlük maksimum kayıp sınırı nedir?", height=110)

    if st.button("Kaynaklı cevap üret", type="primary", disabled=not question.strip(), key="ask"):
        try:
            if provider == "demo":
                result = get_demo_answer(question)
                latency = result.latency_seconds
            else:
                engine = build_engine(provider, top_k)
                with st.spinner("Kaynaklar aranıyor ve cevap üretiliyor..."):
                    started = time.perf_counter()
                    result = engine.ask(question, top_k=top_k, max_distance=max_distance)
                    latency = time.perf_counter() - started
            st.subheader("Cevap")
            st.write(result.answer)
            c1, c2, c3 = st.columns(3)
            c1.metric("Durum", result.status)
            c2.metric("Kaynak sayısı", len(result.sources))
            c3.metric("Yanıt süresi", f"{latency:.2f} sn")
            if provider == "demo":
                st.caption("Bu sonuç paketlenmiş demo kanıtıdır; bu oturumda LLM çağrısı yapılmadı.")
            if result.sources:
                st.subheader("Kaynak kanıtları")
                for i, source in enumerate(result.sources, 1):
                    chunk_no = getattr(source, "chunk_index", getattr(source, "chunk_id", "?"))
                    label = f"{i}. {source.source_file} · chunk {chunk_no} · distance {source.distance:.4f}"
                    with st.expander(label, expanded=i == 1):
                        st.code(source.text, language=None)
            else:
                st.warning("İlgili kaynak bulunamadığı için sistem cevap üretmedi veya demo sorusu mevcut değil.")
        except Exception as exc:
            st.error(str(exc))

with docs_tab:
    if provider == "demo":
        st.info("Belge yükleme ve indeksleme canlı modlarda kullanılabilir. Demo modu paketlenmiş kanıtları gösterir.")
    else:
        st.subheader("Belge yükle ve indeksle")
        st.write("TXT, MD, PDF ve DOCX dosyaları desteklenir. Aynı adlı belge yeniden yüklenirse eski parçaları değiştirilir.")
        uploads = st.file_uploader("Belgeleri seçin", type=[ext.lstrip(".") for ext in EXTENSION_TO_TYPE], accept_multiple_files=True)
        c1, c2 = st.columns(2)
        chunk_size = c1.number_input("Chunk boyutu (kelime)", 40, 500, 100, 10)
        overlap = c2.number_input("Overlap (kelime)", 0, 200, 20, 5)
        if st.button("Seçili belgeleri indeksle", disabled=not uploads, key="index"):
            reports = []
            with st.spinner("Belgeler hazırlanıyor ve vektör veritabanına yazılıyor..."):
                for uploaded in uploads:
                    target = UPLOAD_DIR / Path(uploaded.name).name
                    target.write_bytes(uploaded.getbuffer())
                    reports.append(index_document(target, get_embedder(), get_store(), int(chunk_size), int(overlap)))
            st.success(f"{len(reports)} belge indekslendi.")
            st.dataframe(reports, use_container_width=True)
            st.cache_resource.clear()
        if st.button("Örnek belgeleri indeksle", key="sample_index"):
            reports = []
            with st.spinner("Örnek belgeler indeksleniyor..."):
                for path in sorted(Path("data/sample").glob("*")):
                    if path.suffix.lower() in EXTENSION_TO_TYPE:
                        reports.append(index_document(path, get_embedder(), get_store()))
            st.success(f"{len(reports)} örnek belge indekslendi.")
            st.dataframe(reports, use_container_width=True)
            st.cache_resource.clear()

with eval_tab:
    if provider == "demo":
        st.subheader("Paketlenmiş 100 soru kanıtı")
        st.warning("Aşağıdaki sonuçlar çevrimdışı ve yeniden üretilebilir baseline kanıtıdır; canlı Groq/Ollama sonucu değildir.")
        st.markdown(load_packaged_evaluation_summary())
        evidence = load_packaged_evidence(limit=20)
        if evidence:
            st.subheader("Örnek soru bazlı kanıt dosyaları")
            st.dataframe(evidence, use_container_width=True)
        html_path = Path("output/offline_evaluation_evidence/evaluation_report.html")
        if html_path.exists():
            st.download_button("Paketlenmiş HTML raporunu indir", html_path.read_bytes(), file_name="offline_evaluation_report.html", mime="text/html")
    else:
        st.subheader("100 soruluk canlı değerlendirme ve kanıt üretimi")
        st.write("Her soru gerçek retrieval → prompt → LLM zincirinden geçirilir; JSON, CSV, başarısız soru listesi, tekil kanıtlar ve HTML raporu üretilir.")
        cases_path = Path("data/eval/rag_eval_questions.json")
        try:
            case_count = len(json.loads(cases_path.read_text(encoding="utf-8")))
        except Exception:
            case_count = 0
        st.metric("Hazır değerlendirme sorusu", case_count)
        if provider == "ollama":
            st.info("Ollama toplu koşusu checkpoint + otomatik retry kullanır. Yarıda kesilirse aynı butona yeniden basınca tamamlanan sorular atlanır; yalnızca runtime_error kalanlar yeniden denenir.")
            confirm_text = "100 yerel LLM çağrısının uzun sürebileceğini anlıyorum."
        else:
            confirm_text = "Canlı LLM çağrılarının süre ve API kullanımı oluşturacağını anlıyorum."
        confirm = st.checkbox(confirm_text)
        if st.button("100 soruyu canlı çalıştır / kaldığı yerden devam et", type="primary", disabled=not confirm, key="eval"):
            try:
                engine = build_engine(provider, top_k)
                output_dir = OUTPUT_DIRECTORY / f"live_evaluation_{provider}"
                progress = st.progress(0, text="Değerlendirme başlatılıyor...")
                status_line = st.empty()

                def on_progress(position: int, total: int, case_id: str, status: str) -> None:
                    percent = int(position / total * 100) if total else 100
                    progress.progress(percent, text=f"{position}/{total} · {case_id} · {status}")
                    status_line.caption("Tamamlanan başarılı/başarısız vakalar checkpoint olarak hemen diske yazılır.")

                with st.spinner("Sorular gerçek pipeline üzerinden çalıştırılıyor; geçici hata bir sonraki soruyu durdurmaz..."):
                    results, evidence, report = run_live_evaluation_with_evidence(
                        engine,
                        cases_path,
                        checkpoint_dir=output_dir,
                        resume=True,
                        continue_on_error=True,
                        progress_callback=on_progress,
                    )
                    paths = export_live_evaluation_evidence(evidence, report, output_dir)
                progress.progress(100, text="Tamamlandı")
                passed = sum(result.passed for result in results)
                runtime_errors = sum(item.status == "runtime_error" for item in evidence)
                a, b, c, d = st.columns(4)
                a.metric("Toplam", len(results))
                b.metric("Başarılı", passed)
                c.metric("Başarı oranı", f"{passed / len(results) * 100:.1f}%" if results else "0%")
                d.metric("Runtime hata", runtime_errors)
                st.markdown(report)
                if runtime_errors:
                    st.warning("Bazı sorular runtime_error ile kaydedildi. Ollama çalışıyorsa aynı butona tekrar basın; tamamlanan sorular atlanır ve yalnızca runtime_error vakaları yeniden denenir.")
                else:
                    st.success("100 soruluk koşu runtime hatasız tamamlandı.")
                st.success(f"Kanıt dosyaları: {paths['html'].parent}")
                st.download_button("HTML raporunu indir", paths["html"].read_bytes(), file_name=f"{provider}_evaluation_report.html", mime="text/html")
                st.download_button("CSV sonuçlarını indir", paths["csv"].read_bytes(), file_name=f"{provider}_live_results.csv", mime="text/csv")
            except Exception as exc:
                st.error(str(exc))

with system_tab:
    st.subheader("Üç çalışma seçeneği")
    st.markdown(
        """
| Mod | Gereksinim | Amaç |
|---|---|---|
| Demo | Ek kurulum yok | Hazır arayüz ve kanıtları inceleme |
| Groq | İnternet + API anahtarı | Hızlı canlı LLM testi |
| Ollama | Ollama + yerel model | Tamamen yerel canlı LLM testi |
"""
    )
    st.code(f"Vector DB: {VECTOR_DB_DIRECTORY}\nOutput: {OUTPUT_DIRECTORY}\nActive mode: {provider}\nTop-k: {top_k}\nMax distance: {max_distance}")
    st.markdown("**Tek komutlar**")
    st.code(
        "streamlit run app.py\n"
        "python scripts/index_documents.py --input-dir data/sample\n"
        "python scripts/run_live_evaluation.py --provider groq\n"
        "python scripts/run_live_evaluation.py --provider ollama\n"
        "python scripts/run_reproducible_offline_evidence.py\n"
        "pytest -q",
        language="bash",
    )
    st.info("Bu uygulama eğitim ve araştırma amaçlıdır; yatırım tavsiyesi üretmez ve işlem açmaz.")
