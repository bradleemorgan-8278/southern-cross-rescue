# Southern Cross German Shepherd Rescue — Website Project

A foster-based German Shepherd rescue site (six pages) plus a GoHighLevel build guide.

## What's in here

```
southern-cross-rescue/
├── index.html            ← the assembled, self-contained prototype (open this in a browser)
├── build.py              ← regenerates index.html from src/ + assets/
├── build-guide.md        ← GHL research, architecture, implementation, security, future phases
├── src/                  ← EDIT THESE, then re-run build.py
│   ├── css.txt           ← the full design system (brand tokens, layout, animations)
│   ├── icons.html        ← inline SVG line-icon sprite
│   ├── page_home.html    ← nav + mobile drawer + Home page
│   ├── page_about.html   ← About
│   ├── page_foster.html  ← Foster (+ Foster Application form placeholder)
│   ├── page_adopt.html   ← Adopt (+ 7-step accordion, Adoption form, dogs grid)
│   ├── pages_edu_donate.html ← Education + Donate (+ Stripe/Payment placeholder)
│   └── footer.html       ← footer + all page JavaScript
└── assets/
    ├── logo-navy.png     ← emblem for light/cream backgrounds
    ├── logo-cream.png    ← emblem for navy/black backgrounds
    └── Logo-original.svg ← the original supplied file (raster JPEG inside an SVG)
```

## How to work on it

The single `index.html` has the logos embedded as base64, which makes it large and awkward to hand-edit. Don't edit `index.html` directly. Instead:

1. Edit the relevant file in `src/` (or the design system in `src/css.txt`).
2. From the project root, run:
   ```bash
   python3 build.py
   ```
3. Open `index.html` in a browser to preview.

`build.py` needs only Python 3 (standard library, no packages).

## Notes carried over from the build

- **Brand palette:** Navy `#1B2A4A`, Gold `#C49A2C`, Highlight Gold `#D4AA3C`, Warm Cream `#F5F2EC`, Secondary Navy `#2C3E5E`, GSD Black `#1C1814`, GSD Tan `#B8864E`.
- **Fonts:** Cinzel (display), EB Garamond (body + italic pull quotes), Raleway (UI/labels/buttons).
- **Logo caveat:** `Logo-original.svg` is a raster JPEG wrapped in an SVG, not true vector. The navy/cream PNGs were made by knocking out the white background and swapping the single ink color so the emblem reads on dark sections. For gold placement at any size, get a real vector (`.ai`/`.eps`/path-based `.svg`) and a one-color gold version from the designer. See `build-guide.md`, Part 3.
- **Form/payment areas** are styled placeholders. `build-guide.md` Part 4 explains exactly which GoHighLevel native Form and Payment elements drop into each, with field lists.
- **Phase 2 hooks:** the Impact section has hidden counter scaffolding (`data-count`) ready for live numbers. See `build-guide.md`, Part 6.

## Suggested next steps in Claude Code

- Split `index.html` into six standalone files for GoHighLevel's Custom HTML Pages upload.
- Wire the Donate page to a real Stripe test flow and a tax-receipt workflow.
- Add the dedicated Volunteer page noted in the guide.
