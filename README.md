# Author Style "-esque" MCP Server

A curated catalog of 11 author writing styles decomposed into 8 orthogonal dimensions, with dual-output paths for text generation and image generation. Each style is an independent "stompbox" that colors prompts with structural writing patterns — not copied text.

## Architecture

```
Layer 1: Taxonomy (0 tokens)     → author_style_taxonomy.py
Layer 2: Deterministic (0 tokens) → author_style_operations.py
Layer 3: Creative synthesis       → Consumer LLM responsibility
Server:  FastMCP interface        → author_style_mcp.py
```

Layer 1 holds the pure data — 11 author coordinates in 8D style-space, dimension specifications, and output vocabulary mappings. Layer 2 performs all deterministic operations: distance computation, weighted interpolation (blending), vocabulary extraction, and prompt generation. No LLM calls at any point. Layer 3 is left to the consuming application — a single Claude or other LLM call that uses the structured directives as creative input.

## The Catalog

| ID | Style | Origin | Signature |
|---|---|---|---|
| `hemingway` | Hemingway-esque | English (American) | Iceberg theory, paratactic flatness, submerged tension |
| `de_sade` | Marquis de Sade-esque | French | Baroque nesting, exhaustive enumeration, philosophical excess |
| `le_guin` | Ursula K. Le Guin-esque | English (American) | Balanced cadence, anthropological worldbuilding, warm precision |
| `didion` | Joan Didion-esque | English (American) | Clinical observation, specific sensory detail, retrospective present |
| `lovecraft` | Lovecraft-esque | English (American) | Accumulative horror, archaic register, cosmic scale |
| `borges` | Borges-esque | Spanish (Argentine) | Labyrinthine logic, infinite recursion, philosophical miniatures |
| `murakami` | Murakami-esque | Japanese | Flat affect, mundane surrealism, domestic loneliness |
| `marquez` | Márquez-esque | Spanish (Colombian) | Magical realism, multigenerational fate, tropical profusion |
| `kafka` | Kafka-esque | German (Czech) | Bureaucratic absurdism, plain surface over impossible premise |
| `shonagon` | Sei Shōnagon-esque | Japanese (Classical) | List-form observation, radical sensory specificity, aesthetic judgment |
| `lispector` | Clarice Lispector-esque | Brazilian Portuguese | Interior stream, philosophical viscerality, self-examining language |

## The 8 Dimensions

All values normalized [0.0, 1.0].

| Dimension | Low End | High End | Text Output | Image Output |
|---|---|---|---|---|
| **Syntactic Density** | Paratactic / flat | Hypotactic / nested | Sentence length, clause depth | Compositional layering depth |
| **Sensory Concreteness** | Abstract / conceptual | Concrete / sensory | Noun register, verb type | Material rendering specificity |
| **Ornamental Register** | Stripped / minimal | Lush / baroque | Adjective density, figurative language | Surface detail complexity |
| **Tension Visibility** | Submerged / iceberg | Externalized / explicit | Show vs. tell ratio | Lighting drama, contrast ratio |
| **Tension Temporality** | Ruptural / episodic | Accumulative / inevitable | Pacing, foreshadowing density | Temporal framing, motion state |
| **Reality Stability** | Unstable / paradoxical | Stable / verifiable | Epistemic mode, hedging language | Spatial logic, physics accuracy |
| **Interiority** | Exterior / behavioral | Interior / consciousness | POV mode, thought access | Framing distance, depth of field |
| **Temporal Mode** | Eternal present / episodic | Cyclical / exhaustive | Tense, temporal scope | Motion blur, temporal compositing |

## Tools

### Layer 1 — Taxonomy Lookup (0 tokens)

- **`get_author_styles()`** — List all 11 authors with coordinates
- **`get_author_style_profile(author_id)`** — Complete profile: coordinates, signature moves, text/image vocabulary
- **`get_style_dimensions()`** — All 8 dimensions with low/mid/high output mappings
- **`get_parameter_names()`** — Ordered parameter list for dynamics integration

