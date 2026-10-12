# Design Notes

## Product direction
The product follows a premium workflow interface: a calm neutral palette, a left-side knowledge workspace, and a right-side evidence and artifact panel. The app is designed to feel like a focused research aide rather than a raw chatbot.

## Interaction model
- A narrow left rail holds session history and provider status.
- The center canvas is the active conversation.
- A right panel exposes evidence, provider state, and generated artifact output.
- Starter prompts reduce friction for first-time users.

## Visual system
- Base palette: warm ivory, dark brown, muted green.
- Accent interaction: soft moss green and olive.
- Card surfaces use layered translucency so that content feels premium but not overdesigned.

## UX principles
- Evidence first: every answer should be traceable.
- Human language: responses are readable and concise.
- Safe previews: artifact output renders within a constrained iframe, not direct raw HTML injection into app DOM.
- Progressive confidence: feature flags and model state keep expectations honest.

## Content patterns
- Builder prompt templates for discovery questions.
- Structured answer cards with small evidence references.
- Artifact output as a preview pane, not a hard navigation step.
