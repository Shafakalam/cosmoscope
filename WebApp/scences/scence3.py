import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import io
import json

try:
    from PIL import Image
except ImportError:
    Image = None


# ============================================================
# COSMOSCOPE — SCENE 3
# ADVANCED DEEP SPACE EXPLORATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"


# ============================================================
# IMAGE LOADER
# ============================================================

def image_to_data_uri(filename, max_size=(1800, 1200), quality=88):

    path = ASSETS_DIR / filename

    if not path.exists():
        return ""

    try:

        if Image is not None:

            img = Image.open(path).convert("RGB")

            img.thumbnail(
                max_size,
                Image.Resampling.LANCZOS
            )

            buffer = io.BytesIO()

            img.save(
                buffer,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            encoded = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

            return (
                "data:image/jpeg;base64,"
                + encoded
            )

        raw = path.read_bytes()

        encoded = base64.b64encode(
            raw
        ).decode("utf-8")

        return (
            "data:image/jpeg;base64,"
            + encoded
        )

    except Exception:
        return ""


# ============================================================
# LOAD ASSETS
# ============================================================

STARFIELD = image_to_data_uri(
    "starfield.jpg",
    (1800, 1200),
    82
)

KUIPER = image_to_data_uri(
    "kuiper_belt.jpg",
    (1800, 1200),
    90
)

INTERSTELLAR = image_to_data_uri(
    "interstellar.jpg",
    (1800, 1200),
    90
)

MILKY_WAY = image_to_data_uri(
    "our_galaxy.jpg",
    (1800, 1800),
    90
)

GALACTIC = image_to_data_uri(
    "insidemilky-way.jpg",
    (1800, 1200),
    90
)


# ============================================================
# DESTINATIONS
# ============================================================

DESTINATIONS = [

    {
        "name": "KUIPER BELT",
        "subtitle": "THE FROZEN FRONTIER",
        "direction": "RIGHT",
        "distance": "Beyond Neptune",
        "image": KUIPER,
        "type": "belt",

        "science": {

            "what":
                "The Kuiper Belt is a huge region beyond Neptune "
                "filled with extremely cold and icy objects.",

            "find":
                "You can find dwarf planets, frozen rocks, icy bodies "
                "and ancient material left over from the Solar System's formation.",

            "why":
                "Scientists study the Kuiper Belt to understand "
                "how our Solar System formed and changed.",

            "facts": [
                "Located beyond Neptune",
                "Contains many icy objects",
                "Pluto is part of this region",
                "Very cold and extremely distant"
            ]
        }
    },


    {
        "name": "INTERSTELLAR SPACE",
        "subtitle": "BETWEEN THE STARS",
        "direction": "LEFT",
        "distance": "Between star systems",
        "image": INTERSTELLAR,
        "type": "interstellar",

        "science": {

            "what":
                "Interstellar space is the enormous region between stars. "
                "It is not completely empty.",

            "find":
                "There are extremely thin clouds of gas, dust, "
                "magnetic fields and energetic particles.",

            "why":
                "Studying interstellar space helps scientists understand "
                "how stars and planetary systems interact with their surroundings.",

            "facts": [
                "Exists between star systems",
                "Contains gas and dust",
                "Particles can travel enormous distances",
                "Spacecraft can enter interstellar space"
            ]
        }
    },


    {
        "name": "MILKY WAY",
        "subtitle": "OUR GALAXY",
        "direction": "STRAIGHT",
        "distance": "About 100,000 light-years across",
        "image": MILKY_WAY,
        "type": "galaxy",

        "science": {

            "what":
                "The Milky Way is the galaxy containing our Solar System. "
                "It contains enormous numbers of stars, gas and dust.",

            "find":
                "The galaxy contains hundreds of billions of stars, "
                "including our Sun, arranged mainly in a large spiral structure.",

            "why":
                "Understanding the Milky Way helps scientists learn "
                "where our Solar System came from and how galaxies evolve.",

            "facts": [
                "Our home galaxy",
                "Contains the Solar System",
                "Has a spiral structure",
                "About 100,000 light-years across"
            ]
        }
    },


    {
        "name": "GALACTIC REGION",
        "subtitle": "DEEP SPACE EXPLORATION",
        "direction": "RIGHT",
        "distance": "Deep galactic space",
        "image": GALACTIC,
        "type": "galactic",

        "science": {

            "what":
                "A galactic region contains enormous collections of stars, "
                "gas, dust and other structures spread across space.",

            "find":
                "Astronomers observe star-forming regions, nebulae, "
                "stellar remnants and clouds of interstellar material.",

            "why":
                "Observing these regions helps scientists investigate "
                "how stars are born, evolve and eventually die.",

            "facts": [
                "Contains huge stellar populations",
                "Stars form inside gas clouds",
                "Nebulae can be observed across galaxies",
                "Light can travel thousands of years to reach us"
            ]
        }
    }

]


DESTINATION_JSON = json.dumps(
    DESTINATIONS,
    ensure_ascii=False
)


# ============================================================
# REQUIRED STREAMLIT FUNCTION
# ============================================================

def show_scene3():

    html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<style>

/* ============================================================
   RESET
   ============================================================ */

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    overflow: hidden;

    background: #000;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}

body {
    color: #eef7ff;
}


/* ============================================================
   MAIN SPACE
   ============================================================ */

#space {

    position: relative;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    background: #000;
}


/* ============================================================
   DEEP SPACE
   ============================================================ */