### Layer 2 — Deterministic Operations (0 tokens)

- **`compute_author_distance(author_id_1, author_id_2)`** — Euclidean distance with per-dimension breakdown
- **`blend_author_styles(blend_spec_json)`** — Weighted interpolation of multiple styles
- **`generate_text_style_prompt(author_id | blend_spec_json | custom_coordinates_json)`** — Text-generation directives
- **`generate_image_style_prompt(author_id | blend_spec_json | custom_coordinates_json, style_modifier)`** — Image-generation visual vocabulary
- **`find_style_extremes()`** — Maximum-contrast pair across catalog
- **`find_nearest_style(author_id)`** — Closest neighbor in style-space

## Usage Examples

### Single style — text prompt
```
generate_text_style_prompt(author_id="kafka")
```
Returns structured directives: sentence architecture, vocabulary constraints, forbidden words, paragraph rhythm, and a composited master prompt string.

### Single style — image prompt
```
generate_image_style_prompt(author_id="marquez", style_modifier="photorealistic")
```
Returns keywords, color palette, compositional rules, and per-dimension visual directives suitable for ComfyUI / Stable Diffusion / DALL-E.

### Blended style
```
blend_author_styles('{"hemingway": 0.6, "borges": 0.3, "shonagon": 0.1}')
```
Interpolates in 8D style-space. Returns blended coordinates, nearest catalog author (Didion, distance 0.406), merged signature moves, and extracted text/image vocabularies for the blend point.

### Distance analysis
```
compute_author_distance("hemingway", "lovecraft")
```
Returns Euclidean distance (1.863), per-dimension breakdown, and identifies the maximum-contrast axis (ornamental_register, gap 0.80).

## Dynamics Integration

Coordinates are directly compatible with `aesthetics-dynamics-core` tools:

```python
# Get Hemingway coordinates
coords = get_coordinates("hemingway")
# → {"syntactic_density": 0.10, "sensory_concreteness": 0.90, ...}

# Use with integrate_trajectory for smooth style morphing
integrate_trajectory(
    start_state=get_coordinates("hemingway"),
    target_state=get_coordinates("lovecraft"),
    parameter_names=PARAMETER_NAMES,
    num_steps=30
)
```

Also composable with `catastrophe-morph` and `surface-design-aesthetics` servers — stack an author style brick with a catastrophe type or surface treatment for cross-domain aesthetic composition.

## Composition Example: The Stompbox Chain

```
User prompt
  → Hemingway-esque (text structure: terse, concrete, submerged)
  → Catastrophe Morph: cusp (visual geometry: sharp vertices, crystalline)
  → Surface Design: matte_ceramic (material: chalky, light-absorbing)
  → Final synthesis (single LLM call)
```

Each brick is independent, deterministic, and zero-cost. Creative synthesis happens once at the end.

## Deployment

FastMCP Cloud entry point:
```
author_style_mcp.py:mcp
```

Local execution:
```bash
python author_style_mcp.py
```

## File Structure

```
author_style_taxonomy.py    # Layer 1: Types, dimensions, author catalog
author_style_operations.py  # Layer 2: Distance, blend, prompt generation
author_style_mcp.py         # FastMCP server with tool decorators
pyproject.toml              # Package configuration
README.md                   # This file
```

## Style-Space Topology Notes

From validation testing:

- **Maximum contrast pair:** Hemingway ↔ Lovecraft (1.863) — wider than Hemingway ↔ de Sade (1.792) due to Lovecraft's combined extremes on ornament, reality stability, and interiority
- **Surprising neighbors:** Kafka ↔ Le Guin (0.636) — structurally closer than their reputations suggest, sharing balanced syntactic density and mid-range tension handling
- **Emergent blends:** 60/30/10 Hemingway/Borges/Shōnagon lands in Didion's neighborhood — concreteness + interiority + sensory precision ≈ cool clinical observation
- **Unique coordinate:** Sei Shōnagon occupies a region no other author approaches — low density + extreme concreteness + episodic temporality + high interiority is a combination absent from the Western literary tradition
