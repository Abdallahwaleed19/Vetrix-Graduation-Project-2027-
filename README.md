# 🧪 Vetrix AI — Next-Gen Veterinary Pharmaceutical LIMS

<div align="center">

![Vetrix Banner](https://img.shields.io/badge/Vetrix-AI--Powered%20LIMS-00F2FE?style=for-the-badge&logo=pharmacist&logoColor=black)
![Compliance](https://img.shields.io/badge/Compliance-CFR%2021%20Part%2011%20%7C%20GMP-10B981?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/Frontend-React.js-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Python](https://img.shields.io/badge/AI%20Core-Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Deployment-Docker%20Containers-2496ED?style=for-the-badge&logo=docker&logoColor=white)

**An Intelligent, High-Tech Laboratory Information Management System (LIMS) Tailored for Veterinary Pharmaceutical QA/QC Laboratories.**

---
</div>

## 📌 Project Overview

**Vetrix** transforms traditional, manual, paper-reliant quality control processes in veterinary pharmaceutical factories into a fully digitized, secure, and AI-enhanced ecosystem. Designed specifically to adhere strictly to **CFR 21 Part 11** and **GMP (Good Manufacturing Practice)** regulations, Vetrix establishes cryptographic data integrity, automated device readings, and predictive risk management.

### 🌟 Core Highlights
* **🔒 CFR 21 Part 11 Compliance:** Cryptographic, immutable Audit Trails, Role-Based Access Control (RBAC), and 2FA E-Signatures.
* **👁️ Computer Vision & Legacy Digitization:** YOLO-based display detection paired with EasyOCR to digitize legacy lab equipment without digital output interfaces.
* **📚 RAG Pharmacopoeia Assistant:** Vector-search (Qdrant/FAISS) semantic assistant providing instant queries against Egyptian Drug Authority (EDA) and British Pharmacopoeia Veterinary (BP Vet) standards.
* **📊 Predictive Analytics & Risk Scoring:** Machine Learning models (Random Forest / XGBoost) for Supplier & Batch Risk Scoring alongside instrument Predictive Maintenance.

---

## 🏗️ System Architecture & Workflow Pipeline

```mermaid
graph TD
    A[Sample Ingestion & QR Labeling] --> B[Visual Inspection & QC Verification]
    B --> C[Legacy Device Screen Capture]
    C --> D[YOLO Screen Detection & EasyOCR Engine]
    D --> E[FastAPI Backend Pipeline]
    E --> F[Cryptographic CFR 21 Audit Trail Engine]
    F --> G[Predictive Risk Scoring & Anomaly Detection]
    G --> H[RAG Assistant Verification against BP Vet / EDA]
    H --> I[E-Signature Approval & CoA Generation]
