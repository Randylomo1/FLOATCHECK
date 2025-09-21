# FloatCheck v2.0 Development Plan

This document outlines the development tasks to build the Floatcheck platform as per the product requirements.

## Phase 1: Core Platform (Foundation)

- [ ] **1. Multi-source Ingestion**:
    - [ ] M-Pesa (SMS, API)
    - [ ] Bank Statements (CSV, OFX)
    - [ ] Manual Uploads (Excel)
    - [ ] STK Pushes (Paybill, Till)
- [ ] **2. Highly Configurable Automatic Matching Engine**:
    - [ ] Rule engine (exact, fuzzy, amount, time window)
    - [ ] Weighted scoring and confidence thresholds
    - [ ] UI for rule building
- [ ] **3. Exception Management Dashboard**:
    - [ ] Queue of exceptions with smart suggestions
    - [ ] Bulk resolution
    - [ ] Audit trail
- [ ] **4. Accounting and ERP Connectors**:
    - [ ] Two-way sync with major ERPs
    - [ ] Webhook support
- [ ] **5. Easy Onboarding & Paybill/Till Verification**:
    - [ ] Onboarding wizard
    - [ ] STK push verification
- [ ] **6. Exportable Audit Reports & Compliance Logs**:
    - [ ] CSV/PDF reports
    - [ ] Scheduled reports
- [ ] **7. Real-time Reconciliation & Streaming Ingest**:
    - [ ] Webhook and polling support

## Phase 2: Growth & Intelligence

- [ ] **8. Smart Anomaly Detection & Fraud Alerts**:
    - [ ] ML-based rules
- [ ] **9. Payments Orchestration & Collect Tools**:
    - [ ] STK push sender
    - [ ] Invoice reminders (Email, WhatsApp, SMS)
    - [ ] Hosted payment links
- [ ] **10. Cashflow Forecasting**:
    - [ ] AR aging with automated chase sequences
- [ ] **11. Rules Marketplace/Templates**:
    - [ ] Pre-built rules for different business types
- [ ] **12. Localized Notifications**:
    - [ ] WhatsApp, SMS, Email integration

## Phase 3: Enterprise & Scale

- [ ] **13. Role-Based Access Control & Approval Workflows**:
- [ ] **14. Cross-product Integrations (Banks, PSPs, Payroll, Tax)**:
- [ ] **15. Marketplace & Partner Program**:
    - [ ] Whitelabel/agency accounts
- [ ] **16. Analytics & Benchmarking**:
- [ ] **17. API & SDK for Developers**:
- [ ] **24. Enterprise Play**:
    - [ ] Custom integrations, SLAs, on-prem deployments

## UI/UX & Frontend

- [X] **Splash & Onboarding**:
    - [X] Splash screen
    - [ ] Animated onboarding slides
- [ ] **Sign Up / Login**:
    - [X] Create User model
    - [X] Create sign-up page
    - [X] Create login page
- [ ] **Business Setup Flow**:
- [ ] **Home Dashboard**:
- [ ] **Reconciliation Flows**:
- [ ] **Reports & Analytics**:
- [ ] **AI Insights & Forecasts**:
- [ ] **Notifications UI**:
- [ ] **Settings**:
- [ ] **22. Mobile-First Dashboard & WhatsApp Flows**:
- [ ] **23. Low/No-Code Rule Builder UI**:

## Cross-cutting Concerns

- [ ] **18. Explainability in Matching**:
- [ ] **19. Confidence Scoring**:
- [ ] **20. SMS Parser + ML Fallback**:
- [ ] **21. Data Retention & Security**:
