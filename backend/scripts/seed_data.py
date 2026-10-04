"""Demo data shared by the seed script, the leak test and the retrieval eval."""

DEMO_PASSWORD = "Passw0rd!demo"

TENANTS = [
    {
        "name": "Acme Corporation",
        "users": [
            ("admin@acme.example", "admin", "Executive"),
            ("manager@acme.example", "manager", "Sales"),
            ("employee@acme.example", "employee", "Support"),
        ],
        "docs": [
            {
                "title": "Acme Employee Handbook",
                "filename": "acme-handbook.txt",
                "roles": ["admin", "manager", "employee"],
                "secrets": [],
                "text": (
                    "ACME CORPORATION GLOBAL EMPLOYEE HANDBOOK & OPERATIONAL POLICIES\n"
                    "Version 4.2 | Human Resources & Legal Operations\n\n"
                    "CHAPTER 1: INTRODUCTION AND ORGANIZATIONAL VALUES\n"
                    "Welcome to Acme Corporation. We are committed to fostering an innovative, inclusive, collaborative, and "
                    "secure working environment for all staff members across our worldwide operations. This comprehensive handbook "
                    "outlines our standard operating procedures, workplace benefits, employment policies, code of conduct, and "
                    "corporate guidelines. Every employee is required to familiarize themselves with these principles upon joining.\n\n"
                    "Acme operates under four foundational cornerstones: Customer Trust, Technical Excellence, Operational "
                    "Integrity, and Mutual Respect. Whether working on client deliverables or developing internal technologies, "
                    "we expect our teams to conduct business with transparency and accountability.\n\n"
                    "CHAPTER 2: WORKING HOURS, ATTENDANCE, AND CORE SCHEDULES\n"
                    "Standard working hours across all Acme corporate offices are 9:00 to 17:30, Monday to Friday, inclusive of "
                    "a one-hour lunch break. To support operational synergy and cross-functional project delivery, core collaboration "
                    "hours are set between 10:00 and 15:00 local time, during which all team members must be reachable via corporate "
                    "messaging channels and available for scheduled team meetings.\n\n"
                    "Flexible scheduling may be arranged with prior written authorization from your direct department manager, "
                    "provided the operational requirements of your business unit are met without degradation in service levels. "
                    "Punctuality and reliability are vital; team members unable to report for duty must notify their manager prior "
                    "to the start of their scheduled shift.\n\n"
                    "CHAPTER 3: ANNUAL VACATION AND PAID TIME OFF (PTO) POLICY\n"
                    "Acme Corporation recognizes the necessity of regular rest, rejuvenation, and work-life balance for sustained "
                    "high performance. Full-time employees receive 25 vacation days per year, plus statutory public holidays recognized "
                    "in their respective operating jurisdictions.\n\n"
                    "Vacation accrues on a pro-rata basis on the first business day of each calendar month. Part-time employees "
                    "accrue leave on a proportional basis matching their contractual working hours. Unused vacation days up to five "
                    "can be carried over into the next year, provided they are utilized before March 31st of the following calendar year. "
                    "Any accrued leave beyond five days that remains untaken on December 31st will lapse unless special written "
                    "exemption has been granted by the Head of People.\n\n"
                    "Requests for vacation leave must be logged through the internal HR employee portal. Requests for consecutive "
                    "leave exceeding two weeks must be submitted at least four weeks in advance to allow for staffing coverage and "
                    "continuity of operational commitments.\n\n"
                    "CHAPTER 4: BUSINESS TRAVEL AND EXPENSE REIMBURSEMENT PROCEDURES\n"
                    "Employees incurring legitimate business expenditures during approved corporate travel or client engagements are "
                    "eligible for complete reimbursement in accordance with our corporate expense policy. Expense reports must be "
                    "submitted within 30 days of the purchase date, with receipts attached through the internal finance portal.\n\n"
                    "All travel bookings should be executed through Acme's corporate travel management tool to leverage preferred partner "
                    "discounts. Daily meal per diems are capped at $75 for domestic travel and $110 for international assignments, "
                    "covering breakfast, lunch, and dinner. Lodging reimbursements are benchmarked against standard business-class hotel "
                    "rates in the destination metropolitan area.\n\n"
                    "Personal expenditures, non-business related transportation, alcoholic beverages without documented client "
                    "entertainment justification, and commercial airline seat upgrades are non-reimbursable. Failure to submit "
                    "itemized receipts within the 30-day window may result in reimbursement denial by the finance audit team.\n\n"
                    "CHAPTER 5: HYBRID WORK POLICY AND OFFICE EXPECTATIONS\n"
                    "In support of modern workplace flexibility while sustaining vibrant in-person mentorship and team collaboration, "
                    "Acme uses a hybrid schedule: employees are expected in the office on Tuesday, Wednesday and Thursday.\n\n"
                    "Mondays and Fridays are optional remote working days for roles not classified as essential on-site operational "
                    "personnel. Employees utilizing remote privileges are expected to maintain an ergonomic, secure home workspace equipped "
                    "with reliable high-speed broadband and an acoustic environment conducive to confidential voice and video discussions.\n\n"
                    "Full-time remote work arrangements are reserved for designated field roles or require formal executive review and "
                    "a quarterly performance and compliance evaluation signed off by the direct Vice President.\n\n"
                    "CHAPTER 6: SICK LEAVE, MEDICAL EMERGENCIES, AND PARENTAL BENEFITS\n"
                    "Staff well-being is paramount. Sick leave is paid for up to ten days per year and does not require a doctor's "
                    "note for the first two days of absence. Absences extending past three consecutive days necessitate medical "
                    "certification submitted directly to Human Resources to qualify for short-term disability coverage.\n\n"
                    "Acme is proud to offer market-leading parental support. Acme offers sixteen weeks of fully paid parental leave for "
                    "primary caregivers and six weeks for secondary caregivers, available within the first twelve months following "
                    "birth, adoption, or long-term foster placement. Re-integration plans and phased return-to-work options are supported "
                    "to assist parents returning to full-time duties.\n\n"
                    "CHAPTER 7: INFORMATION TECHNOLOGY, SECURITY AND DEVICE MANAGEMENT\n"
                    "Safeguarding customer confidentiality and proprietary corporate intelligence is critical to our SOC 2 and ISO 27001 "
                    "compliance mandates. All corporate computing assets must be provisioned and managed by the Corporate IT department.\n\n"
                    "All laptops must use full-disk encryption and lock automatically after five minutes of user inactivity. Employees "
                    "must use multi-factor authentication (MFA) across all identity providers, VPN gateways, and cloud applications. "
                    "Report lost devices to the IT desk immediately so remote cryptographic wipe procedures can be initiated. Under no "
                    "circumstances should corporate credentials or customer databases be accessed on unmanaged personal devices.\n\n"
                    "CHAPTER 8: WORKPLACE HARASSMENT, DIVERSITY, AND GRIEVANCE ESCALATION\n"
                    "Acme Corporation maintains zero tolerance for harassment, discrimination, bullying, or retaliation of any form. "
                    "We are dedicated to creating an environment where individuals of all backgrounds, ethnicities, gender identities, "
                    "and abilities can thrive professionally. Any employee experiencing or witnessing misconduct should report the "
                    "incident immediately to Human Resources, their manager, or through our anonymous ethics whistleblower hotline.\n\n"
                    "All complaints are investigated promptly, thoroughly, and impartially, with strict protection against retaliation "
                    "for reporting in good faith. Confirmed violations of our anti-harassment policy will lead to disciplinary measures "
                    "up to and including immediate termination of employment for cause."
                ),
            },
            {
                "title": "Acme Q4 Sales Plan",
                "filename": "acme-q4-sales.txt",
                "roles": ["admin", "manager"],
                "secrets": ["project falcon", "14% quota increase"],
                "text": (
                    "ACME CORPORATION GLOBAL ENTERPRISE SALES PLAYBOOK & Q4 REVENUE GOALS\n"
                    "Document ID: STRAT-2026-Q4-CONFIDENTIAL | Distribution: Sales Leadership\n\n"
                    "SECTION 1: EXECUTIVE REVENUE MANDATE & MARKET OUTLOOK\n"
                    "Following record adoption across mid-market enterprise tiers in Q2 and accelerated expansion across international "
                    "territories during Q3, Acme Corporation is positioned to execute our most aggressive growth quarter to date. "
                    "The Q4 sales plan sets a 14% quota increase for all regional sales managers across North America and EMEA.\n\n"
                    "This quota adjustment reflects expanding customer renewal rates, higher annual contract values (ACV) across "
                    "key segments, and increased pipeline generation from our product-led marketing campaigns. All regional directors "
                    "are expected to realign their individual contributor quota distribution within the first week of the quarter.\n\n"
                    "SECTION 2: PROJECT FALCON STRATEGIC HEALTHCARE VERTICAL INITIATIVE\n"
                    "Project Falcon is the codename for our push into enterprise healthcare accounts. This strategic campaign focuses "
                    "on deploying our HIPAA-compliant software infrastructure to major hospital systems, regional health networks, "
                    "and clinical medical device manufacturers. The dedicated enterprise healthcare unit will be led by the VP of "
                    "Strategic Accounts.\n\n"
                    "The Project Falcon target account list includes 85 tier-one healthcare conglomerates across the United States. "
                    "Specialized healthcare solution engineers, compliance architects, and dedicated regulatory legal counsel have been "
                    "allocated to support sales pods pursuing these accounts. Contract templates have been pre-approved for HIPAA "
                    "Business Associate Agreements (BAAs) and HITRUST certified cloud infrastructure.\n\n"
                    "SECTION 3: PIPELINE MANAGEMENT, CADENCE, AND FORECAST ACCURACY\n"
                    "Forecasting predictability is the bedrock of corporate financial planning. Weekly deal inspection routines are "
                    "enforced across all regional pods. Managers must schedule weekly pipeline reviews and submit forecasts every Friday "
                    "before 17:00 EST.\n\n"
                    "Deals forecasted in commit stage must have verified executive stakeholder alignment, budget confirmation, and "
                    "active legal counsel engagement. Opportunities lacking mutual close plans signed by both parties may not be entered "
                    "into the 90-day commit category within Salesforce.\n\n"
                    "SECTION 4: PRICING GOVERNANCE, DISCOUNTS, AND APPROVAL THRESHOLDS\n"
                    "To safeguard gross margins and maintain consistent market pricing, strict discounting governance is enforced "
                    "globally. Standard commercial price schedules provide field sales reps with up to 10% discretionary discounting.\n\n"
                    "Discounts between 10.1% and 15% require sign-off from the Regional Sales Director. Discounts above 15% require "
                    "approval from the VP of Sales. Non-standard legal terms, multi-year payment holidays, or custom SLA commitments "
                    "require joint sign-off from Legal and the Chief Financial Officer before formal customer issuance.\n\n"
                    "SECTION 5: INCENTIVE COMPENSATION AND COMMISSION ACCELERATOR POOL\n"
                    "To motivate and reward aggressive overperformance during the final quarter, executive leadership has authorized "
                    "enhanced commission accelerators. Individual account executives exceeding 120% of their quarterly quota unlock "
                    "an automatic 1.5x commission accelerator on all bookings achieved beyond that threshold.\n\n"
                    "In addition, the top three performing teams will receive a bonus pool funded at two percent of net new revenue "
                    "closed during the quarter. Special President's Club qualification will be awarded to reps who close at least "
                    "two tier-one enterprise accounts under the Project Falcon healthcare banner."
                ),
            },
            {
                "title": "Acme CEO Compensation",
                "filename": "acme-ceo-comp.txt",
                "roles": ["admin"],
                "secrets": ["1,850,000", "250,000 shares"],
                "text": (
                    "ACME CORPORATION BOARD OF DIRECTORS COMPENSATION COMMITTEE REPORT\n"
                    "Document ID: GOV-EXEC-2026-COMP | Highly Confidential | Restriced: Board & Admin\n\n"
                    "SECTION 1: METHODOLOGY AND MARKET BENCHMARKING\n"
                    "The board compensation committee conducted its annual market compensation benchmark against comparable peer "
                    "technology companies in the high-growth enterprise software sector. The evaluation evaluated total direct compensation "
                    "(TDC), cash incentives, equity retention, and shareholder alignment across organizations with comparable market capitalization.\n\n"
                    "SECTION 2: EXECUTIVE BASE SALARY ADJUSTMENT\n"
                    "Following independent compensation advisory analysis, the committee approved adjustments to executive cash compensation. "
                    "The CEO's base salary for the fiscal year is $1,850,000. This represents an annualized market adjustment approved "
                    "unanimously by independent directors during the Q1 meeting to reflect stellar operational execution.\n\n"
                    "SECTION 3: LONG-TERM EQUITY INCENTIVE STRUCTURE\n"
                    "To ensure sustained alignment between executive leadership and long-term shareholder value creation, equity grants "
                    "were approved with rigorous multi-year vesting conditions. In addition, the CEO received an equity grant of 250,000 shares "
                    "vesting over four years.\n\n"
                    "Twenty-five percent of the initial grant vests on the first anniversary of employment, with remaining tranches vesting "
                    "in equal monthly installments thereafter over the subsequent thirty-six months. Accelerated vesting applies solely "
                    "in the event of a change in corporate control subject to double-trigger terms requiring both acquisition and termination.\n\n"
                    "SECTION 4: ANNUAL PERFORMANCE BONUS AND CONFIDENTIALITY\n"
                    "The annual performance bonus target is 120 percent of base salary, contingent upon reaching targets in GAAP operating "
                    "profitability, net customer retention, and employee satisfaction benchmarks. This information is restricted to the board "
                    "and company administrators. Any unauthorized disclosure or transmission of executive compensation data violates "
                    "board bylaws, corporate governance guidelines, and non-disclosure obligations."
                ),
            },
            {
                "title": "Acme Board Summary",
                "filename": "acme-board-summary.txt",
                "roles": ["admin"],
                "secrets": ["brightwave", "$42 million"],
                "text": (
                    "ACME CORPORATION CONFIDENTIAL BOARD MINUTES & STRATEGIC DISCUSSIONS\n"
                    "Document ID: BOD-MIN-2026-Q2-CONFIDENTIAL | Distribution: Board Members Only\n\n"
                    "ITEM 1: STRATEGIC M&A AND ACQUISITION APPROVAL\n"
                    "Following extensive technical and financial due diligence presented by the M&A advisory committee, the board approved "
                    "the acquisition of Brightwave for $42 million, to close in the second quarter. The transaction consists of seventy percent "
                    "cash consideration funded through existing reserves and thirty percent restricted stock units.\n\n"
                    "Brightwave's proprietary vector clustering algorithms and semantic indexing engine will be integrated directly into our "
                    "core product architecture, enhancing query throughput and reducing embedding compute costs by an estimated 35%.\n\n"
                    "ITEM 2: REGULATORY DISCLOSURES AND PUBLIC COMMUNICATION\n"
                    "The decision is confidential until the public announcement scheduled for release following SEC regulatory filing clearance "
                    "and Hart-Scott-Rodino pre-merger notification review. All board members and senior executives are subject to strict insider "
                    "trading restrictions starting immediately.\n\n"
                    "ITEM 3: OPERATIONAL RESTRUCTURING AND RESOURCE ALLOCATION\n"
                    "The board also discussed layoffs in the legacy hardware division but deferred a decision to next quarter. A sub-committee "
                    "has been formed to evaluate redeploying affected technical staff to cloud infrastructure initiatives. Meeting was adjourned "
                    "following unanimous ratification of all presented committee resolutions."
                ),
            },
        ],
    },
    {
        "name": "Globex Industries",
        "users": [
            ("admin@globex.example", "admin", "Executive"),
            ("manager@globex.example", "manager", "Product"),
            ("employee@globex.example", "employee", "Operations"),
        ],
        "docs": [
            {
                "title": "Globex Employee Handbook",
                "filename": "globex-handbook.txt",
                "roles": ["admin", "manager", "employee"],
                "secrets": [],
                "text": (
                    "GLOBEX INDUSTRIES CORPORATE EMPLOYEE HANDBOOK & OPERATIONAL POLICIES\n"
                    "Version 3.8 | People Operations & Operational Integrity\n\n"
                    "1. WORKING ENVIRONMENT & FLEXIBILITY\n"
                    "Globex Industries embraces workplace flexibility to foster productivity and support work-life integration. "
                    "Globex supports remote work for up to three days per week with manager approval. Employees are encouraged to "
                    "establish working hours that optimize cross-timezone collaboration with our European and Asian teams. Core hours "
                    "are observed between 10:00 and 16:00 local time.\n\n"
                    "2. PAID LEAVE ALLOWANCES AND TIME OFF\n"
                    "Rest and rejuvenation are essential to sustained operational high performance. Employees receive 22 vacation days "
                    "per year, accruing monthly from their date of hire. Annual leave must be booked through the HR portal at least two "
                    "weeks prior to the intended start date to ensure team coverage and business continuity.\n\n"
                    "3. CORPORATE TRAVEL AND ENTERTAINMENT GUIDELINES\n"
                    "All business travel must be justified by commercial or technical objectives. Travel must be booked through the "
                    "internal travel portal at least 14 days in advance to secure negotiated enterprise discounts. All travel itineraries "
                    "exceeding $1,000 require vice-president approval before ticketing. Expense reports with itemized receipts must be "
                    "submitted within 30 days of trip completion.\n\n"
                    "4. COMPLIANCE & MANDATORY SECURITY PROTOCOLS\n"
                    "Protecting customer information and industrial assets is non-negotiable. Security training is mandatory every year "
                    "for all staff. Completion certificates must be uploaded to the compliance portal by November 30th annually. Failure "
                    "to complete mandatory training may result in suspension of corporate network privileges."
                ),
            },
            {
                "title": "Globex Product Roadmap",
                "filename": "globex-roadmap.txt",
                "roles": ["admin", "manager"],
                "secrets": ["orion platform", "march 2027"],
                "text": (
                    "GLOBEX INDUSTRIES ENGINEERING & PRODUCT ROADMAP\n"
                    "Document ID: GLX-ENG-ROADMAP-2027 | Internal Product Strategy\n\n"
                    "1. CORE INFRASTRUCTURE MILESTONE\n"
                    "The Orion platform is scheduled for launch in March 2027. This platform re-engineers our distributed message pipeline "
                    "to achieve sub-millisecond data delivery at scale across edge nodes worldwide. Architectural improvements provide "
                    "fault tolerance, geo-replicated state storage, and dynamic load partitioning.\n\n"
                    "2. PARTNER ENGAGEMENT & BETA TIMELINE\n"
                    "Beta access begins in November for selected partners across the financial services sector. Feedback collection and "
                    "stress testing will run continuously through January, focusing on throughput under heavy market volatility and peak loads.\n\n"
                    "3. MOBILE CLIENT DEPLOYMENT AND ECOSYSTEM\n"
                    "The mobile client will follow one quarter after the main release, delivering native iOS and Android experiences. "
                    "Developer SDKs and client libraries in Rust, Go, and Python will be published concurrently with the enterprise launch."
                ),
            },
            {
                "title": "Globex Executive Compensation",
                "filename": "globex-exec-comp.txt",
                "roles": ["admin"],
                "secrets": ["2,300,000", "$600,000"],
                "text": (
                    "GLOBEX INDUSTRIES EXECUTIVE BOARD SUMMARY & COMPENSATION REVIEW\n"
                    "Document ID: GLX-BOD-2026-COMP | Restricted: Board & Administrators\n\n"
                    "1. EXECUTIVE BASE SALARY\n"
                    "The Globex chief executive earns a base salary of $2,300,000. This reflects executive leadership across multiple "
                    "international subsidiaries, direct oversight of multi-year infrastructure modernization, and operational expansion "
                    "into Asia-Pacific markets.\n\n"
                    "2. EXECUTIVE RETENTION PROGRAM\n"
                    "To maintain executive continuity during the Orion platform rollout, a retention bonus of $600,000 is paid to each "
                    "executive who remains through the end of next year. These figures are restricted to administrators. Any disclosure "
                    "outside authorized board channels constitutes a direct breach of fiduciary responsibility."
                ),
            },
        ],
    },
]
# Assert that every document without 'employee' role has non-empty secrets defined
for _t in TENANTS:
    for _d in _t["docs"]:
        if "employee" not in _d["roles"]:
            assert _d.get("secrets"), (
                f"Document {_d['title']!r} in tenant {_t['name']!r} has restricted roles "
                f"{_d['roles']} but no secrets defined for leak testing!"
            )

def all_users():
    """Yield (email, role, tenant_name) for every seeded user."""
    for tenant in TENANTS:
        for email, role, _dept in tenant["users"]:
            yield email, role, tenant["name"]


def visible_docs(tenant_name: str, role: str):
    for tenant in TENANTS:
        if tenant["name"] == tenant_name:
            return [d for d in tenant["docs"] if role in d["roles"]]
    return []


def forbidden_docs(tenant_name: str, role: str):
    """Every seeded document this user must never see (other tenants + higher roles)."""
    allowed = {d["title"] for d in visible_docs(tenant_name, role)}
    return [d for t in TENANTS for d in t["docs"] if d["title"] not in allowed]
