import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import mimetypes


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS = BASE_DIR / "assets"


# ============================================================
# ASSET LOADER
# ============================================================

def asset_data(filename):

    path = ASSETS / filename

    if not path.exists():
        return ""

    try:

        with open(path, "rb") as f:
            encoded = base64.b64encode(
                f.read()
            ).decode("utf-8")

        mime = (
            mimetypes.guess_type(str(path))[0]
            or "image/jpeg"
        )

        return f"data:{mime};base64,{encoded}"

    except Exception:

        return ""


# ============================================================
# LOAD SCENE 1 ASSETS
# ============================================================

EARTH = asset_data(
    "earth_texture.jpg"
)

MOON = asset_data(
    "moon_texture.jpg"
)

STARS = asset_data(
    "starfield.jpg"
)


# ============================================================
# SCENE 1
# ============================================================

def show_scene1():

    # ========================================================
    # CHECK ASSETS
    # ========================================================

    missing = []

    if not EARTH:
        missing.append(
            "earth_texture.jpg"
        )

    if not MOON:
        missing.append(
            "moon_texture.jpg"
        )

    if not STARS:
        missing.append(
            "starfield.jpg"
        )

    if missing:

        st.error(
            "Scene 1 is missing these assets: "
            + ", ".join(missing)
        )

        return


    # ========================================================
    # HTML / CSS / THREE.JS
    # ========================================================

    html = r"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta
    name="viewport"
    content="width=device-width,
             initial-scale=1.0,
             maximum-scale=1.0,
             user-scalable=no"
>

<script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>


<style>

/* ============================================================
   GLOBAL
   ============================================================ */

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

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}


body {

    position: relative;

}


/* ============================================================
   THREE.JS SPACE
   ============================================================ */

#space {

    position: fixed;

    inset: 0;

    width: 100%;

    height: 100%;

    overflow: hidden;

    background: #000;

}


canvas {

    display: block;

}


/* ============================================================
   TOP BRAND
   ============================================================ */

#brand {

    position: fixed;

    top: 32px;

    left: 38px;

    z-index: 20;

    pointer-events: none;

    color: white;

    font-size: 30px;

    font-weight: 800;

    letter-spacing: 9px;

    text-shadow:
        0 0 12px
        rgba(255,255,255,.35),

        0 0 30px
        rgba(100,160,255,.25);

}


#subtitle {

    position: fixed;

    top: 75px;

    left: 40px;

    z-index: 20;

    pointer-events: none;

    color:
        rgba(205,220,245,.72);

    font-size: 10px;

    letter-spacing: 4px;

}


/* ============================================================
   EARTH INFORMATION
   ============================================================ */

#earthInfo {

    position: fixed;

    left: 42px;

    top: 50%;

    transform:
        translateY(-50%);

    z-index: 20;

    width: 310px;

    padding: 20px;

    border-left:
        2px solid
        rgba(120,180,255,.55);

    background:
        linear-gradient(
            90deg,
            rgba(3,10,22,.72),
            rgba(3,10,22,.30),
            transparent
        );

    backdrop-filter:
        blur(5px);

    pointer-events: none;

}


#earthTag {

    color:
        rgba(140,195,255,.9);

    font-size: 9px;

    font-weight: 700;

    letter-spacing: 3px;

    margin-bottom: 8px;

}


#earthTitle {

    color: white;

    font-size: 25px;

    font-weight: 800;

    letter-spacing: 2px;

    margin-bottom: 12px;

}


#earthDescription {

    color:
        rgba(220,230,245,.72);

    font-size: 11px;

    line-height: 1.7;

    max-width: 285px;

}


/* ============================================================
   FACTS
   ============================================================ */

#facts {

    margin-top: 18px;

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 7px;

}


.fact {

    padding: 9px;

    border:
        1px solid
        rgba(130,180,255,.14);

    background:
        rgba(255,255,255,.035);

    border-radius: 6px;

}


.factLabel {

    color:
        rgba(190,210,240,.45);

    font-size: 7px;

    letter-spacing: 1px;

    margin-bottom: 4px;

}


.factValue {

    color: white;

    font-size: 10px;

}


/* ============================================================
   MOON LABEL
   ============================================================ */

#moonLabel {

    position: fixed;

    right: 120px;

    bottom: 145px;

    z-index: 20;

    pointer-events: none;

    color:
        rgba(220,230,245,.65);

    font-size: 8px;

    letter-spacing: 2px;

}


#moonLabel::before {

    content: "";

    display: inline-block;

    width: 24px;

    height: 1px;

    margin-right: 8px;

    vertical-align: middle;

    background:
        rgba(150,195,255,.5);

}


/* ============================================================
   BOTTOM STATUS
   ============================================================ */

