# Development Plan

1. *Create `tasks.md`.* This file will store the development plan.
2. *Setup project structure.* Create directories for source code (`src`), tests (`tests`), and data (`data`).
3. *Implement PDF parsing engine.*
    - Accept PDF uploads.
    - Use `pdfplumber` to extract text and tables.
    - Implement OCR using Tesseract for image-based PDFs.
    - Use an LLM (e.g., GPT-4) to parse extracted text to JSON, identifying:
        - Insurance type
        - Provider name
        - Renewal date
        - Premium amount
        - Coverage type & excess
    - Output structured JSON and a summary card.
4. *Implement Renewal Timing Engine.*
    - Calculate the "sweet spot" for renewal (20-27 days prior, average ~23-26 days).
    - Display countdown to the ideal renewal window.
    - Show contextual information (e.g., potential savings).
5. *Implement Action-Oriented Dashboard.*
    - Display policy cards with key information and renewal countdown.
    - Include a dummy "Start getting quotes" button/form.
6. *Implement Notifications & Reminders.*
    - Send email or app reminders when in the "sweet spot".
7. *Implement Manual Review & Confidence Flagging.*
    - Flag fields with missing or low-confidence data.
    - Allow manual correction of extracted information.
8. *Write Unit Tests.* Implement tests for all features, following TDD principles.
9. *Integrate components.* Ensure all parts of the application work together.
10. *Submit the change.*
