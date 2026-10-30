# 🧬 Vetrix Architecture & Diagrams Documentation

Welcome to the architectural documentation repository for **Vetrix** (AI-Powered Veterinary Pharmaceutical Laboratory Information Management System). 

This directory contains all the C4 Model diagrams, Entity Relationship Diagrams (ERD), BPMN Workflows, and UML Sequence Diagrams required for technical presentation, academic evaluation, and system implementation.

---

## 📌 Executive Summary & Architectural Rules

**Vetrix** is designed with strict adherence to pharmaceutical regulatory standards (**21 CFR Part 11**):
1. **Human-in-the-Loop:** All AI capabilities (OCR, RAG, Anomaly Detection, Risk Scoring) are strictly **advisory**. Final approvals, batch releases, and Certificate of Analysis (CoA) generation require human authorization via E-Signatures.
2. **Central Integration Point:** The **FastAPI Backend API** is the single gateway to the system. The React Web Frontend never interacts directly with databases or internal AI models.
3. **Storage Separation:** Operational LIMS data is stored in **PostgreSQL**, raw document assets in **Document Storage (S3/Local)**, and vector embeddings in **FAISS Index**.

---

## 📂 Repository Contents & Diagram Index

### 1. High-Level Architecture & Context Diagrams
* **System Context Diagram (C4 Level 1):** Defines the system boundary and external actors (Analyst, QA Manager, Admin, Supervisor, Management) and external sources (Instruments, Standards).
* **C4 Container Diagram (C4 Level 2):** Illustrates the high-level deployable containers, tech stack, and network protocols.
  * 📄 *HTML Renderer included:* `vetrix_c4_clean_diagram.html` (HD interactive SVG/PNG exporter).

### 2. Internal System Components
* **Backend Component Diagram:** Decomposes the FastAPI application into a 4-Layer modular architecture:
  * `API Controllers Layer`
  * `Application / Business Logic Layer`
  * `AI Integration Layer`
  * `Data Access Layer (Repositories)`

### 3. Data Architecture
* **Entity Relationship Diagram (ERD):** A normalized (3NF) relational schema for PostgreSQL featuring:
  * `Identity & Access` (Users, Roles, RBAC)
  * `Batch & Sample Management` (Suppliers, Batches, Samples, History)
  * `Laboratory Testing & Specs` (Tests, Methods, Measurements, Spec Parameters)
  * `Quality & Compliance` (Rule-based OOS, Investigations, Actions, E-Signatures, CoAs, Audit Trail)
  * `AI Processing` (Jobs, Results, Human Confirmations)

### 4. Workflows & Sequence Modeling
* **Activity Diagrams / BPMN Workflows:**
  * `Diagram A:` Master Laboratory Lifecycle Workflow
  * `Diagram B:` OOS Investigation Subprocess Workflow
  * `Diagram C:` AI-Assisted Measurement Entry (OCR & Voice)
  * `Diagram D:` Human Review & CoA Authorization
  * `Diagram E:` AI Anomaly Detection Workflow
* **UML Sequence Diagrams:** Detailed API interaction traces covering all 5 core workflows with conditional `alt`, `opt`, and `loop` fragments.

---

## 🛠️ Technology Stack Summary

| Layer | Component | Technology |
| :--- | :--- | :--- |
| **Presentation Layer** | Frontend Web App | React.js, TypeScript, Tailwind CSS, Shadcn/UI |
| **Logic Layer** | Backend API | Python, FastAPI, Pydantic, SQLAlchemy |
| **Database Layer** | Relational DB | PostgreSQL (3NF Schema + Cryptographic Audit Trail) |
| **Vector DB** | Knowledge Storage | FAISS / Qdrant |
| **AI/ML Engines** | Vision & OCR | YOLO, PaddleOCR / EasyOCR |
| **AI/ML Engines** | NLP & GenAI | Whisper (Voice), LangChain, Text-to-SQL |
| **AI/ML Engines** | Predictive ML | Scikit-learn (Isolation Forest), XGBoost |
| **DevOps** | Containerization | Docker, Docker Compose, GitHub Actions |

---

## 🚀 How to Render and View Diagrams

### Option 1: VS Code / IDE Preview
Install the **Mermaid Preview** or **Markdown Preview Enhanced** extension to view `.md` files containing Mermaid blocks directly inside your editor.

### Option 2: Browser Interactive Renderer (Recommended for Presentations)
Open `vetrix_c4_clean_diagram.html` directly in any web browser to view, interact with, and download high-definition PNG/SVG images for your presentation slides.

### Option 3: Mermaid Live Editor
Copy any `mermaid` code block from the documentation and paste it directly into [Mermaid Live Editor](https://mermaid.live).

---

## 👥 Team Parallel Development Framework

Work is split across team members without blocking dependencies using **API Contracts** and **Mock Data**:

* **Member 1 (Backend & System Integration):** FastAPI Core, RBAC, Validation Engine, Audit Trail, E-Signatures.
* **Member 2 (Frontend Developer):** React Web App, Sample Screens, OOS Workspaces, AI Chat, Dashboards.
* **Member 3 (Data Engineer):** PostgreSQL ERD, Schema Migrations, Synthetic Dataset Generation, Docker Setup.
* **Member 4 (ML & Predictive Analytics):** Anomaly Detection Models & Supplier Risk Scoring Services.
* **Member 5 (Generative AI & NLP):** OCR Engine, Whisper Voice Entry, RAG Pharmacopoeia Assistant, Text-to-SQL.
* **Member 6 (QA & DevOps):** PyTest Suite, CI/CD Pipeline, Docker Compose, Technical Documentation.

---

## 📄 License & Confidentiality
This architecture documentation is created as part of the **Vetrix Graduation Project** for Veterinary LIMS AI implementation. All rights reserved.
