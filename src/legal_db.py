"""
In-memory legal document database with realistic contracts, cases, and statutes.
Production deployments should replace this with a proper search backend (Elasticsearch, pgvector, etc.).
"""

from typing import List, Optional
import re

# ---------------------------------------------------------------------------
# Document corpus
# ---------------------------------------------------------------------------

DOCUMENTS = [
    {
        "id": "doc-001",
        "title": "Standard Software as a Service (SaaS) Agreement",
        "type": "contract",
        "jurisdiction": "US-CA",
        "summary": (
            "A comprehensive SaaS subscription agreement covering service levels, data privacy, "
            "acceptable use, intellectual property ownership, limitation of liability, and termination rights."
        ),
        "date": "2024-01-15",
        "parties": ["Provider LLC", "Customer Entity"],
        "full_text": """SOFTWARE AS A SERVICE AGREEMENT

This Software as a Service Agreement ("Agreement") is entered into as of the Effective Date
between Provider LLC ("Provider") and the subscribing entity ("Customer").

1. SERVICES
Provider will make the Service available to Customer pursuant to this Agreement and the applicable
Order Form. Provider grants Customer a non-exclusive, non-transferable right to access and use the
Service during the Subscription Term, solely for Customer's internal business purposes.

2. RESTRICTIONS
Customer shall not: (a) license, sublicense, sell, resell, transfer, assign, or otherwise commercially
exploit the Service; (b) modify or make derivative works based upon the Service; (c) reverse engineer
the Service; (d) access the Service to build a competitive product or service.

3. FEES AND PAYMENT
Customer will pay all fees specified in Order Forms. Fees are non-refundable except as expressly set
forth herein. Provider reserves the right to modify pricing with thirty (30) days written notice.
Overdue amounts accrue interest at 1.5% per month.

4. DATA OWNERSHIP AND PRIVACY
As between Provider and Customer, Customer owns all Customer Data. Provider will maintain
appropriate administrative, physical, and technical safeguards for protection of Customer Data.
Provider will not disclose Customer Data to third parties except as compelled by law.

5. INTELLECTUAL PROPERTY
Provider retains all right, title, and interest in and to the Service. Customer retains all right,
title, and interest in and to Customer Data.

6. CONFIDENTIALITY
Each party agrees to protect the confidential information of the other party using the same degree
of care it uses for its own confidential information, but no less than reasonable care.

7. WARRANTIES AND DISCLAIMERS
Provider warrants that the Service will perform materially in accordance with the applicable
documentation. EXCEPT AS EXPRESSLY PROVIDED, THE SERVICE IS PROVIDED "AS IS." PROVIDER DISCLAIMS
ALL OTHER WARRANTIES, EXPRESS OR IMPLIED.

8. LIMITATION OF LIABILITY
IN NO EVENT SHALL EITHER PARTY'S AGGREGATE LIABILITY EXCEED THE FEES PAID IN THE TWELVE MONTHS
PRIOR TO THE CLAIM. IN NO EVENT SHALL EITHER PARTY BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL,
OR CONSEQUENTIAL DAMAGES.

9. TERM AND TERMINATION
This Agreement commences on the Effective Date and continues for the Initial Subscription Term.
Either party may terminate for material breach upon thirty (30) days written notice if such breach
remains uncured.

10. GOVERNING LAW
This Agreement shall be governed by the laws of the State of California, without regard to its
conflict of laws provisions. Disputes shall be resolved in San Francisco County, California.""",
        "citations": ["Cal. Civ. Code § 1670.8", "UCC § 2-316"],
        "tags": ["saas", "technology", "subscription", "software", "ip"],
    },
    {
        "id": "doc-002",
        "title": "Non-Disclosure Agreement (Mutual)",
        "type": "contract",
        "jurisdiction": "US-NY",
        "summary": (
            "Mutual NDA for business negotiations protecting trade secrets, proprietary technology, "
            "financial information, and business strategies. Includes carve-outs for public domain "
            "information and independent development."
        ),
        "date": "2024-03-22",
        "parties": ["Party A", "Party B"],
        "full_text": """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of the date last signed below
between the parties identified in the signature block (each a "Party" and collectively the "Parties").

1. PURPOSE
The Parties wish to explore a potential business relationship and may disclose certain confidential
information to each other for the purpose of evaluating such relationship ("Purpose").

2. CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by either Party that is designated as
confidential or that reasonably should be understood to be confidential given the nature of the
information and the circumstances of disclosure, including but not limited to: technical data,
trade secrets, know-how, research, product plans, products, services, customers, markets, software,
developments, inventions, processes, formulas, technology, designs, drawings, engineering, hardware
configuration, marketing plans, finances, or other business information.

3. EXCLUSIONS
Confidential Information does not include information that: (a) is or becomes publicly known through
no action or inaction of the receiving Party; (b) was in the receiving Party's possession before
disclosure; (c) is rightfully obtained from a third party without restriction; or (d) is independently
developed by the receiving Party without use of Confidential Information.

4. OBLIGATIONS
Each Party agrees to: (a) hold the other Party's Confidential Information in strict confidence;
(b) not disclose it to third parties without prior written consent; (c) use it only for the Purpose;
(d) protect it with at least the same degree of care used for its own confidential information.

5. TERM
This Agreement shall remain in effect for three (3) years from the date of execution. Obligations
of confidentiality survive termination for an additional two (2) years.

6. RETURN OF MATERIALS
Upon request, each Party shall return or certify destruction of all Confidential Information.

7. GOVERNING LAW
This Agreement shall be governed by the laws of the State of New York.""",
        "citations": ["N.Y. Gen. Bus. Law § 399-dd", "Uniform Trade Secrets Act"],
        "tags": ["nda", "confidentiality", "trade-secrets", "business"],
    },
    {
        "id": "doc-003",
        "title": "Employment Agreement — Senior Software Engineer",
        "type": "contract",
        "jurisdiction": "US-WA",
        "summary": (
            "At-will employment agreement for a senior software engineer role including compensation, "
            "equity vesting schedule, IP assignment, non-solicitation covenant, and benefits."
        ),
        "date": "2024-06-01",
        "parties": ["TechCorp Inc.", "Employee"],
        "full_text": """EMPLOYMENT AGREEMENT

This Employment Agreement ("Agreement") is entered into between TechCorp Inc. ("Company") and
the individual identified in the signature block ("Employee").

1. POSITION AND DUTIES
Employee is hired as Senior Software Engineer. Employee will report to the VP of Engineering and
perform duties consistent with the role, as reasonably directed by the Company.

2. COMPENSATION
Base Salary: $185,000 per year, payable in accordance with Company's standard payroll schedule.
Annual Bonus: Target of 15% of base salary, based on individual and Company performance metrics.
Equity: Option to purchase 25,000 shares of Common Stock, vesting over 4 years with a 1-year cliff,
subject to the Company's equity plan.

3. BENEFITS
Employee is eligible for standard Company benefits including health, dental, vision insurance;
401(k) with 4% employer match; and 20 days PTO per year.

4. AT-WILL EMPLOYMENT
Employment is at-will and may be terminated by either party at any time, with or without cause or
notice, subject to applicable law.

5. INTELLECTUAL PROPERTY ASSIGNMENT
Employee assigns to Company all inventions, developments, and works of authorship created during
employment that relate to the Company's business or result from use of Company resources.

6. NON-SOLICITATION
During employment and for twelve (12) months after termination, Employee will not solicit Company
employees or customers with whom Employee had material contact.

7. CONFIDENTIALITY
Employee agrees to maintain the confidentiality of all Company proprietary information during and
after employment.

8. GOVERNING LAW
This Agreement is governed by Washington State law. The non-solicitation provision shall not apply
to the extent prohibited by RCW 49.62.""",
        "citations": ["RCW 49.62", "RCW 49.44.140"],
        "tags": ["employment", "software-engineer", "equity", "ip-assignment", "non-solicitation"],
    },
    {
        "id": "doc-004",
        "title": "California Consumer Privacy Act (CCPA) — Cal. Civ. Code § 1798.100",
        "type": "statute",
        "jurisdiction": "US-CA",
        "summary": (
            "The CCPA grants California consumers rights over their personal information including "
            "the right to know, right to delete, right to opt-out of sale, and right to non-discrimination."
        ),
        "date": "2020-01-01",
        "parties": None,
        "full_text": """CALIFORNIA CONSUMER PRIVACY ACT OF 2018
Cal. Civ. Code § 1798.100 et seq.

§ 1798.100. Right to Know About Personal Information Collected, Disclosed, or Sold
(a) A consumer shall have the right to request that a business that collects a consumer's personal
information disclose to that consumer the categories and specific pieces of personal information
the business has collected.

(b) A business that collects a consumer's personal information shall, at or before the point of
collection, inform consumers as to the categories of personal information to be collected and the
purposes for which the categories of personal information shall be used.

§ 1798.105. Right to Delete Personal Information
(a) A consumer shall have the right to request that a business delete any personal information about
the consumer which the business has collected from the consumer.

(b) A business that receives a verifiable consumer request for deletion shall delete the consumer's
personal information from its records and direct any service providers to delete the consumer's
personal information from their records.

§ 1798.110. Right to Know Categories of Personal Information Disclosed
A consumer shall have the right to request that a business that sells the consumer's personal
information, or that discloses it for a business purpose, disclose to that consumer:
(a) The categories of personal information that the business collected about the consumer.
(b) The categories of personal information that the business sold about the consumer.
(c) The categories of third parties to whom the personal information was sold.

§ 1798.120. Right to Opt-Out of Sale of Personal Information
(a) A consumer shall have the right, at any time, to direct a business that sells personal information
about the consumer to third parties not to sell the consumer's personal information.

§ 1798.125. Right to Non-Discrimination
(a)(1) A business shall not discriminate against a consumer because the consumer exercised any of the
consumer's rights under this title, including by:
(A) Denying goods or services to the consumer.
(B) Charging different prices or rates for goods or services.
(C) Providing a different level or quality of goods or services.

§ 1798.185. Regulations
The Attorney General shall solicit broad public participation and adopt regulations to further the
purposes of this title.""",
        "citations": ["Cal. Civ. Code § 1798.100", "GDPR Art. 17", "40 C.F.R. § 122"],
        "tags": ["privacy", "ccpa", "california", "consumer-rights", "data-protection"],
    },
    {
        "id": "doc-005",
        "title": "Commercial Lease Agreement — Office Space",
        "type": "contract",
        "jurisdiction": "US-TX",
        "summary": (
            "Commercial office lease covering rent escalation schedule, tenant improvement allowance, "
            "subletting rights, force majeure provisions, and landlord/tenant maintenance obligations."
        ),
        "date": "2023-11-01",
        "parties": ["Landlord Property Group LLC", "Tenant Corp"],
        "full_text": """COMMERCIAL LEASE AGREEMENT

This Commercial Lease Agreement ("Lease") is entered into between Landlord Property Group LLC
("Landlord") and Tenant Corp ("Tenant").

PREMISES: Suite 400, 1200 Main Street, Austin, TX 78701, comprising approximately 8,500 rentable
square feet ("Premises").

1. TERM
The Lease Term commences on January 1, 2024 and expires on December 31, 2028 (60 months).

2. RENT
Base Rent: $25,500/month (Year 1), escalating 3% annually.
Year 1: $25,500/month | Year 2: $26,265/month | Year 3: $27,053/month
Year 4: $27,865/month | Year 5: $28,701/month

3. SECURITY DEPOSIT
Tenant shall deposit $76,500 (3 months' rent) as security. Deposit earns no interest.

4. TENANT IMPROVEMENT ALLOWANCE
Landlord provides a $127,500 ($15/SF) Tenant Improvement Allowance for approved improvements.
Any unused allowance is forfeited.

5. USE
Premises shall be used solely for general office purposes. Tenant shall comply with all applicable
laws, codes, and regulations.

6. MAINTENANCE
Landlord: HVAC systems, building structure, common areas, plumbing, electrical to suite.
Tenant: Interior surfaces, light bulbs, suite-level fixtures, and Tenant's property.

7. SUBLETTING AND ASSIGNMENT
Tenant may not sublet or assign without Landlord's prior written consent, not to be unreasonably withheld.
Landlord may withhold consent if proposed subtenant's credit is materially weaker than Tenant's.

8. FORCE MAJEURE
Neither party shall be in default if performance is delayed by acts of God, government orders,
pandemics, or other events beyond reasonable control, provided prompt written notice is given.

9. DEFAULT AND REMEDIES
If Tenant fails to pay rent within 5 days of due date, Landlord may assess a 5% late fee.
After 30 days' written notice and failure to cure, Landlord may terminate this Lease.

10. GOVERNING LAW
Texas law governs this Lease. Venue is Travis County, Texas.""",
        "citations": ["Tex. Prop. Code § 91.001", "Tex. Prop. Code § 93.001"],
        "tags": ["commercial-lease", "real-estate", "office", "texas"],
    },
    {
        "id": "doc-006",
        "title": "General Data Protection Regulation (GDPR) — Article 17 Right to Erasure",
        "type": "statute",
        "jurisdiction": "EU",
        "summary": (
            "GDPR Article 17 establishes the 'right to be forgotten', requiring data controllers to "
            "erase personal data without undue delay when specified conditions are met."
        ),
        "date": "2018-05-25",
        "parties": None,
        "full_text": """GENERAL DATA PROTECTION REGULATION (EU) 2016/679
Article 17 — Right to Erasure ('Right to Be Forgotten')

1. The data subject shall have the right to obtain from the controller the erasure of personal data
concerning him or her without undue delay and the controller shall have the obligation to erase
personal data without undue delay where one of the following grounds applies:

(a) the personal data are no longer necessary in relation to the purposes for which they were
collected or otherwise processed;

(b) the data subject withdraws consent on which the processing is based according to point (a) of
Article 6(1), or point (a) of Article 9(2), and where there is no other legal ground for the processing;

(c) the data subject objects to the processing pursuant to Article 21(1) and there are no overriding
legitimate grounds for the processing, or the data subject objects to the processing pursuant to
Article 21(2);

(d) the personal data have been unlawfully processed;

(e) the personal data have to be erased for compliance with a legal obligation in Union or Member
State law to which the controller is subject;

(f) the personal data have been collected in relation to the offer of information society services
referred to in Article 8(1).

2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to
erase the personal data, the controller, taking account of available technology and the cost of
implementation, shall take reasonable steps, including technical measures, to inform controllers
which are processing the personal data that the data subject has requested the erasure.

3. Paragraphs 1 and 2 shall not apply to the extent that processing is necessary:
(a) for exercising the right of freedom of expression and information;
(b) for compliance with a legal obligation which requires processing by Union or Member State law;
(c) for reasons of public interest in the area of public health;
(d) for archiving purposes in the public interest, scientific or historical research purposes or
statistical purposes in accordance with Article 89(1);
(e) for the establishment, exercise or defence of legal claims.""",
        "citations": ["GDPR Art. 6", "GDPR Art. 9", "GDPR Art. 21", "GDPR Art. 89"],
        "tags": ["gdpr", "privacy", "eu", "right-to-erasure", "data-protection"],
    },
]

