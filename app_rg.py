import streamlit as st
import base64
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import math
import time
import datetime
import sys
from pathlib import Path
from html import escape

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from score_engine import (
    classify_pathway,
    score_debtor_cohort,
    review_status,
)
from ui_kit import design_styles, icon

# ============================================================
# ICONS (base64 embedded) — dipakai di loading page
# ============================================================
ICONS = {
    "loading_icon": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAGv0lEQVR42u2Zf2xVZxnHv8/znvuD/hgbrISi4LLgdFQzY/9wQsvJiXMyjMmS5V4TWgQ0pXYTqkGNyZKdexL/8A9HqWthHa4/sDB3r3EzLgYTsrtLCzJJE7UBXLLBVMY2GFD66/bee9738Y/e1o5osrWUlXk+yU1uznnvOef7Pj/Pc4GAgICAgICAgICAgICAWxERmvrEkkkVbMiHhBbwc0l1R0coGvVbidVtYFpETCG+/NamzPe8UYgQiOTDXpgXqiNPKx8bftzP5/YT5DMQfHGMFy8DACQSszLWQhUMO522BhobC7ps8SesaHS3NqZJ8vkXrWiodC7X5QXlxq7LAFDd0RHKOI5fc6Btg1KcFKMfO7750T5SvMwSoz8embiIK5Oia3r3bq492PEX+0DbagCIJZOqtrN95YbW1sjHQqzd5Uad5P5qAFjfu3dX7cGOEzXPtlZMib31svR1WdV1XX5pxQo10NhYqO5wS0rLlx/gcJTEmAqTz18eH3unbqDRG1+TTIarAA0AZ69e5YHGRn9mUluYJUYmN9YVl23XtWaejMViav1z+59Yf+jpXgCoPdhxsvZXuytv+TpsJ7uWZ+Lb3gGANUk3fKdZuQ4KDxKpewBcMrncstBtZSZ/bfi97JjaUXbhgvJXL/sJiFeJrwukOCRGv3VxyPz09ebm/PXl64NizatK12W7oqJE32HtUYvCd9X27vsrmCcUh+4VMpdEJDNR8Pe8uqnhXbvNLePyu7/QH07/CfUpff/+Jz9lgb6KQuHHIhaT+IYs62dLS/xDrwNn4LoMz1s4gm3XtTKep6Xn6c8DUvbyN+oeqD3UMShA59jYWMPJLTsuT63d8IfWyOGHdo6BqN9Op60MUhClSIw5e2zbzmNT62q6294Q5jl5pTVfls14ng8AEsI3FVtr7NSze0w+f6a/rqllxob4AHB4Y3MOaAYAZBzHn443QgSuy2uqqqzTp075QjTnknTDBceSSZWKx/Xq1h2R5UvufV5EzuWz2XhkcdmXOD+RAECxZJJT8bh/X0vL7eV3RncaI+WA0SoctozvDx7b/GiPUWrSkp5nKtJpA88z6GmXBSXYTrtWyon763r2rCIVeY6AF/rqmn5ePP33qZbxYvFA6ZKQTYz7ldGtRik2xlgw8nj19u2HIr7yETI33PmsGyc2bWUcx6/pabdZqV8I5Im++qbfXb/ufS6rjRLIQP+WHX+cOra2+6mt2cpKKgn5IvPQ+c5dsIBiqSSnHMev6dnXQIqaAKrvq//uoJ1OW/jXqbsQiT6ss1kFKFBEaZ2beOH41uY3hIggVBJLxtQddz/Arw1eUJooBAA5AOF5SC9z3UICQVLxuK7t3fckWYjLsPnK0frGQburK5pxHF8z/1CMWa2Bq77xh0jxZ8FqBwCwAhOTpOIpXVm9XY/m39aQyTCdr4Z59hYWISQSZN+zYqkW0w3gYl9d04NwXYolk+GzR47oogdIfnSk60TDrj8DwJd/2XKGLOuRj6rtm7VgN5Egz/OMdD5VCeZf9219rLeYVSUF5Gd2cSoUWjrVUvqWtXQ61WoA/+O1IDcBhMMLSLDneQYidJRocH3nngnntz0/KmSzmomILGtcj4z+pv87zZcgQgLRUzV3ffderVE0PhmCof/eSETnx8Jzi+FEYnKiGA63SS4fJmOGJa+viTFf40joW1MGfv8d5T/jG2Yhvm4uVXyjisxT62/NUbCASKSn/crI0ZMtA888Mw4AtV1tPixeOR3uZkY7aAzN9rmZ8NEKtl95RSHtwpxnFVlbVbnh4dbzADB6mZZQsRHR54kIWtnpYgz/A0oAttOupd+EEjZsp13r9KkUh0ZLlUTAi1bAKoCVksl1wJuWnXZh/inExKqYMG++S2ccx884ng9INnfuytuHNzbnDm9szomRIQAjGcfzScy479OVjOP5GcfzicwVCEYzjudrwVUpfk99Lp4/saslS5DsQKM3XsiOXgLJ+OTvtk1kHM83oGxh6Np7sxnP3pCgWNfZ+m0VCn8STJtMofCSgIYAQFmqFoKI1voIKxWD0X8zgtcm3ZKqwPRpo/0XmdV9QrRKtPk9E0gEDMVboE0PgNuh+OuizQEiYhExbFmbiORlcy27u7/pB+eQSBA8z9w0wWu72x0Oh5YaXRgmzaXMwhqAIpnQhkWRLBKYMUMcVoKQnhx/5GHIF0YJQfJg8tmgZGoUqUiNQHS5MdowqXEQyqarF6kRUlSaGxs//mrD99+d7TD+/4o5Wdh1XT5dVXXT/65JxeIGhMCyAQEBAQEBAQEBAQEBAQEfkH8D4FYYfmPEhLgAAAAASUVORK5CYII=",
}


def login_illustration_html():
    """Return the self-contained parallax illustration used on the login page."""

    art_path = APP_DIR / "assets" / "login-umkm-rural.webp"
    if art_path.exists():
        encoded = base64.b64encode(art_path.read_bytes()).decode("ascii")
        art_src = f"data:image/webp;base64,{encoded}"
    else:
        art_src = ""

    return """
<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root {
    --mx-far: 0px;
    --my-far: 0px;
    --mx-mid: 0px;
    --my-mid: 0px;
    --mx-near: 0px;
    --my-near: 0px;
    --wind-x: 0px;
    --wind-y: 0px;
    --wind-rot: 0deg;
  }
  * { box-sizing: border-box; }
  html, body { width: 100%; height: 100%; margin: 0; overflow: hidden; }
  body {
    background: transparent;
    color: #15213d;
    font-family: 'Fira Sans', 'Segoe UI', sans-serif;
  }
  .art-shell {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 600px;
    overflow: hidden;
    isolation: isolate;
    border-radius: 28px;
    background: linear-gradient(145deg, #e3f5fb 0%, #d5efee 46%, #f4e4bd 120%);
    box-shadow: -10px -10px 24px rgba(255,255,255,.82), 16px 20px 34px rgba(64,92,119,.17);
  }
  .art-shell::before {
    content: '';
    position: absolute;
    inset: 0;
    z-index: 3;
    pointer-events: none;
    background:
      linear-gradient(90deg, rgba(247,250,245,.96) 0%, rgba(247,250,245,.76) 14%, rgba(247,250,245,.18) 37%, transparent 57%),
      linear-gradient(180deg, rgba(16,46,86,.06), transparent 26%, rgba(8,67,70,.18) 100%);
  }
  .art-shell::after {
    content: '';
    position: absolute;
    inset: 12px;
    z-index: 4;
    border: 1px solid rgba(255,255,255,.60);
    border-radius: 21px;
    pointer-events: none;
  }
  .art-image {
    position: absolute;
    z-index: 1;
    inset: -4%;
    width: 108%;
    height: 108%;
    object-fit: cover;
    transform: translate3d(var(--mx-far), var(--my-far), 0) scale(1.045);
    transform-origin: center center;
    filter: saturate(.96) contrast(.98);
    transition: transform .18s cubic-bezier(.22,.8,.28,1), filter .35s ease;
    will-change: transform;
  }
  .art-shell:hover .art-image { filter: saturate(1.02) contrast(1); }
  .art-glow {
    position: absolute;
    z-index: 2;
    width: 230px;
    height: 230px;
    right: 11%;
    top: 8%;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,.40), rgba(255,255,255,0) 68%);
    transform: translate3d(var(--mx-mid), var(--my-mid), 0);
    pointer-events: none;
    transition: transform .22s cubic-bezier(.22,.8,.28,1);
  }
  .art-badge {
    position: absolute;
    z-index: 5;
    top: 26px;
    right: 28px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 12px;
    border: 1px solid rgba(255,255,255,.66);
    border-radius: 999px;
    background: rgba(255,255,255,.48);
    color: #174a55;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: .8px;
    text-transform: uppercase;
    box-shadow: -4px -4px 9px rgba(255,255,255,.54), 5px 7px 14px rgba(44,86,100,.12);
    backdrop-filter: blur(8px);
    transform: translate3d(var(--mx-near), var(--my-near), 0);
    transition: transform .22s cubic-bezier(.22,.8,.28,1);
  }
  .art-badge i {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #12a983;
    box-shadow: 0 0 0 4px rgba(18,169,131,.16);
  }
  .art-note {
    position: absolute;
    z-index: 5;
    left: 28px;
    bottom: 27px;
    width: min(335px, calc(100% - 56px));
    padding: 17px 19px 16px;
    border: 1px solid rgba(255,255,255,.70);
    border-radius: 19px;
    background: rgba(255,255,255,.62);
    box-shadow: -7px -7px 15px rgba(255,255,255,.55), 9px 12px 21px rgba(49,85,100,.15), inset 1px 1px 0 rgba(255,255,255,.72);
    backdrop-filter: blur(10px);
    transform: translate3d(var(--mx-near), var(--my-near), 0);
    transition: transform .22s cubic-bezier(.22,.8,.28,1);
  }
  .art-kicker {
    display: block;
    margin-bottom: 7px;
    color: #0b8b72;
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 1.4px;
    text-transform: uppercase;
  }
  .art-note strong {
    display: block;
    max-width: 285px;
    color: #16324e;
    font-size: 18px;
    line-height: 1.15;
    letter-spacing: -.35px;
  }
  .art-note p {
    margin: 8px 0 0;
    color: #52687a;
    font-size: 11px;
    line-height: 1.5;
  }
  .wind-lines {
    position: absolute;
    z-index: 4;
    right: 6%;
    top: 22%;
    width: 43%;
    height: 25%;
    opacity: .46;
    pointer-events: none;
    transform: translate3d(var(--mx-mid), var(--my-mid), 0);
    transition: transform .25s cubic-bezier(.22,.8,.28,1);
  }
  .wind-lines path {
    fill: none;
    stroke: rgba(255,255,255,.78);
    stroke-width: 1.5;
    stroke-linecap: round;
    stroke-dasharray: 5 9;
    animation: windFlow 7s ease-in-out infinite;
  }
  .wind-lines path:nth-child(2) { animation-delay: -2.4s; opacity: .72; }
  .wind-lines path:nth-child(3) { animation-delay: -4.1s; opacity: .52; }
  .wind-layer {
    position: absolute;
    z-index: 5;
    pointer-events: none;
    transform: translate3d(calc(var(--mx-near) + var(--wind-x)), calc(var(--my-near) + var(--wind-y)), 0) rotate(var(--wind-rot));
    transition: transform .25s cubic-bezier(.22,.8,.28,1);
  }
  .wind-layer svg { display: block; width: 36px; height: 36px; filter: drop-shadow(0 4px 6px rgba(48,82,87,.22)); }
  .wind-a { left: 48%; top: 14%; }
  .wind-b { right: 20%; top: 54%; }
  .wind-c { left: 64%; bottom: 25%; }
  .leaf-a { animation: leafSway 5.8s ease-in-out infinite; }
  .leaf-b { animation: leafSway 6.5s ease-in-out -2s infinite reverse; }
  .leaf-c { animation: leafSway 5.2s ease-in-out -3.2s infinite; }
  @keyframes windFlow {
    0%, 100% { stroke-dashoffset: 0; opacity: .18; }
    50% { stroke-dashoffset: -28; opacity: .78; }
  }
  @keyframes leafSway {
    0%, 100% { transform: translate3d(-4px, -2px, 0) rotate(-12deg); opacity: .68; }
    35% { transform: translate3d(8px, 6px, 0) rotate(10deg); opacity: 1; }
    70% { transform: translate3d(20px, 17px, 0) rotate(27deg); opacity: .78; }
  }
  @media (max-width: 700px) {
    .art-shell { min-height: 440px; border-radius: 22px; }
    .art-shell::after { inset: 9px; border-radius: 16px; }
    .art-badge { top: 18px; right: 18px; }
    .art-note { left: 18px; bottom: 18px; width: calc(100% - 36px); }
    .art-note strong { font-size: 16px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .art-image, .art-glow, .art-badge, .art-note, .wind-lines, .wind-layer { transition: none; }
    .wind-lines path, .leaf-a, .leaf-b, .leaf-c { animation: none; }
  }
</style>
</head>
<body>
  <div class="art-shell" role="img" aria-label="Ilustrasi petani kopi dan pelaku usaha kecil bertransaksi di pasar desa dengan latar sawah">
    <img class="art-image" src="__ART_URI__" alt="">
    <div class="art-glow"></div>
    <div class="art-badge"><i></i> Rural MSME intelligence</div>
    <svg class="wind-lines" viewBox="0 0 220 120" aria-hidden="true">
      <path d="M8 34C45 4 80 8 111 34s58 28 100 1"></path>
      <path d="M36 62c27-20 55-18 78 2s50 21 83 0"></path>
      <path d="M72 89c21-14 42-12 60 2s36 13 60 0"></path>
    </svg>
    <div class="wind-layer wind-a"><svg class="leaf-a" viewBox="0 0 32 32" aria-hidden="true"><path d="M5 24C7 11 15 5 27 4c-1 12-8 20-22 20Z" fill="#75b995"></path><path d="M7 23c6-6 11-11 18-16" stroke="#3d866f" stroke-width="1.3" fill="none" stroke-linecap="round"></path></svg></div>
    <div class="wind-layer wind-b"><svg class="leaf-b" viewBox="0 0 32 32" aria-hidden="true"><path d="M5 24C7 11 15 5 27 4c-1 12-8 20-22 20Z" fill="#e6ab63"></path><path d="M7 23c6-6 11-11 18-16" stroke="#b87d3f" stroke-width="1.3" fill="none" stroke-linecap="round"></path></svg></div>
    <div class="wind-layer wind-c"><svg class="leaf-c" viewBox="0 0 32 32" aria-hidden="true"><path d="M5 24C7 11 15 5 27 4c-1 12-8 20-22 20Z" fill="#df8e91"></path><path d="M7 23c6-6 11-11 18-16" stroke="#a8586a" stroke-width="1.3" fill="none" stroke-linecap="round"></path></svg></div>
    <div class="art-note">
      <span class="art-kicker">Bukti yang dekat dengan realitas</span>
      <strong>Lahan, pasar, dan cerita usaha dalam satu pandangan.</strong>
      <p>Penilaian yang lebih kontekstual untuk UMKM berkelanjutan.</p>
    </div>
  </div>
  <script>
    (() => {
      const shell = document.querySelector('.art-shell');
      if (!shell || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      let frame = 0;
      let targetX = 0;
      let targetY = 0;
      const render = () => {
        shell.style.setProperty('--mx-far', `${(targetX * .42).toFixed(2)}px`);
        shell.style.setProperty('--my-far', `${(targetY * .42).toFixed(2)}px`);
        shell.style.setProperty('--mx-mid', `${(targetX * .78).toFixed(2)}px`);
        shell.style.setProperty('--my-mid', `${(targetY * .78).toFixed(2)}px`);
        shell.style.setProperty('--mx-near', `${targetX.toFixed(2)}px`);
        shell.style.setProperty('--my-near', `${targetY.toFixed(2)}px`);
        frame = 0;
      };
      const move = (event) => {
        const box = shell.getBoundingClientRect();
        targetX = ((event.clientX - box.left) / box.width - .5) * 18;
        targetY = ((event.clientY - box.top) / box.height - .5) * 14;
        if (!frame) frame = requestAnimationFrame(render);
      };
      const reset = () => {
        targetX = 0;
        targetY = 0;
        if (!frame) frame = requestAnimationFrame(render);
      };
      const leafLayers = Array.from(shell.querySelectorAll('.wind-layer'));
      const leafStart = performance.now();
      const animateLeaves = (now) => {
        const elapsed = (now - leafStart) / 1000;
        leafLayers.forEach((leaf, index) => {
          const phase = elapsed * (0.52 + index * 0.07) + index * 1.7;
          const drift = Math.sin(phase) * 12 + Math.sin(phase * .42) * 5;
          const fall = (Math.sin(elapsed * .38 + index * 1.2) * .5 + .5) * 18;
          const rotate = Math.sin(phase * .8) * 18;
          leaf.style.setProperty('--wind-x', `${drift.toFixed(2)}px`);
          leaf.style.setProperty('--wind-y', `${fall.toFixed(2)}px`);
          leaf.style.setProperty('--wind-rot', `${rotate.toFixed(2)}deg`);
        });
        requestAnimationFrame(animateLeaves);
      };
      requestAnimationFrame(animateLeaves);
      shell.addEventListener('pointermove', move, { passive: true });
      shell.addEventListener('pointerleave', reset, { passive: true });
    })();
  </script>
</body>
</html>
""".replace("__ART_URI__", art_src)

