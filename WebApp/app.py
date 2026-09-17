import streamlit as st
import importlib.util
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CosmoScope",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# GLOBAL STREAMLIT STYLE
# ============================================================

st.markdown(
    """
    <style>

    header {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    footer {
        display: none !important;
    }

    #MainMenu {
        display: none !important;
    }

    html,
    body,
    [data-testid="stApp"],
    [data-testid="stAppViewContainer"] {
        margin: 0 !important;
        padding: 0 !important;
        background: #000000 !important;
    }

    .stApp {
        background: #000000 !important;
    }

    .main {
        padding: 0 !important;
        margin: 0 !important;
    }

    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        padding: 0 !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }

    iframe {
        border: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PROJECT PATHS
# ============================================================

WEBAPP_DIR = Path(__file__).resolve().parent
SCENCES_DIR = WEBAPP_DIR / "scences"


if not SCENCES_DIR.exists():

    st.error(
        f"""
        Scene folder not found.

        Expected:
        {SCENCES_DIR}
        """
    )

    st.stop()


# ============================================================
# SESSION STATE
# ============================================================

if "scene" not in st.session_state:
    st.session_state.scene = 1


# ============================================================
# READ URL SCENE
# ============================================================

scene_parameter = st.query_params.get(
    "scene",
    "1"
)

try:

    requested_scene = int(
        scene_parameter
    )

except (
    ValueError,
    TypeError
):

    requested_scene = 1


if requested_scene in (
    1,
    2,
    3,
    4,
    5
):

    st.session_state.scene = (
        requested_scene
    )

else:

    st.session_state.scene = 1

    st.query_params["scene"] = "1"


# ============================================================
# LOAD SCENE
# ============================================================

def load_scene(
    filename,
    module_name
):

    scene_path = (
        SCENCES_DIR /
        filename
    )

    if not scene_path.exists():

        st.error(
            f"""
            Scene file not found.

            Expected:
            {scene_path}
            """
        )

        st.stop()


    spec = (
        importlib.util
        .spec_from_file_location(
            module_name,
            scene_path
        )
    )


    if spec is None:

        st.error(
            f"Could not load {filename}"
        )

        st.stop()


    if spec.loader is None:

        st.error(
            f"Could not create loader for {filename}"
        )

        st.stop()


    module = (
        importlib.util
        .module_from_spec(spec)
    )


    try:

        spec.loader.exec_module(
            module
        )

    except Exception as e:

        st.error(
            f"""
            Error loading {filename}

            {type(e).__name__}: {e}
            """
        )

        st.stop()


    return module


# ============================================================
# CHANGE SCENE
# ============================================================

def change_scene(
    scene_number
):

    if scene_number not in (
        1,
        2,
        3,
        4,
        5
    ):

        scene_number = 1


    st.session_state.scene = (
        scene_number
    )

    st.query_params["scene"] = (
        str(scene_number)
    )

    st.rerun()


# ============================================================
# SCENE 1
# ============================================================

if st.session_state.scene == 1:

    scene1 = load_scene(
        "scence1.py",
        "cosmoscope_scence1"
    )


    if hasattr(
        scene1,
        "show_scene1"
    ):

        scene1.show_scene1()

    elif hasattr(
        scene1,
        "show_scence1"
    ):

        scene1.show_scence1()

    else:

        st.error(
            "Scene 1 function not found."
        )

        st.stop()


    st.markdown(
        """
        <style>

        div.stButton > button {

            position: fixed;

            right: 32px;
            bottom: 28px;

            z-index: 9999;

            width: 190px;

            border:
                1px solid
                rgba(160,215,255,.45);

            border-radius: 5px;

            background:
                rgba(4,14,25,.92);

            color:
                rgba(235,247,255,.96);

            font-size: 10px;

            letter-spacing: 2px;

            font-weight: 600;

        }

        div.stButton > button:hover {

            border-color:
                rgba(205,235,255,.9);

            background:
                rgba(20,70,105,.9);

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "LEAVE EARTH  →",
        key="leave_earth_button"
    ):

        change_scene(2)


# ============================================================
# SCENE 2
# ============================================================

elif st.session_state.scene == 2:

    scene2 = load_scene(
        "scence2.py",
        "cosmoscope_scence2"
    )


    if hasattr(
        scene2,
        "show_scene2"
    ):

        scene2.show_scene2()

    elif hasattr(
        scene2,
        "show_scence2"
    ):

        scene2.show_scence2()

    else:

        st.error(
            "Scene 2 function not found."
        )

        st.stop()


    st.markdown(
        """
        <style>

        div.stButton > button {

            position: fixed;

            right: 32px;
            bottom: 28px;

            z-index: 9999;

            width: 180px;

            border:
                1px solid
                rgba(160,215,255,.45);

            border-radius: 5px;

            background:
                rgba(4,14,25,.92);

            color:
                rgba(235,247,255,.96);

            font-size: 10px;

            letter-spacing: 2px;

            font-weight: 600;

        }

        div.stButton > button:hover {

            border-color:
                rgba(205,235,255,.9);

            background:
                rgba(20,70,105,.9);

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "GO BEYOND  →",
        key="go_beyond_button"
    ):

        change_scene(3)


# ============================================================
# SCENE 3
# ============================================================

elif st.session_state.scene == 3:

    scene3 = load_scene(
        "scence3.py",
        "cosmoscope_scence3"
    )


    if hasattr(
        scene3,
        "show_scene3"
    ):

        scene3.show_scene3()

    elif hasattr(
        scene3,
        "show_scence3"
    ):

        scene3.show_scence3()

    else:

        st.error(
            "Scene 3 function not found."
        )

        st.stop()


    # ========================================================
    # SCENE 3 → SCENE 4 BUTTON
    # ========================================================

    st.markdown(
        """
        <style>

        div.stButton > button {

            position: fixed;

            right: 32px;
            bottom: 28px;

            z-index: 999999;

            width: 205px;

            height: 42px;

            border:
                1px solid
                rgba(160,215,255,.45);

            border-radius: 5px;

            background:
                rgba(4,14,25,.94);

            color:
                rgba(235,247,255,.96);

            font-size: 10px;

            letter-spacing: 2px;

            font-weight: 600;

            box-shadow:
                0 0 18px
                rgba(70,150,220,.08);

        }

        div.stButton > button:hover {

            border-color:
                rgba(205,235,255,.9);

            background:
                rgba(20,70,105,.94);

            box-shadow:
                0 0 24px
                rgba(90,180,255,.18);

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "LEAVE MILKY WAY  →",
        key="leave_milky_way_button"
    ):

        change_scene(4)


# ============================================================
# SCENE 4
# ============================================================

elif st.session_state.scene == 4:

    scene4 = load_scene(
        "scence4.py",
        "cosmoscope_scence4"
    )


    if hasattr(
        scene4,
        "show_scene4"
    ):

        scene4.show_scene4()

    elif hasattr(
        scene4,
        "show_scence4"
    ):

        scene4.show_scence4()

    else:

        st.error(
            "Scene 4 function not found."
        )

        st.stop()


    # ========================================================
    # SCENE 4 → SCENE 5 BUTTON
    # ========================================================

    st.markdown(
        """
        <style>

        div.stButton > button {

            position: fixed;

            right: 32px;
            bottom: 28px;

            z-index: 999999;

            width: 245px;

            height: 42px;

            border:
                1px solid
                rgba(160,215,255,.45);

            border-radius: 5px;

            background:
                rgba(4,14,25,.94);

            color:
                rgba(235,247,255,.96);

            font-size: 10px;

            letter-spacing: 2px;

            font-weight: 600;

            box-shadow:
                0 0 18px
                rgba(70,150,220,.08);

        }

        div.stButton > button:hover {

            border-color:
                rgba(205,235,255,.9);

            background:
                rgba(20,70,105,.94);

            box-shadow:
                0 0 24px
                rgba(90,180,255,.18);

        }

        </style>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "ENTER EXOPLANET ANALYSIS  →",
        key="enter_exoplanet_analysis_button"
    ):

        change_scene(5)


# ============================================================
# SCENE 5 — FINAL DISCOVERY
# ============================================================

elif st.session_state.scene == 5:

    scene5 = load_scene(
        "scence5.py",
        "cosmoscope_scence5"
    )


    if hasattr(
        scene5,
        "show_scene5"
    ):

        scene5.show_scene5()

    elif hasattr(
        scene5,
        "show_scence5"
    ):

        scene5.show_scence5()

    else:

        st.error(
            "Scene 5 function not found."
        )

        st.stop()


# ============================================================
# FALLBACK
# ============================================================

else:

    change_scene(1)