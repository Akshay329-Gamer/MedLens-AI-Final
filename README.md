# MedLens — AI Clinical Insight

> AI-powered clinical information intelligence for structuring and reviewing medical reports.

Built for the **PromptWars × AIMERverse** hackathon at **MVSR Engineering College**, presented by **Hack2Skill × Google for Developers** in collaboration with **MVSR AIMERS**.

---

## 🩺 Problem

Medical information is often scattered across laboratory reports, prescriptions, patient history, and other documents.

Important information such as:

- Test names
- Values
- Units
- Reference ranges
- Dates
- Observations
- Patient-provided information

can be difficult to review quickly.

MedLens addresses this problem by transforming uploaded medical reports into a structured and understandable clinical information record.

---

## 💡 Solution

**MedLens** is a multimodal AI-powered clinical information structuring application.

Users provide basic patient context and upload a medical report as a PDF or image.

The system then:

1. Reads the uploaded report using multimodal AI.
2. Extracts relevant medical test information.
3. Structures the extracted information into a consistent record.
4. Compares values against reference ranges explicitly present in the source report.
5. Detects potential conflicts in supplied information.
6. Generates a concise patient-friendly summary.
7. Clearly communicates the need for human verification.

MedLens is designed as a **clinical information organization and review-support tool**, not an autonomous medical decision system.

---

## ✨ Key Features

### Patient Information Intake

Users can provide:

- Age
- Sex
- Symptoms
- Known conditions
- Allergies
- Current medications

This information is supplied to the AI as patient context.

### Medical Report Processing

Supported formats:

- PDF
- JPG / JPEG
- PNG
- WEBP

Maximum upload size:

**8 MB**

The system extracts:

- Test name
- Value
- Unit
- Reference range
- Status
- Date
- Observation
- Source

### Reference-Range-Aware Classification

MedLens does **not** invent laboratory reference ranges.

A result can be classified as:

- `LOW`
- `NORMAL`
- `HIGH`

only when the uploaded report itself provides a reference range that supports the classification.

If the reference range is missing or insufficient:

`UNKNOWN`

is returned.

This prevents the AI from silently substituting general medical knowledge for the source document.

### Conflict Detection

The system checks the supplied patient information and extracted report information for obvious contradictions.

Potential conflicts are displayed separately so they can be reviewed by a human.

Missing optional information is not automatically treated as a conflict.

### Source & Provenance

Extracted test information is marked as coming from the:

`uploaded report`

This makes the origin of extracted information visible to the reviewer.

### Patient-Friendly Summary

MedLens generates a concise summary based on the information present in the uploaded report and supplied patient context.

If a report contains its own clinical interpretation, the system is instructed to attribute it to the report rather than presenting it as an independent AI conclusion.

### Responsible AI

The system explicitly avoids:

- Medical diagnosis
- Treatment prescription
- Medication changes
- Dosage recommendations
- Invented reference ranges
- Unsupported medical conclusions

AI-extracted information should be reviewed by a qualified human before clinical use.

---

## 🧠 AI Processing Logic

The application uses a multimodal AI model through OpenRouter.

### Processing Pipeline

```text
Patient Information
        +
Uploaded Medical Report
        ↓
File Validation
        ↓
Base64 Encoding
        ↓
Multimodal AI Processing
        ↓
Structured JSON Extraction
        ↓
JSON Cleaning
        ↓
Result Normalization
        ↓
Reference-Range Classification
        ↓
Conflict Detection
        ↓
Patient-Friendly Summary
        ↓
Human Review
```

The AI is explicitly instructed to return structured JSON rather than an unrestricted conversational response.

### Expected AI Output

```json
{
  "tests": [
    {
      "test_name": "string",
      "value": "string",
      "unit": "string",
      "reference_range": "string",
      "status": "LOW | NORMAL | HIGH | UNKNOWN",
      "date": "string",
      "observation": "string",
      "source": "uploaded report"
    }
  ],
  "conflicts": [
    "string"
  ],
  "summary": "string"
}
```

---

## 🔐 Safety & Responsible AI

MedLens is intentionally designed as an **information-structuring and review-support system**.

The AI prompt contains explicit safeguards against:

- Diagnosis
- Disease inference
- Speculation
- Treatment recommendations
- Medication changes
- Dosage recommendations
- Inventing laboratory values
- Inventing units
- Inventing dates
- Inventing reference ranges

When a medical interpretation is already present in the source report, the application instructs the model to present it as an attributed statement such as:

> "The report states..."

rather than presenting the interpretation as an independent AI diagnosis.

Uncertain or missing information is not silently converted into facts.

---

## 🛡️ Security

Security considerations include:

- API credentials are stored as server-side environment variables.
- The OpenRouter API key is never hardcoded in the source code.
- `.env` files are excluded through `.gitignore`.
- Uploaded files are processed in memory.
- Uploaded files are not intentionally persisted by the application.
- File types are validated before processing.
- File size is limited to 8 MB.
- Patient text fields are bounded before being included in the AI prompt.
- AI error responses are truncated before being returned to the client.

The application does not expose the OpenRouter API key to the browser.

---

## ⚡ Efficiency & Reliability

MedLens includes controls to reduce unnecessary AI usage and improve predictable behavior.

### Efficiency Controls

- Patient-provided text is limited before prompt construction.
- AI output is limited using a maximum token budget.
- Low temperature is used for more consistent structured extraction.
- Prompts are focused on the required extraction task.
- Uploaded files are processed in memory.
- API request timeouts prevent indefinitely hanging requests.

### Error Handling

The backend handles:

- Missing API configuration
- Unsupported file types
- Oversized files
- Invalid patient JSON
- API failures
- Empty model responses
- Unexpected AI output
- Request timeouts
- Network errors
- Unexpected server errors

