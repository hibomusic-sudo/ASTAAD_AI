# AI Rage - Somali Educational AI Platform 🚀

Welcome to the **AI Rage** repository! This project is an advanced, AI-driven educational platform built on top of the open-source **DeepTutor** framework. It is specifically designed to provide high-quality tutoring and guidance to Somali students in their native language, focusing on **Vibe Coding, AI Automation, Video Editing, and Basic Programming**.

## 🌟 Key Features

- **Somali-Native AI Agent**: A custom-tailored LLM persona ("AI Rage") that communicates flawlessly in Somali, maintaining a respectful, engaging, and professional teaching style.
- **Multi-Channel Integration**: Chat with the bot natively across popular platforms without downloading a new app:
  - 📱 Telegram Bot
  - 💬 Facebook Messenger
- **Automated Curriculum & Knowledge Base (RAG)**: Uses Retrieval-Augmented Generation (RAG) to fetch course materials from PDFs, Youtube Transcripts, Loom Videos, and Whop lessons, ensuring students get accurate, curriculum-specific answers without hallucinations.
- **Interactive Course Navigation**: The bot presents students with Native Telegram Menus/Buttons to easily navigate between courses, quizzes, and community groups.
- **Smart Quiz Evaluator**: Automatically assesses student quiz results and distributes the correct VIP group links upon successful graduation.
- **Scheduled Broadcasting (Cron)**: Automated weekly schedule announcements to keep students on track with their classes.

## 🔗 Supported Communities & Courses

AI Rage seamlessly connects students to our vibrant communities based on their learning paths:
*   **AI BOT (Automation) 4 Days Course**
*   **AI Video Editing Mastery**
*   **Fasalka Barashada AI**
*   **Loom & Himbomusic Workspaces**

## ⚙️ Technical Architecture

AI Rage is built as a **Level 2 Capability Plugin** inside the DeepTutor agent-native architecture:

```text
DeepTutor Engine
├── Capabilities (Multi-step Agent Pipelines)
│   └── AI Rage (Custom Somali Persona & Tools)
│       ├── CommunityLinksTool (Interactive UI)
│       ├── ScheduleTool (CRUD Class Management)
│       └── ClassworkTool (Course Management)
├── Tools (Level 1)
│   └── RAG (Knowledge Base Retrieval)
└── Channels
    ├── Telegram (Long-polling, Inline Keyboards)
    └── Facebook (Webhook)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd DeepTutor
   ```

2. Install dependencies:
   ```bash
   pip install -e ".[tutorbot]"
   ```

3. Setup Environment Variables:
   Create a `.env` file in the root directory and add your LLM API keys (e.g., `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`).

4. Configure the Bot:
   Edit `data/tutorbot/ai_rage/config.yaml` to include your Telegram Token and Facebook Webhook tokens.

5. Run the Server:
   ```bash
   python -m deeptutor_cli.main serve
   ```
   The bot will automatically connect to Telegram and start listening for messages!

## 🎓 Ingestion (Adding Course Materials)

To add new PDFs or lessons to the AI's brain (RAG):
```bash
python -m deeptutor_cli.main kb create ai_rage_tutorials --doc path/to/your/lesson.pdf
```

---
*Built with ❤️ for the Somali Tech Community.*