#deepSpace {

    position: absolute;

    left: -15%;
    top: -15%;

    width: 130%;
    height: 130%;

    background-image:

        radial-gradient(
            circle at center,
            rgba(30,60,100,.10),
            rgba(0,0,0,.48) 55%,
            rgba(0,0,0,.92) 100%
        ),

        url("__STARS__");

    background-size: cover;

    background-position: center;

    transform:
        translate3d(0,0,0)
        scale(1.08);

    will-change: transform;
}


/* ============================================================
   STAR DEPTH
   ============================================================ */

#starDepth {

    position: absolute;

    left: -20%;
    top: -20%;

    width: 140%;
    height: 140%;

    background-image:
        url("__STARS__");

    background-size: 85% auto;

    background-position: center;

    opacity: .38;

    mix-blend-mode: screen;

    will-change: transform;
}


/* ============================================================
   TRAVEL PARTICLES
   ============================================================ */

#travelParticles {

    position: absolute;

    inset: 0;

    pointer-events: none;

    overflow: hidden;
}

.travelStar {

    position: absolute;

    width: 1px;
    height: 1px;

    background:
        rgba(220,240,255,.95);

    box-shadow:
        0 0 6px
        rgba(180,220,255,.85);

    opacity: 0;

    transform-origin: center;

    will-change: transform, left, top;
}


/* ============================================================
   DESTINATION
   ============================================================ */

#destination {

    position: absolute;

    inset: 0;

    display: flex;

    align-items: center;
    justify-content: center;

    opacity: 0;

    visibility: hidden;

    overflow: hidden;

    transition:
        opacity 1.2s ease,
        visibility 1.2s ease;
}

#destination.visible {

    opacity: 1;

    visibility: visible;
}


/* ============================================================
   NORMAL DESTINATION IMAGE
   ============================================================ */

#destinationImage {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 100%;
    height: 100%;

    object-fit: cover;

    transform:
        translate(-50%, -50%)
        scale(1.04);

    filter:
        brightness(.72)
        contrast(1.07)
        saturate(.96);

    will-change: transform;
}


/* ============================================================
   GALAXY CONTAINER
   ============================================================ */

#galaxyMotion {

    position: absolute;

    inset: -15%;

    display: flex;

    align-items: center;
    justify-content: center;

    pointer-events: none;

    opacity: 0;

    transition:
        opacity 1.3s ease;

    will-change: transform;
}

#galaxyMotion.active {
    opacity: 1;
}


/* ============================================================
   GALAXY IMAGE
   ============================================================ */

#galaxyImage {

    position: absolute;

    width: 100%;
    height: 100%;

    object-fit: cover;

    transform-origin:
        center center;

    filter:
        brightness(.75)
        contrast(1.10)
        saturate(1.03);

    will-change:
        transform;
}


/* ============================================================
   GALAXY STAR LAYER
   ============================================================ */

#galaxyStars {

    position: absolute;

    inset: -20%;

    background-image:
        url("__STARS__");

    background-size:
        70% auto;

    background-position:
        center;

    opacity: .24;

    mix-blend-mode:
        screen;

    will-change:
        transform;
}


/* ============================================================
   GALAXY OUTER DEPTH LAYER
   ============================================================ */

#galaxyDepth {

    position: absolute;

    inset: -12%;

    pointer-events: none;

    background-image:
        url("__STARS__");

    background-size:
        55% auto;

    background-position:
        center;

    opacity: .15;

    mix-blend-mode:
        screen;

    will-change:
        transform;
}


/* ============================================================
   GALAXY PARTICLES
   ============================================================ */

#galaxyParticles {

    position: absolute;

    inset: 0;

    pointer-events: none;

    overflow: hidden;
}

.galaxyParticle {

    position: absolute;

    width: 2px;
    height: 2px;

    border-radius: 50%;

    background:
        rgba(225,242,255,.78);

    box-shadow:
        0 0 7px
        rgba(170,220,255,.55);

    will-change:
        transform;
}


/* ============================================================
   KUIPER BELT
   ============================================================ */

#beltMotion {

    position: absolute;

    inset: 0;

    pointer-events: none;

    opacity: 0;

    transition:
        opacity 1.2s ease;
}

#beltMotion.active {
    opacity: 1;
}

.beltObject {

    position: absolute;

    width: 3px;
    height: 3px;

    border-radius: 50%;

    background:
        rgba(235,245,255,.95);

    box-shadow:
        0 0 8px
        rgba(180,220,255,.85);

    will-change:
        transform;
}


/* ============================================================
   INTERSTELLAR
   ============================================================ */

#interstellarFlow {

    position: absolute;

    inset: 0;

    opacity: 0;

    pointer-events: none;

    transition:
        opacity 1.1s ease;
}

#interstellarFlow.active {
    opacity: 1;
}

.flowLine {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 1px;

    height: 180px;

    transform-origin:
        center bottom;

    background:
        linear-gradient(
            to top,
            transparent,
            rgba(205,235,255,.65),
            transparent
        );

    opacity: .35;

    will-change:
        transform;
}


/* ============================================================
   VIGNETTE
   ============================================================ */

#vignette {

    position: absolute;

    inset: 0;

    pointer-events: none;

    background:
        radial-gradient(
            ellipse at center,
            transparent 34%,
            rgba(0,0,0,.18) 67%,
            rgba(0,0,0,.80) 100%
        );
}


/* ============================================================
   HUD
   ============================================================ */

#hud {

    position: absolute;

    inset: 0;

    pointer-events: none;
}


/* ============================================================
   TOP BAR
   ============================================================ */

.topBar {

    position: absolute;

    top: 22px;

    left: 27px;
    right: 27px;

    display: flex;

    align-items: center;

    justify-content: space-between;

    z-index: 50;
}

