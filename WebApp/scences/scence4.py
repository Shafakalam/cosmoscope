import streamlit as st
import streamlit.components.v1 as components

from pathlib import Path
import base64
import io


# ============================================================
# COSMOSCOPE - SCENE 4
# NEBULAE -> STAR CLUSTERS -> BLACK HOLES -> GALAXIES
# -> EXOPLANETS
#
# Real local NASA/space assets
# Real NASA WebM exploration videos for every Scene 4 category
# 30-second automatic loop for each video
#
# Put this file in:
#   CosmoScope/scences/scence4.py
#
# Put assets in:
#   CosmoScope/assets/
#
# Required black-hole video:
#   assets/black_hole.webm
# ============================================================


def show_scene4():

    BASE_DIR = Path(__file__).resolve().parent.parent
    ASSETS_DIR = BASE_DIR / "assets"

    # --------------------------------------------------------
    # IMAGE LOADER
    # --------------------------------------------------------

    def load_image(filename, max_size=2200, quality=90):

        path = ASSETS_DIR / filename

        if not path.exists():
            return ""

        try:
            from PIL import Image

            image = Image.open(path).convert("RGB")

            image.thumbnail(
                (max_size, max_size),
                Image.Resampling.LANCZOS
            )

            buffer = io.BytesIO()

            image.save(
                buffer,
                format="JPEG",
                quality=quality,
                optimize=True
            )

            encoded = base64.b64encode(
                buffer.getvalue()
            ).decode("utf-8")

            return "data:image/jpeg;base64," + encoded

        except Exception:

            try:
                encoded = base64.b64encode(
                    path.read_bytes()
                ).decode("utf-8")

                suffix = path.suffix.lower()

                if suffix == ".png":
                    mime = "image/png"
                elif suffix in [".jpg", ".jpeg"]:
                    mime = "image/jpeg"
                elif suffix == ".webp":
                    mime = "image/webp"
                else:
                    mime = "image/jpeg"

                return "data:" + mime + ";base64," + encoded

            except Exception:
                return ""


    # --------------------------------------------------------
    # VIDEO LOADER
    # --------------------------------------------------------

    def load_video(filename):

        path = ASSETS_DIR / filename

        if not path.exists():
            return ""

        try:
            encoded = base64.b64encode(
                path.read_bytes()
            ).decode("utf-8")

            suffix = path.suffix.lower()

            if suffix == ".webm":
                mime = "video/webm"
            elif suffix == ".mp4":
                mime = "video/mp4"
            else:
                mime = "video/webm"

            return "data:" + mime + ";base64," + encoded

        except Exception:
            return ""


    # --------------------------------------------------------
    # REAL SPACE ASSETS
    # --------------------------------------------------------

    NEBULA_VIDEO = load_video("nebula.webm")
    STAR_CLUSTER_VIDEO = load_video("star_cluster.webm")
    BLACK_HOLE_VIDEO = load_video("black_hole.webm")
    GALAXY_VIDEO = load_video("galaxy.webm")
    EXOPLANET_VIDEO = load_video("exoplanet.webm")

    # Optional still fallback if the video is missing.
    BLACK_HOLE_STILL = load_image("black_hole.png")

    ANDROMEDA = load_image("andromeda.jpg")

    EXOPLANET = load_image("exoplanet.jpg")
    EXOPLANET_TYPES = load_image("exoplanet_types.png")

    STARFIELD = load_image("starfield.jpg")


    # --------------------------------------------------------
    # STREAMLIT PAGE CSS
    # --------------------------------------------------------

    st.markdown(
        """
        <style>

        header {
            display: none !important;
        }

        footer {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        .stApp {
            background: #010308 !important;
        }

        [data-testid="stAppViewContainer"] {
            background: #010308 !important;
        }

        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # COMPLETE HTML
    #
    # Raw triple-quoted string is intentional.
    # Do NOT change this to an f-string.
    # --------------------------------------------------------

    html = r"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

* {
    box-sizing: border-box;
}

html,
body {

    width: 100%;
    height: 100%;

    margin: 0;
    padding: 0;

    overflow: hidden;

    background: #010308;

    color: #eef8ff;

    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Arial,
        sans-serif;
}

button {
    font-family: inherit;
}

#cosmoscope {

    position: relative;

    width: 100vw;
    height: 100vh;

    overflow: hidden;

    background:
        radial-gradient(
            ellipse at 50% 45%,
            #0a1724 0%,
            #030811 48%,
            #010205 100%
        );
}


/* ==========================================================
   BACKGROUND
   ========================================================== */

.background {

    position: absolute;

    inset: 0;

    z-index: 0;

    background-image:
        radial-gradient(
            circle at 20% 25%,
            rgba(130,190,225,.055) 0 1px,
            transparent 2px
        ),
        radial-gradient(
            circle at 75% 70%,
            rgba(130,190,225,.04) 0 1px,
            transparent 2px
        );

    background-size:
        175px 175px,
        240px 240px;

    animation:
        backgroundDrift 38s linear infinite;

    pointer-events: none;
}

@keyframes backgroundDrift {

    from {
        transform: translate3d(0,0,0);
    }

    to {
        transform: translate3d(-70px,28px,0);
    }
}


/* ==========================================================
   HEADER
   ========================================================== */

.header {

    position: absolute;

    left: 0;
    right: 0;
    top: 0;

    height: 78px;

    z-index: 60;

    display: flex;

    align-items: center;

    justify-content: space-between;

    padding: 0 28px;

    border-bottom:
        1px solid
        rgba(170,215,240,.10);

    background:
        linear-gradient(
            180deg,
            rgba(2,7,13,.96),
            rgba(2,7,13,.65),
            transparent
        );
}

.brand {

    font-size: 11px;

    font-weight: 600;

    letter-spacing: 4px;

    color:
        rgba(242,249,255,.95);
}

.headerCenter {

    font-size: 8px;

    letter-spacing: 3px;

    color:
        rgba(165,205,230,.48);
}

.status {

    display: flex;

    align-items: center;

    gap: 8px;

    font-size: 7px;

    letter-spacing: 1.7px;

    color:
        rgba(190,225,242,.58);
}

.statusDot {

    width: 6px;
    height: 6px;

    border-radius: 50%;

    background: #a8ddff;

    box-shadow:
        0 0 12px
        rgba(100,210,255,.8);

    animation:
        statusPulse 2s ease-in-out infinite;
}

@keyframes statusPulse {

    0%,
    100% {
        opacity: .4;
    }

    50% {
        opacity: 1;
    }
}


/* ==========================================================
   LEFT NAV
   ========================================================== */

.leftPanel {

    position: absolute;

    left: 22px;

    top: 102px;
    bottom: 28px;

    width: 222px;

    z-index: 45;

    border-right:
        1px solid
        rgba(160,210,240,.09);

    padding-right: 18px;
}

.navHeading {

    margin-bottom: 13px;

    font-size: 7px;

    letter-spacing: 2.8px;

    color:
        rgba(145,195,225,.42);
}

.nav {

    display: flex;

    flex-direction: column;

    gap: 5px;
}

.navButton {

    position: relative;

    width: 100%;

    height: 43px;

    border:
        1px solid
        transparent;

    border-radius: 3px;

    background:
        rgba(5,14,23,.46);

    color:
        rgba(210,231,243,.55);

    cursor: pointer;

    text-align: left;

    padding: 0 12px;

    font-size: 8px;

    letter-spacing: 1.8px;

    transition:
        background .25s ease,
        border .25s ease,
        color .25s ease;
}

.navButton:hover {

    background:
        rgba(18,47,70,.54);

    border-color:
        rgba(170,220,248,.18);

    color: #f3fbff;
}

.navButton.active {

    background:
        linear-gradient(
            90deg,
            rgba(35,88,120,.52),
            rgba(12,32,49,.50)
        );

    border-color:
        rgba(170,220,248,.34);

    color: #f3fbff;

    box-shadow:
        inset 0 0 22px
        rgba(100,190,235,.035);
}

.navButton.active::before {

    content: "";

    position: absolute;

    left: -1px;

    top: 8px;
    bottom: 8px;

    width: 2px;

    background: #a9ddff;

    box-shadow:
        0 0 13px
        rgba(120,215,255,.75);
}


/* ==========================================================
   MAIN VIEWER
   ========================================================== */

.viewer {

    position: absolute;

    left: 260px;
    right: 320px;

    top: 98px;
    bottom: 78px;

    overflow: hidden;

    background: #000;

    border:
        1px solid
        rgba(170,220,245,.17);

    border-radius: 5px;

    box-shadow:
        0 25px 80px
        rgba(0,0,0,.55);

    cursor: grab;

    touch-action: none;
}

.viewer.dragging {
    cursor: grabbing;
}


/* ==========================================================
   STILL IMAGE CAMERA
   ========================================================== */

#spaceImage {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 100%;
    height: 100%;

    object-fit: contain;

    transform-origin: center center;

    user-select: none;

    pointer-events: none;

    will-change: transform, opacity;

    backface-visibility: hidden;

    opacity: 0;

    transition:
        opacity .5s ease;

    filter:
        saturate(1.04)
        contrast(1.015);
}


/* ==========================================================
   BLACK HOLE VIDEO
   ========================================================== */

#spaceVideo {

    position: absolute;

    left: 50%;
    top: 50%;

    width: 100%;
    height: 100%;

    object-fit: contain;

    transform:
        translate3d(-50%,-50%,0)
        scale(1);

    transform-origin: center center;

    opacity: 0;

    pointer-events: none;

    transition:
        opacity .45s ease;

    background: #000;

    filter:
        saturate(1.03)
        contrast(1.03);

    will-change:
        transform,
        opacity;
}


/* ==========================================================
   VIEWER DEPTH
   ========================================================== */

.viewer::before {

    content: "";

    position: absolute;

    inset: 0;

    z-index: 12;

    pointer-events: none;

    background:
        radial-gradient(
            ellipse at center,
            transparent 46%,
            rgba(0,0,0,.08) 70%,
            rgba(0,0,0,.34) 100%
        );
}

.viewer::after {

    content: "";

    position: absolute;

    inset: 0;

    z-index: 13;

    pointer-events: none;

    background:
        linear-gradient(
            180deg,
            rgba(255,255,255,.018),
            transparent 25%,
            transparent 78%,
            rgba(0,0,0,.13)
        );
}


/* ==========================================================
   IMAGE DATA
   ========================================================== */

.imageInfo {

    position: absolute;

    left: 14px;
    right: 14px;
    top: 14px;

    z-index: 25;

    display: flex;

    justify-content: space-between;

    pointer-events: none;
}

.imageTag,
.cameraTag {

    padding: 7px 10px;

    border:
        1px solid
        rgba(180,220,245,.18);

    border-radius: 3px;

    background:
        rgba(0,0,0,.52);

    font-size: 7px;

    letter-spacing: 1.7px;

    color:
        rgba(230,244,251,.68);

    backdrop-filter:
        blur(5px);
}


/* ==========================================================
   SUBTLE SCAN
   ========================================================== */

.scanLine {

    position: absolute;

    left: 0;
    right: 0;

    top: -5px;

    height: 1px;

    z-index: 18;

    pointer-events: none;

    background:
        rgba(175,225,248,.07);

    box-shadow:
        0 0 12px
        rgba(140,210,245,.08);

    animation:
        scan 10s linear infinite;
}

@keyframes scan {

    0% {
        top: -5px;
        opacity: 0;
    }

    10% {
        opacity: .35;
    }

    90% {
        opacity: .10;
    }

    100% {
        top: 105%;
        opacity: 0;
    }
}


/* ==========================================================
   REGION MARKER
   ========================================================== */

.targetMarker {

    position: absolute;

    width: 58px;
    height: 58px;

    z-index: 30;

    pointer-events: none;

    opacity: 0;

    transition:
        opacity .3s ease;
}

.targetMarker.visible {
    opacity: .62;
}

.targetMarker::before,
.targetMarker::after {

    content: "";

    position: absolute;

    background:
        rgba(190,228,247,.72);
}

.targetMarker::before {

    left: 0;
    right: 0;

    top: 50%;

    height: 1px;
}

.targetMarker::after {

    top: 0;
    bottom: 0;

    left: 50%;

    width: 1px;
}

.targetLabel {

    position: absolute;

    left: 34px;
    top: 29px;

    white-space: nowrap;

    font-size: 6px;

    letter-spacing: 1.4px;

    color:
        rgba(225,243,250,.64);
}


/* ==========================================================
   RIGHT PANEL
   ========================================================== */

.rightPanel {

    position: absolute;

    right: 22px;

    top: 98px;
    bottom: 28px;

    width: 280px;

    z-index: 45;

    display: flex;

    flex-direction: column;
}

.objectType {

    font-size: 7px;

    letter-spacing: 2.7px;

    color:
        rgba(150,200,230,.48);

    margin-bottom: 8px;
}

.objectTitle {

    font-size: 27px;

    font-weight: 300;

    letter-spacing: 1.2px;

    line-height: 1.1;

    color:
        #f5fbff;

    margin-bottom: 12px;
}

.objectSubtitle {

    font-size: 9px;

    line-height: 1.75;

    color:
        rgba(205,227,240,.62);

    margin-bottom: 17px;
}


/* ==========================================================
   DATA
   ========================================================== */

.dataGrid {

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 6px;
}

.dataCard {

    min-height: 62px;

    padding: 11px;

    border:
        1px solid
        rgba(155,205,235,.12);

    border-radius: 4px;

    background:
        rgba(5,14,24,.56);
}

.dataLabel {

    margin-bottom: 7px;

    font-size: 6px;

    letter-spacing: 1.7px;

    color:
        rgba(145,195,225,.44);
}

.dataValue {

    font-size: 9px;

    line-height: 1.45;

    color:
        rgba(235,247,252,.82);
}


/* ==========================================================
   SCIENCE BOX
   ========================================================== */

.scienceBox {

    margin-top: 8px;

    padding: 13px;

    border:
        1px solid
        rgba(155,205,235,.11);

    border-radius: 4px;

    background:
        rgba(5,14,24,.46);
}

.scienceHeading {

    margin-bottom: 7px;

    font-size: 6px;

    letter-spacing: 2px;

    color:
        rgba(145,195,225,.43);
}

.scienceText {

    font-size: 8px;

    line-height: 1.7;

    color:
        rgba(205,226,239,.61);
}


/* ==========================================================
   OBSERVATION VIEWS
   ========================================================== */

.views {

    margin-top: auto;
}

.viewsHeading {

    margin-bottom: 7px;

    font-size: 6px;

    letter-spacing: 2px;

    color:
        rgba(145,195,225,.42);
}

.viewRow {

    display: flex;

    gap: 6px;
}

.viewButton {

    flex: 1;

    height: 48px;

    padding: 0;

    overflow: hidden;

    border:
        1px solid
        rgba(155,205,235,.13);

    border-radius: 3px;

    background: #03070b;

    cursor: pointer;

    opacity: .55;

    transition:
        opacity .2s ease,
        border .2s ease;
}

.viewButton:hover {

    opacity: .95;

    border-color:
        rgba(180,225,250,.42);
}

.viewButton.active {

    opacity: 1;

    border-color:
        rgba(180,230,255,.70);
}

.viewButton img {

    width: 100%;
    height: 100%;

    object-fit: cover;
}


/* ==========================================================
   CAMERA CONTROLS
   ========================================================== */

.cameraControls {

    position: absolute;

    left: 260px;
    right: 320px;

    bottom: 25px;

    height: 36px;

    z-index: 55;

    display: flex;

    justify-content: center;

    align-items: center;

    gap: 5px;
}

.control {

    height: 34px;

    min-width: 43px;

    padding:
        0 10px;

    border:
        1px solid
        rgba(160,210,240,.16);

    border-radius: 3px;

    background:
        rgba(4,12,21,.86);

    color:
        rgba(215,235,247,.68);

    cursor: pointer;

    font-size: 7px;

    letter-spacing: 1.4px;

    transition:
        .2s ease;
}

.control:hover {

    background:
        rgba(20,55,80,.82);

    border-color:
        rgba(180,230,250,.48);

    color: #fff;
}

.control.active {

    border-color:
        rgba(170,225,250,.55);

    color: #f3fbff;

    background:
        rgba(20,55,78,.75);
}

.zoomReadout {

    min-width: 55px;

    text-align: center;

    font-size: 7px;

    letter-spacing: 1.4px;

    color:
        rgba(180,215,235,.52);
}


/* ==========================================================
   LOCATION
   ========================================================== */

.location {

    position: absolute;

    left: 22px;

    bottom: 29px;

    z-index: 55;
}

.locationLabel {

    margin-bottom: 5px;

    font-size: 6px;

    letter-spacing: 2px;

    color:
        rgba(145,195,225,.38);
}

.locationValue {

    font-size: 8px;

    letter-spacing: 1.2px;

    color:
        rgba(215,235,246,.62);
}


/* ==========================================================
   MODAL
   ========================================================== */

.modalLayer {

    position: absolute;

    inset: 0;

    z-index: 100;

    display: flex;

    justify-content: center;

    align-items: center;

    background:
        rgba(0,3,7,.76);

    backdrop-filter:
        blur(9px);

    opacity: 0;

    visibility: hidden;

    pointer-events: none;

    transition:
        opacity .25s ease;
}

.modalLayer.open {

    opacity: 1;

    visibility: visible;

    pointer-events: auto;
}

.modal {

    width: min(660px, 88vw);

    max-height: 80vh;

    overflow: auto;

    padding: 27px;

    border:
        1px solid
        rgba(175,220,247,.25);

    border-radius: 5px;

    background:
        rgba(3,11,20,.97);

    box-shadow:
        0 30px 100px
        rgba(0,0,0,.65);
}

.modalHeader {

    display: flex;

    justify-content: space-between;

    align-items: flex-start;

    padding-bottom: 17px;

    margin-bottom: 17px;

    border-bottom:
        1px solid
        rgba(160,210,240,.12);
}

.modalLabel {

    font-size: 6px;

    letter-spacing: 2.5px;

    color:
        rgba(150,200,230,.45);

    margin-bottom: 7px;
}

.modalTitle {

    font-size: 24px;

    font-weight: 300;

    letter-spacing: 1.3px;
}

.closeButton {

    width: 31px;
    height: 31px;

    border: none;

    border-radius: 3px;

    background:
        rgba(255,255,255,.05);

    color:
        rgba(220,238,248,.68);

    cursor: pointer;

    font-size: 17px;
}

.closeButton:hover {

    background:
        rgba(255,255,255,.11);

    color: white;
}

.modalText {

    font-size: 10px;

    line-height: 1.85;

    color:
        rgba(210,232,242,.70);
}

.modalFact {

    margin-top: 18px;

    padding: 14px;

    border-left:
        2px solid
        rgba(160,215,245,.45);

    background:
        rgba(100,170,220,.05);

    font-size: 8px;

    line-height: 1.75;

    color:
        rgba(195,225,240,.62);
}


/* ==========================================================
   LOADING
   ========================================================== */

.loading {

    position: absolute;

    inset: 0;

    z-index: 90;

    display: flex;

    align-items: center;

    justify-content: center;

    background:
        rgba(0,3,7,.60);

    pointer-events: none;

    opacity: 0;

    transition:
        opacity .25s ease;
}

.loading.show {
    opacity: 1;
}

.loadingText {

    padding:
        11px 15px;

    border:
        1px solid
        rgba(175,220,245,.18);

    border-radius: 3px;

    background:
        rgba(2,9,16,.88);

    font-size: 7px;

    letter-spacing: 2px;

    color:
        rgba(220,240,249,.68);
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 1100px) {

    .rightPanel {
        display: none;
    }

    .viewer {
        right: 22px;
    }

    .cameraControls {
        right: 22px;
    }
}

@media (max-width: 750px) {

    .headerCenter,
    .status {
        display: none;
    }

    .leftPanel {

        left: 10px;
        right: 10px;

        top: 76px;

        bottom: auto;

        width: auto;

        height: 50px;

        border-right: none;

        padding-right: 0;
    }

    .navHeading {
        display: none;
    }

    .nav {

        flex-direction: row;

        overflow-x: auto;
    }

    .navButton {
        min-width: 130px;
    }

    .viewer {

        left: 10px;
        right: 10px;

        top: 137px;
        bottom: 85px;
    }

    .cameraControls {

        left: 10px;
        right: 10px;

        bottom: 28px;

        overflow-x: auto;

        justify-content: flex-start;
    }

    .location {
        display: none;
    }
}

</style>

</head>


<body>

<div id="cosmoscope">


    <div class="background"></div>


    <!-- ======================================================
         HEADER
         ====================================================== -->

    <header class="header">

        <div class="brand">
            COSMOSCOPE
        </div>

        <div class="headerCenter">
            DEEP SPACE EXPLORATION / SCENE 04
        </div>

        <div class="status">

            <span class="statusDot"></span>

            OPTICAL EXPLORATION ACTIVE

        </div>

    </header>


    <!-- ======================================================
         LEFT NAVIGATION
         ====================================================== -->

    <aside class="leftPanel">

        <div class="navHeading">
            EXPLORATION TARGETS
        </div>

        <nav class="nav">

            <button
                class="navButton active"
                data-object="nebula"
            >
                01 / NEBULAE
            </button>

            <button
                class="navButton"
                data-object="cluster"
            >
                02 / STAR CLUSTERS
            </button>

            <button
                class="navButton"
                data-object="blackhole"
            >
                03 / BLACK HOLES
            </button>

            <button
                class="navButton"
                data-object="galaxy"
            >
                04 / OTHER GALAXIES
            </button>

            <button
                class="navButton"
                data-object="exoplanet"
            >
                05 / EXOPLANETS
            </button>

        </nav>

    </aside>


    <!-- ======================================================
         MAIN VIEWER
         ====================================================== -->

    <main
        class="viewer"
        id="viewer"
    >

        <div class="imageInfo">

            <div
                class="imageTag"
                id="imageTag"
            >
                NASA / JWST
            </div>

            <div
                class="cameraTag"
                id="cameraTag"
            >
                OPTICAL CAMERA / ACTIVE
            </div>

        </div>


        <div class="scanLine"></div>


        <!-- REAL SPACE IMAGE -->

        <img
            id="spaceImage"
            draggable="false"
            alt="Astronomical object"
        >


        <!-- REAL NASA BLACK HOLE VIDEO -->

        <video
            id="spaceVideo"
            muted
            autoplay
            loop
            playsinline
            preload="auto"
        ></video>


        <div
            class="targetMarker"
            id="targetMarker"
            style="
                left: 45%;
                top: 38%;
            "
        >

            <div class="targetLabel">
                REGION OF INTEREST
            </div>

        </div>


        <div
            class="loading"
            id="loading"
        >

            <div class="loadingText">
                ACQUIRING ASTRONOMICAL IMAGE
            </div>

        </div>

    </main>


    <!-- ======================================================
         RIGHT SCIENCE PANEL
         ====================================================== -->

    <aside class="rightPanel">

        <div
            class="objectType"
            id="objectType"
        >
            EMISSION NEBULA
        </div>

        <div
            class="objectTitle"
            id="objectTitle"
        >
            PILLARS OF CREATION
        </div>

        <div
            class="objectSubtitle"
            id="objectSubtitle"
        >
            A star-forming region inside the Eagle Nebula,
            observed in infrared wavelengths.
        </div>


        <div class="dataGrid">

            <div class="dataCard">

                <div class="dataLabel">
                    TYPE
                </div>

                <div
                    class="dataValue"
                    id="dataType"
                >
                    Emission Nebula
                </div>

            </div>


            <div class="dataCard">

                <div class="dataLabel">
                    CATALOG
                </div>

                <div
                    class="dataValue"
                    id="dataCatalog"
                >
                    M16
                </div>

            </div>


            <div class="dataCard">

                <div class="dataLabel">
                    DISTANCE
                </div>

                <div
                    class="dataValue"
                    id="dataDistance"
                >
                    ~6,500 ly
                </div>

            </div>


            <div class="dataCard">

                <div class="dataLabel">
                    OBSERVATORY
                </div>

                <div
                    class="dataValue"
                    id="dataTelescope"
                >
                    JWST
                </div>

            </div>

        </div>


        <div class="scienceBox">

            <div class="scienceHeading">
                SCIENTIFIC CONTEXT
            </div>

            <div
                class="scienceText"
                id="scienceText"
            >
                Dense clouds of gas and dust form active
                environments where new stars can form.
            </div>

        </div>


        <div class="views">

            <div class="viewsHeading">
                AVAILABLE OBSERVATION VIEWS
            </div>

            <div
                class="viewRow"
                id="viewRow"
            ></div>

        </div>

    </aside>


    <!-- ======================================================
         CAMERA CONTROLS
         ====================================================== -->

    <div class="cameraControls">

        <button
            class="control"
            id="zoomOut"
        >
            −
        </button>

        <div
            class="zoomReadout"
            id="zoomReadout"
        >
            100%
        </div>

        <button
            class="control"
            id="zoomIn"
        >
            +
        </button>

        <button
            class="control"
            id="reset"
        >
            RESET VIEW
        </button>

        <button
            class="control active"
            id="motion"
        >
            MOTION ON
        </button>

        <button
            class="control"
            id="speed"
        >
            SPEED 1X
        </button>

        <button
            class="control"
            id="markers"
        >
            MARKERS
        </button>

        <button
            class="control"
            id="science"
        >
            SCIENCE
        </button>

    </div>


    <!-- ======================================================
         LOCATION
         ====================================================== -->

    <div class="location">

        <div class="locationLabel">
            CURRENT REGION
        </div>

        <div
            class="locationValue"
            id="locationValue"
        >
            EAGLE NEBULA / M16
        </div>

    </div>


    <!-- ======================================================
         SCIENCE MODAL
         ====================================================== -->

    <div
        class="modalLayer"
        id="modalLayer"
    >

        <section class="modal">

            <div class="modalHeader">

                <div>

                    <div class="modalLabel">
                        COSMOSCOPE SCIENCE FILE
                    </div>

                    <div
                        class="modalTitle"
                        id="modalTitle"
                    >
                        PILLARS OF CREATION
                    </div>

                </div>

                <button
                    class="closeButton"
                    id="closeModal"
                >
                    ×
                </button>

            </div>


            <div
                class="modalText"
                id="modalText"
            >
                Dense clouds of gas and dust inside the
                Eagle Nebula form a complex stellar nursery.
            </div>


            <div
                class="modalFact"
                id="modalFact"
            >
                Infrared observations allow astronomers to
                examine structures hidden by interstellar dust.
            </div>

        </section>

    </div>

</div>


<script>

/* ==========================================================
   REAL LOCAL ASSETS
   ========================================================== */

const ASSETS = {

    nebulaVideo:
        "__NEBULA_VIDEO__",

    starClusterVideo:
        "__STAR_CLUSTER_VIDEO__",

    blackHoleVideo:
        "__BLACK_HOLE_VIDEO__",

    galaxyVideo:
        "__GALAXY_VIDEO__",

    exoplanetVideo:
        "__EXOPLANET_VIDEO__",

    blackHoleStill:
        "__BLACK_HOLE_STILL__",

    andromeda:
        "__ANDROMEDA__",

    exoplanet:
        "__EXOPLANET__",

    exoplanetTypes:
        "__EXOPLANET_TYPES__"

};


/* ==========================================================
   OBJECT DATABASE
   ========================================================== */

const DATA = {

    nebula: {

        type:
            "EMISSION NEBULA",

        title:
            "PILLARS OF CREATION",

        subtitle:
            "A star-forming region inside the Eagle Nebula, observed in infrared wavelengths.",

        dataType:
            "Emission Nebula",

        catalog:
            "M16",

        distance:
            "~6,500 ly",

        telescope:
            "JWST",

        location:
            "EAGLE NEBULA / M16",

        tag:
            "NASA / JWST",

        science:
            "Dense clouds of gas and dust form active environments where young stars develop. Infrared observations reveal structures hidden by dust.",

        modal:
            "The Pillars of Creation are dense structures within the Eagle Nebula. Their dusty environment contains regions where new stars are forming.",

        fact:
            "Infrared observations are especially useful for examining stellar nurseries because infrared light can pass through more dust than visible light.",

        views: [
            {
                key: "nebulaVideo",
                label: "NASA WEBM"
            }
        ],

        profile: {

            zoom: 0.055,

            driftX: 24,

            driftY: 15,

            speed: 0.00016,

            parallax: 8

        }

    },


    cluster: {

        type:
            "GLOBULAR STAR CLUSTER",

        title:
            "NGC 362",

        subtitle:
            "A dense spherical concentration of stars held together by gravity.",

        dataType:
            "Globular Cluster",

        catalog:
            "NGC 362",

        distance:
            "~28,000 ly",

        telescope:
            "HUBBLE",

        location:
            "NGC 362 / STAR CLUSTER",

        tag:
            "NASA / HUBBLE",

        science:
            "Globular clusters contain huge populations of stars packed into relatively compact regions.",

        modal:
            "NGC 362 is a globular star cluster. Its dense stellar population provides astronomers with a useful environment for studying stellar evolution and old stellar systems.",

        fact:
            "The apparent spherical structure comes from the gravitational binding of a very large population of stars.",

        views: [
            {
                key: "starClusterVideo",
                label: "NASA WEBM"
            }
        ],

        profile: {

            zoom: 0.035,

            driftX: 16,

            driftY: 9,

            speed: 0.00012,

            parallax: 6

        }

    },


    blackhole: {

        type:
            "COMPACT GRAVITATIONAL OBJECT",

        title:
            "BLACK HOLE",

        subtitle:
            "A region of spacetime where gravity is strong enough that light cannot escape beyond the event horizon.",

        dataType:
            "Scientific Visualization",

        catalog:
            "NASA MODEL",

        distance:
            "SIMULATION",

        telescope:
            "NASA / GSFC",

        location:
            "BLACK HOLE / ACCRETION DISK",

        tag:
            "NASA / SCIENTIFIC VISUALIZATION",

        science:
            "Hot material around a black hole can form an accretion disk as matter falls inward under extreme gravity.",

        modal:
            "The black-hole animation shows a scientific visualization of an accretion disk around a black hole. The dark central region represents the black hole, while the bright surrounding structure represents hot material.",

        fact:
            "The moving visualization is a scientific simulation. It is not a direct photograph of the black hole itself.",

        views: [
            {
                key: "blackHoleVideo",
                label: "NASA 360°"
            }
        ],

        profile: {

            zoom: 0.025,

            driftX: 5,

            driftY: 4,

            speed: 0.00008,

            parallax: 3

        }

    },


    galaxy: {

        type:
            "SPIRAL GALAXY",

        title:
            "ANDROMEDA GALAXY",

        subtitle:
            "The nearest major spiral galaxy to the Milky Way.",

        dataType:
            "Spiral Galaxy",

        catalog:
            "M31",

        distance:
            "~2.5 million ly",

        telescope:
            "NASA / ESA",

        location:
            "ANDROMEDA / M31",

        tag:
            "NASA / ESA / HUBBLE",

        science:
            "Andromeda is a large spiral galaxy containing hundreds of billions of stars and extensive dust and star-forming regions.",

        modal:
            "The Andromeda Galaxy, catalogued as M31, is the nearest major galaxy to the Milky Way and provides astronomers with an important laboratory for studying galaxy structure and evolution.",

        fact:
            "Its immense distance means that the light reaching Earth has travelled for roughly 2.5 million years.",

        views: [
            {
                key: "galaxyVideo",
                label: "NASA WEBM"
            }
        ],

        profile: {

            zoom: 0.065,

            driftX: 30,

            driftY: 13,

            speed: 0.00010,

            parallax: 11

        }

    },


    exoplanet: {

        type:
            "EXOPLANET",

        title:
            "EXOPLANET WORLDS",

        subtitle:
            "Planets orbiting stars beyond our Solar System, detected using astronomical observations.",

        dataType:
            "Planet Beyond Solar System",

        catalog:
            "EXOPLANET ARCHIVE",

        distance:
            "VARIES",

        telescope:
            "NASA MISSIONS",

        location:
            "EXOPLANET EXPLORATION",

        tag:
            "NASA EXOPLANET ARCHIVE",

        science:
            "Astronomers detect exoplanets using methods such as transits and radial velocity measurements.",

        modal:
            "Thousands of confirmed exoplanets have been identified beyond our Solar System. Their sizes, orbital periods, temperatures and host stars provide clues about planetary formation and diversity.",

        fact:
            "Many exoplanets are too distant to photograph directly. Their existence can often be inferred from the effect they produce on their host star.",

        views: [
            {
                key: "exoplanetVideo",
                label: "NASA WEBM"
            }
        ],

        profile: {

            zoom: 0.050,

            driftX: 18,

            driftY: 12,

            speed: 0.00014,

            parallax: 8

        }

    }

};


/* ==========================================================
   STATE
   ========================================================== */

let currentObject = "nebula";

let currentImageKey = "pillars";

let motionEnabled = true;

let playbackSpeed = 1;

let markersEnabled = false;

let scienceOpen = false;

let cameraPaused = false;

let panX = 0;

let panY = 0;

let zoom = 1;

let targetZoom = 1;

let pointerX = 0;

let pointerY = 0;

let manualOffsetX = 0;

let manualOffsetY = 0;

let motionTime = Math.random() * 1000;

let lastFrame = performance.now();

let dragStartX = 0;

let dragStartY = 0;

let dragOriginX = 0;

let dragOriginY = 0;

let dragging = false;


/* ==========================================================
   DOM
   ========================================================== */

const viewer =
    document.getElementById("viewer");

const image =
    document.getElementById("spaceImage");

const spaceVideo =
    document.getElementById("spaceVideo");

const imageTag =
    document.getElementById("imageTag");

const cameraTag =
    document.getElementById("cameraTag");

const objectType =
    document.getElementById("objectType");

const objectTitle =
    document.getElementById("objectTitle");

const objectSubtitle =
    document.getElementById("objectSubtitle");

const dataType =
    document.getElementById("dataType");

const dataCatalog =
    document.getElementById("dataCatalog");

const dataDistance =
    document.getElementById("dataDistance");

const dataTelescope =
    document.getElementById("dataTelescope");

const scienceText =
    document.getElementById("scienceText");

const locationValue =
    document.getElementById("locationValue");

const viewRow =
    document.getElementById("viewRow");

const targetMarker =
    document.getElementById("targetMarker");

const loading =
    document.getElementById("loading");

const zoomReadout =
    document.getElementById("zoomReadout");

const modalLayer =
    document.getElementById("modalLayer");

const modalTitle =
    document.getElementById("modalTitle");

const modalText =
    document.getElementById("modalText");

const modalFact =
    document.getElementById("modalFact");

const motionButton =
    document.getElementById("motion");

const speedButton =
    document.getElementById("speed");

const markersButton =
    document.getElementById("markers");

const scienceButton =
    document.getElementById("science");


/* ==========================================================
   UTILITY
   ========================================================== */

function clamp(value, min, max) {

    return Math.max(
        min,
        Math.min(max, value)
    );

}


/* ==========================================================
   UPDATE CAMERA STATUS
   ========================================================== */

function updateCameraStatus() {

    if (!motionEnabled) {

        cameraTag.textContent =
            "OPTICAL CAMERA / MANUAL";

        return;

    }

    if (cameraPaused) {

        cameraTag.textContent =
            "MANUAL EXPLORATION / PAUSED";

        return;

    }

    cameraTag.textContent =
        "OPTICAL CAMERA / ACTIVE";

}


/* ==========================================================
   UPDATE TRANSFORM
   ========================================================== */

function updateTransform() {

    const objectData =
        DATA[currentObject];

    const profile =
        objectData.profile;

    const time =
        motionTime;

    let autoX = 0;

    let autoY = 0;

    let autoZoom = 1;


    if (motionEnabled && !cameraPaused) {

        autoX =
            Math.sin(
                time * profile.speed
            ) *
            profile.driftX;

        autoY =
            Math.cos(
                time * profile.speed * 0.83
            ) *
            profile.driftY;

        autoZoom =
            1 +
            Math.sin(
                time * profile.speed * 0.62
            ) *
            profile.zoom;

    }


    const totalX =
        autoX +
        manualOffsetX +
        panX;

    const totalY =
        autoY +
        manualOffsetY +
        panY;


    const finalZoom =
        targetZoom *
        autoZoom;


    if (spaceVideo.style.opacity === "1") {

        spaceVideo.style.transform =
            "translate3d(" +
            (
                -50 +
                totalX / 8
            ) +
            "%," +
            (
                -50 +
                totalY / 8
            ) +
            "%,0) scale(" +
            finalZoom +
            ")";

        return;

    }


    image.style.transform =
        "translate3d(" +
        (
            -50 +
            totalX / 8
        ) +
        "%," +
        (
            -50 +
            totalY / 8
        ) +
        "%,0) scale(" +
        finalZoom +
        ")";

}


/* ==========================================================
   SMOOTH POINTER PARALLAX
   ========================================================== */

function updateParallax() {

    const objectData =
        DATA[currentObject];

    const profile =
        objectData.profile;

    const targetX =
        pointerX *
        profile.parallax;

    const targetY =
        pointerY *
        profile.parallax;


    manualOffsetX +=
        (
            targetX -
            manualOffsetX
        ) *
        0.035;


    manualOffsetY +=
        (
            targetY -
            manualOffsetY
        ) *
        0.035;

}


/* ==========================================================
   CAMERA LOOP
   ========================================================== */

function cameraLoop(now) {

    const delta =
        now -
        lastFrame;

    lastFrame = now;

    motionTime +=
        delta;

    updateParallax();

    updateTransform();

    updateCameraStatus();

    requestAnimationFrame(
        cameraLoop
    );

}


/* ==========================================================
   IMAGE LOADING
   ========================================================== */

function loadVideo(key) {

    const src = ASSETS[key];

    currentImageKey = key;

    loading.classList.add("show");

    cameraPaused = true;

    panX = 0;
    panY = 0;
    zoom = 1;
    targetZoom = 1;
    motionTime = Math.random() * 30000;

    image.style.opacity = "0";

    try {
        spaceVideo.pause();
    }
    catch (e) {}

    if (!src) {
        spaceVideo.removeAttribute("src");
        spaceVideo.style.opacity = "0";
        loading.classList.remove("show");
        cameraPaused = false;
        updateCameraStatus();
        return;
    }

    spaceVideo.style.opacity = "0";
    spaceVideo.src = src;
    spaceVideo.currentTime = 0;
    spaceVideo.playbackRate = playbackSpeed;

    spaceVideo.onloadedmetadata = function() {
        try {
            spaceVideo.currentTime = 0;
        }
        catch (e) {}

        spaceVideo.style.opacity = "1";

        const playPromise = spaceVideo.play();
        if (playPromise && playPromise.catch) {
            playPromise.catch(function() {});
        }

        setTimeout(function() {
            loading.classList.remove("show");
            cameraPaused = false;
            updateCameraStatus();
        }, 220);
    };

    spaceVideo.onerror = function() {
        spaceVideo.style.opacity = "0";
        loading.classList.remove("show");
        cameraPaused = false;
        updateCameraStatus();
    };

}


/* ==========================================================
   30 SECOND SCIENTIFIC LOOP
   ========================================================== */

spaceVideo.addEventListener("timeupdate", function() {

    if (!spaceVideo.src) {
        return;
    }

    if (spaceVideo.currentTime >= 30) {
        try {
            spaceVideo.currentTime = 0;
            spaceVideo.play();
        }
        catch (e) {}
    }

});


/* ==========================================================
   BLACK HOLE VIDEO
   ========================================================== */

function showBlackHole() {

    loadVideo("blackHoleVideo");

}


/* ==========================================================
   UPDATE INFORMATION
   ========================================================== */

function updateInformation() {

    const objectData =
        DATA[currentObject];


    objectType.textContent =
        objectData.type;

    objectTitle.textContent =
        objectData.title;

    objectSubtitle.textContent =
        objectData.subtitle;

    dataType.textContent =
        objectData.dataType;

    dataCatalog.textContent =
        objectData.catalog;

    dataDistance.textContent =
        objectData.distance;

    dataTelescope.textContent =
        objectData.telescope;

    scienceText.textContent =
        objectData.science;

    locationValue.textContent =
        objectData.location;

    imageTag.textContent =
        objectData.tag;


    modalTitle.textContent =
        objectData.title;

    modalText.textContent =
        objectData.modal;

    modalFact.textContent =
        objectData.fact;


    buildViews();

}


/* ==========================================================
   BUILD VIEW BUTTONS
   ========================================================== */

function buildViews() {

    viewRow.innerHTML =
        "";


    const views =
        DATA[currentObject].views;


    views.forEach(
        function(view) {

            const button =
                document.createElement(
                    "button"
                );

            button.className =
                "viewButton";


            if (
                view.key ===
                currentImageKey
            ) {

                button.classList.add(
                    "active"
                );

            }


            const thumb =
                document.createElement(
                    "div"
                );


            thumb.style.width =
                "100%";

            thumb.style.height =
                "100%";


            const thumbVideo =
                document.createElement("video");

            thumbVideo.src =
                ASSETS[view.key] ||
                "";

            thumbVideo.muted = true;
            thumbVideo.autoplay = true;
            thumbVideo.loop = true;
            thumbVideo.playsInline = true;
            thumbVideo.preload = "metadata";

            thumb.appendChild(
                thumbVideo
            );


            button.appendChild(
                thumb
            );


            button.title =
                view.label;


            button.addEventListener(
                "click",
                function(event) {

                    event.stopPropagation();

                    loadView(
                        view.key
                    );

                }
            );


            viewRow.appendChild(
                button
            );

        }
    );

}


/* ==========================================================
   LOAD VIEW
   ========================================================== */

function loadView(key) {

    currentImageKey = key;

    loadVideo(key);

    buildViews();

}


/* ==========================================================
   SELECT OBJECT
   ========================================================== */

function selectObject(key) {

    if (!DATA[key]) {
        return;
    }


    currentObject =
        key;


    document
        .querySelectorAll(
            ".navButton"
        )
        .forEach(
            function(button) {

                button.classList.toggle(
                    "active",
                    button.dataset.object ===
                    key
                );

            }
        );


    updateInformation();


    currentImageKey =
        DATA[key].views[0].key;


    loadView(
        currentImageKey
    );

}


/* ==========================================================
   NAVIGATION BUTTONS
   ========================================================== */

document
    .querySelectorAll(
        ".navButton"
    )
    .forEach(
        function(button) {

            button.addEventListener(
                "click",
                function() {

                    selectObject(
                        button.dataset.object
                    );

                }
            );

        }
    );


/* ==========================================================
   MOUSE PARALLAX
   ========================================================== */

viewer.addEventListener(
    "pointermove",
    function(event) {

        const rect =
            viewer.getBoundingClientRect();


        pointerX =
            (
                event.clientX -
                rect.left
            ) /
            rect.width -
            0.5;


        pointerY =
            (
                event.clientY -
                rect.top
            ) /
            rect.height -
            0.5;


        if (dragging) {

            const dx =
                event.clientX -
                dragStartX;

            const dy =
                event.clientY -
                dragStartY;


            panX =
                dragOriginX +
                dx /
                8;

            panY =
                dragOriginY +
                dy /
                8;

        }

    }
);


/* ==========================================================
   POINTER DOWN
   ========================================================== */

viewer.addEventListener(
    "pointerdown",
    function(event) {

        dragging =
            true;

        cameraPaused =
            true;

        viewer.classList.add(
            "dragging"
        );


        dragStartX =
            event.clientX;

        dragStartY =
            event.clientY;


        dragOriginX =
            panX;

        dragOriginY =
            panY;


        try {
            viewer.setPointerCapture(
                event.pointerId
            );
        }
        catch (e) {}

    }
);


/* ==========================================================
   POINTER UP
   ========================================================== */

function finishDrag(event) {

    if (!dragging) {
        return;
    }


    dragging =
        false;

    viewer.classList.remove(
        "dragging"
    );


    try {
        viewer.releasePointerCapture(
            event.pointerId
        );
    }
    catch (e) {}


    setTimeout(
        function() {

            cameraPaused =
                false;

        },
        1200
    );

}


viewer.addEventListener(
    "pointerup",
    finishDrag
);

viewer.addEventListener(
    "pointercancel",
    finishDrag
);


/* ==========================================================
   POINTER LEAVE
   ========================================================== */

viewer.addEventListener(
    "pointerleave",
    function() {

        pointerX *= .88;
        pointerY *= .88;

    }
);


/* ==========================================================
   WHEEL ZOOM
   ========================================================== */

viewer.addEventListener(
    "wheel",
    function(event) {

        event.preventDefault();

        const amount =
            event.deltaY < 0
                ? 0.08
                : -0.08;


        targetZoom =
            clamp(
                targetZoom + amount,
                0.8,
                2.5
            );


        updateZoomReadout();

    },
    {
        passive: false
    }
);


/* ==========================================================
   ZOOM BUTTONS
   ========================================================== */

document
    .getElementById("zoomIn")
    .addEventListener(
        "click",
        function() {

            targetZoom =
                clamp(
                    targetZoom + 0.12,
                    0.8,
                    2.5
                );

            updateZoomReadout();

        }
    );


document
    .getElementById("zoomOut")
    .addEventListener(
        "click",
        function() {

            targetZoom =
                clamp(
                    targetZoom - 0.12,
                    0.8,
                    2.5
                );

            updateZoomReadout();

        }
    );


/* ==========================================================
   ZOOM READOUT
   ========================================================== */

function updateZoomReadout() {

    zoomReadout.textContent =
        Math.round(
            targetZoom * 100
        ) +
        "%";

}


/* ==========================================================
   RESET VIEW
   ========================================================== */

document
    .getElementById("reset")
    .addEventListener(
        "click",
        function() {

            panX = 0;
            panY = 0;

            targetZoom = 1;

            manualOffsetX = 0;
            manualOffsetY = 0;

            motionTime =
                Math.random() *
                30000;

            updateZoomReadout();

        }
    );


/* ==========================================================
   MOTION ON / OFF
   ========================================================== */

motionButton.addEventListener(
    "click",
    function() {

        motionEnabled =
            !motionEnabled;


        motionButton.classList.toggle(
            "active",
            motionEnabled
        );


        motionButton.textContent =
            motionEnabled
                ? "MOTION ON"
                : "MOTION OFF";


        if (!motionEnabled) {

            cameraPaused =
                false;

        }

    }
);


/* ==========================================================
   PLAYBACK SPEED
   ========================================================== */

speedButton.addEventListener(
    "click",
    function() {

        playbackSpeed =
            playbackSpeed === 1
                ? 2
                : 1;

        spaceVideo.playbackRate =
            playbackSpeed;

        speedButton.textContent =
            playbackSpeed === 2
                ? "SPEED 2X"
                : "SPEED 1X";

        speedButton.classList.toggle(
            "active",
            playbackSpeed === 2
        );

    }
);


/* ==========================================================
   MARKERS
   ========================================================== */

markersButton.addEventListener(
    "click",
    function() {

        markersEnabled =
            !markersEnabled;


        targetMarker.classList.toggle(
            "visible",
            markersEnabled
        );


        markersButton.classList.toggle(
            "active",
            markersEnabled
        );

    }
);


/* ==========================================================
   SCIENCE MODAL
   ========================================================== */

function openScience() {

    scienceOpen =
        true;

    modalLayer.classList.add(
        "open"
    );

}


function closeScience() {

    scienceOpen =
        false;

    modalLayer.classList.remove(
        "open"
    );

}


scienceButton.addEventListener(
    "click",
    openScience
);


document
    .getElementById("closeModal")
    .addEventListener(
        "click",
        closeScience
    );


modalLayer.addEventListener(
    "click",
    function(event) {

        if (
            event.target ===
            modalLayer
        ) {

            closeScience();

        }

    }
);


/* ==========================================================
   KEYBOARD CONTROLS
   ========================================================== */

document.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key ===
            "Escape"
        ) {

            closeScience();

        }


        if (
            event.key ===
            "+"
            ||
            event.key ===
            "="
        ) {

            targetZoom =
                clamp(
                    targetZoom + .1,
                    .8,
                    2.5
                );

            updateZoomReadout();

        }


        if (
            event.key ===
            "-"
        ) {

            targetZoom =
                clamp(
                    targetZoom - .1,
                    .8,
                    2.5
                );

            updateZoomReadout();

        }


        if (
            event.key ===
            "r"
            ||
            event.key ===
            "R"
        ) {

            panX = 0;
            panY = 0;

            targetZoom = 1;

            manualOffsetX = 0;
            manualOffsetY = 0;

            updateZoomReadout();

        }

    }
);


/* ==========================================================
   INITIALIZE
   ========================================================== */

updateInformation();

updateZoomReadout();

loadView(
    "nebulaVideo"
);

requestAnimationFrame(
    cameraLoop
);

</script>

</body>
</html>
"""


    # --------------------------------------------------------
    # SAFE PLACEHOLDER REPLACEMENT
    # --------------------------------------------------------

    html = (
        html
        .replace("__NEBULA_VIDEO__", NEBULA_VIDEO)
        .replace("__STAR_CLUSTER_VIDEO__", STAR_CLUSTER_VIDEO)
        .replace("__BLACK_HOLE_VIDEO__", BLACK_HOLE_VIDEO)
        .replace("__GALAXY_VIDEO__", GALAXY_VIDEO)
        .replace("__EXOPLANET_VIDEO__", EXOPLANET_VIDEO)
        .replace("__BLACK_HOLE_STILL__", BLACK_HOLE_STILL)
        .replace("__ANDROMEDA__", ANDROMEDA)
        .replace("__EXOPLANET__", EXOPLANET)
        .replace("__EXOPLANET_TYPES__", EXOPLANET_TYPES)
    )


    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    components.html(
        html,
        height=900,
        scrolling=False
    )


# ------------------------------------------------------------
# Compatibility alias
# app.py can call either name.
# ------------------------------------------------------------

def show_scence4():
    show_scene4()
