"""
Author Style Operations — Layer 2 (Deterministic, 0 Tokens)

Interpolation, distance computation, vocabulary extraction, and
prompt generation from author style coordinates.

All operations are pure computation — no LLM calls.
"""

import json
import math
from typing import Optional

from author_style_taxonomy import (
    AUTHOR_CATALOG,
    DIMENSIONS,
    PARAMETER_NAMES,
    AuthorCoordinates,
    get_coordinates,
)


# ---------------------------------------------------------------------------
# Distance computation
# ---------------------------------------------------------------------------

def compute_style_distance(
    author_id_1: str,
    author_id_2: str,
    weighted: bool = False,
) -> dict:
    """
    Compute Euclidean distance between two authors in style-space.

    Args:
        author_id_1: First author ID
        author_id_2: Second author ID
        weighted: If True, weight perceptually salient dimensions higher

    Returns:
        dict with total distance, per-dimension breakdown, and max-contrast axis
    """
    c1 = get_coordinates(author_id_1)
    c2 = get_coordinates(author_id_2)

    # Perceptual weights — some dimensions contribute more to
    # perceived style difference. These are tunable.
    PERCEPTUAL_WEIGHTS = {
        "syntactic_density":    1.2,
        "sensory_concreteness": 1.0,
        "ornamental_register":  1.1,
        "tension_visibility":   0.9,
        "tension_temporality":  0.8,
        "reality_stability":    1.0,
        "interiority":          1.0,
        "temporal_mode":        0.8,
    }

    per_dim = {}
    sum_sq = 0.0

    for p in PARAMETER_NAMES:
        diff = c2[p] - c1[p]
        w = PERCEPTUAL_WEIGHTS[p] if weighted else 1.0
        weighted_diff = diff * w
        per_dim[p] = {
            "value_1": c1[p],
            "value_2": c2[p],
            "raw_difference": round(diff, 3),
            "weighted_difference": round(weighted_diff, 3),
            "absolute_gap": round(abs(diff), 3),
        }
        sum_sq += weighted_diff ** 2

    total = math.sqrt(sum_sq)

    # Find max-contrast axis
    max_axis = max(per_dim, key=lambda k: per_dim[k]["absolute_gap"])

    return {
        "author_1": AUTHOR_CATALOG[author_id_1]["display_name"],
        "author_2": AUTHOR_CATALOG[author_id_2]["display_name"],
        "euclidean_distance": round(total, 4),
        "normalized_distance": round(total / math.sqrt(len(PARAMETER_NAMES)), 4),
        "max_contrast_axis": max_axis,
        "max_contrast_gap": per_dim[max_axis]["absolute_gap"],
        "per_dimension": per_dim,
    }


# ---------------------------------------------------------------------------
# Interpolation (blending)
# ---------------------------------------------------------------------------

def interpolate_styles(
    blend_spec: dict[str, float],
) -> dict:
    """
    Blend multiple author styles by weighted interpolation.

    Args:
        blend_spec: Mapping of author_id -> weight (0.0-1.0).
                    Weights are normalized to sum to 1.0.

    Returns:
        dict with blended coordinates, nearest author, and output vocabularies

    Example:
        interpolate_styles({"hemingway": 0.7, "borges": 0.3})
    """
    if not blend_spec:
        raise ValueError("blend_spec must contain at least one author")

    # Normalize weights
    total_weight = sum(blend_spec.values())
    if total_weight <= 0:
        raise ValueError("Weights must sum to a positive value")

    normalized = {k: v / total_weight for k, v in blend_spec.items()}

    # Compute blended coordinates
    blended: dict[str, float] = {}
    for p in PARAMETER_NAMES:
        val = 0.0
        for author_id, weight in normalized.items():
            coords = get_coordinates(author_id)
            val += coords[p] * weight
        blended[p] = round(val, 4)

    # Find nearest catalog author to blended point
    min_dist = float("inf")
    nearest = None
    for aid in AUTHOR_CATALOG:
        coords = get_coordinates(aid)
        dist = math.sqrt(sum(
            (blended[p] - coords[p]) ** 2 for p in PARAMETER_NAMES
        ))
        if dist < min_dist:
            min_dist = dist
            nearest = aid

    # Extract output vocabularies for blended state
    text_output = _extract_text_vocabulary(blended)
    image_output = _extract_image_vocabulary(blended)

    # Blend signature moves from contributing authors
    blended_moves = []
    for author_id, weight in sorted(normalized.items(),
                                     key=lambda x: -x[1]):
        entry = AUTHOR_CATALOG[author_id]
        n_moves = max(1, round(weight * 5))
        blended_moves.extend(entry["signature_moves"][:n_moves])

    return {
        "blend_spec": {
            aid: round(w, 3) for aid, w in normalized.items()
        },
        "blend_display": " / ".join(
            f"{round(w * 100)}% {AUTHOR_CATALOG[aid]['display_name']}"
            for aid, w in sorted(normalized.items(), key=lambda x: -x[1])
        ),
        "coordinates": blended,
        "nearest_catalog_author": {
            "id": nearest,
            "display_name": AUTHOR_CATALOG[nearest]["display_name"],
            "distance": round(min_dist, 4),
        },
        "signature_moves": blended_moves,
        "text_vocabulary": text_output,
        "image_vocabulary": image_output,
    }


