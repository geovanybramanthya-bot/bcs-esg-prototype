"""Mesin contextual BWM dan reference-anchored cohort TOPSIS ESG-BCS.

Seluruh penilaian ahli, profil acuan, dan ambang status pada modul ini adalah
asumsi proof-of-concept berbasis data simulasi. Hasilnya hanya memprioritaskan
tinjauan analis dan tidak menghasilkan persetujuan atau penolakan otomatis.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
from scipy.optimize import linprog


CREDIT_CRITERIA = ("Character", "Capacity", "Capital", "Condition", "Collateral")
ESG_CRITERIA = ("Environmental", "Social", "Governance")
ALL_CRITERIA = CREDIT_CRITERIA + ESG_CRITERIA
CONFIG_PATH = Path(__file__).with_name("bwm_profiles.json")


def classify_pathway(debtor):
    """Turunkan jalur secara transparan dari empat kelompok ketersediaan data."""
    available = sum(bool(v) for v in debtor["data_availability"].values())
    return available < 2, available


def load_bwm_config(path: Path | str = CONFIG_PATH):
    """Muat penilaian ahli yang berversi dan terpisah dari logika program."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def solve_bwm(criteria, best, worst, best_to_others, others_to_worst):
    """Selesaikan model linear Best-Worst Method.

    Model meminimalkan deviasi maksimum xi pada dua kelompok kendala:
    |w_best - a_best,j w_j| <= xi dan |w_j - a_j,worst w_worst| <= xi.
    """
    criteria = tuple(criteria)
    n = len(criteria)
    if n < 2 or len(best_to_others) != n or len(others_to_worst) != n:
        raise ValueError("Konfigurasi BWM harus memiliki panjang yang sama dengan kriteria.")
    if best not in criteria or worst not in criteria or best == worst:
        raise ValueError("Kriteria best dan worst harus berbeda dan terdaftar.")

    bto = np.asarray(best_to_others, dtype=float)
    otw = np.asarray(others_to_worst, dtype=float)
    if np.any((bto < 1) | (bto > 9)) or np.any((otw < 1) | (otw > 9)):
        raise ValueError("Nilai perbandingan BWM harus berada pada skala 1 sampai 9.")

    best_idx = criteria.index(best)
    worst_idx = criteria.index(worst)
    if not np.isclose(bto[best_idx], 1) or not np.isclose(otw[worst_idx], 1):
        raise ValueError("Perbandingan kriteria terhadap dirinya sendiri harus bernilai 1.")

    # Variabel keputusan: w_1 ... w_n, xi.
    a_ub, b_ub = [], []
    for j in range(n):
        row = np.zeros(n + 1)
        row[best_idx] += 1.0
        row[j] -= bto[j]
        row[-1] = -1.0
        a_ub.append(row)
        b_ub.append(0.0)
        a_ub.append(-row)
        a_ub[-1][-1] = -1.0
        b_ub.append(0.0)

        row = np.zeros(n + 1)
        row[j] += 1.0
        row[worst_idx] -= otw[j]
        row[-1] = -1.0
        a_ub.append(row)
        b_ub.append(0.0)
        a_ub.append(-row)
        a_ub[-1][-1] = -1.0
        b_ub.append(0.0)

    objective = np.zeros(n + 1)
    objective[-1] = 1.0
    equality = np.zeros((1, n + 1))
    equality[0, :n] = 1.0
    result = linprog(
        objective,
        A_ub=np.asarray(a_ub),
        b_ub=np.asarray(b_ub),
        A_eq=equality,
        b_eq=np.array([1.0]),
        bounds=[(0.0, 1.0)] * n + [(0.0, None)],
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"Optimasi BWM gagal: {result.message}")

    weights = np.clip(result.x[:n], 0.0, 1.0)
    weights /= weights.sum()
    return {
        "criteria": criteria,
        "best": best,
        "worst": worst,
        "weights": weights,
        "xi": float(result.x[-1]),
    }


