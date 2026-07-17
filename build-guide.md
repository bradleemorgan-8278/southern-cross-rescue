# Southern Cross German Shepherd Rescue
## Website Design + GoHighLevel Build Guide

Prepared as the companion document to the single-file prototype `southern-cross-rescue-prototype.html`.
This guide is organized in six parts: (1) GoHighLevel research summary, (2) site architecture map, (3) prototype overview and the one logo decision you need to sign off on, (4) the page-by-page GoHighLevel implementation guide, (5) the platform security checklist, and (6) future-phase integration notes.

All research below was verified against current GoHighLevel documentation and reporting in June 2026. Where something is likely to drift, I have said so and linked the source so it can be re-checked before you build.

---

## Part 1 — GoHighLevel Research Summary (current June 2026)

### 1.1 How the builder is actually structured
GoHighLevel ("GHL") gives you two page products that share the same drag-and-drop engine: **Funnels** (linear, step-based, the only product that supports split testing) and **Websites/Sites** (multi-page, the right choice for an authority site like this one). The editor nests content as **Sections > Rows > Columns**, and every element has separate desktop, tablet, and mobile property panels, so you can hide elements per device, change font sizes per breakpoint, and reorder column stacking on mobile.

Three places let you push past the stock builder:
- **Custom CSS tab** (site/funnel Settings) for site-wide styling.
- **Tracking Code** (header/footer) for site-wide JavaScript.
- **Code / Embed element** dropped into any section for inline HTML, CSS, or JS.

One important limit to design around: **global styles are per-funnel, not account-wide.** Brand colors and fonts set as "global" apply to that one site, so keep the whole public site inside a single Website project to avoid re-keying the palette.

### 1.2 The single most useful finding for this project: Custom HTML Pages
GHL shipped a **Custom HTML Pages** feature for HighLevel-hosted WordPress sites. You upload a single `.html` file (up to **5 MB**) and publish it as a live page on your mapped domain, using your existing HighLevel SSL and domain setup. The catch worth planning for: **one page per upload**, and any images, CSS, or JS must be referenced by **absolute URLs** (relative paths and multi-folder uploads are not supported).

Why this matters: the prototype I built is a hand-coded, fully designed file. The Custom HTML Pages route lets that design go live almost exactly as drawn, instead of being rebuilt block by block in the visual editor. The trade-off is that those pages then live "outside" the drag-and-drop editor, so non-technical edits are harder. This produces the two build paths described in Part 4.
Source: https://help.gohighlevel.com/support/solutions/articles/155000006571-wordpress-custom-html-pages

### 1.3 What GHL does well here
- **All-in-one for a nonprofit.** One platform covers donor CRM, donation forms, email and SMS, pipelines, calendars, and automations, which replaces a stack of separate tools.
- **Recurring donations through Stripe**, at any frequency, with automated thank-you and tax-receipt workflows.
- **Volunteer coordination** through calendars (shift booking with capacity limits), pipelines (a dedicated volunteer stage), and automated onboarding, reminders, and follow-up.
- **Hosting** on Google Cloud with a CDN and automatic WebP image conversion.
- **SEO**: per-page meta controls plus automatically generated JSON-LD schema for local business and FAQ content.

### 1.4 Constraints and the workarounds we will use
| Constraint | Practical effect | Workaround in this build |
|---|---|---|
| Limited native animation | No built-in scroll reveals, counters, accordions | Ship them via the prototype's own CSS/JS (Path A), or recreate the key ones with a Code Block (Path B) |
| Page speed on heavy native pages | Runtime rendering can score ~25-45 on mobile PageSpeed | Keep sections lean, lazy-load images, prefer the static HTML page route for the homepage |
| Editor sluggish on very long pages | 50+ sections feels slow to edit | Split long pages, or use the static HTML route |
| "Every GHL site looks like a GHL site" | Template fingerprint | The custom design system and fonts in this build remove that fingerprint |
| Forms embed code is an iframe | Iframe embeds lose URL parameters and add load time | On GHL-hosted pages, use the **native Form element**, not the iframe embed |

