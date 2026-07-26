"""Reusable visual primitives for the ESG-BCS Streamlit prototype.

The scoring engine stays deliberately separate from this module.  Everything
here is presentation-only: icons, design tokens, and motion rules.
"""

from __future__ import annotations


_ICON_PATHS = {
    "dashboard": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    "geospatial": '<path d="M12 21s-6-5.3-6-10a6 6 0 1 1 12 0c0 4.7-6 10-6 10Z"/><circle cx="12" cy="11" r="2.2"/>',
    "detail": '<rect x="4.5" y="3" width="15" height="18" rx="2.2"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4.5"/>',
    "math": '<path d="M17.5 5H7l5 7-5 7h10.5"/>',
    "comparison": '<path d="M12 3.5v17"/><rect x="3.5" y="7" width="6" height="10" rx="1.6"/><rect x="14.5" y="7" width="6" height="10" rx="1.6"/>',
    "shield": '<path d="M12 3 19 6v5.2c0 4.4-2.8 7.8-7 9.8-4.2-2-7-5.4-7-9.8V6l7-3Z"/><path d="m9 12 2 2 4-4"/>',
    "activity": '<path d="M3 12h4l2-6 4 12 2-6h6"/>',
    "user": '<circle cx="12" cy="8" r="3.2"/><path d="M5 20c.7-3.3 3-5 7-5s6.3 1.7 7 5"/>',
    "logout": '<path d="M10 5H6.5A1.5 1.5 0 0 0 5 6.5v11A1.5 1.5 0 0 0 6.5 19H10"/><path d="M14 8l4 4-4 4M18 12H9"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M7 3v4M17 3v4M3.5 9h17"/>',
    "check": '<path d="m5 12 4.2 4.2L19 6.5"/>',
    "x": '<path d="m6 6 12 12M18 6 6 18"/>',
    "alert": '<path d="M12 4 21 19H3L12 4Z"/><path d="M12 9v4M12 16h.01"/>',
    "building": '<path d="M4 21V5l8-3 8 3v16M2 21h20M8 8h1M15 8h1M8 12h1M15 12h1M8 16h1M15 16h1"/>',
    "ruler": '<path d="m4 16 12-12 4 4L8 20H4v-4Z"/><path d="m13 7 4 4M10 10l4 4M7 13l4 4"/>',
    "leaf": '<path d="M20 4C11 4 5 8 5 15c0 2.7 2 5 5 5 7 0 10-6 10-16Z"/><path d="M4 20c2-4 6-7 11-9"/>',
    "database": '<ellipse cx="12" cy="5" rx="7" ry="3"/><path d="M5 5v7c0 1.7 3.1 3 7 3s7-1.3 7-3V5M5 12v7c0 1.7 3.1 3 7 3s7-1.3 7-3v-7"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "eye": '<path d="M2.5 12s3.2-5 9.5-5 9.5 5 9.5 5-3.2 5-9.5 5-9.5-5-9.5-5Z"/><circle cx="12" cy="12" r="2.2"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    "route": '<circle cx="6" cy="18" r="2"/><circle cx="18" cy="6" r="2"/><path d="M8 18c5 0 2-8 8-8"/>',
    "spark": '<path d="m12 3 1.3 5.7L19 10l-5.7 1.3L12 17l-1.3-5.7L5 10l5.7-1.3L12 3ZM19 16l.6 2.4L22 19l-2.4.6L19 22l-.6-2.4L16 19l2.4-.6L19 16Z"/>',
    "arrow-right": '<path d="M4 12h15M13 6l6 6-6 6"/>',
    "arrow-up-right": '<path d="M5 19 19 5M9 5h10v10"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5M12 8h.01"/>',
    "lock": '<rect x="5" y="10" width="14" height="10" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5h8v2M3 12h18M10 12v2h4v-2"/>',
    "network": '<circle cx="12" cy="5" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><path d="m10.8 6.8-4.6 9.4M13.2 6.8l4.6 9.4M7 18h10"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "search": '<circle cx="10.8" cy="10.8" r="6.2"/><path d="m16 16 4 4"/>',
}