.brand {

    font-size: 10px;

    letter-spacing: 3px;

    font-weight: 600;

    color:
        rgba(230,245,255,.78);
}

.status {

    display: flex;

    align-items: center;

    gap: 8px;

    font-size: 8px;

    letter-spacing: 2px;

    color:
        rgba(220,238,250,.58);
}

.statusDot {

    width: 6px;
    height: 6px;

    border-radius: 50%;

    background:
        #9ed8ff;

    box-shadow:
        0 0 10px
        rgba(110,190,255,.8);
}


/* ============================================================
   NEXT / LEAVE MILKY WAY BUTTON
   ============================================================ */

#nextButton {

    position: absolute;

    top: 20px;
    right: 27px;

    z-index: 100;

    padding:
        11px 17px;

    border:
        1px solid
        rgba(150,205,255,.42);

    border-radius: 5px;

    background:
        rgba(3,12,23,.88);

    color:
        rgba(235,247,255,.96);

    font-size: 9px;

    font-weight: 600;

    letter-spacing: 1.6px;

    cursor: pointer;

    pointer-events: auto;

    backdrop-filter:
        blur(12px);

    transition:
        all .25s ease;
}

#nextButton:hover {

    background:
        rgba(20,70,105,.68);

    border-color:
        rgba(180,225,255,.85);

    box-shadow:
        0 0 24px
        rgba(70,160,255,.22);

    transform:
        translateY(-1px);
}

#nextButton.disabled {

    opacity: .22;

    pointer-events: none;
}


/* ============================================================
   TRAVEL HUD
   ============================================================ */

#travelHud {

    position: absolute;

    left: 30px;

    bottom: 30px;

    z-index: 40;

    max-width: 450px;

    pointer-events: none;
}

.phase {

    font-size: 8px;

    letter-spacing: 2.7px;

    color:
        rgba(150,205,245,.62);

    margin-bottom: 8px;
}

.travelMessage {

    font-size: 15px;

    font-weight: 500;

    letter-spacing: .5px;

    color:
        rgba(242,248,255,.94);

    text-shadow:
        0 2px 15px
        rgba(0,0,0,.9);
}

.route {

    margin-top: 10px;

    font-size: 8px;

    letter-spacing: 1.7px;

    color:
        rgba(170,205,230,.54);
}


/* ============================================================
   ARRIVAL
   ============================================================ */

#arrival {

    position: absolute;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%);

    width:
        min(760px, 90vw);

    text-align: center;

    z-index: 30;

    opacity: 0;

    pointer-events: none;

    transition:
        opacity 1s ease;
}

#arrival.visible {

    opacity: 1;

    pointer-events: auto;
}

.arrivalLabel {

    font-size: 10px;

    letter-spacing: 4px;

    color:
        rgba(180,220,250,.70);

    margin-bottom: 14px;
}

.arrivalTitle {

    font-size:
        clamp(30px, 5vw, 56px);

    line-height: 1;

    letter-spacing: 5px;

    font-weight: 500;

    color: #f4f9ff;

    text-shadow:
        0 0 35px
        rgba(100,180,255,.20);
}

.arrivalSubtitle {

    margin-top: 13px;

    font-size: 10px;

    letter-spacing: 3px;

    color:
        rgba(205,225,240,.68);
}


/* ============================================================
   LEARN BUTTON
   ============================================================ */

#learnButton {

    margin-top: 27px;

    padding:
        12px 21px;

    border:
        1px solid
        rgba(160,215,255,.55);

    border-radius: 5px;

    background:
        rgba(4,16,29,.80);

    color:
        rgba(240,249,255,.96);

    font-size: 9px;

    font-weight: 600;

    letter-spacing: 1.8px;

    cursor: pointer;

    pointer-events: auto;

    transition:
        all .25s ease;

    backdrop-filter:
        blur(10px);
}

#learnButton:hover {

    background:
        rgba(20,72,108,.68);

    border-color:
        rgba(210,238,255,.90);

    box-shadow:
        0 0 28px
        rgba(70,160,255,.22);

    transform:
        translateY(-1px);
}


/* ============================================================
   SCIENCE PANEL
   ============================================================ */

#sciencePanel {

    position: absolute;

    left: 50%;
    top: 50%;

    transform:
        translate(-50%, -50%)
        scale(.97);

    width:
        min(900px, 91vw);

    max-height:
        82vh;

    overflow-y:
        auto;

    z-index: 200;

    padding: 30px;

    border:
        1px solid
        rgba(160,210,245,.28);

    border-radius: 9px;

    background:
        linear-gradient(
            135deg,
            rgba(5,17,29,.97),
            rgba(3,9,18,.98)
        );

    box-shadow:
        0 20px 80px
        rgba(0,0,0,.65),

        0 0 45px
        rgba(50,130,200,.08);

    backdrop-filter:
        blur(18px);

    opacity: 0;

    visibility: hidden;

    pointer-events: none;

    transition:
        opacity .35s ease,
        transform .35s ease,
        visibility .35s ease;
}

#sciencePanel.open {

    opacity: 1;

    visibility: visible;

    pointer-events: auto;

    transform:
        translate(-50%, -50%)
        scale(1);
}


/* ============================================================
   PANEL
   ============================================================ */

.panelHeader {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    border-bottom:
        1px solid
        rgba(170,215,245,.13);

    padding-bottom: 20px;

    margin-bottom: 22px;
}

.panelEyebrow {

    font-size: 8px;

    letter-spacing: 2.5px;

    color:
        rgba(140,200,240,.58);

    margin-bottom: 7px;
}