---

## ♿ Accessibility

The interface includes accessibility-oriented improvements including:

- Semantic HTML sections
- Explicit label and input associations
- Keyboard-visible focus indicators
- Screen-reader-friendly status updates
- `aria-live` processing and result regions
- Accessible file upload labeling
- Table captions
- Table column scopes
- Accessible conflict alerts
- Descriptive page metadata
- Responsive layout for smaller screens

The goal is to make the information workflow usable beyond mouse-only interaction.

---

## 🧪 Testing

MedLens includes automated tests using **pytest**.

The test suite verifies core data-processing functions including:

- JSON markdown-fence removal
- JSON extraction from surrounding text
- Data URL generation
- Structured result normalization
- Handling of missing result sections
- Validation of normalized output structure

Tests are automatically executed using **GitHub Actions** whenever changes are pushed to the `main` branch or submitted through a pull request.

### Run Tests Locally

```bash
pytest -q
```

---

## 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │       Browser        │
                         │  HTML/CSS/JavaScript │
                         └──────────┬───────────┘
                                    │
                       Patient Info + Report
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    FastAPI Backend   │
                         ├──────────────────────┤
                         │ File validation      │
                         │ Size validation      │
                         │ Patient parsing      │
                         │ Prompt construction  │
                         │ Base64 encoding      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    OpenRouter API    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ MiniMax M3 Multimodal│
                         │         AI           │
                         └──────────┬───────────┘
                                    │
                              Structured JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Result Processing  │
                         ├──────────────────────┤
                         │ JSON cleaning        │
                         │ Normalization        │
                         │ Status validation    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      MedLens UI      │
                         ├──────────────────────┤
                         │ Medical Record       │
                         │ Conflict Detection   │
                         │ Patient Summary      │
                         │ Responsible AI       │
                         └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Requests

### Frontend

- HTML
- CSS
- JavaScript

### AI

- OpenRouter API
- MiniMax M3 multimodal AI

### Testing

- pytest
- GitHub Actions

### Deployment

- Docker
- Render

---

## 📁 Project Structure

```text
MedLens-AI-Final/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── tests/
│   └── test_app.py
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 How It Works

### 1. Enter Patient Context

The user provides whatever patient information is available.

Optional information can be left blank.

### 2. Upload a Medical Report

The user uploads a supported medical report.

The backend validates:

- MIME type
- File size

### 3. AI Extraction

The report is sent to the multimodal AI model together with a strict extraction prompt.

The model is instructed to return structured JSON.

### 4. Normalize the Response

The backend cleans the model response and normalizes the returned fields.

Invalid status values are converted to:

`UNKNOWN`

### 5. Review the Structured Record

The extracted tests are displayed in a structured table.

| Field | Description |
|---|---|
| Test | Extracted test name |
| Value | Reported value |
| Unit | Reported unit |
| Reference Range | Range from source report |
| Status | LOW / NORMAL / HIGH / UNKNOWN |
| Date | Reported test date |
| Observation | Report observation |
| Source | Information provenance |

### 6. Review Conflicts

Potential contradictions are displayed separately for human review.

### 7. Read the Summary

A concise patient-friendly summary is generated from the supplied information.

### 8. Human Verification

The interface clearly communicates that AI-extracted information requires human review before clinical use.

---

## 📊 Example Use Cases

MedLens can help organize information from reports such as:

- Complete blood counts
- Biochemistry reports
- Urinalysis
- Imaging reports
- Other supported medical documents

The system focuses on **structuring information contained in the source**, rather than independently interpreting or diagnosing the patient.

---

## ⚠️ Limitations

MedLens has important limitations:

- AI extraction can contain errors.
- Poor-quality scans may reduce extraction accuracy.
- Handwritten or unclear information may be difficult to process.
- The system depends on the information available in the uploaded source.
- Missing reference ranges result in `UNKNOWN` rather than an inferred range.
- The application does not replace professional medical review.
- The system does not provide autonomous diagnosis or treatment decisions.

Users should verify extracted information against the original report.

---

## 🌐 Deployment

The application is containerized using Docker and deployed as a web service on Render.

The OpenRouter API credential is configured as a server-side environment variable.

No API credentials are included in the public repository.

---

## 🎯 Challenge Alignment

MedLens addresses the core requirements of the **MedLens — AI Clinical Insight** challenge.

| Challenge Requirement | MedLens Implementation |
|---|---|
| Patient information intake | Age, sex, symptoms, conditions, allergies, medications |
| Medical report processing | PDF and image processing |
| Structured medical record | Structured test table |
| Reference-range awareness | Source-report-only classification |
| Source & provenance | Uploaded report source field |
| AI summary | Patient-friendly summary |
| Conflict detection | Potential contradiction detection |
| Human verification | Explicit review requirement |
| Safety | No diagnosis or treatment recommendations |
| Reliability | Validation and error handling |
| Accessibility | Semantic and keyboard-friendly interface |
| Testing | Automated pytest + GitHub Actions |
| Deployment | Docker + Render |

---

## 📌 Responsible Use

MedLens is intended for **information organization and review support**.

It should not be used as a substitute for qualified medical professionals.

All AI-extracted information should be checked against the original medical report before being used for any clinical purpose.

---

## 👨‍💻 Project Information

**Project:** MedLens — AI Clinical Insight

**Hackathon:** PromptWars × AIMERverse

**Presented by:** Hack2Skill × Google for Developers

**In collaboration with:** MVSR AIMERS

**Institution:** MVSR Engineering College

---

## 📄 License

This project was created as a hackathon project for demonstration and evaluation purposes.
