# EduMAS Video Storyboard & Production Guide

## Scene-by-Scene Breakdown

| Time | Duration | Scene | Voiceover | Visual Elements | Notes |
|------|----------|-------|-----------|-----------------|-------|
| 0:00-0:15 | 15s | **Opening** | Introduce EduMAS & promise | System dashboard, AI effects, animated title | Upbeat, professional tone |
| 0:15-0:45 | 30s | **The Problem** | Why education needs automation | Manual grading, papers piling up, stressed teacher | Relatable, shows pain point |
| 0:45-1:30 | 45s | **Agent 1: Coordinator** | Coordinator fetches Wikipedia | Coordinator icon, Wikipedia data flowing in, JSON summary | Show wiki API call |
| 1:30-1:50 | 20s | **Agent 2: Quiz Generator** | Generates 5 MCQ questions | Quiz icon, 5 questions appearing, difficulty indicators | Show actual quiz JSON |
| 1:50-2:00 | 10s | **Agent 3: Grader** | Student submits, grades | Grader icon, student answers vs. key, checkmarks/X marks | Simple comparison |
| 2:00-2:20 | 20s | **Agent 4: Report Writer** | Compiles final report | Report icon, JSON report appearing, timestamp | Show final output |
| 2:20-3:10 | 50s | **The 4 Tools** | Explain each tool role | Tool icons connecting to agents (Wikipedia, File Saver, Scorer, Compiler) | Highlight integration |
| 3:10-4:00 | 50s | **Full Pipeline Animation** | Data flows through all 4 agents | Animated flow: Student Input → Coordinator → Generator → Grader → Writer → Report | Use arrows, color coding |
| 4:00-4:40 | 40s | **Key Features** | Zero cost, privacy, tested, extensible | Icons for: 💰 Cost, 🔒 Privacy, ✅ Tests, 🔧 Extensible | Feature highlights |
| 4:40-4:55 | 15s | **Benefits Summary** | Recap advantages | Dashboard screenshot, report output, logo | Professional conclusion |
| 4:55-5:00 | 5s | **Closing** | Call to action or closing message | EduMAS logo, credits rolling | Fade to black |

---

## Visual Elements Checklist

### Diagrams to Create
- [ ] **Pipeline Flowchart** – 4 boxes (Coordinator → Quiz Gen → Grader → Report Writer) with arrows
- [ ] **Data Flow Diagram** – Show input (topic) flowing through pipeline to output (report)
- [ ] **Agent-Tool Matrix** – Show which tool each agent uses
- [ ] **System Architecture** – Full technical overview

### Screenshots/Screen Recordings
- [ ] Terminal running `python main.py`
- [ ] Wikipedia API response (JSON)
- [ ] Generated quiz.json file
- [ ] Sample student answers form
- [ ] Final report_*.json output
- [ ] (Optional) React dashboard screenshot

### Icons/Graphics
- [ ] 📋 Coordinator Agent icon
- [ ] ❓ Quiz Generator icon
- [ ] ✏️ Grader Agent icon
- [ ] 📄 Report Writer icon
- [ ] 🌐 Wikipedia tool icon
- [ ] 💾 File Save tool icon
- [ ] 🧮 Scoring tool icon
- [ ] 📋 Report Compiler tool icon

### Text Overlays
- [ ] "EduMAS: Educational Multi-Agent System"
- [ ] "Zero Cloud Costs"
- [ ] "Privacy-First Design"
- [ ] "54 Unit Tests"
- [ ] "Built on CrewAI + Ollama"
- [ ] "4 Agents. 4 Tools. 1 Pipeline."

---

## Technical Specs for Recording

| Parameter | Value |
|-----------|-------|
| **Resolution** | 1920x1080 (Full HD) or 2560x1440 (4K) |
| **Frame Rate** | 30 fps (recommended) or 60 fps (premium) |
| **Audio Sample Rate** | 48 kHz (video standard) |
| **Bitrate** | 8-12 Mbps (H.264) |
| **File Format** | MP4 (H.264) or WebM (VP9) |
| **Codec** | H.264 or H.265 (HEVC) |

---

## Recording Software Recommendations

### Free Options
- **OBS Studio** – Best for full pipeline + voiceover recording
- **ScreenFlow** (Mac) – Intuitive screen capture
- **Camtasia** – Easier editing, paid but worth it

### Workflow
1. **Screen Recording Phase**
   - Record main pipeline execution (1-2 minutes)
   - Record individual agent outputs
   - Record final report generation
   
2. **Voiceover Phase**
   - Record narration in quiet environment (use audio editor)
   - Use professional microphone (USB condenser or headset)
   - Record in Audacity or Adobe Audition
   
3. **Editing Phase**
   - Combine screen recording + voiceover
   - Add animated transitions (2-3s between scenes)
   - Add background music (keep volume -20dB)
   - Export to MP4

---

## Music & Sound Recommendations

### Background Music (Royalty-Free Sources)
- **Epidemic Sound** – High quality, professional
- **AudioJungle** – Affordable one-time licenses
- **YouTube Audio Library** – Free, limited selection
- **Incompetech** – Free, good variety

