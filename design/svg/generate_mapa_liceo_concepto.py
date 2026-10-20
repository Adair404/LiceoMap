#!/usr/bin/env python3
"""Generate a simplified, mobile-readable redraw of the Liceo B-4 plan."""

from pathlib import Path

OUTPUT = Path(__file__).with_name("mapa_liceo_concepto.svg")

SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="880" height="1320" viewBox="0 0 880 1320"
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
      .walk { fill: #14263d; stroke: #294663; stroke-width: 2; }
      .queue-walk { fill: #0a84ff; stroke: #35587d; stroke-width: 2; }
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
  </defs>

  <rect width="880" height="1320" fill="#07111f"/>

  <!-- Orientation and street names make the plan readable without relying on color. -->
  <g id="orientacion">
    <rect class="road" x="30" y="24" width="820" height="58" rx="14"/>
    <text class="road-label" x="380" y="60" text-anchor="middle">CALLE ALFREDO THOMAS · NORTE</text>
    <path d="M810 98V54" stroke="#f4f8ff" stroke-width="4" marker-end="url(#arrow)"/>
    <text class="north" x="810" y="42" text-anchor="middle">N</text>
  </g>

  <rect id="recinto_liceo" class="site" x="30" y="98" width="820" height="1080" rx="22"/>
  <g id="circulaciones">
    <path id="paso_peatonal_01" class="walk" d="M48 187H832V211H48Z"/>
    <path id="paso_peatonal_02" class="walk" d="M48 426H532V451H48Z"/>
    <path id="paso_peatonal_04" class="walk" d="M48 1032H832V1058H48Z"/>
    <path id="paso_peatonal_05" class="walk" d="M163 190H188V426H163Z"/>
    <path id="paso_peatonal_03" class="walk" d="M494 205H520V650H494Z"/>
    <path id="paso_peatonal_07" class="walk" d="M48 650H832V676H48Z"/>
    <path id="paso_peatonal_08_pasillo_porteria" class="walk" d="M148 676H176V900H210V1032H190V912H148Z"/>
  </g>

  <!-- The central patio is the entire open quadrangle between the surrounding walkways. -->
  <g transform="translate(0 -40)">
  <g id="patio_central">
    <rect x="188" y="716" width="318" height="234" fill="#10233a"/>
    <rect x="194" y="722" width="306" height="222" fill="url(#paving)"/>
    <rect x="208" y="738" width="112" height="72" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <rect x="330" y="738" width="112" height="72" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <rect x="208" y="826" width="112" height="98" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <rect x="330" y="826" width="112" height="98" rx="6" fill="#162b46" stroke="#4f7193" stroke-width="2"/>
    <rect x="245" y="812" width="204" height="29" rx="11" fill="#0d315b"/>
    <text class="block-name" x="347" y="833" text-anchor="middle">PATIO CENTRAL</text>
  </g>
  <path id="paso_peatonal_06_fila_comedor" class="queue-walk" d="M424 716H466V947H424Z"/>
  </g>

  <!-- Block L faces Calle Alfredo Thomas. Room divisions are schematic. -->
  <g id="bloque_l" class="building">
    <rect x="70" y="112" width="620" height="72" rx="8" fill="#17385f"/>
    <path class="room" d="M78 120H189V176H78Z"/>
    <path class="room-alt" d="M193 120H304V176H193Z"/>
    <path class="room" d="M308 120H419V176H308Z"/>
    <path class="room-alt" d="M423 120H534V176H423Z"/>
    <path class="room" d="M538 120H682V176H538Z"/>
  </g>
  <text class="small-label" x="380" y="205" text-anchor="middle">L · PABELLÓN NORTE</text>

  <!-- K: recognizable indoor court, with the west-side service wing shown separately. -->
  <g id="anexo_bloque_k" class="building">
    <rect x="76" y="222" width="75" height="194" rx="8" fill="#15385c"/>
    <path class="room" d="M84 232H143V286H84Z"/>
    <path class="room-alt" d="M84 292H143V346H84Z"/>
    <path class="room" d="M84 352H143V406H84Z"/>
  </g>
  <g id="bloque_k" class="building">
    <rect x="160" y="222" width="330" height="194" rx="12" class="gym"/>
    <rect x="164" y="224" width="322" height="24" rx="8" fill="#0d315b"/>
    <g id="cancha_gimnasio_k">
      <rect x="181" y="252" width="288" height="134" rx="4" fill="#1d69b7" stroke="#fff" stroke-width="3"/>
      <path class="court-mark" d="M325 252V386M181 319H469"/>
      <circle class="court-mark" cx="325" cy="319" r="25"/>
      <path class="court-mark" d="M181 287h30v64h-30M469 287h-30v64h30"/>
    </g>
    <rect x="262" y="391" width="126" height="25" rx="8" fill="#0d315b"/>
    <text class="on-dark" x="325" y="241" text-anchor="middle" font-size="14" font-weight="850">K · GIMNASIO</text>
  </g>

  <!-- E and the open stage area; the latter is also used as a court. -->
  <g id="bloque_e" class="building">
    <rect x="520" y="218" width="104" height="168" rx="10" class="admin"/>
    <rect x="524" y="222" width="96" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room" x="530" y="250" width="84" height="50" rx="4"/>
    <rect class="room-alt" x="530" y="306" width="84" height="74" rx="4"/>
    <text class="on-dark" x="572" y="239" text-anchor="middle" font-size="13" font-weight="850">E · PABELLÓN</text>
  </g>
  <g id="bloque_d_pabellon" class="building">
    <rect x="520" y="390" width="104" height="168" rx="10" class="admin"/>
    <rect x="524" y="394" width="96" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room" x="530" y="422" width="84" height="50" rx="4"/>
    <rect class="room-alt" x="530" y="478" width="84" height="74" rx="4"/>
    <text class="on-dark" x="572" y="411" text-anchor="middle" font-size="13" font-weight="850">D · PABELLÓN</text>
  </g>
  <g id="bloque_c_este" class="building">
    <rect x="520" y="562" width="104" height="84" rx="10" class="admin"/>
    <rect x="524" y="566" width="96" height="24" rx="7" fill="#0d4d96"/>
    <rect class="room-alt" x="530" y="594" width="84" height="46" rx="4"/>
    <text class="on-dark" x="572" y="583" text-anchor="middle" font-size="13" font-weight="850">C · PABELLÓN</text>
  </g>
  <g transform="translate(0 -40)">
  <g id="escenario_cancha_este" aria-label="Escenario, espacio abierto usado como cancha">
    <rect x="532" y="716" width="180" height="234" fill="#12243a" stroke="#35587d" stroke-width="3"/>
    <g id="gimnasio_escenario" aria-label="Gimnasio">
      <rect x="532" y="876" width="101" height="74" fill="#183452" stroke="#17385f" stroke-width="2"/>
      <text x="582" y="918" text-anchor="middle" font-size="12" font-weight="850">GIMNASIO</text>
    </g>
    <g id="kiosco_escenario" aria-label="Kiosco">
      <rect x="633" y="876" width="79" height="74" fill="#1a3d66" stroke="#35587d" stroke-width="2"/>
      <text x="672" y="918" text-anchor="middle" font-size="12" font-weight="850">KIOSCO</text>
    </g>
  </g>
  </g>

  <!-- D and C are two distinct teaching wings; letter markers remain legible at phone scale. -->
  <g id="bloque_d" class="building">
    <rect x="386" y="466" width="104" height="88" rx="10" class="classroom"/>
    <rect x="390" y="470" width="96" height="24" rx="7" fill="#168dff"/>
    <rect class="room" x="394" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="442" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <text style="fill:#07111f" x="438" y="487" text-anchor="middle" font-size="12" font-weight="850">D · AULAS</text>
  </g>
  <g id="bloque_c" class="building">
    <rect x="386" y="560" width="104" height="88" rx="8" class="classroom"/>
    <rect x="390" y="564" width="96" height="24" rx="6" fill="#168dff"/>
    <rect class="room" x="394" y="594" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="442" y="594" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <text style="fill:#07111f" x="438" y="581" text-anchor="middle" font-size="12" font-weight="850">C · AULAS</text>
  </g>

  <!-- B is the central teaching / administration wing. -->
  <g id="bloque_b" class="building">
    <rect x="184" y="466" width="198" height="182" rx="10" class="classroom"/>
    <rect x="190" y="470" width="186" height="24" rx="7" fill="#168dff"/>
    <rect class="room" x="194" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="246" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="298" y="500" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="194" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room" x="246" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <rect class="room-alt" x="298" y="570" width="44" height="44" rx="4" data-area-util="49.70 m2" data-area-ejes="51.84 m2" data-medida-ejes="7.2 x 7.2 m">
      <title>Aula tipo del plano: 49,70 m2 útiles; 51,84 m2 por ejes (7,2 x 7,2 m nominales).</title>
    </rect>
    <text style="fill:#07111f" x="283" y="487" text-anchor="middle" font-size="12" font-weight="850">B · AULAS / ADMIN.</text>
  </g>

  <!-- West-side J, I and F are shown as long, separate wings as on the plan. -->
  <g id="bloque_j" class="building">
    <rect x="74" y="452" width="74" height="186" rx="10" class="admin"/>
    <path class="room" d="M83 460.2H139V498.7H83Z"/>
    <path class="room-alt" d="M83 503.6H139V543.2H83Z"/>
    <path class="room" d="M83 548.2H139V587.7H83Z"/>
    <path class="room-alt" d="M83 592.6H139V628.8H83Z"/>
    <rect x="90" y="519.8" width="42" height="52" rx="12" fill="#0d4d96"/>
    <text class="block-letter" x="111" y="554.9" text-anchor="middle">J</text>
  </g>
  <g transform="translate(0 -40)">
  <g id="bloque_i" class="building">
    <rect x="74" y="732" width="74" height="99" rx="10" fill="#168dff"/>
    <path class="room" d="M83 741H139V777H83Z"/>
    <path class="room-alt" d="M83 783H139V822H83Z"/>
    <rect x="90" y="755" width="42" height="50" rx="12" fill="#168dff"/>
    <text class="block-letter" x="111" y="790" text-anchor="middle">I</text>
  </g>
  <g id="bloque_f" class="building">
    <rect x="74" y="842" width="74" height="98" rx="10" fill="#168dff"/>
    <path class="room" d="M83 851H139V886H83Z"/>
    <path class="room-alt" d="M83 892H139V931H83Z"/>
    <rect x="90" y="867" width="42" height="50" rx="12" fill="#168dff"/>
    <text class="block-letter" x="111" y="902" text-anchor="middle">F</text>
  </g>
  </g>

  <!-- Eastern outdoor court shown in the architectural plan; not a multicancha. -->
  <g id="patio_deportivo_este">
    <rect x="628" y="295" width="159" height="263" rx="12" fill="#087bff" stroke="#24486d" stroke-width="4"/>
    <rect class="court-mark" x="641" y="309" width="133" height="226"/>
    <path class="court-mark" d="M641 422H774"/>
    <circle class="court-mark" cx="707.5" cy="422" r="22"/>
    <rect x="637.5" y="502" width="140" height="28" rx="7" fill="#0754ad"/>
    <text class="on-dark" x="707.5" y="521" text-anchor="middle" font-size="13" font-weight="850">CANCHA</text>
  </g>
  <g id="aulas_g_provisional" class="building">
    <rect x="628" y="218" width="159" height="73" rx="10" class="classroom"/>
    <text style="fill:#07111f" x="707.5" y="259" text-anchor="middle" font-size="14" font-weight="850">AULAS G</text>
  </g>

  <!-- Provisional southern volumes sit directly behind the dining room; internal room layouts remain unconfirmed. -->
  <g transform="translate(0 -40)">
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
      <text x="292" y="985" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">AULAS · 1° PISO</text>
      <text x="292" y="1036" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">AULAS · 2° PISO</text>
    </g>
    <g id="aulas_tras_comedor_derecha_provisional" aria-label="Estructura de aulas de dos pisos; distribución pendiente">
      <rect x="374" y="950" width="176" height="112" rx="6" fill="#168dff" stroke="#24486d" stroke-width="3"/>
      <rect x="382" y="958" width="160" height="44" rx="4" fill="#eaf3ff" stroke="#6685a7" stroke-width="2"/>
      <rect x="382" y="1009" width="160" height="44" rx="4" fill="#fff" stroke="#6685a7" stroke-width="2"/>
      <text x="462" y="985" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">AULAS · 1° PISO</text>
      <text x="462" y="1036" text-anchor="middle" font-size="12" font-weight="850" style="fill:#07111f">AULAS · 2° PISO</text>
    </g>
  </g>

  <!-- Portería and the public entrance align with Avenida Loa. -->
  <g id="bloque_h" class="building">
    <g id="sector_utp_provisional">
      <rect x="48" y="952" width="72" height="120" rx="8" fill="#17385f"/>
      <rect x="56" y="960" width="56" height="104" rx="5" fill="#3c8dff"/>
      <text style="fill:#07111f" x="84" y="1016" text-anchor="middle" font-size="11" font-weight="850">UTP</text>
    </g>
    <g id="sector_porteria">
      <rect x="128" y="952" width="62" height="120" rx="8" fill="#17385f"/>
      <rect x="136" y="960" width="46" height="104" rx="5" fill="#eaf3ff"/>
      <text x="159" y="1008" text-anchor="middle" font-size="8" font-weight="850" style="fill:#07111f">PORTERÍA</text>
      <text x="159" y="1024" text-anchor="middle" font-size="10" font-weight="850" style="fill:#07111f">H</text>
    </g>
  </g>
  <g id="zona_estacionamiento">
    <rect x="554" y="950" width="158" height="122" rx="8" fill="#142a45" stroke="#35587d" stroke-width="3"/>
    <path d="M566 978H700M566 1008H700M566 1038H700M594 952V1070M628 952V1070M662 952V1070M696 952V1070" stroke="#35587d" stroke-width="2"/>
    <rect x="586" y="954" width="94" height="20" rx="7" fill="#17385f"/>
    <text class="on-dark" x="633" y="969" text-anchor="middle" font-size="12" font-weight="850">PARKING</text>
  </g>

  <g id="avenida_loa">
    <rect class="road" x="30" y="1230" width="820" height="72" rx="14"/>
    <text class="road-label" x="380" y="1274" text-anchor="middle">AVENIDA LOA · ACCESO PRINCIPAL</text>
  </g>
  <g id="acceso_peatonal_loa">
    <path d="M372 1230V1098" class="path-line"/>
    <path d="M372 1230V1098" class="route-line" marker-end="url(#arrow)"/>
    <circle class="node" cx="372" cy="1225" r="9"/>
    <rect x="290" y="1240" width="164" height="20" rx="8" fill="#168dff"/>
    <text style="fill:#07111f" x="372" y="1255" text-anchor="middle" font-size="12" font-weight="850">ENTRADA PEATONAL</text>
  </g>
  </g>

  <g id="identificadores_pasos" aria-label="Identificadores de pasos">
    <g aria-label="Paso 01, paso horizontal norte">
      <rect class="step-marker" x="746" y="187" width="48" height="24" rx="9"/>
      <text class="step-label" x="770" y="204">P01</text>
    </g>
    <g aria-label="Paso 02, paso horizontal superior">
      <rect class="step-marker" x="466" y="426" width="48" height="24" rx="9"/>
      <text class="step-label" x="490" y="443">P02</text>
    </g>
    <g aria-label="Paso 03, paso longitudinal este">
      <rect class="step-marker" x="494" y="590" width="48" height="24" rx="9"/>
      <text class="step-label" x="518" y="607">P03</text>
    </g>
    <g aria-label="Paso 04, paso horizontal sur">
      <rect class="step-marker" x="160" y="1033" width="48" height="24" rx="9"/>
      <text class="step-label" x="184" y="1050">P04</text>
    </g>
    <g aria-label="Paso 05, paso longitudinal oeste">
      <rect class="step-marker" x="151" y="393" width="48" height="24" rx="9"/>
      <text class="step-label" x="175" y="410">P05</text>
    </g>
    <g aria-label="Paso 06, fila del comedor">
      <rect x="389" y="688" width="112" height="38" rx="9" fill="#0a84ff" stroke="#a6d5ff" stroke-width="3"/>
      <text x="445" y="704" text-anchor="middle" font-size="9" font-weight="900" style="fill:#07111f">P06 · FILA DEL</text>
      <text x="445" y="718" text-anchor="middle" font-size="10" font-weight="900" style="fill:#07111f">COMEDOR</text>
    </g>
    <g aria-label="Paso 07, paso horizontal inferior">
      <rect class="step-marker" x="206" y="651" width="48" height="24" rx="9"/>
      <text class="step-label" x="230" y="668">P07</text>
    </g>
    <g aria-label="Paso 08, pasillo a la derecha de Portería que conecta P07 con P04">
      <rect class="step-marker" x="138" y="818" width="48" height="24" rx="9"/>
      <text class="step-label" x="162" y="835">P08</text>
    </g>
  </g>

  <g transform="translate(0 -40)">
  <g id="leyenda">
    <rect x="30" y="1312" width="820" height="1" fill="#35587d"/>
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
    <rect width="880" height="1320" fill="url(#map_grid_minor)"/>
    <rect width="880" height="1320" fill="url(#map_grid_major)"/>
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
for x in range(0, 880, 40):
    grid_coordinates.append(f'    <text x="{x + 2}" y="95">{x}</text>')
for row, y in enumerate(range(0, 1320, 40), start=1):
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