# ---------------------------------------------------------------------------
# Case law corpus
# ---------------------------------------------------------------------------

CASES = [
    {
        "id": "case-001",
        "case_name": "Smith v. National Data Corp.",
        "citation": "487 F.3d 1200 (9th Cir. 2023)",
        "court": "9th Circuit",
        "year": 2023,
        "judges": ["Hon. Patricia Chen", "Hon. Robert Vasquez", "Hon. Linda Park"],
        "summary": (
            "Ninth Circuit held that AI-generated data profiles constitute 'personal information' "
            "under the CCPA, affirming injunctive relief and damages award."
        ),
        "facts": (
            "National Data Corp. aggregated public records, social media activity, and purchase history "
            "to build detailed consumer profiles, selling them to marketing firms without consumer "
            "consent. Plaintiff class alleged violations of the CCPA and California's Unfair "
            "Competition Law (UCL). District court granted summary judgment for plaintiffs and awarded "
            "$45 million in statutory damages."
        ),
        "holding": (
            "AI-synthesized consumer profiles derived from multiple public data sources constitute "
            "'personal information' under Cal. Civ. Code § 1798.140(o). Sale of such profiles without "
            "opt-out mechanism violates CCPA § 1798.120. Statutory damages of $100-$750 per consumer "
            "per incident are appropriate."
        ),
        "reasoning": (
            "The court reasoned that the CCPA's definition of personal information is intentionally "
            "broad and technology-neutral. Even where individual data points are public, their "
            "aggregation into a profile capable of uniquely identifying a consumer falls within the "
            "statute's protective scope. The court rejected the argument that data already in the public "
            "domain loses privacy protection upon aggregation, citing legislative history emphasizing "
            "the aggregation problem."
        ),
        "dissent": (
            "Judge Vasquez dissented, arguing the majority's reading extends the CCPA beyond its "
            "textual limits and that fully public information cannot form the basis of a privacy claim."
        ),
        "citations_cited": [
            "Cal. Civ. Code § 1798.100",
            "Cal. Civ. Code § 1798.120",
            "Cal. Civ. Code § 1798.140(o)",
            "Sorrells v. Cliffs Internet, 312 F.3d 1101 (9th Cir. 2020)",
        ],
        "cited_by": [
            "Ramirez v. AdTech Partners, 501 F.3d 890 (9th Cir. 2024)",
            "FTC v. DataBroker Inc., 58 F.4th 222 (D.C. Cir. 2024)",
        ],
        "tags": ["ccpa", "privacy", "ai", "data-broker", "class-action"],
    },
    {
        "id": "case-002",
        "case_name": "Blockchain Ventures LLC v. FinTech Dynamics Inc.",
        "citation": "334 F. Supp. 3d 445 (S.D.N.Y. 2022)",
        "court": "S.D.N.Y.",
        "year": 2022,
        "judges": ["Hon. Margaret O'Brien"],
        "summary": (
            "Southern District of New York enforced a SaaS agreement's limitation of liability clause "
            "against breach of contract and negligence claims arising from a platform outage."
        ),
        "facts": (
            "Plaintiff Blockchain Ventures entered a SaaS agreement with FinTech Dynamics for trading "
            "infrastructure. A 14-hour outage caused by defendant's misconfigured load balancer "
            "resulted in plaintiff's claimed losses of $8.2 million in missed trading opportunities. "
            "The SaaS agreement capped liability at fees paid in the prior 12 months ($420,000)."
        ),
        "holding": (
            "The limitation of liability clause is enforceable under New York law. Plaintiff's recovery "
            "is capped at $420,000 — the contractually specified maximum. The clause is not unconscionable "
            "where parties are sophisticated commercial entities that negotiated at arm's length."
        ),
        "reasoning": (
            "Under New York law, courts enforce limitation of liability clauses between commercial parties "
            "unless the clause is unconscionable or violates public policy. The clause was conspicuous, "
            "negotiated, and mutual. Plaintiff's claimed consequential damages — lost trading profits — "
            "are precisely the type of speculative losses that such clauses are designed to exclude. "
            "The court distinguished cases involving gross negligence or intentional misconduct."
        ),
        "dissent": None,
        "citations_cited": [
            "Kalisch-Jarcho, Inc. v. City of New York, 58 N.Y.2d 377 (1983)",
            "Sommer v. Federal Signal Corp., 79 N.Y.2d 540 (1992)",
            "UCC § 2-719",
        ],
        "cited_by": [
            "Axon Technologies v. CloudBase LLC, 401 F. Supp. 3d 120 (S.D.N.Y. 2023)",
        ],
        "tags": ["saas", "limitation-of-liability", "breach-of-contract", "commercial", "new-york"],
    },
    {
        "id": "case-003",
        "case_name": "Alvarez v. Horizon Healthcare Group",
        "citation": "612 F.3d 788 (5th Cir. 2023)",
        "court": "5th Circuit",
        "year": 2023,
        "judges": ["Hon. James Tatum", "Hon. Sarah Nguyen", "Hon. William Cross"],
        "summary": (
            "Fifth Circuit affirmed jury verdict finding employer liable for wrongful termination "
            "in violation of FMLA after employee was dismissed during protected medical leave."
        ),
        "facts": (
            "Plaintiff Maria Alvarez, a registered nurse employed by Horizon Healthcare Group for "
            "11 years, requested FMLA leave for a serious health condition. Within three weeks of "
            "returning from leave, she was terminated for alleged performance deficiencies. Evidence "
            "showed her performance evaluations had been uniformly positive prior to the leave request. "
            "The jury awarded $325,000 in compensatory damages and $800,000 in punitive damages."
        ),
        "holding": (
            "Employer's termination of employee within three weeks of FMLA leave return, combined with "
            "pretextual performance justification contradicted by prior reviews, constitutes FMLA "
            "retaliation under 29 U.S.C. § 2615(a)(2). Punitive damages award is affirmed."
        ),
        "reasoning": (
            "The court applied the burden-shifting McDonnell Douglas framework. Plaintiff established "
            "a prima facie case of retaliation through temporal proximity and stellar prior evaluations. "
            "Defendant's articulated reason — performance deficiencies — was undermined by the "
            "documentary record. The inference of pretext was further supported by the supervisor's "
            "comment that Alvarez's leave had been 'inconvenient for the unit.' The court found "
            "sufficient evidence of malice to sustain the punitive damages award."
        ),
        "dissent": None,
        "citations_cited": [
            "29 U.S.C. § 2615(a)(2)",
            "McDonnell Douglas Corp. v. Green, 411 U.S. 792 (1973)",
            "Elsensohn v. St. Tammany Parish Sheriff's Office, 530 F.3d 368 (5th Cir. 2008)",
        ],
        "cited_by": [
            "Torres v. MedGroup Inc., 644 F.3d 102 (5th Cir. 2024)",
        ],
        "tags": ["employment", "fmla", "wrongful-termination", "retaliation", "healthcare"],
    },
    {
        "id": "case-004",
        "case_name": "OpenAI Technologies Inc. v. Synthesize Corp.",
        "citation": "No. 23-cv-04521 (N.D. Cal. 2024)",
        "court": "N.D. Cal.",
        "year": 2024,
        "judges": ["Hon. Diane Lev"],
        "summary": (
            "District court denied preliminary injunction in copyright infringement suit over AI model "
            "training on copyrighted works, finding plaintiff failed to demonstrate likelihood of success."
        ),
        "facts": (
            "Plaintiff alleged defendant's large language model was trained on plaintiff's proprietary "
            "dataset without license, constituting copyright infringement and misappropriation of trade "
            "secrets. Defendant moved to dismiss, arguing fair use and the transformative nature of AI "
            "training. Plaintiff sought a preliminary injunction to halt model deployment."
        ),
        "holding": (
            "Plaintiff's motion for preliminary injunction is DENIED. Plaintiff has not demonstrated "
            "a likelihood of success on the merits on either the copyright or trade secrets claims. "
            "The balance of equities and public interest do not favor a halt to model deployment pending "
            "full adjudication."
        ),
        "reasoning": (
            "On copyright: the court found the fair use question is genuinely contested and not clearly "
            "resolved in plaintiff's favor. AI training may qualify as transformative use, and plaintiff "
            "failed to demonstrate market harm from the training use specifically. On trade secrets: "
            "plaintiff presented insufficient evidence that defendant obtained the dataset through "
            "improper means rather than independent collection. Injunctive relief in this nascent "
            "legal area requires a clearer showing than plaintiff provided."
        ),
        "dissent": None,
        "citations_cited": [
            "17 U.S.C. § 107",
            "Uniform Trade Secrets Act",
            "Authors Guild v. Google Inc., 804 F.3d 202 (2d Cir. 2015)",
            "Campbell v. Acuff-Rose Music Inc., 510 U.S. 569 (1994)",
        ],
        "cited_by": [],
        "tags": ["ai", "copyright", "fair-use", "trade-secrets", "llm", "preliminary-injunction"],
    },
    {
        "id": "case-005",
        "case_name": "In re TechStart Inc. Bankruptcy",
        "citation": "No. 23-11052 (Bankr. D. Del. 2024)",
        "court": "Bankr. D. Del.",
        "year": 2024,
        "judges": ["Hon. Robert M. Sheridan"],
        "summary": (
            "Delaware bankruptcy court approved Chapter 11 reorganization plan for AI startup, "
            "addressing treatment of IP assets, employee retention, and creditor waterfall."
        ),
        "facts": (
            "TechStart Inc., an AI infrastructure company, filed for Chapter 11 protection with "
            "$142 million in secured debt and $38 million in unsecured claims. The company's primary "
            "assets were three issued patents, one pending patent application, and a proprietary "
            "training dataset. A stalking horse bidder offered $67 million for the IP assets. Secured "
            "creditors objected to the proposed distribution waterfall."
        ),
        "holding": (
            "Reorganization plan is CONFIRMED. The court approves the $67 million stalking horse "
            "bid as fair and reasonable. The proposed distribution waterfall complies with the "
            "absolute priority rule. Employee retention bonuses are approved as necessary to preserve "
            "going concern value during the sale process."
        ),
        "reasoning": (
            "The court found the plan was proposed in good faith and the IP valuation methodology "
            "was sound. The stalking horse protections (3% break-up fee plus expense reimbursement) "
            "were within market range and necessary to attract competitive bids. Secured creditors "
            "will receive 47 cents on the dollar — below par but above liquidation value. The court "
            "rejected the unsecured creditors' committee's objection to the retention bonuses, finding "
            "them essential to preserving the value of the estate's assets."
        ),
        "dissent": None,
        "citations_cited": [
            "11 U.S.C. § 363",
            "11 U.S.C. § 1129",
            "In re Integrated Resources, 147 B.R. 650 (Bankr. S.D.N.Y. 1992)",
        ],
        "cited_by": [],
        "tags": ["bankruptcy", "chapter-11", "ip-assets", "ai", "delaware", "reorganization"],
    },
]

