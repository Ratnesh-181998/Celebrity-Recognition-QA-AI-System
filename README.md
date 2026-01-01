# 🧠 Celebrity Recognition & Q/A AI System
### *Multimodal Biometric Intelligence & Contextual AI Assistant*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://appudtzei3tyyttd6xjhwur.streamlit.app/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Groq AI](https://img.shields.io/badge/AI-Groq%20LLaMA--4-purple)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Container-Docker-blue)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Orchestration-GKE-4285F4)](https://cloud.google.com/kubernetes-engine)

---

<img width="940" height="486" alt="image" src="https://github.com/user-attachments/assets/e3a65503-355d-488c-800b-6a25ac582e2a" />

---
## 🚀 Project Overview

The **Celebrity Recognition & QA AI System** is a state-of-the-art multimodal application that combines computer vision with Large Language Models (LLMs) to detect identities and answer questions about them in real-time.

Built with **Streamlit** for the frontend and a **Flask** microservices backend, this system leverages **OpenCV** for facial detection, **Vision Transformers (ViT)** for biometric encodings, and **Groq's LLaMA-4 Vision** model to provide rich, context-aware information about recognized personalities.

---
## 🌐🎬 Live Demo
🚀 **Try it now:**
- **Streamlit Profile** - https://share.streamlit.io/user/ratnesh-181998
- **Project Demo** - https://celebrity-recognition-q-ai-system-nlan8szprudhrz9ctaappgxa.streamlit.app/
---

**Key Features:**
*   **Real-time Face Detection**: High-accuracy detection using OpenCV.
*   **Instant Identification**: Matches faces against a vector database of celebrity embeddings.
*   **Intelligent Q/A**: Ask *anything* about the detected person (career, movies, net worth) and get instant AI-generated answers.
*   **Cloud-Native Architecture**: Designed for scalability with Docker and Kubernetes (GKE).

---

## 🎬 Live Project Demo

> Experience the full flow: **Upload/Select -> Detect -> Interact**

![Project Demo Walkthrough](demo_walkthrough.gif)

---

## 🏗️ System Architecture

<img width="997" height="524" alt="image" src="https://github.com/user-attachments/assets/124df920-9792-4f49-a011-d3f91f030702" />


The project follows a decoupled Microservices architecture to ensure scalability and maintainability.

<img width="1327" height="215" alt="image" src="https://github.com/user-attachments/assets/25af5400-e90b-425c-9e23-ca0ed8039d6d" />

<img width="1380" height="229" alt="image" src="https://github.com/user-attachments/assets/79432472-55b4-41c7-82c6-ad7021dacbc3" />

---

### 🧠 Intelligence Layer
*   **Vision Transformer (ViT)**: Converts facial features into 128-dimensional dense vector embeddings for precise ID matching.
*   **Groq LLaMA-4 Vision**: A multimodal LLM that ingests identity context and user queries to generate human-like responses with near-zero latency.

---

## 🖥️ UI & Tab Description

The application is organized into comprehensive tabs for ease of use and transparency:

### 1. 📂 Demo Project (Main Interface)
*   **Interactive Gallery**: Choose from high-quality sample images (e.g., *Robert Downey Jr., Scarlett Johansson*).
*   **Smart Upload**: Drag-and-drop your own images for analysis.
*   **Live Detection**: One-click process to detect faces and identify celebrities.
*   **Chat with "RatneshAI"**: A built-in chatbot that holds context about the detected celebrity. Ask *"What is his best movie?"* and get an answer specific to Robert Downey Jr.
*   **Refresh Utility**: Instantly reset sessions to test new scenarios.

