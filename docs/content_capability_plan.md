# LinkedIn API Capabilities & Finalized Content Plan

## 1. Official LinkedIn API Capability Audit

Based on your active developer product tier (**Share on LinkedIn** default access), here is the technical breakdown of what is natively supported via API versus restricted:

| Content Type | API Support Status | Endpoint Used | Automation Implementation Strategy |
|---|---|---|---|
| **Text Posts** | **Supported** | `POST https://api.linkedin.com/rest/posts` | Direct commentary text dispatch. |
| **Image Posts** | **Supported** | `POST https://api.linkedin.com/rest/assets?action=registerUpload` | Upload image binary, get media asset URN, attach to post. |
| **Video Posts** | **Supported** | `POST https://api.linkedin.com/rest/assets?action=registerUpload` | Upload video binary, get asset URN, attach to post. |
| **Native Polls** | **API Restricted** | Not supported in basic tier | **Simulated Text Polls**: Format as "Option A vs Option B" in text body, prompting users to comment their vote. |
| **Article / Link Previews** | **Supported** | `POST https://api.linkedin.com/rest/posts` | Attach article URL in distribution or place in first comment. |

---

## 2. Finalized Weekly Content Mix Strategy

To maximize reach while operating within basic API access, content is structured into four distinct formats:

```
+-------------------------------------------------------------------+
|                     WEEKLY CONTENT DISTRIBUTION                   |
+-------------------------------------------------------------------+
|  [80%] Serious Technical Breakdowns (GitHub Trends & AI Systems)  |
|  [10%] Text-Based Engineering Memes & Dev Anecdotes               |
|  [5%]  High Quality Image-Based Memes                             |
|  [5%]  Simulated Text-Based Interactive Choice Polls              |
+-------------------------------------------------------------------+
```

---

## 3. 7-Day Content Execution Schedule

| Day | Content Category | Format Type | Content Focus & Objective |
|---|---|---|---|
| **Monday** | Serious Technical | Text + Code Snippet | GitHub Trending Repo Breakdown (Architecture & performance analysis). |
| **Tuesday** | Simulated Text Poll | Text Only | Tech Debate (e.g., "Postgres vs DuckDB for real-time analytics. Comment A or B"). |
| **Wednesday**| Serious Technical | Text + Architecture Diagram | Deep Dive into AI Agent Frameworks (LangGraph, AutoGen, CrewAI). |
| **Thursday** | Text Meme | Text Only | Relatable developer observation or code review anecdote. |
| **Friday** | Serious Technical | Text + Image Chart | System Design benchmark or LLM latency optimization strategy. |
| **Saturday** | Image Meme | Text + Image Asset | High quality, clean software engineering meme graphic. |
| **Sunday** | Serious Technical | Text Only | Weekly AI & Open-Source Roundup (Summary of top 3 breakthroughs). |

---

## 4. Native Poll vs Simulated Poll Mechanics

Since native LinkedIn Poll cards require restricted enterprise endpoints, the engine executes **Simulated Choice Polls** via text commentary:

### Simulated Poll Template:
```
System Design Debate: REST vs gRPC for internal microservices.

Option A: REST (Simplicity, standard tooling, easy debugging)
Option B: gRPC (HTTP/2, Protobuf serialization, strict contracts)

Drop your choice (A or B) and your reasoning in the comments below!
```

**Algorithmic Benefit**: Comments carry higher algorithmic weight than native poll clicks, giving simulated text polls greater organic feed distribution.
