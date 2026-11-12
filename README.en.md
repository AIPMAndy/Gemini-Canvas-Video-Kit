# Gemini Canvas Video Kit

**A browser-first, open-source kit for making record-ready motion videos with the Gemini web app's Canvas feature.** No CLI, API keys, or installation required for the core workflow.

## How it works
1. Open `index.html` in a browser and generate a detailed video prompt.
2. Open [Gemini](https://gemini.google.com/) on the web and select **Canvas**.
3. Paste the generated prompt and ask Gemini to build the running, self-contained HTML experience.
4. Preview, refine, play it full-screen and record with your operating system's screen recorder.

## Included
- `index.html`: offline prompt builder for six video formats.
- `examples/launch-showcase.html`: working ~30-second animated fictional product walkthrough.
- `examples/knowledge-explainer.html`: working 15-second explainer.
- `templates/`: reusable prompts and troubleshooting follow-ups.
- `docs/`: getting started, recording/audio caveats, quality checklist, and limitations.

## Scope and limitations
This project creates **code-driven animated browser pages**, not photorealistic text-to-video clips. The Gemini Canvas feature should not be represented as a native one-click MP4 exporter. Browser speech synthesis and screen recording of tab audio are not reliably portable. The examples contain fictional UI and must never be passed off as recorded real user activity.

Gemini Canvas official overview: https://gemini.google/us/overview/canvas/
Gemini Canvas help: https://support.google.com/gemini/answer/16047321

**Created by AI 酋长 Andy / 星觉科技** — [Website](https://metaver.vip/) · [Company](https://www.a6no1.cn/) · [GitHub](https://github.com/AIPMAndy)

Not affiliated with Google. Licensed under MIT.