# ---------------------------------------------------------------------------
# Vocabulary extraction
# ---------------------------------------------------------------------------

def _get_tier(value: float) -> str:
    """Map a 0-1 value to low/mid/high tier."""
    if value < 0.33:
        return "low"
    elif value < 0.67:
        return "mid"
    else:
        return "high"


def _interpolate_tier_vocabularies(
    dim_id: str,
    value: float,
    output_type: str,  # "text_output_mapping" or "image_output_mapping"
) -> dict:
    """
    For values near tier boundaries, blend adjacent tier vocabularies.
    Returns the primary tier's vocabulary with boundary proximity info.
    """
    dim = DIMENSIONS[dim_id]
    tier = _get_tier(value)
    result = dict(dim[output_type][tier])
    result["_dimension"] = dim_id
    result["_value"] = round(value, 3)
    result["_tier"] = tier

    # Boundary proximity — useful for Layer 3 to modulate intensity
    if value < 0.33:
        result["_boundary_proximity"] = round(value / 0.33, 3)
    elif value < 0.67:
        result["_boundary_proximity"] = round((value - 0.33) / 0.34, 3)
    else:
        result["_boundary_proximity"] = round((value - 0.67) / 0.33, 3)

    return result


def _extract_text_vocabulary(coordinates: dict[str, float]) -> dict:
    """Extract complete text generation vocabulary from coordinates."""
    result = {}
    for dim_id in PARAMETER_NAMES:
        result[dim_id] = _interpolate_tier_vocabularies(
            dim_id, coordinates[dim_id], "text_output_mapping"
        )
    return result


def _extract_image_vocabulary(coordinates: dict[str, float]) -> dict:
    """Extract complete image generation vocabulary from coordinates."""
    result = {}
    for dim_id in PARAMETER_NAMES:
        result[dim_id] = _interpolate_tier_vocabularies(
            dim_id, coordinates[dim_id], "image_output_mapping"
        )
    return result


# ---------------------------------------------------------------------------
# Prompt generation
# ---------------------------------------------------------------------------

def generate_text_prompt(
    author_id: Optional[str] = None,
    blend_spec: Optional[dict[str, float]] = None,
    custom_coordinates: Optional[dict[str, float]] = None,
) -> dict:
    """
    Generate text-generation-ready style directives.

    Provide exactly one of: author_id, blend_spec, or custom_coordinates.

    Returns:
        dict with structured directives and a composited prompt string
    """
    if author_id:
        coords = get_coordinates(author_id)
        entry = AUTHOR_CATALOG[author_id]
        source_label = entry["display_name"]
        text_vocab = entry["text_vocabulary"]
        sig_moves = entry["signature_moves"]
    elif blend_spec:
        result = interpolate_styles(blend_spec)
        coords = result["coordinates"]
        source_label = result["blend_display"]
        text_vocab = {}  # Blended — use dimension extraction
        sig_moves = result["signature_moves"]
    elif custom_coordinates:
        coords = custom_coordinates
        source_label = "Custom coordinates"
        text_vocab = {}
        sig_moves = []
    else:
        raise ValueError("Provide author_id, blend_spec, or custom_coordinates")

    # Extract per-dimension directives
    dim_directives = _extract_text_vocabulary(coords)

    # Compose master directive string
    directive_parts = []
    for dim_id in PARAMETER_NAMES:
        tier_data = dim_directives[dim_id]
        # Find the *_directive key
        for k, v in tier_data.items():
            if k.endswith("_directive") and isinstance(v, str):
                directive_parts.append(v)

    master_directive = " ".join(directive_parts)

    # Add signature moves if available
    moves_text = ""
    if sig_moves:
        moves_text = "Key techniques: " + "; ".join(sig_moves[:5]) + "."

    # Add author-specific vocabulary if available
    vocab_text = ""
    if text_vocab:
        if "register" in text_vocab:
            vocab_text += f"Register: {text_vocab['register']}. "
        if "paragraph_rhythm" in text_vocab:
            vocab_text += f"Paragraph rhythm: {text_vocab['paragraph_rhythm']}. "
        if "forbidden" in text_vocab:
            vocab_text += f"Avoid these words: {', '.join(text_vocab['forbidden'])}. "

    return {
        "source": source_label,
        "coordinates": coords,
        "master_directive": master_directive,
        "signature_moves": moves_text,
        "vocabulary_constraints": vocab_text,
        "full_prompt": f"[Style: {source_label}] {master_directive} {moves_text} {vocab_text}".strip(),
        "per_dimension_directives": dim_directives,
    }