def icon(name: str, size: int = 18, stroke: float = 1.8, extra_class: str = "") -> str:
    """Return a consistent currentColor SVG icon for HTML fragments."""

    path = _ICON_PATHS.get(name, _ICON_PATHS["info"])
    classes = f' class="ui-icon {extra_class}"' if extra_class else ' class="ui-icon"'
    return (
        f'<svg{classes} width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="currentColor" stroke-width="{stroke}" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        f'{path}</svg>'
    )


def design_styles() -> str:
    """Return the visual system and motion layer used by the prototype."""

    return r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --ui-bg: #f4f7fb;
  --ui-surface: rgba(255,255,255,.92);
  --ui-surface-solid: #ffffff;
  --ui-ink: #15213d;
  --ui-muted: #71809a;
  --ui-subtle: #9ca9bd;
  --ui-line: #e4eaf3;
  --ui-line-strong: #d5deeb;
  --ui-navy: #142b5f;
  --ui-navy-2: #0b1734;
  --ui-violet: #6658d8;
  --ui-teal: #12a983;
  --ui-cyan: #31c8bf;
  --ui-amber: #d88927;
  --ui-red: #d95555;
  --ui-shadow-1: 0 1px 2px rgba(21,33,61,.04), 0 8px 24px rgba(21,33,61,.05);
  --ui-shadow-2: 0 12px 32px rgba(21,33,61,.09), 0 2px 7px rgba(21,33,61,.05);
  /* Restrained claymorphism tokens. Used only on selected surfaces. */
  --clay-surface: linear-gradient(145deg, #fbfdff 0%, #eef4fa 100%);
  --clay-highlight: rgba(255,255,255,.88);
  --clay-shadow: rgba(79,103,137,.16);
  --clay-shadow-soft: rgba(255,255,255,.92);
  --clay-inset: inset 1px 1px 0 rgba(255,255,255,.72), inset -1px -1px 0 rgba(116,143,177,.07);
  --ui-ease: cubic-bezier(.22,.8,.28,1);
}