.panelTitle {

    font-size:
        clamp(20px, 3vw, 30px);

    letter-spacing: 2.5px;

    font-weight: 500;

    color: #f5faff;
}

.closeButton {

    border: none;

    background:
        rgba(255,255,255,.04);

    color:
        rgba(225,240,250,.75);

    width: 34px;
    height: 34px;

    border-radius: 5px;

    font-size: 18px;

    cursor: pointer;
}

.closeButton:hover {

    background:
        rgba(255,255,255,.09);

    color: #fff;
}


/* ============================================================
   STUDY GRID
   ============================================================ */

.studyGrid {

    display: grid;

    grid-template-columns:
        repeat(2, minmax(0, 1fr));

    gap: 14px;
}

.studyCard {

    padding: 19px;

    min-height: 150px;

    border:
        1px solid
        rgba(155,205,240,.14);

    border-radius: 7px;

    background:
        rgba(255,255,255,.025);

    transition:
        border .25s ease,
        background .25s ease,
        transform .25s ease;
}

.studyCard:hover {

    border-color:
        rgba(155,215,255,.32);

    background:
        rgba(70,140,190,.06);

    transform:
        translateY(-2px);
}

.cardLabel {

    font-size: 9px;

    letter-spacing: 2px;

    color:
        rgba(130,195,235,.68);

    margin-bottom: 11px;

    font-weight: 600;
}

.cardText {

    font-size: 14px;

    line-height: 1.65;

    color:
        rgba(236,245,252,.92);

    font-weight: 400;
}

.factList {

    margin: 0;

    padding: 0;

    list-style: none;
}

.factList li {

    padding: 6px 0;

    font-size: 13px;

    line-height: 1.45;

    color:
        rgba(230,242,250,.88);

    border-bottom:
        1px solid
        rgba(160,205,235,.08);
}

.factList li:last-child {
    border-bottom: none;
}

.factList li::before {

    content: "•";

    color:
        rgba(150,215,255,.85);

    margin-right: 9px;
}

.panelFooter {

    margin-top: 21px;

    padding-top: 16px;

    border-top:
        1px solid
        rgba(160,205,235,.11);

    display: flex;

    justify-content: space-between;

    gap: 15px;

    font-size: 8px;

    letter-spacing: 1.5px;

    color:
        rgba(170,205,225,.48);
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    .topBar {

        top: 16px;

        left: 16px;
        right: 16px;
    }

    .brand {

        font-size: 7px;

        letter-spacing: 2px;
    }

    .status {
        display: none;
    }

    #nextButton {

        top: 48px;

        right: 16px;

        padding:
            9px 12px;

        font-size: 8px;
    }

    #travelHud {

        left: 17px;

        bottom: 19px;

        right: 17px;
    }

    .travelMessage {
        font-size: 13px;
    }

    .route {
        font-size: 7px;
    }

    #sciencePanel {

        padding: 20px;

        max-height:
            88vh;
    }

    .studyGrid {
        grid-template-columns: 1fr;
    }

    .studyCard {
        min-height: auto;
    }

    .cardText {

        font-size: 13px;

        line-height: 1.6;
    }

    .panelFooter {
        flex-direction: column;
    }

}

</style>

</head>


<body>


<div id="space">


    <div id="deepSpace"></div>

    <div id="starDepth"></div>

    <div id="travelParticles"></div>


    <!-- DESTINATION -->

    <div id="destination">


        <img
            id="destinationImage"
            src=""
            alt=""
        >


        <!-- MILKY WAY -->

        <div id="galaxyMotion">

            <img
                id="galaxyImage"
                src=""
                alt=""
            >

            <div id="galaxyStars"></div>

            <div id="galaxyDepth"></div>

            <div id="galaxyParticles"></div>

        </div>


        <!-- KUIPER -->

        <div id="beltMotion"></div>


        <!-- INTERSTELLAR -->

        <div id="interstellarFlow"></div>


    </div>


    <div id="vignette"></div>


    <!-- HUD -->

    <div id="hud">


        <div class="topBar">

            <div class="brand">
                COSMOSCOPE / DEEP SPACE
            </div>

            <div class="status">

                <span class="statusDot"></span>

                EXPLORATION SYSTEM ONLINE

            </div>

        </div>


        <!-- NEXT / LEAVE MILKY WAY -->

        <button
            id="nextButton"
            class="disabled"
        >
            NEXT DESTINATION →
        </button>


        <!-- TRAVEL HUD -->

        <div id="travelHud">

            <div
                class="phase"
                id="phase"
            >
                NAVIGATION
            </div>

            <div
                class="travelMessage"
                id="travelMessage"
            >
                INITIALIZING DEEP SPACE TRAVEL
            </div>

            <div
                class="route"
                id="route"
            >
                ROUTE CALCULATING
            </div>

        </div>


        <!-- ARRIVAL -->

        <div id="arrival">

            <div class="arrivalLabel">
                TARGET REACHED
            </div>

            <div
                class="arrivalTitle"
                id="arrivalTitle"
            >
                DESTINATION
            </div>

            <div
                class="arrivalSubtitle"
                id="arrivalSubtitle"
            >
                DEEP SPACE REGION
            </div>

            <button id="learnButton">
                EXPLORE TARGET INFO →
            </button>

        </div>


        <!-- SCIENCE PANEL -->

        <div id="sciencePanel">


            <div class="panelHeader">

                <div>

                    <div class="panelEyebrow">
                        TARGET SCIENCE
                    </div>

                    <div
                        class="panelTitle"
                        id="panelTitle"
                    >
                        DESTINATION
                    </div>

                </div>

                <button
                    class="closeButton"
                    id="closeButton"
                >
                    ×
                </button>

            </div>


            <div class="studyGrid">


                <div class="studyCard">

                    <div class="cardLabel">
                        WHAT IS IT?
                    </div>

                    <div
                        class="cardText"
                        id="whatText"
                    ></div>

                </div>


                <div class="studyCard">

                    <div class="cardLabel">
                        WHAT WILL YOU FIND?
                    </div>

                    <div
                        class="cardText"
                        id="findText"
                    ></div>

                </div>


                <div class="studyCard">

                    <div class="cardLabel">
                        WHY DOES IT MATTER?
                    </div>

                    <div
                        class="cardText"
                        id="whyText"
                    ></div>

                </div>


                <div class="studyCard">

                    <div class="cardLabel">
                        QUICK FACTS
                    </div>

                    <ul
                        class="factList"
                        id="factsList"
                    ></ul>

                </div>


            </div>


            <div class="panelFooter">

                <span id="distanceText">
                    NAVIGATION DATA
                </span>

                <span>
                    COSMOSCOPE SCIENCE MODULE
                </span>

            </div>


        </div>


    </div>


