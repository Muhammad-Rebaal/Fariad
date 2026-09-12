# Karachi Civic Authorities — Complete Reference
### Mandates, Jurisdiction, Websites & How to File a Complaint With Each

*Compiled Sept 2026. Government websites in Karachi change domains/uptime often — re-verify links periodically in production.*

---

## Output Formatting Rules (CRITICAL)
When responding to a user's complaint, you MUST follow these formatting rules:
1. **Already Registered Check**: If the User Context indicates "Prior Complaints in Area" > 0, you MUST explicitly state that similar complaints from their area are already registered in the system, and show them the exact count of prior complaints.
2. **Multiple Parties/Authorities**: If the complaint involves multiple authorities (e.g. KMC and KWSC both have overlapping jurisdictions or need to be contacted), you MUST provide the contact links and details for ALL involved parties. Present them clearly and distinctly, explaining exactly what each party is responsible for and what the user needs to do with them. Do not just show one contact.

---

## 1. Karachi Metropolitan Corporation (KMC)

**Website:** kmc.gos.pk (also home.kmc.gos.pk / e-section pages)
**Legal basis:** Sindh Local Government Act, 2013 (SLGA) / Sindh People's Local Government Act, 2021
**HQ:** KMC Building, M.A. Jinnah Road, Karachi | Phone: +92 21 992 1511-7 | mayor@kmc.gos.pk