html, body, [class*="css"] { font-family: 'Fira Sans', 'Plus Jakarta Sans', sans-serif !important; }
body { background: var(--ui-bg) !important; }
.stApp {
  background:
    radial-gradient(900px 360px at 15% -8%, rgba(102,88,216,.10), transparent 68%),
    radial-gradient(820px 420px at 102% 8%, rgba(18,169,131,.09), transparent 62%),
    linear-gradient(180deg, #f9fbfd 0%, var(--ui-bg) 72%, #eef3f9 100%) !important;
}
.block-container { max-width: 1440px !important; padding: 0 38px 72px !important; }

/* Brand shell */
.topstrip {
  height: 30px !important; padding: 0 14px !important; border-radius: 0 0 10px 10px !important;
  background: linear-gradient(90deg, var(--ui-navy-2), var(--ui-navy)) !important;
  letter-spacing: .25px !important; font-size: 10px !important;
}
.topstrip .ts-id { color: rgba(255,255,255,.82) !important; }
.topstrip .ts-seal { width: 9px !important; height: 9px !important; border-radius: 3px !important; }
.topstrip .ts-right { font-family: 'Fira Code', monospace !important; font-size: 9px !important; }
.navbar-logo { padding-top: 18px !important; gap: 11px !important; }
.navbar-title { font-size: 16px !important; letter-spacing: -.35px !important; }
.navbar-title .sub { color: var(--ui-subtle) !important; font-size: 9px !important; letter-spacing: 1.5px !important; }
.nl-emblem { filter: drop-shadow(0 8px 16px rgba(20,43,95,.18)); }
.user-chip { padding-top: 19px !important; }
.user-chip .avatar { background: linear-gradient(135deg, var(--ui-violet), var(--ui-teal)) !important; box-shadow: 0 6px 16px rgba(102,88,216,.22); }
.user-chip .uc-name { font-size: 12px !important; }
.user-chip .uc-role { font-size: 10px !important; color: var(--ui-muted) !important; }
.navline { background: linear-gradient(90deg, transparent, var(--ui-line-strong), transparent) !important; }

.nav-menu {
  display: flex; align-items: center; justify-content: center; gap: 4px;
  padding: 14px 0 10px;
}
.nav-item {
  display: flex; align-items: center; gap: 8px; position: relative;
  padding: 9px 14px; border-radius: 12px; color: var(--ui-muted);
  font-size: 12.5px; font-weight: 600; white-space: nowrap;
  transition: color .22s var(--ui-ease), background .22s var(--ui-ease), transform .22s var(--ui-ease);
}
.nav-item::after {
  content: ''; position: absolute; left: 15px; right: 15px; bottom: -8px; height: 2px;
  border-radius: 2px; background: transparent; transform: scaleX(.2);
  transition: transform .28s var(--ui-ease), background .28s var(--ui-ease);
}
.nav-item:hover { color: var(--ui-navy); background: rgba(255,255,255,.65); transform: translateY(-1px); }
.nav-item.is-active { color: var(--ui-navy); background: rgba(255,255,255,.84); box-shadow: var(--ui-shadow-1); }
.nav-item.is-active::after { background: linear-gradient(90deg, var(--ui-violet), var(--ui-teal)); transform: scaleX(1); }
.nav-icon { width: 17px; height: 17px; display: inline-flex; color: currentColor; }
.ui-icon { display: inline-block; flex: 0 0 auto; vertical-align: middle; }
.rp-score-label { display: inline-flex; align-items: center; gap: 8px; }
.score-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; box-shadow: 0 0 0 3px rgba(21,33,61,.04); }
.rp-detail-key .ui-icon { color: var(--ui-violet); }
.nav-overlay { margin-top: -49px !important; }
.nav-overlay .stButton > button { height: 45px !important; border-radius: 12px !important; }

/* Shared surfaces */
.card, .math-card, .geo-vcard, .geo-var, .insight-card, .soft-note {
  border-color: var(--ui-line) !important; border-radius: 18px !important;
  box-shadow: var(--ui-shadow-1) !important; transition: transform .25s var(--ui-ease), box-shadow .25s var(--ui-ease), border-color .25s var(--ui-ease) !important;
}
.card:hover, .math-card:hover, .geo-vcard:hover, .geo-var:hover { transform: translateY(-3px) !important; box-shadow: var(--ui-shadow-2) !important; border-color: rgba(102,88,216,.22) !important; }
.card-title { font-size: 12px !important; letter-spacing: .65px !important; text-transform: uppercase; color: var(--ui-muted) !important; }
.debtor-bar { padding-top: 24px !important; }
.debtor-name { font-size: 29px !important; letter-spacing: -.9px !important; }
.debtor-sub { color: var(--ui-muted) !important; font-size: 13px !important; }
.debtor-badge { border-radius: 999px !important; letter-spacing: .25px; }
.workspace-head { display:flex; align-items:center; justify-content:space-between; gap:18px; padding:20px 2px 0; }
.workspace-head .eyebrow { color:var(--ui-violet); font-family:'Fira Code',monospace; font-size:9px; font-weight:700; letter-spacing:1.25px; text-transform:uppercase; }
.workspace-head .headline { color:var(--ui-ink); font-size:13px; font-weight:700; margin-top:5px; }
.workspace-head .meta { display:flex; align-items:center; gap:8px; flex-wrap:wrap; justify-content:flex-end; }
.workspace-tag { display:inline-flex; align-items:center; gap:6px; padding:7px 10px; border:1px solid var(--ui-line); border-radius:999px; color:var(--ui-muted); background:rgba(255,255,255,.62); font-size:10px; font-weight:700; }
.workspace-tag .ui-icon { color:var(--ui-teal); }

