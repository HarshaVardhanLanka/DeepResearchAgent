

# 🤖 Open Deep Research Agent

### An Autonomous AI Researcher powered by LangGraph, Tavily, and OpenRouter.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://deepresearchagent-mffwgepvlhywhla8tosr8z.streamlit.app/)

##  Overview

The **Open Deep Research Agent** is not just a chatbot—it is an autonomous research assistant designed to perform in-depth web analysis and document synthesis. Unlike standard LLMs that rely solely on training data, this agent actively browses the web, verifies facts, and compiles structured reports with citations.

It features a **Memory System** backed by MongoDB to store your research history and supports **PDF Analysis** to combine internal documents with external web knowledge.

---

##  System Requirements

Since this agent relies on **Cloud APIs** (OpenRouter, Tavily) for the heavy computational lifting, it is lightweight to run locally. You do **not** need a high-end GPU.

###  Hardware Requirements
*   **Processor (CPU):** Minimum Dual-core processor (Intel i3/Ryzen 3 or equivalent).
*   **RAM:** 4 GB minimum (8 GB recommended for smoother PDF processing).
*   **Storage:** At least 500 MB free space (for libraries and temporary PDF storage).
*   **Internet Connection:** **Critical.** A stable broadband connection is required as the agent constantly communicates with external APIs and the MongoDB cloud database.
*   **GPU:** **Not Required.** (LLM inference is handled via API).

###  Software Requirements
*   **Operating System:** Windows 10/11.
*   **Python:** Version **3.11** or later versions
*   **Web Browser:** Latest version of Chrome, Firefox, Edge, or Safari.
*   **Code Editor:** VS Code (Recommended) or PyCharm for local development.
*   **Git:** To clone the repository.

---

##  Architecture & Workflow

The system is built on a **State Graph** architecture using `LangGraph`. It treats the research process as a pipeline of specialized agents passing a "State" object between them.

![Architecture Diagram](architecture_diagram.png)

###  The Workflow

The agent follows a cyclical workflow to ensure high-quality output:

```mermaid
graph LR
    User(User Input) --> Planner
    Planner(🧠 Planner Agent) -->|Generates Queries| Searcher
    Searcher(🔎 Searcher Agent) -->|Web Results| Writer
    Writer(✍️ Writer Agent) -->|Final Report| Output
    Output -->|Save| MongoDB
```

1.  **User Input:** The user provides a topic or uploads a PDF.
2.  **Planner:** Analyzes the request to determine if it's a new topic or a follow-up. Generates targeted search queries.
3.  **Searcher:** Executes the search queries using the Tavily API to gather real-time, verified sources.
4.  **Writer:** Synthesizes the search results and PDF context into a coherent, cited report.
5.  **Storage:** The session is saved to a MongoDB cloud database for persistent history.

---

##  Agent Roles 

Here is how the individual components interact to form the intelligent system:

###  Planner
The **Planner** acts as the strategist. It is responsible for decision-making before any action is taken.
*   **Context Analysis:** It compares the current query with chat history to classify the intent.
*   **Decision Logic:** It strictly differentiates between a **Follow-up** (bridging context) and a **New Topic** (ignoring history to prevent hallucinations).
*   **Output:** It generates precise, optimized search queries rather than generic text.

###  Writer / Executor
The **Writer** serves as the synthesizer and executor. It transforms raw data into human-readable insight.
*   **Adaptive Formatting:** It dynamically switches styles—producing concise **single paragraphs** for specific answers or detailed **Markdown reports** for deep research.
*   **Fact Verification:** It ensures all claims are backed by the search data.
*   **Citation Engine:** In Academic Mode, it links specific URLs to claims; in General Mode, it provides a clean summary.

###  Pipeline / Agent Flow
The system operates on a linear state graph built with **LangGraph**:

1.  **State Initialization:** The User Input and History are loaded into the shared State.
2.  **Plan:** The Planner Node analyzes the state and outputs a search strategy.
3.  **Execution (Search):** The Searcher Node executes the strategy using the Tavily API to gather live web content and PDF context.
4.  **Synthesis:** The Writer Node compiles the gathered data into the final response.
5.  **Persistence:** The final state is saved to the **MongoDB Cloud** for long-term memory.

---

## 🧠 Memory & History Management

The Open Deep Research Agent features a robust, persistent memory system designed to handle long-term research data without "context pollution."

### 1. Cloud Storage (MongoDB Atlas)
Unlike simple chatbots that lose data when the tab closes, this agent uses **MongoDB Atlas (Cloud Database)** for persistent storage.
*   **Auto-Save:** Every research query, generated report, and chat exchange is automatically securely saved to the cloud.
*   **Cross-Device:** Since data is cloud-hosted, you can access your research history from any device or browser.
*   **Management:** Users can **View** past reports, **Resume** old conversations, or **Delete** irrelevant entries permanently from the database.

### 2. Smart Context Logic
To maintain high performance and accuracy, the agent uses a **Sliding Window Strategy**:
*   **Token Optimization:** The agent actively recalls the full text of the **last 2 exchanges** for immediate follow-ups.
*   **Context Truncation:** Older messages (up to 10) are summarized or truncated. This prevents the "Ghosting Effect" (where the AI gets confused by old, irrelevant topics).
*   **Topic Isolation:** The **Planner Agent** intelligently analyzes new queries. If it detects a **New Topic** (unrelated to history), it forces the system to ignore previous context, ensuring a fresh, unbiased search.

---


### 🔗 Access the Live Agent
**[Click Here to Start Researching](https://deepresearchagent-mffwgepvlhywhla8tosr8z.streamlit.app/)**

---

### 💻 Local Setup Guide (Execute each line seperately)

1. **Clone the Repo:**
   ```bash
   git clone https://github.com/HarshaVardhanLanka/DeepResearchAgent.git
   cd DeepResearchAgent
   ```
   
2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
3. **Install Requirements:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Secrets:**
   Create a `.streamlit/secrets.toml` file:
   ```toml
   OPENROUTER_API_KEY = "sk-..."
   TAVILY_API_KEY = "tvly-..."
   MONGO_URI = "mongodb+srv://..."
   ```

5. **Run the App:**
   ```bash
   streamlit run app.py
   ```
   