# ---------------------------------------------------------------------------
# Template corpus
# ---------------------------------------------------------------------------

TEMPLATES = {
    "nda": {
        "type": "nda",
        "title": "Mutual Non-Disclosure Agreement Template",
        "description": (
            "Balanced mutual NDA suitable for business negotiations, partnership discussions, "
            "and M&A due diligence. Includes carve-outs for public domain, independent development, "
            "and compelled disclosure."
        ),
        "jurisdiction": "US (Multi-State)",
        "last_updated": "2024-08-01",
        "sections": [
            "Parties",
            "Definition of Confidential Information",
            "Exclusions",
            "Obligations of Receiving Party",
            "Term and Survival",
            "Return or Destruction of Materials",
            "Injunctive Relief",
            "Governing Law",
            "Signature Block",
        ],
        "template_text": """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of [DATE] ("Effective Date")
between [PARTY A NAME], a [STATE] [ENTITY TYPE] ("Party A"), and [PARTY B NAME], a [STATE] [ENTITY TYPE]
("Party B") (each a "Party" and collectively the "Parties").

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by one Party ("Discloser") to the other
("Recipient") that is: (a) marked "Confidential" or "Proprietary"; (b) identified as confidential
at time of oral disclosure and confirmed in writing within [10] days; or (c) reasonably understood
to be confidential given the nature and circumstances of disclosure.

Confidential Information includes, without limitation: business plans, financial projections,
customer lists, technical specifications, source code, trade secrets, product roadmaps, pricing,
and personnel information.

2. EXCLUSIONS
Confidential Information does not include information that:
(a) Is or becomes publicly available through no breach of this Agreement;
(b) Was rightfully known to Recipient before disclosure;
(c) Is rightfully obtained from a third party without restriction;
(d) Is independently developed by Recipient without use of Confidential Information;
(e) Must be disclosed by law or court order (with prompt notice to Discloser).

3. OBLIGATIONS
Recipient agrees to:
(a) Use Confidential Information solely for [PURPOSE];
(b) Hold it in confidence with at least reasonable care;
(c) Disclose it only to employees/contractors with need-to-know who are bound by confidentiality;
(d) Notify Discloser promptly of any unauthorized disclosure.

4. TERM
This Agreement is effective as of the Effective Date and continues for [2] years. Obligations of
confidentiality survive expiration for [2] additional years.

5. RETURN / DESTRUCTION
Upon written request, Recipient shall promptly return or certify destruction of all Confidential
Information, except for archival copies retained by counsel.

6. INJUNCTIVE RELIEF
Breach may cause irreparable harm for which monetary damages are inadequate. Each Party consents
to injunctive relief without bond or other security.

7. GOVERNING LAW
This Agreement is governed by the laws of [GOVERNING STATE], without regard to conflicts principles.

PARTY A: _________________________    PARTY B: _________________________
Name:    _________________________    Name:    _________________________
Title:   _________________________    Title:   _________________________
Date:    _________________________    Date:    _________________________""",
        "notes": (
            "Replace bracketed placeholders before use. Consider state-specific requirements "
            "for trade secret protection. If one party is the primary discloser, consider a "
            "one-way NDA instead."
        ),
    },
    "saas_agreement": {
        "type": "saas_agreement",
        "title": "Software as a Service (SaaS) Subscription Agreement Template",
        "description": (
            "Comprehensive SaaS agreement for B2B software providers. Covers service levels, "
            "data security, intellectual property, limitation of liability, and termination."
        ),
        "jurisdiction": "US (Multi-State)",
        "last_updated": "2024-10-15",
        "sections": [
            "Services and License",
            "Restrictions",
            "Fees and Payment",
            "Service Levels and Support",
            "Data Ownership and Security",
            "Intellectual Property",
            "Confidentiality",
            "Warranties",
            "Limitation of Liability",
            "Indemnification",
            "Term and Termination",
            "General Provisions",
        ],
        "template_text": """SOFTWARE AS A SERVICE AGREEMENT

This Software as a Service Agreement ("Agreement") is entered into as of [DATE] ("Effective Date")
between [PROVIDER NAME] ("Provider") and [CUSTOMER NAME] ("Customer").

1. SERVICES AND LICENSE
Provider grants Customer a non-exclusive, non-transferable right to access and use [SERVICE NAME]
("Service") during the Subscription Term for Customer's internal business purposes, subject to this
Agreement and the applicable Order Form.

2. RESTRICTIONS
Customer shall not: (a) sublicense or resell access; (b) reverse engineer the Service;
(c) use the Service to build a competitive product; (d) access beyond authorized users.

3. FEES AND PAYMENT
Fees are as specified in the Order Form. Invoices are due [30] days from receipt. Overdue amounts
accrue interest at [1.5%/month]. Provider may suspend Service after [15] days' notice of non-payment.

4. SERVICE LEVELS
Provider targets [99.9%] monthly uptime, excluding scheduled maintenance and events beyond Provider's
control. Customer's sole remedy for SLA breach is service credits per the SLA Schedule.

5. DATA OWNERSHIP AND SECURITY
Customer owns all Customer Data. Provider processes Customer Data only to deliver the Service.
Provider will maintain industry-standard security controls (SOC 2 Type II or equivalent).

6. INTELLECTUAL PROPERTY
Provider retains all right in the Service. Customer retains all right in Customer Data.
Each party retains pre-existing IP.

7. CONFIDENTIALITY
Each party will protect the other's Confidential Information using reasonable care and not disclose
it to third parties without consent. Obligations survive termination for [3] years.

8. WARRANTIES
Provider warrants the Service will perform materially per documentation. EXCEPT AS STATED, THE
SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND.

9. LIMITATION OF LIABILITY
AGGREGATE LIABILITY IS CAPPED AT FEES PAID IN THE PRIOR [12] MONTHS. NEITHER PARTY IS LIABLE FOR
INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES.

10. INDEMNIFICATION
Each party will indemnify the other for third-party claims arising from: (a) Provider's infringement
of third-party IP; (b) Customer's misuse of the Service or Customer Data.

11. TERM AND TERMINATION
Initial term: [1 year], auto-renewing unless cancelled [30] days before renewal. Either party may
terminate for material breach upon [30] days' notice if uncured.

12. GENERAL
Governing law: [STATE]. Entire agreement. Amendments must be in writing.""",
        "notes": (
            "Customize SLA targets, liability caps, and data security requirements based on "
            "your risk profile. B2B enterprise customers will often negotiate limits and indemnities."
        ),
    },
    "employment_agreement": {
        "type": "employment_agreement",
        "title": "At-Will Employment Agreement Template",
        "description": (
            "Standard at-will employment agreement for US companies covering compensation, "
            "equity, IP assignment, confidentiality, and non-solicitation."
        ),
        "jurisdiction": "US (Multi-State)",
        "last_updated": "2024-09-01",
        "sections": [
            "Position and Start Date",
            "Compensation and Benefits",
            "Equity",
            "At-Will Status",
            "IP Assignment",
            "Confidentiality",
            "Non-Solicitation",
            "Arbitration",
            "Governing Law",
        ],
        "template_text": """EMPLOYMENT AGREEMENT

This Employment Agreement is entered into as of [START DATE] between [COMPANY NAME] ("Company")
and [EMPLOYEE NAME] ("Employee").

1. POSITION
Employee is hired as [JOB TITLE], reporting to [REPORTING MANAGER TITLE], commencing [START DATE].

2. COMPENSATION
Base Salary: $[AMOUNT] per year, paid per Company's standard payroll schedule.
Bonus: Target [X]% of base salary, subject to individual and Company performance.
Benefits: Employee is eligible for standard Company benefits as described in the Employee Handbook.

3. EQUITY
Subject to Board approval and the Company's equity plan, Employee will receive [X shares / X options]
vesting over [4 years] with a [1-year] cliff.

4. AT-WILL EMPLOYMENT
Employment is at-will. Either party may terminate the relationship at any time, with or without
cause or advance notice, subject to applicable law.

5. INTELLECTUAL PROPERTY ASSIGNMENT
Employee assigns to Company all inventions conceived or reduced to practice during employment that:
(a) relate to the Company's business; or (b) result from use of Company resources.
[Note: California, Washington, Delaware, and other states have statutory carve-outs for inventions
developed entirely on Employee's own time without Company resources — include applicable carve-out.]

6. CONFIDENTIALITY
Employee will not use or disclose Company Confidential Information during or after employment,
except as necessary to perform job duties.

7. NON-SOLICITATION
For [12 months] after termination, Employee will not solicit Company employees or customers with
whom Employee had material contact during the last [12 months] of employment.
[Note: Non-competes and broad non-solicitation clauses are void or heavily restricted in CA, ND, OK,
MN, and other states. Confirm enforceability in applicable jurisdiction.]

8. DISPUTE RESOLUTION
Disputes shall be resolved by binding arbitration under [AAA / JAMS] rules in [CITY, STATE].
Class action waiver applies to the maximum extent permitted by law.

9. GOVERNING LAW
[STATE] law governs this Agreement. This is the entire agreement between the parties regarding
employment terms and supersedes all prior negotiations.""",
        "notes": (
            "Non-compete and non-solicitation enforceability varies significantly by state. "
            "Review IP assignment carve-outs for your jurisdiction. Have employment counsel "
            "review before use in California, Washington, Illinois, or Minnesota."
        ),
    },
    "independent_contractor": {
        "type": "independent_contractor",
        "title": "Independent Contractor Agreement Template",
        "description": (
            "Contractor agreement covering scope of work, payment terms, IP assignment, "
            "independent contractor status, and confidentiality."
        ),
        "jurisdiction": "US (Multi-State)",
        "last_updated": "2024-07-15",
        "sections": [
            "Services and Deliverables",
            "Compensation and Invoicing",
            "Independent Contractor Status",
            "Intellectual Property",
            "Confidentiality",
            "Term and Termination",
            "Governing Law",
        ],
        "template_text": """INDEPENDENT CONTRACTOR AGREEMENT

This Independent Contractor Agreement ("Agreement") is entered into as of [DATE] between
[COMPANY NAME] ("Company") and [CONTRACTOR NAME] ("Contractor").

1. SERVICES
Contractor will provide the following services: [DESCRIPTION OF SERVICES].
Deliverables: [LIST DELIVERABLES AND MILESTONES].
Timeline: [PROJECT TIMELINE OR DURATION].

2. COMPENSATION
Rate: $[AMOUNT] per [hour/project].
Payment: Company will pay invoices within [30] days of receipt.
Expenses: [Reimbursed per policy / not reimbursed] with prior written approval.

3. INDEPENDENT CONTRACTOR STATUS
Contractor is an independent contractor, not an employee. Contractor is responsible for all taxes
on compensation received. Company will issue Form 1099-NEC if required by law.
Contractor retains control over the manner and means of performing the Services.

4. INTELLECTUAL PROPERTY
All work product, deliverables, and inventions created under this Agreement are "works made for hire"
to the maximum extent permitted by law. To the extent not qualifying as work for hire, Contractor
irrevocably assigns all rights in such work product to Company.

5. CONFIDENTIALITY
Contractor will not disclose Company Confidential Information during or after this Agreement.
Obligations survive termination for [3] years.

6. TERM AND TERMINATION
Term: [START DATE] through [END DATE / COMPLETION OF PROJECT].
Either party may terminate with [14] days' written notice. Company may terminate immediately for
material breach.

7. GOVERNING LAW
[STATE] law governs. Entire Agreement. Amendments must be in writing.""",
        "notes": (
            "Misclassification risk is significant. Apply the ABC test (California/Massachusetts) "
            "or economic reality test to confirm contractor status. Have outside counsel review "
            "for engagements over $25,000 or where contractor works exclusively for Company."
        ),
    },
}