st.set_page_config(page_title="BCS-ESG System", page_icon=":material/analytics:", layout="wide", initial_sidebar_state="collapsed")

# ============================================================
# SESSION STATE
# ============================================================
for k, v in [
    ("page","login"),
    ("view","dashboard"),
    ("res",None),
    ("loading",False),
    ("load_step",0),
    ("demo_guide_seen",False),
    ("demo_guide_requested",False),
]:
    if k not in st.session_state: st.session_state[k] = v

# ============================================================
# DATABASE
# ============================================================
DB = {
    "3374010101010001": {"nama":"Geovany Bramanthya","usaha":"Petani Kopi","lokasi":"Sidomulyo, Semarang","alamat":"Semarang, Jawa Tengah","id_type":"KTP","id_no":"3374 **** **** 0001","tgl_lahir":"12 Mar 1990","sejak":"Jan 2018","activity_type":"agri","data_availability":{"transaction_history":False,"digital_payments":False,"financial_statements":False,"credit_bureau":True},"5C":[95,70,65,85,40],"ESG":[72,88,30],"lat":-7.0051,"lng":110.4381,
        "geo":{"ndvi":0.74,"ndvi_label":"Vegetasi rapat / lahan produktif","proximity_m":1150,"proximity_poi":"Pasar Sidomulyo","road_m":420,"building_verified":True,"building_count":2,"flood_risk":"Rendah","flood_score":86,"land_use":"Perkebunan / lahan pertanian","land_class":"agri","protected_zone_ok":True,"ntl":4.1,"ntl_label":"Rendah (rural)","claim":"Lahan kopi produktif","claim_match":True}},
    "3374010101010002": {"nama":"Salma Aulia","usaha":"Toko Online Fashion","lokasi":"Kota Semarang","alamat":"Semarang, Jawa Tengah","id_type":"KTP","id_no":"3374 **** **** 5412","tgl_lahir":"14 Jul 1993","sejak":"Mar 2021","activity_type":"urban","data_availability":{"transaction_history":True,"digital_payments":True,"financial_statements":True,"credit_bureau":True},"5C":[60,90,80,75,85],"ESG":[65,70,80],"lat":-6.9667,"lng":110.4167,
        "geo":{"ndvi":0.19,"ndvi_label":"Area terbangun / urban","proximity_m":280,"proximity_poi":"Pusat Niaga Simpang Lima","road_m":60,"building_verified":True,"building_count":8,"flood_risk":"Sedang","flood_score":58,"land_use":"Permukiman / komersial","land_class":"urban","protected_zone_ok":True,"ntl":29.3,"ntl_label":"Tinggi (urban)","claim":"Toko & gudang online","claim_match":True}},
    "3374010101010003": {"nama":"Reva Adinda","usaha":"Pengrajin Anyaman","lokasi":"Penglipuran, Bali","alamat":"Bali","id_type":"KTP","id_no":"5171 **** **** 0003","tgl_lahir":"03 Aug 1988","sejak":"Jun 2015","activity_type":"mixed","data_availability":{"transaction_history":True,"digital_payments":False,"financial_statements":False,"credit_bureau":False},"5C":[90,65,60,80,30],"ESG":[80,85,25],"lat":-8.4095,"lng":115.1889,
        "geo":{"ndvi":0.57,"ndvi_label":"Vegetasi sedang","proximity_m":2300,"proximity_poi":"Pasar Bangli","road_m":150,"building_verified":True,"building_count":3,"flood_risk":"Rendah","flood_score":91,"land_use":"Permukiman pedesaan / vegetasi","land_class":"mixed","protected_zone_ok":True,"ntl":6.5,"ntl_label":"Rendah-sedang","claim":"Workshop anyaman desa","claim_match":True}},
    "3374010101010004": {"nama":"Tirta Wahyu","usaha":"Agribisnis (klaim lahan)","lokasi":"Lokasi belum terverifikasi","alamat":"Demak, Jawa Tengah","id_type":"KTP","id_no":"3321 **** **** 0004","tgl_lahir":"09 Sep 1991","sejak":"Klaim 2022","activity_type":"agri","data_availability":{"transaction_history":False,"digital_payments":False,"financial_statements":False,"credit_bureau":False},"5C":[10,35,35,30,8],"ESG":[18,25,12],"lat":-6.8901,"lng":110.6400,
        "geo":{"ndvi":0.11,"ndvi_label":"Lahan gundul / non-vegetasi","proximity_m":5200,"proximity_poi":"Pasar terdekat","road_m":1800,"building_verified":False,"building_count":0,"flood_risk":"Tinggi","flood_score":31,"land_use":"Lahan kosong / tidak teridentifikasi","land_class":"empty","protected_zone_ok":False,"ntl":0.6,"ntl_label":"Nyaris nol","claim":"Lahan pertanian produktif","claim_match":False}},
}


def close_demo_guide():
    """Tutup panduan dan cegah dialog terbuka kembali pada sesi yang sama."""
    st.session_state.demo_guide_seen = True
    st.session_state.demo_guide_requested = False


@st.dialog(
    "Akun demo siap digunakan",
    width="large",
    dismissible=True,
    icon=":material/account_circle:",
    on_dismiss=close_demo_guide,
)
def render_demo_guide():
    st.markdown(
        """
        <section class="demo-guide-hero">
            <div class="demo-guide-kicker">Panduan singkat untuk dewan juri</div>
            <h2>Jelajahi prototipe tanpa memasukkan NIK pribadi.</h2>
            <p>
                Empat profil simulasi telah disiapkan pada halaman masuk.
                Tutup panduan ini, lalu pilih salah satu tombol profil untuk
                membuka <i>workspace</i> penilaian secara langsung.
            </p>
        </section>
        <div class="demo-guide-flow" aria-label="Alur penggunaan akun demo">
            <span><b>1</b> Tutup panduan</span>
            <i aria-hidden="true"></i>
            <span><b>2</b> Pilih profil simulasi</span>
            <i aria-hidden="true"></i>
            <span><b>3</b> Tinjau hasil analisis</span>
        </div>
        <div class="demo-guide-grid">
            <article class="demo-profile-card is-amber">
                <div class="demo-profile-tag">Data-Thin · 1/4 data</div>
                <h3>Geovany Bramanthya</h3>
                <p>Petani kopi sebagai skenario inklusi debitur dengan data terbatas.</p>
            </article>
            <article class="demo-profile-card is-teal">
                <div class="demo-profile-tag">Data-Rich · 4/4 data</div>
                <h3>Salma Aulia</h3>
                <p>Toko daring sebagai pembanding dengan ketersediaan data lengkap.</p>
            </article>
            <article class="demo-profile-card is-violet">
                <div class="demo-profile-tag">Data-Thin · 1/4 data</div>
                <h3>Reva Adinda</h3>
                <p>Pengrajin rural untuk melihat penilaian yang tetap kontekstual.</p>
            </article>
            <article class="demo-profile-card is-red">
                <div class="demo-profile-tag">Verifikasi klaim · 0/4 data</div>
                <h3>Tirta Wahyu</h3>
                <p>Skenario kontradiksi bukti yang diarahkan ke tinjauan manusia.</p>
            </article>
        </div>
        <div class="demo-guide-note">
            Seluruh identitas, data, skor, dan hasil pada prototipe merupakan simulasi akademik.
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(
        "Lihat profil demo",
        key="close_demo_guide",
        type="primary",
        width="stretch",
    ):
        close_demo_guide()
        st.rerun()


AVATAR_BY_NIK = {
    "3374010101010001": "geovany",
    "3374010101010002": "salma",
    "3374010101010003": "reva",
    "3374010101010004": "tirta",
}

# ============================================================
get_status = review_status

# Palet semantik
C_VI   = "#C2761A"   # Vi / kredit (amber institusional)
C_ESG  = "#0F9D6B"   # ESG (hijau)
C_FCS  = "#1D4ED8"   # Final Credit Score (biru)
C_INK  = "#0E1B33"

# ============================================================
# GEOSPATIAL INTELLIGENCE  (verifikasi objektif)
# ============================================================
def geo_status(g):
    # Sinyal verifikasi untuk human review, bukan keputusan kredit otomatis.
    if not g["building_verified"]:
        return ("suspicious","TINJAUAN VERIFIKASI FISIK","#DC2626","rgba(220,38,38,0.07)","rgba(220,38,38,0.30)",
                "Bangunan belum terdeteksi dalam radius simulasi. Kondisi ini memicu verifikasi lapangan dan tidak menjadi dasar penolakan otomatis.")
    if not g["claim_match"]:
        return ("inconsistent","TINJAUAN KONSISTENSI KLAIM","#C2761A","rgba(194,118,26,0.07)","rgba(194,118,26,0.30)",
                "Klaim aktivitas belum konsisten dengan indikator geospasial simulasi. Analis harus meminta bukti tambahan atau melakukan verifikasi lapangan.")
    return ("verified","TERVERIFIKASI","#0F9D6B","rgba(15,157,107,0.07)","rgba(15,157,107,0.28)",
            "Lokasi usaha terverifikasi secara objektif. Bangunan terdeteksi dan klaim lahan konsisten dengan citra satelit.")

def ndvi_palette(v):
    if v >= 0.6: return "#0F9D6B","Tinggi"
    if v >= 0.35: return "#C2761A","Sedang"
    return "#DC2626","Rendah"

def flood_palette(level):
    return {"Rendah":"#0F9D6B","Sedang":"#C2761A","Tinggi":"#DC2626"}.get(level,"#8A97AE")

def landuse_palette(cls):
    return {"agri":"#0F9D6B","mixed":"#5BA88A","urban":"#6D49C9","empty":"#DC2626"}.get(cls,"#8A97AE")

def meter_label(m):
    return f"{m/1000:.1f} km" if m >= 1000 else f"{int(m)} m"

def fmt4(value):
    """Format angka UI dengan maksimal empat desimal tanpa nol ekor."""
    return f"{float(value):.4f}".rstrip("0").rstrip(".")


# ============================================================
# TANGGAL INDONESIA
# ============================================================
_HARI  = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"]
_BULAN = ["","Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus","September","Oktober","November","Desember"]
def tanggal_id():
    n = datetime.datetime.now()
    return f"{_HARI[n.weekday()]}, {n.day} {_BULAN[n.month]} {n.year}"

# ============================================================
# EMBLEM (inline SVG, dipakai navbar + login)
# ============================================================
def emblem(size=44, uid="e0"):
    return f"""<svg viewBox="0 0 96 96" width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g{uid}" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E8841A"/><stop offset="100%" stop-color="#0F9D6B"/>
    </linearGradient>
  </defs>
  <rect x="16" y="16" width="64" height="64" rx="13" ry="13" transform="rotate(45 48 48)"
    fill="none" stroke="url(#g{uid})" stroke-width="5"/>
  <circle cx="30" cy="66" r="6.5" fill="#E8841A"/>
  <circle cx="48" cy="48" r="6.5" fill="#C2761A"/>
  <circle cx="66" cy="30" r="6.5" fill="#0F9D6B"/>
  <line x1="30" y1="66" x2="48" y2="48" stroke="url(#g{uid})" stroke-width="4.5" stroke-linecap="round"/>
  <line x1="48" y1="48" x2="66" y2="30" stroke="url(#g{uid})" stroke-width="4.5" stroke-linecap="round"/>
  <polyline points="59,23 68,23 68,32" fill="none" stroke="#0F9D6B" stroke-width="4.5"
    stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

# Ikon navigasi (inline SVG, currentColor)
NAV_SVG = {
    "dashboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.6"/><rect x="14" y="3" width="7" height="7" rx="1.6"/><rect x="14" y="14" width="7" height="7" rx="1.6"/><rect x="3" y="14" width="7" height="7" rx="1.6"/></svg>',
    "geospatial": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6-5.3-6-10a6 6 0 1 1 12 0c0 4.7-6 10-6 10Z"/><circle cx="12" cy="11" r="2.3"/></svg>',
    "detail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><rect x="4.5" y="3" width="15" height="18" rx="2.2"/><path d="M8.5 8h7M8.5 12h7M8.5 16h4.5"/></svg>',
    "math": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M17.5 5H7l5 7-5 7h10.5"/></svg>',
    "comparison": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3.5v17"/><rect x="3.5" y="7" width="6" height="10" rx="1.6"/><rect x="14.5" y="7" width="6" height="10" rx="1.6"/></svg>',
}

# ============================================================
# CHART FUNCTIONS
# ============================================================
def donut_chart(value, color, label, height=210):
    pct = value * 100
    fig = go.Figure()
    fig.add_trace(go.Pie(
        values=[pct, 100-pct], hole=0.78,
        marker=dict(colors=[color, '#E9EEF6'], line=dict(width=0)),
        textinfo='none', hoverinfo='none', direction='clockwise', sort=False, rotation=90,
    ))
    fig.add_annotation(text=f"<b>{value}</b>", x=0.5, y=0.52, showarrow=False,
        font=dict(size=27, color=C_INK, family='JetBrains Mono'), xref='paper', yref='paper')
    fig.add_annotation(text=label, x=0.5, y=0.34, showarrow=False,
        font=dict(size=10, color='#8A97AE', family='Plus Jakarta Sans'), xref='paper', yref='paper')
    fig.update_layout(showlegend=False, margin=dict(l=10,r=10,t=10,b=10),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=height)
    return fig

def radar_chart(values, labels, color_rgb, height=300):
    vals = [v/100 for v in values]
    vals_closed = vals + [vals[0]]
    labs_closed = labels + [labels[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_closed, theta=labs_closed, fill='toself',
        fillcolor=f'rgba({color_rgb},0.18)', line=dict(color=f'rgb({color_rgb})', width=2.5),
        marker=dict(size=7, color=f'rgb({color_rgb})'), hoverinfo='skip'))
    fig.update_layout(
        polar=dict(bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0,1], showticklabels=False,
                gridcolor='rgba(14,27,51,0.09)', linecolor='rgba(14,27,51,0.09)'),
            angularaxis=dict(gridcolor='rgba(14,27,51,0.10)', linecolor='rgba(14,27,51,0.10)',
                tickfont=dict(color='#51607A', size=12), rotation=90)),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False, margin=dict(l=40,r=40,t=40,b=40), height=height, dragmode=False)
    return fig

# ============================================================
# CSS — TEMA INSTITUSIONAL TERANG
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root{
  --bg:#E9EEF5; --surface:#FFFFFF; --surface-2:#F5F8FC; --surface-3:#EEF3F9;
  --ink:#0E1B33; --ink-2:#51607A; --ink-3:#93A1B8;
  --line:#E3E9F1; --line-2:#D6DEEA;
  --primary:#14306E; --primary-d:#0C1F4A; --accent:#1D4ED8;
  --vi:#C2761A; --vi-soft:#FBF1E2; --esg:#0F9D6B; --esg-soft:#E5F6EF; --fcs:#1D4ED8; --fcs-soft:#E7EDFC;
  --ok:#0F9D6B; --warn:#C2761A; --bad:#DC2626;
  --shadow-sm:0 1px 2px rgba(14,27,51,.04), 0 6px 18px rgba(14,27,51,.05);
  --shadow-md:0 2px 6px rgba(14,27,51,.06), 0 18px 40px rgba(14,27,51,.08);
  --shadow-lg:0 8px 24px rgba(14,27,51,.10), 0 40px 80px rgba(14,27,51,.12);
}

