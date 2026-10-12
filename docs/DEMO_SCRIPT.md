# Demo Script

## Goal
Show that the app is a grounded, evidence-first assistant that can answer a product question and produce a reusable artifact.

## Stage 1: Launch
1. Open the repo root.
2. Activate the backend environment.
3. Run the backend via uvicorn or the provided Makefile.
4. Run the frontend with Vite.

## Stage 2: Basic interaction
1. Select a starter prompt such as "What should a growth-focused founder prioritize?"
2. Observe the answer structure and evidence list.
3. Explain that the model uses transcript chunks as supporting evidence.

## Stage 3: Artifact generation
1. Trigger the artifact generation action.
2. Notice the generated brief appears as a preview.
3. Explain that the artifact is not a free-form hallucination; it is based on the same evidence set.

## Stage 4: Security and trust
1. Note the iframe render and sandboxed artifact preview.
2. Explain the evidence citations and source traceability.
3. Discuss the fallback path when no cloud provider is configured.

## Short speaking notes
- "This is not a generic chatbot. It is a grounded research workflow."
- "The right panel shows the evidence behind the answer."
- "The artifact is built from the same transcript context, which makes it more reusable."
