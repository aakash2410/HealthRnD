---
name: Precision Intelligence
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#45464d'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#515f74'
  on-secondary: '#ffffff'
  secondary-container: '#d5e3fd'
  on-secondary-container: '#57657b'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#07006c'
  on-tertiary-container: '#7073ff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d5e3fd'
  secondary-fixed-dim: '#b9c7e0'
  on-secondary-fixed: '#0d1c2f'
  on-secondary-fixed-variant: '#3a485c'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  title-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
  max-width: 1440px
---

## Brand & Style

This design system embodies the concept of **Precision Intelligence**, a visual language tailored for the rigorous demands of healthcare innovation scouting. It balances the sterile authority of a clinical environment with the advanced analytical power of modern data science. 

The aesthetic is **Corporate Modern with a Data-Centric Lean**. It prioritizes extreme clarity, high information density, and a sense of "Human-in-the-Loop" orchestration. The interface acts as a high-fidelity instrument, utilizing subtle graph-inspired textures—such as micro-grids and connecting nodes—to suggest interconnected insights. Surfaces are organized through a disciplined card-based architecture that manages complexity without overwhelming the user, fostering an atmosphere of total control and absolute trustworthiness.

## Colors

The palette is rooted in **Sophisticated Clinical Blues and Slate Grays**, providing a neutral, calm foundation that allows healthcare data to take center stage. 

- **Primary & Secondary:** Deep slate and charcoal tones provide structural grounding and high-contrast text rendering.
- **Surface Colors:** Crisp whites and very light slate grays (F8FAFC) create a multi-layered "paper" feel, essential for high-density information.
- **Functional Accents:**
    - **Clinical Indigo:** Used for orchestration elements, AI-assisted insights, and primary "Human-in-the-Loop" actions.
    - **Success Green & Warning Amber:** Reserved strictly for status indicators, risk assessments, and data validation states.
    - **Borders:** A consistent use of light gray borders (#E2E8F0) replaces heavy shadows to maintain a clean, laboratory-like precision.

## Typography

The design system utilizes **Inter** as its primary typeface due to its exceptional legibility at small sizes and high-density layouts. 

- **Hierarchical Scale:** Large headlines use tighter letter spacing and heavier weights to command attention. 
- **Data Tables:** Body-md (14px) is the standard for most interface text, providing a balance between density and readability.
- **Labels:** Micro-labels (12px) are frequently used for metadata, using uppercase styling and increased tracking to differentiate them from interactive text.
- **Tabular Data:** For technical values and scout IDs, a secondary monospaced font (JetBrains Mono) is introduced to ensure numerical alignment and a "technical instrument" feel.

## Layout & Spacing

This design system employs a **Fixed-Fluid Hybrid Grid** based on a 4px baseline. 

- **Desktop:** A 12-column grid with a 1440px max-width. Gutters are kept tight (16px) to maximize the "high-density" requirement.
- **Tablet:** 8-column grid with 24px margins.
- **Mobile:** 4-column grid with 16px margins. 

Layouts are primarily **Card-Based**. Complex dashboards are broken into functional "modules" or "widgets" that can be rearranged or expanded. Within these cards, horizontal spacing is prioritized to support tabular data and multi-step orchestration workflows. A "High-Density" toggle is recommended for expert users, reducing internal card padding from 24px to 16px.

## Elevation & Depth

To maintain a "Precision Intelligence" aesthetic, depth is communicated through **Tonal Layering and Low-Contrast Outlines** rather than heavy shadows.

- **Level 0 (Background):** The base canvas uses the neutral slate-tinted white.
- **Level 1 (Cards/Modules):** Pure white surfaces with a 1px solid border (#E2E8F0). This creates a crisp, "cut-out" appearance.
- **Level 2 (Active/Hover):** A very soft, diffused shadow (0px 4px 12px rgba(15, 23, 42, 0.05)) is used only for interactive elements or modals to indicate state change.
- **Orchestration Layers:** Overlays used for AI insights utilize a subtle backdrop blur (glassmorphism) to suggest a separate layer of "intelligence" processing over the raw data.

## Shapes

Shapes follow a **Soft-Precision** logic. 

- **Standard Elements:** Buttons, cards, and input fields use a `0.25rem` (4px) corner radius. This provides a professional, geometric feel that avoids the "playfulness" of rounder shapes while feeling more modern than sharp edges.
- **Data Indicators:** Chips and status tags may use a `rounded-lg` (8px) radius to distinguish them from structural UI elements.
- **Orchestration Nodes:** Small circular elements are used strictly for graph-inspired patterns and "Human-in-the-Loop" status pings to represent individual data nodes.

## Components

The component library is designed for high-fidelity scouting and data-rich environments:

- **Data Cards:** The primary container. Must include a header area for titles and "action menus," a body for data visualization or lists, and an optional footer for metadata.
- **Human-in-the-Loop Orchestrators:** A specialized component set including "Decision Steppers" and "Verification Badges" (using Clinical Indigo) to highlight where human intervention is needed.
- **Segmented Controls:** Used instead of tabs for filtering data views, maintaining the "instrument" aesthetic.
- **Status Micro-Chips:** Compact, semi-transparent badges used within tables to indicate scouting phases (e.g., "In Review," "Validated," "Risk Flagged").
- **Search & Filter Bars:** Integrated directly into the header or card top-actions, utilizing high-contrast borders and clear focus states.
- **Input Fields:** Minimalist design with 1px borders that thicken and change to Clinical Indigo upon focus. Labeling is always persistent (never placeholder-only) to ensure clarity in complex forms.