Sources: https://www.gohighlevel.ai/blog/gohighlevel-landing-page-builder and https://www.pandacodegen.com/blog/best-website-builder-for-gohighlevel-agencies

### 1.5 Fonts
GHL now supports **native custom-font upload** (an Agency Settings > Labs feature) accepting `.ttf`, `.otf`, `.woff`, and `.woff2`, selectable per text element under Typography. You can also use Google Fonts. The three brand faces, **Cinzel**, **EB Garamond**, and **Raleway**, are all on Google Fonts. The native font picker does not always list every Google Font, so the most reliable method is to load them yourself with a CSS `@import` in the Custom CSS tab (snippet in Part 4). 
Sources: https://help.gohighlevel.com/support/solutions/articles/155000005918-using-custom-font-in-funnels-and-websites

### 1.6 Forms
GHL forms can be added two ways. On a GHL-hosted page, use the **native Form element** (drag it in, style inherits your page theme). The **embed** option is an iframe; it works on non-GHL sites but loses URL parameters, so reserve it for that case. Forms support layouts (inline, popup, slide-in, sticky sidebar), and you can listen for the `formSubmitted` PostMessage event if you ever embed via iframe and need conversion tracking.
Source: https://help.gohighlevel.com/support/solutions/articles/155000004538-how-to-use-embedding-options-for-forms-triggers-layouts-and-deactivation-settings-explained

### 1.7 Payments and donations
The **Payment element** lives inside the form builder (Add Element > Integrations) and is built for donations: up to **15 suggested amounts** plus an **"Other Amount"** option, in your chosen currency, as **one-time, subscription, or donation** types. Requirements and limits to know:
- A gateway must be connected first. **Stripe** is the standard; Authorize.net and NMI are also supported (those two require First Name as mandatory).
- You must create **Products and Price Points** under Payments before the amounts will map correctly.
- **Refunds are not supported inside the form** (handle in Stripe).
- The **old API-based Stripe Connect method is no longer supported**; connect Stripe through the current integration.
Sources: https://help.gohighlevel.com/support/solutions/articles/155000001884-payment-in-forms-including-donations- and https://consultevo.com/gohighlevel-payment-in-forms/

### 1.8 Portals (for the future donor/volunteer/foster areas)
GHL's **Client Portal** is a branded, login-protected hub on `clientclub.net` or a custom subdomain (for example `portal.yourdomain.org`). It combines **Memberships/Courses**, **Communities**, custom dashboards that merge each user's own data, and embedded iFrames/forms. This is the foundation for gated Donor, Volunteer, and Foster portals later (Part 6).
Sources: https://help.gohighlevel.com/support/solutions/articles/155000000193-how-to-set-up-the-client-portal- and https://help.gohighlevel.com/support/solutions/articles/155000000280-how-to-setup-customize-and-manage-your-communities

### 1.9 Security and nonprofit posture (summary; full checklist in Part 5)
GoHighLevel holds **SOC 2 Type II** (reported February 2026) and **ISO 27001**, with data encrypted in transit over **TLS 1.2/1.3**. Card data is handled by Stripe (PCI scope stays with Stripe). The clear guidance for nonprofits: **do not store full SSNs or government ID numbers in contact fields.**
Source: https://netpartners.marketing/how-nonprofits-use-gohighlevel-crm-to-streamline-donations-engage-supporters-and-automate-operations/

---

## Part 2 — Site Architecture Map