<img width="1899" height="845" alt="image" src="https://github.com/user-attachments/assets/ca4a8cd4-e0de-49a0-92e9-7673a8db00da" />
<img width="1832" height="824" alt="image" src="https://github.com/user-attachments/assets/335f158c-7f6a-433a-b677-a1aa5c88e882" />
<img width="1869" height="802" alt="image" src="https://github.com/user-attachments/assets/c43c3afb-8464-491d-98c2-4aa60717065c" />
<img width="1898" height="868" alt="image" src="https://github.com/user-attachments/assets/8ab05900-1e8e-4e98-8547-15657cde0e6e" />
<img width="1883" height="844" alt="image" src="https://github.com/user-attachments/assets/2fd054cd-2788-4750-bc6c-ff1d2b4c0015" />

### 2. 📝 About Project
*   Contains the **Project Explanation**, detailing the problem statement, solution approach, and high-level design doc (HLD).
*   Ideal for stakeholders to understand the business value.
<img width="1866" height="857" alt="image" src="https://github.com/user-attachments/assets/4f30418e-e536-44f5-9c80-d486021debc8" />
<img width="1881" height="844" alt="image" src="https://github.com/user-attachments/assets/c1c6349b-c79a-4d77-a96c-dcf8505eb39f" />
<img width="1280" height="714" alt="image" src="https://github.com/user-attachments/assets/51aa865a-6521-4053-b93b-0ac981754e37" />
<img width="1657" height="673" alt="image" src="https://github.com/user-attachments/assets/1d0f8537-853f-4943-b94e-8d4ecaed24a8" />


### 3. 🛠️ Tech Stack
Breakdown of the modern stack used, categorized by layer:
*   **🧠 Intelligence**: Groq API, Vision Transformers, PyTorch.
*   **💻 Application**: Streamlit (Frontend), Flask (Backend), RESTful APIs.
*   **☁️ DevOps/LLMOps**: Google Kubernetes Engine (GKE), Docker, CircleCI, Artifact Registry.
*   
<img width="1865" height="830" alt="image" src="https://github.com/user-attachments/assets/5141b4b0-c25a-405c-836e-6a654133def6" />

### 4. 📐 Architecture
*   Visualizes the **High-Level Design (HLD)** and data flow using Graphviz.
*   Explains the request lifecycle from browser to AI inference.
  
<img width="1629" height="800" alt="image" src="https://github.com/user-attachments/assets/dd5358e7-e43e-4c4d-b570-6c0de2849156" />
<img width="1224" height="538" alt="image" src="https://github.com/user-attachments/assets/6e2e3c17-543d-4bb4-8ccf-a20439516edc" />
<img width="1671" height="753" alt="image" src="https://github.com/user-attachments/assets/79130010-71fe-44b0-aa68-ff4d1e1e91ab" />
<img width="1668" height="831" alt="image" src="https://github.com/user-attachments/assets/bd2c66ae-b842-4162-b2ff-dbefe92cf698" />
<img width="1658" height="836" alt="image" src="https://github.com/user-attachments/assets/69913572-3b09-4cff-9ea3-a009db2a44e6" />

### 5. 📡 System Logs
*   Real-time **stdout/stderr** streaming.
*   Monitors connectivity, API status, and error tracing for debugging.
<img width="1667" height="819" alt="image" src="https://github.com/user-attachments/assets/5a9c16d8-e1cc-4c28-aeba-5d314ac958de" />
<img width="1670" height="819" alt="image" src="https://github.com/user-attachments/assets/d498a485-d75e-4225-99cd-2e81cfa4da02" />

---

## 🛠️ Technology Stack

| Domain | Technologies Used |
| :--- | :--- |
| **Frontend** | Streamlit, HTML5, CSS3 Custom Components |
| **Backend** | Flask, Python 3.9+, REST APIs |
| **Computer Vision** | OpenCV (Haar Cascades), Pillow |
| **AI / ML** | Vision Transformers (ViT), Groq LLaMA-4 Vision |
| **Database** | Vector Store (In-memory/FAISS compatible logic) |
| **DevOps/LLMOps/AIOps** | Docker, Kubernetes (GKE), Git LFS, CircleCI |
| **Cloud** | Streamlit Cloud, Google Cloud Platform (GCP) |

---

## ⚙️ Installation & Setup