#status {

    position: fixed;

    right: 35px;

    bottom: 30px;

    z-index: 20;

    pointer-events: none;

    color:
        rgba(205,220,245,.40);

    font-size: 8px;

    letter-spacing: 2px;

}


/* ============================================================
   TOP RIGHT STATUS
   ============================================================ */

#systemStatus {

    position: fixed;

    top: 30px;

    right: 35px;

    z-index: 20;

    pointer-events: none;

    color:
        rgba(160,205,255,.58);

    font-size: 8px;

    letter-spacing: 2px;

}


.statusDot {

    display: inline-block;

    width: 6px;

    height: 6px;

    margin-right: 6px;

    border-radius: 50%;

    background:
        #78b7ff;

    box-shadow:
        0 0 9px
        rgba(100,180,255,.8);

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

    width: 190px;

    height: 1px;

    margin-top: 16px;

    background:
        linear-gradient(
            90deg,
            transparent,
            #8db9ff,
            transparent
        );

    animation:
        loading 1.4s infinite;

}


@keyframes loading {

    0% {

        opacity: .2;

        transform:
            scaleX(.2);

    }

    50% {

        opacity: 1;

        transform:
            scaleX(1);

    }

    100% {

        opacity: .2;

        transform:
            scaleX(.2);

    }

}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {

    #brand {

        top: 20px;

        left: 20px;

        font-size: 20px;

        letter-spacing: 5px;

    }


    #subtitle {

        top: 53px;

        left: 22px;

        font-size: 7px;

        letter-spacing: 2px;

    }


    #systemStatus {

        top: 20px;

        right: 20px;

        font-size: 7px;

    }


    #earthInfo {

        left: 20px;

        top: auto;

        bottom: 125px;

        transform: none;

        width: 270px;

        padding: 14px;

    }


    #earthTitle {

        font-size: 19px;

    }


    #earthDescription {

        font-size: 9px;

    }


    #facts {

        margin-top: 10px;

    }


    #moonLabel {

        display: none;

    }


    #status {

        display: none;

    }

}

</style>

</head>


<body>


<!-- ============================================================
     THREE.JS SPACE
     ============================================================ -->

<div id="space"></div>


<!-- ============================================================
     BRAND
     ============================================================ -->

<div id="brand">
    COSMOSCOPE
</div>


<div id="subtitle">
    VIRTUAL SPACE EXPLORATION
</div>


<!-- ============================================================
     SYSTEM STATUS
     ============================================================ -->

<div id="systemStatus">

    <span class="statusDot"></span>

    EARTH SYSTEM • ONLINE

</div>


<!-- ============================================================
     EARTH INFORMATION
     ============================================================ -->

<div id="earthInfo">

    <div id="earthTag">
        EARTH — OUR HOME PLANET
    </div>


    <div id="earthTitle">
        PLANET EARTH
    </div>


    <div id="earthDescription">

        The third planet from the Sun
        and the only known world
        currently supporting life.

    </div>


    <!-- ========================================================
         FACTS
         ======================================================== -->

    <div id="facts">


        <div class="fact">

            <div class="factLabel">
                DIAMETER
            </div>

            <div class="factValue">
                12,742 km
            </div>

        </div>


        <div class="fact">

            <div class="factLabel">
                DAY
            </div>

            <div class="factValue">
                23h 56m
            </div>

        </div>


        <div class="fact">

            <div class="factLabel">
                YEAR
            </div>

            <div class="factValue">
                365.25 days
            </div>

        </div>


        <div class="fact">

            <div class="factLabel">
                MOONS
            </div>

            <div class="factValue">
                1
            </div>

        </div>


    </div>

</div>


<!-- ============================================================
     MOON LABEL
     ============================================================ -->

<div id="moonLabel">
    MOON
</div>


<!-- ============================================================
     BOTTOM STATUS
     ============================================================ -->

<div id="status">
    DRAG TO ROTATE • SCROLL TO ZOOM
</div>


<!-- ============================================================
     THREE.JS
     ============================================================ -->

<script>


/* ============================================================
   ASSET DATA
   ============================================================ */

const earthTextureData =
    "__EARTH__";


const moonTextureData =
    "__MOON__";


const starfieldTextureData =
    "__STARS__";


/* ============================================================
   CONTAINER
   ============================================================ */

const container =
    document.getElementById(
        "space"
    );


/* ============================================================
   THREE.JS SCENE
   ============================================================ */

const scene =
    new THREE.Scene();


/* ============================================================
   CAMERA
   ============================================================ */

const camera =
    new THREE.PerspectiveCamera(

        45,

        window.innerWidth /
        window.innerHeight,

        0.1,

        1000

    );


camera.position.set(
    0,
    0.8,
    7.2
);


/* ============================================================
   RENDERER
   ============================================================ */

const renderer =
    new THREE.WebGLRenderer({

        antialias:
            true,

        powerPreference:
            "high-performance"

    });


