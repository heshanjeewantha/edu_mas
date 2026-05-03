# EduMAS: 5-Minute Video Script
## Educational Multi-Agent System Demo

---

## [OPENING - 0:00-0:15]

**[Scene: Show system dashboard/interface]**

> "Imagine an intelligent educational system that automatically creates quizzes, grades them, and generates detailed reports—all running locally on your computer. That's EduMAS: the Educational Multi-Agent System."

> "Today, we're walking through how this AI-powered system works, the intelligent agents behind the scenes, and why it's revolutionizing personalized learning."

---

## [THE PROBLEM - 0:15-0:45]

**[Scene: Show traditional quiz creation—manual work, papers, grading]**

> "Creating educational quizzes is time-consuming. Teachers manually research topics, write questions, grade answers, and compile reports. This takes hours."

> "What if machines could do this automatically? That's where EduMAS comes in."

> "Built on CrewAI and powered by Ollama's local AI model, EduMAS automates the entire quiz pipeline—from topic research to final grade report—without relying on expensive cloud APIs."

> "Zero cloud costs. Zero paid subscriptions. Completely open-source and privacy-first."

---

## [SYSTEM ARCHITECTURE - 0:45-2:00]

**[Scene: Animated pipeline diagram showing the flow]**

> "Let's break down how EduMAS works. At its core, it's a 4-agent pipeline working in sequence."

> "A student inputs a topic—say, 'Apples'—and a difficulty level: easy, medium, or hard."

---

### **AGENT 1: The Coordinator**

**[Scene: Show Agent 1 icon/animation]**

> "First, the Coordinator Agent springs into action. Its job: validate the topic and fetch accurate information."

> "It queries Wikipedia using the Wikipedia API tool to pull factual, grounded knowledge about the topic. This becomes the foundation for everything that follows."

> "Key principle: never invent facts. If Wikipedia doesn't have it, the Coordinator says so. Accuracy is paramount."

---

### **AGENT 2: The Quiz Generator**

**[Scene: Show Agent 2 icon/animation, then a sample quiz on screen]**

> "Next, the Quiz Generator Agent takes the topic summary and creates exactly 5 multiple-choice questions."

> "It respects Bloom's Taxonomy: easy questions test recall, medium questions test comprehension, and hard questions test application and analysis."

> "Each question has four options—A, B, C, and D—with one correct answer. The quiz is saved as a structured JSON file."

> "Again, it never invents facts. Every question is grounded in the knowledge from the Coordinator."

---

### **AGENT 3: The Grader**

**[Scene: Show Agent 3 icon/animation, show a student submitting answers]**

> "Once a student submits their answers, the Grader Agent takes over."

> "It reads the quiz, compares each student answer against the answer key, and produces a detailed scoring report."

> "It's objective, fair, and strict. The Grader returns the raw scores without modification—no partial credit unless earned."

---

### **AGENT 4: The Report Writer**

**[Scene: Show Agent 4 icon/animation, show final report on screen]**

> "Finally, the Report Writer Agent compiles everything: the topic, the student name, the quiz questions, individual question feedback, and the final score."

> "It outputs a clean, structured JSON report with a timestamp, saved to disk."

> "This report includes the overall score percentage, pass/fail status against a threshold, and detailed feedback for each question."

---

## [THE TOOLS - 2:00-3:30]

**[Scene: Show tool icons and their interactions]**

> "Behind every agent are specialized tools that handle real-world work."

> "**Tool 1: Wikipedia Fetcher** – The Coordinator uses this to fetch accurate topic summaries from Wikipedia's free API. No authentication, no costs."

> "**Tool 2: Quiz File Saver** – The Quiz Generator uses this to save the generated 5 questions as a structured JSON file to disk."

> "**Tool 3: Answer Scorer** – The Grader uses this to systematically score each student answer and produce a detailed breakdown."

> "**Tool 4: Report Compiler** – The Report Writer uses this to merge all outputs into a final, timestamped report."

> "These tools work together seamlessly, passing data down the pipeline. The coordinator's output becomes the quiz generator's input, and so on."

---

## [DATA FLOW VISUALIZATION - 3:30-4:15]

**[Scene: Animated data flow showing the pipeline end-to-end]**

> "Here's what happens when a student uses EduMAS:"

> "1. Student enters: Topic 'Apples' + Difficulty 'Medium'"

> "2. Coordinator fetches Wikipedia summary on apples"

> "3. Quiz Generator creates 5 medium-difficulty questions about apples"

> "4. Student answers all 5 questions"

> "5. Grader evaluates answers against the answer key"

> "6. Report Writer compiles results into a timestamped JSON report"

> "The entire pipeline runs in minutes. All data stays local. All processing happens on-device."

---

## [KEY FEATURES & BENEFITS - 4:15-4:50]

**[Scene: Show dashboard, test results, report output]**

> "What makes EduMAS special?"

> "**Zero Cost**: No paid APIs, no cloud subscriptions. Just open-source software."

> "**Privacy-First**: All data stays on your computer. No student data leaves your network."

> "**Extensible**: Built on CrewAI, so you can add more agents, more tools, and more sophisticated workflows."

> "**Fully Tested**: Over 50 unit tests ensure each agent and tool works reliably."

> "**Frontend Ready**: Includes a React dashboard for students to submit answers and view reports."

> "**Scalable**: Run it on a single machine or deploy across multiple instances."

---

## [CLOSING - 4:50-5:00]

**[Scene: Show the EduMAS logo, system working]**

> "EduMAS proves that intelligent, multi-agent educational systems can be built locally, affordably, and transparently."

> "No expensive cloud platforms. No black-box AI. Just pure, orchestrated intelligence."

> "The future of personalized, automated education is here."

> "And it's open-source."

---

## VISUAL ASSETS TO PREPARE

1. **System Architecture Diagram** – Flowchart showing Coordinator → Quiz Generator → Grader → Report Writer
2. **Agent Icons** – 4 distinct icons for each agent (Coordinator, Generator, Grader, Writer)
3. **Sample Quiz JSON** – Show 5 questions on screen
4. **Sample Report** – Show final report output with score breakdown
5. **Data Flow Animation** – Animated pipeline showing data moving through agents
6. **Dashboard Mockup** – React interface for student interaction
7. **Tool Diagram** – Show 4 tools connecting to respective agents
8. **Logo/Branding** – EduMAS title card and closing slide

---

## VOICEOVER PACING

- **Total Duration**: 5 minutes (300 seconds)
- **Word Count**: ~750 words
- **Speaking Pace**: 150 words/minute
- **Pauses**: 2-3 seconds between major sections for visual transitions

---

## OPTIONAL EXTENDED SEGMENTS (Add 2-3 minutes)

### Technical Deep-Dive (2:00 additional)
- Show actual code snippets from agent definitions
- Explain CrewAI framework and how it orchestrates agents
- Explain Ollama integration and llama3:8b model
- Show requirements.txt and setup process

### Use Cases & Future Vision (1:00 additional)
- Online learning platforms automating assessments
- Corporate training systems for employee onboarding
- Accessibility tools for personalized learning at scale
- Integration with Learning Management Systems (Canvas, Moodle)

---

## RECORDING TIPS

1. Use screen recording software (OBS, Camtasia) to capture system in action
2. Record voiceover separately with clear audio
3. Add background music (royalty-free) at low volume during transitions
4. Use text overlays for key statistics (e.g., "Zero Cloud Costs", "54 Unit Tests")
5. Include 1-2 second transitions between scenes
6. Add captions for accessibility