### Prerequisites
*   Python 3.9 or higher
*   Git (with LFS support)
*   Standard Python development environment

### 1. Clone the Repository
```bash
git clone https://github.com/Ratnesh-181998/Celebrity-Recognition-QA-AI-System.git
cd Celebrity-Recognition-QA-AI-System
```

### 2. Install Dependencies
This project uses `git lfs` for large model files. Ensure it is installed:
```bash
git lfs install
git lfs pull
```
Install python libraries:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file (or use Streamlit Secrets) with your API keys:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Run Locally
```bash
streamlit run "Celebrity Detector_QA_streamlit_app.py"
```
---

## ☁️ Deployment

### Streamlit Cloud
1.  Push this repo to GitHub.
2.  Login to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Connect your GitHub account and select this repository.
4.  Set the `GROQ_API_KEY` in the **Advanced Settings > Secrets** section.
5.  Click **Deploy**.

*Note: The `requirements.txt` is optimized for cloud environments, including `opencv-python-headless`.*

---

## 🚀 DevOps/LLMops & CI/CD Pipeline (GCP & CircleCI)

This project uses a robust CI/CD pipeline integrated with **CircleCI** and **Google Kubernetes Engine (GKE)** for automated deployment.

### 🔄 Pipeline Workflow
1.  **Commit**: Code is pushed to GitHub.
2.  **CircleCI Trigger**: The pipeline automatically builds the Docker image.
3.  **Container Registry**: The image is pushed to **Google Artifact Registry**.
4.  **Deployment**: The updated image is deployed to the **GKE Cluster**.

### 🐳 Docker Configuration
The application is containerized using a lightweight **Python 3.10-slim** image with optimized layers:

*   **Base Image**: `python:3.10-slim`
*   **System Deps**: `libgl1`, `libglib2.0-0` (for OpenCV)
*   **Optimization**: `PYTHONDONTWRITEBYTECODE=1` for performance.
*   **Port**: Exposes `5000` for the Flask backend.

### ☁️ GCP Deployment Requirements
For a full enterprise-grade deployment on Google Cloud, ensure:
1.  **APIs Enabled**: Kubernetes Engine, Container Registry, Cloud Build.
2.  **Service Account**: With `Storage Admin` and `Artifact Registry Writer` roles.
3.  **Secrets Management**: `GROQ_API_KEY` injected via Kubernetes Secrets.

> *For detailed step-by-step documentation on setting up the GCP environment and CircleCI pipeline, check the `FULL_DOCUMENTATION.md` file in this repository.*


---

## 🗺️ Roadmap & Future Enhancements

*   [ ] integration of Live Webcam Feed for real-time video detection.
*   [ ] Expansion of Celebrity Database (currently 10k+ identities).
*   [ ] Multi-language support for Q/A.
*   [ ] Mobile-Optimized Layout.

        
---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` file for more information.

> **MIT License Summary**: You can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, provided you include the original copyright notice.

---

## 📞 Contact & Links

**Ratnesh Kumar Singh | Data Scientist (AI/ML Engineer 4+ Yrs Exp)**

*   💼 **LinkedIn**: [ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)
*   🐙 **GitHub**: [Ratnesh-181998](https://github.com/Ratnesh-181998)

### 🔗 Quick Links
*   🌐 **Live Demo App**: [Launch Streamlit App](https://celebrity-recognition-q-ai-system-nlan8szprudhrz9ctaappgxa.streamlit.app/)
*   📖 **Project Wiki**: [Documentation](https://github.com/Ratnesh-181998/Celebrity-Recognition-QA-AI-System/wiki)
*   🐛 **Report a Bug**: [Issue Tracker](https://github.com/Ratnesh-181998/Celebrity-Recognition-QA-AI-System/issues)
*   💬 **Join Discussion**: [Community Chat](https://github.com/Ratnesh-181998/Celebrity-Recognition-QA-AI-System/discussions)

---
*Built with ❤️ by Ratnesh using Generative AI & Computer Vision.*
