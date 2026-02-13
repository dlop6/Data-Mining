"""Genera figuras con formato listo para informe usando los resultados de Q1-Q5."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_TABLES = BASE_DIR / "output" / "tables"
OUTPUT_FIGURES = BASE_DIR / "output" / "figures"
REPORT_FIG_DIR = OUTPUT_FIGURES / "report_ready"
REPORT_FIG_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid", context="talk")

DEPREG_TO_NOMBRE = {
    1: "Guatemala",
    2: "El Progreso",
    3: "Sacatepéquez",
    4: "Chimaltenango",
    5: "Escuintla",
    6: "Santa Rosa",
    7: "Sololá",
    8: "Totonicapán",
    9: "Quetzaltenango",
    10: "Suchitepéquez",
    11: "Retalhuleu",
    12: "San Marcos",
    13: "Huehuetenango",
    14: "Quiché",
    15: "Baja Verapaz",
    16: "Alta Verapaz",
    17: "Petén",
    18: "Izabal",
    19: "Zacapa",
    20: "Chiquimula",
    21: "Jalapa",
    22: "Jutiapa",
}


def format_dep_label(code: int) -> str:
    return f"{int(code):02d} - {DEPREG_TO_NOMBRE.get(int(code), 'Desconocido')}"


def preparar_panel_departamental(nac_df: pd.DataFrame, def_df: pd.DataFrame) -> pd.DataFrame:
    """Replica el panel departamental usado en el notebook."""
    nac = nac_df.copy()
    defun = def_df.copy()

    for column in ("año", "depreg"):
        nac[column] = pd.to_numeric(nac[column], errors="coerce")
        defun[column] = pd.to_numeric(defun[column], errors="coerce")
    defun["edadif"] = pd.to_numeric(defun["edadif"], errors="coerce")

    nac = nac.dropna(subset=["año", "depreg"])
    defun = defun.dropna(subset=["año", "depreg", "edadif"])

    nac[["año", "depreg"]] = nac[["año", "depreg"]].astype(int)
    defun[["año", "depreg"]] = defun[["año", "depreg"]].astype(int)

    panel_nac = nac.groupby(["año", "depreg"]).size().rename("nacimientos").reset_index()
    panel_def = (
        defun[defun["edadif"] < 1]
        .groupby(["año", "depreg"]).size()
        .rename("defunciones_infantiles")
        .reset_index()
    )

    panel = panel_nac.merge(panel_def, on=["año", "depreg"], how="left")
    panel["defunciones_infantiles"] = panel["defunciones_infantiles"].fillna(0).astype(int)
    panel["tasa_mortalidad_infantil_x1000"] = (
        panel["defunciones_infantiles"] / panel["nacimientos"]
    ) * 1000
    return panel


def register_fig(fig: plt.Figure, filename: str) -> Path:
    path = REPORT_FIG_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def main() -> None:
    nac_df = pd.read_csv(BASE_DIR / "data" / "processed" / "nacimientos_clean_2009_2022.csv")
    def_df = pd.read_csv(BASE_DIR / "data" / "processed" / "defunciones_clean_2009_2022.csv")

    panel_departamental = preparar_panel_departamental(nac_df, def_df)

    # Ilustración 1: Tendencia Q1
    q1_df = pd.read_csv(OUTPUT_TABLES / "q1_mortalidad_infantil_anual_2009_2022.csv")
    x = q1_df["año"].astype(float).to_numpy()
    y = q1_df["tasa_mortalidad_infantil_x1000"].astype(float).to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    trend = slope * x + intercept
    ss_res = np.sum((y - trend) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - (ss_res / ss_tot)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(q1_df["año"], y, marker="o", linewidth=2.4, label="Tasa observada")
    ax.plot(q1_df["año"], trend, linestyle="--", linewidth=2.2, label=f"Tendencia lineal (R²={r2:.3f})")
    ax.set_title("Tendencia de mortalidad infantil en Guatemala, 2009-2022")
    ax.set_xlabel("Año")
    ax.set_ylabel("Defunciones infantiles por cada 1,000 nacimientos")
    ax.legend()
    ax.grid(alpha=0.3)
    register_fig(fig, "fig01_q1_tendencia.png")

    # Ilustración 2: Barras departamentales Q2
    dep_periodo = (
        panel_departamental
        .groupby("depreg", as_index=False)[["nacimientos", "defunciones_infantiles"]]
        .sum()
    )
    dep_periodo["tasa"] = (dep_periodo["defunciones_infantiles"] / dep_periodo["nacimientos"]) * 1000
    dep_periodo["dep_label"] = dep_periodo["depreg"].apply(format_dep_label)
    dep_sorted = dep_periodo.sort_values("tasa")
    fig, ax = plt.subplots(figsize=(12, 9))
    sns.barplot(data=dep_sorted, x="tasa", y="dep_label", palette="YlOrRd", ax=ax)
    ax.set_title("Tasa acumulada de mortalidad infantil por departamento (2009-2022)")
    ax.set_xlabel("Defunciones infantiles por cada 1,000 nacimientos")
    ax.set_ylabel("Departamento")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.2f"))
    register_fig(fig, "fig02_q2_tasa_departamentos.png")

    # Ilustración 3: Heatmap departamental Q2
    dep_order = [format_dep_label(dep) for dep in sorted(DEPREG_TO_NOMBRE.keys())]
    heat_data = (
        panel_departamental
        .assign(dep_label=lambda d: d["depreg"].apply(format_dep_label))
        .pivot_table(index="dep_label", columns="año", values="tasa_mortalidad_infantil_x1000", aggfunc="mean")
        .reindex(dep_order)
    )
    fig, ax = plt.subplots(figsize=(13, 10))
    sns.heatmap(heat_data, cmap="YlOrRd", linewidths=0.3, linecolor="white", cbar_kws={"label": "Tasa x1,000"}, ax=ax)
    ax.set_title("Evolución anual de la tasa por departamento (2009-2022)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Departamento")
    register_fig(fig, "fig03_q2_heatmap_departamentos.png")

    # Ilustración 4: Heatmap mensual Q3
    panel_mensual = pd.read_csv(OUTPUT_TABLES / "q3_mortalidad_infantil_mensual_2009_2022.csv")
    meses_order = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    heat_month = (
        panel_mensual
        .pivot_table(index="mes_nombre", columns="año", values="tasa_mortalidad_infantil_x1000", aggfunc="mean")
        .reindex(meses_order)
    )
    fig, ax = plt.subplots(figsize=(13, 5))
    sns.heatmap(heat_month, cmap="Reds", linewidths=0.25, linecolor="white", cbar_kws={"label": "Tasa x1,000"}, ax=ax)
    ax.set_title("Tasa mensual de mortalidad infantil (2009-2022)")
    ax.set_xlabel("Año")
    ax.set_ylabel("Mes")
    register_fig(fig, "fig04_q3_heatmap_mensual.png")

    # Ilustración 5: Perfil estacional Q3
    resumen_meses = pd.read_csv(OUTPUT_TABLES / "q3_resumen_estacional.csv")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(resumen_meses["mes_nombre"], resumen_meses["tasa_promedio"], marker="o", linewidth=2.4, color="#D32F2F")
    ax.fill_between(
        resumen_meses["mes_nombre"],
        resumen_meses["tasa_promedio"] - resumen_meses["tasa_std"].fillna(0),
        resumen_meses["tasa_promedio"] + resumen_meses["tasa_std"].fillna(0),
        alpha=0.2,
        color="#F28F8F",
    )
    ax.set_title("Perfil estacional promedio de mortalidad infantil")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Tasa por cada 1,000 nacimientos")
    register_fig(fig, "fig05_q3_perfil_estacional.png")

    # Ilustraciones 6 y 7: Variables demográficas Q4
    q4_df = pd.read_csv(OUTPUT_TABLES / "q4_tasas_demograficas.csv")
    area_df = q4_df[q4_df["variable"] == "areag"].copy()
    area_labels = {"1.0": "Área urbana", "2.0": "Área rural", "9.0": "Sin dato"}
    area_df["categoria_label"] = area_df["categoria"].astype(str).map(area_labels).fillna(area_df["categoria"].astype(str))
    area_df = area_df.sort_values("tasa_mortalidad_infantil_x1000", ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=area_df, x="categoria_label", y="tasa_mortalidad_infantil_x1000", palette="viridis", ax=ax)
    ax.set_title("Tasa de mortalidad infantil por área geográfica")
    ax.set_xlabel("Categoría")
    ax.set_ylabel("Tasa por cada 1,000 nacimientos")
    register_fig(fig, "fig06_q4_area_geografica.png")

    sexo_df = q4_df[q4_df["variable"] == "sexo"].copy()
    sexo_labels = {"1.0": "Niños", "2.0": "Niñas"}
    sexo_df["categoria_label"] = sexo_df["categoria"].astype(str).map(sexo_labels).fillna(sexo_df["categoria"].astype(str))
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=sexo_df, x="categoria_label", y="tasa_mortalidad_infantil_x1000", palette="magma", ax=ax)
    ax.set_title("Tasa de mortalidad infantil por sexo")
    ax.set_xlabel("Sexo")
    ax.set_ylabel("Tasa por cada 1,000 nacimientos")
    register_fig(fig, "fig07_q4_sexo.png")

    # Ilustraciones 8 y 9: Clustering Q5
    clusters_df = pd.read_csv(OUTPUT_TABLES / "q5_clusters_departamentos.csv")
    cluster_labels = pd.read_csv(OUTPUT_TABLES / "q5_cluster_summary.csv")
    label_map = dict(zip(cluster_labels["cluster"], cluster_labels["cluster_label"]))
    clusters_df["cluster_label"] = clusters_df["cluster"].map(label_map)

    fig, ax = plt.subplots(figsize=(11, 7))
    sns.scatterplot(
        data=clusters_df,
        x="media_tasa",
        y="pendiente_tendencia",
        hue="cluster_label",
        style="cluster_label",
        s=150,
        palette="tab10",
        ax=ax,
    )
    for _, row in clusters_df.iterrows():
        ax.text(row["media_tasa"] + 0.01, row["pendiente_tendencia"] + 0.002, int(row["depreg"]), fontsize=9)
    ax.set_title("Clusters departamentales según nivel y tendencia de mortalidad infantil")
    ax.set_xlabel("Tasa promedio por cada 1,000 (2009-2022)")
    ax.set_ylabel("Pendiente de la tendencia anual")
    ax.legend(title="Cluster")
    register_fig(fig, "fig08_q5_dispersion_clusters.png")

    sil_df = pd.read_csv(OUTPUT_TABLES / "q5_silhouette_scores.csv")
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=sil_df, x="k", y="silhouette", palette="Blues_d", ax=ax)
    ax.set_title("Evaluación de número de clusters (coeficiente de silueta)")
    ax.set_xlabel("Número de clusters (k)")
    ax.set_ylabel("Coeficiente de silueta promedio")
    ax.set_ylim(0, 0.6)
    register_fig(fig, "fig09_q5_silueta.png")

    summary = pd.DataFrame(sorted(REPORT_FIG_DIR.iterdir()))
    print("Se generaron", len(summary), "figuras en", REPORT_FIG_DIR)


if __name__ == "__main__":
    main()