/* Showcase-inspired motion */
@keyframes uiPageIn { from { opacity: 0; transform: translateY(14px) scale(.992); filter: blur(2px); } to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); } }
@keyframes uiFadeThrough { 0% { opacity: 0; transform: scale(.98); } 45% { opacity: 1; transform: scale(1); } 100% { opacity: 1; transform: scale(1); } }
@keyframes uiRise { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
@keyframes uiScaleIn { from { opacity: 0; transform: scale(.94); } to { opacity: 1; transform: scale(1); } }
@keyframes uiPulseLine { 0%,100% { opacity: .45; transform: scaleX(.75); } 50% { opacity: 1; transform: scaleX(1); } }
.block-container { animation: uiPageIn .42s var(--ui-ease) both; }
.hero-strip { animation: uiFadeThrough .48s var(--ui-ease) both !important; }
.hero-strip::before { content: ''; position: absolute; inset: 0; opacity: .18; background-image: linear-gradient(rgba(255,255,255,.16) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.16) 1px, transparent 1px); background-size: 28px 28px; mask-image: linear-gradient(90deg, black, transparent 78%); pointer-events: none; }
.hero-strip > * { position: relative; z-index: 1; }
.score-orbit { animation: uiScaleIn .48s var(--ui-ease) both !important; }
.score-orbit:nth-child(2) { animation-delay: .06s !important; }
.score-orbit:nth-child(3) { animation-delay: .12s !important; }
.rec-item, .geo-vcard, .geo-var, .math-card { animation: uiRise .38s var(--ui-ease) both; }
.rec-item:nth-child(2), .geo-vcard:nth-child(2), .geo-var:nth-child(2) { animation-delay: .05s; }
.rec-item:nth-child(3), .geo-vcard:nth-child(3), .geo-var:nth-child(3) { animation-delay: .10s; }
.rec-item:nth-child(4), .geo-var:nth-child(4) { animation-delay: .15s; }
.rec-item:nth-child(5), .geo-var:nth-child(5) { animation-delay: .20s; }
.formula-bar { border-left: 3px solid var(--ui-violet) !important; animation: uiRise .42s var(--ui-ease) .18s both !important; }
.math-result-badge { font-family: 'Fira Code', monospace !important; }

/* Selective claymorphism layer
   The visual language is tactile, but the analytical canvas remains calm. */