</div>


<script>


/* ============================================================
   DATA
   ============================================================ */

const DESTINATIONS =
    __DESTINATIONS__;


let destinationIndex = 0;

let travelling = false;

let arrived = false;

let travelStart = 0;

let destinationTime = 0;

const TRAVEL_DURATION = 4000;


/* ============================================================
   DOM
   ============================================================ */

const deepSpace =
    document.getElementById(
        "deepSpace"
    );

const starDepth =
    document.getElementById(
        "starDepth"
    );

const destination =
    document.getElementById(
        "destination"
    );

const destinationImage =
    document.getElementById(
        "destinationImage"
    );

const galaxyMotion =
    document.getElementById(
        "galaxyMotion"
    );

const galaxyImage =
    document.getElementById(
        "galaxyImage"
    );

const galaxyStars =
    document.getElementById(
        "galaxyStars"
    );

const galaxyDepth =
    document.getElementById(
        "galaxyDepth"
    );

const galaxyParticles =
    document.getElementById(
        "galaxyParticles"
    );

const beltMotion =
    document.getElementById(
        "beltMotion"
    );

const interstellarFlow =
    document.getElementById(
        "interstellarFlow"
    );

const travelParticles =
    document.getElementById(
        "travelParticles"
    );

const phase =
    document.getElementById(
        "phase"
    );

const travelMessage =
    document.getElementById(
        "travelMessage"
    );

const route =
    document.getElementById(
        "route"
    );

const arrival =
    document.getElementById(
        "arrival"
    );

const arrivalTitle =
    document.getElementById(
        "arrivalTitle"
    );

const arrivalSubtitle =
    document.getElementById(
        "arrivalSubtitle"
    );

const nextButton =
    document.getElementById(
        "nextButton"
    );

const learnButton =
    document.getElementById(
        "learnButton"
    );

const sciencePanel =
    document.getElementById(
        "sciencePanel"
    );

const closeButton =
    document.getElementById(
        "closeButton"
    );

const panelTitle =
    document.getElementById(
        "panelTitle"
    );

const whatText =
    document.getElementById(
        "whatText"
    );

const findText =
    document.getElementById(
        "findText"
    );

const whyText =
    document.getElementById(
        "whyText"
    );

const factsList =
    document.getElementById(
        "factsList"
    );

const distanceText =
    document.getElementById(
        "distanceText"
    );


/* ============================================================
   TRAVEL STARS
   ============================================================ */

const stars = [];


for (let i = 0; i < 240; i++) {

    const star =
        document.createElement(
            "div"
        );

    star.className =
        "travelStar";

    const x =
        Math.random() * 100;

    const y =
        Math.random() * 100;

    const depth =
        .25 +
        Math.random() * 1.5;

    const speed =
        .45 +
        Math.random() * 1.7;

    star.style.left =
        x + "%";

    star.style.top =
        y + "%";

    star.style.width =
        (
            depth * 1.7
        ) + "px";

    star.style.height =
        (
            depth * 1.7
        ) + "px";

    travelParticles.appendChild(
        star
    );

    stars.push({

        element: star,

        x: x,

        y: y,

        depth: depth,

        speed: speed

    });

}


/* ============================================================
   KUIPER OBJECTS
   ============================================================ */

const beltObjects = [];


for (let i = 0; i < 110; i++) {

    const object =
        document.createElement(
            "div"
        );

    object.className =
        "beltObject";

    beltMotion.appendChild(
        object
    );

    beltObjects.push({

        element: object,

        angle:
            Math.random() *
            Math.PI *
            2,

        radius:
            18 +
            Math.random() *
            40,

        speed:
            .00025 +
            Math.random() *
            .0010,

        depth:
            .35 +
            Math.random() *
            1.3

    });

}


/* ============================================================
   GALAXY PARTICLES
   ============================================================ */

const galaxyParticleData = [];


for (let i = 0; i < 120; i++) {

    const particle =
        document.createElement(
            "div"
        );

    particle.className =
        "galaxyParticle";

    galaxyParticles.appendChild(
        particle
    );


    const radius =
        8 +
        Math.random() *
        47;

    const angle =
        Math.random() *
        Math.PI *
        2;


    galaxyParticleData.push({

        element: particle,

        angle: angle,

        radius: radius,

        speed:
            .00018 +
            Math.random() *
            .00042,

        depth:
            .35 +
            Math.random() *
            .8

    });

}