def derive_contextual_weights(is_data_thin, config=None):
    """Turunkan bobot hierarkis BWM untuk jalur data-thin atau data-rich."""
    config = config or load_bwm_config()
    profile_key = "data_thin" if is_data_thin else "data_rich"
    profile = config["profiles"][profile_key]

    solved = {}
    for layer in ("top_level", "credit", "esg"):
        item = profile[layer]
        solved[layer] = solve_bwm(
            item["criteria"], item["best"], item["worst"],
            item["best_to_others"], item["others_to_worst"],
        )

    top = solved["top_level"]["weights"]
    credit = solved["credit"]["weights"]
    esg = solved["esg"]["weights"]
    global_weights = np.concatenate((top[0] * credit, top[1] * esg))
    global_weights /= global_weights.sum()
    return {
        "profile": profile_key,
        "version": config["version"],
        "top_weights": top,
        "credit_weights": credit,
        "esg_weights": esg,
        "global_weights": global_weights,
        "best_worst": {
            layer: {"best": solved[layer]["best"], "worst": solved[layer]["worst"]}
            for layer in solved
        },
        "xi": {layer: solved[layer]["xi"] for layer in solved},
    }


def calculate_environmental_score(debtor):
    """Ubah indikator risiko geospasial menjadi skor manfaat 0 sampai 100."""
    geo = debtor["geo"]
    if debtor["activity_type"] == "agri":
        if geo["claim_match"]:
            ndvi_consistency = min(max(geo["ndvi"] / 0.70 * 100, 0), 100)
        else:
            ndvi_consistency = min(geo["ndvi"] / 0.50 * 100, 35)
    else:
        ndvi_consistency = 100 if geo["claim_match"] else 35

    land_fit = {"agri": 90, "urban": 85, "mixed": 85, "empty": 15}.get(
        geo["land_class"], 50
    )
    if not geo["claim_match"]:
        land_fit = min(land_fit, 10)

    protected = 100 if geo.get("protected_zone_ok", True) else 20
    components = {
        "Konsistensi NDVI": round(ndvi_consistency, 1),
        "Ketahanan banjir": float(geo["flood_score"]),
        "Kesesuaian lahan": float(land_fit),
        "Kepatuhan zona lindung": float(protected),
    }
    return round(sum(components.values()) / len(components), 1), components


def debtor_criteria(debtor):
    environmental, detail = calculate_environmental_score(debtor)
    values = np.asarray(
        list(debtor["5C"]) + [environmental, debtor["ESG"][1], debtor["ESG"][2]],
        dtype=float,
    )
    return np.clip(values, 0.0, 100.0), detail


def reference_anchored_topsis(matrix, weights, lower=None, upper=None):
    """TOPSIS dengan cohort tetap dan dua profil acuan kebijakan.

    Semua kolom harus sudah berupa benefit score. Profil acuan 0 dan 100
    menjaga perhitungan tetap terdefinisi ketika cohort masih sangat kecil.
    """
    matrix = np.asarray(matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] < 1:
        raise ValueError("Matriks TOPSIS harus berisi minimal satu alternatif.")
    weights = np.asarray(weights, dtype=float)
    if matrix.shape[1] != len(weights) or np.any(weights < 0):
        raise ValueError("Bobot TOPSIS tidak sesuai dengan jumlah kriteria.")
    if not np.isclose(weights.sum(), 1.0):
        weights = weights / weights.sum()

    lower = np.zeros(matrix.shape[1]) if lower is None else np.asarray(lower, dtype=float)
    upper = np.full(matrix.shape[1], 100.0) if upper is None else np.asarray(upper, dtype=float)
    if lower.shape != upper.shape or lower.shape[0] != matrix.shape[1] or np.any(lower >= upper):
        raise ValueError("Profil acuan bawah dan atas tidak valid.")
    if np.any(matrix < lower) or np.any(matrix > upper):
        raise ValueError("Nilai alternatif berada di luar profil acuan.")

    augmented = np.vstack((matrix, lower, upper))
    denominator = np.linalg.norm(augmented, axis=0)
    denominator = np.where(denominator == 0.0, 1.0, denominator)
    normalized = augmented / denominator
    weighted = normalized * weights
    negative_ideal = weighted[-2]
    positive_ideal = weighted[-1]
    distance_positive = np.linalg.norm(weighted - positive_ideal, axis=1)
    distance_negative = np.linalg.norm(weighted - negative_ideal, axis=1)
    total_distance = distance_positive + distance_negative
    closeness = np.divide(
        distance_negative,
        total_distance,
        out=np.zeros_like(distance_negative),
        where=total_distance > 0,
    )
    n = matrix.shape[0]
    return {
        "scores": np.round(closeness[:n], 4),
        "distance_positive": distance_positive[:n],
        "distance_negative": distance_negative[:n],
        "normalized": normalized[:n],
        "weighted": weighted[:n],
        "anchor_scores": (float(closeness[-2]), float(closeness[-1])),
    }


