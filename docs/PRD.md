# Product Requirements Document

## User and problem
Founders, PMs, and growth teams need a way to turn transcript-based product thinking into practical decisions. The current problem is fragmented context: insights are scattered across podcasts, newsletters, and notes, and there is no reliable way to inspect evidence or convert that thinking into an artifact. The Lenny Growth Assistant is a grounded research workspace that supports discovery, recommendation, writing, and artifact generation.

## Primary jobs to be done
- Ask a product or growth question grounded in trusted transcript material.
- View the source passages behind the answer.
- Turn an answer into a structured brief or a written essay.
- Generate a shareable artifact in Markdown or HTML preview.

## Success metrics
- Supported questions return source-backed evidence in the answer flow.
- Unsupported questions abstain with a clear explanation.
- Session history remains accessible across HTTP requests.
- The app can run locally with a default Ollama path and a fallback to a safe demo response.
- The core chat-to-artifact flow completes in a local smoke test.

## Assumptions
- Network access is not guaranteed for all transcript source access.
- The local demo uses synthetic transcript fixtures clearly labeled as demo material.
- No real API keys are committed to the repo.

## Scope and exclusions
In scope:
- FastAPI backend, SQLAlchemy persistence, retrieval, evidence, artifact preview, chat flow, local model integration.

Out of scope:
- Multi-user authentication and production-grade observability beyond local demo quality.
- Real podcast licensing automation.

## User flows
1. User opens the app and sees a starter set of grounded prompts.
2. User asks a question; the backend retrieves supporting evidence and generates a grounded answer.
3. User inspects the evidence panel and can create an artifact.
4. User chooses to generate a Ship 30 essay or Growth Brief.
5. User previews the artifact in an isolated iframe.

## Functional requirements
- Session persistence and message retrieval.
- Provider selection and status visibility.
- Source citation and evidence inspection.
- Artifact generation in markdown and HTML preview.
- Local demo compatibility without external APIs.

## Non-functional requirements
- Secure preview model with sandboxed iframe.
- Graceful degradation when Ollama or model providers are unavailable.
- Clear request IDs and structured error responses.
- Reproducible startup via Docker Compose and local commands.

## Acceptance criteria
- Health endpoint responds successfully.
- Chat API returns structured answer and evidence.
- Source retrieval produces traceable evidence.
- Artifact page renders safely.
- Project runs without secrets in the repo.

## Risks and mitigations
- Local model quality may degrade; fallback is explicit and honest.
- No real Lenny transcript access may limit range; synthetic fixtures disclose the model.
- HTML preview security requires restrictive sandboxing and no direct DOM injection.

## Implementation priorities
1. Working backend and local provider path.
2. Retrieval, evidence, and session logic.
3. Frontend interaction model and artifact preview.
4. Documentation and demo flow.