/* ============================================================
   INTERSTELLAR FLOW
   ============================================================ */

for (let i = 0; i < 45; i++) {

    const line =
        document.createElement(
            "div"
        );

    line.className =
        "flowLine";

    const angle =
        Math.random() *
        Math.PI *
        2;

    const distance =
        8 +
        Math.random() *
        65;

    line.style.transform =
        "translate(-50%, -50%) " +
        "rotate(" +
        angle +
        "rad) " +
        "translateY(-" +
        distance +
        "vh)";

    line.style.height =
        (
            100 +
            Math.random() *
            260
        ) + "px";

    line.style.opacity =
        .10 +
        Math.random() *
        .30;

    interstellarFlow.appendChild(
        line
    );

}


/* ============================================================
   START
   ============================================================ */

function startJourney() {

    destinationIndex = 0;

    startTravel();

}


/* ============================================================
   START TRAVEL
   ============================================================ */

function startTravel() {

    const target =
        DESTINATIONS[
            destinationIndex
        ];


    travelling = true;

    arrived = false;

    travelStart =
        performance.now();


    destinationTime = 0;


    destination.classList.remove(
        "visible"
    );

    arrival.classList.remove(
        "visible"
    );


    galaxyMotion.classList.remove(
        "active"
    );

    beltMotion.classList.remove(
        "active"
    );

    interstellarFlow.classList.remove(
        "active"
    );


    destinationImage.src = "";

    galaxyImage.src = "";


    nextButton.classList.add(
        "disabled"
    );


    nextButton.textContent =
        "NEXT DESTINATION →";


    deepSpace.style.transform =
        "translate3d(0,0,0) scale(1.08)";


    starDepth.style.transform =
        "translate3d(0,0,0) scale(1.10)";


    galaxyMotion.style.transform =
        "translate3d(0,0,0)";


    phase.textContent =
        "AUTOMATED NAVIGATION";


    travelMessage.textContent =
        "TRAVELLING THROUGH DEEP SPACE";


    route.textContent =
        "VECTOR " +
        target.direction +
        " / DESTINATION " +
        (
            destinationIndex + 1
        ) +
        " OF " +
        DESTINATIONS.length;


    requestAnimationFrame(
        travelFrame
    );

}


/* ============================================================
   TRAVEL
   ============================================================ */

function travelFrame(now) {

    if (!travelling)
        return;


    const elapsed =
        now -
        travelStart;


    const progress =
        Math.min(
            elapsed /
            TRAVEL_DURATION,
            1
        );


    const acceleration =
        Math.pow(
            progress,
            1.65
        );


    const zoom =
        1.08 +
        acceleration *
        .82;


    const driftX =
        Math.sin(
            progress *
            Math.PI *
            1.6
        ) *
        5;


    const driftY =
        Math.cos(
            progress *
            Math.PI *
            1.3
        ) *
        3;


    deepSpace.style.transform =
        "translate3d(" +
        driftX +
        "%," +
        driftY +
        "%,0) scale(" +
        zoom +
        ")";


    const depthMove =
        acceleration *
        21;


    starDepth.style.transform =
        "translate3d(" +
        (
            -depthMove *
            .35
        ) +
        "%," +
        (
            depthMove *
            .14
        ) +
        "%,0) scale(" +
        (
            1.10 +
            acceleration *
            .34
        ) +
        ")";


    stars.forEach(
        (star) => {

            let x =
                star.x +
                progress *
                star.speed *
                58 *
                star.depth;


            let y =
                star.y +
                progress *
                star.speed *
                10 *
                star.depth;


            if (x > 110)
                x -= 120;

            if (y > 110)
                y -= 120;


            const stretch =
                1 +
                acceleration *
                10 *
                star.depth;


            star.element.style.left =
                x + "%";

            star.element.style.top =
                y + "%";

            star.element.style.opacity =
                Math.min(
                    .12 +
                    acceleration *
                    .85 *
                    star.depth,
                    1
                );

            star.element.style.transform =
                "scaleX(" +
                stretch +
                ")";

        }
    );


    const target =
        DESTINATIONS[
            destinationIndex
        ];


    if (progress < .25) {

        travelMessage.textContent =
            "TRAVELLING THROUGH DEEP SPACE";

    }

    else if (progress < .50) {

        travelMessage.textContent =
            "NAVIGATION LOCKED — " +
            target.direction +
            " COURSE";

    }

    else if (progress < .75) {

        travelMessage.textContent =
            "SCANNING SPACE AHEAD — TARGET APPROACHING";

    }

    else if (progress < .92) {

        travelMessage.textContent =
            "TARGET AHEAD — PREPARING APPROACH";

    }

    else {

        travelMessage.textContent =
            "FINAL APPROACH — ARRIVAL IMMINENT";

    }


    if (progress >= 1) {

        beginApproach();

        return;
    }


    requestAnimationFrame(
        travelFrame
    );

}


/* ============================================================
   ARRIVAL
   ============================================================ */

