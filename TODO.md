# FloatCheck v2.0 Development Plan

This document outlines the development tasks to build the Floatcheck platform as per the product requirements.

## Phase 1: Core Platform (Foundation)

- [X] **1. Multi-source Ingestion**:
    - [X] M-Pesa (SMS, API)
    - [X] Bank Statements (CSV, OFX)
    - [X] Manual Uploads (Excel)
    - [X] STK Pushes (Paybill, Till)
- [X] **2. Highly Configurable Automatic Matching Engine**:
    - [X] Rule engine (exact, fuzzy, amount, time window)
    - [X] UI for rule building
- [X] **3. Exception Management Dashboard**:
    - [X] Queue of exceptions with smart suggestions
    - [X] Bulk resolution
    - [X] Audit trail
- [X] **4. Accounting and ERP Connectors**:
    - [X] Basic integration management UI
    - [X] Two-way sync with major ERPs
    - [X] Webhook support
- [X] **5. Easy Onboarding & Paybill/Till Verification**:
    - [X] Onboarding wizard
    - [X] STK push verification
- [ ] **6. Exportable Audit Reports & Compliance Logs**:
    - [X] CSV reports for reconciliation results
    - [X] PDF reports
    - [X] Scheduled reports
    - [ ] Exportable audit logs
- [X] **7. Real-time Reconciliation & Streaming Ingest**:
    - [X] Webhook and polling support

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
- [X] **Sign Up / Login**:
    - [X] Create User model
    - [X] Create sign-up page
    - [X] Create login page
- [X] **Business Setup Flow**
- [X] **Home Dashboard**
- [X] **Reconciliation Flows**
- [ ] **Reports & Analytics**:
- [ ] **AI Insights & Forecasts**:
- [ ] **Notifications UI**:
- [ ] **Settings**:
- [ ] **22. Mobile-First Dashboard & WhatsApp Flows**:
- [X] **23. Low/No-Code Rule Builder UI**:

## Cross-cutting Concerns

- [ ] **18. Explainability in Matching**:
- [ ] **19. Confidence Scoring**:
- [ ] **20. SMS Parser + ML Fallback**:
- [ ] **21. Data Retention & Security**:
