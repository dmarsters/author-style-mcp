"""
Author Style MCP Server — "-esque" Writing Style Bricks

A curated catalog of 11 author writing styles decomposed into 8 orthogonal
dimensions, with dual-output paths for text generation and image generation.

Architecture:
    Layer 1: Taxonomy lookup (0 tokens) — author_style_taxonomy.py
    Layer 2: Deterministic ops (0 tokens) — author_style_operations.py
    Layer 3: Creative synthesis (single LLM call) — consumer responsibility

FastMCP Cloud deployment:
    Entry point: author_style_mcp.py:mcp
"""

import json
from typing import Optional

from fastmcp import FastMCP

from author_style_taxonomy import (
    AUTHOR_CATALOG,
    DIMENSIONS,
    PARAMETER_NAMES,
)
from author_style_operations import (
    compute_style_distance,
    find_max_contrast_pair,
    find_nearest_neighbor,
    generate_image_prompt,
    generate_text_prompt,
    get_author_profile,
    interpolate_styles,
    list_authors,
)


mcp = FastMCP("author-style-esque")


# -----------------------------------------------------------------------
# Layer 1 tools — pure taxonomy lookup (0 tokens)
# -----------------------------------------------------------------------

@mcp.tool()
def get_author_styles() -> str:
    """List all 11 curated author style bricks with coordinates.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Returns:
        JSON mapping author IDs to display names, language origins,
        and 8D style-space coordinates.
    """
    return json.dumps(list_authors(), indent=2)


@mcp.tool()
def get_author_style_profile(author_id: str) -> str:
    """Get complete profile for an author style brick.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Args:
        author_id: One of the 11 author IDs (hemingway, de_sade, le_guin,
            didion, lovecraft, borges, murakami, marquez, kafka,
            shonagon, lispector)

    Returns:
        Complete profile including coordinates, signature moves,
        text vocabulary, and image vocabulary.
    """
    return json.dumps(get_author_profile(author_id), indent=2)


@mcp.tool()
def get_style_dimensions() -> str:
    """List all 8 style-space dimensions with descriptions and output mappings.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Returns:
        JSON with dimension specs including text and image output mappings
        at low/mid/high tiers.
    """
    return json.dumps(DIMENSIONS, indent=2)


@mcp.tool()
def get_parameter_names() -> str:
    """Return ordered list of parameter names for dynamics integration.

    Layer 1: Pure taxonomy lookup (0 tokens)

    Use this to get parameter names compatible with aesthetics-dynamics-core
    tools (integrate_trajectory, compute_gradient_field, etc.)
    """
    return json.dumps(PARAMETER_NAMES)


# -----------------------------------------------------------------------
# Layer 2 tools — deterministic operations (0 tokens)
# -----------------------------------------------------------------------

@mcp.tool()
def compute_author_distance(
    author_id_1: str,
    author_id_2: str,
    weighted: bool = False,
) -> str:
    """Compute distance between two author styles in 8D style-space.

    Layer 2: Pure distance computation (0 tokens)

    Args:
        author_id_1: First author ID
        author_id_2: Second author ID
        weighted: If True, apply perceptual salience weights

    Returns:
        Distance with per-dimension breakdown and max-contrast axis.
    """
    return json.dumps(
        compute_style_distance(author_id_1, author_id_2, weighted),
        indent=2,
    )


@mcp.tool()
def blend_author_styles(blend_spec_json: str) -> str:
    """Blend multiple author styles by weighted interpolation.

    Layer 2: Deterministic interpolation (0 tokens)

    Computes weighted average in style-space, extracts output vocabularies,
    and identifies nearest catalog author to the blended point.

    Args:
        blend_spec_json: JSON string mapping author_id -> weight.
            Example: '{"hemingway": 0.7, "borges": 0.3}'
            Weights are normalized to sum to 1.0.

    Returns:
        Blended coordinates, nearest catalog author, signature moves,
        and text/image vocabulary for the blend point.
    """
    blend_spec = json.loads(blend_spec_json)
    return json.dumps(interpolate_styles(blend_spec), indent=2)


@mcp.tool()
def generate_text_style_prompt(
    author_id: str = "",
    blend_spec_json: str = "",
    custom_coordinates_json: str = "",
) -> str:
    """Generate text-generation-ready style directives.

    Layer 2: Deterministic prompt synthesis (0 tokens)

    Provide exactly one of: author_id, blend_spec_json, or custom_coordinates_json.

    Args:
        author_id: Single author ID for pure style
        blend_spec_json: JSON blend spec, e.g. '{"hemingway": 0.6, "kafka": 0.4}'
        custom_coordinates_json: JSON with 8D coordinates

    Returns:
        Structured directives including master directive string,
        signature moves, vocabulary constraints, and full composited prompt.
    """
    kwargs = {}
    if author_id:
        kwargs["author_id"] = author_id
    elif blend_spec_json:
        kwargs["blend_spec"] = json.loads(blend_spec_json)
    elif custom_coordinates_json:
        kwargs["custom_coordinates"] = json.loads(custom_coordinates_json)

    return json.dumps(generate_text_prompt(**kwargs), indent=2)


@mcp.tool()
def generate_image_style_prompt(
    author_id: str = "",
    blend_spec_json: str = "",
    custom_coordinates_json: str = "",
    style_modifier: str = "",
) -> str:
    """Generate image-generation-ready visual directives from author style.

    Layer 2: Deterministic prompt synthesis (0 tokens)

    Translates author style coordinates into visual vocabulary suitable
    for ComfyUI, Stable Diffusion, DALL-E, etc.

    Provide exactly one of: author_id, blend_spec_json, or custom_coordinates_json.

    Args:
        author_id: Single author ID for pure style
        blend_spec_json: JSON blend spec, e.g. '{"murakami": 0.5, "lispector": 0.5}'
        custom_coordinates_json: JSON with 8D coordinates
        style_modifier: Optional prefix (e.g. "photorealistic", "oil painting")

    Returns:
        Keywords, color palette, compositional rules, per-dimension visuals,
        and composited prompt string.
    """
    kwargs = {"style_modifier": style_modifier}
    if author_id:
        kwargs["author_id"] = author_id
    elif blend_spec_json:
        kwargs["blend_spec"] = json.loads(blend_spec_json)
    elif custom_coordinates_json:
        kwargs["custom_coordinates"] = json.loads(custom_coordinates_json)

    return json.dumps(generate_image_prompt(**kwargs), indent=2)


@mcp.tool()
def find_style_extremes() -> str:
    """Find the maximum-contrast author pair in style-space.

    Layer 2: Distance computation across all pairs (0 tokens)

    Returns:
        The two authors with greatest Euclidean distance,
        with full per-dimension breakdown.
    """
    return json.dumps(find_max_contrast_pair(), indent=2)


@mcp.tool()
def find_nearest_style(author_id: str) -> str:
    """Find the closest author style to a given author.

    Layer 2: Distance computation (0 tokens)

    Args:
        author_id: Author to find neighbors for

    Returns:
        Nearest author with distance and per-dimension breakdown.
    """
    return json.dumps(find_nearest_neighbor(author_id), indent=2)


# -----------------------------------------------------------------------
# Server info
# -----------------------------------------------------------------------

@mcp.tool()
def get_server_info() -> str:
    """Get information about the Author Style MCP server.

    Returns server metadata, available authors, dimensions, and capabilities.
    """
    return json.dumps({
        "name": "Author Style '-esque' MCP Server",
        "version": "0.1.0",
        "description": (
            "Curated catalog of 11 author writing styles decomposed into "
            "8 orthogonal dimensions with dual text/image output paths. "
            "Each style is an independent 'stompbox' that colors prompts "
            "with structural writing patterns — not copied text."
        ),
        "architecture": {
            "layer_1": "Taxonomy lookup — author coordinates, dimensions (0 tokens)",
            "layer_2": "Deterministic ops — distance, blend, prompt gen (0 tokens)",
            "layer_3": "Creative synthesis — consumer LLM responsibility",
        },
        "dimensions": len(PARAMETER_NAMES),
        "parameter_names": PARAMETER_NAMES,
        "authors": {
            aid: {
                "display_name": entry["display_name"],
                "language_origin": entry["language_origin"],
            }
            for aid, entry in AUTHOR_CATALOG.items()
        },
        "n_authors": len(AUTHOR_CATALOG),
        "capabilities": [
            "Single author style extraction (text + image)",
            "Multi-author weighted blending",
            "Style distance computation",
            "Nearest neighbor / max contrast discovery",
            "Compatible with aesthetics-dynamics-core for trajectory integration",
            "Compatible with catastrophe-morph and surface-design-aesthetics for composition",
        ],
        "dynamics_integration": (
            "Use get_parameter_names() to get ordered parameter list, then "
            "pass author coordinates to aesthetics-dynamics-core tools like "
            "integrate_trajectory, compute_gradient_field, or "
            "identify_attractor_basins for style-space dynamics analysis."
        ),
    }, indent=2)


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