**Suggested Genre**: Upbeat tech/corporate background (130-150 BPM)

**Volume**: -20 to -15 dB (ducked low)

### Sound Effects (Optional)
- Smooth transitions: "whoosh" sound (very subtle)
- Data flowing: "digital" or "data stream" sound
- Agent activation: "ding" or "alert" tone
- Report generation: "paper" or "print" sound

---

## Text Overlay Style Guide

### Font Recommendations
- **Headlines**: Bold sans-serif (Montserrat Bold, Inter Bold)
- **Body Text**: Regular sans-serif (Open Sans, Roboto)
- **Tech Terms**: Monospace (Monaco, JetBrains Mono) – for code snippets

### Color Scheme
- **Primary**: Dark blue (#1a365d) for text
- **Accent 1**: Bright cyan (#00d9ff) for agent highlights
- **Accent 2**: Lime green (#00ff41) for success/checkmarks
- **Accent 3**: Orange (#ff6b35) for warnings/important
- **Background**: White (#ffffff) or very dark gray (#0f1419)

---

## Content Outline with Timestamps

```
0:00-0:15   [OPENING]
  └─ What is EduMAS? (AI-powered quiz system)
  
0:15-0:45   [PROBLEM & SOLUTION]
  └─ Why education needs automation
  └─ Zero-cost, privacy-first approach
  
0:45-2:20   [THE 4 AGENTS]
  ├─ 1:00-1:30  Agent 1: Coordinator (Wikipedia fetcher)
  ├─ 1:30-1:50  Agent 2: Quiz Generator (Creates 5 MCQs)
  ├─ 1:50-2:00  Agent 3: Grader (Scores answers)
  └─ 2:00-2:20  Agent 4: Report Writer (Compiles report)
  
2:20-3:10   [THE 4 TOOLS]
  └─ Wikipedia API
  └─ File Saver
  └─ Answer Scorer
  └─ Report Compiler
  
3:10-4:00   [FULL PIPELINE ANIMATION]
  └─ Student input → Final report (complete flow)
  
4:00-4:40   [KEY FEATURES]
  └─ Zero cost
  └─ Privacy-first
  └─ Fully tested (54 tests)
  └─ Open-source
  └─ Extensible
  
4:40-5:00   [CLOSING]
  └─ Call to action
  └─ Logo/branding
```

---

## Optimization Tips

### For YouTube Upload
1. **Metadata**
   - Title: "EduMAS: How AI Creates Quizzes Automatically | CrewAI + Ollama"
   - Description: Include GitHub link, tech stack, timestamps
   - Tags: crewai, ollama, ai, education, python, multi-agent, llm
   - Thumbnail: Bold text "EduMAS" + agent icons

2. **Captions**
   - Auto-generate via YouTube, then edit for accuracy
   - Add timestamps for each section
   - Highlight technical terms

3. **SEO Optimization**
   - Keyword: "multi-agent system", "local AI", "education automation"
   - Include CrewAI and Ollama in description (for searchability)

---

## Production Timeline (Estimated)

| Phase | Time | Tasks |
|-------|------|-------|
| **Planning** | 1-2 hrs | Script review, visual planning, asset gathering |
| **Preparation** | 2-3 hrs | Create diagrams, capture screenshots, record system demos |
| **Recording** | 2-3 hrs | Screen recording + voiceover narration |
| **Editing** | 3-4 hrs | Sync audio, add transitions, color grade, effects |
| **Review & Export** | 1-2 hrs | QA, final adjustments, export to MP4 |
| **Upload & Optimization** | 1 hr | Upload to YouTube, add metadata, optimize |
| **Total** | **10-15 hrs** | Professional quality 5-minute video |

---

## Common Recording Mistakes to Avoid

❌ **Don't**: Record with background noise (fans, traffic, pets)  
✅ **Do**: Record in a quiet room during off-peak hours

❌ **Don't**: Use tiny fonts (< 24pt) on screen  
✅ **Do**: Increase font size to 36pt+ for readability

❌ **Don't**: Talk too fast or too slow  
✅ **Do**: Aim for 150 words/minute with natural pacing

❌ **Don't**: Use overly colorful or clashing color schemes  
✅ **Do**: Stick to 3-4 colors max for cohesion

❌ **Don't**: Jump between scenes too quickly  
✅ **Do**: Use 2-3 second transitions to let visuals breathe

❌ **Don't**: Forget about captions/accessibility  
✅ **Do**: Add captions for hearing-impaired viewers

---

## Example Script with Timings

**[0:00-0:15]** "Imagine an intelligent system that automatically creates quizzes, grades them, and generates detailed reports—all running locally. That's EduMAS." *[Show dashboard, zoom in on key components]*

**[0:45-1:30]** "The Coordinator Agent fetches accurate information from Wikipedia. Watch as it pulls real data..." *[Animate Wikipedia icon, show JSON response]*

---

## Next Steps

1. ✅ Review and approve script
2. ⏳ Create or gather visual assets
3. ⏳ Set up recording environment
4. ⏳ Record screen + voiceover
5. ⏳ Edit and sync audio
6. ⏳ Add graphics and effects
7. ⏳ Export and upload