renderer.setPixelRatio(

    Math.min(
        window.devicePixelRatio,
        2
    )

);


renderer.setSize(

    window.innerWidth,

    window.innerHeight

);


renderer.outputColorSpace =
    THREE.SRGBColorSpace;


renderer.toneMapping =
    THREE.ACESFilmicToneMapping;


renderer.toneMappingExposure =
    1.05;


container.appendChild(
    renderer.domElement
);


/* ============================================================
   TEXTURE LOADER
   ============================================================ */

const textureLoader =
    new THREE.TextureLoader();


function loadTexture(data) {

    if (
        !data ||
        data.length < 20
    ) {

        return null;

    }


    try {

        const texture =
            textureLoader.load(
                data
            );


        texture.colorSpace =
            THREE.SRGBColorSpace;


        return texture;

    }
    catch (error) {

        return null;

    }

}


/* ============================================================
   STARFIELD
   ============================================================ */

const starTexture =
    loadTexture(
        starfieldTextureData
    );


if (starTexture) {

    starTexture.mapping =
        THREE.EquirectangularReflectionMapping;

    scene.background =
        starTexture;

}
else {

    scene.background =
        new THREE.Color(
            0x000006
        );

}


/* ============================================================
   LIGHTING
   ============================================================ */

const ambientLight =
    new THREE.AmbientLight(

        0x667799,

        0.38

    );


scene.add(
    ambientLight
);


const sunLight =
    new THREE.DirectionalLight(

        0xffffff,

        2.6

    );


sunLight.position.set(

    5,

    3,

    5

);


scene.add(
    sunLight
);


/* ============================================================
   EARTH GROUP
   ============================================================ */

const earthGroup =
    new THREE.Group();


scene.add(
    earthGroup
);


/* ============================================================
   EARTH
   ============================================================ */

const earthGeometry =
    new THREE.SphereGeometry(

        2.05,

        96,

        96

    );


const earthTexture =
    loadTexture(
        earthTextureData
    );


let earthMaterial;


if (earthTexture) {

    earthMaterial =
        new THREE.MeshStandardMaterial({

            map:
                earthTexture,

            roughness:
                0.78,

            metalness:
                0.0

        });

}
else {

    earthMaterial =
        new THREE.MeshStandardMaterial({

            color:
                0x2b6cff,

            roughness:
                0.8

        });

}


const earth =
    new THREE.Mesh(

        earthGeometry,

        earthMaterial

    );


earth.position.set(

    0,

    0,

    0

);


earthGroup.add(
    earth
);


/* ============================================================
   EARTH ATMOSPHERE
   ============================================================ */

const atmosphereGeometry =
    new THREE.SphereGeometry(

        2.10,

        64,

        64

    );


const atmosphereMaterial =
    new THREE.MeshBasicMaterial({

        color:
            0x4d9dff,

        transparent:
            true,

        opacity:
            0.055,

        side:
            THREE.BackSide

    });


const atmosphere =
    new THREE.Mesh(

        atmosphereGeometry,

        atmosphereMaterial

    );


earthGroup.add(
    atmosphere
);


/* ============================================================
   MOON ORBIT
   ============================================================ */

const moonOrbit =
    new THREE.Group();


earthGroup.add(
    moonOrbit
);


/* ============================================================
   MOON
   ============================================================ */

const moonGeometry =
    new THREE.SphereGeometry(

        0.55,

        64,

        64

    );


const moonTexture =
    loadTexture(
        moonTextureData
    );


let moonMaterial;


if (moonTexture) {

    moonMaterial =
        new THREE.MeshStandardMaterial({

            map:
                moonTexture,

            roughness:
                0.95,

            metalness:
                0

        });

}
else {

    moonMaterial =
        new THREE.MeshStandardMaterial({

            color:
                0xaaa9a5,

            roughness:
                1

        });

}


const moon =
    new THREE.Mesh(

        moonGeometry,

        moonMaterial

    );


moon.position.set(

    3.25,

    0.25,

    0

);


moonOrbit.add(
    moon
);


/* ============================================================
   MOON LIGHT
   ============================================================ */

const moonLight =
    new THREE.PointLight(

        0x9bbdff,

        0.18,

        15

    );


moonLight.position.set(

    3,

    2,

    2

);


scene.add(
    moonLight
);


/* ============================================================
   INITIAL EARTH ROTATION
   ============================================================ */

earth.rotation.y =
    -0.5;


/* ============================================================
   CAMERA CONTROL
   ============================================================ */

let distance =
    7.2;


let angleX =
    0;


let angleY =
    0.12;


let targetX =
    0;


let targetY =
    0;


let isDragging =
    false;


let lastX =
    0;


let lastY =
    0;


/* ============================================================
   POINTER DOWN
   ============================================================ */