def generate_image_prompt(
    author_id: Optional[str] = None,
    blend_spec: Optional[dict[str, float]] = None,
    custom_coordinates: Optional[dict[str, float]] = None,
    style_modifier: str = "",
) -> dict:
    """
    Generate image-generation-ready visual directives.

    Provide exactly one of: author_id, blend_spec, or custom_coordinates.

    Returns:
        dict with keywords, compositional rules, and a composited prompt string
    """
    if author_id:
        coords = get_coordinates(author_id)
        entry = AUTHOR_CATALOG[author_id]
        source_label = entry["display_name"]
        img_vocab = entry["image_vocabulary"]
    elif blend_spec:
        result = interpolate_styles(blend_spec)
        coords = result["coordinates"]
        source_label = result["blend_display"]
        img_vocab = result["image_vocabulary"]
    elif custom_coordinates:
        coords = custom_coordinates
        source_label = "Custom coordinates"
        img_vocab = {"keywords": [], "color_palette": [], "compositional_rules": []}
    else:
        raise ValueError("Provide author_id, blend_spec, or custom_coordinates")

    # Extract per-dimension visual directives
    dim_visuals = _extract_image_vocabulary(coords)

    # Collect all visual directives
    visual_directive_parts = []
    for dim_id in PARAMETER_NAMES:
        tier_data = dim_visuals[dim_id]
        for k, v in tier_data.items():
            if k.endswith("_directive") and isinstance(v, str):
                visual_directive_parts.append(v)

    # Compose keyword list from author vocabulary + dimension extraction
    all_keywords = list(img_vocab.get("keywords", []))

    # Compose color palette
    colors = img_vocab.get("color_palette", [])

    # Compose compositional rules
    rules = img_vocab.get("compositional_rules", [])

    # Build the master prompt
    prompt_parts = []
    if style_modifier:
        prompt_parts.append(style_modifier)
    prompt_parts.extend(all_keywords[:8])
    if colors:
        prompt_parts.append(f"color palette: {', '.join(colors[:4])}")
    prompt_parts.extend(visual_directive_parts[:6])

    master_prompt = ", ".join(prompt_parts)

    return {
        "source": source_label,
        "coordinates": coords,
        "prompt": master_prompt,
        "keywords": all_keywords,
        "color_palette": colors,
        "compositional_rules": rules,
        "per_dimension_visuals": dim_visuals,
    }


# ---------------------------------------------------------------------------
# Catalog queries
# ---------------------------------------------------------------------------

def list_authors() -> dict:
    """List all available author styles with display names and origins."""
    return {
        aid: {
            "display_name": entry["display_name"],
            "language_origin": entry["language_origin"],
            "coordinates": entry["coordinates"],
        }
        for aid, entry in AUTHOR_CATALOG.items()
    }


def get_author_profile(author_id: str) -> dict:
    """Get complete profile for an author style brick."""
    if author_id not in AUTHOR_CATALOG:
        raise ValueError(
            f"Unknown author '{author_id}'. "
            f"Available: {list(AUTHOR_CATALOG.keys())}"
        )
    return dict(AUTHOR_CATALOG[author_id])


def find_max_contrast_pair() -> dict:
    """Find the two authors with maximum distance in style-space."""
    authors = list(AUTHOR_CATALOG.keys())
    max_dist = 0.0
    max_pair = (None, None)

    for i, a1 in enumerate(authors):
        for a2 in authors[i + 1:]:
            result = compute_style_distance(a1, a2)
            if result["euclidean_distance"] > max_dist:
                max_dist = result["euclidean_distance"]
                max_pair = (a1, a2)

    return compute_style_distance(max_pair[0], max_pair[1])


def find_nearest_neighbor(author_id: str) -> dict:
    """Find the closest author in style-space to the given author."""
    authors = list(AUTHOR_CATALOG.keys())
    min_dist = float("inf")
    nearest = None

    for other in authors:
        if other == author_id:
            continue
        result = compute_style_distance(author_id, other)
        if result["euclidean_distance"] < min_dist:
            min_dist = result["euclidean_distance"]
            nearest = other

    return compute_style_distance(author_id, nearest)
