# Integrations & Ecosystem

Projects built on yasbd, from spaCy pipelines to medical text and real-time translation.

> [!NOTE]
> This list isn't exhaustive. It only shows integrations we know about. If you've built something on yasbd, open a PR and add it here.

* 🔵 **[spaCy Component](https://github.com/speedyk-005/yasbd-lib/blob/main/README.md#spacy-component):** Plug `yasbd` straight into any spaCy v3+ pipeline as a fast sentence segmenter.
* 📦 **[Lang Packs](https://github.com/speedyk-005/yasbd-lib/blob/main/README.md#-lang-packs):** Plug in modular rule sets (like `yasbd-auxlang`) for extended language support.
* 🧩 **[chunklet-py](https://speedyk-005.github.io/chunklet-py/latest/supported-languages/):** Powers polyglot RAG document chunking as the core SBD workhorse.
* 🏥 **[OpenMed](https://github.com/maziyarpanahi/openmed/blob/master/docs/analyze-text.md):** Integrates `yasbd` as a specialized backend for medical text segmentation.
* 🎙 **[LiveTranslate](https://github.com/TheDeathDragon/LiveTranslate/blob/main/i18n/CHANGELOG_en.md#2026-08-17):** Real-time audio translation for Windows using yasbd-lib for incremental ASR sentence segmentation.
* 🏠 **[wyoming_openai](https://github.com/roryeckel/wyoming_openai#overview):** OpenAI-compatible Wyoming proxy that uses yasbd for incremental TTS streaming via sentence boundary chunking.
* 🇭🇹 **[kreyolib](https://github.com/AyitiDev/kreyolib#sentence-splitter-api):** A software library for Haitian Creole (Kreyòl Ayisyen) natural language processing, text normalization, and localization. Currently in alpha. Uses yasbd for sentence boundary detection as part of its NLP tooling.
* 📑 **[prosediff](https://github.com/raffaelemancuso/prosediff):** Side-by-side prose diff for Word, OpenDocument, and Markdown that restores tracked changes, detects sentence offsets with yasbd, and uses AI to evaluate edits.
* 🕵️‍♂️ **[scout](https://github.com/abraham-jacob/scout):** An AI agent that locally scrapes and scores LinkedIn jobs, using yasbd to deterministically split descriptions into sentence units so the LLM can safely drop boilerplate without altering the text.