# ---------------------------------------------------------------------------
# Category metadata
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "id": "cat-contracts",
        "name": "Contracts & Agreements",
        "description": "Commercial contracts, employment agreements, and other binding legal instruments.",
        "document_count": 3,
        "subtypes": ["saas_agreement", "nda", "employment_agreement", "independent_contractor", "commercial_lease"],
    },
    {
        "id": "cat-statutes",
        "name": "Statutes & Regulations",
        "description": "Federal and state legislation, administrative regulations, and ordinances.",
        "document_count": 2,
        "subtypes": ["privacy_law", "employment_law", "securities_regulation", "tax_law"],
    },
    {
        "id": "cat-case-law",
        "name": "Case Law & Judicial Opinions",
        "description": "Published court opinions from federal and state courts across all circuits.",
        "document_count": 5,
        "subtypes": ["circuit_court", "district_court", "bankruptcy_court", "state_supreme_court"],
    },
    {
        "id": "cat-templates",
        "name": "Legal Templates",
        "description": "Attorney-reviewed template agreements and forms for common legal needs.",
        "document_count": 4,
        "subtypes": ["nda", "saas_agreement", "employment_agreement", "independent_contractor"],
    },
]


# ---------------------------------------------------------------------------
# Search helpers
# ---------------------------------------------------------------------------

