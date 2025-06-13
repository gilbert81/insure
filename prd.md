Below is a **product requirements document** for your insurance assistant MVP, connecting **PDF parsing**, **intelligent renewal advice**, and **action-driven workflow**—without needing a business website as a credibility anchor:

---

## 📘 Product Requirements Document (PRD)

### 1. **Objective**

Build a digital assistant that:

* **Auto-extracts** essential details from uploaded insurance PDFs.
* **Surfaces key info** (type, provider, renewal date, cost, coverage).
* **Advises optimal renewal timing**, based on data-driven sweet spots.
* **Guides users** to take action (search for quotes, start comparison workflows).

---

### 2. **User Personas**

* **Busy individuals** who want a reminder system + simple insurance admin.
* **Cost-conscious savers** seeking optimal timing to renew and save.
* **Digitally comfortable** users open to semi-automated workflows (upload PDF, get pushed to comparison sites).

---

### 3. **Core Features & Functional Requirements**

#### A. PDF Parsing Engine

* Accept `.pdf` uploads.
* Auto-detect text vs image PDF.
* Extract structured data:

  * Insurance type (car, home, travel, etc.)
  * Provider name
  * Renewal date
  * Premium amount
  * Coverage type & excess
* Output: structured JSON + summary card.

#### B. Renewal Timing Engine

* Use market data to calculate the “sweet spot” for renewal:

  * 20–27 days ahead, average sweet spot \~23–26 days ([moneyexpert.com][1], [moneysavingexpert.com][2]).
* Display:

  * Countdown to “ideal renewal window.”
  * Contextual info: expected cost difference & why timing matters.

    > “Users renewing 26 days early save an avg. £164 vs. same-day renewal” .
  * Tips from expert consensus (Martin Lewis, Go.Compare) ([which.co.uk][3]).

#### C. Action-Oriented Dashboard

* Show **policy cards** with:

  * Key info & renewal countdown.
  * Renewal readiness indicator (“Ideal window starting in X days”).
  * **Action button**: “Start getting quotes”.

    * Pre-fill forms using data.
    * Interface with comparison sites via API/scraping.
    * Display quotes comparison.
    * Option to finalize externally and upload documentation.

#### D. Notifications & Reminders

* Calendar invites / push notifications:

  * Reminder when in the 3–4 week “sweet spot.”
  * Optional follow-ups if user delays action.

#### E. Manual Review & Confidence Flagging

* PDF extraction flags:

  * Missing dates, low-confidence fields.
* Show “Verify this info” prompts.
* Allow manual correction before dashboard inclusion.

---

### 4. **MVP Scope – Tabular Summary**

| Feature                 | Included in MVP? | Notes                               |
| ----------------------- | ---------------- | ----------------------------------- |
| PDF upload & ingestion  | ✅ Yes            | Support PDF + image conversion      |
| Text/table extraction   | ✅ Yes            | Use pdfplumber + Tesseract OCR      |
| LLM parsing to JSON     | ✅ Yes            | GPT‑4 prompts for field extraction  |
| Renewal date detection  | ✅ Yes            | Calculate days left                 |
| Timing advice & tips    | ✅ Yes            | Use UK data and citations           |
| Policy dashboard        | ✅ Yes            | Presentation layer                  |
| Quote initiation        | ⚠️ Minimal       | Pre-fill/scrape one comparison site |
| Notifications           | ✅ Yes            | Email/app reminders                 |
| Manual review interface | ✅ Yes            | Detect errors & allow edits         |

---

### 5. **User Experience Flow (UI Sketch)**

```
[Dashboard: Policy Cards List]
-----------------------------------------------------
| Car Insurance • Provider: Admiral                |
| Renewal: 2025‑07‑15 • 26 days left 🟢 (Ideal     |
| window) • £723 • Fully comprehensive • £250 excess |
| [Start getting quotes]                          |
-----------------------------------------------------
| Home Insurance • Provider: DirectLine           |
| Renewal: 2025‑09‑10 • 89 days left 🔵           |
| [View details]                                  |
-----------------------------------------------------
```

Upon clicking **Start getting quotes**:

* Show auto-filled form UI for comparison site.
* Display returned quotes:

  * List by price, coverage, excess, provider fees.
* Action buttons: **Choose this policy** → link to provider site or download PDF.

---

### 6. **Technical Architecture**

1. **Front-End**

   * Upload UI → parse & display reminders.
   * Dashboard with countdown & action prompts.
   * Quote initiation interface.

2. **Back-End**

   * PDF pipeline:

     * detect type → extract via pdfplumber + Tesseract.
     * send extracted text → LLM endpoint for JSON extraction.
   * Renewal logic module:

     * Uses UK market timing data.
     * Calculates optimal window.
   * Quote automation:

     * Pre-fill via Puppeteer or API for one comparison engine.
   * Notification scheduler.

3. **Data Storage**

   * Policies table: type, provider, renewal\_date, premium, coverage, status, confidence flags.
   * User actions, history, notification status.

---

### 7. **Metrics & Success Criteria**

* **Extraction accuracy**: ≥90% key fields parsed automatically.
* **User activation**: ≥50% click-through to quote flow.
* **Conversion proxy**: ≥20% finalize quote via UI link.
* **User satisfaction**: qualitative feedback: “It reminded me at the right time” / “I saved money”.

---

### 8. **Milestones & Timeline**

1. Week 1–2: PDF pipeline & JSON extraction.
2. Week 3–4: Dashboard UI with countdown logic.
3. Week 5–6: Quote pre-fill flow + basic scraping prototype.
4. Week 7–8: Notification system + manual review UI.
5. Week 9: QA, bugfix, soft pilot release.
6. Week 10: Pilot feedback, improvements, MVP launch.