**Responsible for:**
- Roads, streetlights, traffic signals (non-cantonment areas)
- Parks, playgrounds, public gardens
- Storm-water drains (as distinct from sewerage — overlaps with KWSC on some drains)
- Birth/death/marriage certificates
- Katchi abadi regularization matters (shared with Sindh Katchi Abadi Authority)
- Anti-encroachment on KMC land/roads (Anti-Encroachment Department)
- Coordinating/oversight umbrella for KWSC, SSWMB, SBCA at the city level (technically attached provincial departments, not KMC sub-departments, but KMC's site links to all of them as "sister departments")

**Not responsible for:** water/sewerage (KWSC), garbage collection contracts (SSWMB), building plan approval (SBCA), cantonment areas.

**How to file a complaint:**
- **Accepts online complaints:** Yes, but through two different, inconsistent front doors — see note below
- **Channel 1 — CCIS portal (the real complaint system):** complaint.kmc.gos.pk/ccis → "Log New Complaint." This requires a "Find Landmark" step (select town/UC/nearest landmark) before you can log the complaint. The page actively blocks automated access, so its exact field list can't be verified programmatically — build your generator to output name, phone, CNIC, town/UC, category, and description, and have the user paste/complete the form manually.
- **Channel 2 — kmc.gos.pk/contact-us/:** on inspection, this page (and its sibling "Contact 1" page) is still running **placeholder/template content** carried over from the WordPress theme — it displays a dummy US address ("345 Park Avenue, San Jose, CA 95110") and a dummy email (egovt@example.com) rather than a working KMC-specific form. **Don't route users to this page expecting a functional complaint form** — treat it as unreliable until KMC finishes rebuilding the site.
- **Channel 3 — phone:** helpline **1339** (KMC-specific, operator logs and routes your complaint); Sindh-wide alternative **1093** (LGD's 24/7 complaint line, also handles birth/death/marriage certificate queries).
- **Verified KMC contact points:** HQ — 1st Floor, M.A. Jinnah Road, Karachi | Phone (general): +92 21 992 1511-7 | Mayor's office direct: (021) 99215125-6 | Email: mayor@kmc.gos.pk | Hours: Mon–Fri, 9:00 am–5:00 pm.
- **Info required (CCIS / 1339):** Name, phone number, CNIC; location via town/UC/landmark; complaint category (roads, streetlights, drains, parks, property assessment, building-plan alteration); free-text description. No document upload is confirmed as mandatory, but a photo strengthens the complaint.

---

## 2. Karachi Water & Sewerage Corporation (KWSC, formerly KWSB)

**Website:** kwsc.gos.pk
**Legal basis:** Sindh Water & Sewerage Services Corporation Act (post-2018 corporatization); previously Sindh Local Government Ordinance-era KWSB
**HQ:** 9th Mile Karsaz, Shahrah-e-Faisal, Karachi

**Responsible for:**
- Water supply (production, transmission, distribution), all non-cantonment areas
- Sewerage network operation, maintenance, and treatment
- Water tanker booking (official channel for areas without piped supply)
- Billing, new connections, illegal-connection complaints
- Sewer line bursts / choked sewers / sewage overflow on roads

**Not responsible for:** storm-water drains not tied to sewerage (KMC), water/sewerage inside cantonment limits (individual cantonment boards run their own).

**Core mandate (three functions):**
1. Bulk production, filtration, treatment, conservation, transmission, and retail distribution of clean water
2. Collection, pumping, treatment, and disposal of sewage and industrial waste in Karachi
3. Billing and collection of water and sewerage charges, including arrears, from consumers

**E-services offered:**
- **E-Payment** — pay water/sewerage bills online
- **Online Duplicate Bills** — retrieve a duplicate bill
- **E-Complaint** — file complaints online (see below)
- **E-Tracking** — track the status of a filed complaint
(Accessed via the "e-Services" menu on the KWSC site.)

**Other contact points (in addition to the main helpline/UAN above):**
- Complaint Centre (Head Office): 021-99230317
- Customer Services Centre, 9th Mile Karsaz: 9th Mile Consumer Services Centre, Karsaz, Karachi | 021-99245138 / 021-99245140

**Water tanker booking — numbers and pricing:**
- Booking window: call between **5:00 AM and 9:00 PM**
- Online Tankers Centre: 021-99245152, 021-99245178, 021-99240802
- **Pricing is volatile and actively under revision — do not hardcode a static price table in the product.** As of the most recent confirmed reporting (July 2026), KWSC's own Hydrants Cell quoted these official rates, which sit noticeably lower than many tanker operators actually charge in practice:

| Tanker size | General Public Supply (GPS) rate | Commercial rate |
|---|---|---|
| 1,000 gallons (~3,785 L) | Rs. 1,560 | Rs. 3,120 |
| 2,000 gallons (~7,570 L) | Rs. 2,184 | — |
| 3,000 gallons (~11,355 L) | Rs. 2,808 | — |
| 5,000 gallons (~18,927 L) | Rs. 3,900 | — |

- Additional transportation charges apply for delivery beyond a 10 km radius from the hydrant.
- **Context your app should surface to users:** KWSC formed a committee in mid-2026 specifically to raise these tariffs, citing rising diesel costs and operators refusing to supply at the existing rate — so a further increase is expected and the numbers above should be treated as a snapshot, not a fixed reference price. Independent reporting also notes many residents already pay well above the officially notified rate, and private (non-official) hydrants can charge roughly double the government rate for the same volume.
- **Product implication:** for the "tanker price transparency" feature, pull live rates via periodic re-verification (news search or KWSC's own notices) rather than embedding the table above as ground truth, and consider showing both the "official/subsidized" rate and a "typical market rate" range so users know what a fair price looks like even when official rates lag behind real costs.

**How to file a complaint:**
- **Accepts online complaints:** Yes — this is the most complete, verifiable form of the three online-capable authorities
- **Channels:** Dedicated portal **complain.kwsc.gos.pk** → "Add Complaint" form directly at **https://complain.kwsc.gos.pk/add/complaint**, available in English/Urdu, with complaint tracking; mobile app **"KWSC CPS"** (Consumer Portal Service, Android); phone helpline **1334**; UAN 021-111-597-200; WhatsApp 0319-2046357 (legacy KWSB number, still referenced)

**Full form fields (verified directly from the live form):**
| Field | Required? | Notes |
|---|---|---|
| Consumer # on BILL | Optional | Only if the complaint is tied to an existing account |
| Applicant Name | **Required** | |
| Applicant Phone Number | **Required** | |
| Applicant Email | Optional | |
| Select Town | **Required** | Dropdown of ~28 KWSC-defined towns (e.g. Baldia, Clifton, Gulshan-e-Iqbal, Korangi, Landhi, Lyari, Malir, Nazimabad, North Nazimabad, Orangi, Saddar, SITE, Sohrab Goth, etc. — a KWSC-specific town list, not identical to the DMC/district boundaries) |
| Select UC / Mohalla | **Required** | Dependent dropdown, populated after Town is selected |
| Applicant Person Address | Optional | |
| Applicant Person Nearest Land Mark | **Required** | |
| Select Complaint Type | **Required** | Dropdown: Billing, Bulk Supply Water, CMC, Environmental/Social Complaints, Hydrant Complaint, New Connection Commercial, Other, Request for Information, Sewerage Complaints, Water Complaints |
| Select Grievance | **Required** | A sub-category dropdown, dependent on Complaint Type selected |
| Description | **Required** | Free text, **350-character limit** — your generator needs to compress/summarize the complaint to fit this |
| Picture | Optional | Single image upload field |

- New connections use a separate form at **complain.kwsc.gos.pk/add/new/connection**, requiring property address and ownership/tenancy details.
- **Design implication:** the 350-character cap on Description is a hard constraint — your complaint-generation prompt should produce a tight, front-loaded summary (what/where/since-when) rather than a full narrative, and rely on the Town/UC/Landmark/Complaint-Type/Grievance dropdowns to carry most of the structured detail.

---

## 3. Sindh Solid Waste Management Board (SSWMB)

**Website:** sswmb.gos.pk | Billing portal: billing.sswmb.gos.pk/portal
**Legal basis:** Sindh Solid Waste Management Board Act, 2014 (amended 2021 for divisional boards)
**HQ:** 3rd Floor, DMC South Building, near Aram Bagh Police Station, Karachi | 021-99333710-03

**Responsible for:**
- Municipal, industrial, agricultural, and medical solid waste collection & disposal
- Street sweeping, garbage point clearance, landfill operations
- Contracting/oversight of private waste collection companies (e.g. area-wise Chinese JV contractors) — residents complain to SSWMB even though a contractor does the physical collection

**Not responsible for:** sewage (KWSC), storm drains (KMC), industrial effluent regulation (Sindh EPA).

**How to file a complaint:**
- **Accepts online complaints:** Yes, but the website form is minimal — the mobile app and phone/WhatsApp lines carry the real complaint detail
- **Channels:** Mobile app **"SSWMB Complain"** (Android/iOS); Contact Us page: **https://sswmb.gos.pk/contact-us/**; phone **021-99333702**; WhatsApp **+92-318-1030851**; dedicated Complaint Cell (launched 2025) for in-person/phone escalation.

**Contact-us page form (verified directly from the live page):**
- Fields: **Name, Email, Message** — a generic 3-field contact form, not a structured complaint intake (no category dropdown, no area/UC selector, no photo upload). Treat this as a fallback/general-inquiry channel, not the primary complaint route.
- Also listed on the same page: office address (3rd Floor, DMC South Building, opposite Aram Bagh Police Station, Karachi-74200), phone 021-99333710-03, fax 021-99333700, email info@sswmb.gos.pk, and a **district area-wise SSWMB officer contact sheet** (published as an image) covering East, West, South, Central, Korangi, Malir, Keamari — useful for routing a complaint to a named officer if the app/phone lines are unresponsive.
- The **mobile app** is the channel that actually structures a complaint (category, location, photo) — direct citizens there over the website form whenever possible.

**Info required (app/phone):** Name and phone number; area/district (each has a separate SSWMB contact officer); nature of complaint (uncollected garbage, missed collection schedule, overflowing bin/dumpster, contractor non-performance). A photo is strongly recommended since collection-point disputes are visually verified.

---

## 4. Sindh Building Control Authority (SBCA)

**Website:** sbca.gos.pk
**Legal basis:** Sindh Building Control Ordinance, 1979; Karachi Building & Town Planning Regulations, 2002
**HQ:** Civic Centre Annexe, University Road, Gulshan-e-Iqbal, Karachi

**Responsible for:**
- Building plan approval & NOCs
- Illegal/unauthorized construction, building-plan violations
- Structural safety, declaring/demolishing dangerous buildings
- Disputes between allottees and builders/developers on approved projects
- Enforcement under Sindh High Court directives (Special Courts under Section 18-A of the Ordinance)

**Not responsible for:** footpath/road encroachment by vendors or land grabbing (KMC/DMC/police), water or sewerage inside a building (KWSC), land title disputes (Board of Revenue/Mukhtiarkar).

**How to file a complaint:**
- **Accepts online complaints:** Yes — the most formalized of all the bodies (SCRM — Smart Complaint Redressal Mechanism)
- **Channels:** Website sbca.gos.pk; mobile app **"SBCA Smart"** (Android & iOS) — supports photo upload, GPS location tagging, complaint tracking, QR-code building lookup; UAN **111-007-222**; walk-in Complaint Centers at SBCA offices
- **Info required:** Registration via phone number and email (OTP-verified); property/construction address (mandatory); complaint type dropdown (illegal/unauthorized construction, building-plan violation, builder-allottee dispute, private-public cell/open-plot scheme violation); photo(s) of the site (app explicitly supports this); GPS location (auto-captured on-site). CNIC is **not** currently mandatory — SBCA removed it from registration in a recent app update, which lowers friction for reporting.
- **Documented process timeline:** registration (1 day) → verification (3 days) → notice under Sec. 7-A if violation confirmed (7 days) → hearing (7 days) → decision (14 days) → appeal window (30 days, Sec. 16) → implementation (4–8 weeks).

---

## 5. District Municipal Corporations / Towns (post-2013/2021 restructuring)

Karachi is split into 7 districts (East, West, South, Central, Korangi, Malir, Keamari), each historically under a DMC, now further divided into ~26 town municipal committees under the 2021 Act.

| District | Known site | Notes |
|---|---|---|
| DMC Korangi | dmckorangi.gos.pk | Confirmed live |
| DMC East/West/South/Central/Malir/Keamari | inconsistent — many lack a stable public portal | Route via KMC's district office directory or **CLICK** aggregator (click.gos.pk) as fallback |

**Responsible for (district/town level):** local health facilities, some parks/community halls, tree planting on local streets, minor local infrastructure — functions delegated down from KMC.

**Useful aggregator:** CLICK — Competitive & Livable City of Karachi (click.gos.pk) — indexes KMC, KWSC, SSWMB, KDA, Sindh govt, and lists union councils by DMC (click.gos.pk/karachiuc); also has its own generic complaint form at click.gos.pk/complain. Good as a lookup table, not a primary complaint channel.

**How to file a complaint:**
- **Accepts online complaints:** Inconsistent — treat as a fallback, not primary
- **Channels:** Where a DMC has a working site, it typically links back to KMC's 1339/CCIS system rather than running independent intake. Commissioner Karachi's site (commissionerkarachi.gos.pk/municipal-services) also has a "Complaint" tab that may route municipal-service complaints across districts.
- **Info required:** Same pattern as KMC — name, contact, location/UC, category, description — since most DMC-level complaints ultimately feed the same civic complaint pipeline. In practice, most citizen-facing complaint volume still routes through KMC's central 1339 line, so treat DMC portals as secondary in your routing logic.

---

## 6. Cantonment Boards (federal jurisdiction — NOT under KMC/Sindh LG Act)

Six cantonments run their own municipal services independently:

| Cantonment | Website | Covers |
|---|---|---|
| Cantonment Board Clifton (CBC) | cbc.gov.pk / clifton.cantonment.gov.pk | DHA phases + Blocks 8–9 Clifton |
| Cantonment Board Faisal | cbfaisal.gov.pk / faisal.cantonment.gov.pk | PAF Base area, Drigh Road |
| Karachi Cantonment Board | cbkarachi.gov.pk | Saddar / core cantt area |
| Cantonment Board Malir | cbmalir.gov.pk | Malir Cantt |
| Korangi Creek Cantonment | (no confirmed stable public site found) | Korangi Creek |
| Manora Cantonment | (no confirmed stable public site found) | Manora Island |

**Legal basis:** Cantonment Act, 1924 (federal) — administered via Military Lands & Cantonments (ML&C), Ministry of Defence, not the Sindh Local Government Department.

**Responsible for:** roads, water, sewerage, waste collection, building control — all municipal functions — *within their boundaries only*.

**How to file a complaint:**
- **Accepts online complaints:** Largely **no** — this is the weak link across the whole system
- **Channels:** Cantonment Board Clifton and Faisal have official sites, but complaint intake is generally by phone/in-person to the CEO's office or the relevant Executive Officer, not a structured web form. Korangi Creek and Manora cantonments have no confirmed public complaint channel at all.
- **Info required (typical for phone/in-person cantonment complaints):** Name, CNIC, contact number, house/plot number; nature of complaint and exact location within the cantonment; often a written application (even just an email or printed form) rather than a ticketed system.
- **Design implication:** if a report is geolocated inside a cantonment boundary, don't promise "submit online" — generate a formatted written complaint (letter format) addressed to the specific cantonment's CEO/Executive Officer, with a phone number as fallback delivery, and flag that in-person follow-up may be needed.

---

## 7. Umbrella / policy-source departments (not complaint channels, but where policies/acts live)

- **Local Government Department, Sindh (LGD)** — lgdsindh.gov.pk — parent department overseeing KMC, DMCs, KWSC, SSWMB; hosts acts, notifications, rules
- **Sindh Building Control Ordinance, 1979** — full text via SBCA/LGD
- **Sindh Solid Waste Management Board Act, 2014** — sswmb.gos.pk/sswm-act-and-agreements
- **Sindh Local Government Act, 2013 / Sindh People's Local Government Act, 2021** — via LGD
- **Cantonment Act, 1924** — federal, via ML&C

---

## Quick routing table for your classifier

| Issue type | Primary authority | Fallback if in cantonment |
|---|---|---|
| Burst water pipe / no water supply | KWSC (1334 / e-complaint) | Relevant cantonment board |
| Sewage overflow / choked sewer | KWSC | Cantonment board |
| Uncollected garbage | SSWMB | Cantonment board |
| Storm drain blocked/overflowing (not sewage) | KMC | Cantonment board |
| Streetlight out / pothole / road damage | KMC (1339) / DMC | Cantonment board |
| Illegal construction / dangerous building | SBCA (SCRM, UAN 111-007-222) | Cantonment board's building branch |
| Footpath/road encroachment (vendors, structures) | KMC Anti-Encroachment Dept, else DMC or police | Cantonment board |
| Park/playground maintenance | KMC / DMC | Cantonment board |
| Birth/death certificate | KMC (NADRA-linked) | — |

---

## Summary — complaint channels at a glance

| Authority | Online complaint? | Best channel | Key required info | Form verified? |
|---|---|---|---|---|
| KMC | Yes (but see caveat) | 1339 phone, or complaint.kmc.gos.pk/ccis | Name, phone, CNIC, UC/town, category, description | CCIS blocks inspection; contact-us page is placeholder/broken |
| KWSC | Yes — most reliable | complain.kwsc.gos.pk/add/complaint or 1334 | Name*, phone*, town*, UC/mohalla*, landmark*, complaint type*, grievance*, description* (350 char), consumer#/email/address/photo optional | **Fully verified**, full field list captured above |
| SSWMB | Partially — app is real, website form is thin | "SSWMB Complain" app or 021-99333702 | App: name, phone, area/district, issue type, photo. Website: only name/email/message | Website form verified (minimal); app fields not independently inspectable |
| SBCA | Yes (most structured process) | "SBCA Smart" app, sbca.gos.pk, or 111-007-222 | Phone/email (OTP), property address, complaint type, photo, GPS | Verified via app-store listing + SBCA's own published SOP, not the live form itself |
| DMC/Town | Inconsistent | Falls back to KMC 1339/CCIS | Same as KMC | Not independently verified |
| Cantonment Boards | Mostly no | Phone/in-person to CEO/EO office | Name, CNIC, contact, plot no., location, written application | No online form exists to verify |

**Design notes for the product:**
1. The biggest reliability risk isn't classification, it's assuming every authority has a working digital complaint channel — several DMC, cantonment, and even KMC's own "contact us" page don't. Build a confidence flag into your routing output ("verified structured form" / "app-only" / "phone/walk-in only") so the generated complaint defaults to the right format automatically.
2. **KWSC is your most reliable integration** — it's the only one of the six where every field, dropdown option, and character limit has been directly confirmed from the live form. Build and test your complaint-generation pipeline against KWSC first, then adapt the pattern to the others as their forms get verified or change.
3. **KMC's public-facing "contact us" page is currently non-functional** (dummy placeholder content) — don't build a scraping/auto-fill integration against it; route KMC complaints to the CCIS system or the 1339 phone line instead.
4. SSWMB's website complaint form is a plain name/email/message box, not a structured intake — treat the mobile app as the real channel and the website as a weak fallback only.
5. SBCA and cantonment boards still need their live forms verified the same way KWSC's was, once their sites/apps allow inspection.
