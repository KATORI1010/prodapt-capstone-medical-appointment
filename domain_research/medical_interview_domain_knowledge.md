# Medical Interview Domain Knowledge for AI Agents

## 1. Purpose of Medical Interviewing

Medical interviewing is a core clinical process used to gather subjective information from patients in order to:

- Understand symptoms and their context
- Assess severity and urgency (triage)
- Support clinical reasoning and decision-making
- Monitor changes over time and treatment effects

For an AI agent, the goal is **not diagnosis**, but **structured, safe, and clinically useful information collection**.

---

## 2. Structured Interview Frameworks

Structured frameworks are widely used in clinical practice to reduce omissions and improve consistency.

### 2.1 OPQRST (Pain Assessment)

OPQRST is a standardized framework focused on pain assessment:

- **O – Onset:** When and how the symptom began
- **P – Provocation / Palliation:** Factors that worsen or relieve the pain
- **Q – Quality:** Character of the pain (e.g., sharp, dull, burning)
- **R – Region / Radiation:** Location and spread of pain
- **S – Severity:** Intensity, often using a numeric scale (0–10)
- **T – Time:** Duration, frequency, and progression over time

OPQRST is commonly used in emergency care, outpatient settings, and nursing assessments.

### 2.2 Other Common Frameworks

- **SAMPLE:** Symptoms, Allergies, Medications, Past history, Last intake, Events
- **SOCRATES:** Site, Onset, Character, Radiation, Associations, Time course, Exacerbating/relieving factors, Severity

AI agents should support multiple frameworks depending on context.

---

## 3. Core Interviewing Know-how (Best Practices)

### 3.1 Question Design

- Start with **open-ended questions** to capture the patient narrative
- Follow with **closed-ended questions** for clarification and structure
- Avoid leading or suggestive questions

### 3.2 Language and Communication

- Use plain, non-technical language
- Reflect and paraphrase patient responses to confirm understanding
- Allow patients to describe symptoms in their own words

### 3.3 Non-verbal and Contextual Cues

In human interviews, clinicians observe:

- Facial expressions and body posture
- Voice tone and hesitation
- Functional limitations

AI agents cannot fully access these cues and must compensate through careful questioning.

---

## 4. Required Clinical Knowledge for AI Agents

### 4.1 Symptom Assessment Concepts

- Acute vs. chronic onset
- Continuous vs. intermittent symptoms
- Localized pain vs. referred or radiating pain

### 4.2 Severity and Scaling

- Numeric Rating Scale (NRS)
- Visual Analog Scale (VAS)

Consistency in scale usage is essential for longitudinal comparison.

### 4.3 Red Flags (Safety-Critical Information)

AI agents must be designed to detect and escalate potential red flags, such as:

- Sudden severe pain
- Neurological deficits
- Chest pain, shortness of breath
- Altered consciousness

This requires predefined escalation and handoff rules.

---

## 5. Domain Challenges in Medical Interviewing

### 5.1 Subjectivity of Symptoms

- Pain and discomfort are inherently subjective
- Numeric scores do not fully capture patient experience

### 5.2 Time Constraints

- Clinical settings often limit interview duration
- AI agents must balance completeness with efficiency

### 5.3 Patient Diversity

- Differences in age, culture, language, and health literacy
- Pediatric, geriatric, and cognitively impaired patients require adaptations

### 5.4 Data Quality and Consistency

- Variability in patient expression
- Incomplete or contradictory answers
- Need for normalization and structured outputs

---

## 6. Role of OPQRST in AI-Based Interviewing

OPQRST functions as:

- A **shared clinical language** across professionals
- A **baseline structure** for pain-related symptom collection
- A **comparison tool** before and after interventions

For AI agents, OPQRST provides:

- Predictable conversation flow
- Structured data fields
- Improved interoperability with clinical documentation

---

## 7. Design Implications for AI Interview Agents

Key design principles include:

- Framework-driven but flexible dialogue
- Explicit handling of uncertainty and missing data
- Clear separation between information gathering and clinical judgment
- Strong safety and escalation mechanisms

---

## 8. Key Takeaway

Medical interviewing is not merely a Q&A task, but a **clinical reasoning process**. Effective AI interview agents must integrate structured frameworks like OPQRST with patient-centered communication, safety awareness, and domain-specific constraints.