### 2.1 Global elements (present on every page)
- **Top gold accent stripe** (4px gradient bar pinned to the very top of the viewport). Non-negotiable brand element.
- **Sticky navigation**: logo + wordmark on the left; Home / About / Foster / Adopt / Education / Donate; a gold Donate button on the right. Frosts (navy, blurred) on scroll. Collapses to a hamburger that opens a full-screen slide-in drawer on mobile.
- **Footer**: emblem + mission statement, an Explore column (all six pages), a Connect column (email, phone, mailing address placeholders, social icons), and a legal bar (501(c)(3) line, EIN placeholder, copyright).

### 2.2 The six pages and their sections
1. **Home** — Hero (headline, sub, CTAs: Foster / Adopt / Donate / Volunteer, plus the emblem) > Our Mission ("More Than Rescue") > mission pull quote > Why Fostering Matters (two-column, dark) > Impact ("Every Rescue Creates a New Beginning", GSD-black, gold headline, six receive-items, hidden metrics scaffold for Phase 2) > Featured Story: Trooper (before/after).
2. **About** — Page intro > "About Southern Cross" intro > Our Story (Adrienne Sharp, Founding Steward / Director Emeritus) > What We Believe (six commitment cards).
3. **Foster** — Page intro > why a foster home matters > What Southern Cross Provides (checklist) > What Foster Families Provide (six cards) > "You May Already Be Exactly What a Dog Needs" > closing + **Foster Application form**.
4. **Adopt** — Page intro > adoption philosophy > Adoption Process (interactive 7-step accordion) > **Adoption Application form** > Currently Available Dogs (dynamic grid, CRM-fed).
5. **Education** — Page intro > why education matters > Topics We Care About (nine-item grid) > Backyard Breeding advocacy.
6. **Donate** — Page intro > the case for giving + "every gift provides" list > **donation form (Stripe/Payment element)** with suggested amounts and frequency > Many Ways to Make a Difference > **The Shepherd's Circle** (monthly giving feature) > other ways to help grid.

### 2.3 Navigation and CTA routing
Every CTA in the prototype is wired: Foster buttons route to Foster, Adopt to Adopt, Donate and "Join The Shepherd's Circle" to Donate, "Read More Success Stories" to Adopt. **One thing to decide:** the brief defines six pages with no dedicated Volunteer page, but the hero has a Volunteer button and volunteering appears under "ways to help" on Donate. For now the Volunteer button routes to the Donate page's involvement section. A dedicated Volunteer page with its own signup form is recommended as an early addition (see Part 6).

---

## Part 3 — Prototype Overview and the Logo Decision

### 3.1 What the prototype is
`southern-cross-rescue-prototype.html` is one self-contained file: all six pages, embedded CSS, the brand fonts loaded from Google Fonts, the logo embedded as image data, and a small amount of JavaScript for the page navigation, scroll reveals, the adoption accordion, the donate amount selector, and the Phase-2 counter scaffolding. It uses client-side page switching so you can click through all six "pages" in one file. Open it in any modern browser. It is responsive to mobile and respects reduced-motion preferences.

Every word of the supplied copy is included verbatim. Form areas are shown as clearly labeled, on-brand placeholders ("GHL Form Embed", "Stripe / GHL Payment") so it is obvious where the live GHL elements drop in. The Available Dogs grid and the impact metrics are placeholders intended to be fed from the CRM.

### 3.2 The one logo decision to sign off on
The supplied `Logo.svg` is not a vector file. It is a single 1250x1250 **raster (JPEG) image wrapped inside an SVG container**, black artwork on a white background. That has one real consequence: a flat black raster cannot be cleanly recolored to gold, and it cannot sit on the navy or black sections as-is without a white box around it.

