import streamlit as st
import streamlit.components.v1 as components
import os
import base64


def show_scence2():

    # ============================================================
    # ASSETS
    # ============================================================

    assets_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "assets"
    )

    def image_data(filename):
        path = os.path.join(assets_dir, filename)

        if not os.path.exists(path):
            return ""

        try:
            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")

            ext = filename.lower().split(".")[-1]

            if ext == "png":
                mime = "image/png"
            elif ext == "webp":
                mime = "image/webp"
            else:
                mime = "image/jpeg"

            return f"data:{mime};base64,{encoded}"

        except Exception:
            return ""

    textures = {
        "galaxy": image_data("galaxy.jpg"),
        "sun": image_data("sun.jpg"),

        "mercury": image_data("mercury.jpg"),
        "venus": image_data("venus.jpg"),
        "earth": image_data("earth.jpg"),
        "mars": image_data("mars.jpg"),
        "jupiter": image_data("jupiter.jpg"),
        "saturn": image_data("saturn.jpg"),
        "uranus": image_data("uranus.jpg"),
        "neptune": image_data("neptune.jpg"),

        "moon": image_data("moon.jpg"),

        "io": image_data("io.jpg"),
        "europa": image_data("europa.jpg"),
        "ganymede": image_data("ganymede.jpg"),
        "callisto": image_data("callisto.jpg"),

        "sat2": image_data("sat2vuu2.jpg"),
        "sat5": image_data("sat5vuu2.jpg"),
        "sat6": image_data("sat6fss1.jpg"),

        "ura1": image_data("ura1vuu2.jpg"),
        "ura3": image_data("ura3vuu2.jpg"),
        "ura4": image_data("ura4vuu2.jpg"),
        "ura5": image_data("ura5vuu2.jpg"),

        "pluto": image_data("pluto.jpg"),
    }

    # ============================================================
    # THREE.JS APPLICATION
    # ============================================================

    html = r"""
<!DOCTYPE html>
<html>
<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0,
               maximum-scale=1.0,
               user-scalable=no">

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html,
body {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background: #000;
    font-family: Arial, Helvetica, sans-serif;
}

#space {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
}

canvas {
    display: block;
}

/* ============================================================
   TOP HUD
   ============================================================ */

#topHUD {
    position: fixed;
    top: 22px;
    left: 28px;
    z-index: 20;
    pointer-events: none;
}

#brand {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 6px;
    color: white;
    text-shadow:
        0 0 10px rgba(255,255,255,.35),
        0 0 25px rgba(100,170,255,.35);
}

#subtitle {
    margin-top: 5px;
    color: rgba(210,225,255,.72);
    font-size: 10px;
    letter-spacing: 3px;
}

/* ============================================================
   RIGHT CONTROL PANEL
   ============================================================ */

#controlPanel {
    position: fixed;
    top: 22px;
    right: 22px;
    width: 245px;
    max-height: calc(100vh - 44px);
    overflow-y: auto;
    z-index: 30;

    padding: 17px;

    border: 1px solid rgba(130,180,255,.28);
    border-radius: 15px;

    background:
        linear-gradient(
            145deg,
            rgba(8,16,32,.88),
            rgba(3,7,16,.78)
        );

    backdrop-filter: blur(15px);

    box-shadow:
        0 15px 50px rgba(0,0,0,.5),
        inset 0 0 25px rgba(100,150,255,.04);
}

#controlPanel::-webkit-scrollbar {
    width: 4px;
}

#controlPanel::-webkit-scrollbar-thumb {
    background: rgba(150,190,255,.35);
    border-radius: 10px;
}

.panelTitle {
    color: white;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.section {
    margin-bottom: 17px;
}

button {
    width: 100%;
    border: 1px solid rgba(140,190,255,.22);
    background: rgba(255,255,255,.045);
    color: #dbe8ff;

    padding: 9px 10px;
    border-radius: 8px;

    margin-bottom: 6px;

    cursor: pointer;

    font-size: 10px;
    letter-spacing: 1px;

    transition:
        background .2s,
        border .2s,
        transform .2s;
}

button:hover {
    background: rgba(110,165,255,.16);
    border-color: rgba(160,205,255,.6);
    transform: translateY(-1px);
}

button.active {
    background: rgba(90,145,255,.20);
    border-color: rgba(140,195,255,.65);
}

.controlRow {
    display: flex;
    gap: 6px;
}

.controlRow button {
    flex: 1;
}

.sliderLabel {
    display: flex;
    justify-content: space-between;

    color: rgba(215,230,255,.72);

    font-size: 9px;
    letter-spacing: 1px;

    margin-bottom: 7px;
}

input[type="range"] {
    width: 100%;
    accent-color: #83b8ff;
}

/* ============================================================
   CAMERA BUTTONS
   ============================================================ */

.cameraGrid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
}

.cameraGrid button {
    margin: 0;
    padding: 8px 4px;
    font-size: 8px;
}

/* ============================================================
   INFO PANEL
   ============================================================ */

#infoPanel {
    position: fixed;
    left: 25px;
    bottom: 25px;

    width: 330px;
    max-height: 390px;

    overflow-y: auto;

    z-index: 25;

    padding: 18px;

    border-radius: 15px;

    border: 1px solid rgba(120,180,255,.28);

    background:
        linear-gradient(
            145deg,
            rgba(5,12,25,.92),
            rgba(2,6,15,.85)
        );

    backdrop-filter: blur(18px);

    box-shadow:
        0 20px 60px rgba(0,0,0,.55),
        inset 0 0 30px rgba(100,160,255,.03);

    color: white;

    display: none;
}

#infoPanel.visible {
    display: block;
}

#infoPanel::-webkit-scrollbar {
    width: 4px;
}

#infoPanel::-webkit-scrollbar-thumb {
    background: rgba(150,190,255,.35);
}

#infoName {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 3px;
}

#infoType {
    color: #91bbff;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.infoGrid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}

.infoItem {
    padding: 8px;
    border-radius: 7px;

    background: rgba(255,255,255,.035);

    border: 1px solid rgba(150,190,255,.08);
}

.infoLabel {
    font-size: 7px;
    color: rgba(210,225,255,.5);
    letter-spacing: 1px;
    margin-bottom: 3px;
}

.infoValue {
    font-size: 10px;
    color: white;
}

#infoFacts {
    margin-top: 12px;

    color: rgba(220,232,255,.72);

    font-size: 10px;
    line-height: 1.6;
}

/* ============================================================
   BOTTOM STATUS
   ============================================================ */

#status {
    position: fixed;
    bottom: 17px;
    right: 285px;

    color: rgba(210,225,255,.48);

    font-size: 8px;
    letter-spacing: 2px;

    z-index: 20;

    pointer-events: none;
}

/* ============================================================
   LABELS
   ============================================================ */

.planetLabel {
    position: fixed;
    z-index: 15;

    pointer-events: none;

    color: white;

    font-size: 9px;
    letter-spacing: 1.5px;

    padding: 4px 7px;

    border-left: 1px solid rgba(160,200,255,.7);

    background: rgba(2,8,18,.55);

    backdrop-filter: blur(5px);

    transform: translate(-50%, -50%);

    white-space: nowrap;

    text-shadow: 0 0 8px black;
}

/* ============================================================
   LOADING
   ============================================================ */

#loading {
    position: fixed;
    inset: 0;

    z-index: 100;

    display: flex;
    align-items: center;
    justify-content: center;

    background: #000;

    color: white;

    font-size: 11px;
    letter-spacing: 4px;
}

.loaderBox {
    text-align: center;
}

.loaderLine {
    width: 180px;
    height: 1px;

    margin-top: 15px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8db9ff,
            transparent
        );

    animation: load 1.5s infinite;
}

@keyframes load {
    0% {
        opacity: .2;
        transform: scaleX(.2);
    }

    50% {
        opacity: 1;
        transform: scaleX(1);
    }

    100% {
        opacity: .2;
        transform: scaleX(.2);
    }
}

/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    #topHUD {
        top: 12px;
        left: 14px;
    }

    #brand {
        font-size: 17px;
        letter-spacing: 4px;
    }

    #subtitle {
        font-size: 7px;
        letter-spacing: 2px;
    }

    #controlPanel {
        top: auto;
        bottom: 10px;
        right: 10px;

        width: 190px;

        max-height: 48vh;

        padding: 11px;
    }

    #infoPanel {
        left: 10px;
        bottom: 10px;

        width: calc(100% - 210px);

        max-height: 38vh;

        padding: 12px;
    }

    #infoName {
        font-size: 17px;
    }

    #status {
        display: none;
    }

    .planetLabel {
        font-size: 7px;
    }
}

</style>
</head>

<body>

<div id="loading">
    <div class="loaderBox">
        INITIALIZING COSMOSCOPE
        <div class="loaderLine"></div>
    </div>
</div>

<div id="space"></div>

<div id="topHUD">
    <div id="brand">SOLAR SYSTEM EXPLORER</div>
    <div id="subtitle">COSMOSCOPE • 3D ASTRONOMY SIMULATION</div>
</div>

<!-- ============================================================
     CONTROL PANEL
     ============================================================ -->

<div id="controlPanel">

    <div class="section">
        <div class="panelTitle">MISSION CONTROL</div>

        <div class="controlRow">
            <button id="playBtn">❚❚ PAUSE</button>
            <button id="resetBtn">RESET CAMERA</button>
        </div>
    </div>

    <div class="section">

        <div class="panelTitle">SIMULATION SPEED</div>

        <div class="sliderLabel">
            <span>TIME FLOW</span>
            <span id="speedValue">1.0×</span>
        </div>

        <input
            id="speedSlider"
            type="range"
            min="0"
            max="5"
            step="0.1"
            value="1">

    </div>

    <div class="section">

        <div class="panelTitle">VISUAL SYSTEMS</div>

        <button id="orbitBtn" class="active">
            ORBIT PATHS
        </button>

        <button id="labelBtn" class="active">
            PLANET LABELS
        </button>

        <button id="asteroidBtn" class="active">
            ASTEROID BELT
        </button>

    </div>

    <div class="section">

        <div class="panelTitle">TARGET PLANET</div>

        <div class="cameraGrid">

            <button data-target="Sun">SUN</button>
            <button data-target="Mercury">MERCURY</button>

            <button data-target="Venus">VENUS</button>
            <button data-target="Earth">EARTH</button>

            <button data-target="Mars">MARS</button>
            <button data-target="Jupiter">JUPITER</button>

            <button data-target="Saturn">SATURN</button>
            <button data-target="Uranus">URANUS</button>

            <button data-target="Neptune">NEPTUNE</button>
            <button data-target="Pluto">PLUTO</button>

        </div>

    </div>

    <div class="section">

        <div class="panelTitle">NAVIGATION</div>

        <button id="overviewBtn">
            COMPLETE SYSTEM OVERVIEW
        </button>

        <button id="innerBtn">
            INNER PLANETS
        </button>

        <button id="outerBtn">
            OUTER PLANETS
        </button>

    </div>

</div>

<!-- ============================================================
     INFO PANEL
     ============================================================ -->

<div id="infoPanel">

    <div id="infoName">Earth</div>

    <div id="infoType">
        Terrestrial Planet
    </div>

    <div class="infoGrid">

        <div class="infoItem">
            <div class="infoLabel">RADIUS</div>
            <div class="infoValue" id="radiusValue">6,371 km</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">MASS</div>
            <div class="infoValue" id="massValue">1 Earth</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">DISTANCE FROM SUN</div>
            <div class="infoValue" id="distanceValue">1 AU</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">ORBITAL PERIOD</div>
            <div class="infoValue" id="orbitValue">365.25 days</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">ROTATION</div>
            <div class="infoValue" id="rotationValue">23.93 h</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">MOONS</div>
            <div class="infoValue" id="moonsValue">1</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">TEMPERATURE</div>
            <div class="infoValue" id="temperatureValue">15°C</div>
        </div>

        <div class="infoItem">
            <div class="infoLabel">ATMOSPHERE</div>
            <div class="infoValue" id="atmosphereValue">
                N₂ / O₂
            </div>
        </div>

    </div>

    <div id="infoFacts">
        Earth is the only known world currently confirmed to
        support life.
    </div>

</div>

<div id="status">
    DRAG TO ROTATE • SCROLL TO ZOOM • CLICK PLANET TO EXPLORE
</div>

<script>

/* ============================================================
   COSMOSCOPE ENGINE
   ============================================================ */

const galaxyTextureData = "__GALAXY__";
const sunTextureData = "__SUN__";

const mercuryTexture = "__MERCURY__";
const venusTexture = "__VENUS__";
const earthTexture = "__EARTH__";
const marsTexture = "__MARS__";
const jupiterTexture = "__JUPITER__";
const saturnTexture = "__SATURN__";
const uranusTexture = "__URANUS__";
const neptuneTexture = "__NEPTUNE__";

const moonTexture = "__MOON__";

const ioTexture = "__IO__";
const europaTexture = "__EUROPA__";
const ganymedeTexture = "__GANYMEDE__";
const callistoTexture = "__CALLISTO__";

const sat2Texture = "__SAT2__";
const sat5Texture = "__SAT5__";
const sat6Texture = "__SAT6__";

const ura1Texture = "__URA1__";
const ura3Texture = "__URA3__";
const ura4Texture = "__URA4__";
const ura5Texture = "__URA5__";

const plutoTexture = "__PLUTO__";

/* ============================================================
   SCENE
   ============================================================ */

const container = document.getElementById("space");

const scene = new THREE.Scene();

scene.fog = new THREE.FogExp2(
    0x000000,
    0.00025
);

/* ============================================================
   CAMERA
   ============================================================ */

const camera = new THREE.PerspectiveCamera(
    55,
    window.innerWidth / window.innerHeight,
    0.1,
    30000
);

camera.position.set(
    0,
    650,
    1150
);

/* ============================================================
   RENDERER
   ============================================================ */

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    powerPreference: "high-performance"
});

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.outputColorSpace =
    THREE.SRGBColorSpace;

renderer.toneMapping =
    THREE.ACESFilmicToneMapping;

renderer.toneMappingExposure = 1.15;

container.appendChild(renderer.domElement);

/* ============================================================
   TEXTURE LOADER
   ============================================================ */

const loader = new THREE.TextureLoader();

function loadTexture(data) {

    if (!data || data.length < 20) {
        return null;
    }

    try {

        const texture = loader.load(data);

        texture.colorSpace =
            THREE.SRGBColorSpace;

        return texture;

    } catch (e) {

        return null;
    }
}

/* ============================================================
   SPACE BACKGROUND
   ============================================================ */

const galaxyTexture =
    loadTexture(galaxyTextureData);

if (galaxyTexture) {

    galaxyTexture.mapping =
        THREE.EquirectangularReflectionMapping;

    scene.background =
        galaxyTexture;

} else {

    scene.background =
        new THREE.Color(0x000006);
}

/* ============================================================
   LIGHTING
   ============================================================ */

scene.add(
    new THREE.AmbientLight(
        0x202535,
        0.22
    )
);

const sunLight =
    new THREE.PointLight(
        0xffffff,
        3.5,
        0,
        1
    );

scene.add(sunLight);

/* ============================================================
   REALISTIC STAR FIELD
   ============================================================ */

function createStars() {

    const geometry =
        new THREE.BufferGeometry();

    const positions = [];

    const starCount = 7000;

    for (
        let i = 0;
        i < starCount;
        i++
    ) {

        const radius =
            5000 + Math.random() * 10000;

        const theta =
            Math.random() * Math.PI * 2;

        const phi =
            Math.acos(
                2 * Math.random() - 1
            );

        positions.push(
            radius *
            Math.sin(phi) *
            Math.cos(theta)
        );

        positions.push(
            radius *
            Math.cos(phi)
        );

        positions.push(
            radius *
            Math.sin(phi) *
            Math.sin(theta)
        );
    }

    geometry.setAttribute(
        "position",
        new THREE.Float32BufferAttribute(
            positions,
            3
        )
    );

    const material =
        new THREE.PointsMaterial({
            color: 0xffffff,
            size: 2.2,
            transparent: true,
            opacity: 0.85,
            sizeAttenuation: true
        });

    return new THREE.Points(
        geometry,
        material
    );
}

scene.add(createStars());

/* ============================================================
   SUN
   ============================================================ */

const sunGroup =
    new THREE.Group();

scene.add(sunGroup);

const sunGeometry =
    new THREE.SphereGeometry(
        58,
        64,
        64
    );

const sunMap =
    loadTexture(sunTextureData);

let sunMaterial;

if (sunMap) {

    sunMaterial =
        new THREE.MeshBasicMaterial({
            map: sunMap
        });

} else {

    sunMaterial =
        new THREE.MeshBasicMaterial({
            color: 0xffaa22
        });
}

const sun =
    new THREE.Mesh(
        sunGeometry,
        sunMaterial
    );

sun.name = "Sun";

sun.userData = {

    selectable: true,

    name: "Sun",

    type: "Star",

    radius: "696,340 km",

    mass: "333,000 Earths",

    distance: "0 AU",

    orbital: "N/A",

    rotation: "25–35 days",

    moons: "8 planets",

    temperature: "5,500°C surface",

    atmosphere:
        "Hydrogen / Helium",

    facts:
        "The Sun contains more than 99% of the mass of the Solar System and powers almost every world within it."

};

sunGroup.add(sun);

/* ============================================================
   SUN GLOW
   ============================================================ */

function createGlowTexture() {

    const canvas =
        document.createElement("canvas");

    canvas.width = 256;
    canvas.height = 256;

    const ctx =
        canvas.getContext("2d");

    const gradient =
        ctx.createRadialGradient(
            128,
            128,
            5,
            128,
            128,
            128
        );

    gradient.addColorStop(
        0,
        "rgba(255,255,220,1)"
    );

    gradient.addColorStop(
        0.15,
        "rgba(255,220,100,.8)"
    );

    gradient.addColorStop(
        0.45,
        "rgba(255,150,30,.35)"
    );

    gradient.addColorStop(
        1,
        "rgba(255,100,0,0)"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0,
        0,
        256,
        256
    );

    return new THREE.CanvasTexture(
        canvas
    );
}

const glowMaterial =
    new THREE.SpriteMaterial({
        map: createGlowTexture(),
        transparent: true,
        blending: THREE.AdditiveBlending,
        depthWrite: false
    });

const sunGlow =
    new THREE.Sprite(
        glowMaterial
    );

sunGlow.scale.set(
    230,
    230,
    1
);

sunGroup.add(sunGlow);

/* ============================================================
   PLANET DATA
   ============================================================ */

const PLANETS = [

    {
        name: "Mercury",
        type: "Terrestrial Planet",
        radius: "2,440 km",
        mass: "0.055 Earth",
        distance: "0.39 AU",
        orbital: "88 days",
        rotation: "58.6 days",
        moons: "0",
        temperature: "167°C average",
        atmosphere: "Extremely thin",
        facts:
            "Mercury is the smallest planet and the closest planet to the Sun.",
        size: 7,
        orbit: 105,
        speed: 0.020,
        texture: mercuryTexture,
        fallback: 0x8a8077
    },

    {
        name: "Venus",
        type: "Terrestrial Planet",
        radius: "6,052 km",
        mass: "0.815 Earth",
        distance: "0.72 AU",
        orbital: "224.7 days",
        rotation: "243 days",
        moons: "0",
        temperature: "464°C",
        atmosphere: "CO₂ / N₂",
        facts:
            "Venus has the hottest planetary surface in the Solar System because of its extreme greenhouse effect.",
        size: 11,
        orbit: 150,
        speed: 0.015,
        texture: venusTexture,
        fallback: 0xd6a56a
    },

    {
        name: "Earth",
        type: "Terrestrial Planet",
        radius: "6,371 km",
        mass: "1 Earth",
        distance: "1 AU",
        orbital: "365.25 days",
        rotation: "23.93 hours",
        moons: "1",
        temperature: "15°C",
        atmosphere: "N₂ / O₂",
        facts:
            "Earth is the only world currently confirmed to support life.",
        size: 12,
        orbit: 205,
        speed: 0.010,
        texture: earthTexture,
        fallback: 0x2b6cff
    },

    {
        name: "Mars",
        type: "Terrestrial Planet",
        radius: "3,390 km",
        mass: "0.107 Earth",
        distance: "1.52 AU",
        orbital: "687 days",
        rotation: "24.6 hours",
        moons: "2",
        temperature: "-63°C",
        atmosphere: "Mostly CO₂",
        facts:
            "Mars is a cold desert world with enormous volcanoes, deep canyons and evidence of ancient water.",
        size: 9,
        orbit: 265,
        speed: 0.008,
        texture: marsTexture,
        fallback: 0xb44b32
    },

    {
        name: "Jupiter",
        type: "Gas Giant",
        radius: "69,911 km",
        mass: "317.8 Earth",
        distance: "5.20 AU",
        orbital: "11.86 years",
        rotation: "9.93 hours",
        moons: "95+",
        temperature: "-110°C",
        atmosphere: "H₂ / He",
        facts:
            "Jupiter is the largest planet and contains the famous Great Red Spot, a gigantic atmospheric storm.",
        size: 31,
        orbit: 390,
        speed: 0.004,
        texture: jupiterTexture,
        fallback: 0xc8925a
    },

    {
        name: "Saturn",
        type: "Gas Giant",
        radius: "58,232 km",
        mass: "95.2 Earth",
        distance: "9.58 AU",
        orbital: "29.45 years",
        rotation: "10.7 hours",
        moons: "140+",
        temperature: "-140°C",
        atmosphere: "H₂ / He",
        facts:
            "Saturn is famous for its spectacular ring system made mainly from ice and rocky particles.",
        size: 27,
        orbit: 530,
        speed: 0.0028,
        texture: saturnTexture,
        fallback: 0xd7bf91
    },

    {
        name: "Uranus",
        type: "Ice Giant",
        radius: "25,362 km",
        mass: "14.5 Earth",
        distance: "19.2 AU",
        orbital: "84 years",
        rotation: "17.2 hours",
        moons: "27",
        temperature: "-195°C",
        atmosphere: "H₂ / He / CH₄",
        facts:
            "Uranus rotates almost on its side, producing one of the strangest seasonal cycles in the Solar System.",
        size: 20,
        orbit: 690,
        speed: 0.0018,
        texture: uranusTexture,
        fallback: 0x74c9d4
    },

    {
        name: "Neptune",
        type: "Ice Giant",
        radius: "24,622 km",
        mass: "17.1 Earth",
        distance: "30.1 AU",
        orbital: "164.8 years",
        rotation: "16.1 hours",
        moons: "14",
        temperature: "-200°C",
        atmosphere: "H₂ / He / CH₄",
        facts:
            "Neptune is the farthest major planet and has some of the fastest winds in the Solar System.",
        size: 19,
        orbit: 850,
        speed: 0.0012,
        texture: neptuneTexture,
        fallback: 0x315dca
    },

    {
        name: "Pluto",
        type: "Dwarf Planet",
        radius: "1,188 km",
        mass: "0.0022 Earth",
        distance: "39.5 AU",
        orbital: "248 years",
        rotation: "6.4 days",
        moons: "5",
        temperature: "-229°C",
        atmosphere: "Nitrogen / Methane",
        facts:
            "Pluto is a distant dwarf planet in the Kuiper Belt with a complex surface and a large heart-shaped region.",
        size: 5,
        orbit: 1030,
        speed: 0.0008,
        texture: plutoTexture,
        fallback: 0x9e9488
    }

];

/* ============================================================
   GLOBAL OBJECT COLLECTIONS
   ============================================================ */

const planetObjects = [];

const orbitObjects = [];

const labelObjects = [];

const moonObjects = [];

const asteroidObjects = [];

const clickableObjects = [];

/* ============================================================
   CREATE ORBIT
   ============================================================ */

function createOrbit(radius) {

    const points = [];

    const segments = 256;

    for (
        let i = 0;
        i <= segments;
        i++
    ) {

        const angle =
            (i / segments) *
            Math.PI *
            2;

        points.push(
            new THREE.Vector3(
                Math.cos(angle) * radius,
                0,
                Math.sin(angle) * radius
            )
        );
    }

    const geometry =
        new THREE.BufferGeometry()
            .setFromPoints(points);

    const material =
        new THREE.LineBasicMaterial({
            color: 0x6f8eb5,
            transparent: true,
            opacity: 0.20
        });

    const line =
        new THREE.Line(
            geometry,
            material
        );

    scene.add(line);

    orbitObjects.push(line);

    return line;
}

/* ============================================================
   CREATE PLANET
   ============================================================ */

function createPlanet(data) {

    const orbitGroup =
        new THREE.Group();

    scene.add(orbitGroup);

    const angle =
        Math.random() *
        Math.PI *
        2;

    orbitGroup.rotation.y =
        angle;

    const geometry =
        new THREE.SphereGeometry(
            data.size,
            48,
            48
        );

    const texture =
        loadTexture(data.texture);

    let material;

    if (texture) {

        material =
            new THREE.MeshStandardMaterial({
                map: texture,
                roughness: 0.8,
                metalness: 0
            });

    } else {

        material =
            new THREE.MeshStandardMaterial({
                color: data.fallback,
                roughness: 0.9
            });
    }

    const planet =
        new THREE.Mesh(
            geometry,
            material
        );

    planet.position.x =
        data.orbit;

    planet.name =
        data.name;

    planet.userData = {

        selectable: true,

        ...data
    };

    orbitGroup.add(planet);

    createOrbit(data.orbit);

    planetObjects.push({
        data: data,
        mesh: planet,
        orbitGroup: orbitGroup
    });

    clickableObjects.push(planet);

    createPlanetLabel(
        planet,
        data.name
    );

    /* ========================================================
       SATURN RINGS
       ======================================================== */

    if (data.name === "Saturn") {

        const ringGeometry =
            new THREE.RingGeometry(
                data.size * 1.35,
                data.size * 2.3,
                96
            );

        const ringMaterial =
            new THREE.MeshBasicMaterial({
                color: 0xc9b998,
                side: THREE.DoubleSide,
                transparent: true,
                opacity: 0.75
            });

        const ring =
            new THREE.Mesh(
                ringGeometry,
                ringMaterial
            );

        ring.rotation.x =
            Math.PI / 2;

        planet.add(ring);

        planet.userData.ring =
            ring;
    }

    return planet;
}

/* ============================================================
   CREATE PLANETS
   ============================================================ */

PLANETS.forEach(
    createPlanet
);

/* ============================================================
   MOON CREATOR
   ============================================================ */

function createMoon(
    parentPlanet,
    name,
    size,
    distance,
    speed,
    textureData,
    fallbackColor
) {

    const moonOrbit =
        new THREE.Group();

    parentPlanet.add(
        moonOrbit
    );

    const geometry =
        new THREE.SphereGeometry(
            size,
            24,
            24
        );

    const texture =
        loadTexture(textureData);

    let material;

    if (texture) {

        material =
            new THREE.MeshStandardMaterial({
                map: texture,
                roughness: 0.9
            });

    } else {

        material =
            new THREE.MeshStandardMaterial({
                color: fallbackColor,
                roughness: 1
            });
    }

    const moon =
        new THREE.Mesh(
            geometry,
            material
        );

    moon.position.x =
        distance;

    moon.name =
        name;

    moon.userData = {

        selectable: true,

        name: name,

        type: "Natural Satellite",

        radius: "See astronomical data",

        mass: "See astronomical data",

        distance:
            "Orbits " +
            parentPlanet.name,

        orbital: "Moon orbit",

        rotation: "Synchronous / varies",

        moons: "N/A",

        temperature: "Varies",

        atmosphere: "Varies",

        facts:
            name +
            " is a natural satellite in the Solar System."
    };

    moonOrbit.add(moon);

    moonObjects.push({

        mesh: moon,

        orbit: moonOrbit,

        speed: speed

    });

    clickableObjects.push(
        moon
    );

    createPlanetLabel(
        moon,
        name
    );

    return moon;
}

/* ============================================================
   FIND PLANET
   ============================================================ */

function getPlanet(name) {

    const item =
        planetObjects.find(
            p =>
                p.data.name === name
        );

    return item
        ? item.mesh
        : null;
}

/* ============================================================
   EARTH MOON
   ============================================================ */

const earth =
    getPlanet("Earth");

if (earth) {

    createMoon(
        earth,
        "Moon",
        3.3,
        28,
        0.035,
        moonTexture,
        0xaaa9a5
    );
}

/* ============================================================
   JUPITER MOONS
   ============================================================ */

const jupiter =
    getPlanet("Jupiter");

if (jupiter) {

    createMoon(
        jupiter,
        "Io",
        4.2,
        48,
        0.030,
        ioTexture,
        0xd5b34f
    );

    createMoon(
        jupiter,
        "Europa",
        3.6,
        62,
        0.023,
        europaTexture,
        0xb9a47e
    );

    createMoon(
        jupiter,
        "Ganymede",
        5.1,
        80,
        0.017,
        ganymedeTexture,
        0x887d70
    );

    createMoon(
        jupiter,
        "Callisto",
        4.8,
        101,
        0.012,
        callistoTexture,
        0x6f655e
    );
}

/* ============================================================
   SATURN MOONS
   ============================================================ */

const saturn =
    getPlanet("Saturn");

if (saturn) {

    createMoon(
        saturn,
        "Titan",
        4.7,
        55,
        0.018,
        sat2Texture,
        0xb08c63
    );

    createMoon(
        saturn,
        "Enceladus",
        2.5,
        42,
        0.032,
        sat5Texture,
        0xd8e3e8
    );

    createMoon(
        saturn,
        "Rhea",
        3.2,
        72,
        0.014,
        sat6Texture,
        0xa8a39c
    );
}

/* ============================================================
   URANUS MOONS
   ============================================================ */

const uranus =
    getPlanet("Uranus");

if (uranus) {

    createMoon(
        uranus,
        "Titania",
        3.7,
        39,
        0.021,
        ura1Texture,
        0x999999
    );

    createMoon(
        uranus,
        "Oberon",
        3.4,
        52,
        0.016,
        ura3Texture,
        0x8a8580
    );

    createMoon(
        uranus,
        "Ariel",
        2.7,
        33,
        0.027,
        ura4Texture,
        0xa4a09b
    );

    createMoon(
        uranus,
        "Umbriel",
        2.8,
        45,
        0.020,
        ura5Texture,
        0x77736e
    );
}

/* ============================================================
   NEPTUNE / TRITON
   ============================================================ */

const neptune =
    getPlanet("Neptune");

if (neptune) {

    createMoon(
        neptune,
        "Triton",
        3.6,
        42,
        -0.018,
        moonTexture,
        0xc0b6ac
    );
}

/* ============================================================
   ASTEROID BELT
   ============================================================ */

const asteroidGroup =
    new THREE.Group();

scene.add(
    asteroidGroup
);

const asteroidCount = 750;

for (
    let i = 0;
    i < asteroidCount;
    i++
) {

    const angle =
        Math.random() *
        Math.PI *
        2;

    const radius =
        310 +
        Math.random() * 65;

    const y =
        (Math.random() - 0.5) *
        22;

    const size =
        0.4 +
        Math.random() * 1.5;

    const geometry =
        new THREE.IcosahedronGeometry(
            size,
            0
        );

    const material =
        new THREE.MeshStandardMaterial({
            color:
                new THREE.Color(
                    0.22 +
                    Math.random() * 0.18,
                    0.20 +
                    Math.random() * 0.15,
                    0.17 +
                    Math.random() * 0.12
                ),
            roughness: 1
        });

    const asteroid =
        new THREE.Mesh(
            geometry,
            material
        );

    asteroid.position.set(
        Math.cos(angle) * radius,
        y,
        Math.sin(angle) * radius
    );

    asteroid.rotation.set(
        Math.random() * 3,
        Math.random() * 3,
        Math.random() * 3
    );

    asteroid.userData.orbitSpeed =
        0.001 +
        Math.random() * 0.003;

    asteroidGroup.add(
        asteroid
    );

    asteroidObjects.push(
        asteroid
    );
}

/* ============================================================
   PLANET LABEL SYSTEM
   ============================================================ */

function createPlanetLabel(
    object,
    text
) {

    const label =
        document.createElement("div");

    label.className =
        "planetLabel";

    label.textContent =
        text;

    label.style.display =
        "none";

    document.body.appendChild(
        label
    );

    labelObjects.push({
        object: object,
        element: label
    });
}

function updateLabels() {

    labelObjects.forEach(
        item => {

            const object =
                item.object;

            const element =
                item.element;

            if (!labelsVisible) {

                element.style.display =
                    "none";

                return;
            }

            const vector =
                new THREE.Vector3();

            object.getWorldPosition(
                vector
            );

            vector.project(
                camera
            );

            const x =
                (vector.x * 0.5 + 0.5) *
                window.innerWidth;

            const y =
                (-vector.y * 0.5 + 0.5) *
                window.innerHeight;

            const visible =
                vector.z < 1 &&
                x > -100 &&
                x < window.innerWidth + 100 &&
                y > -100 &&
                y < window.innerHeight + 100;

            if (visible) {

                element.style.display =
                    "block";

                element.style.left =
                    x + "px";

                element.style.top =
                    y + "px";

            } else {

                element.style.display =
                    "none";
            }
        }
    );
}

/* ============================================================
   CAMERA CONTROL
   ============================================================ */

let cameraTarget =
    new THREE.Vector3(
        0,
        0,
        0
    );

let desiredCamera =
    new THREE.Vector3(
        0,
        650,
        1150
    );

let cameraDistance =
    1150;

let cameraAngleX = 0;

let cameraAngleY = 0.5;

let isDragging = false;

let lastX = 0;

let lastY = 0;

let moved = false;

/* ============================================================
   MOUSE DRAG
   ============================================================ */

renderer.domElement.addEventListener(
    "pointerdown",
    event => {

        isDragging = true;

        moved = false;

        lastX =
            event.clientX;

        lastY =
            event.clientY;
    }
);

renderer.domElement.addEventListener(
    "pointermove",
    event => {

        if (!isDragging) {
            return;
        }

        const dx =
            event.clientX -
            lastX;

        const dy =
            event.clientY -
            lastY;

        if (
            Math.abs(dx) > 2 ||
            Math.abs(dy) > 2
        ) {

            moved = true;
        }

        cameraAngleX -=
            dx * 0.005;

        cameraAngleY -=
            dy * 0.005;

        cameraAngleY =
            Math.max(
                -1.35,
                Math.min(
                    1.35,
                    cameraAngleY
                )
            );

        lastX =
            event.clientX;

        lastY =
            event.clientY;
    }
);

renderer.domElement.addEventListener(
    "pointerup",
    event => {

        isDragging = false;

        if (!moved) {

            selectObject(
                event.clientX,
                event.clientY
            );
        }
    }
);

/* ============================================================
   TOUCH PINCH / ZOOM
   ============================================================ */

let touchDistance = null;

renderer.domElement.addEventListener(
    "touchstart",
    event => {

        if (
            event.touches.length === 2
        ) {

            touchDistance =
                getTouchDistance(
                    event.touches
                );
        }
    },
    {
        passive: true
    }
);

renderer.domElement.addEventListener(
    "touchmove",
    event => {

        if (
            event.touches.length === 2
        ) {

            const newDistance =
                getTouchDistance(
                    event.touches
                );

            if (
                touchDistance !== null
            ) {

                const difference =
                    newDistance -
                    touchDistance;

                cameraDistance -=
                    difference * 1.2;

                cameraDistance =
                    Math.max(
                        50,
                        Math.min(
                            7000,
                            cameraDistance
                        )
                    );
            }

            touchDistance =
                newDistance;
        }
    },
    {
        passive: true
    }
);

renderer.domElement.addEventListener(
    "touchend",
    () => {

        touchDistance =
            null;
    }
);

function getTouchDistance(
    touches
) {

    const dx =
        touches[0].clientX -
        touches[1].clientX;

    const dy =
        touches[0].clientY -
        touches[1].clientY;

    return Math.sqrt(
        dx * dx +
        dy * dy
    );
}

/* ============================================================
   MOUSE WHEEL
   ============================================================ */

renderer.domElement.addEventListener(
    "wheel",
    event => {

        cameraDistance +=
            event.deltaY * 0.8;

        cameraDistance =
            Math.max(
                50,
                Math.min(
                    7000,
                    cameraDistance
                )
            );
    },
    {
        passive: true
    }
);

/* ============================================================
   RAYCASTER
   ============================================================ */

const raycaster =
    new THREE.Raycaster();

const pointer =
    new THREE.Vector2();

function selectObject(
    clientX,
    clientY
) {

    const rect =
        renderer.domElement
            .getBoundingClientRect();

    pointer.x =
        (
            (clientX - rect.left) /
            rect.width
        ) * 2 - 1;

    pointer.y =
        -(
            (clientY - rect.top) /
            rect.height
        ) * 2 + 1;

    raycaster.setFromCamera(
        pointer,
        camera
    );

    const hits =
        raycaster.intersectObjects(
            clickableObjects,
            true
        );

    if (
        hits.length === 0
    ) {

        return;
    }

    let selected =
        hits[0].object;

    while (
        selected &&
        !selected.userData.selectable
    ) {

        selected =
            selected.parent;
    }

    if (
        selected &&
        selected.userData
    ) {

        showInfo(
            selected.userData
        );
    }
}

/* ============================================================
   INFO PANEL
   ============================================================ */

function showInfo(data) {

    document.getElementById(
        "infoName"
    ).textContent =
        data.name || "Unknown";

    document.getElementById(
        "infoType"
    ).textContent =
        data.type || "Celestial Object";

    document.getElementById(
        "radiusValue"
    ).textContent =
        data.radius || "—";

    document.getElementById(
        "massValue"
    ).textContent =
        data.mass || "—";

    document.getElementById(
        "distanceValue"
    ).textContent =
        data.distance || "—";

    document.getElementById(
        "orbitValue"
    ).textContent =
        data.orbital || "—";

    document.getElementById(
        "rotationValue"
    ).textContent =
        data.rotation || "—";

    document.getElementById(
        "moonsValue"
    ).textContent =
        data.moons || "—";

    document.getElementById(
        "temperatureValue"
    ).textContent =
        data.temperature || "—";

    document.getElementById(
        "atmosphereValue"
    ).textContent =
        data.atmosphere || "—";

    document.getElementById(
        "infoFacts"
    ).textContent =
        data.facts || "";

    document.getElementById(
        "infoPanel"
    ).classList.add(
        "visible"
    );
}

/* ============================================================
   PLAY / PAUSE
   ============================================================ */

let playing = true;

let simulationSpeed = 1;

const playBtn =
    document.getElementById(
        "playBtn"
    );

playBtn.addEventListener(
    "click",
    () => {

        playing =
            !playing;

        playBtn.textContent =
            playing
                ? "❚❚ PAUSE"
                : "▶ PLAY";
    }
);

/* ============================================================
   SPEED
   ============================================================ */

const speedSlider =
    document.getElementById(
        "speedSlider"
    );

const speedValue =
    document.getElementById(
        "speedValue"
    );

speedSlider.addEventListener(
    "input",
    () => {

        simulationSpeed =
            parseFloat(
                speedSlider.value
            );

        speedValue.textContent =
            simulationSpeed.toFixed(1) +
            "×";
    }
);

/* ============================================================
   TOGGLES
   ============================================================ */

let orbitsVisible = true;

let labelsVisible = true;

let asteroidsVisible = true;

document.getElementById(
    "orbitBtn"
).addEventListener(
    "click",
    function () {

        orbitsVisible =
            !orbitsVisible;

        orbitObjects.forEach(
            orbit => {

                orbit.visible =
                    orbitsVisible;
            }
        );

        this.classList.toggle(
            "active",
            orbitsVisible
        );
    }
);

document.getElementById(
    "labelBtn"
).addEventListener(
    "click",
    function () {

        labelsVisible =
            !labelsVisible;

        this.classList.toggle(
            "active",
            labelsVisible
        );
    }
);

document.getElementById(
    "asteroidBtn"
).addEventListener(
    "click",
    function () {

        asteroidsVisible =
            !asteroidsVisible;

        asteroidGroup.visible =
            asteroidsVisible;

        this.classList.toggle(
            "active",
            asteroidsVisible
        );
    }
);

/* ============================================================
   CAMERA TARGET
   ============================================================ */

function focusPlanet(
    name
) {

    if (
        name === "Sun"
    ) {

        cameraTarget.set(
            0,
            0,
            0
        );

        desiredCamera.set(
            0,
            170,
            300
        );

        cameraDistance =
            350;

        return;
    }

    const planet =
        getPlanet(name);

    if (!planet) {
        return;
    }

    planet.getWorldPosition(
        cameraTarget
    );

    const size =
        planet.geometry.parameters.radius;

    cameraDistance =
        Math.max(
            size * 10,
            100
        );

    desiredCamera.set(
        cameraTarget.x +
            cameraDistance * 0.35,

        cameraTarget.y +
            cameraDistance * 0.25,

        cameraTarget.z +
            cameraDistance
    );
}

/* ============================================================
   PLANET CAMERA BUTTONS
   ============================================================ */

document
    .querySelectorAll(
        "[data-target]"
    )
    .forEach(
        button => {

            button.addEventListener(
                "click",
                () => {

                    focusPlanet(
                        button.dataset.target
                    );
                }
            );
        }
    );

/* ============================================================
   OVERVIEW
   ============================================================ */

function overview() {

    cameraTarget.set(
        0,
        0,
        0
    );

    cameraDistance =
        1450;

    cameraAngleX =
        0;

    cameraAngleY =
        0.45;
}

document.getElementById(
    "overviewBtn"
).addEventListener(
    "click",
    overview
);

/* ============================================================
   INNER PLANETS
   ============================================================ */

document.getElementById(
    "innerBtn"
).addEventListener(
    "click",
    () => {

        cameraTarget.set(
            0,
            0,
            0
        );

        cameraDistance =
            470;

        cameraAngleY =
            0.45;
    }
);

/* ============================================================
   OUTER PLANETS
   ============================================================ */

document.getElementById(
    "outerBtn"
).addEventListener(
    "click",
    () => {

        cameraTarget.set(
            0,
            0,
            0
        );

        cameraDistance =
            1250;

        cameraAngleY =
            0.42;
    }
);

/* ============================================================
   RESET CAMERA
   ============================================================ */

document.getElementById(
    "resetBtn"
).addEventListener(
    "click",
    overview
);

/* ============================================================
   ANIMATION
   ============================================================ */

const clock =
    new THREE.Clock();

function animate() {

    requestAnimationFrame(
        animate
    );

    const delta =
        clock.getDelta();

    if (playing) {

        /* ====================================================
           PLANET ORBITS
           ==================================================== */

        planetObjects.forEach(
            item => {

                item.orbitGroup.rotation.y +=
                    item.data.speed *
                    simulationSpeed *
                    delta *
                    60;

                item.mesh.rotation.y +=
                    0.004 *
                    simulationSpeed;

                if (
                    item.mesh.userData.ring
                ) {

                    item.mesh.userData
                        .ring.rotation.z +=
                        0.0005 *
                        simulationSpeed;
                }
            }
        );

        /* ====================================================
           MOON ORBITS
           ==================================================== */

        moonObjects.forEach(
            moon => {

                moon.orbit.rotation.y +=
                    moon.speed *
                    simulationSpeed *
                    delta *
                    60;

                moon.mesh.rotation.y +=
                    0.01 *
                    simulationSpeed;
            }
        );

        /* ====================================================
           ASTEROIDS
           ==================================================== */

        asteroidObjects.forEach(
            asteroid => {

                const angle =
                    Math.atan2(
                        asteroid.position.z,
                        asteroid.position.x
                    );

                const radius =
                    Math.sqrt(
                        asteroid.position.x *
                        asteroid.position.x +
                        asteroid.position.z *
                        asteroid.position.z
                    );

                const newAngle =
                    angle +
                    asteroid.userData.orbitSpeed *
                    simulationSpeed *
                    delta *
                    60;

                asteroid.position.x =
                    Math.cos(newAngle) *
                    radius;

                asteroid.position.z =
                    Math.sin(newAngle) *
                    radius;

                asteroid.rotation.x +=
                    0.002 *
                    simulationSpeed;

                asteroid.rotation.y +=
                    0.003 *
                    simulationSpeed;
            }
        );

        /* ====================================================
           SUN ROTATION
           ==================================================== */

        sun.rotation.y +=
            0.0015 *
            simulationSpeed;

        sunGlow.material.opacity =
            0.72 +
            Math.sin(
                performance.now() * 0.0015
            ) * 0.08;
    }

    /* ========================================================
       CAMERA
       ======================================================== */

    const horizontal =
        Math.cos(
            cameraAngleY
        ) *
        cameraDistance;

    const vertical =
        Math.sin(
            cameraAngleY
        ) *
        cameraDistance;

    const offsetX =
        Math.sin(
            cameraAngleX
        ) *
        horizontal;

    const offsetZ =
        Math.cos(
            cameraAngleX
        ) *
        horizontal;

    desiredCamera.set(
        cameraTarget.x +
            offsetX,

        cameraTarget.y +
            vertical,

        cameraTarget.z +
            offsetZ
    );

    camera.position.lerp(
        desiredCamera,
        0.055
    );

    camera.lookAt(
        cameraTarget
    );

    /* ========================================================
       LABELS
       ======================================================== */

    updateLabels();

    /* ========================================================
       RENDER
       ======================================================== */

    renderer.render(
        scene,
        camera
    );
}

/* ============================================================
   RESIZE
   ============================================================ */

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            window.innerWidth /
            window.innerHeight;

        camera.updateProjectionMatrix();

        renderer.setSize(
            window.innerWidth,
            window.innerHeight
        );
    }
);

/* ============================================================
   START
   ============================================================ */

setTimeout(
    () => {

        document.getElementById(
            "loading"
        ).style.display =
            "none";

    },
    1000
);

overview();

animate();

</script>

</body>
</html>
"""

    # ============================================================
    # INSERT LOCAL IMAGES
    # ============================================================

    html = html.replace(
        "__GALAXY__",
        textures["galaxy"]
    )

    html = html.replace(
        "__SUN__",
        textures["sun"]
    )

    html = html.replace(
        "__MERCURY__",
        textures["mercury"]
    )

    html = html.replace(
        "__VENUS__",
        textures["venus"]
    )

    html = html.replace(
        "__EARTH__",
        textures["earth"]
    )

    html = html.replace(
        "__MARS__",
        textures["mars"]
    )

    html = html.replace(
        "__JUPITER__",
        textures["jupiter"]
    )

    html = html.replace(
        "__SATURN__",
        textures["saturn"]
    )

    html = html.replace(
        "__URANUS__",
        textures["uranus"]
    )

    html = html.replace(
        "__NEPTUNE__",
        textures["neptune"]
    )

    html = html.replace(
        "__MOON__",
        textures["moon"]
    )

    html = html.replace(
        "__IO__",
        textures["io"]
    )

    html = html.replace(
        "__EUROPA__",
        textures["europa"]
    )

    html = html.replace(
        "__GANYMEDE__",
        textures["ganymede"]
    )

    html = html.replace(
        "__CALLISTO__",
        textures["callisto"]
    )

    html = html.replace(
        "__SAT2__",
        textures["sat2"]
    )

    html = html.replace(
        "__SAT5__",
        textures["sat5"]
    )

    html = html.replace(
        "__SAT6__",
        textures["sat6"]
    )

    html = html.replace(
        "__URA1__",
        textures["ura1"]
    )

    html = html.replace(
        "__URA3__",
        textures["ura3"]
    )

    html = html.replace(
        "__URA4__",
        textures["ura4"]
    )

    html = html.replace(
        "__URA5__",
        textures["ura5"]
    )

    html = html.replace(
        "__PLUTO__",
        textures["pluto"]
    )

    # ============================================================
    # STREAMLIT THREE.JS VIEW
    # ============================================================

    components.html(
        html,
        height=900,
        scrolling=False
    )

    # ============================================================
    # GO BEYOND → SCENE 3
    # ============================================================

    st.markdown(
        """
        <style>

        /* GO BEYOND BUTTON */

        div[data-testid="stButton"] {
            position: fixed !important;
            left: 50% !important;
            bottom: 28px !important;

            transform: translateX(-50%) !important;

            z-index: 999999 !important;

            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stButton"] button {

            width: auto !important;
            min-width: 0 !important;
            height: auto !important;

            padding: 9px 18px !important;

            margin: 0 !important;

            background:
                rgba(5, 15, 30, 0.90) !important;

            color:
                rgba(235, 245, 255, 0.92) !important;

            border:
                1px solid rgba(120, 190, 255, 0.55) !important;

            border-radius: 6px !important;

            font-size: 9px !important;

            font-weight: 600 !important;

            letter-spacing: 1.6px !important;

            line-height: 1.2 !important;

            cursor: pointer !important;

            box-shadow:
                0 0 14px rgba(70, 160, 255, 0.12) !important;

            transition:
                all 0.2s ease !important;
        }

        div[data-testid="stButton"] button:hover {

            background:
                rgba(30, 80, 140, 0.38) !important;

            color:
                #ffffff !important;

            border-color:
                rgba(180, 225, 255, 0.90) !important;

            box-shadow:
                0 0 22px rgba(70, 160, 255, 0.25) !important;

            transform:
                translateY(-1px) !important;
        }

        @media (max-width: 700px) {

            div[data-testid="stButton"] {
                bottom: 18px !important;
            }

            div[data-testid="stButton"] button {

                padding: 8px 14px !important;

                font-size: 8px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "GO BEYOND  →",
        key="go_beyond_button"
    ):
        st.session_state.scene = 3
        st.query_params["scene"] = "3"
        st.rerun()