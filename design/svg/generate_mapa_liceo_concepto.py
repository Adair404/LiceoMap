#!/usr/bin/env python3
"""Generate a simplified, mobile-readable redraw of the Liceo B-4 plan."""

from pathlib import Path

OUTPUT = Path(__file__).with_name("mapa_liceo_concepto.svg")

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="920" height="1350" viewBox="0 0 920 1350"
     role="img" aria-labelledby="title description">
  <title id="title">Mapa orientativo del Liceo B-4 Antonio Varas de la Barra</title>
  <desc id="description">Vista simplificada basada en el plano arquitectónico. Calle Alfredo Thomas queda al norte, Avenida Loa al sur. Los bloques y patios conservan su distribución general; confirme los nombres y accesos en terreno.</desc>
  <defs>
    <style>
      text { font-family: system-ui, "Segoe UI", sans-serif; fill: #f4f8ff; }
      .on-dark { fill: #fff !important; }
      .building text { stroke: none; }
      .road { fill: #12243a; }
      .site { fill: #0b1728; stroke: #35587d; stroke-width: 4; }
      .walk { fill: #14263d; stroke: #4f7aa3; stroke-width: 3; }
      .queue-walk { fill: #0a84ff; stroke: #6fa3d1; stroke-width: 3; }
      .building { stroke: #24486d; stroke-width: 4; }
      .room { fill: #fff; stroke: #6685a7; stroke-width: 2; }
      .room-alt { fill: #eaf3ff; stroke: #6685a7; stroke-width: 2; }
      .gym { fill: #1464b5; }
      .classroom { fill: #168dff; }
      .admin { fill: #0a84ff; }
      .sport { fill: #168dff; }
      .special { fill: #168dff; }
      .block-letter { font-size: 30px; font-weight: 900; fill: #fff; }
      .block-name { font-size: 18px; font-weight: 800; fill: #fff; }
      .small-label { font-size: 15px; font-weight: 700; }
      .road-label { font-size: 18px; font-weight: 850; letter-spacing: 1.2px; fill: #d4e9ff; }
      .court-mark { fill: none; stroke: #fff; stroke-width: 3; }
      .path-line { fill: none; stroke: #fff; stroke-width: 15; stroke-linecap: round; }
      .route-line { fill: none; stroke: #168dff; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 12 9; }
      .node { fill: #168dff; stroke: #fff; stroke-width: 4; }
      .step-marker { fill: #0d315b; stroke: #fff; stroke-width: 3; }
      .step-label { fill: #fff; font-size: 15px; font-weight: 900; text-anchor: middle; }
      .north { font-size: 16px; font-weight: 900; }
    </style>
    <pattern id="paving" width="18" height="18" patternUnits="userSpaceOnUse">
      <path d="M18 0H0V18" fill="none" stroke="#223b59" stroke-width="1"/>
    </pattern>
    <pattern id="map_grid_minor" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M20 0H0V20" fill="none" stroke="#dceeff" stroke-opacity="0.2" stroke-width="0.8"/>
    </pattern>
    <pattern id="map_grid_major" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="#dceeff" stroke-opacity="0.36" stroke-width="1"/>
    </pattern>
    <marker id="arrow" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto">
      <path d="M0 0L10 5L0 10Z" fill="#168dff"/>
    </marker>
    <pattern id="malla_reja" width="6" height="6" patternUnits="userSpaceOnUse">
      <path d="M0 0L6 6M6 0L0 6" stroke="#dceeff" stroke-width="0.9"/>
    </pattern>
  </defs>

  <rect width="920" height="1350" fill="#07111f"/>

  <!-- Orientation and street names make the plan readable without relying on color. -->
  <g id="orientacion">
    <rect class="road" x="30" y="24" width="860" height="58" rx="14"/>
    <text class="road-label" x="420" y="60" text-anchor="middle">CALLE ALFREDO THOMAS · NORTE</text>
    <path d="M850 98V54" stroke="#f4f8ff" stroke-width="4" marker-end="url(#arrow)"/>
    <text class="north" x="850" y="42" text-anchor="middle">N</text>
  </g>

  <path id="recinto_liceo" class="site" d="M52 98H801A22 22 0 0 1 823 120V538A22 22 0 0 1 801 560H702A22 22 0 0 0 680 582V1218A22 22 0 0 1 658 1240H52A22 22 0 0 1 30 1218V120A22 22 0 0 1 52 98Z"/>
  <g id="contenido_desplazado_40" transform="translate(40 0)">
  <g id="circulaciones">
    <path id="paso_peatonal_01" class="walk" d="M48 187H783V211H48Z"/>
    <path id="paso_peatonal_02" class="walk" d="M48 426H426V451H48Z"/>
    <path id="paso_peatonal_07" class="walk" d="M48 660H640V686H48Z"/>
    <path id="paso_peatonal_09_p02_p07" class="walk" d="M48 451H73V660H48Z"/>
    <path id="paso_peatonal_12_p01_p02" class="walk" d="M48 211H73V426H48Z"/>
    <path id="paso_peatonal_03" class="walk" d="M400 205H426V660H400Z"/>
    <path id="paso_peatonal_08_pasillo_porteria" class="walk" d="M148 686H176V1112H148Z"/>
  </g>

  <g id="pasto_sobre_bloque_b" aria-label="Pasto y árboles sobre B">
    <rect x="73" y="451" width="327" height="15" fill="#2f7d4f" opacity=".85"/>
    <g fill="#1d5c38" stroke="#0f3a22" stroke-width="1">
      <circle cx="340" cy="458.5" r="6"/>
      <circle cx="362" cy="458.5" r="6"/>
      <circle cx="384" cy="458.5" r="6"/>
    </g>
    <g fill="#4fae6f">
      <circle cx="338.5" cy="457" r="2.2"/>
      <circle cx="360.5" cy="457" r="2.2"/>
      <circle cx="382.5" cy="457" r="2.2"/>
    </g>
  </g>

  <!-- The central patio is the entire open quadrangle between the surrounding walkways. -->
  <g transform="translate(0 60)">
  <g id="patio_central">
    <rect x="176" y="626" width="290" height="324" fill="#10233a"/>
    <rect x="182" y="632" width="284" height="312" fill="url(#paving)"/>
    <rect id="patio_cuadro_temp_01" x="176" y="638" width="124" height="135" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <g id="mesas_taca_taca_t1" transform="translate(238 686) scale(0.8) translate(-234 -705.5)" aria-label="Nueve mesas de taca-taca">
      <g id="mesa_taca_taca_t1_01"><rect x="181" y="655.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="183.5" y="658.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M196 658.0V673.0" stroke="#dceeff" stroke-width=".8"/><circle cx="196" cy="665.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M187 658.5V672.5"/><path d="M193 658.5V672.5"/><path d="M199 658.5V672.5"/><path d="M205 658.5V672.5"/></g><g fill="#eaf3ff"><circle cx="187" cy="662.5" r="1.4"/><circle cx="187" cy="668.5" r="1.4"/><circle cx="193" cy="661.5" r="1.4"/><circle cx="193" cy="665.5" r="1.4"/><circle cx="193" cy="669.5" r="1.4"/><circle cx="199" cy="661.5" r="1.4"/><circle cx="199" cy="665.5" r="1.4"/><circle cx="199" cy="669.5" r="1.4"/><circle cx="205" cy="662.5" r="1.4"/><circle cx="205" cy="668.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_02"><rect x="219" y="655.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="221.5" y="658.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M234 658.0V673.0" stroke="#dceeff" stroke-width=".8"/><circle cx="234" cy="665.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M225 658.5V672.5"/><path d="M231 658.5V672.5"/><path d="M237 658.5V672.5"/><path d="M243 658.5V672.5"/></g><g fill="#eaf3ff"><circle cx="225" cy="662.5" r="1.4"/><circle cx="225" cy="668.5" r="1.4"/><circle cx="231" cy="661.5" r="1.4"/><circle cx="231" cy="665.5" r="1.4"/><circle cx="231" cy="669.5" r="1.4"/><circle cx="237" cy="661.5" r="1.4"/><circle cx="237" cy="665.5" r="1.4"/><circle cx="237" cy="669.5" r="1.4"/><circle cx="243" cy="662.5" r="1.4"/><circle cx="243" cy="668.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_03"><rect x="257" y="655.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="259.5" y="658.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M272 658.0V673.0" stroke="#dceeff" stroke-width=".8"/><circle cx="272" cy="665.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M263 658.5V672.5"/><path d="M269 658.5V672.5"/><path d="M275 658.5V672.5"/><path d="M281 658.5V672.5"/></g><g fill="#eaf3ff"><circle cx="263" cy="662.5" r="1.4"/><circle cx="263" cy="668.5" r="1.4"/><circle cx="269" cy="661.5" r="1.4"/><circle cx="269" cy="665.5" r="1.4"/><circle cx="269" cy="669.5" r="1.4"/><circle cx="275" cy="661.5" r="1.4"/><circle cx="275" cy="665.5" r="1.4"/><circle cx="275" cy="669.5" r="1.4"/><circle cx="281" cy="662.5" r="1.4"/><circle cx="281" cy="668.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_04"><rect x="181" y="695.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="183.5" y="698.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M196 698.0V713.0" stroke="#dceeff" stroke-width=".8"/><circle cx="196" cy="705.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M187 698.5V712.5"/><path d="M193 698.5V712.5"/><path d="M199 698.5V712.5"/><path d="M205 698.5V712.5"/></g><g fill="#eaf3ff"><circle cx="187" cy="702.5" r="1.4"/><circle cx="187" cy="708.5" r="1.4"/><circle cx="193" cy="701.5" r="1.4"/><circle cx="193" cy="705.5" r="1.4"/><circle cx="193" cy="709.5" r="1.4"/><circle cx="199" cy="701.5" r="1.4"/><circle cx="199" cy="705.5" r="1.4"/><circle cx="199" cy="709.5" r="1.4"/><circle cx="205" cy="702.5" r="1.4"/><circle cx="205" cy="708.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_05"><rect x="219" y="695.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="221.5" y="698.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M234 698.0V713.0" stroke="#dceeff" stroke-width=".8"/><circle cx="234" cy="705.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M225 698.5V712.5"/><path d="M231 698.5V712.5"/><path d="M237 698.5V712.5"/><path d="M243 698.5V712.5"/></g><g fill="#eaf3ff"><circle cx="225" cy="702.5" r="1.4"/><circle cx="225" cy="708.5" r="1.4"/><circle cx="231" cy="701.5" r="1.4"/><circle cx="231" cy="705.5" r="1.4"/><circle cx="231" cy="709.5" r="1.4"/><circle cx="237" cy="701.5" r="1.4"/><circle cx="237" cy="705.5" r="1.4"/><circle cx="237" cy="709.5" r="1.4"/><circle cx="243" cy="702.5" r="1.4"/><circle cx="243" cy="708.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_06"><rect x="257" y="695.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="259.5" y="698.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M272 698.0V713.0" stroke="#dceeff" stroke-width=".8"/><circle cx="272" cy="705.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M263 698.5V712.5"/><path d="M269 698.5V712.5"/><path d="M275 698.5V712.5"/><path d="M281 698.5V712.5"/></g><g fill="#eaf3ff"><circle cx="263" cy="702.5" r="1.4"/><circle cx="263" cy="708.5" r="1.4"/><circle cx="269" cy="701.5" r="1.4"/><circle cx="269" cy="705.5" r="1.4"/><circle cx="269" cy="709.5" r="1.4"/><circle cx="275" cy="701.5" r="1.4"/><circle cx="275" cy="705.5" r="1.4"/><circle cx="275" cy="709.5" r="1.4"/><circle cx="281" cy="702.5" r="1.4"/><circle cx="281" cy="708.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_07"><rect x="181" y="735.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="183.5" y="738.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M196 738.0V753.0" stroke="#dceeff" stroke-width=".8"/><circle cx="196" cy="745.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M187 738.5V752.5"/><path d="M193 738.5V752.5"/><path d="M199 738.5V752.5"/><path d="M205 738.5V752.5"/></g><g fill="#eaf3ff"><circle cx="187" cy="742.5" r="1.4"/><circle cx="187" cy="748.5" r="1.4"/><circle cx="193" cy="741.5" r="1.4"/><circle cx="193" cy="745.5" r="1.4"/><circle cx="193" cy="749.5" r="1.4"/><circle cx="199" cy="741.5" r="1.4"/><circle cx="199" cy="745.5" r="1.4"/><circle cx="199" cy="749.5" r="1.4"/><circle cx="205" cy="742.5" r="1.4"/><circle cx="205" cy="748.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_08"><rect x="219" y="735.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="221.5" y="738.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M234 738.0V753.0" stroke="#dceeff" stroke-width=".8"/><circle cx="234" cy="745.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M225 738.5V752.5"/><path d="M231 738.5V752.5"/><path d="M237 738.5V752.5"/><path d="M243 738.5V752.5"/></g><g fill="#eaf3ff"><circle cx="225" cy="742.5" r="1.4"/><circle cx="225" cy="748.5" r="1.4"/><circle cx="231" cy="741.5" r="1.4"/><circle cx="231" cy="745.5" r="1.4"/><circle cx="231" cy="749.5" r="1.4"/><circle cx="237" cy="741.5" r="1.4"/><circle cx="237" cy="745.5" r="1.4"/><circle cx="237" cy="749.5" r="1.4"/><circle cx="243" cy="742.5" r="1.4"/><circle cx="243" cy="748.5" r="1.4"/></g></g>
      <g id="mesa_taca_taca_t1_09"><rect x="257" y="735.5" width="30" height="20" rx="2.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><rect x="259.5" y="738.0" width="25" height="15" rx="1.5" fill="#168dff"/><path d="M272 738.0V753.0" stroke="#dceeff" stroke-width=".8"/><circle cx="272" cy="745.5" r="2.8" fill="none" stroke="#dceeff" stroke-width=".8"/><g stroke="#17385f" stroke-width=".9" stroke-linecap="round"><path d="M263 738.5V752.5"/><path d="M269 738.5V752.5"/><path d="M275 738.5V752.5"/><path d="M281 738.5V752.5"/></g><g fill="#eaf3ff"><circle cx="263" cy="742.5" r="1.4"/><circle cx="263" cy="748.5" r="1.4"/><circle cx="269" cy="741.5" r="1.4"/><circle cx="269" cy="745.5" r="1.4"/><circle cx="269" cy="749.5" r="1.4"/><circle cx="275" cy="741.5" r="1.4"/><circle cx="275" cy="745.5" r="1.4"/><circle cx="275" cy="749.5" r="1.4"/><circle cx="281" cy="742.5" r="1.4"/><circle cx="281" cy="748.5" r="1.4"/></g></g>
    </g>
    <g id="mesas_ping_pong_t1" aria-label="Dos mesas de ping pong">
      <g id="mesa_ping_pong_t1_01"><rect x="190" y="738" width="44" height="24" rx="2" fill="#168dff" stroke="#eaf3ff" stroke-width="1.5"/><path d="M192 750.0H232" stroke="#dceeff" stroke-width=".8"/><path d="M212.0 736V764" stroke="#17385f" stroke-width="1.6" stroke-linecap="round"/><path d="M212.0 738V762" stroke="#eaf3ff" stroke-width=".6" stroke-dasharray="1.5 1.5"/></g>
      <g id="mesa_ping_pong_t1_02"><rect x="242" y="738" width="44" height="24" rx="2" fill="#168dff" stroke="#eaf3ff" stroke-width="1.5"/><path d="M244 750.0H284" stroke="#dceeff" stroke-width=".8"/><path d="M264.0 736V764" stroke="#17385f" stroke-width="1.6" stroke-linecap="round"/><path d="M264.0 738V762" stroke="#eaf3ff" stroke-width=".6" stroke-dasharray="1.5 1.5"/></g>
    </g>
    <rect id="patio_cuadro_temp_02" x="310" y="638" width="112" height="135" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <rect id="patio_cuadro_temp_03" x="176" y="789" width="124" height="135" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <g id="fuentes_arbustos_t3" transform="translate(-191 -783.5) scale(2)" aria-label="Nueve fuentes con arbustos">
      <g id="fuente_t3_01" transform="translate(192 803) scale(0.9) translate(-192 -803)"><circle cx="192" cy="803" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="192" cy="803" r="4.8" fill="#0f3a22"/><circle cx="190.4" cy="802.2" r="2.6" fill="#2f7d4f"/><circle cx="193.8" cy="801.8" r="2.3" fill="#4fae6f"/><circle cx="192.3" cy="804.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_02" transform="translate(209 803) scale(0.9) translate(-209 -803)"><circle cx="209" cy="803" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="209" cy="803" r="4.8" fill="#0f3a22"/><circle cx="207.4" cy="802.2" r="2.6" fill="#2f7d4f"/><circle cx="210.8" cy="801.8" r="2.3" fill="#4fae6f"/><circle cx="209.3" cy="804.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_03" transform="translate(226 803) scale(0.9) translate(-226 -803)"><circle cx="226" cy="803" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="226" cy="803" r="4.8" fill="#0f3a22"/><circle cx="224.4" cy="802.2" r="2.6" fill="#2f7d4f"/><circle cx="227.8" cy="801.8" r="2.3" fill="#4fae6f"/><circle cx="226.3" cy="804.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_04" transform="translate(192 820) scale(0.9) translate(-192 -820)"><circle cx="192" cy="820" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="192" cy="820" r="4.8" fill="#0f3a22"/><circle cx="190.4" cy="819.2" r="2.6" fill="#2f7d4f"/><circle cx="193.8" cy="818.8" r="2.3" fill="#4fae6f"/><circle cx="192.3" cy="821.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_05" transform="translate(209 820) scale(0.9) translate(-209 -820)"><circle cx="209" cy="820" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="209" cy="820" r="4.8" fill="#0f3a22"/><circle cx="207.4" cy="819.2" r="2.6" fill="#2f7d4f"/><circle cx="210.8" cy="818.8" r="2.3" fill="#4fae6f"/><circle cx="209.3" cy="821.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_06" transform="translate(226 820) scale(0.9) translate(-226 -820)"><circle cx="226" cy="820" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="226" cy="820" r="4.8" fill="#0f3a22"/><circle cx="224.4" cy="819.2" r="2.6" fill="#2f7d4f"/><circle cx="227.8" cy="818.8" r="2.3" fill="#4fae6f"/><circle cx="226.3" cy="821.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_07" transform="translate(192 837) scale(0.9) translate(-192 -837)"><circle cx="192" cy="837" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="192" cy="837" r="4.8" fill="#0f3a22"/><circle cx="190.4" cy="836.2" r="2.6" fill="#2f7d4f"/><circle cx="193.8" cy="835.8" r="2.3" fill="#4fae6f"/><circle cx="192.3" cy="838.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_08" transform="translate(209 837) scale(0.9) translate(-209 -837)"><circle cx="209" cy="837" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="209" cy="837" r="4.8" fill="#0f3a22"/><circle cx="207.4" cy="836.2" r="2.6" fill="#2f7d4f"/><circle cx="210.8" cy="835.8" r="2.3" fill="#4fae6f"/><circle cx="209.3" cy="838.8" r="2.4" fill="#1d5c38"/></g>
      <g id="fuente_t3_09" transform="translate(226 837) scale(0.9) translate(-226 -837)"><circle cx="226" cy="837" r="6.5" fill="#eaf3ff" stroke="#6685a7" stroke-width="1"/><circle cx="226" cy="837" r="4.8" fill="#0f3a22"/><circle cx="224.4" cy="836.2" r="2.6" fill="#2f7d4f"/><circle cx="227.8" cy="835.8" r="2.3" fill="#4fae6f"/><circle cx="226.3" cy="838.8" r="2.4" fill="#1d5c38"/></g>
    </g>
    <rect id="patio_cuadro_temp_04" x="310" y="789" width="112" height="135" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <g id="etiquetas_temporales_patio" fill="#fff" stroke="#07111f" stroke-width="3" paint-order="stroke">
    <text class="on-dark" x="238" y="712" text-anchor="middle" font-size="16" font-weight="900">T1</text>
    <text class="on-dark" x="366" y="712" text-anchor="middle" font-size="16" font-weight="900">T2</text>
    <text class="on-dark" x="238" y="862" text-anchor="middle" font-size="16" font-weight="900">T3</text>
    <text class="on-dark" x="366" y="862" text-anchor="middle" font-size="16" font-weight="900">T4</text>
    </g>
    <rect x="245" y="766" width="204" height="29" rx="11" fill="#0d315b"/>
    <text class="block-name" x="347" y="787" text-anchor="middle">PATIO CENTRAL</text>
  </g>
  <path id="paso_peatonal_06_fila_comedor" class="queue-walk" d="M424 626H452V947H424Z"/>
  </g>

  <!-- Block L faces Calle Alfredo Thomas. Room divisions are schematic. -->
  <g id="bloque_l" class="building">
    <rect x="40" y="112" width="743" height="72" rx="8" fill="#17385f"/>
    <path class="room" d="M48.0 120H190.2V176H48.0Z"/>
    <path class="room-alt" d="M194.2 120H336.4V176H194.2Z"/>
    <path class="room" d="M340.4 120H482.6V176H340.4Z"/>
    <path class="room-alt" d="M486.6 120H628.8V176H486.6Z"/>
    <path class="room" d="M632.8 120H775.0V176H632.8Z"/>
  </g>
  <text class="small-label" x="300" y="205" text-anchor="middle">L · PABELLÓN NORTE</text>

  <!-- K: recognizable indoor court, with the west-side service wing shown separately. -->
  <g id="anexo_bloque_k" class="building">
    <rect x="76" y="222" width="75" height="194" rx="8" fill="#15385c"/>
    <path class="room" d="M84 232H143V286H84Z"/>
    <path class="room-alt" d="M84 292H143V346H84Z"/>
    <path class="room" d="M84 352H143V406H84Z"/>
  </g>
  <g id="bloque_k" class="building">
    <rect x="160" y="222" width="236" height="194" rx="12" class="gym"/>
    <rect x="164" y="224" width="228" height="24" rx="8" fill="#0d315b"/>
    <g id="cancha_gimnasio_k">
      <rect x="181" y="252" width="194" height="134" rx="4" fill="#1d69b7" stroke="#fff" stroke-width="3"/>
      <path class="court-mark" d="M278 252V386M181 319H375"/>
      <circle class="court-mark" cx="278" cy="319" r="25"/>
      <path class="court-mark" d="M181 287h30v64h-30M375 287h-30v64h30"/>
    </g>
    <rect x="215" y="391" width="126" height="25" rx="8" fill="#0d315b"/>
    <text class="on-dark" x="278" y="241" text-anchor="middle" font-size="14" font-weight="850">K · GIMNASIO</text>
  </g>

  <!-- E and the open stage area; the latter is also used as a court. -->
  <g id="aulas_e_d_c_junto_a_p03" transform="translate(-94 0)">
  <g id="bloque_e" class="building">
    <rect x="540" y="218" width="129" height="168" rx="10" class="admin"/>
    <rect x="544" y="222" width="121" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room" x="550" y="250" width="109" height="50" rx="4"/>
    <rect class="room-alt" x="550" y="306" width="109" height="74" rx="4"/>
    <text class="on-dark" x="604.5" y="239" text-anchor="middle" font-size="13" font-weight="850">E · AULAS</text>
  </g>
  <g id="bloque_d_pabellon" class="building">
    <rect x="540" y="390" width="129" height="168" rx="10" class="admin"/>
    <rect x="544" y="394" width="121" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room" x="550" y="422" width="109" height="50" rx="4"/>
    <rect class="room-alt" x="550" y="478" width="109" height="74" rx="4"/>
    <text class="on-dark" x="604.5" y="411" text-anchor="middle" font-size="13" font-weight="850">D · AULAS</text>
  </g>
  <g id="bloque_c_este" class="building">
    <rect x="540" y="562" width="129" height="84" rx="10" class="admin"/>
    <rect x="544" y="566" width="121" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room-alt" x="550" y="594" width="109" height="46" rx="4"/>
    <text class="on-dark" x="604.5" y="583" text-anchor="middle" font-size="13" font-weight="850">C · AULAS</text>
  </g>
  </g>
  <g transform="translate(0 60)">
  <g id="escenario_cancha_este" transform="translate(-66 0)" aria-label="Escenario, espacio abierto usado como cancha">
    <rect class="admin building" x="532" y="626" width="180" height="324"/>
    <g id="cancha_deportiva_interior">
      <rect x="550" y="637" width="115" height="216" rx="3" style="fill:#1464b5" stroke="#dceeff" stroke-width="2"/>
      <path d="M550 745H665" stroke="#dceeff" stroke-opacity=".5" stroke-width="1.5"/>
      <g id="escenario_cancha">
        <rect x="668" y="693" width="37" height="107" rx="2" style="fill:#8c97a3" stroke="#dceeff" stroke-width="1.5"/>
        <path d="M668 693V800" stroke="#ff9a3c" stroke-width="3"/>
      </g>
    </g>
    <text class="on-dark" x="607" y="690" text-anchor="middle" font-size="13" font-weight="850">CANCHA</text>
    <text class="on-dark" x="607" y="706" text-anchor="middle" font-size="13" font-weight="850">DEPORTIVA</text>
    <g id="gimnasio_escenario" aria-label="Gimnasio">
      <rect class="classroom building" x="532" y="876" width="101" height="52" style="fill:#6b7f95"/>
      <text class="on-dark" x="582" y="907" text-anchor="middle" font-size="12" font-weight="850">GIMNASIO</text>
    </g>
    <g id="kiosco_escenario" aria-label="Kiosco">
      <rect class="classroom building" x="657" y="876" width="55" height="86" style="fill:#fff"/>
      <text x="684" y="923" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">KIOSCO</text>
    </g>
    <g id="pasillo_gimnasio_kiosco" aria-label="Pasillo hacia el kiosco">
      <path id="paso_peatonal_10_gimnasio" class="walk" d="M532 928H633V962H532Z"/>
      <path id="paso_peatonal_11_kiosco" class="walk" d="M633 876H657V962H633Z"/>
    </g>
  </g>
  </g>

  <g id="bloques_b_c_d_junto_a_j" transform="translate(-36 0)">
    <!-- B is the central teaching / administration wing. -->
  <g id="bloque_b" class="building">
    <rect x="110" y="466" width="316" height="182" rx="10" class="classroom"/>
    <rect x="116" y="470" width="304" height="24" rx="7" fill="#168dff"/>
    <rect class="room" x="120" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="172" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="224" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="276" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="328" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="380" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="120" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="172" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="224" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="276" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="328" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="380" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <text style="fill:#07111f" x="268" y="487" text-anchor="middle" font-size="12" font-weight="850">B · AULAS / ADMIN.</text>
  </g>
  </g>

  <!-- West-side J, I and F are shown as long, separate wings as on the plan. -->
  <g transform="translate(0 60)">
  <g id="bloque_i" class="building" transform="translate(-40 0)">
    <rect x="74" y="652" width="74" height="179" rx="10" fill="#168dff"/>
    <path class="room" d="M83 661H139V738.5H83Z"/>
    <path class="room-alt" d="M83 744.5H139V822H83Z"/>
    <rect x="90" y="716" width="42" height="50" rx="12" fill="#168dff"/>
    <text class="block-letter" x="111" y="751" text-anchor="middle">I</text>
  </g>
  <g id="bloque_f" class="building" transform="translate(-40 0)">
    <rect x="74" y="842" width="74" height="98" rx="10" fill="#168dff"/>
    <path class="room" d="M83 851H139V886H83Z"/>
    <path class="room-alt" d="M83 892H139V931H83Z"/>
    <rect x="90" y="867" width="42" height="50" rx="12" fill="#168dff"/>
    <text class="block-letter" x="111" y="902" text-anchor="middle">F</text>
    <text class="on-dark" x="122" y="949" text-anchor="middle" font-size="9" font-weight="850">F · DEPENDENCIAS</text>
  </g>
  </g>

  <!-- Eastern outdoor court shown in the architectural plan; not a multicancha. -->
  <g id="patio_deportivo_este" transform="translate(-5 0)">
    <rect x="628" y="295" width="159" height="263" rx="12" fill="#087bff" stroke="#24486d" stroke-width="4"/>
    <rect class="court-mark" x="641" y="309" width="133" height="226"/>
    <path class="court-mark" d="M641 422H774"/>
    <circle class="court-mark" cx="707.5" cy="422" r="22"/>
    <rect x="637.5" y="502" width="140" height="28" rx="7" fill="#0754ad"/>
    <text class="on-dark" x="707.5" y="521" text-anchor="middle" font-size="13" font-weight="850">CANCHA</text>
  </g>
  <g id="bloque_q640" class="building">
    <rect x="600" y="580" width="40" height="80" rx="6" class="classroom"/>
  </g>
  <g id="aulas_g_provisional" class="building" transform="translate(-5 0)">
    <rect x="628" y="218" width="159" height="73" rx="10" class="classroom"/>
    <text style="fill:#07111f" x="707.5" y="259" text-anchor="middle" font-size="14" font-weight="850">AULAS A32–A33</text>
  </g>

  <!-- Provisional southern volumes sit directly behind the dining room; internal room layouts remain unconfirmed. -->
  <g transform="translate(0 60)">
  <g id="edificio_acceso_sur" class="building">
    <path d="M210 945H550V1068H210Z" fill="#15385c"/>
    <g id="comedor_acceso_loa" transform="translate(74.4 292) scale(0.8 0.7)">
      <path d="M307 940V872H317V859C331 854 346 840 372 840C398 840 413 854 427 859V872H437V940Z" fill="#0a84ff" stroke="#35587d" stroke-width="3"/>
      <text style="fill:#07111f" x="372" y="894" text-anchor="middle" font-size="17" font-weight="850">COMEDOR</text>
    </g>
    <g id="aulas_tras_comedor_izquierda_provisional" aria-label="Estructura de aulas de dos pisos; distribución pendiente">
      <rect x="214" y="950" width="156" height="112" rx="6" fill="#168dff" stroke="#24486d" stroke-width="3"/>
      <rect x="222" y="958" width="140" height="44" rx="4" fill="#eaf3ff" stroke="#6685a7" stroke-width="2"/>
      <rect x="222" y="1009" width="140" height="44" rx="4" fill="#fff" stroke="#6685a7" stroke-width="2"/>
      <text x="292" y="985" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">SECTOR SUR</text>
    </g>
    <g id="aulas_tras_comedor_derecha_provisional" aria-label="Estructura de aulas de dos pisos; distribución pendiente">
      <rect x="374" y="950" width="176" height="112" rx="6" fill="#168dff" stroke="#24486d" stroke-width="3"/>
      <rect x="382" y="958" width="160" height="44" rx="4" fill="#eaf3ff" stroke="#6685a7" stroke-width="2"/>
      <rect x="382" y="1009" width="160" height="44" rx="4" fill="#fff" stroke="#6685a7" stroke-width="2"/>
      <text x="462" y="985" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">SECTOR SUR</text>
    </g>
  </g>

  <!-- Portería and the public entrance align with Avenida Loa. -->
  <g id="bloque_h" class="building">
    <g id="sector_utp_provisional" aria-label="Bloque J, antes UTP">
      <path d="M-4 652H30V952H120V1100H-4Z" fill="#17385f" stroke="#24486d" stroke-width="4" stroke-linejoin="round"/>
      <path d="M4 660H22V960H112V1092H4Z" fill="#3c8dff" stroke="#3c8dff" stroke-width="8" stroke-linejoin="round"/>
      <text style="fill:#07111f" x="58" y="1024" text-anchor="middle" font-size="20" font-weight="900">J</text>
    </g>
    <g id="sector_porteria" transform="translate(0 100)">
      <rect x="128" y="952" width="72" height="60" rx="8" fill="#17385f"/>
      <rect x="136" y="960" width="56" height="44" rx="5" fill="#eaf3ff"/>
      <text x="164" y="978" text-anchor="middle" font-size="8" font-weight="850" style="fill:#07111f">PORTERÍA</text>
      <text x="164" y="994" text-anchor="middle" font-size="10" font-weight="850" style="fill:#07111f">H</text>
    </g>
    <g id="sector_inspectoria" aria-label="Inspectoría">
      <rect x="204" y="1068" width="72" height="44" rx="8" fill="#17385f"/>
      <rect x="212" y="1076" width="56" height="28" rx="5" fill="#eaf3ff"/>
      <text x="240" y="1094" text-anchor="middle" font-size="8" font-weight="850" style="fill:#07111f">INSPECTORÍA</text>
    </g>
  </g>
  <g id="zona_estacionamiento">
    <path d="M2 1112H556V962H628A8 8 0 0 1 636 970V1168A8 8 0 0 1 628 1176H2A8 8 0 0 1 -6 1168V1120A8 8 0 0 1 2 1112Z" fill="#142a45" stroke="#35587d" stroke-width="3"/>
    <path d="M34 1112V1176M70 1112V1176M106 1112V1176M142 1112V1176M178 1112V1176M214 1112V1176M250 1112V1176M286 1112V1176M322 1112V1176M358 1112V1176M394 1112V1176M430 1112V1176M466 1112V1176M502 1112V1176M538 1112V1176M574 1112V1176M610 1112V1176M580 962V1112M608 962V1112" stroke="#35587d" stroke-width="2"/>
    <rect x="260" y="1117" width="140" height="22" rx="7" fill="#17385f"/>
    <text class="on-dark" x="330" y="1133" text-anchor="middle" font-size="11" font-weight="850">ESTACIONAMIENTO</text>
  </g>
  <g id="camino_entrada_peatonal" aria-label="Camino de la entrada peatonal">
    <rect x="124" y="1112" width="72" height="68" fill="#eaf3ff"/>
  </g>
  <g id="reja_estacionamiento" aria-label="Malla">
    <rect x="276" y="1108" width="280" height="8" fill="url(#malla_reja)" stroke="#dceeff" stroke-width="1.5"/>
    <g id="porton" aria-label="Portón">
      <rect x="556" y="1100" width="84" height="24" rx="4" fill="#0e2038" stroke="#dceeff" stroke-width="3"/>
      <path d="M598 1100V1124" fill="none" stroke="#dceeff" stroke-width="2" stroke-linecap="round"/>
      <rect x="578" y="1086" width="40" height="12" rx="4" fill="#17385f"/>
      <text class="on-dark" x="598" y="1095" text-anchor="middle" font-size="8" font-weight="850">PORTÓN</text>
    </g>
  </g>

  <g id="pasto_arbustos_sector_sur" aria-label="Pasto y arbustos sobre el sector sur">
    <rect x="220" y="926" width="60" height="16" rx="4" fill="#2f7d4f" opacity=".85"/>
    <g fill="#1d5c38" stroke="#0f3a22" stroke-width=".8">
      <circle cx="232" cy="934" r="4.2"/>
      <circle cx="250" cy="933" r="3.6"/>
      <circle cx="268" cy="934.5" r="4.2"/>
    </g>
    <g fill="#4fae6f">
      <circle cx="231" cy="933" r="1.4"/>
      <circle cx="249" cy="932" r="1.2"/>
      <circle cx="267" cy="933.5" r="1.4"/>
    </g>
  </g>
  <g id="pasto_arbustos_junto_p08" aria-label="Pasto y arbustos junto a P08">
    <rect x="120" y="980" width="26" height="61" rx="4" fill="#2f7d4f" opacity=".85"/>
    <g fill="#1d5c38" stroke="#0f3a22" stroke-width=".8"><circle cx="130" cy="996" r="4.6"/><circle cx="136" cy="1014" r="4.6"/><circle cx="131" cy="1032" r="4.6"/></g>
    <g fill="#4fae6f"><circle cx="129" cy="994.5" r="1.5"/><circle cx="135" cy="1012.5" r="1.5"/><circle cx="130" cy="1030.5" r="1.5"/></g>
  </g>
  </g>
  <g transform="translate(0 10)">
  <g id="avenida_loa">
    <rect class="road" x="-10" y="1230" width="860" height="56" rx="14"/>
    <text class="road-label" x="380" y="1274" text-anchor="middle">AVENIDA LOA · ACCESO PRINCIPAL</text>
  </g>
  <g id="acceso_peatonal_loa">
    <path d="M160 1228V1192" fill="none" stroke="#168dff" stroke-width="12"/>
    <path d="M160 1168L178 1194H142Z" fill="#168dff"/>
    <rect x="78" y="1240" width="164" height="20" rx="8" fill="#168dff"/>
    <text style="fill:#07111f" x="160" y="1255" text-anchor="middle" font-size="12" font-weight="850">ENTRADA PEATONAL</text>
  </g>
  </g>

  <g id="paso_peatonal_03_resaltado">
    <path class="walk" d="M400 205H426V660H400Z"/>
  </g>

  <g id="identificadores_pasos" aria-label="Identificadores de pasos">
    <g aria-label="Paso 01, paso horizontal norte">
      <rect class="step-marker" x="706" y="187" width="48" height="24" rx="9"/>
      <text class="step-label" x="730" y="204">P01</text>
    </g>
    <g aria-label="Paso 02, paso horizontal superior">
      <rect class="step-marker" x="372" y="426" width="48" height="24" rx="9"/>
      <text class="step-label" x="396" y="443">P02</text>
    </g>
    <g aria-label="Paso 03, paso longitudinal este">
      <rect class="step-marker" x="400" y="590" width="48" height="24" rx="9"/>
      <text class="step-label" x="424" y="607">P03</text>
    </g>
    <g aria-label="Paso 06, fila del comedor" transform="translate(-14 100)">
      <rect x="389" y="688" width="112" height="38" rx="9" fill="#0a84ff" stroke="#a6d5ff" stroke-width="3"/>
      <text x="445" y="704" text-anchor="middle" font-size="9" font-weight="900" style="fill:#07111f">P06 · FILA DEL</text>
      <text x="445" y="718" text-anchor="middle" font-size="10" font-weight="900" style="fill:#07111f">COMEDOR</text>
    </g>
    <g aria-label="Paso 07, paso horizontal inferior">
      <rect class="step-marker" x="206" y="651" width="48" height="24" rx="9"/>
      <text class="step-label" x="230" y="668">P07</text>
    </g>
    <g aria-label="Paso 08, pasillo a la derecha de Portería que conecta P07 con el sur" transform="translate(0 100)">
      <rect class="step-marker" x="138" y="818" width="48" height="24" rx="9"/>
      <text class="step-label" x="162" y="835">P08</text>
    </g>
  </g>

  </g>
  <g transform="translate(0 -10)">
  <g id="leyenda">
    <rect x="30" y="1312" width="860" height="1" fill="#35587d"/>
    <circle cx="74" cy="1332" r="9" fill="#168dff"/>
    <text x="91" y="1338" font-size="14" font-weight="700">Aulas</text>
    <circle cx="181" cy="1332" r="9" fill="#0a84ff"/>
    <text x="198" y="1338" font-size="14" font-weight="700">Pabellón</text>
    <circle cx="314" cy="1332" r="9" fill="#1464b5"/>
    <text x="331" y="1338" font-size="14" font-weight="700">Gimnasio</text>
    <circle cx="455" cy="1332" r="9" fill="#168dff"/>
    <text x="472" y="1338" font-size="14" font-weight="700">Cancha</text>
    <path d="M574 1332h34" class="route-line"/>
    <text x="616" y="1338" font-size="14" font-weight="700">Acceso</text>
  </g>
  </g>
  <g id="cuadricula_temporal_mapa" pointer-events="none" aria-label="Cuadrícula temporal de 20 unidades, coordenadas cada 40">
    <rect width="920" height="1350" fill="url(#map_grid_minor)"/>
    <rect width="920" height="1350" fill="url(#map_grid_major)"/>
  </g>
  __MAP_GRID_COORDINATES__
</svg>
"""

def spreadsheet_row(index: int) -> str:
    label = ""
    while index:
        index, remainder = divmod(index - 1, 26)
        label = chr(65 + remainder) + label
    return label

grid_coordinates = ['<g id="coordenadas_temporales_mapa" fill="#fff" stroke="#07111f" stroke-width="2.5" paint-order="stroke" font-size="9" font-weight="900">']
for x in range(0, 920, 40):
    grid_coordinates.append(f'    <text x="{x + 2}" y="95">{x}</text>')
for row, y in enumerate(range(0, 1350, 40), start=1):
    grid_coordinates.append(f'    <text x="4" y="{y + 13}">{spreadsheet_row(row)}</text>')
grid_coordinates.append("  </g>")
SVG = SVG.replace("__MAP_GRID_COORDINATES__", "\n  ".join(grid_coordinates))

OUTPUT.write_text(SVG, encoding="utf-8")
print(f"SVG generado: {OUTPUT}")

DETAIL_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="__CANVAS_HEIGHT__" viewBox="0 0 1000 __CANVAS_HEIGHT__"
     role="img" aria-labelledby="title description">
  <title id="title">Zona central - __LEVEL_LABEL__</title>
  <desc id="description">Esquema provisional de salas y escaleras trazado a partir del croquis del equipo. Las posiciones de las salas se repiten en ambos niveles, pero sus nombres y medidas aún deben confirmarse.</desc>
  <defs>
    <style>
      text { font-family: system-ui, "Segoe UI", sans-serif; fill: #183246; }
      .on-dark { fill: #fff !important; }
      .header { fill: #1f3a5f; }
      .walk { fill: #e9eff2; stroke: #b5c4cd; stroke-width: 2; }
      .floor { fill: #e4ebef; stroke: #c0cbd1; stroke-width: 2; }
      .wing { fill: #dce7ed; stroke: #536f81; stroke-width: 3; }
      .room { fill: #fff; stroke: #cf554b; stroke-width: 4; }
      .room-alt { fill: #fff8f5; stroke: #cf554b; stroke-width: 4; }
      .block-label { fill: #1f3a5f; font-size: 20px; font-weight: 850; text-anchor: middle; }
      .room-label { font-size: 15px; font-weight: 750; text-anchor: middle; }
      .room-code { font-size: 14px; font-weight: 850; text-anchor: middle; fill: #a43c35; }
      .note { fill: #4b6577; font-size: 15px; font-weight: 650; }
      .stair-base { fill: #29343b; stroke: #10191e; stroke-width: 2; }
      .tread { stroke: #fff; stroke-width: 3; }
      .stair-arrow { fill: none; stroke: #fff; stroke-width: 3; }
    </style>
    <marker id="up-arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto">
      <path d="M0 0L9 4.5L0 9Z" fill="#fff"/>
    </marker>
  </defs>
  <rect width="1000" height="__CANVAS_HEIGHT__" fill="#f2f6f8"/>
  <rect class="header" x="30" y="24" width="940" height="68" rx="16"/>
  <text class="on-dark" x="500" y="67" text-anchor="middle" font-size="29" font-weight="900">ZONA CENTRAL · __LEVEL_LABEL__</text>
  <text class="note" x="500" y="122" text-anchor="middle">Esquema provisional basado en el croquis · los recintos aún no tienen nombre definitivo</text>

  <rect id="planta_continua" class="floor" x="45" y="145" width="910" height="__FLOOR_HEIGHT__" rx="12"/>

  <g transform="translate(0, __ROOM_OFFSET__)">
  __ROOM_LAYOUT__
  </g>

  <!-- Each room group has its own stair; opposing flights share each footprint. -->
  <g id="escalera_provisional___LEVEL___01" transform="translate(-10, __STAIR_OFFSET__)">
    <rect class="stair-base" x="214" y="214" width="46" height="136" rx="5"/>
    <path class="tread" d="M217 225H257M217 236H257M217 247H257M217 258H257M217 269H257M217 280H257M217 291H257M217 302H257M217 313H257M217 324H257M217 335H257"/>
    <path class="stair-arrow" d="M226 337V231" marker-end="url(#up-arrow)"/>
    <path class="stair-arrow" d="M248 230V336" marker-end="url(#up-arrow)"/>
  </g>
  <g id="escalera_provisional___LEVEL___02" transform="translate(20, __STAIR_OFFSET__)">
    <rect class="stair-base" x="645" y="214" width="46" height="136" rx="5"/>
    <path class="tread" d="M648 225H688M648 236H688M648 247H688M648 258H688M648 269H688M648 280H688M648 291H688M648 302H688M648 313H688M648 324H688M648 335H688"/>
    <path class="stair-arrow" d="M657 337V231" marker-end="url(#up-arrow)"/>
    <path class="stair-arrow" d="M679 230V336" marker-end="url(#up-arrow)"/>
  </g>

  <g id="room_id_legend" transform="translate(0, __LEGEND_OFFSET__)">
    <rect class="room" x="70" y="570" width="36" height="28" rx="4"/>
    <text class="note" x="118" y="590">Sala provisional · esquema aproximado</text>
    <rect class="stair-base" x="541" y="566" width="28" height="36" rx="4"/>
    <path class="tread" d="M546 570V598M553 570V598M560 570V598"/>
    <text class="note" x="581" y="590">Dos tramos opuestos, misma huella</text>
    <text class="note" x="70" y="622">Piso continuo, sin pasillos marcados; recintos y medidas provisionales.</text>
  </g>
</svg>
"""

GROUND_ROOM_LAYOUT = """<g id="sector_j">
    <rect class="wing" x="70" y="198" width="135" height="292" rx="12"/>
    <text class="block-label" x="137" y="191">J</text>
    <rect id="sala_provisional_planta_baja_01" class="room" x="84" y="211" width="107" height="78" rx="7"/>
    <rect id="sala_provisional_planta_baja_02" class="room-alt" x="84" y="300" width="107" height="78" rx="7"/>
    <rect id="sala_provisional_planta_baja_03" class="room" x="84" y="389" width="107" height="87" rx="7"/>
  </g>
  <g id="sector_b">
    <rect class="wing" x="285" y="198" width="350" height="142" rx="12"/>
    <text class="block-label" x="460" y="191">B</text>
    <rect id="sala_provisional_planta_baja_04" class="room" x="300" y="211" width="96" height="55" rx="7"/>
    <rect id="sala_provisional_planta_baja_05" class="room-alt" x="409" y="211" width="96" height="55" rx="7"/>
    <rect id="sala_provisional_planta_baja_06" class="room" x="518" y="211" width="102" height="55" rx="7"/>
    <rect id="sala_provisional_planta_baja_07" class="room-alt" x="300" y="278" width="150" height="48" rx="7"/>
    <rect id="sala_provisional_planta_baja_08" class="room" x="463" y="278" width="157" height="48" rx="7"/>
  </g>
  <g id="sector_intermedio">
    <rect id="sala_provisional_planta_baja_13" class="room" x="285" y="356" width="142" height="62" rx="7"/>
    <rect id="sala_provisional_planta_baja_14" class="room-alt" x="439" y="356" width="196" height="62" rx="7"/>
    <rect id="sala_provisional_planta_baja_15" class="room-alt" x="285" y="432" width="118" height="58" rx="7"/>
    <rect id="sala_provisional_planta_baja_16" class="room" x="415" y="432" width="220" height="58" rx="7"/>
  </g>
  <g id="sector_d">
    <rect class="wing" x="700" y="198" width="230" height="142" rx="12"/>
    <text class="block-label" x="815" y="191">D</text>
    <rect id="sala_provisional_planta_baja_17" class="room" x="714" y="211" width="91" height="116" rx="7"/>
    <rect id="sala_provisional_planta_baja_18" class="room-alt" x="823" y="211" width="93" height="116" rx="7"/>
  </g>
  <g id="sector_c">
    <rect class="wing" x="700" y="360" width="230" height="130" rx="12"/>
    <text class="block-label" x="815" y="353">C</text>
    <rect id="sala_provisional_planta_baja_19" class="room-alt" x="714" y="373" width="91" height="103" rx="7"/>
    <rect id="sala_provisional_planta_baja_20" class="room" x="823" y="373" width="93" height="103" rx="7"/>
  </g>"""

UPPER_ROOM_LAYOUT = """<g id="salas_lado_izquierdo_escalera_01">
    <text class="block-label" x="132" y="191">J</text>
    <rect id="sala_provisional_segundo_piso_01" class="room" x="70" y="214" width="126" height="100" rx="9"/>
    <text class="room-code" x="133" y="269">P2-01</text>
    <rect id="sala_provisional_segundo_piso_02" class="room-alt" x="70" y="333" width="126" height="100" rx="9"/>
    <text class="room-code" x="133" y="388">P2-02</text>
  </g>
  <g id="salas_lado_derecho_escalera_01">
    <text class="block-label" x="324" y="191">B</text>
    <rect id="sala_provisional_segundo_piso_03" class="room" x="258" y="214" width="142" height="100" rx="9"/>
    <text class="room-code" x="329" y="269">P2-03</text>
    <rect id="sala_provisional_segundo_piso_04" class="room-alt" x="258" y="333" width="142" height="100" rx="9"/>
    <text class="room-code" x="329" y="388">P2-04</text>
  </g>
  <g id="salas_lado_izquierdo_escalera_02">
    <text class="block-label" x="578" y="191">B</text>
    <rect id="sala_provisional_segundo_piso_05" class="room-alt" x="530" y="214" width="126" height="100" rx="9"/>
    <text class="room-code" x="593" y="269">P2-05</text>
    <rect id="sala_provisional_segundo_piso_06" class="room" x="530" y="333" width="126" height="100" rx="9"/>
    <text class="room-code" x="593" y="388">P2-06</text>
  </g>
  <g id="salas_lado_derecho_escalera_02">
    <text class="block-label" x="837" y="191">D / C</text>
    <rect id="sala_provisional_segundo_piso_07" class="room" x="720" y="214" width="230" height="100" rx="9"/>
    <text class="room-code" x="835" y="269">P2-07</text>
    <rect id="sala_provisional_segundo_piso_08" class="room-alt" x="720" y="333" width="230" height="100" rx="9"/>
    <text class="room-code" x="835" y="388">P2-08</text>
  </g>"""

DETAIL_DIR = OUTPUT.parent / "svg"
DETAIL_DIR.mkdir(exist_ok=True)
for level, level_label, filename, room_layout in (
    ("planta_baja", "PLANTA BAJA", "zona_central_planta_baja.svg", GROUND_ROOM_LAYOUT),
    ("segundo_piso", "SEGUNDO PISO", "zona_central_segundo_piso.svg", UPPER_ROOM_LAYOUT),
):
    is_upper_floor = level == "segundo_piso"
    detail_svg = (
        DETAIL_TEMPLATE.replace("__LEVEL_LABEL__", level_label)
        .replace("__LEVEL__", level)
        .replace("__ROOM_LAYOUT__", room_layout)
        .replace("__CANVAS_HEIGHT__", "790" if is_upper_floor else "650")
        .replace("__FLOOR_HEIGHT__", "514" if is_upper_floor else "394")
        .replace("__ROOM_OFFSET__", "130" if is_upper_floor else "0")
        .replace("__STAIR_OFFSET__", "-32" if is_upper_floor else "0")
        .replace("__LEGEND_OFFSET__", "120" if is_upper_floor else "0")
    )
    detail_path = DETAIL_DIR / filename
    detail_path.write_text(detail_svg, encoding="utf-8")
    print(f"SVG de detalle generado: {detail_path}")
