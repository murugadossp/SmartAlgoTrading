# Modern UI, theme toggle, and card-based frontend

Plan for redesigning the SmartAlgoTrading frontend with a modern look, light/dark theme, and card-based layout.

## Current state

- Single `frontend/src/App.jsx` with inline route components and a plain `<nav>`.
- `frontend/src/index.css` is minimal: `system-ui`, basic nav/main styles, no theme or design tokens.
- No theme switching, no header with profile area, no card-based layout.

## Target outcome

- **Theme**: Light/dark mode via CSS variables and a toggle in the header; preference persisted in `localStorage`.
- **Typography**: Modern font (e.g. **Inter** or **DM Sans** from Google Fonts), clear hierarchy and spacing.
- **Layout**: App shell with a fixed/sticky header (logo, nav, theme toggle, user-profile placeholder), and a constrained main content area.
- **Visual style**: Card-based UI—reusable `Card` component, feature cards on the home page, and consistent cards for Portfolio / Explore / Learning sections.
- **User profile**: Placeholder only (e.g. avatar circle + "Profile" or "Sign in" label); real auth/profile implemented later.

---

## 1. Theme system (light / dark)

- **CSS variables** in a dedicated file (e.g. `frontend/src/theme.css`) for backgrounds, text, borders, focus ring, link color, card background and shadow.
- **Two themes**: `[data-theme="light"]` and `[data-theme="dark"]` on root, with variables swapped per theme.
- **React**: Theme context with `theme` and `toggleTheme`; initial value from `localStorage` (key e.g. `smart-algo-theme`) or `prefers-color-scheme`; set `data-theme` on root.
- **Toggle**: Sun/moon icon (inline SVG) in the header.

---

## 2. Typography and base styles

- **Font**: Load one modern font (e.g. **Inter** or **DM Sans**) from Google Fonts in `index.html`.
- **Base**: Font on `body`; base font size and line-height; heading scale; optional `.text-muted`.
- **Spacing**: Simple scale (e.g. 4–48 px); content `max-width: 1200px`, centered.

---

## 3. App shell and header

- **Header**: Sticky; left: logo + app name; nav links (Portfolio Mode, Explore Algos, Learning); right: theme toggle + user profile placeholder.
- **User profile placeholder**: Circle avatar + "Profile" or "Sign in"; no action for now.
- **Nav**: `NavLink` with active class.
- **Main**: Padding and max-width.

---

## 4. Card component and card-based layout

- **Card**: Theme-aware background, border-radius, shadow, padding; optional `title`, `onClick`, `className`.
- **Home**: Hero + grid of 3 feature cards (Portfolio, Explore, Learning) linking to routes.
- **Other pages**: Placeholder content wrapped in cards.

---

## 5. Implementation order

1. Add theme CSS variables (light/dark) and base typography/spacing.
2. Implement ThemeContext and theme toggle; set `data-theme` on root.
3. Add Layout with header (logo, nav, theme toggle, user placeholder).
4. Add Card component; refactor home to hero + feature-card grid.
5. Wire Layout into App; use cards on placeholder pages.
6. Load font in index.html; polish spacing and shadows.