function beginApproach() {

    travelling = false;

    arrived = true;


    const target =
        DESTINATIONS[
            destinationIndex
        ];


    destinationImage.src =
        target.image;


    destinationImage.style.opacity =
        "1";


    destinationImage.style.transform =
        "translate(-50%, -50%) scale(1.05)";


    galaxyImage.style.transform =
        "rotate(0deg) scale(1.04)";


    galaxyStars.style.transform =
        "rotate(0deg) scale(1.05)";


    galaxyDepth.style.transform =
        "rotate(0deg) scale(1.08)";


    if (
        target.type ===
        "galaxy"
    ) {

        galaxyImage.src =
            target.image;

        destinationImage.style.opacity =
            "0";

    }


    destination.classList.add(
        "visible"
    );


    if (
        target.type ===
        "belt"
    ) {

        beltMotion.classList.add(
            "active"
        );

    }


    if (
        target.type ===
        "interstellar"
    ) {

        interstellarFlow.classList.add(
            "active"
        );

    }


    if (
        target.type ===
        "galaxy"
    ) {

        galaxyMotion.classList.add(
            "active"
        );

    }


    phase.textContent =
        "ARRIVAL CONFIRMED";


    travelMessage.textContent =
        "TARGET REACHED";


    route.textContent =
        target.name +
        " / " +
        target.distance;


    arrivalTitle.textContent =
        target.name;


    arrivalSubtitle.textContent =
        target.subtitle;


    arrival.classList.add(
        "visible"
    );


    nextButton.classList.remove(
        "disabled"
    );


    /*
     * FINAL DESTINATION OF SCENE 3
     *
     * After GALACTIC REGION the button changes
     * from NEXT DESTINATION to LEAVE MILKY WAY.
     */

    if (
        destinationIndex ===
        DESTINATIONS.length - 1
    ) {

        nextButton.textContent =
            "LEAVE MILKY WAY →";

    } else {

        nextButton.textContent =
            "NEXT DESTINATION →";

    }


    destinationTime = 0;


    requestAnimationFrame(
        destinationFrame
    );

}


/* ============================================================
   DESTINATION MOTION
   ============================================================ */

function destinationFrame(now) {

    if (!arrived)
        return;


    destinationTime +=
        0.016;


    const target =
        DESTINATIONS[
            destinationIndex
        ];


    /* ========================================================
       KUIPER BELT
       ======================================================== */

    if (
        target.type ===
        "belt"
    ) {

        const width =
            window.innerWidth;

        const height =
            window.innerHeight;


        beltObjects.forEach(
            (obj) => {

                obj.angle +=
                    obj.speed *
                    12;


                const cx =
                    width *
                    .5;


                const cy =
                    height *
                    .52;


                const rx =
                    width *
                    (
                        obj.radius /
                        100
                    );


                const ry =
                    height *
                    (
                        obj.radius /
                        150
                    );


                const x =
                    cx +
                    Math.cos(
                        obj.angle
                    ) *
                    rx;


                const y =
                    cy +
                    Math.sin(
                        obj.angle
                    ) *
                    ry;


                const scale =
                    .45 +
                    obj.depth *
                    .58;


                obj.element.style.transform =
                    "translate(" +
                    x +
                    "px," +
                    y +
                    "px) scale(" +
                    scale +
                    ")";


                obj.element.style.opacity =
                    .30 +
                    obj.depth *
                    .40;

            }
        );


        const cameraX =
            Math.sin(
                destinationTime *
                .12
            ) *
            1.0;


        const cameraY =
            Math.cos(
                destinationTime *
                .10
            ) *
            .7;


        destinationImage.style.transform =
            "translate(calc(-50% + " +
            cameraX +
            "%), calc(-50% + " +
            cameraY +
            "%)) scale(1.05)";

    }


    /* ========================================================
       INTERSTELLAR SPACE
       ======================================================== */

    if (
        target.type ===
        "interstellar"
    ) {

        const x =
            Math.sin(
                destinationTime *
                .08
            ) *
            1.5;


        const y =
            Math.cos(
                destinationTime *
                .11
            ) *
            1.0;


        const scale =
            1.05 +
            Math.sin(
                destinationTime *
                .14
            ) *
            .025;


        destinationImage.style.transform =
            "translate(calc(-50% + " +
            x +
            "%), calc(-50% + " +
            y +
            "%)) scale(" +
            scale +
            ")";


        const lines =
            interstellarFlow.children;


        for (
            let i = 0;
            i < lines.length;
            i++
        ) {

            const line =
                lines[i];


            const movement =
                Math.sin(
                    destinationTime *
                    (
                        .35 +
                        (i % 7) *
                        .07
                    )
                ) *
                5;


            line.style.marginTop =
                movement +
                "px";

        }

    }


    /* ========================================================
       MILKY WAY
       ======================================================== */

    if (
        target.type ===
        "galaxy"
    ) {

        const coreRotation =
            destinationTime *
            1.15;


        const starRotation =
            destinationTime *
            -0.34;


        const depthRotation =
            destinationTime *
            0.52;


        const galaxyScale =
            1.075 +
            Math.sin(
                destinationTime *
                .22
            ) *
            .025;


        const galaxyX =
            Math.sin(
                destinationTime *
                .17
            ) *
            1.25;


        const galaxyY =
            Math.cos(
                destinationTime *
                .13
            ) *
            .80;


        galaxyImage.style.transform =
            "translate(" +
            galaxyX +
            "%," +
            galaxyY +
            "%) " +
            "rotate(" +
            coreRotation +
            "deg) " +
            "scale(" +
            galaxyScale +
            ")";


        const starsScale =
            1.10 +
            Math.sin(
                destinationTime *
                .18
            ) *
            .025;


        galaxyStars.style.transform =
            "rotate(" +
            starRotation +
            "deg) " +
            "scale(" +
            starsScale +
            ")";


        galaxyDepth.style.transform =
            "rotate(" +
            depthRotation +
            "deg) " +
            "scale(" +
            (
                1.08 +
                Math.sin(
                    destinationTime *
                    .16
                ) *
                .035
            ) +
            ")";


        const width =
            window.innerWidth;


        const height =
            window.innerHeight;


        galaxyParticleData.forEach(
            (particle) => {

                particle.angle +=
                    particle.speed *
                    10;


                const rx =
                    width *
                    (
                        particle.radius /
                        100
                    );


                const ry =
                    height *
                    (
                        particle.radius /
                        150
                    );


                const x =
                    width *
                    .5 +
                    Math.cos(
                        particle.angle
                    ) *
                    rx;


                const y =
                    height *
                    .5 +
                    Math.sin(
                        particle.angle
                    ) *
                    ry;


                const size =
                    .5 +
                    particle.depth *
                    1.4;


                particle.element.style.transform =
                    "translate(" +
                    x +
                    "px," +
                    y +
                    "px) scale(" +
                    size +
                    ")";


                particle.element.style.opacity =
                    .18 +
                    particle.depth *
                    .42;

            }
        );


        const cameraX =
            Math.sin(
                destinationTime *
                .055
            ) *
            1.15;


        const cameraY =
            Math.cos(
                destinationTime *
                .047
            ) *
            .85;


        galaxyMotion.style.transform =
            "translate3d(" +
            cameraX +
            "%," +
            cameraY +
            "%,0)";

    }


    /* ========================================================
       GALACTIC REGION
       ======================================================== */

    if (
        target.type ===
        "galactic"
    ) {

        const orbitalRotation =
            destinationTime *
            0.62;


        const orbitX =
            Math.sin(
                destinationTime *
                .16
            ) *
            2.4;


        const orbitY =
            Math.cos(
                destinationTime *
                .12
            ) *
            1.7;


        const scale =
            1.08 +
            Math.sin(
                destinationTime *
                .20
            ) *
            .035;


        const tilt =
            Math.sin(
                destinationTime *
                .11
            ) *
            2.8;


        destinationImage.style.transform =
            "translate(calc(-50% + " +
            orbitX +
            "%), calc(-50% + " +
            orbitY +
            "%)) " +
            "rotate(" +
            (
                orbitalRotation +
                tilt
            ) +
            "deg) " +
            "scale(" +
            scale +
            ")";


        const cameraX =
            Math.sin(
                destinationTime *
                .075
            ) *
            1.5;


        const cameraY =
            Math.cos(
                destinationTime *
                .065
            ) *
            1.1;


        destination.style.transform =
            "translate3d(" +
            cameraX +
            "%," +
            cameraY +
            "%,0)";


        const depthScale =
            1 +
            Math.sin(
                destinationTime *
                .13
            ) *
            .018;


        destinationImage.style.filter =
            "brightness(.72) " +
            "contrast(1.08) " +
            "saturate(.98) " +
            "blur(0px)";


        deepSpace.style.transform =
            "translate3d(" +
            (
                Math.sin(
                    destinationTime *
                    .035
                ) *
                1.2
            ) +
            "%," +
            (
                Math.cos(
                    destinationTime *
                    .041
                ) *
                .8
            ) +
            "%,0) scale(" +
            depthScale +
            ")";

    }


    requestAnimationFrame(
        destinationFrame
    );

}


