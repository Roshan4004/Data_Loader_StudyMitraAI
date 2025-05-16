# 📄 data_loader (StudyMitraAI)

This repo contains the **embedding microservice** for [StudyMitraAI](https://github.com/Roshan4004/StudyMitraAI).

This data_loader section of that project does:

- Ingests PDFs (e.g. textbooks, notes)
- Chunks and embeds using HuggingFace Sentence Transformers
- Saves to a FAISS (or Qdrant/Chroma) vector store
- Powered by FastAPI, meant to be run **locally**

📂 Outputs embeddings to: `../vector_store/`

---

⚠️ This is **not a user-facing repo** — it's a development microservice just to showcase how data from google drive is loaded, chuncked and then embedded for an application.

See the full app: [StudyMitraAI →](https://github.com/Roshan4004/StudyMitraAI)