renderer.domElement.addEventListener(

    "pointerdown",

    function(event) {

        isDragging =
            true;


        lastX =
            event.clientX;


        lastY =
            event.clientY;

    }

);


/* ============================================================
   POINTER MOVE
   ============================================================ */

renderer.domElement.addEventListener(

    "pointermove",

    function(event) {

        if (!isDragging) {

            return;

        }


        const dx =
            event.clientX -
            lastX;


        const dy =
            event.clientY -
            lastY;


        angleX -=
            dx * 0.004;


        angleY -=
            dy * 0.004;


        angleY =
            Math.max(

                -1.2,

                Math.min(
                    1.2,
                    angleY
                )

            );


        lastX =
            event.clientX;


        lastY =
            event.clientY;

    }

);


/* ============================================================
   POINTER UP
   ============================================================ */

window.addEventListener(

    "pointerup",

    function() {

        isDragging =
            false;

    }

);


/* ============================================================
   WHEEL ZOOM
   ============================================================ */

renderer.domElement.addEventListener(

    "wheel",

    function(event) {

        distance +=
            event.deltaY *
            0.005;


        distance =
            Math.max(

                4.0,

                Math.min(
                    14,
                    distance
                )

            );

    },

    {
        passive: true
    }

);


/* ============================================================
   TOUCH ZOOM
   ============================================================ */

let touchStartDistance =
    null;


renderer.domElement.addEventListener(

    "touchstart",

    function(event) {

        if (
            event.touches.length === 2
        ) {

            const dx =
                event.touches[0].clientX -
                event.touches[1].clientX;


            const dy =
                event.touches[0].clientY -
                event.touches[1].clientY;


            touchStartDistance =
                Math.sqrt(

                    dx * dx +
                    dy * dy

                );

        }

    },

    {
        passive: true
    }

);


/* ============================================================
   TOUCH MOVE
   ============================================================ */

renderer.domElement.addEventListener(

    "touchmove",

    function(event) {

        if (

            event.touches.length === 2 &&

            touchStartDistance !== null

        ) {

            const dx =
                event.touches[0].clientX -
                event.touches[1].clientX;


            const dy =
                event.touches[0].clientY -
                event.touches[1].clientY;


            const currentDistance =
                Math.sqrt(

                    dx * dx +
                    dy * dy

                );


            const difference =
                currentDistance -
                touchStartDistance;


            distance -=
                difference *
                0.008;


            distance =
                Math.max(

                    4,

                    Math.min(
                        14,
                        distance
                    )

                );


            touchStartDistance =
                currentDistance;

        }

    },

    {
        passive: true
    }

);


/* ============================================================
   TOUCH END
   ============================================================ */

renderer.domElement.addEventListener(

    "touchend",

    function() {

        touchStartDistance =
            null;

    }

);


/* ============================================================
   ANIMATION CLOCK
   ============================================================ */

const clock =
    new THREE.Clock();


/* ============================================================
   ANIMATION
   ============================================================ */

function animate() {

    requestAnimationFrame(
        animate
    );


    const delta =
        clock.getDelta();


    /* --------------------------------------------------------
       EARTH ROTATION
       -------------------------------------------------------- */

    earth.rotation.y +=
        0.035 *
        delta;


    /* --------------------------------------------------------
       MOON ORBIT
       -------------------------------------------------------- */

    moonOrbit.rotation.y +=
        0.18 *
        delta;


    /* --------------------------------------------------------
       MOON ROTATION
       -------------------------------------------------------- */

    moon.rotation.y +=
        0.015;


    /* --------------------------------------------------------
       CAMERA POSITION
       -------------------------------------------------------- */

    const horizontal =
        Math.cos(
            angleY
        ) *
        distance;


    const vertical =
        Math.sin(
            angleY
        ) *
        distance;


    const desiredX =
        Math.sin(
            angleX
        ) *
        horizontal;


    const desiredZ =
        Math.cos(
            angleX
        ) *
        horizontal;


    camera.position.x +=

        (
            desiredX -
            camera.position.x
        ) *
        0.06;


    camera.position.y +=

        (
            vertical -
            camera.position.y
        ) *
        0.06;


    camera.position.z +=

        (
            desiredZ -
            camera.position.z
        ) *
        0.06;


    camera.lookAt(

        targetX,

        targetY,

        0

    );


    /* --------------------------------------------------------
       RENDER
       -------------------------------------------------------- */

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

    function() {

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

animate();


</script>

</body>

</html>
"""


    # ========================================================
    # INSERT ASSETS
    # ========================================================

    html = (

        html

        .replace(
            "__EARTH__",
            EARTH
        )

        .replace(
            "__MOON__",
            MOON
        )

        .replace(
            "__STARS__",
            STARS
        )

    )


    # ========================================================
    # DISPLAY SCENE
    # ========================================================

    components.html(

        html,

        height=900,

        scrolling=False

    )