/* ============================================================
   SCIENCE PANEL
   ============================================================ */

function openScience() {

    const target =
        DESTINATIONS[
            destinationIndex
        ];


    panelTitle.textContent =
        target.name;


    whatText.textContent =
        target.science.what;


    findText.textContent =
        target.science.find;


    whyText.textContent =
        target.science.why;


    distanceText.textContent =
        "LOCATION / " +
        target.distance;


    factsList.innerHTML =
        "";


    target.science.facts.forEach(
        (fact) => {

            const li =
                document.createElement(
                    "li"
                );

            li.textContent =
                fact;

            factsList.appendChild(
                li
            );

        }
    );


    sciencePanel.classList.add(
        "open"
    );

}


/* ============================================================
   CLOSE
   ============================================================ */

function closeScience() {

    sciencePanel.classList.remove(
        "open"
    );

}


/* ============================================================
   EVENTS
   ============================================================ */

learnButton.addEventListener(
    "click",
    openScience
);


closeButton.addEventListener(
    "click",
    closeScience
);


/* ============================================================
   NEXT / LEAVE MILKY WAY
   ============================================================ */

nextButton.addEventListener(
    "click",
    () => {

        if (!arrived)
            return;


        closeScience();


        /*
         * FINAL DESTINATION
         *
         * GALACTIC REGION
         *        ↓
         * LEAVE MILKY WAY →
         *        ↓
         * SCENE 4
         */

        if (
            destinationIndex ===
            DESTINATIONS.length - 1
        ) {

            window.parent.location.href =
                "?scene=4";

            return;
        }


        /*
         * Continue Scene 3.
         */

        destinationIndex++;


        startTravel();

    }
);


/* ============================================================
   ESC
   ============================================================ */

document.addEventListener(
    "keydown",
    (event) => {

        if (
            event.key ===
            "Escape"
        ) {

            closeScience();

        }

    }
);


/* ============================================================
   START
   ============================================================ */

startJourney();


</script>

</body>

</html>
"""


    # ========================================================
    # INSERT LOCAL IMAGES
    # ========================================================

    html = (
        html
        .replace(
            "__STARS__",
            STARFIELD
        )
        .replace(
            "__DESTINATIONS__",
            DESTINATION_JSON
        )
    )


    # ========================================================
    # RENDER
    # ========================================================

    components.html(
        html,
        height=900,
        scrolling=False
    )


# ============================================================
# OPTIONAL ALIAS
# ============================================================

def show_scence3():
    show_scene3()