*, *::before, *::after { box-sizing:border-box; }
html, body, [class*="css"] { font-family:'Plus Jakarta Sans',sans-serif !important; color:var(--ink); }
html, body, #root { min-height:100vh !important; }
html{ scroll-behavior:smooth; }
.stApp{
  background:
    radial-gradient(1100px 560px at 10% -8%, rgba(20,48,110,.06), transparent 60%),
    radial-gradient(900px 480px at 102% -4%, rgba(15,157,107,.05), transparent 55%),
    linear-gradient(180deg,#F2F5FA 0%, #E7ECF4 100%) !important;
  position:relative; isolation:isolate; min-height:100vh !important;
  height:auto !important; overflow:visible !important;
}
.stApp::before{ content:""; position:fixed; width:460px; height:460px; right:-170px; top:26%; border-radius:50%;
  background:radial-gradient(circle,rgba(29,78,216,.09),rgba(29,78,216,0) 68%); pointer-events:none; z-index:-1; filter:blur(2px); }
.stApp::after{ content:""; position:fixed; width:360px; height:360px; left:-160px; bottom:3%; border-radius:50%;
  background:radial-gradient(circle,rgba(15,157,107,.07),rgba(15,157,107,0) 70%); pointer-events:none; z-index:-1; }
[data-testid="stAppViewContainer"]{
  background:transparent !important; min-height:100vh !important;
  height:auto !important; overflow:visible !important;
}
[data-testid="stMain"],[data-testid="stMainBlockContainer"]{ background:transparent !important; }
.stTextInput > div { background:transparent !important; }
[data-testid="stPlotlyChart"]{ background:transparent !important; }
#MainMenu, footer, header, .stDeployButton { visibility:hidden !important; display:none !important; }
[data-testid="collapsedControl"]{ display:none !important; }
section[data-testid="stSidebar"]{ display:none !important; }
.block-container{ max-width:1340px !important; padding:0 30px 60px !important; margin:0 auto !important; }

/* ======= TOP STRIP ======= */
.topstrip{
  display:flex; align-items:center; justify-content:space-between;
  background:linear-gradient(90deg,var(--primary-d),var(--primary));
  color:#fff; height:34px; padding:0 18px; border-radius:0 0 2px 2px;
  font-size:11.5px; font-weight:600; letter-spacing:.4px;
}
.topstrip .ts-id{ display:flex; align-items:center; gap:9px; color:rgba(255,255,255,.85); }
.topstrip .ts-seal{ width:14px;height:14px;border-radius:3px;background:linear-gradient(135deg,#E8841A,#0F9D6B); }
.topstrip .ts-right{ display:flex; align-items:center; gap:14px; color:rgba(255,255,255,.7); font-family:'JetBrains Mono',monospace; font-size:11px; }
.topstrip .ts-live{ display:flex; align-items:center; gap:6px; }
.dot-ok{ width:7px;height:7px;border-radius:50%;background:#34D399;box-shadow:0 0 0 3px rgba(52,211,153,.25); }

/* ======= NAVBAR ======= */
.navbar-logo{ display:flex; align-items:center; gap:12px; padding-top:8px; }
.navbar-logo .nl-emblem{ filter:drop-shadow(0 4px 10px rgba(20,48,110,.18)); }
.navbar-title{ font-size:16px; font-weight:800; color:var(--ink); letter-spacing:-.2px; line-height:1.05; }
.navbar-title .sub{ display:block; font-size:10px; font-weight:600; letter-spacing:1.4px; color:var(--ink-3); text-transform:uppercase; margin-top:2px; }
.user-chip{ display:flex; align-items:center; justify-content:flex-end; gap:10px; padding-top:12px; }
.user-chip .avatar{ width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,var(--primary),var(--accent));color:#fff;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:700; }
.user-chip .uc-meta{ text-align:right; line-height:1.15; }
.user-chip .uc-name{ font-size:13px;font-weight:700;color:var(--ink); }
.user-chip .uc-role{ font-size:11px;color:var(--ink-3);font-weight:500; }
.navline{ height:1px;background:var(--line);margin:0; }

/* ======= CARD ======= */
.card{
  background:var(--surface); border-radius:14px; padding:20px;
  border:1px solid var(--line); box-shadow:var(--shadow-sm); transition:box-shadow .25s ease, transform .25s ease, border-color .25s ease;
  position:relative; overflow:hidden;
}
.card::before{ content:""; position:absolute; inset:0 0 auto 0; height:2px; background:linear-gradient(90deg,transparent,var(--accent),transparent); opacity:0; transition:opacity .25s ease; }
.card:hover{ box-shadow:var(--shadow-md); transform:translateY(-2px); border-color:rgba(29,78,216,.18); }
.card:hover::before{ opacity:1; }
.card-title{ font-size:13px; font-weight:700; color:var(--ink); margin-bottom:16px; letter-spacing:-.1px; }

/* ======= DASHBOARD HERO ======= */
.hero-strip{ display:flex; align-items:center; justify-content:space-between; gap:18px; padding:15px 18px; margin:0 0 18px;
  border-radius:16px; background:linear-gradient(105deg,rgba(20,48,110,.97),rgba(29,78,216,.94) 64%,rgba(15,157,107,.90));
  color:#fff; box-shadow:0 14px 34px rgba(20,48,110,.18); position:relative; overflow:hidden; animation:fadeUp .5s ease-out both; }
.hero-strip::after{ content:""; position:absolute; width:240px; height:240px; right:-64px; top:-116px; border:1px solid rgba(255,255,255,.16); border-radius:50%; box-shadow:0 0 0 26px rgba(255,255,255,.04),0 0 0 52px rgba(255,255,255,.025); }
.hero-kicker{ font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:700; letter-spacing:1.6px; color:rgba(255,255,255,.66); text-transform:uppercase; margin-bottom:4px; }
.hero-caption{ font-size:13px; color:rgba(255,255,255,.92); line-height:1.45; }
.hero-caption b{ color:#fff; }
.hero-meta{ display:flex; align-items:center; gap:8px; flex-wrap:wrap; position:relative; z-index:1; }
.hero-pill{ padding:8px 11px; border-radius:10px; background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.18); font-family:'JetBrains Mono',monospace; font-size:10.5px; font-weight:700; white-space:nowrap; }
.hero-pill strong{ color:#fff; font-size:12px; }
.score-orbit{ border-radius:16px; transition:transform .3s ease, box-shadow .3s ease; }
.score-orbit:hover{ transform:translateY(-4px); box-shadow:0 16px 34px rgba(20,48,110,.12); }

/* ======= DEBTOR BAR ======= */
.debtor-bar{ padding:20px 2px 0; }
.debtor-name{ font-size:26px; font-weight:800; color:var(--ink); display:inline; letter-spacing:-.6px; }
.debtor-badge{ display:inline-block; padding:4px 12px; border-radius:999px; font-size:12px; font-weight:700; margin-left:12px; vertical-align:middle; }
.badge-thin{ background:var(--vi-soft); color:var(--vi); border:1px solid rgba(194,118,26,.25); }
.badge-rich{ background:var(--esg-soft); color:var(--esg); border:1px solid rgba(15,157,107,.25); }
.debtor-sub{ font-size:14px; color:var(--ink-2); margin-top:5px; }

/* ======= SEGMENTED BAR ======= */
.seg-row{ display:flex; align-items:center; gap:12px; margin-bottom:14px; }
.seg-label{ font-size:13px; font-weight:600; color:var(--ink-2); width:130px; flex-shrink:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.seg-track{ flex:1; height:7px; background:#EDF1F8; border-radius:4px; overflow:hidden; position:relative; }
.seg-fill{ height:100%; border-radius:4px; }
.seg-green { background:var(--esg); }
.seg-orange{ background:var(--vi); }
.seg-red   { background:var(--bad); }
.seg-score { font-family:'JetBrains Mono',monospace; font-size:14px; font-weight:700; width:38px; text-align:right; }

/* ======= FORMULA BAR ======= */
.formula-bar{
  background:linear-gradient(180deg,#fff,var(--surface-2)); border-radius:12px; padding:15px 22px;
  font-family:'JetBrains Mono',monospace; font-size:14.5px; margin-top:16px;
  border:1px solid var(--line); display:flex; align-items:center; gap:9px; box-shadow:var(--shadow-sm); flex-wrap:wrap;
}
.formula-bar .fop{ color:var(--ink-3); }

/* ======= RIGHT PANEL ======= */
.rp-section-title{ font-size:14px; font-weight:700; color:var(--ink); margin-bottom:14px; }
.rp-score-row{ display:flex; justify-content:space-between; align-items:center; padding:11px 0; border-bottom:1px solid var(--line); }
.rp-score-row:last-child{ border-bottom:none; }
.rp-score-label{ font-size:13px; color:var(--ink-2); font-weight:500; }
.rp-detail-row{ display:flex; justify-content:space-between; align-items:center; padding:9px 0; border-bottom:1px solid var(--line); }
.rp-detail-row:last-child{ border-bottom:none; }
.rp-detail-key{ font-size:12px; color:var(--ink-3); display:flex; align-items:center; gap:8px; }
.rp-detail-val{ font-size:12px; font-weight:600; color:var(--ink); }
.rp-map-addr{ font-size:11px; color:var(--ink-3); margin-top:8px; font-family:'JetBrains Mono',monospace; }

/* ======= MATH STEPS ======= */
.math-card{ background:var(--surface); border-radius:14px; padding:22px 28px; margin-bottom:14px; border:1px solid var(--line); box-shadow:var(--shadow-sm); }
.math-label{ font-size:13px; font-weight:800; letter-spacing:1.4px; text-transform:uppercase; margin-bottom:12px; }
.math-result-badge{ display:inline-block; border-radius:10px; padding:11px 18px; font-family:'JetBrains Mono',monospace; font-size:16px; font-weight:700; margin-top:12px; }
.badge-green { background:var(--esg-soft); color:var(--esg); border:1px solid rgba(15,157,107,.22); }
.badge-purple{ background:#EEEAFB; color:#6D49C9; border:1px solid rgba(109,73,201,.22); }
.badge-orange{ background:var(--vi-soft); color:var(--vi); border:1px solid rgba(194,118,26,.22); }
.badge-blue  { background:var(--fcs-soft); color:var(--fcs); border:1px solid rgba(29,78,216,.22); }
.katex{ font-size:1.32em !important; color:var(--ink) !important; }
.katex-display{ margin:14px 0 !important; }

/* ======= STATUS ======= */
.status-priority { color:var(--ok); font-weight:800; font-size:14px; }
.status-review{ color:var(--warn); font-weight:800; font-size:14px; }
.status-manual { color:var(--bad); font-weight:800; font-size:14px; }

/* ======= COMPARISON ======= */
.vs-badge{ width:48px;height:48px;border-radius:14px;background:var(--surface);display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:800;color:var(--ink-3);border:1px solid var(--line);box-shadow:var(--shadow-sm); }
.weight-bar-wrap{ border-radius:10px;overflow:hidden;height:42px;display:flex;margin:12px 0;border:1px solid var(--line); }
.weight-alpha{ display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:#fff; }
.weight-beta { display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono',monospace;font-size:13px;font-weight:700;color:var(--ink-2);background:var(--surface-3); }
.comp-score-box{ background:var(--surface-2);border-radius:10px;padding:13px 16px;border:1px solid var(--line); }
.comp-score-label{ font-size:10px;color:var(--ink-3);font-weight:700;margin-bottom:4px;letter-spacing:.5px;text-transform:uppercase; }
.comp-score-val{ font-family:'JetBrains Mono',monospace;font-size:22px;font-weight:800; }
.insight-card{ background:var(--surface);border-radius:14px;padding:18px 20px;border:1px solid var(--line);border-left:4px solid var(--esg);display:flex;align-items:flex-start;gap:14px;margin-top:16px;box-shadow:var(--shadow-sm); }
.soft-note{ margin-top:12px;padding:14px 18px;background:var(--surface-2);border-radius:12px;border:1px solid var(--line);border-left:3px solid var(--line-2);font-size:13px;color:var(--ink-2);line-height:1.7; }

/* ======= BUTTONS ======= */
.stButton > button[kind="primary"]{
  background:linear-gradient(135deg,var(--primary),var(--accent)) !important; color:#fff !important;
  border:none !important; border-radius:12px !important; font-family:'Plus Jakarta Sans',sans-serif !important;
  font-weight:800 !important; font-size:15px !important; height:52px !important; width:100% !important;
  box-shadow:0 8px 22px rgba(20,48,110,.28) !important; transition:all .18s ease !important; letter-spacing:.2px !important;
}
.stButton > button[kind="primary"]:hover{ transform:translateY(-2px) !important; box-shadow:0 12px 28px rgba(20,48,110,.34) !important; }
.stButton > button[kind="secondary"]{
  background:var(--surface) !important; color:var(--primary) !important; border:1px solid var(--line-2) !important;
  border-radius:10px !important; font-family:'Plus Jakarta Sans',sans-serif !important; font-weight:700 !important;
  font-size:13px !important; box-shadow:var(--shadow-sm) !important; transition:all .18s ease !important;
}
.stButton > button[kind="secondary"]:hover{ border-color:var(--accent) !important; color:var(--accent) !important; transform:translateY(-1px) !important; }
.stButton > button:focus-visible{ outline:3px solid rgba(29,78,216,.28) !important; outline-offset:3px !important; }

/* Inputs */
.stTextInput label{ color:var(--ink-2) !important; font-size:11px !important; font-weight:700 !important; letter-spacing:1.4px !important; text-transform:uppercase !important; }
.stTextInput > div > div > input{
  background:var(--surface) !important; border:1.5px solid var(--line-2) !important; color:var(--ink) !important;
  border-radius:11px !important; font-family:'JetBrains Mono',monospace !important; font-size:15px !important; padding:13px 16px !important;
  transition:all .18s ease !important;
}
.stTextInput > div > div > input:focus{ border-color:var(--accent) !important; box-shadow:0 0 0 4px rgba(29,78,216,.12) !important; }
.stTextInput > div > div > input::placeholder{ color:var(--ink-3) !important; }

/* ======= NAV — overlay buttons (transparan, klik) ======= */
.nav-overlay{ margin-top:-50px; position:relative; z-index:10; }
.nav-overlay .stButton > button{
  background:transparent !important; border:none !important; color:transparent !important; font-size:0 !important;
  height:46px !important; width:100% !important; padding:0 !important; margin:0 !important; box-shadow:none !important;
  cursor:pointer !important; position:relative !important; z-index:10 !important;
}
.nav-overlay .stButton > button:hover,.nav-overlay .stButton > button:focus{ background:transparent !important; border:none !important; box-shadow:none !important; transform:none !important; }

/* Generic */
.stProgress > div > div > div > div{ background:var(--accent) !important; }

/* ======= LOGIN ======= */
.auth-panel{
  background:linear-gradient(160deg,var(--primary-d) 0%,var(--primary) 60%,#1B3F86 100%);
  border-radius:22px; padding:46px 42px; min-height:560px; position:relative; overflow:hidden;
  box-shadow:var(--shadow-lg); color:#fff;
}
.auth-panel::before{ content:""; position:absolute; inset:0;
  background:radial-gradient(420px 280px at 88% 6%, rgba(15,157,107,.22), transparent 60%),
            radial-gradient(360px 260px at 4% 96%, rgba(232,132,26,.18), transparent 60%); }
.auth-panel::after{ content:""; position:absolute; inset:0; opacity:.5;
  background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
  background-size:34px 34px; mask-image:radial-gradient(ellipse at center,#000 35%,transparent 80%); }
.auth-panel > *{ position:relative; z-index:2; }
.auth-cred{ display:flex;gap:8px;flex-wrap:wrap;margin-top:18px; }
.auth-cred span{ font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;color:rgba(255,255,255,.9);background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.16);padding:6px 11px;border-radius:999px; }
[data-testid="stVerticalBlockBorderWrapper"]{ background:var(--surface) !important; border-radius:22px !important; border:1px solid var(--line) !important; box-shadow:var(--shadow-lg) !important; }
[data-testid="stVerticalBlockBorderWrapper"] > div[data-testid="stVerticalBlock"]{ padding:36px 32px !important; }
.demo-chip{ }

/* ======= DEMO ACCOUNT GUIDE ======= */
[data-testid="stDialog"] [role="dialog"]{
  max-height:calc(100dvh - 96px) !important;
  overflow-x:hidden !important;
  overflow-y:auto !important;
  color-scheme:light !important;
  color:#15213d !important;
  background:linear-gradient(145deg,rgba(255,255,255,.99),#edf4fa) !important;
  border:1px solid rgba(255,255,255,.96) !important;
  border-radius:28px !important;
  box-shadow:
    -10px -10px 24px rgba(255,255,255,.78),
    18px 24px 58px rgba(35,56,91,.22),
    inset 1px 1px 0 rgba(255,255,255,.92) !important;
  animation:demoGuideIn .28s cubic-bezier(.2,.75,.3,1) both;
}
[data-testid="stDialog"] [role="dialog"] > div{
  background:transparent !important;
}
[data-testid="stDialog"] [role="dialog"] button[aria-label="Close"]{
  color:#15213d !important;
  -webkit-text-fill-color:#15213d !important;
  background:rgba(255,255,255,.76) !important;
  border:1px solid rgba(21,33,61,.08) !important;
  border-radius:12px !important;
}
[data-testid="stDialog"] [role="dialog"] button[aria-label="Close"] svg{
  color:#15213d !important;
  fill:currentColor !important;
}
[data-testid="stDialog"] h2,
[data-testid="stDialog"] h3,
[data-testid="stDialog"] p{
  opacity:1 !important;
  visibility:visible !important;
}
[data-testid="stDialog"] [role="dialog"] > div > div:first-child h2{
  color:#15213d !important;
  -webkit-text-fill-color:#15213d !important;
  font-size:27px !important;
  font-weight:800 !important;
  line-height:1.25 !important;
}
.demo-guide-hero{
  position:relative;
  overflow:hidden;
  padding:21px 23px 20px;
  border:1px solid rgba(255,255,255,.92);
  border-radius:22px;
  background:
    radial-gradient(circle at 92% 12%,rgba(49,200,191,.20),transparent 30%),
    linear-gradient(135deg,#f8fbff,#eaf2fb);
  box-shadow:
    -5px -5px 12px rgba(255,255,255,.90),
    7px 9px 20px rgba(60,84,119,.12),
    inset 1px 1px 0 rgba(255,255,255,.90);
}
.demo-guide-hero::after{
  content:"";
  position:absolute;
  width:130px;
  height:130px;
  right:-58px;
  bottom:-72px;
  border-radius:50%;
  border:1px solid rgba(102,88,216,.16);
  box-shadow:0 0 0 18px rgba(102,88,216,.04),0 0 0 36px rgba(102,88,216,.025);
}
.demo-guide-kicker{
  margin-bottom:8px;
  color:#087a68 !important;
  font-family:'JetBrains Mono',monospace;
  font-size:11px;
  font-weight:800;
  letter-spacing:1.2px;
  text-transform:uppercase;
}
.demo-guide-hero h2{
  position:relative;
  z-index:1;
  margin:0 !important;
  max-width:620px;
  color:#15213d !important;
  -webkit-text-fill-color:#15213d !important;
  font-size:28px !important;
  font-weight:800 !important;
  line-height:1.18 !important;
  letter-spacing:-.55px !important;
}
.demo-guide-hero p{
  position:relative;
  z-index:1;
  max-width:640px;
  margin:10px 0 0 !important;
  color:#5e6f88 !important;
  -webkit-text-fill-color:#5e6f88 !important;
  font-size:15px !important;
  line-height:1.62 !important;
}
.demo-guide-flow{
  display:flex;
  align-items:center;
  justify-content:center;
  gap:10px;
  margin:18px 4px 16px;
  color:#52627b;
  -webkit-text-fill-color:#52627b;
  font-size:13px;
  font-weight:700;
}
.demo-guide-flow span{ display:flex;align-items:center;gap:6px;white-space:nowrap; }
.demo-guide-flow b{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  width:28px;
  height:28px;
  border-radius:8px;
  color:#fff;
  -webkit-text-fill-color:#fff;
  background:linear-gradient(135deg,#14306e,#6658d8);
  box-shadow:0 5px 10px rgba(70,62,173,.20);
}
.demo-guide-flow i{
  width:28px;
  height:1px;
  background:linear-gradient(90deg,#cbd5e3,#9dabbe);
}
.demo-guide-grid{
  display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));
  gap:11px;
}
.demo-profile-card{
  position:relative;
  overflow:hidden;
  min-height:132px;
  padding:17px 18px;
  border:1px solid rgba(255,255,255,.92);
  border-radius:18px;
  background:linear-gradient(145deg,#ffffff,#eef4fa);
  box-shadow:
    -4px -4px 10px rgba(255,255,255,.88),
    6px 8px 16px rgba(59,82,115,.11),
    inset 1px 1px 0 rgba(255,255,255,.84);
}
.demo-profile-card::before{
  content:"";
  position:absolute;
  inset:0 auto 0 0;
  width:4px;
  background:var(--demo-color);
}
.demo-profile-card.is-amber{ --demo-color:#c2761a; }
.demo-profile-card.is-teal{ --demo-color:#0f9d6b; }
.demo-profile-card.is-violet{ --demo-color:#6658d8; }
.demo-profile-card.is-red{ --demo-color:#c94a4a; }
.demo-profile-tag{
  color:var(--demo-color);
  -webkit-text-fill-color:var(--demo-color);
  font-family:'JetBrains Mono',monospace;
  font-size:10px;
  font-weight:800;
  letter-spacing:.45px;
  text-transform:uppercase;
}
.demo-profile-card h3{
  margin:7px 0 4px !important;
  color:#15213d !important;
  -webkit-text-fill-color:#15213d !important;
  font-size:16px !important;
  font-weight:800 !important;
  line-height:1.25 !important;
}
.demo-profile-card p{
  margin:0 !important;
  color:#66758d !important;
  -webkit-text-fill-color:#66758d !important;
  font-size:13px !important;
  line-height:1.48 !important;
}
.demo-guide-note{
  margin:14px 2px 4px;
  color:#71809a;
  -webkit-text-fill-color:#71809a;
  font-size:11.5px;
  line-height:1.5;
  text-align:center;
}
@keyframes demoGuideIn{
  from{ opacity:0;transform:translateY(10px) scale(.985); }
  to{ opacity:1;transform:translateY(0) scale(1); }
}

/* ======= ANIMATIONS ======= */
@keyframes fadeUp{ from{opacity:0;transform:translateY(18px);} to{opacity:1;transform:translateY(0);} }
@keyframes fadeIn{ from{opacity:0;} to{opacity:1;} }
@keyframes popIn{ 0%{opacity:0;transform:scale(.85);} 70%{transform:scale(1.03);} 100%{opacity:1;transform:scale(1);} }
@keyframes slideDown{ from{opacity:0;transform:translateY(-10px);} to{opacity:1;transform:translateY(0);} }
@keyframes slideRight{ from{opacity:0;transform:translateX(24px);} to{opacity:1;transform:translateX(0);} }
@keyframes floaty{ 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }

.topstrip{ animation:slideDown .4s ease-out both; }
.navbar-logo,.user-chip{ animation:fadeIn .5s ease-out both; }
.math-card{ animation:fadeUp .45s ease-out both; }
.insight-card,.soft-note{ animation:fadeUp .5s ease-out both; }
.debtor-bar{ animation:fadeUp .35s ease-out both; }
.formula-bar{ animation:fadeUp .5s ease-out both; animation-delay:.25s; animation-fill-mode:both; }
.auth-panel{ animation:slideDown .55s cubic-bezier(.2,.7,.3,1) both; }
[data-testid="stVerticalBlockBorderWrapper"]{ animation:slideRight .55s cubic-bezier(.2,.7,.3,1) both; animation-delay:.1s; }
.emblem-float{ animation:floaty 4.5s ease-in-out infinite; }

[data-testid="stPlotlyChart"]{ animation:popIn .65s cubic-bezier(.2,.8,.3,1.05) both; }
[data-testid="stPlotlyChart"]:nth-of-type(2){ animation-delay:.1s; }
[data-testid="stPlotlyChart"]:nth-of-type(3){ animation-delay:.2s; }

.rec-wrap{ animation:fadeUp .45s ease-out both; }
.rec-item{ animation:fadeUp .4s ease-out both; }
.hero-pill{ animation:popIn .55s cubic-bezier(.2,.8,.3,1.05) both; }
.hero-pill:nth-child(2){ animation-delay:.08s; } .hero-pill:nth-child(3){ animation-delay:.16s; }

.delay-1{ animation-delay:.08s !important; } .delay-2{ animation-delay:.16s !important; }
.delay-3{ animation-delay:.24s !important; } .delay-4{ animation-delay:.32s !important; } .delay-5{ animation-delay:.40s !important; }

/* ======= GEOSPATIAL ======= */
.geo-banner{ display:flex;align-items:center;gap:16px;border-radius:16px;padding:18px 22px;margin-bottom:18px;border:1px solid;animation:fadeUp .45s ease-out both; }
.geo-banner .gb-ico{ width:46px;height:46px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0; }
.geo-banner .gb-title{ font-size:16px;font-weight:800;letter-spacing:.3px; }
.geo-banner .gb-desc{ font-size:13px;color:var(--ink-2);line-height:1.55;margin-top:3px; }
.geo-vcard{ background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 16px 14px;height:100%;animation:fadeUp .45s ease-out both; }
.geo-vcard .vh{ display:flex;align-items:center;gap:8px;margin-bottom:10px; }
.geo-vcard .vh .vi-ico{ width:30px;height:30px;border-radius:9px;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0; }
.geo-vcard .vh .vt{ font-size:13px;font-weight:800;color:var(--ink); }
.geo-vcard .vbody{ font-size:12.5px;color:var(--ink-2);line-height:1.5; }
.geo-flag{ display:inline-flex;align-items:center;gap:6px;font-size:11px;font-weight:800;letter-spacing:.4px;padding:4px 10px;border-radius:999px;margin-top:8px; }
.geo-map-key{ display:flex;flex-wrap:wrap;gap:14px;margin-top:10px;font-size:11.5px;color:var(--ink-2); }
.geo-map-key span{ display:inline-flex;align-items:center;gap:6px; }
.geo-map-key i{ width:11px;height:11px;border-radius:3px;display:inline-block; }
.geo-var{ background:var(--surface);border:1px solid var(--line);border-radius:13px;padding:14px 15px;animation:fadeUp .4s ease-out both; }
.geo-var .gv-top{ display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:7px; }
.geo-var .gv-name{ font-size:12px;font-weight:700;color:var(--ink); }
.geo-var .gv-src{ font-size:9.5px;font-family:'JetBrains Mono',monospace;color:var(--ink-3);letter-spacing:.3px;text-transform:uppercase; }
.geo-var .gv-val{ font-family:'JetBrains Mono',monospace;font-size:23px;font-weight:700;letter-spacing:-.5px;line-height:1; }
.geo-var .gv-sub{ font-size:11px;color:var(--ink-2);margin-top:4px; }
.geo-var .gv-map{ font-size:10px;color:var(--ink-3);margin-top:9px;padding-top:8px;border-top:1px dashed var(--line-2); }
.geo-var .gv-map b{ color:var(--ink-2); }
.geo-link-row{ display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--line); }
.geo-link-row:last-child{ border-bottom:none; }
.geo-link-row .glr-var{ font-size:12.5px;font-weight:700;color:var(--ink);flex:1; }
.geo-link-row .glr-arrow{ color:var(--ink-3);font-size:13px; }
.geo-link-row .glr-tag{ font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:7px; }
.glr-5c{ background:rgba(194,118,26,0.10);color:#9A5D12; }
.glr-esg{ background:rgba(15,157,107,0.10);color:#0B7A53; }

@media (max-width:900px){
  .block-container{ padding-left:16px !important; padding-right:16px !important; }
  .hero-strip{ align-items:flex-start; flex-direction:column; }
  .hero-meta{ width:100%; }
  .hero-pill{ flex:1; text-align:center; }
}
@media (max-width:640px){
  .demo-guide-grid{ grid-template-columns:1fr; }
  .demo-guide-flow{ align-items:flex-start; flex-direction:column; }
  .demo-guide-flow i{ display:none; }
  [data-testid="stDialog"] [role="dialog"] > div > div:first-child h2{ font-size:23px !important; }
  .demo-guide-hero h2{ font-size:23px !important; }
  .demo-guide-hero p{ font-size:14px !important; }
  .demo-profile-card h3{ font-size:15px !important; }
  .demo-profile-card p{ font-size:12.5px !important; }
}
@media (prefers-reduced-motion:reduce){
  *, *::before, *::after{ animation-duration:.001ms !important; animation-iteration-count:1 !important; transition-duration:.001ms !important; scroll-behavior:auto !important; }
}
</style>
""", unsafe_allow_html=True)

# Presentation-only design system layer. The score engine remains unchanged.
st.markdown(design_styles(), unsafe_allow_html=True)

# Critical profile-card styles live in the main app as a cache-safe guard.
# Streamlit can keep imported presentation modules alive during hot reloads.
st.markdown(r"""
<style id="identity-card-guard">
.identity-card {
  position: relative !important;
  overflow: hidden !important;
  margin-bottom: 14px !important;
  padding: 14px 14px 16px !important;
  color: #15213d !important;
  -webkit-text-fill-color: #15213d !important;
  background: linear-gradient(145deg, rgba(255,255,255,.98), #eef4fa) !important;
  border: 1px solid rgba(255,255,255,.92) !important;
  border-radius: 26px !important;
  box-shadow: -7px -7px 16px rgba(255,255,255,.84), 10px 14px 30px rgba(49,72,105,.14), inset 1px 1px 0 rgba(255,255,255,.88) !important;
  text-align: center !important;
  opacity: 1 !important;
  visibility: visible !important;
  isolation: isolate !important;
}
.identity-card::before {
  content: '' !important;
  position: absolute !important;
  width: 190px !important;
  height: 190px !important;
  right: -98px !important;
  top: -102px !important;
  z-index: 0 !important;
  border-radius: 50% !important;
  background: radial-gradient(circle, rgba(18,169,131,.17), transparent 68%) !important;
  pointer-events: none !important;
}
.identity-card .identity-card-head,
.identity-card .identity-name,
.identity-card .identity-role,
.identity-card .identity-address,
.identity-card .identity-address-sub,
.identity-card .identity-note {
  position: relative !important;
  z-index: 2 !important;
  opacity: 1 !important;
  visibility: visible !important;
  filter: none !important;
  mix-blend-mode: normal !important;
}
.identity-card .identity-card-head {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 8px !important;
  margin-bottom: 12px !important;
  text-align: left !important;
}
.identity-card .identity-kicker {
  color: #5b4fc4 !important;
  -webkit-text-fill-color: #5b4fc4 !important;
  font-size: 9px !important;
  font-weight: 800 !important;
  letter-spacing: 1px !important;
  text-transform: uppercase !important;
  opacity: 1 !important;
}
.identity-card .identity-chip {
  padding: 5px 8px !important;
  color: #087a68 !important;
  -webkit-text-fill-color: #087a68 !important;
  background: #e5f6f1 !important;
  border: 1px solid #b9e7da !important;
  border-radius: 999px !important;
  font-size: 8.5px !important;
  font-weight: 800 !important;
  white-space: nowrap !important;
  opacity: 1 !important;
}
.identity-card .identity-avatar-wrap {
  position: relative !important;
  z-index: 2 !important;
  display: block !important;
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  aspect-ratio: 1 / 1 !important;
  margin: 0 0 16px !important;
  padding: 5px !important;
  overflow: hidden !important;
  border: 1px solid rgba(255,255,255,.96) !important;
  border-radius: 26px !important;
  background: linear-gradient(145deg, #ffffff, #dfe9f3) !important;
  box-shadow: 0 20px 38px rgba(20,43,95,.18), 0 7px 16px rgba(18,169,131,.10), inset 1px 1px 0 rgba(255,255,255,.92) !important;
}
.identity-card .identity-avatar,
.identity-card .identity-avatar-fallback {
  display: block !important;
  width: 100% !important;
  height: 100% !important;
  max-width: 100% !important;
  border-radius: 21px !important;
  object-fit: cover !important;
  object-position: center 34% !important;
  opacity: 1 !important;
  visibility: visible !important;
  clip-path: inset(0 round 21px) !important;
}
.identity-card .identity-name {
  color: #15213d !important;
  -webkit-text-fill-color: #15213d !important;
  font-size: 17px !important;
  font-weight: 800 !important;
  line-height: 1.25 !important;
}
.identity-card .identity-role,
.identity-card .identity-address {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 6px !important;
  margin-top: 7px !important;
  color: #4f6078 !important;
  -webkit-text-fill-color: #4f6078 !important;
  font-size: 11px !important;
  line-height: 1.45 !important;
}
.identity-card .identity-address {
  margin-top: 5px !important;
  color: #142b5f !important;
  -webkit-text-fill-color: #142b5f !important;
  font-weight: 700 !important;
}
.identity-card .identity-role .ui-icon,
.identity-card .identity-address .ui-icon {
  color: #0b8b72 !important;
  -webkit-text-fill-color: #0b8b72 !important;
  flex: 0 0 auto !important;
}
.identity-card .identity-address-sub {
  margin-top: 3px !important;
  color: #5e6f88 !important;
  -webkit-text-fill-color: #5e6f88 !important;
  font-size: 10px !important;
  line-height: 1.4 !important;
}
.identity-card .identity-note {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 5px !important;
  margin-top: 13px !important;
  padding-top: 11px !important;
  color: #5e6f88 !important;
  -webkit-text-fill-color: #5e6f88 !important;
  border-top: 1px solid #dce4ef !important;
  font-size: 9.5px !important;
  line-height: 1.45 !important;
}
.identity-card .identity-note .ui-icon {
  color: #5b4fc4 !important;
  -webkit-text-fill-color: #5b4fc4 !important;
  flex: 0 0 auto !important;
}
.identity-card--comparison .identity-avatar-wrap {
  max-width: 240px !important;
  margin-left: auto !important;
  margin-right: auto !important;
}
@media (max-width: 760px) {
  .identity-card { border-radius: 22px !important; }
  .identity-card .identity-avatar-wrap { border-radius: 22px !important; }
  .identity-card .identity-avatar,
  .identity-card .identity-avatar-fallback { border-radius: 17px !important; clip-path: inset(0 round 17px) !important; }
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HELPER: SEGMENTED BAR
# ============================================================
def seg_bar(label, score, max_score=100):
    pct = (score / max_score) * 100
    if score >= 70: cls = "seg-green"; col = C_ESG
    elif score >= 50: cls = "seg-orange"; col = C_VI
    else: cls = "seg-red"; col = "#DC2626"
    return f"""
    <div class="seg-row">
        <span class="seg-label">{label}</span>
        <div class="seg-track"><div class="seg-fill {cls}" style="width:{pct}%"></div></div>
        <span class="seg-score" style="color:{col}">{score/100:.2f}</span>
    </div>"""

def seg_bar_esg(icon, label, score):
    pct = score
    if score >= 70: cls = "seg-green"; col = C_ESG
    elif score >= 50: cls = "seg-orange"; col = C_VI
    else: cls = "seg-red"; col = "#DC2626"
    return f"""
    <div class="seg-row">
        <span class="seg-label"><b style="color:{col}">{icon}</b>&nbsp; {label}</span>
        <div class="seg-track"><div class="seg-fill {cls}" style="width:{pct}%"></div></div>
        <span class="seg-score" style="color:{col}">{score/100:.2f}</span>
    </div>"""


def avatar_data_uri(avatar_key):
    """Load a local synthetic avatar as a self-contained data URI."""
    avatar_path = APP_DIR / "assets" / "avatars" / f"{avatar_key}.webp"
    if not avatar_path.exists():
        return ""
    encoded = base64.b64encode(avatar_path.read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def profile_card_html(d, avatar_key, extra_class=""):
    """Build the visual debtor profile without exposing sensitive identity data."""
    avatar_src = avatar_data_uri(avatar_key)
    safe_name = escape(d["nama"])
    initials = "".join(part[0] for part in d["nama"].split()[:2]).upper()
    if avatar_src:
        avatar_markup = f'<img class="identity-avatar" src="{avatar_src}" alt="Avatar sintetis {safe_name}" loading="eager" style="display:block;width:100%;height:100%;object-fit:cover;object-position:center 34%;border-radius:21px;opacity:1;visibility:visible">'
    else:
        avatar_markup = f'<div class="identity-avatar-fallback" aria-label="Inisial {safe_name}">{escape(initials)}</div>'
    class_name = f" identity-card{extra_class}" if extra_class else " identity-card"
    return f"""
    <div class="{class_name.strip()}" style="position:relative;overflow:hidden;padding:14px;border-radius:26px;background:linear-gradient(145deg,#ffffff,#eef4fa);color:#15213d;-webkit-text-fill-color:#15213d;opacity:1;visibility:visible;box-shadow:0 14px 30px rgba(49,72,105,.14)">
        <div class="identity-card-head" style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px;opacity:1;visibility:visible">
            <span class="identity-kicker" style="color:#5b4fc4;-webkit-text-fill-color:#5b4fc4;opacity:1">Profil debitur</span>
            <span class="identity-chip" style="color:#087a68;-webkit-text-fill-color:#087a68;background:#e5f6f1;border:1px solid #b9e7da;border-radius:999px;opacity:1">Avatar sintetis</span>
        </div>
        <div class="identity-avatar-wrap" style="display:block;width:100%;height:auto;aspect-ratio:1/1;margin:0 0 16px;padding:5px;overflow:hidden;border-radius:26px;background:linear-gradient(145deg,#ffffff,#dfe9f3);box-shadow:0 20px 38px rgba(20,43,95,.18),0 7px 16px rgba(18,169,131,.10)">{avatar_markup}</div>
        <div class="identity-name" style="color:#15213d;-webkit-text-fill-color:#15213d;font-weight:800;opacity:1;visibility:visible">{safe_name}</div>
        <div class="identity-role" style="color:#4f6078;-webkit-text-fill-color:#4f6078;opacity:1;visibility:visible">{icon("briefcase", 14)}<span>{escape(d["usaha"])}</span></div>
        <div class="identity-address" style="color:#142b5f;-webkit-text-fill-color:#142b5f;opacity:1;visibility:visible">{icon("geospatial", 14)}<span>{escape(d["lokasi"])}</span></div>
        <div class="identity-address-sub" style="color:#5e6f88;-webkit-text-fill-color:#5e6f88;opacity:1;visibility:visible">{escape(d["alamat"])}</div>
        <div class="identity-note" style="color:#5e6f88;-webkit-text-fill-color:#5e6f88;opacity:1;visibility:visible">{icon("info", 12)} Foto sintetis untuk demonstrasi, bukan data biometrik.</div>
    </div>
    """

# ============================================================
# HELPER: NAVBAR
# ============================================================
def render_navbar(active_view, show_logout=True):
    st.markdown(f"""
    <div class="topstrip">
        <div class="ts-id"><span class="ts-seal"></span>SISTEM PENILAIAN KREDIT UMKM BERBASIS ESG &amp; GEOSPASIAL</div>
        <div class="ts-right"><span>{tanggal_id()}</span><span class="ts-live"><span class="dot-ok"></span>SISTEM AKTIF</span></div>
    </div>
    """, unsafe_allow_html=True)

    nav_items = [
        ("dashboard", "Dashboard"),
        ("geospatial","Geospatial"),
        ("detail",    "Detail"),
        ("math",      "Math"),
        ("comparison","Perbandingan"),
    ]
    nb_l, nb_c, nb_r = st.columns([2.3, 5, 2.2])
    with nb_l:
        st.markdown(
            f'<div class="navbar-logo"><span class="nl-emblem">{emblem(40,"nav")}</span>'
            f'<span class="navbar-title">BCS-ESG <span style="color:var(--ui-violet)">Command Center</span><span class="sub">Credit Scoring Authority</span></span></div>',
            unsafe_allow_html=True)
    with nb_c:
        nav_html = '<div class="nav-menu">'
        for key, label in nav_items:
            is_active = active_view == key
            state = "is-active" if is_active else ""
            nav_html += f'<div class="nav-item {state}"><span class="nav-icon">{icon(key, 17)}</span><span>{label}</span></div>'
        nav_html += '</div>'
        st.markdown(nav_html, unsafe_allow_html=True)
        btn_cols = st.columns(5)
        for i, (key, label) in enumerate(nav_items):
            with btn_cols[i]:
                st.markdown('<div class="nav-overlay">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{key}", width="stretch"):
                    st.session_state.view = key
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
    with nb_r:
        uc1, uc2 = st.columns([1.3, 1])
        with uc1:
            st.markdown(
                f'<div class="user-chip"><div class="uc-meta"><div class="uc-name">Petugas Analis</div>'
                f'<div class="uc-role">Unit Penilaian Kredit</div></div><div class="avatar">{icon("user", 17)}</div></div>',
                unsafe_allow_html=True)
        with uc2:
            st.markdown('<div style="padding-top:14px">', unsafe_allow_html=True)
            if show_logout and st.button("Keluar", key="logout_top", type="secondary", width="stretch"):
                st.session_state.page = "login"
                st.session_state.res = None
                st.session_state.view = "dashboard"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="navline"></div>', unsafe_allow_html=True)


# ============================================================
# HELPER: RIGHT PANEL
# ============================================================
def render_right_panel(d, vi, esg, fcs, thin):
    sk, _ = get_status(fcs)
    lat, lng = d["lat"], d["lng"]

    st.markdown(f"""
    <div class="card" style="margin-bottom:12px">
        <div class="rp-section-title">Ringkasan Skor</div>
        <div class="rp-score-row"><span class="rp-score-label">TOPSIS Kredit</span><span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{C_VI};font-size:16px">{vi}</span></div>
        <div class="rp-score-row"><span class="rp-score-label">TOPSIS ESG</span><span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{C_ESG};font-size:16px">{esg}</span></div>
        <div class="rp-score-row"><span class="rp-score-label">TOPSIS Terintegrasi</span><span style="font-family:JetBrains Mono,monospace;font-weight:700;color:{C_FCS};font-size:16px">{fcs}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="margin-bottom:12px">
        <div class="rp-section-title">Detail Debitur</div>
        <div class="rp-detail-row"><span class="rp-detail-key">Identitas</span><span class="rp-detail-val">{d['id_type']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">Nomor identitas</span><span class="rp-detail-val">{d['id_no']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">Tanggal lahir</span><span class="rp-detail-val">{d['tgl_lahir']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">Alamat</span><span class="rp-detail-val">{d['alamat']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">Jenis usaha</span><span class="rp-detail-val">{d['usaha']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">Sejak</span><span class="rp-detail-val">{d['sejak']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="rp-section-title" style="margin-top:4px">Lokasi Usaha</div>', unsafe_allow_html=True)
    mini = folium.Map(location=[lat,lng], zoom_start=13,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", zoom_control=False, scrollWheelZoom=False, dragging=False, attributionControl=False)
    folium.Marker(location=[lat,lng], icon=folium.Icon(color="green", icon="home", prefix="fa")).add_to(mini)
    st_folium(mini, width=None, height=160, returned_objects=[])
    st.markdown(f'<div class="rp-map-addr">{d["lokasi"]}<br>Lat {lat:.4f}, Long {lng:.4f}</div>', unsafe_allow_html=True)

# ============================================================
# Visual refresh: audit rail replaces the older presentation helper above.
# The duplicate definition is intentional so the scoring and map logic stay
# isolated while the UI can evolve safely.
def render_right_panel(d, vi, esg, fcs, thin, avatar_key="geovany"):
    sk, _ = get_status(fcs)
    lat, lng = d["lat"], d["lng"]
    coverage = int(sum(bool(value) for value in d["data_availability"].values()) / 4 * 100)
    status_color = C_ESG if sk == "priority" else C_VI if sk == "review" else "#DC2626"
    status_label = "Prioritas evaluasi" if sk == "priority" else "Tinjauan lanjutan" if sk == "review" else "Tinjauan manual"

    st.markdown(profile_card_html(d, avatar_key), unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card audit-rail" style="margin-bottom:12px">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px">
            <div class="rp-section-title" style="margin:0">Audit snapshot</div>
            <span style="color:{status_color};display:inline-flex;align-items:center;gap:5px;font-size:10px;font-weight:800;text-transform:uppercase;letter-spacing:.7px">{icon("activity", 13)} {status_label}</span>
        </div>
        <div class="rp-score-row"><span class="rp-score-label"><span class="score-dot" style="background:{C_VI}"></span>TOPSIS Kredit</span><span style="color:{C_VI};font-size:16px">{vi}</span></div>
        <div class="rp-score-row"><span class="rp-score-label"><span class="score-dot" style="background:{C_ESG}"></span>TOPSIS ESG</span><span style="color:{C_ESG};font-size:16px">{esg}</span></div>
        <div class="rp-score-row"><span class="rp-score-label"><span class="score-dot" style="background:{C_FCS}"></span>TOPSIS Terintegrasi</span><span style="color:{C_FCS};font-size:16px">{fcs}</span></div>
        <div style="margin-top:14px;padding-top:13px;border-top:1px solid var(--ui-line)">
            <div style="display:flex;justify-content:space-between;align-items:center;font-size:11px;color:var(--ui-muted);margin-bottom:7px"><span>Data coverage</span><b style="font-family:'Fira Code',monospace;color:var(--ui-ink)">{coverage}%</b></div>
            <div style="height:6px;border-radius:99px;background:#edf1f7;overflow:hidden"><div style="height:100%;width:{coverage}%;background:linear-gradient(90deg,{C_FCS},{C_ESG});border-radius:99px"></div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="margin-bottom:12px">
        <div class="rp-section-title">Detail Debitur</div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("shield", 14)} Jenis Identitas</span><span class="rp-detail-val">{d['id_type']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("lock", 14)} No. Identitas</span><span class="rp-detail-val">{d['id_no']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("calendar", 14)} Tanggal Lahir</span><span class="rp-detail-val">{d['tgl_lahir']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("geospatial", 14)} Alamat</span><span class="rp-detail-val">{d['alamat']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("briefcase", 14)} Jenis Usaha</span><span class="rp-detail-val">{d['usaha']}</span></div>
        <div class="rp-detail-row"><span class="rp-detail-key">{icon("clock", 14)} Sejak</span><span class="rp-detail-val">{d['sejak']}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div class="rp-section-title" style="margin-top:4px;display:flex;align-items:center;gap:7px">{icon("geospatial", 15)} Lokasi Usaha</div>', unsafe_allow_html=True)
    mini = folium.Map(location=[lat, lng], zoom_start=13,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", zoom_control=False, scrollWheelZoom=False, dragging=False, attributionControl=False)
    folium.Marker(location=[lat, lng], icon=folium.Icon(color="green", icon="building", prefix="fa")).add_to(mini)
    st_folium(mini, width=None, height=160, returned_objects=[])
    st.markdown(f'<div class="rp-map-addr">{d["lokasi"]}<br><span style="color:var(--ui-subtle)">Lat {lat:.4f}, Long {lng:.4f}</span></div>', unsafe_allow_html=True)


# ============================================================
# ======== HALAMAN LOGIN ========
# ============================================================
if st.session_state.page == "login":
    # Restored framing from the first split-screen version.
    st.markdown('<style>.block-container{padding:32px 28px 34px !important}</style>', unsafe_allow_html=True)
    if not st.session_state.demo_guide_seen or st.session_state.demo_guide_requested:
        render_demo_guide()

    fcol, _gap, artcol = st.columns([0.92, 0.05, 1.12], gap="small")

    with fcol:
        with st.container(border=True):
            st.markdown(f"""
            <div class="login-form-intro">
                <div class="login-brand-row">
                    <span class="login-brand-mark">{emblem(34,"login-brand")}</span>
                    <div>
                        <div class="login-brand-name" style="color:#142b5f !important">BCS-ESG Command Center</div>
                        <div class="login-brand-role" style="color:#71809a !important">Credit Scoring Authority</div>
                    </div>
                </div>
                <div class="login-kicker" style="color:#0b8b72 !important">Portal analis / secure review</div>
                <div class="login-title" style="color:#15213d !important">Mulai dari <em style="color:#6658d8 !important;font-style:normal">bukti.</em></div>
                <div class="login-description" style="color:#5e6f88 !important">Masuk untuk meninjau profil UMKM dengan pendekatan 5C, ESG, dan verifikasi geospasial yang lebih kontekstual.</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="login-field-label" style="color:#15213d !important">NIK Debitur</div>', unsafe_allow_html=True)
            nik = st.text_input("NIK Debitur", placeholder="Masukkan 16 digit NIK", key="login_nik", label_visibility="collapsed")
            st.markdown('<div class="login-field-hint" style="color:#71809a !important">Gunakan NIK simulasi untuk membuka workspace penilaian.</div>', unsafe_allow_html=True)

            if st.button("Masuk ke Sistem", key="btn_login", type="primary", width="stretch"):
                if nik in DB:
                    st.session_state.page = "loading"
                    st.session_state.load_step = 0
                    st.session_state.pending_nik = nik
                    st.rerun()
                elif nik:
                    st.markdown(f'<div class="login-feedback is-error">{icon("x", 15)}<span>NIK tidak ditemukan dalam basis data.</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="login-feedback is-warning">{icon("alert", 15)}<span>Masukkan NIK terlebih dahulu.</span></div>', unsafe_allow_html=True)

            st.markdown(f'<div class="login-meta-row" style="color:#5e6f88 !important">{icon("lock", 14)} <span>Data simulasi tersimpan lokal dan keputusan akhir tetap berada pada analis manusia.</span></div>', unsafe_allow_html=True)
            if st.button("Panduan akun demo", key="open_demo_guide", type="secondary", width="stretch"):
                st.session_state.demo_guide_requested = True
                st.rerun()
            st.markdown('<div class="login-divider" style="color:#8796aa !important">Profil simulasi</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-demo-title" style="color:#5e6f88 !important">Pilih salah satu profil untuk mencoba alur penilaian tanpa memasukkan NIK manual.</div>', unsafe_allow_html=True)

            for key_nik, info in DB.items():
                is_thin, available = classify_pathway(info)
                tag = f"Data-Thin · {available}/4 data" if is_thin else f"Data-Rich · {available}/4 data"
                if st.button(f"{info['nama']}  ·  {info['usaha']}  ·  {tag}", key=f"demo_{key_nik}", type="secondary", width="stretch"):
                    st.session_state.page = "loading"
                    st.session_state.load_step = 0
                    st.session_state.pending_nik = key_nik
                    st.rerun()

            st.markdown('<div class="login-legal" style="color:#8796aa !important">PROTOTIPE AKADEMIK · DATA SIMULASI · TIDAK UNTUK PRODUKSI</div>', unsafe_allow_html=True)

    with artcol:
        st.html(login_illustration_html(), unsafe_allow_javascript=True)

    # Final contrast guard: Streamlit theme or parent styles must not wash out
    # the login copy after the illustration component is mounted.
    st.markdown("""
    <style>
    .login-form-intro,
    .login-form-intro .login-brand-name,
    .login-form-intro .login-brand-role,
    .login-form-intro .login-kicker,
    .login-form-intro .login-title,
    .login-form-intro .login-description,
    .login-field-label,
    .login-field-hint,
    .login-meta-row,
    .login-divider,
    .login-demo-title,
    .login-legal {
        opacity: 1 !important;
        visibility: visible !important;
    }
    .login-form-intro .login-brand-name { color: #142b5f !important; -webkit-text-fill-color: #142b5f !important; }
    .login-form-intro .login-brand-role { color: #71809a !important; -webkit-text-fill-color: #71809a !important; }
    .login-form-intro .login-kicker { color: #0b8b72 !important; -webkit-text-fill-color: #0b8b72 !important; }
    .login-form-intro .login-title { color: #15213d !important; -webkit-text-fill-color: #15213d !important; }
    .login-form-intro .login-title em { color: #6658d8 !important; -webkit-text-fill-color: #6658d8 !important; }
    .login-form-intro .login-description { color: #5e6f88 !important; -webkit-text-fill-color: #5e6f88 !important; }
    .login-field-label { color: #15213d !important; -webkit-text-fill-color: #15213d !important; }
    .login-field-hint { color: #71809a !important; -webkit-text-fill-color: #71809a !important; }
    .login-meta-row { color: #5e6f88 !important; -webkit-text-fill-color: #5e6f88 !important; }
    .login-divider { color: #71809a !important; -webkit-text-fill-color: #71809a !important; }
    .login-demo-title { color: #5e6f88 !important; -webkit-text-fill-color: #5e6f88 !important; }
    .login-legal { color: #8796aa !important; -webkit-text-fill-color: #8796aa !important; }
    </style>
    """, unsafe_allow_html=True)

    st.stop()

    st.markdown('<style>.block-container{padding:48px 30px 40px !important}</style>', unsafe_allow_html=True)

    svg_pentagon = """<svg viewBox="0 0 340 250" xmlns="http://www.w3.org/2000/svg" width="100%" height="210">
      <polygon points="170,28 246,86 217,176 123,176 94,86"
        fill="rgba(255,255,255,0.05)" stroke="rgba(255,255,255,0.30)" stroke-width="1.5" stroke-dasharray="5,4"/>
      <circle cx="170" cy="28" r="22" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>
      <text x="170" y="33" text-anchor="middle" fill="#fff" font-size="9" font-weight="700">Character</text>
      <circle cx="246" cy="86" r="22" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>
      <text x="246" y="91" text-anchor="middle" fill="#fff" font-size="9" font-weight="700">Capacity</text>
      <circle cx="217" cy="176" r="22" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>
      <text x="217" y="181" text-anchor="middle" fill="#fff" font-size="9" font-weight="700">Capital</text>
      <circle cx="123" cy="176" r="22" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>
      <text x="123" y="181" text-anchor="middle" fill="#fff" font-size="9" font-weight="700">Condition</text>
      <circle cx="94" cy="86" r="22" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.35)" stroke-width="1.5"/>
      <text x="94" y="91" text-anchor="middle" fill="#fff" font-size="9" font-weight="700">Collateral</text>
      <line x1="170" y1="50" x2="170" y2="98" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="224" y1="96" x2="188" y2="110" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="206" y1="155" x2="185" y2="135" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="134" y1="155" x2="155" y2="135" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/>
      <line x1="116" y1="96" x2="152" y2="110" stroke="rgba(255,255,255,0.18)" stroke-width="1" stroke-dasharray="3,3"/>
      <circle cx="170" cy="112" r="26" fill="rgba(15,157,107,0.18)" stroke="rgba(52,211,153,0.55)" stroke-width="1.5"/>
      <text x="170" y="108" text-anchor="middle" fill="#5EEAB0" font-size="9" font-weight="800" font-family="monospace">BCS</text>
      <text x="170" y="120" text-anchor="middle" fill="#5EEAB0" font-size="9" font-weight="800" font-family="monospace">ESG</text>
    </svg>"""

    pcol, _gap, fcol = st.columns([1.05, 0.06, 0.95])

    # ----- Panel kiri (branding institusional) -----
    with pcol:
        st.markdown(f"""
        <div class="auth-panel">
            <div style="display:flex;align-items:center;gap:14px;margin-bottom:30px">
                <span class="emblem-float" style="filter:drop-shadow(0 6px 16px rgba(0,0,0,.3))">{emblem(52,"login")}</span>
                <div>
                    <div style="font-size:18px;font-weight:800;letter-spacing:-.3px">BCS-ESG System</div>
                    <div style="font-size:11px;font-weight:600;letter-spacing:1.6px;color:rgba(255,255,255,.6);text-transform:uppercase;margin-top:2px">Credit Scoring Authority</div>
                </div>
            </div>
            <div style="font-size:34px;font-weight:800;letter-spacing:-1px;line-height:1.15;margin-bottom:14px">
                Penilaian Kredit UMKM<br>yang Cerdas &amp; Berkelanjutan
            </div>
            <div style="font-size:14px;color:rgba(255,255,255,.72);line-height:1.7;max-width:430px">
                Platform pendukung penilaian kredit yang memadukan prinsip 5C, indikator ESG, dan data geospasial
                untuk prioritas evaluasi yang transparan. Keputusan akhir tetap berada pada analis manusia.
            </div>
            <div class="auth-cred">
                <span>POJK No. 29/2024</span><span>Contextual BWM</span><span>Cohort TOPSIS</span><span>Geospatial</span>
            </div>
            <div style="margin:22px auto 0;max-width:340px;opacity:.95">{svg_pentagon}</div>
            <div style="font-family:JetBrains Mono,monospace;font-size:10px;color:rgba(255,255,255,.4);letter-spacing:2px;margin-top:8px;text-align:center">
                UNIVERSITAS DIPONEGORO · SEMARANG · 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ----- Panel kanan (form) -----
    with fcol:
        with st.container(border=True):
            st.markdown("""
            <div style="margin-bottom:24px">
                <div style="font-size:12px;font-weight:700;letter-spacing:1.6px;color:var(--accent);text-transform:uppercase;margin-bottom:8px">Portal Masuk</div>
                <div style="font-size:30px;font-weight:800;color:var(--ink);letter-spacing:-.8px;margin-bottom:6px">Verifikasi Debitur</div>
                <div style="font-size:14px;color:var(--ink-2);line-height:1.6">Masukkan NIK debitur untuk memulai proses penilaian kredit.</div>
            </div>
            """, unsafe_allow_html=True)

            nik = st.text_input("NIK Debitur", placeholder="Masukkan 16 digit NIK", key="login_nik")
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)

            if st.button("Masuk ke Sistem  →", key="btn_login", type="primary", width="stretch"):
                if nik in DB:
                    st.session_state.page = "loading"
                    st.session_state.load_step = 0
                    st.session_state.pending_nik = nik
                    st.rerun()
                elif nik:
                    st.markdown(f'<p style="color:var(--bad);font-weight:700;font-size:13px;margin-top:10px;display:flex;align-items:center;gap:6px">{icon("x", 15)} NIK tidak ditemukan dalam basis data.</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="color:var(--warn);font-weight:700;font-size:13px;margin-top:10px;display:flex;align-items:center;gap:6px">{icon("alert", 15)} Masukkan NIK terlebih dahulu.</p>', unsafe_allow_html=True)

            # Akun demo (chip)
            st.markdown('<div style="margin:22px 0 10px;display:flex;align-items:center;gap:10px"><div style="flex:1;height:1px;background:var(--line)"></div><span style="font-size:11px;font-weight:700;letter-spacing:1.2px;color:var(--ink-3);text-transform:uppercase">Akun Demo</span><div style="flex:1;height:1px;background:var(--line)"></div></div>', unsafe_allow_html=True)

            for key_nik, info in DB.items():
                is_thin, available = classify_pathway(info)
                tag = f"Data-Thin · {available}/4 data" if is_thin else f"Data-Rich · {available}/4 data"
                if st.button(f"{info['nama']}  ·  {info['usaha']}  ·  {tag}", key=f"demo_{key_nik}", type="secondary", width="stretch"):
                    st.session_state.page = "loading"
                    st.session_state.load_step = 0
                    st.session_state.pending_nik = key_nik
                    st.rerun()

            st.markdown('<div style="text-align:center;font-family:JetBrains Mono,monospace;font-size:10px;color:var(--ink-3);margin-top:20px;letter-spacing:1px">PROTOTIPE AKADEMIK · TIDAK UNTUK PRODUKSI</div>', unsafe_allow_html=True)

# ============================================================
# ======== LOADING PAGE ========
# ============================================================
elif st.session_state.page == "loading":
    render_navbar("dashboard", show_logout=False)

    steps = [
        "Identitas terverifikasi",
        "Menurunkan bobot BWM sesuai jalur data",
        "Membentuk cohort pembanding yang setara",
        "Menghitung kedekatan ideal TOPSIS",
    ]
    prog_pct = [25, 50, 75, 100]
    step_idx = st.session_state.load_step

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        ring_dash   = 345.6
        ring_offset = ring_dash * (1 - prog_pct[min(step_idx, 3)] / 100)
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;align-items:center;padding-top:56px;padding-bottom:36px">
            <div style="position:relative;width:152px;height:152px;margin-bottom:30px">
                <svg viewBox="0 0 152 152" width="152" height="152">
                    <circle cx="76" cy="76" r="63" fill="none" stroke="#E3E9F1" stroke-width="10"/>
                    <circle cx="76" cy="76" r="63" fill="none" stroke="#1D4ED8" stroke-width="10"
                        stroke-dasharray="{ring_dash:.1f}" stroke-dashoffset="{ring_offset:.1f}"
                        stroke-linecap="round" transform="rotate(-90 76 76)" style="transition:stroke-dashoffset .5s ease"/>
                </svg>
                <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
                    width:96px;height:96px;background:#fff;border-radius:22px;border:1px solid var(--line);
                    box-shadow:var(--shadow-md);display:flex;align-items:center;justify-content:center">{emblem(54,"load")}</div>
            </div>
            <div style="font-size:25px;font-weight:800;color:var(--ink);margin-bottom:6px;letter-spacing:-.5px">Memproses Analisis</div>
            <div style="font-size:13px;color:var(--ink-2);margin-bottom:34px">Mohon tunggu, sistem sedang menghitung skor untuk prioritas evaluasi.</div>
        </div>
        """, unsafe_allow_html=True)

        for i, s in enumerate(steps):
            if i < step_idx:
                icon = '<div style="width:28px;height:28px;border-radius:50%;background:#0F9D6B;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:13px;color:#fff;font-weight:700">&#10003;</div>'
                txt  = f'<span style="font-size:15px;font-weight:600;color:var(--ink);font-family:Plus Jakarta Sans,sans-serif">{s}</span>'
            elif i == step_idx:
                icon = '<div style="width:28px;height:28px;border-radius:50%;border:2.5px solid #1D4ED8;background:rgba(29,78,216,.08);flex-shrink:0"></div>'
                txt  = f'<span style="font-size:15px;font-weight:700;color:var(--ink);font-family:Plus Jakarta Sans,sans-serif">{s}</span>'
            else:
                icon = '<div style="width:28px;height:28px;border-radius:50%;border:2px solid var(--line-2);flex-shrink:0"></div>'
                txt  = f'<span style="font-size:15px;font-weight:400;color:var(--ink-3);font-family:Plus Jakarta Sans,sans-serif">{s}</span>'
            st.markdown(f'<div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;max-width:340px;margin-left:auto;margin-right:auto">{icon}{txt}</div>', unsafe_allow_html=True)

    pct = prog_pct[min(step_idx, 3)]
    st.markdown(f"""
    <div style="position:fixed;bottom:0;left:0;right:0;height:3px;background:rgba(20,48,110,.10)">
        <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#14306E,#1D4ED8);border-radius:0 2px 2px 0;transition:width .4s ease"></div>
    </div>
    """, unsafe_allow_html=True)

    if step_idx < 4:
        time.sleep(0.7)
        st.session_state.load_step += 1
        st.rerun()
    else:
        nik = st.session_state.pending_nik
        d = DB[nik]
        cohort_result = score_debtor_cohort(DB)[nik]
        alpha, beta = cohort_result["top_weights"]
        st.session_state.res = {
            "nik": nik, "d": d, **cohort_result,
            "alpha": float(alpha), "beta": float(beta),
        }
        st.session_state.load_step = 0
        st.session_state.page = "dashboard"
        st.session_state.view = "dashboard"
        st.rerun()

# ============================================================
# ======== DASHBOARD ========
# ============================================================
elif st.session_state.page == "dashboard":
    r=st.session_state.res; d=r["d"]; vi=r["vi"]; esg=r["esg"]; fcs=r["fcs"]
    alpha=r["alpha"]; beta=r["beta"]; thin=r["thin"]
    avatar_key=AVATAR_BY_NIK.get(r["nik"], "geovany")
    esg_values=r["esg_values"]
    sk,stxt=get_status(fcs); wv=r["wv"]
    K=["Character","Capacity","Capital","Condition","Collateral"]
    E_labels=["Environmental","Social","Governance"]; EW=r["esg_weights"]
    bc="badge-thin" if thin else "badge-rich"
    bt="Data-Thin" if thin else "Data-Rich"
    st_col=C_ESG if sk=="priority" else C_VI if sk=="review" else "#DC2626"

    render_navbar(st.session_state.view)

    # FORMULA bar (dipakai ulang)
    def formula_html():
        return (f'<div class="formula-bar"><span style="font-size:17px">C</span>'
                f'<span class="fop">TOPSIS C =</span><span style="color:{C_ESG};font-weight:700">D− {r["distance_negative"]:.4f}</span>'
                f'<span class="fop">/</span><span style="color:{C_VI};font-weight:700">(D+ {r["distance_positive"]:.4f} + D− {r["distance_negative"]:.4f})</span>'
                f'<span class="fop">=</span><span style="color:{C_FCS};font-weight:800">{fcs}</span>'
                f'<span class="fop">· Peringkat {r["rank"]}/{r["cohort_size"]} jalur</span></div>')

    # Clean SVG version used by the refreshed interface.
    def formula_html():
        return (f'<div class="formula-bar"><span style="color:var(--ui-violet);display:inline-flex">{icon("math", 17)}</span>'
                f'<span class="fop">TOPSIS C =</span><span style="color:{C_ESG};font-weight:700">D- {r["distance_negative"]:.4f}</span>'
                f'<span class="fop">/</span><span style="color:{C_VI};font-weight:700">(D+ {r["distance_positive"]:.4f} + D- {r["distance_negative"]:.4f})</span>'
                f'<span class="fop">=</span><span style="color:{C_FCS};font-weight:800">{fcs}</span>'
                f'<span class="fop">&middot; Peringkat {r["rank"]}/{r["cohort_size"]} jalur</span></div>')

    # ============ VIEW: DASHBOARD ============
    if st.session_state.view == "dashboard":
        main_col, rp_col = st.columns([3.2, 1], gap="medium")
        with main_col:
            st.markdown(f'''
            <div class="workspace-head">
                <div><div class="eyebrow">Underwriting workspace / live review</div><div class="headline">Evidence-led credit intelligence for sustainable MSMEs</div></div>
                <div class="meta"><span class="workspace-tag">{icon("database", 13)} Simulasi terkendali</span><span class="workspace-tag">{icon("shield", 13)} Human-in-the-loop</span></div>
            </div>
            ''', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="debtor-bar">
                <span class="debtor-name">{d['nama']}</span>
                <span class="debtor-badge {bc}">{bt}</span>
                <div class="debtor-sub">{d['usaha']} · {d['lokasi']}</div>
            </div>
            <div style="height:16px"></div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="hero-strip">
                <div>
                    <div class="hero-kicker">Live cohort analysis · proof-of-concept</div>
                    <div class="hero-caption">Profil berada pada <b>peringkat {r['rank']} dari {r['cohort_size']}</b> pemohon di jalur {bt}. Keputusan akhir tetap melalui tinjauan analis.</div>
                </div>
                <div class="hero-meta">
                    <span class="hero-pill">BWM <strong>{r['bwm_profile'].replace('data_', '')}</strong></span>
                    <span class="hero-pill">Cohort <strong>{r['cohort_size']}</strong></span>
                    <span class="hero-pill">Review <strong>Human-in-loop</strong></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            dc1, dc2, dc3 = st.columns(3, gap="medium")
            with dc1:
                st.markdown('<div class="card score-orbit" style="text-align:center">', unsafe_allow_html=True)
                st.plotly_chart(donut_chart(vi, C_VI, "KREDIT"), width="stretch", config={"displayModeBar":False})
                st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.4px;color:var(--ink-3);text-transform:uppercase;margin-top:-10px;padding-bottom:8px">TOPSIS KREDIT</div></div>', unsafe_allow_html=True)
            with dc2:
                st.markdown('<div class="card score-orbit" style="text-align:center">', unsafe_allow_html=True)
                st.plotly_chart(donut_chart(esg, C_ESG, "ESG"), width="stretch", config={"displayModeBar":False})
                st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.4px;color:var(--ink-3);text-transform:uppercase;margin-top:-10px;padding-bottom:8px">TOPSIS ESG</div></div>', unsafe_allow_html=True)
            with dc3:
                st.markdown('<div class="card score-orbit" style="text-align:center">', unsafe_allow_html=True)
                st.plotly_chart(donut_chart(fcs, C_FCS, "INTEGRATED"), width="stretch", config={"displayModeBar":False})
                st.markdown(f'<div style="font-size:11px;font-weight:700;letter-spacing:1.4px;color:var(--ink-3);text-transform:uppercase;margin-top:-10px">TOPSIS TERINTEGRASI</div><div class="status-{sk}" style="margin:6px 0 8px">{"✓ " if sk=="priority" else ""}{stxt}</div></div>', unsafe_allow_html=True)

            dd1, dd2 = st.columns(2, gap="medium")
            with dd1:
                bars = "".join([seg_bar(K[i], d["5C"][i]) for i in range(5)])
                st.markdown(f'<div class="card"><div class="card-title">Penilaian 5C</div>{bars}</div>', unsafe_allow_html=True)
            with dd2:
                esg_bars = "".join([seg_bar_esg(["E","S","G"][i], E_labels[i], esg_values[i]) for i in range(3)])
                st.markdown(f'<div class="card"><div class="card-title">ESG Dimensions</div>{esg_bars}</div>', unsafe_allow_html=True)

            # ====== REKOMENDASI ======
            recs = []
            scores_5c = dict(zip(K, d["5C"]))
            esg_scores = dict(zip(E_labels, esg_values))
            if scores_5c["Collateral"] < 50:
                recs.append(("alert","TINGGI","#DC2626","rgba(220,38,38,0.07)","rgba(220,38,38,0.30)","Agunan Lemah","Siapkan agunan fisik seperti BPKB kendaraan atau sertifikat tanah. Skor Collateral di bawah 50 meningkatkan risiko kredit secara signifikan."))
            if esg_scores["Governance"] < 70:
                recs.append(("alert","TINGGI","#DC2626","rgba(220,38,38,0.07)","rgba(220,38,38,0.30)","Bukti Tata Kelola Belum Lengkap","Lengkapi legalitas usaha dan dokumen tata kelola yang relevan. Skor Governance rendah menjadi alasan permintaan bukti tambahan, bukan penolakan otomatis."))
            if scores_5c["Capacity"] < 65:
                recs.append(("activity","SEDANG","#C2761A","rgba(194,118,26,0.07)","rgba(194,118,26,0.28)","Kapasitas Usaha Perlu Diperkuat","Lengkapi laporan arus kas 3 bulan terakhir dan bukti omzet usaha. Dokumentasi yang lengkap dapat meningkatkan skor Capacity secara signifikan."))
            if scores_5c["Capital"] < 65:
                recs.append(("activity","SEDANG","#C2761A","rgba(194,118,26,0.07)","rgba(194,118,26,0.28)","Modal Usaha Terbatas","Catat aset usaha secara formal. Peralatan, stok, dan aset tetap yang terdaftar dapat meningkatkan skor Capital."))
            if esg_scores["Environmental"] < 65:
                recs.append(("activity","SEDANG","#C2761A","rgba(194,118,26,0.07)","rgba(194,118,26,0.28)","Skor Lingkungan Rendah","NDVI Score menunjukkan aktivitas lahan rendah. Pertimbangkan praktik usaha ramah lingkungan untuk meningkatkan skor Environmental."))
            if scores_5c["Character"] < 70:
                recs.append(("clock","RENDAH","#D9A007","rgba(217,160,7,0.08)","rgba(217,160,7,0.28)","Riwayat Kredit Perlu Diperbaiki","Pastikan semua kewajiban cicilan dibayar tepat waktu. Riwayat pembayaran yang konsisten meningkatkan skor Character."))
            if esg_scores["Social"] < 65:
                recs.append(("clock","RENDAH","#D9A007","rgba(217,160,7,0.08)","rgba(217,160,7,0.28)","Modal Sosial Perlu Ditingkatkan","Bergabunglah dengan koperasi atau BUMDes setempat. Keterlibatan komunitas aktif meningkatkan skor Social secara signifikan."))
            if fcs >= 0.75:
                recs.insert(0, ("check","INFO","#0F9D6B","rgba(15,157,107,0.07)","rgba(15,157,107,0.28)","Prioritas Evaluasi Tinggi",f"Skor FCS {fcs} menempatkan profil pada prioritas evaluasi. Analis tetap memeriksa bukti, kebijakan kredit, dan risiko sebelum mengambil keputusan."))
            if not recs:
                recs.append(("check","INFO","#0F9D6B","rgba(15,157,107,0.07)","rgba(15,157,107,0.28)","Semua Indikator Dalam Batas Aman","Profil kredit debitur memenuhi semua standar minimum BCS-ESG. Tidak ada perbaikan mendesak yang diperlukan saat ini."))
            priority_order = {"TINGGI":0,"SEDANG":1,"RENDAH":2,"INFO":3}
            recs.sort(key=lambda x: priority_order.get(x[1], 4))
            recs = recs[:4]
            st.markdown(f'<div class="rec-wrap card" style="border-left:4px solid {C_VI};padding:22px 24px 14px;margin-top:16px"><div style="display:flex;align-items:center;gap:10px;margin-bottom:18px"><span style="font-size:17px;font-weight:800;color:var(--ink);letter-spacing:-.2px">Rekomendasi Peningkatan Skor</span><span style="font-size:11px;background:var(--vi-soft);color:{C_VI};border:1px solid rgba(194,118,26,.28);padding:3px 11px;border-radius:999px;font-weight:700;font-family:JetBrains Mono,monospace">{len(recs)} item</span></div>', unsafe_allow_html=True)
            for idx_r, (rec_icon, priority, color, bg, border, title, desc) in enumerate(recs):
                delay = f"{0.1 + idx_r * 0.1:.1f}s"
                rec_icon_name = "check" if priority == "INFO" else "alert" if priority == "TINGGI" else "activity"
                rec_icon_html = icon(rec_icon_name, 19)
                st.markdown(f'<div class="rec-item" style="display:flex;gap:14px;padding:16px 18px;background:{bg};border-radius:12px;border:1px solid {border};margin-bottom:10px;animation-delay:{delay}"><div style="color:{color};width:22px;height:22px;display:flex;align-items:center;justify-content:center;flex-shrink:0">{rec_icon_html}</div><div style="flex:1"><div style="display:flex;align-items:center;gap:8px;margin-bottom:6px"><span style="font-size:15px;font-weight:800;color:var(--ink)">{title}</span><span style="font-size:10px;font-weight:800;padding:3px 9px;border-radius:5px;background:{color}1f;color:{color};border:1px solid {color}55;letter-spacing:1px;font-family:JetBrains Mono,monospace">{priority}</span></div><div style="font-size:13.5px;color:var(--ink-2);line-height:1.7">{desc}</div></div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(formula_html(), unsafe_allow_html=True)

        with rp_col:
            render_right_panel(d, vi, esg, fcs, thin, avatar_key)

    # ============ VIEW: GEOSPATIAL ============
    elif st.session_state.view == "geospatial":
        g = d["geo"]
        lat, lng = d["lat"], d["lng"]
        gcode, glabel, gcol, gbg, gborder, gdesc = geo_status(g)
        nd_col, nd_lbl = ndvi_palette(g["ndvi"])
        fl_col = flood_palette(g["flood_risk"])
        lu_col = landuse_palette(g["land_class"])
        bcolor = "#0F9D6B" if g["building_verified"] else "#DC2626"

        st.markdown(f"""
        <div style="padding:18px 2px 12px">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px">
                <span style="color:var(--ui-violet);display:inline-flex">{icon("geospatial", 20)}</span>
                <span style="font-size:20px;font-weight:800;color:var(--ink);letter-spacing:-.4px">Geospatial Intelligence Layer</span>
            </div>
            <div style="font-size:13px;color:var(--ink-2)">Mengubah indikator lokasi menjadi komponen Environmental yang dapat diaudit serta sinyal verifikasi untuk tinjauan manusia.</div>
        </div>
        """, unsafe_allow_html=True)

        gico = icon("check", 20) if gcode == "verified" else (icon("alert", 20) if gcode == "inconsistent" else icon("x", 20))
        st.markdown(f"""
        <div class="geo-banner" style="background:{gbg};border-color:{gborder}">
            <div class="gb-ico" style="background:{gcol};color:#fff">{gico}</div>
            <div>
                <div class="gb-title" style="color:{gcol}">{glabel}</div>
                <div class="gb-desc">{gdesc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        main_col, rp_col = st.columns([3.2, 1], gap="medium")
        with main_col:
            # ---------- PETA MULTI-LAYER ----------
            mk = "green" if fcs >= 0.70 else "orange" if fcs >= 0.50 else "red"
            popup_html = f"""<div style="font-family:Arial;width:220px;padding:8px">
                <b style="font-size:14px">{d['nama']}</b><br>
                <span style="font-size:12px;color:#666">{d['usaha']}</span>
                <hr style="margin:8px 0">
                <table style="width:100%;font-size:13px">
                    <tr><td>NDVI</td><td style="text-align:right;font-weight:bold;color:{nd_col}">{g['ndvi']:.2f}</td></tr>
                    <tr><td>Proximity</td><td style="text-align:right;font-weight:bold">{meter_label(g['proximity_m'])}</td></tr>
                    <tr><td>Bangunan</td><td style="text-align:right;font-weight:bold;color:{bcolor}">{'Terverifikasi' if g['building_verified'] else 'Tidak ada'}</td></tr>
                    <tr><td><b>FCS</b></td><td style="text-align:right;font-weight:bold;font-size:15px;color:{C_FCS}">{fcs}</td></tr>
                </table>
            </div>"""
            m = folium.Map(location=[lat, lng], zoom_start=15, tiles=None)
            folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}", attr="Esri World Imagery", name="Citra Satelit").add_to(m)
            folium.TileLayer("OpenStreetMap", name="Peta Jalan").add_to(m)
            folium.TileLayer("https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png", attr="OpenTopoMap (CC-BY-SA)", name="Topografi").add_to(m)
            # Zona risiko banjir (overlay ilustratif)
            folium.Circle(location=[lat, lng], radius=470, color=fl_col, weight=1, fill=True,
                fill_color=fl_col, fill_opacity=0.10, tooltip=f"Zona risiko banjir: {g['flood_risk']}").add_to(m)
            # Radius verifikasi bangunan 100 m
            folium.Circle(location=[lat, lng], radius=100, color=bcolor, weight=2.5, fill=True,
                fill_color=bcolor, fill_opacity=0.06, dash_array="6",
                tooltip=f"Radius verifikasi bangunan 100 m · {'Terverifikasi' if g['building_verified'] else 'Tidak ditemukan bangunan'}").add_to(m)
            # Marker debitur
            folium.Marker(location=[lat, lng], popup=folium.Popup(popup_html, max_width=240),
                tooltip=d['nama'], icon=folium.Icon(color=mk, icon="home", prefix="fa")).add_to(m)
            # Proximity: POI terdekat + garis jarak
            offs = g["proximity_m"] / 111000.0
            poi_lat = lat + offs * 0.55
            poi_lng = lng + offs * 0.85 / max(math.cos(math.radians(lat)), 0.2)
            folium.Marker(location=[poi_lat, poi_lng],
                tooltip=f"{g['proximity_poi']} · {meter_label(g['proximity_m'])}",
                icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa")).add_to(m)
            folium.PolyLine([[lat, lng], [poi_lat, poi_lng]], color="#1D4ED8", weight=2.5,
                dash_array="5", tooltip=f"Proximity index: {meter_label(g['proximity_m'])}").add_to(m)
            folium.LayerControl(collapsed=False).add_to(m)
            st_folium(m, width=None, height=440, returned_objects=[])

            st.markdown(f"""
            <div class="geo-map-key">
                <span><i style="background:{bcolor}"></i> Radius verifikasi bangunan (100 m)</span>
                <span><i style="background:{fl_col}"></i> Zona risiko banjir: {g['flood_risk']}</span>
                <span><i style="background:#1D4ED8"></i> Proximity ke {g['proximity_poi']}</span>
            </div>
            <div class="soft-note" style="border-left-color:var(--accent);margin-top:12px">
                Esri World Imagery hanya berfungsi sebagai basemap demonstrasi, bukan sumber nilai NDVI. Pada pilot, NDVI, tutupan lahan, zona lindung, dan risiko banjir harus ditarik dari sumber resmi atau tervalidasi dengan penanda waktu. Seluruh angka pada prototipe ini adalah data simulasi.
            </div>
            """, unsafe_allow_html=True)

            # ---------- 3 MEKANISME VERIFIKASI OBJEKTIF ----------
            st.markdown('<div style="height:10px"></div><div class="card-title" style="padding-left:2px">Mekanisme Verifikasi Objektif</div>', unsafe_allow_html=True)
            v1, v2, v3 = st.columns(3, gap="medium")
            with v1:
                bflag_col = "#0F9D6B" if g["building_verified"] else "#DC2626"
                bflag_txt = "TERVERIFIKASI" if g["building_verified"] else "TIDAK DITEMUKAN"
                bflag_bg = "rgba(15,157,107,0.10)" if g["building_verified"] else "rgba(220,38,38,0.10)"
                st.markdown(f"""
                <div class="geo-vcard delay-1">
                    <div class="vh"><div class="vi-ico" style="background:rgba(20,48,110,0.08);color:var(--ui-navy)">{icon("building", 15)}</div><div class="vt">Building Footprint</div></div>
                    <div class="vbody">Cek keberadaan bangunan dalam radius 100 m dari koordinat. Ketidakhadiran bangunan memicu permintaan bukti tambahan atau verifikasi lapangan.<br><br>
                    Bangunan terdeteksi: <b style="color:{bflag_col}">{g['building_count']}</b></div>
                    <div class="geo-flag" style="background:{bflag_bg};color:{bflag_col}">● {bflag_txt}</div>
                </div>
                """, unsafe_allow_html=True)
            with v2:
                px_col = "#1D4ED8"
                px_txt = "KONTEKS LOGISTIK"
                st.markdown(f"""
                <div class="geo-vcard delay-2">
                    <div class="vh"><div class="vi-ico" style="background:rgba(29,78,216,0.08);color:#1D4ED8">{icon("ruler", 15)}</div><div class="vt">Proximity Index</div></div>
                    <div class="vbody">Jarak ke pusat ekonomi dan akses logistik ditampilkan sebagai konteks analis. Jarak tidak mengurangi skor agar tidak menghukum UMKM rural.<br><br>
                    Ke {g['proximity_poi']}: <b>{meter_label(g['proximity_m'])}</b><br>Ke jalan utama: <b>{meter_label(g['road_m'])}</b></div>
                    <div class="geo-flag" style="background:rgba(29,78,216,0.10);color:{px_col}">● {px_txt}</div>
                </div>
                """, unsafe_allow_html=True)
            with v3:
                cm_col = "#0F9D6B" if g["claim_match"] else "#C2761A"
                cm_txt = "KLAIM KONSISTEN" if g["claim_match"] else "INKONSISTEN"
                cm_bg = "rgba(15,157,107,0.10)" if g["claim_match"] else "rgba(194,118,26,0.10)"
                st.markdown(f"""
                <div class="geo-vcard delay-3">
                    <div class="vh"><div class="vi-ico" style="background:rgba(15,157,107,0.10);color:var(--ui-teal)">{icon("leaf", 15)}</div><div class="vt">NDVI Verification</div></div>
                    <div class="vbody">Sinyal vegetasi berbasis citra diuji silang dengan jenis aktivitas dan waktu pengamatan untuk memeriksa konsistensi klaim.<br><br>
                    NDVI: <b style="color:{nd_col}">{g['ndvi']:.2f}</b> ({nd_lbl})<br>Klaim: <b>{g['claim']}</b></div>
                    <div class="geo-flag" style="background:{cm_bg};color:{cm_col}">● {cm_txt}</div>
                </div>
                """, unsafe_allow_html=True)

            # ---------- 6 VARIABEL GEOSPASIAL ----------
            st.markdown('<div style="height:14px"></div><div class="card-title" style="padding-left:2px">Variabel Geospasial Terintegrasi</div>', unsafe_allow_html=True)
            geovars = [
                ("NDVI Konsistensi", "Sumber pilot tervalidasi", f"{g['ndvi']:.2f}", nd_col, g["ndvi_label"], "Environmental (ESG)"),
                ("Proximity", "OpenStreetMap", meter_label(g["proximity_m"]), "#1D4ED8", f"ke {g['proximity_poi']}", "Konteks analis, bukan skor"),
                ("Building Footprint", "Sumber pilot tervalidasi", f"{g['building_count']} unit" if g["building_verified"] else "0 unit", bcolor, "Terverifikasi" if g["building_verified"] else "Perlu tinjauan", "Status verifikasi"),
                ("Flood Risk Zone", "BNPB / BIG", g["flood_risk"], fl_col, f"Skor aman {g['flood_score']}/100", "Environmental (ESG)"),
                ("Land Use / Tutupan Lahan", "KLHK / BIG", g["land_use"].split(" /")[0], lu_col, g["land_use"], "E (ESG)"),
                ("Zona Lindung", "KLHK / BIG", "Sesuai" if g.get("protected_zone_ok", True) else "Perlu tinjauan", "#0F9D6B" if g.get("protected_zone_ok", True) else "#DC2626", "Pemeriksaan kepatuhan spasial", "Environmental (ESG)"),
            ]
            for row_start in (0, 3):
                cc = st.columns(3, gap="medium")
                for j in range(3):
                    name, src, val, vcol, sub, mp = geovars[row_start + j]
                    with cc[j]:
                        st.markdown(f"""
                        <div class="geo-var">
                            <div class="gv-top"><span class="gv-name">{name}</span><span class="gv-src">{src}</span></div>
                            <div class="gv-val" style="color:{vcol}">{val}</div>
                            <div class="gv-sub">{sub}</div>
                            <div class="gv-map">Peran: <b>{mp}</b></div>
                        </div>
                        """, unsafe_allow_html=True)

            # ---------- PEMETAAN KONTRIBUSI KE SCORING ----------
            st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
            links = [
                ("NDVI Konsistensi", "—", "Environmental (ESG)"),
                ("Proximity", "Konteks analis", "—"),
                ("Building Footprint", "Status verifikasi", "—"),
                ("Flood Risk Zone", "—", "Environmental (ESG)"),
                ("Land Use", "—", "Environmental (ESG)"),
                ("Zona Lindung", "—", "Environmental (ESG)"),
            ]
            rows = ""
            for var, c5, esg_t in links:
                tag5 = f'<span class="glr-tag glr-5c">{c5}</span>' if c5 != "—" else ""
                tage = f'<span class="glr-tag glr-esg">{esg_t}</span>' if esg_t != "—" else ""
                rows += f'<div class="geo-link-row"><span class="glr-var">{var}</span><span class="glr-arrow">→</span>{tag5}{tage}</div>'
            st.markdown(f"""
            <div class="card">
                <div class="card-title">Peran Variabel Geospasial</div>
                <div style="font-size:12px;color:var(--ink-2);margin-bottom:6px">NDVI, banjir, kesesuaian lahan, dan zona lindung membentuk Environmental. Building footprint dan kontradiksi klaim membentuk status verifikasi. Proximity hanya memberi konteks logistik.</div>
                {rows}
            </div>
            """, unsafe_allow_html=True)
            st.markdown(formula_html(), unsafe_allow_html=True)
        with rp_col:
            render_right_panel(d, vi, esg, fcs, thin, avatar_key)

    # ============ VIEW: DETAIL ============
    elif st.session_state.view == "detail":
        main_col, rp_col = st.columns([3.2, 1], gap="medium")
        with main_col:
            st.markdown(f'<div class="debtor-bar"><span class="debtor-name">{d["nama"]}</span><span class="debtor-badge {bc}">{bt}</span><div class="debtor-sub">{d["usaha"]} · {d["lokasi"]}</div></div><div style="height:16px"></div>', unsafe_allow_html=True)
            dd1, dd2 = st.columns(2, gap="medium")
            with dd1:
                bars = "".join([seg_bar(K[i], d["5C"][i]) for i in range(5)])
                bw_rows = "".join([f'<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:12px;color:var(--ink-2)"><span>{K[i]}</span><span style="font-family:JetBrains Mono,monospace;font-weight:600">{int(wv[i]*100)}%</span></div>' for i in range(5)])
                st.markdown(f'<div class="card"><div class="card-title">Penilaian 5C · Prinsip Kredit</div>{bars}<div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--line)"><div style="font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px">Bobot Contextual BWM</div>{bw_rows}<div class="soft-note">Jalur diturunkan dari {r["data_available"]}/4 kelompok data yang tersedia. Bobot berasal dari optimasi penilaian best-worst profil {r["bwm_profile"]}, versi {r["bwm_version"]}.</div></div></div>', unsafe_allow_html=True)
            with dd2:
                esg_bars = "".join([seg_bar_esg(["E","S","G"][i], E_labels[i], esg_values[i]) for i in range(3)])
                ew_rows = "".join([f'<div style="display:flex;justify-content:space-between;padding:4px 0;font-size:12px;color:var(--ink-2)"><span>{E_labels[i]}</span><span style="font-family:JetBrains Mono,monospace;font-weight:600">{int(EW[i]*100)}%</span></div>' for i in range(3)])
                st.markdown(f'<div class="card"><div class="card-title">ESG Score · Sustainability</div>{esg_bars}<div style="margin-top:14px;padding-top:12px;border-top:1px solid var(--line)"><div style="font-size:10px;letter-spacing:1.4px;text-transform:uppercase;color:var(--ink-3);margin-bottom:8px">Bobot ESG dari BWM</div>{ew_rows}</div></div>', unsafe_allow_html=True)
            st.markdown(formula_html(), unsafe_allow_html=True)
        with rp_col:
            render_right_panel(d, vi, esg, fcs, thin, avatar_key)

    # ============ VIEW: MATH ============
    elif st.session_state.view == "math":
        normalized = r["normalized_global"]
        weighted = r["weighted_global"]
        global_weights = r["global_weights"]
        st.markdown('<div style="padding:18px 2px 6px"><div style="font-size:20px;font-weight:800;color:var(--ink);margin-bottom:4px;letter-spacing:-.4px">Behind the Math</div><div style="font-size:13px;color:var(--ink-2)">Contextual BWM menurunkan bobot dari penilaian ahli, lalu cohort TOPSIS menghitung kedekatan relatif terhadap profil acuan. Seluruh data dan penilaian ahli masih berupa simulasi proof-of-concept.</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="math-card delay-1" style="border-left:4px solid #0F9D6B"><div class="math-label" style="color:#0F9D6B">STEP 1 · CONTEXTUAL BWM</div>', unsafe_allow_html=True)
        st.latex(r"\min\ \xi \quad \mathrm{s.t.}\quad |w_B-a_{Bj}w_j|\leq\xi,\ |w_j-a_{jW}w_W|\leq\xi")
        weight_str = ", ".join([f"{x:.4f}" for x in global_weights])
        xi_max = max(r["bwm_xi"].values())
        st.markdown(f'<div class="math-result-badge badge-green">w global = [{weight_str}] · deviasi maksimum = {xi_max:.4f}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="math-card delay-2" style="border-left:4px solid #6D49C9"><div class="math-label" style="color:#6D49C9">STEP 2 · COHORT NORMALIZATION</div>', unsafe_allow_html=True)
        st.latex(r"r_{ij}=\frac{x_{ij}}{\sqrt{\sum_i x_{ij}^{2}}}")
        norm_str = ", ".join([f"{x:.4f}" for x in normalized])
        st.markdown(f'<div class="math-result-badge badge-purple">r_i = [{norm_str}]</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="math-card delay-3" style="border-left:4px solid #C2761A"><div class="math-label" style="color:#C2761A">STEP 3 · WEIGHTED DECISION MATRIX</div>', unsafe_allow_html=True)
        st.latex(r"v_{ij}=w_j\,r_{ij}")
        weighted_str = ", ".join([f"{x:.4f}" for x in weighted])
        st.markdown(f'<div class="math-result-badge badge-orange">v_i = [{weighted_str}]</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="math-card delay-4" style="border-left:4px solid #0F9D6B"><div class="math-label" style="color:#0F9D6B">STEP 4 · IDEAL DISTANCES</div>', unsafe_allow_html=True)
        st.latex(r"D_i^+=\sqrt{\sum_j(v_{ij}-v_j^+)^2},\qquad D_i^-=\sqrt{\sum_j(v_{ij}-v_j^-)^2}")
        st.markdown(f'<div class="math-result-badge badge-green">D+ = {r["distance_positive"]:.4f} · D− = {r["distance_negative"]:.4f}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="math-card delay-5" style="border-left:4px solid #1D4ED8"><div class="math-label" style="color:#1D4ED8">STEP 5 · TOPSIS CLOSENESS</div>', unsafe_allow_html=True)
        st.latex(r"C_i=\frac{D_i^-}{D_i^+ + D_i^-}")
        st.markdown(f'<div class="math-result-badge badge-blue" style="font-size:18px">C = {fcs} · peringkat {r["rank"]}/{r["cohort_size"]} pada jalur {bt}</div></div>', unsafe_allow_html=True)

    # ============ VIEW: COMPARISON ============
    elif st.session_state.view == "comparison":
        st.markdown('<div style="padding:18px 2px 12px"><div style="font-size:20px;font-weight:800;color:var(--ink);margin-bottom:4px;letter-spacing:-.4px">Perbandingan dengan Profil Acuan Atas</div><div style="font-size:13px;color:var(--ink-2)">Profil aktual dibandingkan dengan anchor 100 yang mengunci solusi ideal positif TOPSIS.</div></div>', unsafe_allow_html=True)

        ideal_5C = [100] * 5
        ideal_ESG = [100] * 3
        ideal_vi = ideal_esg = ideal_fcs = 1.0
        ia, ib = alpha, beta

        col_l, col_vs, col_r = st.columns([5, 0.7, 5], gap="small")

        with col_l:
            st.markdown(profile_card_html(d, avatar_key, " identity-card--comparison"), unsafe_allow_html=True)
            fig1 = radar_chart(d["5C"], K, "194,118,26")
            st.plotly_chart(fig1, width="stretch", config={"displayModeBar":False,"staticPlot":True})
            st.markdown(f"""
            <div class="card" style="margin-top:8px">
                <div style="font-size:12px;color:var(--ink-2);margin-bottom:8px">Bobot BWM tingkat utama (Kredit : ESG)</div>
                <div class="weight-bar-wrap">
                    <div class="weight-alpha" style="width:{alpha*100}%;background:{C_VI}">α = {fmt4(alpha)}</div>
                    <div class="weight-beta" style="width:{beta*100}%">β = {fmt4(beta)}</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px">
                    <div class="comp-score-box"><div class="comp-score-label">Vi Score</div><div class="comp-score-val" style="color:{C_VI}">{vi}</div></div>
                    <div class="comp-score-box"><div class="comp-score-label">ESG Score</div><div class="comp-score-val" style="color:{C_VI}">{esg}</div></div>
                    <div class="comp-score-box"><div class="comp-score-label">FCS</div><div class="comp-score-val" style="color:{C_VI}">{fcs}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_vs:
            st.markdown('<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:80px"><div class="vs-badge">VS</div></div>', unsafe_allow_html=True)

        with col_r:
            st.markdown(f"""
            <div class="card" style="border:1px solid rgba(15,157,107,0.25)">
                <span class="debtor-badge badge-rich" style="margin-bottom:12px;display:inline-flex;align-items:center;gap:6px">{icon("target", 14)} Positive-Ideal Anchor</span>
                <div style="font-size:20px;font-weight:800;color:var(--ink)">Profil Acuan Atas TOPSIS</div>
                <div style="font-size:13px;color:var(--ink-2);margin-bottom:12px">Anchor teknis bernilai 100, bukan standar persetujuan kredit.</div>
            </div>
            """, unsafe_allow_html=True)
            fig2 = radar_chart(ideal_5C, K, "15,157,107")
            st.plotly_chart(fig2, width="stretch", config={"displayModeBar":False,"staticPlot":True})
            st.markdown(f"""
            <div class="card" style="margin-top:8px;border:1px solid rgba(15,157,107,0.2)">
                <div style="font-size:12px;color:var(--ink-2);margin-bottom:8px">Bobot BWM tingkat utama · Jalur {bt}</div>
                <div class="weight-bar-wrap">
                    <div class="weight-alpha" style="width:{ia*100}%;background:{C_ESG}">α = {fmt4(ia)}</div>
                    <div class="weight-beta" style="width:{ib*100}%">β = {fmt4(ib)}</div>
                </div>
                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-top:12px">
                    <div class="comp-score-box"><div class="comp-score-label">Vi Score</div><div class="comp-score-val" style="color:{C_ESG}">{ideal_vi}</div></div>
                    <div class="comp-score-box"><div class="comp-score-label">ESG Score</div><div class="comp-score-val" style="color:{C_ESG}">{ideal_esg}</div></div>
                    <div class="comp-score-box"><div class="comp-score-label">FCS</div><div class="comp-score-val" style="color:{C_ESG}">{ideal_fcs}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        gap_vi  = round(ideal_vi - vi, 4)
        gap_esg = round(ideal_esg - esg, 4)
        gap_fcs = round(ideal_fcs - fcs, 4)
        gap_col = C_ESG if gap_fcs <= 0.05 else C_VI if gap_fcs <= 0.15 else "#DC2626"
        gap_txt = "Sangat dekat dengan profil ideal" if gap_fcs <= 0.05 else "Terdapat ruang peningkatan yang signifikan" if gap_fcs <= 0.15 else "Diperlukan peningkatan pada beberapa dimensi"

        st.markdown(f"""
        <div class="insight-card">
            <span style="color:var(--ui-violet);display:inline-flex">{icon("activity", 21)}</span>
            <div>
                <div style="font-size:14px;color:var(--ink);line-height:1.6;margin-bottom:8px">
                    <b>Gap Analysis:</b> {gap_txt}
                </div>
                <div style="display:flex;gap:24px;font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--ink-2)">
                    <span>Gap Vi: <b style="color:{gap_col}">{'−' if gap_vi<0 else '+'}{abs(gap_vi)}</b></span>
                    <span>Gap ESG: <b style="color:{gap_col}">{'−' if gap_esg<0 else '+'}{abs(gap_esg)}</b></span>
                    <span>Gap FCS: <b style="color:{gap_col}">{'−' if gap_fcs<0 else '+'}{abs(gap_fcs)}</b></span>
                </div>
            </div>
        </div>
        <div class="soft-note">
            {icon("info", 16)} Profil acuan atas hanya menstabilkan solusi ideal positif TOPSIS pada cohort kecil. Skor tetap menjadi alat prioritas tinjauan dan bukan keputusan kredit otomatis.
        </div>
        """, unsafe_allow_html=True)