To honor the brand rule that the emblem appears in the navigation and footer, and to keep it crisp on dark backgrounds, I did the following and am flagging it for your approval:
- I removed the white background to make the emblem transparent, and produced two clean variants: a **navy** emblem for light/cream areas and a **cream** emblem for navy/black areas. The artwork itself is unchanged in shape and proportion; only the background was knocked out and the single ink color swapped so it reads on dark. The emblem is never stretched or distorted.
- For the small gold paw accents in the UI (pull quotes, the Shepherd's Circle, section marks), I used a **separate simple vector paw mark**, not a recolored version of your logo, so nothing alters the official emblem.

**Recommended next step:** ask your designer for the original vector (the true `.ai`, `.eps`, or a genuine path-based `.svg`) and, ideally, a one-color gold version. With a real vector we can place a gold emblem anywhere at any size with no quality loss, and retire the workaround above.

---

## Part 4 — GoHighLevel Implementation Guide

You have two viable paths. Read 4.1 to choose, then do the global setup in 4.2, then follow the page notes in 4.3.

### 4.1 Choose your build path
- **Path A — Static HTML pages (fastest, closest to the prototype).** Split the prototype into six standalone `.html` files (one per page), host the images and any shared CSS/JS at absolute URLs (GHL Media Library or a CDN), and upload each via **Custom HTML Pages**. Pros: the design ships pixel-accurate, animations included; fast pages. Cons: edits happen in code, not the visual editor; one upload per page.
- **Path B — Native rebuild in the Site Builder.** Recreate each page with Sections/Rows/Columns, native Forms, and the Payment element, pasting the prototype's section styling into Custom CSS and using Code Blocks for the three interactive moments (scroll reveals, the adoption accordion, the impact counters). Pros: staff can edit visually; native forms and payments are first-class. Cons: more setup time; you will re-implement the look carefully.

A sensible hybrid many orgs use: build **Donate, Foster, and Adopt natively** (so forms and payments are native and editable), and ship **Home, About, and Education as static HTML** (where the design carries the most weight and content changes least).

### 4.2 Global setup (do this once, before any page)

**Brand color tokens (exact hex):**
| Token | Hex | Use |
|---|---|---|
| Navy | `#1B2A4A` | Primary brand, nav, dark sections |
| Gold | `#C49A2C` | Primary accent, dividers, buttons |
| Highlight Gold | `#D4AA3C` | Hover, headlines on dark, emphasis |
| White | `#FFFFFF` | Text on dark only |
| Warm Cream | `#F5F2EC` | Default light section background (never pure white) |
| Secondary Navy | `#2C3E5E` | Secondary dark panels |
| GSD Black | `#1C1814` | Highest-contrast "markings" sections (Impact, advocacy) |
| GSD Tan/Sable | `#B8864E` | 8-12% washes and small accents only |

**Fonts.** In Site Settings > Custom CSS, paste this import and base mapping, then in Typography set Headlines = Cinzel, Body = EB Garamond:
```css
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=EB+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Raleway:wght@400;500;600;700&display=swap');
h1,h2,h3,h4{font-family:'Cinzel',serif;letter-spacing:.09em}
body,p,li{font-family:'EB Garamond',serif;line-height:1.75}
.label,.btn,.eyebrow,nav a{font-family:'Raleway',sans-serif}
```
Font roles: **Cinzel** for display/headlines/wordmark (wide letter-spacing, used in caps); **EB Garamond** for body and the italic pull quotes; **Raleway** for UI only (nav, labels, buttons).

**Accent stripe.** Add this once in the footer Tracking Code so it appears site-wide:
```html
<div style="position:fixed;top:0;left:0;right:0;height:4px;z-index:9999;
background:linear-gradient(90deg,#C49A2C,#D4AA3C,#C49A2C)"></div>
```

**Logo.** Upload the navy and cream emblem variants to the Media Library; use the cream emblem in the (navy) nav and footer, the navy emblem on any cream area.

**Navigation + footer.** Build these as a global header and global footer so they appear on every page. Mirror the routing in Part 2.

### 4.3 Page-by-page notes
For each page: set the **SEO** fields (Pages > page > Settings): a unique title and meta description, an Open Graph share image, and a clean URL slug (`/`, `/about`, `/foster`, `/adopt`, `/education`, `/donate`). Check the **mobile** panel on every section (stack columns, reduce display type, confirm the hamburger). Enable lazy-loading on images.

**Home.** Hero is a full-viewport navy section; if native, set a background image with a 20-30% navy overlay and place the cream emblem in the right column. The Impact section background is GSD Black `#1C1814` with the **headline in gold** `#D4AA3C` and cream body. The Impact metrics are intentionally hidden until Phase 2; leave the counter markup in place. Trooper uses a navy-to-black gradient with before/after image slots (recommended 900x640).

**About.** Mostly type and cards. Render the six "What We Believe" items as a three-column card grid. The Our Story section uses the large faint "STORY" ghost label behind the headline (a Code Block or a positioned text element if native).

**Foster.** Two forms-free content sections plus the **Foster Application form** at the bottom. Build the form natively with fields: First name, Last name, Email, Phone, Address/City/State, Home type (own/rent), Landlord approval (if renting), Yard (fenced/no), Other pets, Prior GSD experience, Hours dog alone/day, Why foster, How heard about us. On submit: add a "Foster Applicant" tag and drop the contact into a Foster pipeline stage, then trigger a confirmation email.

**Adopt.** The **7-step adoption process** is the one interactive element here. Natively, use a Code Block with a simple accordion (the markup and script are already in the prototype, copy them). Build the **Adoption Application form** (fields: applicant details, household size, children ages, other pets, home/yard, fencing, activity level, dog-of-interest, references, vet reference). On submit: tag "Adoption Applicant", create an opportunity in an Adoption pipeline, notify the team. The **Currently Available Dogs** grid should be CRM-driven: maintain dogs as records (a custom object or a dedicated pipeline) and render cards from that list so volunteers update availability in one place.

**Education.** Static content; the Topics grid is a simple icon + label grid. Good candidate for Path A (static HTML) since it rarely changes.

**Donate.** This is the priority native build.
1. In **Payments**, connect **Stripe**, then create a "Donation" Product with Price Points for $25, $50, $100, $250, and a user-defined amount; add a monthly Price Point for The Shepherd's Circle.
2. Build a **Form** with the **Payment element** (Add Element > Integrations): enable donation type, add the suggested amounts, enable "Other Amount", and offer a one-time vs monthly choice.
3. Keep donor fields minimal (Name, Email, optional Phone) to protect conversion.
4. Build a **workflow** triggered on successful payment that sends a branded **tax-receipt email** (donor name, amount, date, your 501(c)(3) and EIN language) and tags monthly donors as "Shepherd's Circle".
5. Remember refunds happen in Stripe, not the form.

---

## Part 5 — Platform Security Configuration Checklist

**Account and access**
- Turn on **two-factor authentication** for every staff and volunteer login.
- Use **role-based permissions**; give volunteers the minimum access they need, and remove access promptly when someone leaves.
- Keep the public site, forms, and CRM in a single sub-account with a clear owner.

**Data handling (important for a rescue)**
- **Never store full SSNs or government ID numbers** in contact fields.
- Collect only what you use. For adopters and fosters, that means contact details, home/household info, and references, not sensitive financial identifiers.
- Let **Stripe** handle all card data so PCI scope stays with Stripe; do not capture raw card numbers in any GHL form or note.
- Store vet and landlord references as text, not uploaded government documents.

**Forms and spam**
- Enable form spam protection / reCAPTCHA on public forms.
- Use double opt-in for email where appropriate, and include a clear unsubscribe in marketing emails.

**Domain, transport, and email**
- Confirm SSL is active on the mapped domain (HighLevel provisions this).
- Verify data is served over **TLS 1.2/1.3** (GHL default).
- Set up **SPF, DKIM, and DMARC** for your sending domain so receipts and updates land in inboxes and cannot be easily spoofed.

**Payments and receipts**
- Connect Stripe with a dedicated organization account; restrict who can issue refunds.
- Test the donation flow with Stripe test mode before going live; confirm the contact, the transaction, and the receipt email all fire.

**Governance**
- GHL's platform certifications (SOC 2 Type II, ISO 27001) cover the platform, not your configuration. Keep a short internal data-handling policy and review access quarterly.
- Keep a record of consent for SMS/email outreach.

---

## Part 6 — Future-Phase Integration Notes

### Phase 2 — Live impact metrics
The Impact section already contains hidden, animated counters (`data-count` markup and the JavaScript that drives them). When you have verified numbers (dogs rescued, foster placements, adoptions, medical cases funded), unhide the metrics block and either hard-set the numbers or feed them from a CRM value. The count-up animation runs on scroll and respects reduced-motion. No redesign needed.

### Phase 3 — Statistics dashboard
Grow the single metrics row into a fuller impact page: year-over-year adoptions, a simple map or list of placements, medical-fund progress, and foster-home growth. Build it as a native page with Code Blocks for charts, or feed a lightweight static HTML page from CRM exports. Keep the visual language identical (gold-on-black numerals, Cinzel labels) so it reads as part of the same site.

### Donor, Volunteer, and Foster portals
Use the **Client Portal** (on a `portal.yourdomain.org` subdomain) as the shell, with **Memberships/Communities** for content and discussion and **custom dashboards** that merge each user's own records:
- **Donor portal:** giving history, recurring-gift management, downloadable receipts and year-end summaries, sponsorship updates.
- **Volunteer portal:** shift calendar and sign-ups (GHL calendars with capacity limits), onboarding course (Memberships), a private community channel, and task pipelines.
- **Foster portal:** the foster's current dog(s), care guidelines and documents, a direct line to the coordinator, and quick update forms.
Each can start simple (a branded dashboard plus a calendar and a form) and grow.

### Dedicated Volunteer page and form
Add a seventh public page, **Volunteer**, with its own hero, the ways volunteers help, and a native signup form (interests, availability, skills, transportation, background-check consent). Re-point the hero's Volunteer button to it. On submit: tag "Volunteer", route into a Volunteer pipeline, and start an onboarding sequence.

### AI and automation workflows
- **Conversation AI** to answer inbound questions 24/7 (adoption process, donation options, event details, volunteer signup) and route real leads to a person.
- **Automated lifecycles:** thank-you and tax-receipt on every gift, lapsed-donor re-engagement, foster-application status updates, adoption-pipeline reminders, post-adoption check-ins, and volunteer shift reminders.
- **Giving Tuesday / year-end campaigns** with timed SMS + email sequences.
- **Year-end giving summaries** auto-generated on December 31 for everyone who gave during the year.

---

### Source references (re-verify before building, since GHL ships changes often)
- Custom HTML Pages: https://help.gohighlevel.com/support/solutions/articles/155000006571-wordpress-custom-html-pages
- Sites/Site Builder overview: https://help.gohighlevel.com/support/solutions/articles/155000001633-websites-overview
- Custom fonts: https://help.gohighlevel.com/support/solutions/articles/155000005918-using-custom-font-in-funnels-and-websites
- Form embedding options: https://help.gohighlevel.com/support/solutions/articles/155000004538-how-to-use-embedding-options-for-forms-triggers-layouts-and-deactivation-settings-explained
- Payment in forms / donations: https://help.gohighlevel.com/support/solutions/articles/155000001884-payment-in-forms-including-donations-
- Client Portal: https://help.gohighlevel.com/support/solutions/articles/155000000193-how-to-set-up-the-client-portal-
- Communities: https://help.gohighlevel.com/support/solutions/articles/155000000280-how-to-setup-customize-and-manage-your-communities
- Nonprofit setup + security posture: https://netpartners.marketing/how-nonprofits-use-gohighlevel-crm-to-streamline-donations-engage-supporters-and-automate-operations/
- Builder limitations overview: https://www.gohighlevel.ai/blog/gohighlevel-landing-page-builder