def score_debtor_cohort(debtors: Mapping[str, Mapping]):
    """Nilai semua debitur dalam cohort jalur yang sebanding."""
    if not debtors:
        raise ValueError("Cohort debitur tidak boleh kosong.")

    prepared = {}
    groups = {True: [], False: []}
    for debtor_id, debtor in debtors.items():
        is_thin, available = classify_pathway(debtor)
        criteria, environmental_detail = debtor_criteria(debtor)
        prepared[debtor_id] = {
            "thin": is_thin,
            "data_available": available,
            "criteria": criteria,
            "environmental_components": environmental_detail,
        }
        groups[is_thin].append(debtor_id)

    output = {}
    for is_thin, ids in groups.items():
        if not ids:
            continue
        bwm = derive_contextual_weights(is_thin)
        matrix = np.vstack([prepared[debtor_id]["criteria"] for debtor_id in ids])
        credit_result = reference_anchored_topsis(matrix[:, :5], bwm["credit_weights"])
        esg_result = reference_anchored_topsis(matrix[:, 5:], bwm["esg_weights"])
        final_result = reference_anchored_topsis(matrix, bwm["global_weights"])
        ranks = np.empty(len(ids), dtype=int)
        order = np.argsort(-final_result["scores"], kind="stable")
        ranks[order] = np.arange(1, len(ids) + 1)

        for i, debtor_id in enumerate(ids):
            raw = prepared[debtor_id]
            output[debtor_id] = {
                "thin": is_thin,
                "data_available": raw["data_available"],
                "criteria": raw["criteria"],
                "normalized_5c": credit_result["normalized"][i],
                "weighted_5c": credit_result["weighted"][i],
                "normalized_global": final_result["normalized"][i],
                "weighted_global": final_result["weighted"][i],
                "wv": bwm["credit_weights"],
                "esg_weights": bwm["esg_weights"],
                "global_weights": bwm["global_weights"],
                "top_weights": bwm["top_weights"],
                "bwm_profile": bwm["profile"],
                "bwm_version": bwm["version"],
                "bwm_best_worst": bwm["best_worst"],
                "bwm_xi": bwm["xi"],
                "vi": float(credit_result["scores"][i]),
                "esg": float(esg_result["scores"][i]),
                "fcs": float(final_result["scores"][i]),
                "distance_positive": float(final_result["distance_positive"][i]),
                "distance_negative": float(final_result["distance_negative"][i]),
                "rank": int(ranks[i]),
                "cohort_size": len(ids),
                "environmental_components": raw["environmental_components"],
                "esg_values": raw["criteria"][5:].tolist(),
            }
    return output


def review_status(final_score):
    """Label antrean tinjauan, bukan keputusan persetujuan kredit."""
    if final_score >= 0.70:
        return "priority", "PRIORITAS EVALUASI"
    if final_score >= 0.50:
        return "review", "TINJAUAN LANJUTAN"
    return "manual", "RISIKO TINGGI, TINJAUAN MANUAL"


def sensitivity_grid(matrix, weights, index):
    """Uji dampak perubahan bobot plus/minus 10 persen pada setiap kriteria."""
    matrix = np.asarray(matrix, dtype=float)
    weights = np.asarray(weights, dtype=float)
    baseline = float(reference_anchored_topsis(matrix, weights)["scores"][index])
    rows = []
    for j, criterion in enumerate(range(matrix.shape[1])):
        for factor in (0.9, 1.1):
            adjusted = weights.copy()
            adjusted[j] *= factor
            adjusted /= adjusted.sum()
            score = float(reference_anchored_topsis(matrix, adjusted)["scores"][index])
            rows.append({"criterion": criterion, "factor": factor, "score": score, "delta": round(score - baseline, 4)})
    return rows