def _score(text: str, query: str) -> float:
    """Naive relevance score based on term frequency."""
    query_terms = re.findall(r"\w+", query.lower())
    text_lower = text.lower()
    if not query_terms:
        return 0.5
    hits = sum(1 for term in query_terms if term in text_lower)
    return round(min(hits / len(query_terms), 1.0), 2)


def search_documents(
    q: str,
    doc_type: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    limit: int = 10,
) -> List[dict]:
    results = []
    for doc in DOCUMENTS:
        if doc_type and doc["type"] != doc_type:
            continue
        if jurisdiction and jurisdiction.upper() not in doc["jurisdiction"].upper():
            continue
        searchable = f"{doc['title']} {doc['summary']} {' '.join(doc['tags'])}"
        score = _score(searchable, q)
        if score > 0 or not q:
            results.append({**doc, "relevance_score": score if q else 1.0})
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:limit]


def get_document(doc_id: str) -> Optional[dict]:
    for doc in DOCUMENTS:
        if doc["id"] == doc_id:
            return doc
    return None


def search_cases(
    q: str,
    court: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = 10,
) -> List[dict]:
    results = []
    for case in CASES:
        if court and court.lower() not in case["court"].lower():
            continue
        if year and case["year"] != year:
            continue
        searchable = f"{case['case_name']} {case['summary']} {case['holding']} {' '.join(case['tags'])}"
        score = _score(searchable, q)
        if score > 0 or not q:
            results.append({**case, "relevance_score": score if q else 1.0})
    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:limit]


def get_case(case_id: str) -> Optional[dict]:
    for case in CASES:
        if case["id"] == case_id:
            return case
    return None


def get_template(template_type: str) -> Optional[dict]:
    return TEMPLATES.get(template_type.lower())


def get_categories() -> List[dict]:
    return CATEGORIES
