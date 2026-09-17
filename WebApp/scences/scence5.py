import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import json
import math
import base64


# ============================================================
# COSMOSCOPE - SCENE 5
# NASA EXOPLANET DATA -> DBSCAN -> UMAP -> LOF -> DISCOVERY
# Final scientific analysis scene
# ============================================================


def show_scene5():
    BASE_DIR = Path(__file__).resolve().parent.parent

    # --------------------------------------------------------
    # Locate the exported NASA dataset.
    # The project layout is: CosmoScope/Results/<file>.csv
    # --------------------------------------------------------
    results_dir = BASE_DIR / "Results"
    data_path = results_dir / "exoplanet_powerbi_clean.csv"

    # Also accept a lowercase results folder for Windows/Linux portability.
    if not data_path.exists():
        data_path = BASE_DIR / "results" / "exoplanet_powerbi_clean.csv"

    # If the file was placed elsewhere inside CosmoScope, find it without
    # changing the expected Results location.
    if not data_path.exists():
        matches = list(BASE_DIR.rglob("exoplanet_powerbi_clean.csv"))
        data_path = matches[0] if matches else None

    # Optional fallback for the older master filename.
    if data_path is None:
        master_candidates = [
            BASE_DIR / "Results" / "exoplanet_powerbi_master.csv",
            BASE_DIR / "results" / "exoplanet_powerbi_master.csv",
            BASE_DIR / "assets" / "exoplanet_powerbi_master.csv",
            BASE_DIR / "exoplanet_powerbi_master.csv",
        ]
        data_path = next(
            (p for p in master_candidates if p.exists()),
            None
        )

    if data_path is None:
        st.error(
            "Scene 5 data file not found. Put exoplanet_powerbi_clean.csv "
            "inside CosmoScope/Results/ or CosmoScope/assets/."
        )
        return

    # --------------------------------------------------------
    # Load data.
    # --------------------------------------------------------
    try:
        import pandas as pd
        import numpy as np
    except Exception as exc:
        st.error("Scene 5 requires pandas and numpy: " + str(exc))
        return

    try:
        df = pd.read_csv(data_path)
    except Exception as exc:
        st.error("Could not read the exoplanet dataset: " + str(exc))
        return

    # Prefer the exact nine-feature matrix when a master NASA export exists.
    exact_features = [
        "pl_rade",
        "pl_masse",
        "pl_dens",
        "pl_orbper",
        "pl_orbsmax",
        "pl_eqt",
        "st_teff",
        "st_mass",
        "st_rad",
    ]

    # The clean Power BI export does not contain pl_dens/pl_orbsmax.
    # Reconstruct them when possible so the same nine-feature structure can
    # still be used for the UMAP exploration.
    work = df.copy()

    if "pl_masse" not in work.columns and "pl_bmasse" in work.columns:
        work["pl_masse"] = pd.to_numeric(
            work["pl_bmasse"],
            errors="coerce"
        )

    if "pl_dens" not in work.columns:
        radius = pd.to_numeric(work.get("pl_rade"), errors="coerce")
        mass = pd.to_numeric(work.get("pl_masse"), errors="coerce")
        with np.errstate(divide="ignore", invalid="ignore"):
            work["pl_dens"] = mass / (radius ** 3)

    if "pl_orbsmax" not in work.columns:
        period = pd.to_numeric(work.get("pl_orbper"), errors="coerce")
        star_mass = pd.to_numeric(work.get("st_mass"), errors="coerce")
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            work["pl_orbsmax"] = (
                ((period / 365.25) ** 2) * star_mass
            ) ** (1.0 / 3.0)

    available_features = [
        col for col in exact_features
        if col in work.columns
    ]

    if len(available_features) != 9:
        st.error(
            "Scene 5 could not assemble the nine numerical features used "
            "by the Colab analysis."
        )
        return

    numeric = work[available_features].apply(
        pd.to_numeric,
        errors="coerce"
    )
    numeric = numeric.replace([np.inf, -np.inf], np.nan)
    numeric = numeric.fillna(numeric.median())

    # --------------------------------------------------------
    # Use stored DBSCAN/LOF results from the user's export.
    # --------------------------------------------------------
    if "DBSCAN_Cluster" not in work.columns:
        st.error("DBSCAN_Cluster is missing from the exported dataset.")
        return

    if "LOF_Label" not in work.columns:
        st.error("LOF_Label is missing from the exported dataset.")
        return

    clusters = pd.to_numeric(
        work["DBSCAN_Cluster"],
        errors="coerce"
    ).fillna(-1).astype(int).to_numpy()

    lof_labels = pd.to_numeric(
        work["LOF_Label"],
        errors="coerce"
    ).fillna(1).astype(int).to_numpy()

    if "LOF_Score" in work.columns:
        lof_scores = pd.to_numeric(
            work["LOF_Score"],
            errors="coerce"
        ).fillna(1.0).to_numpy()
    else:
        lof_scores = np.ones(len(work), dtype=float)

    names = (
        work["pl_name"].astype(str)
        if "pl_name" in work.columns
        else pd.Series(
            ["Unknown world " + str(i + 1) for i in range(len(work))]
        )
    )

    # --------------------------------------------------------
    # UMAP calculation.
    # --------------------------------------------------------
    umap_status = "UMAP"
    X_scaled = None
    umap_xy = None

    try:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(numeric)
    except Exception as exc:
        st.error("Could not scale the exoplanet features: " + str(exc))
        return

    try:
        import umap.umap_ as umap

        reducer = umap.UMAP(
            n_components=2,
            n_neighbors=15,
            min_dist=0.1,
            random_state=42,
        )
        umap_xy = reducer.fit_transform(X_scaled)
    except Exception:
        # Keep the scene usable if umap-learn is not installed.
        # This is explicitly labelled in the interface as a fallback.
        try:
            from sklearn.decomposition import PCA
            umap_xy = PCA(
                n_components=2,
                random_state=42,
            ).fit_transform(X_scaled)
            umap_status = "2D FALLBACK"
        except Exception as exc:
            st.error("Could not create the 2D analysis view: " + str(exc))
            return

    # --------------------------------------------------------
    # Derived summaries from the user's stored results.
    # --------------------------------------------------------
    total = len(work)
    cluster_values = sorted(set(int(x) for x in clusters))
    real_clusters = [x for x in cluster_values if x != -1]
    cluster_count = len(real_clusters)
    noise_count = int(np.sum(clusters == -1))
    normal_count = int(np.sum(lof_labels == 1))
    outlier_count = int(np.sum(lof_labels == -1))

    # Top 20 from the stored LOF results.
    order = np.argsort(-lof_scores)
    top_idx = [int(i) for i in order if lof_labels[int(i)] == -1][:20]

    top_rows = []
    for i in top_idx:
        row = work.iloc[i]
        top_rows.append({
            "name": str(names.iloc[i]),
            "cluster": int(clusters[i]),
            "score": float(lof_scores[i]),
            "radius": float(pd.to_numeric(row.get("pl_rade"), errors="coerce")) if pd.notna(pd.to_numeric(row.get("pl_rade"), errors="coerce")) else None,
            "mass": float(pd.to_numeric(row.get("pl_masse", row.get("pl_bmasse")), errors="coerce")) if pd.notna(pd.to_numeric(row.get("pl_masse", row.get("pl_bmasse")), errors="coerce")) else None,
            "temperature": float(pd.to_numeric(row.get("pl_eqt"), errors="coerce")) if pd.notna(pd.to_numeric(row.get("pl_eqt"), errors="coerce")) else None,
            "period": float(pd.to_numeric(row.get("pl_orbper"), errors="coerce")) if pd.notna(pd.to_numeric(row.get("pl_orbper"), errors="coerce")) else None,
            "distance": float(pd.to_numeric(row.get("sy_dist"), errors="coerce")) if pd.notna(pd.to_numeric(row.get("sy_dist"), errors="coerce")) else None,
        })

    # --------------------------------------------------------
    # UMAP points sent to the self-contained browser UI.
    # --------------------------------------------------------
    points = []
    for i in range(total):
        row = work.iloc[i]
        def safe_num(column, fallback=None):
            value = pd.to_numeric(row.get(column, fallback), errors="coerce")
            return float(value) if pd.notna(value) else None
        points.append({
            "x": round(float(umap_xy[i, 0]), 5),
            "y": round(float(umap_xy[i, 1]), 5),
            "cluster": int(clusters[i]),
            "outlier": int(lof_labels[i]) == -1,
            "name": str(names.iloc[i]),
            "score": round(float(lof_scores[i]), 5),
            "method": str(row.get("discoverymethod", "NASA ARCHIVE")),
            "year": safe_num("disc_year"),
            "radius": safe_num("pl_rade"),
            "mass": safe_num("pl_bmasse", row.get("pl_masse")),
            "temperature": safe_num("pl_eqt"),
        })

    # Cluster counts.
    cluster_counts = {}
    for c in cluster_values:
        cluster_counts[str(c)] = int(np.sum(clusters == c))

    # Cluster/LOF combined counts.
    cluster_outliers = {}
    for c in cluster_values:
        mask = clusters == c
        cluster_outliers[str(c)] = int(np.sum(mask & (lof_labels == -1)))

    # Browser-searchable rows used by the Explore Planet panel and data table.
    rows = []
    for i in range(total):
        row = work.iloc[i]
        def row_num(column, fallback=None):
            value = pd.to_numeric(row.get(column, fallback), errors="coerce")
            return float(value) if pd.notna(value) else None
        rows.append({
            "name": str(names.iloc[i]),
            "method": str(row.get("discoverymethod", "NASA ARCHIVE")),
            "year": row_num("disc_year"),
            "radius": row_num("pl_rade"),
            "mass": row_num("pl_bmasse", row.get("pl_masse")),
            "temperature": row_num("pl_eqt"),
            "period": row_num("pl_orbper"),
            "distance": row_num("sy_dist"),
            "cluster": int(clusters[i]),
            "outlier": int(lof_labels[i]) == -1,
            "lof": round(float(lof_scores[i]), 5),
            "x": round(float(umap_xy[i, 0]), 5),
            "y": round(float(umap_xy[i, 1]), 5),
        })

    payload = {
        "total": total,
        "clusters": cluster_count,
        "noise": noise_count,
        "normal": normal_count,
        "outliers": outlier_count,
        "clusterCounts": cluster_counts,
        "clusterOutliers": cluster_outliers,
        "umapStatus": umap_status,
        "points": points,
        "rows": rows,
        "top": top_rows,
        "dataFile": data_path.name,
        "features": available_features,
        "dbscan": {
            "eps": 0.5,
            "minSamples": 10,
        },
        "umap": {
            "neighbors": 15,
            "minDist": 0.1,
            "seed": 42,
        },
        "lof": {
            "neighbors": 20,
            "contamination": "0.05 / stored result",
        },
        "evaluation": {
            "silhouette": 0.1427,
            "davies": 1.2562,
            "calinski": 366.8790,
        },
    }

    data_json = json.dumps(
        payload,
        separators=(",", ":"),
        allow_nan=False,
    )

    # --------------------------------------------------------
    # Local Solar System reference gallery.
    # Images are loaded only from the project's assets folder.
    # --------------------------------------------------------
    def load_asset(name):
        path = BASE_DIR / "assets" / name
        if not path.exists():
            return ""
        try:
            raw = path.read_bytes()
            ext = path.suffix.lower()
            mime = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".webp": "image/webp",
            }.get(ext, "application/octet-stream")
            return "data:" + mime + ";base64," + base64.b64encode(raw).decode("ascii")
        except Exception:
            return ""

    solar_objects = [
        {
            "name": "Mercury", "type": "TERRESTRIAL PLANET", "image": load_asset("mercury.jpg"),
            "distance": "0.387 AU", "year": "88 Earth days", "moons": "0",
            "description": "The smallest planet and the world closest to the Sun. Its surface is heavily cratered and its temperature changes dramatically between day and night.",
            "moonsInfo": "Mercury has no natural moons.", "moonCards": []
        },
        {
            "name": "Venus", "type": "TERRESTRIAL PLANET", "image": load_asset("venus.jpg"),
            "distance": "0.723 AU", "year": "224.7 Earth days", "moons": "0",
            "description": "A rocky world wrapped in a thick carbon-dioxide atmosphere. Venus is the hottest planet in our solar system.",
            "moonsInfo": "Venus has no natural moons.", "moonCards": []
        },
        {
            "name": "Earth", "type": "TERRESTRIAL PLANET", "image": load_asset("earth.jpg"),
            "distance": "1.000 AU", "year": "365.25 Earth days", "moons": "1",
            "description": "Our home world, with extensive liquid water at its surface and the only life currently known to science.",
            "moonsInfo": "Earth has one natural moon: the Moon.",
            "moonCards": [{"name":"Moon","image":load_asset("moon_texture.jpg"),"fact":"Earth's natural satellite; its surface preserves a record of impacts from early solar-system history."}]
        },
        {
            "name": "Mars", "type": "TERRESTRIAL PLANET", "image": load_asset("mars.jpg"),
            "distance": "1.524 AU", "year": "687 Earth days", "moons": "2",
            "description": "The Red Planet, a cold rocky world with polar ice, ancient valleys and a thin atmosphere.",
            "moonsInfo": "Mars has two small moons: Phobos and Deimos. No Phobos/Deimos image is currently present in your assets folder.",
            "moonCards": []
        },
        {
            "name": "Jupiter", "type": "GAS GIANT", "image": load_asset("jupiter.jpg"),
            "distance": "5.203 AU", "year": "11.86 Earth years", "moons": "95+",
            "description": "The largest planet, dominated by hydrogen and helium and famous for its Great Red Spot and powerful storms.",
            "moonsInfo": "Jupiter has many moons. The four large Galilean moons are Io, Europa, Ganymede and Callisto.",
            "moonCards": [
                {"name":"Io","image":load_asset("io.jpg"),"fact":"Volcanically active moon with a surface continually reshaped by eruptions."},
                {"name":"Europa","image":load_asset("europa.jpg"),"fact":"Icy moon with strong evidence for a subsurface ocean beneath its frozen crust."},
                {"name":"Ganymede","image":load_asset("ganymede.jpg"),"fact":"The largest moon in the solar system and the only moon known to have its own magnetic field."},
                {"name":"Callisto","image":load_asset("callisto.jpg"),"fact":"Heavily cratered outer Galilean moon with an ancient surface."}
            ]
        },
        {
            "name": "Saturn", "type": "GAS GIANT", "image": load_asset("saturn.jpg"),
            "distance": "9.537 AU", "year": "29.45 Earth years", "moons": "274 confirmed*",
            "description": "A giant planet surrounded by an extensive ring system made of countless pieces of ice and rock.",
            "moonsInfo": "Saturn has many moons, including Titan, Enceladus, Rhea and Iapetus.", "moonCards": [
                {"name":"Titan","image":load_asset("saturn_moon_titan.jpg"),"fact":"Saturn's largest moon and the only moon known to have a thick atmosphere; it has lakes and seas of liquid hydrocarbons."},
                {"name":"Enceladus","image":load_asset("saturn_moon_enceladus.jpg"),"fact":"An icy moon with a global subsurface ocean and water-rich plumes erupting from fractures near its south pole."},
                {"name":"Rhea","image":load_asset("saturn_moon_rhea.jpg"),"fact":"A heavily cratered icy moon with a bright surface and a tenuous environment."},
                {"name":"Iapetus","image":"","fact":"A two-toned moon famous for its dramatic light and dark hemispheres and a prominent equatorial ridge."}
            ]
        },
        {
            "name": "Uranus", "type": "ICE GIANT", "image": load_asset("uranus.jpg"),
            "distance": "19.19 AU", "year": "84 Earth years", "moons": "28 known",
            "description": "A pale blue ice giant rotating on its side relative to the plane of its orbit, with a faint ring system.",
            "moonsInfo": "Uranus has many moons, including Titania, Oberon, Ariel, Umbriel and Miranda.", "moonCards": [
                {"name":"Titania","image":load_asset("uranus_moon_titania.jpg"),"fact":"The largest moon of Uranus, with a fractured icy surface."},
                {"name":"Oberon","image":load_asset("uranus_moon_oberon.jpg"),"fact":"The outermost of Uranus's five major moons, heavily cratered and ancient."},
                {"name":"Ariel","image":load_asset("uranus_moon_ariel.jpg"),"fact":"A bright icy moon with valleys, faults and evidence of past geological activity."},
                {"name":"Umbriel","image":load_asset("uranus_moon_umbriel.jpg"),"fact":"A dark, heavily cratered Uranian moon with an old surface."},
                {"name":"Miranda","image":load_asset("uranus_moon_miranda.jpg"),"fact":"A small Uranian moon with dramatic cliffs, grooves and patchwork terrains."}
            ]
        },
        {
            "name": "Neptune", "type": "ICE GIANT", "image": load_asset("neptune.jpg"),
            "distance": "30.07 AU", "year": "164.8 Earth years", "moons": "16 known",
            "description": "The most distant major planet, an ice giant with fast winds, storms and a deep blue appearance.",
            "moonsInfo": "Neptune has 16 known moons; Triton is the largest.", "moonCards": [
                {"name":"Triton","image":load_asset("neptune_moon_triton.jpg"),"fact":"Neptune's largest moon, likely captured from the Kuiper Belt, with nitrogen frost and active geyser-like plumes."}
            ]
        },
        {
            "name": "Pluto", "type": "DWARF PLANET", "image": load_asset("pluto.jpg"),
            "distance": "39.5 AU average", "year": "248 Earth years", "moons": "5",
            "description": "A dwarf planet in the Kuiper Belt. Its largest moon, Charon, is unusually large compared with Pluto.",
            "moonsInfo": "Pluto has five known moons: Charon, Styx, Nix, Kerberos and Hydra.", "moonCards": [
                {"name":"Charon","image":load_asset("pluto_moon_charon.jpg"),"fact":"Pluto's largest moon, so large relative to Pluto that the pair is often described as a binary dwarf-planet system."},
                {"name":"Styx","image":load_asset("pluto_moon_styx.jpg"),"fact":"A small irregular moon orbiting Pluto beyond Charon."},
                {"name":"Nix","image":load_asset("pluto_moon_nix.jpg"),"fact":"A small, irregular moon discovered in images from the Hubble Space Telescope."},
                {"name":"Kerberos","image":load_asset("pluto_moon_kerberos.jpg"),"fact":"A small irregular moon located between Nix and Hydra."},
                {"name":"Hydra","image":load_asset("pluto_moon_hydra.jpg"),"fact":"The outermost known moon of Pluto, irregular in shape and highly reflective."}
            ]
        }
    ]
    exoplanet_image = load_asset("exoplanet.jpg")
    payload["exoplanetImage"] = exoplanet_image
    data_json = json.dumps(payload, separators=(",", ":"), allow_nan=False)
    solar_json = json.dumps(solar_objects, separators=(",", ":"), ensure_ascii=False)

    # --------------------------------------------------------
    # Render HTML. Raw string + replace: no f-string braces.
    # --------------------------------------------------------
    html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{box-sizing:border-box}html,body{margin:0;padding:0;width:100%;min-height:100%;overflow:auto;background:#050a12;color:#eef6ff;font-family:Segoe UI,Arial,sans-serif}button,input{font:inherit}button{cursor:pointer}
#app{min-height:100vh;height:auto;overflow:visible;background:radial-gradient(circle at 80% 10%,rgba(78,130,180,.14),transparent 30%),linear-gradient(145deg,#040912,#07111d 55%,#04070d)}
#top{height:82px;display:flex;align-items:center;justify-content:space-between;padding:0 28px;border-bottom:1px solid rgba(170,205,235,.16);background:rgba(3,8,15,.88)}
.brandMain{font-size:26px;font-weight:800;letter-spacing:4px}.brandSub{font-size:12px;font-weight:600;letter-spacing:2px;color:#9eb5ca;margin-top:5px}.status{font-size:12px;font-weight:700;letter-spacing:1.5px;color:#b8cada}.dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#8fc6df;margin-right:9px}
#pipeline{height:74px;display:flex;align-items:center;gap:7px;padding:10px 24px;border-bottom:1px solid rgba(170,205,235,.13);overflow-x:auto;background:rgba(5,12,21,.82)}
.step{min-width:145px;cursor:pointer;height:50px;border:1px solid rgba(150,190,220,.16);border-radius:8px;padding:7px 11px;background:rgba(10,21,34,.7);transition:.2s}.step b{font-size:13px;letter-spacing:.8px}.step span{display:block;font-size:11px;color:#8fa7bb;margin-top:4px}.step.active{border-color:rgba(155,214,244,.7);background:rgba(25,62,88,.72)}.arrow{color:#7690a7;font-size:18px}
#layout{height:calc(100% - 156px);display:grid;grid-template-columns:210px 1fr;min-height:0}.side{border-right:1px solid rgba(170,205,235,.13);padding:20px 14px;background:rgba(4,10,17,.82);overflow:auto}.mission{font-size:11px;letter-spacing:2px;color:#86a0b7;font-weight:700;margin:0 8px 12px}.nav{width:100%;text-align:left;border:1px solid transparent;border-radius:7px;background:transparent;color:#aebfd0;padding:12px 11px;margin:3px 0;font-size:13px;font-weight:700;letter-spacing:.7px}.nav:hover{background:rgba(70,120,160,.12)}.nav.active{background:rgba(55,105,140,.2);border-color:rgba(150,205,235,.38);color:#f1f7fc}.nav small{display:block;font-size:10px;color:#758da2;margin-top:4px;font-weight:500;letter-spacing:.3px}.method{margin-top:24px;border-top:1px solid rgba(170,205,235,.14);padding-top:16px}.method div{display:flex;justify-content:space-between;font-size:11px;margin:10px 5px;color:#92a9bd}.method b{color:#d7e6f1}
#main{min-width:0;min-height:0;overflow:visible;position:relative}.view{display:none;min-height:calc(100vh - 156px);height:auto;overflow:visible;padding:30px 34px 70px}.view.active{display:block}.kicker{font-size:12px;font-weight:800;letter-spacing:2px;color:#8eacc2}.title{font-size:38px;font-weight:800;letter-spacing:1px;margin:7px 0 10px}.lead{font-size:17px;line-height:1.55;color:#b8c9d7;max-width:900px}.sectionHead{display:flex;justify-content:space-between;gap:20px;align-items:flex-end;margin-bottom:22px}.pill{border:1px solid rgba(155,205,235,.3);border-radius:999px;padding:8px 12px;font-size:11px;font-weight:700;color:#bcd1e0;white-space:nowrap}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:22px 0}.card{border:1px solid rgba(160,200,230,.16);background:rgba(10,23,37,.78);border-radius:10px;padding:18px}.card .label{font-size:11px;font-weight:800;letter-spacing:1.3px;color:#8fa9bd}.card .value{font-size:30px;font-weight:800;margin-top:7px}.card p{font-size:13px;line-height:1.45;color:#9eb2c4;margin:8px 0 0}.info{border-left:3px solid rgba(150,205,235,.65);background:rgba(18,35,52,.65);padding:16px 18px;border-radius:7px;font-size:15px;line-height:1.55;color:#c4d4e0}.info b{color:#f2f7fb}.dataGrid{display:grid;grid-template-columns:1fr 320px;gap:18px}.panel{border:1px solid rgba(160,200,230,.16);background:rgba(7,17,28,.82);border-radius:10px;padding:18px}.panel h3{font-size:18px;margin:0 0 9px}.panel p{font-size:14px;line-height:1.55;color:#9eb2c4}.search{width:100%;padding:11px 12px;background:#091522;border:1px solid rgba(160,200,230,.22);border-radius:7px;color:#eef6ff;outline:none}.tableWrap{margin-top:12px;overflow:auto;max-height:440px;border:1px solid rgba(160,200,230,.13);border-radius:8px}.dataTable{width:100%;border-collapse:collapse;min-width:760px}.dataTable th{position:sticky;top:0;background:#0b1928;color:#9fb5c7;font-size:11px;letter-spacing:1px;text-align:left;padding:11px;border-bottom:1px solid rgba(160,200,230,.16)}.dataTable td{padding:10px 11px;font-size:13px;border-bottom:1px solid rgba(160,200,230,.08);color:#d4e1eb}.dataTable tr:hover td{background:rgba(70,120,160,.08)}
.chartLayout{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:20px;height:calc(100% - 10px)}.chartPanel{position:relative;border:1px solid rgba(160,200,230,.16);background:rgba(5,14,24,.88);border-radius:10px;min-height:480px;overflow:hidden}.chartPanel canvas{width:100%;height:100%;display:block}.selectionDock{margin-top:18px;border-color:rgba(130,205,240,.22);background:linear-gradient(135deg,rgba(10,28,42,.96),rgba(5,13,21,.96));font-size:13px;line-height:1.55;color:#b8cbd7}.selectionDock #selectionDockBody{font-weight:700;color:#dbe9f1}.chartSelection{position:absolute;left:14px;bottom:14px;display:flex;align-items:center;gap:10px;width:min(360px,calc(100% - 28px));padding:8px;background:rgba(3,10,18,.9);border:1px solid rgba(160,210,235,.22);border-radius:8px;z-index:8}.chartSelection img{width:82px;height:82px;object-fit:cover;aspect-ratio:1/1;border-radius:8px;width:54px;height:54px;object-fit:cover;border-radius:6px;border:1px solid rgba(180,220,240,.25);flex:0 0 54px}.chartSelection b{display:block;font-size:13px}.chartSelection span{display:block;font-size:10px;line-height:1.35;color:#8ea7ba;margin-top:3px}.selectionDock{margin-top:18px;border-color:rgba(130,205,240,.22);background:linear-gradient(135deg,rgba(10,28,42,.96),rgba(5,13,21,.96));font-size:13px;line-height:1.55;color:#b8cbd7}.selectionDock #selectionDockBody{font-weight:700;color:#dbe9f1}.chartSelection{position:absolute;left:14px;bottom:14px;display:flex;align-items:center;gap:10px;width:min(360px,calc(100% - 28px));padding:8px;background:rgba(3,10,18,.9);border:1px solid rgba(160,210,235,.22);border-radius:8px;z-index:8}.chartSelection img{width:82px;height:82px;object-fit:cover;aspect-ratio:1/1;border-radius:8px;width:54px;height:54px;object-fit:cover;border-radius:6px;border:1px solid rgba(180,220,240,.25);flex:0 0 54px}.chartSelection b{display:block;font-size:13px}.chartSelection span{display:block;font-size:10px;line-height:1.35;color:#8ea7ba;margin-top:3px}.explainPanel{border:1px solid rgba(160,200,230,.16);background:rgba(8,19,31,.9);border-radius:10px;padding:22px;overflow:auto}.big{font-size:42px;font-weight:800;letter-spacing:1px;margin:7px 0 12px}.explainPanel h3{font-size:19px;margin:20px 0 8px}.explainPanel p{font-size:15px;line-height:1.6;color:#aabccc}.formula{padding:13px;border-radius:7px;background:rgba(45,82,108,.2);border:1px solid rgba(150,205,235,.18);font-size:14px;font-weight:700;line-height:1.5}.controls{display:flex;gap:7px;position:absolute;right:14px;top:14px}.control{border:1px solid rgba(155,205,235,.28);background:rgba(4,12,20,.9);color:#d8e7f2;border-radius:6px;padding:8px 10px;font-size:11px;font-weight:800}.control:hover{background:rgba(50,95,125,.45)}
.worldButton{width:100%;cursor:pointer;text-align:left}.dataRow{cursor:pointer}.dataRow:hover{background:rgba(55,105,135,.2)}.dataRow.selected{background:rgba(55,105,135,.3);outline:1px solid rgba(150,215,245,.35)}.worldGrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.world{border:1px solid rgba(160,200,230,.16);border-radius:10px;background:rgba(8,19,31,.86);padding:17px}.world h3{font-size:18px;margin:0 0 6px}.world .score{font-size:28px;font-weight:800}.world .why{font-size:13px;line-height:1.5;color:#a7baca;margin-top:8px}.tag{display:inline-block;margin-top:9px;padding:5px 8px;border-radius:5px;background:rgba(160,205,235,.09);font-size:10px;font-weight:800;letter-spacing:.8px;color:#abc3d4}
#discovery{max-width:1100px;margin:auto;padding:12px 0 40px}.final{border:1px solid rgba(160,205,235,.24);border-radius:12px;background:linear-gradient(145deg,rgba(13,31,48,.95),rgba(6,14,24,.94));padding:34px}.final h1{font-size:50px;margin:8px 0 14px}.final p{font-size:17px;line-height:1.65;color:#b6c8d6;max-width:900px}.journey{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-top:24px}.journey div{padding:12px;border:1px solid rgba(160,200,230,.14);border-radius:7px;background:rgba(10,22,35,.72);font-size:13px;font-weight:700}.journey span{display:block;font-size:10px;color:#8199ad;margin-top:4px;font-weight:500}.finalStats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}.finalStat{padding:18px;border-radius:8px;background:rgba(50,90,120,.16);border:1px solid rgba(160,205,235,.16)}.finalStat b{font-size:30px}.finalStat span{display:block;font-size:11px;color:#8ea6b9;margin-top:5px;letter-spacing:1px}.note{font-size:12px;color:#7f96a8;margin-top:18px;line-height:1.5}
.tooltip{position:fixed;pointer-events:none;opacity:0;z-index:20;background:#081522;border:1px solid rgba(160,205,235,.35);border-radius:7px;padding:10px 12px;min-width:210px;transition:opacity .15s}.ttName{font-size:14px;font-weight:800}.ttLine{font-size:12px;color:#9db2c3;margin-top:5px}

.panelHead{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}.muted{font-size:13px!important;color:#8fa7bb!important;margin:4px 0 0!important}.liveTag{font-size:10px;letter-spacing:1.4px;font-weight:800;color:#9dd7ef;border:1px solid rgba(145,205,235,.3);padding:6px 8px;border-radius:999px;white-space:nowrap}.exploreGrid{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(330px,.85fr);gap:18px;margin-top:18px}.searchResults{display:grid;gap:6px;margin:10px 0}.resultItem{width:100%;display:flex;justify-content:space-between;align-items:center;text-align:left;background:#0a1724;border:1px solid rgba(160,200,230,.12);border-radius:7px;color:#dbe9f3;padding:10px 12px}.resultItem:hover,.resultItem.active{border-color:rgba(150,215,245,.55);background:rgba(40,82,110,.35)}.resultItem b{font-size:13px}.resultItem span{font-size:11px;color:#89a4b8}.planetHero{display:flex;gap:15px;align-items:center}.planetHero img{width:120px;height:120px;object-fit:cover;aspect-ratio:1/1;width:124px;height:124px;border-radius:8px;object-fit:cover;background:#02060b;border:1px solid rgba(170,215,240,.3);box-shadow:0 0 24px rgba(100,170,220,.15)}.planetHero h2{font-size:25px;margin:5px 0 4px}.statusLine{font-size:12px;line-height:1.45;color:#9fb4c6}.exploreStats{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:18px 0}.exploreStats>div{border:1px solid rgba(160,200,230,.13);background:#091522;border-radius:7px;padding:10px}.exploreStats b{display:block;font-size:18px}.exploreStats span{display:block;font-size:9px;color:#8199ad;letter-spacing:1px;margin-top:4px}.exploreCopy{font-size:13px;line-height:1.55;color:#b6c8d6}.miniMap{margin-top:15px;border-top:1px solid rgba(160,200,230,.12);padding-top:12px}.miniMapTitle{font-size:10px;letter-spacing:1.4px;color:#7f9ab0;font-weight:800}.miniMapRow{display:grid;grid-template-columns:1fr auto 1fr auto;gap:10px;align-items:center;margin-top:8px;font-size:11px;color:#8199ad}.miniMapRow b{font-size:14px;color:#dbe9f2}.exploreActions{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.control.primary{border-color:rgba(155,215,245,.55);background:rgba(37,88,120,.35)}
.threeBadge{position:absolute;top:15px;left:16px;z-index:20;padding:7px 10px;border:1px solid rgba(150,215,245,.25);border-radius:999px;background:rgba(3,10,18,.72);font-size:9px;letter-spacing:1.2px;color:#b5cedd;font-weight:800}.solarStage canvas{display:block;width:100%!important;height:100%!important}.solarExplorer > .solarStage{width:100%;grid-column:1}.solarExplorer > .panel{width:100%;}.solarExplorer .solarDetail{text-align:center}.solarExplorer .solarDetail .solarHero{margin-left:auto;margin-right:auto}.solarExplorer .solarDetail .planetStats{text-align:left}.solarExplorer .solarDetail .moonHeader{text-align:left}.solarExplorer .solarDetail .moonGrid{text-align:left}.solarStage #threeSolarMount{position:absolute;left:0;top:0;width:100%;height:100%;z-index:2;display:block}.solarStage #threeSolarMount canvas{display:block;width:100%!important;height:100%!important}.solarFallback{position:absolute;left:50%;top:50%;width:330px;height:330px;transform:translate(-50%,-50%);border-radius:50%;object-fit:cover;z-index:1;opacity:.92;filter:saturate(1.08);box-shadow:0 0 60px rgba(120,180,220,.18)}.solarToolbar{display:flex;gap:8px;margin-bottom:14px}.solarToolbar .search{flex:1}.solarExplorer{display:grid;grid-template-columns:1fr;gap:18px;min-height:690px}.solarStage{position:relative;height:620px;min-height:620px;border:1px solid rgba(160,205,235,.16);border-radius:12px;overflow:hidden;background:radial-gradient(circle at 50% 50%,rgba(75,120,165,.12),transparent 20%),radial-gradient(circle at 50% 50%,rgba(255,170,80,.06),transparent 42%),#02060b}.solarStage:before{content:"";position:absolute;inset:0;background-image:radial-gradient(circle at 20% 30%,rgba(255,255,255,.8) 0 1px,transparent 1.5px),radial-gradient(circle at 70% 18%,rgba(190,220,255,.55) 0 1px,transparent 1.5px),radial-gradient(circle at 83% 70%,rgba(255,255,255,.65) 0 1px,transparent 1.5px);background-size:180px 160px,230px 190px,260px 210px;opacity:.25}.orbit{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);border:1px solid rgba(145,190,220,.16);border-radius:50%;pointer-events:none}.orbit1{width:18%;height:18%}.orbit2{width:28%;height:28%}.orbit3{width:38%;height:38%}.orbit4{width:48%;height:48%}.orbit5{width:60%;height:60%}.orbit6{width:72%;height:72%}.orbit7{width:84%;height:84%}.orbit8{width:96%;height:96%}.sunCore{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:92px;height:92px;border-radius:50%;z-index:4;text-align:center}.sunCore img{width:92px;height:92px;object-fit:cover;border-radius:50%;animation:spinPlanet 28s linear infinite;box-shadow:0 0 35px rgba(255,184,80,.3)}.sunCore span{position:absolute;left:50%;top:100%;transform:translateX(-50%);font-size:10px;font-weight:800;letter-spacing:1.5px;color:#e8c997}.orbiter{position:absolute;left:50%;top:50%;z-index:5;transform-origin:0 0}.planetNode{position:absolute;transform:translate(-50%,-50%);border:1px solid rgba(185,220,240,.25);border-radius:50%;background:#03070c;padding:0;overflow:visible;transition:transform .2s,border-color .2s;box-shadow:0 0 0 rgba(100,190,240,0)}.planetNode:hover,.planetNode.active{border-color:rgba(180,230,250,.85);box-shadow:0 0 25px rgba(100,190,240,.2);transform:translate(-50%,-50%) scale(1.13)}.planetNode img{display:block;width:100%;height:100%;border-radius:50%;object-fit:cover;animation:spinPlanet var(--spin,16s) linear infinite}.planetNode .nodeLabel{position:absolute;top:calc(100% + 7px);left:50%;transform:translateX(-50%);white-space:nowrap;font-size:10px;font-weight:800;letter-spacing:.7px;color:#cfe0ea;text-shadow:0 1px 3px #000}.solarLegend{position:absolute;left:16px;bottom:13px;font-size:9px;letter-spacing:1px;color:#71889b;z-index:10}.planetList{display:grid;grid-template-columns:1fr 1fr;gap:7px;max-height:260px;overflow:auto}.planetCard{position:relative;display:flex;align-items:center;gap:9px;text-align:left;background:#08131f;border:1px solid rgba(160,200,230,.12);border-radius:8px;color:#dce8f0;padding:7px}.planetCard:hover,.planetCard.active{border-color:rgba(150,215,245,.6);background:rgba(35,75,102,.35)}.planetThumb{width:36px;height:36px;border-radius:50%;object-fit:cover;flex:0 0 36px}.planetName{font-size:12px;font-weight:800}.planetType{font-size:9px;color:#7891a4;margin-top:2px}.detailText{font-size:13px;line-height:1.55;color:#aabfce;margin-top:12px}.detailSub{font-size:10px;letter-spacing:1.5px;color:#7f9bb0;font-weight:800}.detailTitle,.planetTargetName{font-size:29px;font-weight:800;letter-spacing:.5px;margin:4px 0}.planetTargetType{font-size:10px;letter-spacing:1.4px;color:#87a4b8;font-weight:800}.solarHero{width:170px;height:170px;border-radius:50%;object-fit:cover;margin:15px auto 12px;display:block;background:#02060b;border:1px solid rgba(175,220,240,.3);animation:spinPlanet 22s linear infinite;box-shadow:0 0 30px rgba(100,170,220,.14)}.solarTag{display:inline-block;border:1px solid rgba(150,210,235,.28);padding:6px 9px;border-radius:999px;color:#a8c7d9;font-size:10px;font-weight:800;letter-spacing:.8px}.planetStats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px}.planetStat{border:1px solid rgba(160,200,230,.12);background:#08131f;border-radius:7px;padding:9px}.planetStat b{display:block;font-size:12px}.planetStat span{display:block;font-size:8px;color:#748da1;margin-top:4px;letter-spacing:.8px}.moonHeader{font-size:11px;letter-spacing:1.3px;font-weight:800;color:#93aec2;margin-bottom:8px}.moonGrid{display:grid;grid-template-columns:1fr 1fr;gap:8px}.moonCard{border:1px solid rgba(160,200,230,.12);border-radius:8px;background:#07121e;overflow:hidden}.moonVisual{position:relative}.moonImage{width:100%;height:110px;object-fit:cover;display:block}.moon3dTag{position:absolute;left:6px;bottom:6px;padding:4px 6px;border-radius:4px;background:rgba(2,8,14,.78);font-size:8px;letter-spacing:1px;color:#b9d5e3;font-weight:800}.moonName{font-size:12px;font-weight:800;padding:8px 8px 0}.moonFact{font-size:10px;line-height:1.45;color:#849bad;padding:4px 8px 9px}.moonNoImage{height:110px;display:flex;align-items:center;justify-content:center;font-size:9px;letter-spacing:1px;color:#70879a;background:#030a11}.moonCard{cursor:pointer}.moonCard:focus-visible{outline:2px solid #8ec8e8;outline-offset:2px}.moonModal{position:fixed;inset:0;z-index:100;background:rgba(1,5,10,.78);display:none;align-items:center;justify-content:center;padding:20px}.moonModal.open{display:flex}.moonModalBox{width:min(680px,94vw);background:#07121e;border:1px solid rgba(160,210,235,.28);border-radius:12px;padding:18px;box-shadow:0 20px 70px rgba(0,0,0,.5)}.moonModalGrid{display:grid;grid-template-columns:190px 1fr;gap:18px;align-items:start}.moonModalImage{width:190px;height:190px;border-radius:50%;object-fit:cover;border:1px solid rgba(170,215,235,.3);background:#030a11}.moonModalNoImage{width:190px;height:190px;border-radius:50%;display:flex;align-items:center;justify-content:center;border:1px dashed rgba(170,215,235,.3);color:#71889b;font-size:10px;letter-spacing:1px;text-align:center}.moonModalName{font-size:28px;font-weight:800;margin:3px 0 8px}.moonModalFact{font-size:14px;line-height:1.6;color:#a8bccb}.moonModalClose{float:right}.noMoon{font-size:11px;line-height:1.5;color:#849bad;border:1px dashed rgba(160,200,230,.16);border-radius:7px;padding:10px;grid-column:1/-1}@keyframes spinPlanet{to{transform:rotate(360deg)}}
@media(max-width:1000px){.exploreGrid,.solarExplorer{grid-template-columns:1fr}.solarStage{min-height:560px}.exploreStats{grid-template-columns:repeat(2,1fr)}}
@media(max-width:1000px){#layout{grid-template-columns:170px 1fr}.cards{grid-template-columns:repeat(2,1fr)}.dataGrid,.chartLayout{grid-template-columns:1fr}.explainPanel{max-height:330px}.worldButton{width:100%;cursor:pointer;text-align:left}.dataRow{cursor:pointer}.dataRow:hover{background:rgba(55,105,135,.2)}.dataRow.selected{background:rgba(55,105,135,.3);outline:1px solid rgba(150,215,245,.35)}.worldGrid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){#top{padding:0 15px}.brandMain{font-size:21px}.brandSub,.status{display:none}#pipeline{padding:8px 12px}.step{min-width:130px}.step b{font-size:11px}.step span{font-size:9px}#layout{grid-template-columns:1fr}.side{height:82px;border-right:0;border-bottom:1px solid rgba(170,205,235,.13);display:flex;overflow-x:auto;padding:8px}.mission,.method{display:none}.nav{min-width:130px;padding:10px;font-size:11px}.view{padding:20px 15px}.title{font-size:30px}.lead{font-size:15px}.cards{grid-template-columns:1fr 1fr}.card .value{font-size:24px}.worldGrid,.journey,.finalStats{grid-template-columns:1fr}.final h1{font-size:38px}}
.worldButton{width:100%;text-align:left;cursor:pointer;color:inherit;font:inherit}.worldButton:hover{border-color:rgba(150,215,245,.55);transform:translateY(-1px)}.worldAction{margin-top:12px;font-size:9px;letter-spacing:1px;color:#8fb4c9;font-weight:800}.solarStage{cursor:default}.solarHint{position:absolute;right:16px;bottom:14px;z-index:10;font-size:9px;letter-spacing:1px;color:#71889b}.planetCard{cursor:pointer;min-height:58px}.planetCard:focus-visible,.worldButton:focus-visible,.moonCard:focus-visible{outline:2px solid #8ec8e8;outline-offset:2px}.moonDetail{margin-top:12px;border:1px solid rgba(150,210,235,.16);border-radius:8px;padding:10px;background:rgba(3,10,17,.7)}.moonDetail.selectedMoon{border-color:rgba(150,215,240,.35)}.moonDetailGrid{display:grid;grid-template-columns:96px 1fr;gap:12px;align-items:center}.moonDetailImage,.moonDetailNoImage{width:96px;height:96px;border-radius:8px;object-fit:cover;border:1px solid rgba(170,215,235,.25);background:#030a11}.moonDetailNoImage{display:flex;align-items:center;justify-content:center;text-align:center;font-size:8px;letter-spacing:.7px;color:#71889b;padding:8px}.moonDetailTitle{font-size:20px;font-weight:800;margin:2px 0 6px}.moonDetailBody{font-size:12px;line-height:1.55;color:#a7bccb}.solarHero{cursor:pointer}.solarHero:hover{border-color:rgba(180,230,250,.7)}
.dataRow.selected td{background:rgba(45,100,130,.18)}.squareSelected{width:82px!important;height:82px!important;object-fit:cover!important;aspect-ratio:1/1!important;border-radius:8px!important}.worldButton:focus-visible,.dataRow:focus-visible{outline:2px solid #8ec8e8;outline-offset:2px}.globalDetail{margin:0 0 18px;border-color:rgba(130,205,240,.25);background:linear-gradient(135deg,rgba(8,24,37,.98),rgba(3,11,18,.98));padding:16px}.globalDetailHead{display:flex;justify-content:space-between;gap:16px;align-items:center}.globalDetailName{font-size:26px;font-weight:900;letter-spacing:.4px;margin:3px 0 5px}.globalDetailHead img{width:92px;height:92px;min-width:92px;object-fit:cover;aspect-ratio:1/1;border-radius:10px;border:1px solid rgba(170,215,235,.3);background:#02070c}.globalStats{display:grid;grid-template-columns:repeat(6,1fr);gap:7px;margin-top:12px}.globalStats>div{border:1px solid rgba(160,200,230,.12);background:#08131f;border-radius:7px;padding:8px}.globalStats b{display:block;font-size:13px;font-weight:900}.globalStats span{display:block;font-size:8px;color:#748da1;margin-top:4px;letter-spacing:.8px}.globalCopy{font-size:12px;line-height:1.55;color:#aabfce;margin-top:12px}.globalCoords{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.globalCoords span{border:1px solid rgba(160,200,230,.12);background:#07121e;border-radius:999px;padding:6px 9px;font-size:9px;color:#7891a4}.globalCoords b{color:#dce8f0;font-size:10px;margin-left:4px}</style>
</head>
<body>
<div id="app">
<header id="top"><div><div class="brandMain">COSMOSCOPE</div><div class="brandSub">EXOPLANET DISCOVERY LABORATORY · MISSION 05</div></div><div class="status"><span class="dot"></span>SCIENTIFIC ANALYSIS ONLINE</div></header>
<div id="pipeline">
<div class="step" data-view="data" role="button" tabindex="0"><b>01 · NASA DATA</b><span>Observed worlds</span></div><div class="arrow">→</div>
<div class="step" data-view="dbscan" role="button" tabindex="0"><b>02 · DBSCAN</b><span>Find groups</span></div><div class="arrow">→</div>
<div class="step" data-view="umap" role="button" tabindex="0"><b>03 · UMAP</b><span>Reveal patterns</span></div><div class="arrow">→</div>
<div class="step" data-view="lof" role="button" tabindex="0"><b>04 · LOF</b><span>Find unusual worlds</span></div><div class="arrow">→</div>
<div class="step" data-view="worlds" role="button" tabindex="0"><b>05 · UNUSUAL WORLDS</b><span>Inspect candidates</span></div><div class="arrow">→</div>
<div class="arrow">→</div><div class="step" data-view="solar" role="button" tabindex="0"><b>06 · PLANETS & MOONS</b><span>Real-world reference</span></div><div class="arrow">→</div><div class="step" data-view="discovery" role="button" tabindex="0"><b>07 · DISCOVERY</b><span>Complete exploration</span></div>
</div>
<div id="layout">
<aside class="side"><div class="mission">MISSION 05</div>
<button class="nav active" data-view="data">01 · NASA DATA<small>Start with observations</small></button>
<button class="nav" data-view="dbscan">02 · DBSCAN<small>Group similar worlds</small></button>
<button class="nav" data-view="umap">03 · UMAP<small>See hidden structure</small></button>
<button class="nav" data-view="lof">04 · LOF<small>Spot local outliers</small></button>
<button class="nav" data-view="worlds">05 · UNUSUAL WORLDS<small>Inspect candidates</small></button>
<button class="nav" data-view="solar">06 · PLANETS & MOONS<small>Real solar-system reference</small></button><button class="nav" data-view="discovery">07 · DISCOVERY<small>Mission summary</small></button>
<div class="method"><div><span>FEATURES</span><b>9</b></div><div><span>DBSCAN</span><b>0.5 / 10</b></div><div><span>UMAP</span><b>15 / 0.1</b></div><div><span>LOF</span><b>20 NN</b></div></div>
</aside>
<main id="main">
<div class="globalDetail panel" id="globalDetail"><div class="globalDetailHead"><div><div class="kicker">CLICKED WORLD · LIVE DETAILS</div><div class="globalDetailName" id="globalName">NO WORLD SELECTED</div><div class="statusLine" id="globalStatus">Click any NASA row, DBSCAN bar, UMAP point, LOF point, unusual-world card, planet, or moon.</div></div><img id="globalImage" alt="Selected world"/></div><div class="globalStats"><div><b id="globalCluster">—</b><span>DBSCAN</span></div><div><b id="globalLof">—</b><span>LOF SCORE</span></div><div><b id="globalTemp">—</b><span>EQ TEMP</span></div><div><b id="globalRadius">—</b><span>RADIUS</span></div><div><b id="globalMass">—</b><span>MASS</span></div><div><b id="globalPeriod">—</b><span>ORBITAL PERIOD</span></div></div><div class="globalCopy" id="globalCopy">The selected observation will be explained here with its measured values and model context.</div><div class="globalCoords"><span>UMAP X <b id="globalX">—</b></span><span>UMAP Y <b id="globalY">—</b></span><span>DISTANCE <b id="globalDistance">—</b></span><span>METHOD <b id="globalMethod">—</b></span><span>YEAR <b id="globalYear">—</b></span></div></div>
<section class="view active" id="view-data">
<div class="sectionHead"><div><div class="kicker">01 · START WITH REAL OBSERVATIONS</div><div class="title">NASA EXOPLANET DATA</div><div class="lead">Explore the complete stored catalog by clicking a listed world, then connect it to DBSCAN, UMAP and LOF.</div></div><div class="pill" id="dataFile"></div></div>
<div class="cards"><div class="card"><div class="label">PLANETS ANALYZED</div><div class="value" id="total"></div><p>Rows available for this analysis.</p></div><div class="card"><div class="label">NUMERICAL FEATURES</div><div class="value">9</div><p>Planet and host-star properties used by the analysis.</p></div><div class="card"><div class="label">DBSCAN GROUPS</div><div class="value" id="clusters"></div><p>Similarity groups found in the stored result.</p></div><div class="card"><div class="label">LOF OUTLIERS</div><div class="value" id="outliers"></div><p>Observations marked unusual by the stored LOF result.</p></div></div>
<div class="info"><b>EXPLORE MODE:</b> Nothing needs to be searched. The catalog is listed below; click any planet row or card and its complete observation appears immediately. “Unusual” means unusual within this dataset and model.</div>
<div class="exploreGrid">
  <div class="panel"><div class="panelHead"><div><h3>NASA CATALOG · CLICK ANY WORLD</h3><p class="muted">Every stored observation is listed. Select a row to inspect its data.</p></div><span class="liveTag">CLICK TO EXPLORE</span></div><div class="tableWrap"><table class="dataTable"><thead><tr><th>PLANET</th><th>METHOD</th><th>YEAR</th><th>RADIUS</th><th>MASS</th><th>TEMP</th><th>DBSCAN</th><th>LOF</th></tr></thead><tbody id="dataBody"></tbody></table></div></div>
  <div class="exploreDetail panel" id="exploreDetail"><div class="planetHero"><img id="explorePlanetImage" alt="Selected exoplanet"/><div><div class="kicker">SELECTED OBSERVATION</div><h2 id="exploreName">CLICK ANY PLANET</h2><div class="statusLine" id="exploreStatus">Choose a row, UMAP point, LOF point, DBSCAN bar, or unusual-world card.</div></div></div><div class="exploreStats"><div><b id="exploreCluster">—</b><span>DBSCAN</span></div><div><b id="exploreLof">—</b><span>LOF SCORE</span></div><div><b id="exploreTemp">—</b><span>EQ TEMP</span></div><div><b id="exploreRadius">—</b><span>RADIUS</span></div></div><div class="exploreCopy" id="exploreCopy">Click any listed observation to connect the NASA measurements with DBSCAN, UMAP and LOF.</div><div class="miniMap"><div class="miniMapTitle">WHERE IT SITS IN THE UMAP / LOF VIEW</div><div class="miniMapRow"><span>UMAP X</span><b id="exploreX">—</b><span>UMAP Y</span><b id="exploreY">—</b></div></div><div class="exploreActions"><button class="control primary" id="openUMAP">OPEN UMAP</button><button class="control" id="openLOF">OPEN LOF</button><button class="control" id="openWorlds">UNUSUAL WORLDS</button></div></div>
</div>
<div class="selectionDock panel" id="selectionDock"><div class="kicker">LIVE SELECTION</div><div id="selectionDockBody">Click anything interactive in Scene 5. The selected world's image and analysis will appear here.</div></div>
</section>
<section class="view" id="view-dbscan"><div class="sectionHead"><div><div class="kicker">02 · FIND SIMILAR WORLDS</div><div class="title">DBSCAN</div><div class="lead">DBSCAN looks for dense groups of observations. We do not need to tell it the number of groups first.</div></div><div class="pill">EPS 0.5 · MIN SAMPLES 10</div></div><div class="chartLayout"><div class="chartPanel"><canvas id="clusterCanvas"></canvas></div><div class="explainPanel"><div class="big">GROUPS</div><div class="formula">Dense region → similar observations<br>Separate region → different population<br>Noise → points without enough neighbors</div><h3>Why use DBSCAN?</h3><p>Exoplanets do not necessarily form neat, equally sized groups. DBSCAN is useful because it searches for dense regions and can label isolated observations as noise.</p><h3>Stored result</h3><p><b id="clusterText"></b> groups are represented in the exported analysis.</p><p>The chart shows how many observations belong to each DBSCAN cluster.</p></div></div></section>
<section class="view" id="view-umap"><div class="sectionHead"><div><div class="kicker">03 · TURN MANY FEATURES INTO A MAP</div><div class="title">UMAP</div><div class="lead">Nine measurements are reduced to two visual dimensions so relationships between worlds become easier to see.</div></div><div class="pill" id="umapStatus"></div></div><div class="chartLayout"><div class="chartPanel"><canvas id="umapCanvas"></canvas><div class="controls"><button class="control" id="zoomIn">ZOOM +</button><button class="control" id="zoomOut">ZOOM −</button><button class="control" id="resetZoom">RESET</button></div><div class="chartSelection"><img id="umapSelectedImage" src="__EXOPLANET_IMAGE__" alt="Selected exoplanet"/><div><b id="umapSelectedName">Click a UMAP point</b><span id="umapSelectedMeta">The selected world appears here.</span></div></div></div><div class="explainPanel"><div class="big">MAP</div><div class="formula">9 features → Standardize → UMAP → 2D</div><h3>What does a point mean?</h3><p>Each point is one observed exoplanet. Nearby points have similar positions in the reduced feature space.</p><h3>Try it</h3><p>Click a point to inspect its planet name, DBSCAN cluster and LOF score. Zoom to explore dense regions.</p><h3>Settings</h3><p>Neighbors: <b>15</b><br>Minimum distance: <b>0.1</b><br>Random state: <b>42</b></p></div></div></section>
<section class="view" id="view-lof"><div class="sectionHead"><div><div class="kicker">04 · FIND WORLDS THAT STAND APART</div><div class="title">LOF — LOCAL OUTLIER FACTOR</div><div class="lead">LOF compares each observation with its local neighborhood and highlights observations that differ from nearby worlds.</div></div><div class="pill">20 NEIGHBORS · STORED RESULT</div></div><div class="cards"><div class="card"><div class="label">NORMAL</div><div class="value" id="normal"></div><p>Observations labeled normal.</p></div><div class="card"><div class="label">POTENTIAL OUTLIERS</div><div class="value" id="lofOut"></div><p>Observations labeled as LOF outliers.</p></div><div class="card"><div class="label">NEIGHBORS</div><div class="value">20</div><p>Local neighborhood size.</p></div><div class="card"><div class="label">CONTAMINATION</div><div class="value">0.05</div><p>Stored analysis setting.</p></div></div><div class="chartLayout" style="height:500px"><div class="chartPanel"><canvas id="lofCanvas"></canvas><div class="chartSelection"><img id="lofSelectedImage" src="__EXOPLANET_IMAGE__" alt="Selected exoplanet"/><div><b id="lofSelectedName">Click a LOF point</b><span id="lofSelectedMeta">The selected world appears here.</span></div></div></div><div class="explainPanel"><div class="big">OUTLIER</div><div class="formula">Higher local unusualness → inspect the observation</div><h3>Important</h3><p>An algorithmic outlier is <b>not automatically a new planet</b>. It is an observation whose measured characteristics differ from nearby observations in the analyzed feature space.</p><h3>Click a point</h3><p>Use the chart to connect the statistical result back to an individual exoplanet.</p></div></div></section>
<section class="view" id="view-worlds"><div class="sectionHead"><div><div class="kicker">05 · RETURN FROM THE MODEL TO REAL WORLDS</div><div class="title">UNUSUAL WORLDS</div><div class="lead">These are the stored LOF candidates that deserve closer inspection because their measured properties are unusual relative to their local neighborhoods.</div></div><div class="pill">TOP STORED CANDIDATES</div></div><div class="worldGrid" id="worldGrid"></div><div class="info" style="margin-top:18px"><b>Interpretation:</b> “Unusual” here means unusual within this analysis. It does not mean the world is confirmed as a scientific discovery.</div></section>
<section class="view" id="view-solar">
<div class="sectionHead"><div><div class="kicker">06 · PLANETS & MOONS</div><div class="title">PLANETS & MOONS</div><div class="lead">Explore one real Solar System world at a time. Choose a planet below, then click a moon to read its story.</div></div><div class="pill">THREE.JS · FOCUSED WORLD</div></div>
<div class="solarExplorer">
  <div class="solarStage" id="solarStage">
    <div class="threeBadge" id="threeModeLabel">EARTH · FOCUSED WORLD</div>
    <img class="solarFallback" id="solarFallbackImage" src="__EARTH__" alt="Selected planet preview"><div id="threeSolarMount"></div>
    <div class="solarHint">CLICK THE PLANET · DRAG TO LOOK AROUND · USE THE PLANET LIST TO EXPLORE</div>
  </div>
  <div class="solarSide">
    <div class="panel"><div class="kicker">CHOOSE A WORLD</div><p class="muted">No searching is required. Every available planet is listed here.</p><div class="planetList" id="planetList"></div></div>
    <div class="panel" id="planetInfoPanel"><div class="kicker">PLANET INFORMATION</div><div class="planetTargetName" id="solarTargetName">Earth</div><div class="planetTargetType" id="solarTargetType">TERRESTRIAL PLANET</div><img class="solarHero" id="planetDetailImage" alt="Selected planet"/><div class="solarTag" id="planetDetailMoons"></div><div class="planetStats"><div class="planetStat"><b id="planetDistance"></b><span>MEAN SUN DISTANCE</span></div><div class="planetStat"><b id="planetYear"></b><span>ORBITAL PERIOD</span></div><div class="planetStat"><b id="planetMoonCount"></b><span>NATURAL MOONS</span></div></div><div class="detailText" id="planetDetailDescription"></div></div>
    <div class="panel"><div class="moonHeader">MOONS OF THIS WORLD</div><div class="detailText" id="planetMoonInfo"></div><div class="moonGrid" id="moonGrid"></div><div class="moonDetail" id="moonDetail"><div class="moonDetailTitle">CLICK A MOON TO EXPLORE</div><div class="moonDetailBody">Its image and scientific information will appear here.</div></div></div>
  </div>
</div>
</section></section></section><div class="moonModal" id="moonModal" role="dialog" aria-modal="true" aria-labelledby="moonModalName"><div class="moonModalBox"><button type="button" class="control moonModalClose" id="moonModalClose">CLOSE</button><div class="kicker">NATURAL SATELLITE</div><div class="moonModalGrid"><div id="moonModalVisual"></div><div><div class="moonModalName" id="moonModalName"></div><div class="planetTargetType" id="moonModalParent"></div><p class="moonModalFact" id="moonModalFact"></p></div></div></div></div><section class="view" id="view-discovery"><div id="discovery"><div class="final"><div class="kicker">07 · COSMOSCOPE FINAL STAGE</div><h1>DISCOVERY</h1><p>CosmoScope began by leaving Earth and exploring the Solar System, then moved through interstellar space, the Milky Way, nebulae, star clusters, black holes, other galaxies and exoplanets. The final stage brings that exploration back to real data.</p><div class="finalStats"><div class="finalStat"><b id="dPlanets"></b><span>PLANETS ANALYZED</span></div><div class="finalStat"><b id="dClusters"></b><span>DBSCAN GROUPS</span></div><div class="finalStat"><b id="dOutliers"></b><span>LOF OUTLIERS</span></div></div><h3 style="font-size:20px;margin-top:30px">THE COMPLETE COSMOSCOPE JOURNEY</h3><div class="journey">
<div>🌙 MOON<span>Earth's companion</span></div><div>🌍 EARTH<span>Our starting point</span></div><div>☀️ SOLAR SYSTEM<span>Planets and moons</span></div><div>☄️ ASTEROIDS & COMETS<span>Small Solar System bodies</span></div><div>❄️ OUTER SOLAR SYSTEM<span>Kuiper region and beyond</span></div><div>🌌 INTERSTELLAR SPACE<span>Beyond the Solar System</span></div><div>⭐ MILKY WAY<span>Our galaxy</span></div><div>🌫️ NEBULAE<span>Clouds of gas and dust</span></div><div>⭐ STAR CLUSTERS<span>Groups of stars</span></div><div>🕳️ BLACK HOLES<span>Extreme gravitational objects</span></div><div>🌌 OTHER GALAXIES<span>Galaxies beyond our own</span></div><div>🪐 EXOPLANETS<span>Worlds orbiting other stars</span></div><div>🔭 NASA EXOPLANET DATA<span>Measured observations</span></div><div>🧩 DBSCAN<span>Find similar groups</span></div><div>🗺️ UMAP<span>Reveal hidden structure</span></div><div>⚠️ LOF<span>Find local anomalies</span></div><div>🔬 UNUSUAL WORLDS<span>Inspect candidates</span></div><div>🪐 PLANETS & MOONS<span>Real solar-system reference</span></div><div>✦ DISCOVERY<span>Questions for further study</span></div>
</div><div class="note">CosmoScope connects visual space exploration with data-driven exoplanet analysis. The final result is an analytical shortlist for further investigation, not a claim of confirmed new discoveries.</div></div></div></section>
</main></div>
<div class="tooltip" id="tooltip"><div class="ttName"></div><div class="ttLine"></div></div>

<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script>
(function(){"use strict";
let threeScene=null,threeCamera=null,threeRenderer=null,threeRoot=null,threeRaycaster=null,threePointer=null;
let active="data";
let solarPaused=false,solarRAF=null,solarLast=0,solarClock=0,selectedPlanet=2;
const DATA=__DATA__;
const SOLAR=__SOLAR__;
let zoom=1;
const palette=["#7ec8e8","#a6d98a","#d8a6e8","#e8c77e","#e89a9a","#8fd6c8","#b9a7e8","#d5b48c"];
const $=id=>document.getElementById(id);
const fmt=(v,n=2)=>Number.isFinite(Number(v))?Number(v).toFixed(n):"—";

function show(view){
  const allowed=["data","dbscan","umap","lof","worlds","solar","discovery"];
  if(!allowed.includes(view)) view="data";
  active=view;
  document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active",v.id==="view-"+view));
  document.querySelectorAll(".nav").forEach(b=>b.classList.toggle("active",b.dataset.view===view));
  const stepIndex={data:0,dbscan:1,umap:2,lof:3,worlds:4,solar:5,discovery:6}[view];
  document.querySelectorAll(".step").forEach((s,i)=>s.classList.toggle("active",i===stepIndex));
  if(view==="solar") renderSolar();
  if(view==="data") renderTable($("search")?$("search").value:"");
  if(view==="dbscan") drawCluster();
  if(view==="umap") drawPoints("umapCanvas",false);
  if(view==="lof") drawPoints("lofCanvas",true);
  if(view==="worlds") renderWorlds();
}
document.addEventListener("click",function(e){
  const nav=e.target.closest(".nav,.step");
  if(nav&&nav.dataset.view){e.preventDefault();show(nav.dataset.view);}
});
document.addEventListener("keydown",function(e){
  const nav=e.target.closest(".nav,.step");
  if(nav&&nav.dataset.view&&(e.key==="Enter"||e.key===" ")){e.preventDefault();show(nav.dataset.view);}
});

function texture(name){
  if(!name||!window.THREE)return null;
  try{const tex=new THREE.TextureLoader().load(name);tex.colorSpace=THREE.SRGBColorSpace;return tex;}catch(e){return null;}
}
function sphereMaterial(image,color){
  const tex=texture(image);
  return new THREE.MeshStandardMaterial({map:tex,color:tex?0xffffff:(color||0x8aa0b0),roughness:.88,metalness:.01});
}
function initThreeSolar(){
  if(threeRenderer||!window.THREE)return;
  const mount=$("threeSolarMount"),stage=$("solarStage"); if(!mount||!stage)return;
  threeScene=new THREE.Scene();
  threeScene.background=new THREE.Color(0x02060b);
  threeCamera=new THREE.PerspectiveCamera(42,Math.max(1,stage.clientWidth)/Math.max(1,stage.clientHeight),.1,180);
  threeCamera.position.set(0,2.2,15.5);
  threeRenderer=new THREE.WebGLRenderer({antialias:true,alpha:true});
  threeRenderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
  threeRenderer.setSize(Math.max(1,stage.clientWidth),Math.max(1,stage.clientHeight));
  threeRenderer.outputColorSpace=THREE.SRGBColorSpace;
  threeRenderer.domElement.style.cursor="grab";
  mount.appendChild(threeRenderer.domElement); const fallback=$("solarFallbackImage"); if(fallback) fallback.style.display="none";
  threeRaycaster=new THREE.Raycaster(); threePointer=new THREE.Vector2();
  threeScene.add(new THREE.AmbientLight(0xb9c9d8,1.25));
  const key=new THREE.DirectionalLight(0xffffff,2.7);key.position.set(7,6,10);threeScene.add(key);
  const fill=new THREE.DirectionalLight(0x8eb7dc,.8);fill.position.set(-6,2,6);threeScene.add(fill);
  const geo=new THREE.BufferGeometry(),pts=[];
  for(let i=0;i<700;i++){const r=35+Math.random()*80,a=Math.random()*Math.PI*2,b=Math.acos(2*Math.random()-1);pts.push(r*Math.sin(b)*Math.cos(a),r*Math.cos(b),r*Math.sin(b)*Math.sin(a));}
  geo.setAttribute("position",new THREE.Float32BufferAttribute(pts,3));
  threeScene.add(new THREE.Points(geo,new THREE.PointsMaterial({color:0xbfdcff,size:.14,sizeAttenuation:true})));
  buildFocusedWorld(selectedPlanet);
  centerSolarCamera();
  threeRenderer.domElement.addEventListener("pointerdown",onThreePointer);
  window.addEventListener("resize",resizeThree);
  solarLast=performance.now();solarRAF=requestAnimationFrame(animateThree);
}
function buildFocusedWorld(index){
  if(!threeScene)return;
  while(threeRoot){threeScene.remove(threeRoot);threeRoot=null;}
  threeRoot=new THREE.Group();threeScene.add(threeRoot);
  const p=SOLAR[index]||SOLAR[2];
  const fallback=$("solarFallbackImage"); if(fallback){fallback.src=p.image||""; fallback.style.display=threeRenderer?"none":"block";}
  const planet=new THREE.Mesh(new THREE.SphereGeometry(3.75,72,72),sphereMaterial(p.image,0x8aa0b0));
  planet.userData={planetIndex:index,isPlanet:true}; threeRoot.add(planet);
  const glow=new THREE.Mesh(new THREE.SphereGeometry(3.84,64,64),new THREE.MeshBasicMaterial({color:0x8fc8ef,transparent:true,opacity:.035,side:THREE.BackSide}));threeRoot.add(glow);
  const moons=p.moonCards||[];
  moons.forEach((m,j)=>{
    const pivot=new THREE.Object3D();pivot.rotation.y=(j/Math.max(1,moons.length))*Math.PI*2;threeRoot.add(pivot);
    const radius=5.6+j*1.55;
    const points=[];for(let k=0;k<=96;k++){const a=k/96*Math.PI*2;points.push(new THREE.Vector3(Math.cos(a)*radius,0,Math.sin(a)*radius));}
    pivot.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color:0x52728a,transparent:true,opacity:.25})));
    const moon=new THREE.Mesh(new THREE.SphereGeometry(.62+(j%2)*.08,42,42),sphereMaterial(m.image,0x9ba6ad));
    moon.position.x=radius;moon.userData={moonIndex:j,planetIndex:index,isMoon:true};pivot.add(moon);
  });
  threeCamera.position.set(0,0,17.5);threeCamera.lookAt(0,0,0);
  $("threeModeLabel").textContent=p.name.toUpperCase()+" · "+(moons.length?moons.length+" MOON"+(moons.length>1?"S":"")+"":"NO NATURAL MOONS");
}
function onThreePointer(e){
  if(!threeRenderer||!threeRaycaster||!threePointer||!threeRoot)return;
  const r=threeRenderer.domElement.getBoundingClientRect();threePointer.x=((e.clientX-r.left)/r.width)*2-1;threePointer.y=-((e.clientY-r.top)/r.height)*2+1;threeRaycaster.setFromCamera(threePointer,threeCamera);
  const hits=threeRaycaster.intersectObjects(threeRoot.children,true).filter(h=>h.object.userData&&(h.object.userData.isPlanet||h.object.userData.isMoon));
  if(!hits.length)return;
  const hit=hits[0].object.userData;
  if(hit.isPlanet){selectedPlanet=hit.planetIndex;renderSolar();return;}
  if(hit.isMoon){const p=SOLAR[hit.planetIndex],m=(p.moonCards||[])[hit.moonIndex];if(m)showMoonDetail(m,p);}
}
function resizeThree(){if(!threeRenderer||!threeCamera)return;const stage=$("solarStage");const w=Math.max(1,stage.clientWidth),h=Math.max(1,stage.clientHeight);threeCamera.aspect=w/h;threeCamera.updateProjectionMatrix();threeRenderer.setSize(w,h,false);threeRenderer.domElement.style.width="100%";threeRenderer.domElement.style.height="100%";}
function centerSolarCamera(){if(!threeCamera)return;threeCamera.position.set(0,0,17.5);threeCamera.lookAt(0,0,0);threeCamera.updateProjectionMatrix();}
function animateThree(now){const dt=Math.min(.05,(now-solarLast)/1000);solarLast=now;if(!solarPaused&&threeRoot){const planet=threeRoot.children.find(o=>o.isMesh&&o.userData&&o.userData.isPlanet);if(planet)planet.rotation.y+=dt*.28;threeRoot.children.forEach(o=>{if(o.type==="Object3D")o.rotation.y+=dt*.12;});}if(threeRenderer)threeRenderer.render(threeScene,threeCamera);solarRAF=requestAnimationFrame(animateThree);}
function renderSolarList(){const list=$("planetList");if(!list)return;list.innerHTML=SOLAR.map((p,i)=>`<button type="button" class="planetCard ${i===selectedPlanet?"active":""}" data-planet="${i}"><img class="planetThumb" src="${p.image}" alt="${esc(p.name)}"><div><div class="planetName">${esc(p.name)}</div><div class="planetType">${esc(p.type)}</div><div class="planetType">${esc(p.moons)} moons</div></div></button>`).join("");list.querySelectorAll("[data-planet]").forEach(b=>b.addEventListener("click",()=>{selectedPlanet=Number(b.dataset.planet);renderSolar();}));}
function showMoonDetail(m,p){const box=$("moonDetail");if(!box)return;box.innerHTML=`<div class="moonDetailGrid">${m.image?`<img class="moonDetailImage" src="${m.image}" alt="${esc(m.name)}">`:`<div class="moonDetailNoImage">NO MOON-SPECIFIC IMAGE<br>IN YOUR ASSETS</div>`}<div><div class="kicker">MOON OF ${esc(p.name).toUpperCase()}</div><div class="moonDetailTitle">${esc(m.name)}</div><div class="moonDetailBody">${esc(m.fact)}</div></div></div>`;box.classList.add("selectedMoon");}
function renderSolarDetail(){const p=SOLAR[selectedPlanet]||SOLAR[2];$("solarTargetName").textContent=p.name;$("solarTargetType").textContent=p.type;$("planetDetailImage").src=p.image||"";$("planetDetailMoons").textContent=p.moons+" NATURAL MOONS / SATELLITES";$("planetDistance").textContent=p.distance;$("planetYear").textContent=p.year;$("planetMoonCount").textContent=p.moons;$("planetDetailDescription").textContent=p.description;$("planetMoonInfo").textContent=p.moonsInfo;const cards=p.moonCards||[];$("moonGrid").innerHTML=cards.length?cards.map((m,j)=>`<button type="button" class="moonCard" data-moon-index="${j}"><div class="moonVisual">${m.image?`<img class="moonImage" src="${m.image}" alt="${esc(m.name)}">`:`<div class="moonNoImage">NO LOCAL IMAGE</div>`}<span class="moon3dTag">CLICK FOR INFO</span></div><div class="moonName">${esc(m.name)}</div><div class="moonFact">${esc(m.fact)}</div></button>`).join(""):`<div class="noMoon">${p.moons==="0"?"This planet has no natural moons.":esc(p.moonsInfo)}</div>`;$("moonGrid").querySelectorAll("[data-moon-index]").forEach(b=>b.addEventListener("click",()=>{const m=cards[Number(b.dataset.moonIndex)];if(m)showMoonDetail(m,p);}));}
function renderSolar(){initThreeSolar();if(window.THREE){buildFocusedWorld(selectedPlanet);centerSolarCamera();}renderSolarList();renderSolarDetail();}

function findRows(){return Array.isArray(DATA.rows)?DATA.rows:[];}
function renderTable(){
  const rows=findRows();
  const body=$("dataBody");
  if(!body)return;
  body.innerHTML=rows.map((r,i)=>`<tr class="dataRow" data-name="${esc(r.name)}"><td><b>${esc(r.name)}</b></td><td>${esc(r.method||"NASA ARCHIVE")}</td><td>${r.year==null?"—":r.year}</td><td>${fmt(r.radius)}</td><td>${fmt(r.mass)}</td><td>${fmt(r.temperature,0)}</td><td>${r.cluster===-1?"NOISE":"C"+r.cluster}</td><td>${fmt(r.lof,3)}</td></tr>`).join("")||`<tr><td colspan="8">No observations are available in the stored dataset.</td></tr>`;
  body.querySelectorAll(".dataRow").forEach(row=>row.addEventListener("click",()=>selectExoplanet(row.dataset.name,"NASA DATA")));
}
function showSelectionDock(target,source){
  if(!target)return;
  const d=$("selectionDockBody");
  if(d)d.innerHTML=`<b>${esc(target.name)}</b> · ${esc(source||"SCENE 5")} · DBSCAN ${target.cluster===-1?"NOISE":"C"+target.cluster} · LOF ${fmt(target.lof,3)} · UMAP (${fmt(target.x,3)}, ${fmt(target.y,3)})`;
  const img=$("globalImage"); if(img)img.src=DATA.exoplanetImage||"";
  $("globalName").textContent=target.name;
  $("globalStatus").textContent=(target.outlier?"LOF FLAGGED AS LOCAL OUTLIER":"LOF WITHIN NORMAL LABEL")+" · "+(target.cluster===-1?"DBSCAN NOISE":"DBSCAN CLUSTER "+target.cluster)+(source?" · "+source:"");
  $("globalCluster").textContent=target.cluster===-1?"NOISE":"C"+target.cluster;
  $("globalLof").textContent=fmt(target.lof,3);
  $("globalTemp").textContent=target.temperature==null?"—":fmt(target.temperature,0)+" K";
  $("globalRadius").textContent=target.radius==null?"—":fmt(target.radius,2)+" R⊕";
  $("globalMass").textContent=target.mass==null?"—":fmt(target.mass,2)+" M⊕";
  $("globalPeriod").textContent=target.period==null?"—":fmt(target.period,3)+" d";
  $("globalX").textContent=fmt(target.x,3); $("globalY").textContent=fmt(target.y,3);
  $("globalDistance").textContent=target.distance==null?"—":fmt(target.distance,2)+" pc";
  $("globalMethod").textContent=target.method||"NASA ARCHIVE"; $("globalYear").textContent=target.year==null?"—":target.year;
  $("globalCopy").textContent=`This observation is connected across Scene 5: NASA catalog measurements → DBSCAN ${target.cluster===-1?"noise":"cluster "+target.cluster} → UMAP (${fmt(target.x,3)}, ${fmt(target.y,3)}) → LOF ${fmt(target.lof,3)}. The LOF flag describes unusualness within this analyzed dataset; it is not by itself a confirmed discovery.`;
}
function selectExoplanet(name,source){
  const rows=findRows();
  const target=rows.find(r=>String(r.name)===String(name)) || rows.find(r=>String(r.name).toLowerCase().includes(String(name||"").toLowerCase()));
  if(!target)return null;
  document.querySelectorAll(".dataRow.selected").forEach(r=>r.classList.remove("selected"));
  document.querySelectorAll(".dataRow").forEach(r=>{if(r.dataset.name===String(target.name))r.classList.add("selected")});
  const img=$("explorePlanetImage");
  if(img)img.src=DATA.exoplanetImage||"";
  $("exploreName").textContent=target.name;
  $("exploreStatus").textContent=(target.outlier?"LOF FLAGGED AS LOCAL OUTLIER":"LOF WITHIN NORMAL LABEL")+" · "+(target.cluster===-1?"DBSCAN NOISE":"DBSCAN CLUSTER "+target.cluster)+(source?" · "+source:"");
  $("exploreCluster").textContent=target.cluster===-1?"NOISE":"C"+target.cluster;
  $("exploreLof").textContent=fmt(target.lof,3);
  $("exploreTemp").textContent=target.temperature==null?"—":fmt(target.temperature,0)+" K";
  $("exploreRadius").textContent=target.radius==null?"—":fmt(target.radius,2)+" R⊕";
  $("exploreX").textContent=fmt(target.x,3); $("exploreY").textContent=fmt(target.y,3);
  $("exploreCopy").textContent=`Discovery method: ${target.method||"NASA ARCHIVE"}. Discovery year: ${target.year==null?"—":target.year}. Mass: ${target.mass==null?"—":fmt(target.mass,2)+" M⊕"}. Orbital period: ${target.period==null?"—":fmt(target.period,3)+" days"}. Distance: ${target.distance==null?"—":fmt(target.distance,2)+" pc"}. DBSCAN: ${target.cluster===-1?"noise":"cluster "+target.cluster}. UMAP: (${fmt(target.x,3)}, ${fmt(target.y,3)}). LOF: ${fmt(target.lof,3)}.`;
  showSelectionDock(target,source);
  return target;
}
function esc(s){return String(s).replace(/[&<>"']/g,m=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[m]))}
function setupCanvas(c){let dpr=window.devicePixelRatio||1,w=c.clientWidth,h=c.clientHeight;c.width=w*dpr;c.height=h*dpr;let x=c.getContext("2d");x.setTransform(dpr,0,0,dpr,0,0);return{x,w,h}}
function grid(c,w,h){c.strokeStyle="rgba(170,205,235,.09)";c.lineWidth=1;for(let i=1;i<9;i++){let x=w*i/9;c.beginPath();c.moveTo(x,0);c.lineTo(x,h);c.stroke()}for(let i=1;i<7;i++){let y=h*i/7;c.beginPath();c.moveTo(0,y);c.lineTo(w,y);c.stroke()}}
function drawCluster(){let {x:c,w,h}=setupCanvas($("clusterCanvas"));c.clearRect(0,0,w,h);grid(c,w,h);let ks=Object.keys(DATA.clusterCounts).filter(k=>Number(k)>=0);let max=Math.max(1,...ks.map(k=>DATA.clusterCounts[k]));let gap=w/Math.max(ks.length,1),bw=Math.min(70,gap*.55);ks.forEach((k,i)=>{let v=DATA.clusterCounts[k],bh=v/max*(h*.68),x=i*gap+(gap-bw)/2,y=h-bh-60;c.fillStyle=palette[i%palette.length];c.globalAlpha=.82;c.fillRect(x,y,bw,bh);c.globalAlpha=1;c.fillStyle="#d8e6ef";c.font="700 13px Segoe UI";c.textAlign="center";c.fillText("C"+k,x+bw/2,h-32);c.font="600 12px Segoe UI";c.fillText(String(v),x+bw/2,y-10)});c.textAlign="left";c.fillStyle="#8fa8bb";c.font="600 12px Segoe UI";c.fillText("OBSERVATIONS PER CLUSTER · CLICK A BAR TO INSPECT WORLDS",18,24)}
function projected(canvas){const pts=Array.isArray(DATA.points)?DATA.points:[];if(!pts.length)return[];let xs=pts.map(p=>Number(p.x)).filter(Number.isFinite),ys=pts.map(p=>Number(p.y)).filter(Number.isFinite);let minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);if(minX===maxX){minX-=1;maxX+=1}if(minY===maxY){minY-=1;maxY+=1}const pad=58,box=canvas.getBoundingClientRect(),w=Math.max(320,box.width),h=Math.max(360,box.height);return pts.map(p=>{let nx=(Number(p.x)-minX)/(maxX-minX),ny=(Number(p.y)-minY)/(maxY-minY);let bx=pad+nx*(w-pad*2),by=pad+(1-ny)*(h-pad*2);return{p,x:w/2+(bx-w/2)*zoom,y:h/2+(by-h/2)*zoom}})}
function drawPoints(id,lof){let canvas=$(id);if(!canvas)return;let{ x:c,w,h}=setupCanvas(canvas);c.clearRect(0,0,w,h);c.fillStyle="#050d16";c.fillRect(0,0,w,h);grid(c,w,h);const pts=projected(canvas);if(!pts.length){c.fillStyle="#a9bfd0";c.font="700 16px Segoe UI";c.fillText("UMAP DATA NOT AVAILABLE",24,36);return;}const normal=pts.filter(o=>!o.p.outlier);const selected=pts.filter(o=>o.p.outlier);normal.forEach(o=>{const p=o.p;c.fillStyle=palette[Math.max(0,p.cluster)%palette.length];c.globalAlpha=.72;c.beginPath();c.arc(o.x,o.y,3.0,0,Math.PI*2);c.fill();c.globalAlpha=1});selected.forEach(o=>{const p=o.p;c.fillStyle=lof?"#f2c66d":"#efb45f";c.beginPath();c.arc(o.x,o.y,5.2,0,Math.PI*2);c.fill();c.strokeStyle="#fff1c8";c.lineWidth=1;c.stroke()});
// Plot frame, axes and readable coordinate ticks make this a true 2-D scientific map.
c.strokeStyle="rgba(180,215,235,.28)";c.lineWidth=1;c.strokeRect(52,48,w-82,h-105);c.fillStyle="#8fa8bb";c.font="600 11px Segoe UI";c.textAlign="center";for(let i=0;i<=5;i++){let x=52+(w-82)*i/5;c.strokeStyle="rgba(170,205,235,.12)";c.beginPath();c.moveTo(x,48);c.lineTo(x,h-57);c.stroke();c.fillText(String(i),x,h-35)}c.textAlign="right";for(let i=0;i<=5;i++){let y=48+(h-105)*i/5;c.strokeStyle="rgba(170,205,235,.12)";c.beginPath();c.moveTo(52,y);c.lineTo(w-30,y);c.stroke();c.fillText(String(5-i),44,y+4)}c.textAlign="left";c.fillStyle="#c5d9e5";c.font="800 13px Segoe UI";c.fillText(lof?"LOF LOCAL-OUTLIER MAP":"UMAP EMBEDDING MAP",66,27);c.font="600 11px Segoe UI";c.fillStyle="#7f99aa";c.fillText(`${pts.length.toLocaleString()} observed worlds · click a point`,66,h-12)}
function draw(){if(active==="dbscan")drawCluster();if(active==="umap")drawPoints("umapCanvas",false);if(active==="lof")drawPoints("lofCanvas",true);if(active==="umap"||active==="lof")requestAnimationFrame(()=>{if(active==="umap")drawPoints("umapCanvas",false);if(active==="lof")drawPoints("lofCanvas",true);});}
function bindCanvas(id){$(id).addEventListener("click",function(e){let r=this.getBoundingClientRect(),mx=e.clientX-r.left,my=e.clientY-r.top,best=null,bd=22;projected(this).forEach(o=>{let d=Math.hypot(o.x-mx,o.y-my);if(d<bd){bd=d;best=o.p}});if(!best)return;const target=selectExoplanet(best.name,id==="umapCanvas"?"UMAP POINT":"LOF POINT");if(!target)return;const img=$(id==="umapCanvas"?"umapSelectedImage":"lofSelectedImage"),nm=$(id==="umapCanvas"?"umapSelectedName":"lofSelectedName"),meta=$(id==="umapCanvas"?"umapSelectedMeta":"lofSelectedMeta");if(img){img.src=DATA.exoplanetImage||"";img.classList.add("squareSelected")}if(nm)nm.textContent=target.name;if(meta)meta.textContent=(id==="umapCanvas"?"UMAP":"LOF")+" selected · DBSCAN "+(target.cluster===-1?"NOISE":"C"+target.cluster)+" · LOF "+fmt(target.lof,3);})}
function renderWorlds(){let arr=DATA.top||[];$("worldGrid").innerHTML=arr.slice(0,12).map((r,i)=>`<button type="button" class="world worldButton" data-world-name="${esc(r.name)}"><div class="kicker">CANDIDATE ${String(i+1).padStart(2,"0")}</div><h3>${esc(r.name)}</h3><div class="score">${fmt(r.score,3)}</div><div class="tag">LOF SCORE · DBSCAN ${r.cluster===-1?"NOISE":r.cluster}</div><div class="why">Radius: ${fmt(r.radius)} · Mass: ${fmt(r.mass)} · Temperature: ${fmt(r.temperature,0)} · Orbital period: ${fmt(r.period,2)} days</div><div class="worldAction">CLICK TO DISPLAY FULL OBSERVATION</div></button>`).join("");$("worldGrid").querySelectorAll("[data-world-name]").forEach(b=>b.addEventListener("click",()=>selectExoplanet(b.dataset.worldName,"UNUSUAL WORLD")));}
$("total").textContent=DATA.total.toLocaleString();$("clusters").textContent=DATA.clusters.toLocaleString();$("outliers").textContent=DATA.outliers.toLocaleString();$("normal").textContent=DATA.normal.toLocaleString();$("lofOut").textContent=DATA.outliers.toLocaleString();$("dPlanets").textContent=DATA.total.toLocaleString();$("dClusters").textContent=DATA.clusters.toLocaleString();$("dOutliers").textContent=DATA.outliers.toLocaleString();$("dataFile").textContent=DATA.dataFile;$("umapStatus").textContent=DATA.umapStatus;$("clusterText").textContent=DATA.clusters;
renderTable();
renderWorlds();
if((DATA.rows||[]).length)selectExoplanet(DATA.rows[0].name,"FIRST LISTED OBSERVATION");
$("total").textContent=DATA.total.toLocaleString();
$("clusters").textContent=DATA.clusters.toLocaleString();
$("outliers").textContent=DATA.outliers.toLocaleString();
$("normal").textContent=DATA.normal.toLocaleString();
$("lofOut").textContent=DATA.outliers.toLocaleString();
$("dPlanets").textContent=DATA.total.toLocaleString();
$("dClusters").textContent=DATA.clusters.toLocaleString();
$("dOutliers").textContent=DATA.outliers.toLocaleString();
$("dataFile").textContent=DATA.dataFile;
$("umapStatus").textContent=DATA.umapStatus;
$("clusterText").textContent=DATA.clusters;

$("openUMAP").addEventListener("click",()=>show("umap"));
$("openLOF").addEventListener("click",()=>show("lof"));
$("openWorlds").addEventListener("click",()=>show("worlds"));
$("zoomIn").addEventListener("click",()=>{zoom=Math.min(3,zoom+.25);draw()});
$("zoomOut").addEventListener("click",()=>{zoom=Math.max(.6,zoom-.25);draw()});
$("resetZoom").addEventListener("click",()=>{zoom=1;draw()});
$("clusterCanvas").addEventListener("click",function(e){const r=this.getBoundingClientRect(),mx=e.clientX-r.left;const ks=Object.keys(DATA.clusterCounts).filter(k=>Number(k)>=0);const gap=r.width/Math.max(ks.length,1),i=Math.floor(mx/gap);if(i<0||i>=ks.length)return;const k=ks[i];const rows=(DATA.rows||[]).filter(x=>Number(x.cluster)===Number(k));if(rows.length){const target=selectExoplanet(rows[0].name,"DBSCAN C"+k);if(target){const panel=$("selectionDockBody");if(panel)panel.innerHTML=`<b>DBSCAN C${esc(k)}</b> · ${rows.length} observations · first listed world: <b>${esc(target.name)}</b> · click another point or open NASA DATA for the full table.`;}}});
bindCanvas("umapCanvas");
bindCanvas("lofCanvas");
window.addEventListener("resize",()=>{draw();resizeThree();}); if(window.ResizeObserver){const ro=new ResizeObserver(()=>{resizeThree();if(active==="umap")drawPoints("umapCanvas",false);if(active==="lof")drawPoints("lofCanvas",true);});const st=$("solarStage"),uc=$("umapCanvas"),lc=$("lofCanvas");if(st)ro.observe(st);if(uc)ro.observe(uc.parentElement);if(lc)ro.observe(lc.parentElement);}
renderSolar();
$("moonModalClose").addEventListener("click",()=>$("moonModal").classList.remove("open"));
$("moonModal").addEventListener("click",e=>{if(e.target===$("moonModal"))$("moonModal").classList.remove("open");});
show("data");
initThreeSolar();

})();
</script>
</body></html>
"""
    html = html.replace(
        "__DATA__",
        data_json
    )
    html = html.replace(
        "__SOLAR__",
        solar_json
    )
    html = html.replace(
        "__SUN__",
        load_asset("sun.jpg")
    )
    html = html.replace(
        "__EXOPLANET_IMAGE__",
        exoplanet_image
    )
    html = html.replace("__MOON__", load_asset("moon_texture.jpg"))
    html = html.replace("__IO__", load_asset("io.jpg"))
    html = html.replace("__EUROPA__", load_asset("europa.jpg"))
    html = html.replace("__GANYMEDE__", load_asset("ganymede.jpg"))
    html = html.replace("__CALLISTO__", load_asset("callisto.jpg"))

    components.html(
        html,
        height=1400,
        scrolling=True
    )


# Compatibility with the spelling used in the existing project.
def show_scence5():
    show_scene5()