.score-orbit,
.geo-vcard,
.geo-var,
.comp-score-box,
.weight-bar-wrap,
.workspace-tag,
.debtor-badge {
  background: var(--clay-surface) !important;
  border-color: rgba(255,255,255,.82) !important;
  box-shadow: -7px -7px 16px var(--clay-shadow-soft),
              9px 11px 22px var(--clay-shadow),
              var(--clay-inset) !important;
}
.score-orbit {
  position: relative;
  overflow: hidden;
  border-radius: 22px !important;
  box-shadow: -10px -10px 22px var(--clay-shadow-soft),
              12px 15px 28px rgba(79,103,137,.18),
              var(--clay-inset) !important;
}
.score-orbit::after {
  content: '';
  position: absolute;
  inset: 1px;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(255,255,255,.34), transparent 34%, transparent 72%, rgba(213,225,238,.10));
  pointer-events: none;
}
.score-orbit > * { position: relative; z-index: 1; }
.score-orbit:hover,
.geo-vcard:hover,
.geo-var:hover {
  transform: translateY(-3px) !important;
  box-shadow: -9px -9px 19px var(--clay-shadow-soft),
              12px 15px 27px rgba(79,103,137,.20),
              var(--clay-inset) !important;
}
.workspace-tag {
  background: linear-gradient(145deg, rgba(255,255,255,.94), rgba(239,245,251,.86)) !important;
  box-shadow: -4px -4px 9px rgba(255,255,255,.88),
              5px 6px 12px rgba(79,103,137,.12),
              inset 1px 1px 0 rgba(255,255,255,.72) !important;
}
.nav-item.is-active {
  background: linear-gradient(145deg, #ffffff, #edf3f9) !important;
  box-shadow: -5px -5px 11px rgba(255,255,255,.9),
              6px 7px 14px rgba(79,103,137,.13),
              inset 1px 1px 0 rgba(255,255,255,.78) !important;
}
.hero-pill {
  box-shadow: inset 1px 1px 0 rgba(255,255,255,.18),
              0 5px 14px rgba(5,19,51,.16) !important;
}
.comp-score-box {
  box-shadow: -4px -4px 9px rgba(255,255,255,.78),
              5px 6px 12px rgba(79,103,137,.09),
              inset 1px 1px 0 rgba(255,255,255,.72) !important;
}
.weight-bar-wrap {
  box-shadow: inset 2px 2px 5px rgba(79,103,137,.08),
              inset -1px -1px 0 rgba(255,255,255,.74) !important;
}
.math-result-badge {
  box-shadow: -4px -4px 9px rgba(255,255,255,.72),
              5px 7px 13px rgba(79,103,137,.10),
              inset 1px 1px 0 rgba(255,255,255,.34) !important;
}
.stTextInput > div > div > input {
  background: linear-gradient(145deg, #f9fcff, #eef4fa) !important;
  border-color: rgba(255,255,255,.86) !important;
  box-shadow: inset 2px 2px 5px rgba(79,103,137,.07),
              inset -2px -2px 5px rgba(255,255,255,.84) !important;
}

/* Data hierarchy */
.hero-strip { border-radius: 22px !important; background: linear-gradient(115deg, #102350 0%, #183d7b 60%, #137b70 125%) !important; box-shadow: 0 18px 38px rgba(20,43,95,.18) !important; }
.hero-kicker { font-family: 'Fira Code', monospace !important; font-size: 9px !important; letter-spacing: 1.4px !important; }
.hero-caption { font-size: 13px !important; }
.hero-pill { border-radius: 999px !important; padding: 8px 12px !important; background: rgba(255,255,255,.10) !important; }
.seg-track { height: 8px !important; background: #edf1f7 !important; }
.seg-fill { box-shadow: 0 0 10px rgba(18,169,131,.14); }
.seg-score, .comp-score-val, .rp-detail-val, .rp-score-row span:last-child { font-family: 'Fira Code', monospace !important; }
.comp-score-box { border-radius: 13px !important; background: linear-gradient(180deg, #fbfcfe, #f2f6fb) !important; }
.weight-bar-wrap { border-radius: 12px !important; background: #eef2f8; }
.insight-card { border-left-color: var(--ui-violet) !important; }
.soft-note { background: rgba(248,250,253,.8) !important; line-height: 1.65 !important; }

/* Controls */
.stButton > button { transition: transform .2s var(--ui-ease), box-shadow .2s var(--ui-ease), border-color .2s var(--ui-ease), background .2s var(--ui-ease) !important; cursor: pointer !important; }
.stButton > button:hover { transform: translateY(-2px) !important; }
.stButton > button:active { transform: scale(.98) !important; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg, var(--ui-navy), var(--ui-violet)) !important; box-shadow: 0 10px 24px rgba(102,88,216,.22) !important; }
.stButton > button[kind="primary"] { box-shadow: 0 10px 24px rgba(102,88,216,.22), inset 1px 1px 0 rgba(255,255,255,.18) !important; }
.stButton > button[kind="secondary"] {
  color: var(--ui-navy) !important;
  border-color: rgba(255,255,255,.86) !important;
  background: linear-gradient(145deg, #ffffff, #eef4fa) !important;
  box-shadow: -5px -5px 11px rgba(255,255,255,.9),
              6px 8px 15px rgba(79,103,137,.13),
              inset 1px 1px 0 rgba(255,255,255,.75) !important;
}
.stButton > button[kind="secondary"]:active { box-shadow: inset 2px 2px 5px rgba(79,103,137,.10), inset -2px -2px 5px rgba(255,255,255,.8) !important; }
.stButton > button:focus-visible { outline: 3px solid rgba(49,200,191,.35) !important; outline-offset: 3px !important; }
.stTextInput > div > div > input { font-family: 'Fira Code', monospace !important; border-radius: 13px !important; }

/* Login and loading */
.login-form-intro { padding: 2px 1px 10px; }
.login-brand-row { display:flex; align-items:center; gap:12px; margin-bottom:30px; }
.login-brand-mark {
  display:flex; align-items:center; justify-content:center; width:46px; height:46px;
  border:1px solid rgba(255,255,255,.80); border-radius:16px;
  background:linear-gradient(145deg, #ffffff, #edf4fa);
  box-shadow:-5px -5px 11px rgba(255,255,255,.88), 6px 8px 15px rgba(79,103,137,.13), inset 1px 1px 0 rgba(255,255,255,.78);
}
.login-brand-name { color:#142b5f !important; font-size:13px; font-weight:800; letter-spacing:.35px; }
.login-brand-role { margin-top:3px; color:#71809a !important; font-size:9px; font-weight:700; letter-spacing:1.15px; text-transform:uppercase; }
.login-kicker { color:#0b8b72 !important; font-family:'Fira Code',monospace; font-size:9px; font-weight:700; letter-spacing:1.3px; text-transform:uppercase; }
.login-title { margin-top:9px; color:#15213d !important; font-size:33px; font-weight:800; line-height:1.08; letter-spacing:-1.05px; }
.login-title em { color:#6658d8 !important; font-style:normal; }
.login-description { max-width:390px; margin-top:12px; color:#5e6f88 !important; font-size:13px; line-height:1.65; }
.login-field-label { margin:12px 0 7px; color:#15213d !important; font-size:11px; font-weight:800; letter-spacing:.7px; text-transform:uppercase; }
.login-field-hint { margin:8px 0 2px; color:#71809a !important; font-size:10.5px; line-height:1.5; }
.login-meta-row { display:flex; align-items:center; gap:7px; margin-top:16px; color:#5e6f88 !important; font-size:10px; line-height:1.4; }
.login-meta-row .ui-icon { color:var(--ui-teal); }
.login-divider { display:flex; align-items:center; gap:10px; margin:24px 0 12px; color:#8796aa !important; font-size:9px; font-weight:800; letter-spacing:1.25px; text-transform:uppercase; }
.login-divider::before, .login-divider::after { content:''; height:1px; flex:1; background:var(--ui-line); }
.login-demo-title { margin-bottom:10px; color:#5e6f88 !important; font-size:11px; line-height:1.45; }
.login-legal { margin-top:20px; color:#8796aa !important; font-family:'Fira Code',monospace; font-size:9px; letter-spacing:.55px; line-height:1.5; text-align:center; }
.login-feedback { display:flex; align-items:center; gap:7px; margin:10px 0 0; font-size:12px; font-weight:700; line-height:1.45; }
.login-feedback .ui-icon { flex:0 0 auto; }
.login-feedback.is-error { color:var(--ui-red); }
.login-feedback.is-warning { color:var(--ui-amber); }
.login-art-caption { color:#71809a !important; }
.identity-card {
  position:relative; overflow:hidden; margin-bottom:14px; padding:14px 14px 16px;
  background:linear-gradient(145deg, #fbfdff 0%, #eef4fa 100%) !important;
  border:1px solid rgba(255,255,255,.92); border-radius:26px !important;
  box-shadow:-7px -7px 16px rgba(255,255,255,.84), 10px 14px 30px rgba(49,72,105,.14), inset 1px 1px 0 rgba(255,255,255,.88);
  text-align:center; animation:uiRise .42s var(--ui-ease) both;
}
.identity-card::before {
  content:''; position:absolute; width:170px; height:170px; right:-90px; top:-94px;
  border-radius:50%; background:radial-gradient(circle, rgba(18,169,131,.15), transparent 68%); pointer-events:none;
}
.identity-card-head { position:relative; z-index:1; display:flex; align-items:center; justify-content:space-between; gap:8px; text-align:left; }
.identity-kicker { color:#5b4fc4 !important; -webkit-text-fill-color:#5b4fc4 !important; font-family:'Fira Code',monospace; font-size:9px; font-weight:800; letter-spacing:1px; text-transform:uppercase; opacity:1 !important; }
.identity-chip { padding:5px 8px; border:1px solid #b9e7da; border-radius:999px; color:#087a68 !important; -webkit-text-fill-color:#087a68 !important; background:#e5f6f1; font-family:'Fira Code',monospace; font-size:8.5px; font-weight:800; white-space:nowrap; opacity:1 !important; }
.identity-avatar-wrap { position:relative; z-index:1; display:block; width:100%; height:auto; aspect-ratio:1/1; margin:0 0 16px; padding:5px; overflow:hidden; border:1px solid rgba(255,255,255,.96); border-radius:26px; background:linear-gradient(145deg,#ffffff,#dfe9f3); box-shadow:0 20px 38px rgba(20,43,95,.18), 0 7px 16px rgba(18,169,131,.10), inset 1px 1px 0 rgba(255,255,255,.92); }
.identity-avatar, .identity-avatar-fallback { display:block; width:100%; height:100%; border-radius:21px; object-fit:cover; object-position:center 34%; opacity:1 !important; visibility:visible !important; clip-path:inset(0 round 21px); }
.identity-avatar-fallback { color:var(--ui-navy); background:linear-gradient(135deg,rgba(102,88,216,.16),rgba(18,169,131,.16)); font-size:24px; font-weight:800; }
.identity-name { position:relative; z-index:1; color:#15213d !important; -webkit-text-fill-color:#15213d !important; font-size:17px; font-weight:800; letter-spacing:-.3px; line-height:1.25; opacity:1 !important; }
.identity-role, .identity-address { position:relative; z-index:1; display:flex; align-items:center; justify-content:center; gap:6px; margin-top:7px; color:#4f6078 !important; -webkit-text-fill-color:#4f6078 !important; font-size:11px; line-height:1.45; opacity:1 !important; }
.identity-role .ui-icon, .identity-address .ui-icon { color:var(--ui-teal); flex:0 0 auto; }
.identity-address { margin-top:5px; color:#142b5f !important; -webkit-text-fill-color:#142b5f !important; font-weight:700; }
.identity-address-sub { position:relative; z-index:1; margin-top:3px; color:#5e6f88 !important; -webkit-text-fill-color:#5e6f88 !important; font-size:10px; line-height:1.4; opacity:1 !important; }
.identity-note { position:relative; z-index:1; display:flex; align-items:center; justify-content:center; gap:5px; margin-top:13px; padding-top:11px; border-top:1px solid #dce4ef; color:#5e6f88 !important; -webkit-text-fill-color:#5e6f88 !important; font-size:9.5px; line-height:1.45; opacity:1 !important; }
.identity-note .ui-icon { color:var(--ui-violet); flex:0 0 auto; }
.identity-card--comparison { margin-bottom:12px; }
.identity-card--comparison .identity-avatar-wrap { max-width:240px; margin-left:auto; margin-right:auto; }
.auth-panel { border-radius: 28px !important; background: linear-gradient(145deg, #0b1734, #183d7b 70%, #126c67) !important; box-shadow: 0 22px 60px rgba(20,43,95,.22) !important; }
.auth-panel::after { background-size: 30px 30px !important; opacity: .28 !important; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius: 24px !important; box-shadow: var(--ui-shadow-2) !important; }

/* Reduce motion and responsive behavior */
@media (max-width: 1100px) { .block-container { padding-left: 22px !important; padding-right: 22px !important; } .nav-item { padding-left: 9px; padding-right: 9px; } }
@media (max-width: 760px) { .block-container { padding-left: 14px !important; padding-right: 14px !important; } .nav-menu { overflow-x: auto; justify-content: flex-start; } .nav-item { font-size: 11px; } .nav-item::after { display: none; } .topstrip .ts-right { display: none; } .debtor-name { font-size: 24px !important; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; scroll-behavior: auto !important; } }
</style>
"""
