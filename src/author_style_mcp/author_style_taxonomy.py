"""
Author Style Taxonomy — Layer 1 (Pure Lookup, 0 Tokens)

Canonical parameter schema for the "-esque" author style MCP server ecosystem.
Each author is a coordinate in 8-dimensional style-space. Text and image generation
outputs are parallel projections from the same coordinate point.

Architecture:
    Layer 1: This file — taxonomy lookup, 0 LLM cost
    Layer 2: Deterministic mapping (interpolation, distance, vocabulary extraction)
    Layer 3: Creative synthesis (single LLM call for final output)

Dimensions:
    1. syntactic_density      — clause nesting depth, sentence structural load
    2. sensory_concreteness   — concrete/sensory vs. abstract/conceptual ratio
    3. ornamental_register    — decoration density, figurative language, lexical rarity
    4. tension_visibility     — surface vs. submerged tension
    5. tension_temporality    — accumulative vs. ruptural tension pacing
    6. reality_stability      — trustworthiness of the depicted world
    7. interiority            — access to inner experience
    8. temporal_mode          — relationship to time (episodic → cyclical/exhaustive)

All values normalized [0.0, 1.0].
"""

from typing import TypedDict, Optional

# ---------------------------------------------------------------------------
# Type definitions
# ---------------------------------------------------------------------------

class AuthorCoordinates(TypedDict):
    """8D coordinate in author style-space."""
    syntactic_density: float
    sensory_concreteness: float
    ornamental_register: float
    tension_visibility: float
    tension_temporality: float
    reality_stability: float
    interiority: float
    temporal_mode: float


class DimensionSpec(TypedDict):
    """Specification for a single taxonomy dimension."""
    id: str
    name: str
    description: str
    low_label: str
    high_label: str
    text_output_mapping: dict
    image_output_mapping: dict


class AuthorEntry(TypedDict):
    """Complete entry for a single author style brick."""
    id: str
    display_name: str
    language_origin: str
    coordinates: AuthorCoordinates
    signature_moves: list[str]
    text_vocabulary: dict
    image_vocabulary: dict


# ---------------------------------------------------------------------------
# Dimension specifications
# ---------------------------------------------------------------------------

DIMENSIONS: dict[str, DimensionSpec] = {
    "syntactic_density": {
        "id": "syntactic_density",
        "name": "Syntactic Density",
        "description": "Structural load per sentence — clause nesting depth, "
                       "ratio of subordinate to main clauses.",
        "low_label": "paratactic / flat",
        "high_label": "hypotactic / deeply nested",
        "text_output_mapping": {
            "low":  {"sentence_length": "short", "clause_depth": 1,
                     "conjunction_preference": ["and", "then", "but"],
                     "structure_directive": "Simple declarative sentences. "
                     "One main clause. Coordinating conjunctions only."},
            "mid":  {"sentence_length": "variable", "clause_depth": 2,
                     "conjunction_preference": ["which", "although", "because", "while"],
                     "structure_directive": "Balanced sentence architecture. "
                     "Mix simple and complex structures. Periodic sentences permitted."},
            "high": {"sentence_length": "long", "clause_depth": 4,
                     "conjunction_preference": ["wherein", "notwithstanding",
                                                "such that", "inasmuch as"],
                     "structure_directive": "Deeply nested subordination. "
                     "Sentences carry multiple embedded qualifications. "
                     "Delay main verb. Exhaustive clause stacking."},
        },
        "image_output_mapping": {
            "low":  {"compositional_layers": 1, "depth_planes": "flat",
                     "visual_directive": "Minimal layering. Single visual plane. "
                     "Clean negative space. Figure isolated against ground."},
            "mid":  {"compositional_layers": 3, "depth_planes": "moderate",
                     "visual_directive": "Three distinct depth planes. "
                     "Foreground, subject, background clearly articulated."},
            "high": {"compositional_layers": 5, "depth_planes": "deep",
                     "visual_directive": "Dense visual layering. Multiple overlapping "
                     "planes. Nested frames-within-frames. Baroque spatial depth."},
        },
    },

    "sensory_concreteness": {
        "id": "sensory_concreteness",
        "name": "Sensory Concreteness",
        "description": "Ratio of concrete sensory nouns/verbs to abstract conceptual language.",
        "low_label": "abstract / conceptual",
        "high_label": "concrete / sensory",
        "text_output_mapping": {
            "low":  {"noun_register": "abstract", "verb_type": "conceptual",
                     "vocabulary_directive": "Latinate abstract vocabulary. "
                     "Ideas, categories, logical relations. "
                     "Nouns you cannot photograph."},
            "mid":  {"noun_register": "mixed", "verb_type": "balanced",
                     "vocabulary_directive": "Ground abstractions in occasional "
                     "concrete detail. Alternate between sensory and conceptual."},
            "high": {"noun_register": "concrete", "verb_type": "physical",
                     "vocabulary_directive": "Anglo-Saxon concrete vocabulary. "
                     "Things with weight, temperature, texture. "
                     "Actions visible to a camera. Nouns you can hold."},
        },
        "image_output_mapping": {
            "low":  {"material_rendering": "diagrammatic",
                     "texture_specificity": "minimal",
                     "visual_directive": "Geometric abstraction. Flat color fields. "
                     "Schematic rather than photographic. Conceptual space."},
            "mid":  {"material_rendering": "suggested",
                     "texture_specificity": "moderate",
                     "visual_directive": "Recognizable materials with selective detail. "
                     "Key textures rendered, others implied."},
            "high": {"material_rendering": "photographic",
                     "texture_specificity": "explicit",
                     "visual_directive": "Explicit material rendering. Visible grain, "
                     "weave, condensation, patina. Surfaces you can feel."},
        },
    },

    "ornamental_register": {
        "id": "ornamental_register",
        "name": "Ornamental Register",
        "description": "Decoration density — adjective frequency, figurative language, "
                       "lexical rarity. The prose surface treatment.",
        "low_label": "stripped / anti-ornamental",
        "high_label": "lush / baroque",
        "text_output_mapping": {
            "low":  {"adjective_density": "minimal", "figurative_frequency": "rare",
                     "vocabulary_register": "common",
                     "surface_directive": "No unnecessary adjectives. "
                     "Plain nouns. Metaphor only when unavoidable. "
                     "Common Anglo-Saxon vocabulary."},
            "mid":  {"adjective_density": "selective", "figurative_frequency": "occasional",
                     "vocabulary_register": "educated",
                     "surface_directive": "Selective ornamentation. Well-placed "
                     "figurative language. Elegant but not excessive."},
            "high": {"adjective_density": "abundant", "figurative_frequency": "dense",
                     "vocabulary_register": "rare/archaic",
                     "surface_directive": "Lush adjectival profusion. "
                     "Dense figurative language. Rare and archaic vocabulary. "
                     "Cataloging through ornamental excess."},
        },
        "image_output_mapping": {
            "low":  {"surface_complexity": "clean",
                     "detail_density": "minimal",
                     "visual_directive": "Clean surfaces. Minimal texture. "
                     "Modernist reduction. Negative space as design element."},
            "mid":  {"surface_complexity": "detailed",
                     "detail_density": "moderate",
                     "visual_directive": "Selective surface detail. Key areas rendered "
                     "with precision, others simplified."},
            "high": {"surface_complexity": "ornate",
                     "detail_density": "maximal",
                     "visual_directive": "Highly detailed ornamental surfaces. "
                     "Pattern-on-pattern. Filigree, brocade, botanical density. "
                     "Horror vacui — every surface activated."},
        },
    },

    "tension_visibility": {
        "id": "tension_visibility",
        "name": "Tension Visibility",
        "description": "Whether tension lives on the surface or remains submerged.",
        "low_label": "submerged / iceberg",
        "high_label": "externalized / explicit",
        "text_output_mapping": {
            "low":  {"show_tell_ratio": "show", "emotional_vocabulary": "absent",
                     "tension_directive": "Never name the emotion. "
                     "Render behavior and objects. "
                     "Reader infers tension from what is not said."},
            "mid":  {"show_tell_ratio": "balanced", "emotional_vocabulary": "restrained",
                     "tension_directive": "Acknowledge tension through measured "
                     "observation. Clinical precision about emotional states."},
            "high": {"show_tell_ratio": "tell", "emotional_vocabulary": "explicit",
                     "tension_directive": "Name the tension directly. "
                     "Escalating emotional vocabulary. "
                     "Narrator's distress is the content."},
        },
        "image_output_mapping": {
            "low":  {"lighting_drama": "even", "contrast_ratio": "low",
                     "visual_directive": "Even, ambient lighting. Tension encoded in "
                     "compositional unease — off-center framing, ambiguous gaze "
                     "vectors, objects slightly wrong."},
            "mid":  {"lighting_drama": "directional", "contrast_ratio": "moderate",
                     "visual_directive": "Directional lighting creating defined shadows. "
                     "Moderate tonal contrast. Tension visible but controlled."},
            "high": {"lighting_drama": "chiaroscuro", "contrast_ratio": "extreme",
                     "visual_directive": "Dramatic chiaroscuro. Deep shadows, "
                     "hard light. Diagonal composition lines. "
                     "Explicit visual conflict and confrontation."},
        },
    },

    "tension_temporality": {
        "id": "tension_temporality",
        "name": "Tension Temporality",
        "description": "Whether tension accumulates slowly over time or arrives as rupture.",
        "low_label": "ruptural / episodic",
        "high_label": "accumulative / inevitable",
        "text_output_mapping": {
            "low":  {"pacing": "episodic", "foreshadowing": "none",
                     "tempo_directive": "Self-contained moments. "
                     "Each passage complete in itself. "
                     "Tension arrives without warning."},
            "mid":  {"pacing": "building", "foreshadowing": "subtle",
                     "tempo_directive": "Gradual escalation through observation. "
                     "Evidence accumulates. Paragraphs lengthen."},
            "high": {"pacing": "inevitable", "foreshadowing": "heavy",
                     "tempo_directive": "Fate announced early, then approached "
                     "with terrible patience. Each sentence worse than the last. "
                     "Progressive revelation of the already-known."},
        },
        "image_output_mapping": {
            "low":  {"temporal_framing": "frozen_instant",
                     "sequence_implication": "none",
                     "visual_directive": "Frozen moment. No implied before or after. "
                     "Complete in the frame. Snapshot temporality."},
            "mid":  {"temporal_framing": "implied_sequence",
                     "sequence_implication": "moderate",
                     "visual_directive": "Implied motion. Traces of what came before — "
                     "footprints, smoke, residue. Subject mid-action."},
            "high": {"temporal_framing": "durational",
                     "sequence_implication": "heavy",
                     "visual_directive": "Temporal compositing. Multiple moments "
                     "layered in single frame. Long exposure blur. "
                     "Generational accumulation visible in environmental detail."},
        },
    },

    "reality_stability": {
        "id": "reality_stability",
        "name": "Reality Stability",
        "description": "How trustworthy is the depicted world — how much impossibility "
                       "the text's internal logic permits.",
        "low_label": "unstable / paradoxical",
        "high_label": "stable / verifiable",
        "text_output_mapping": {
            "low":  {"epistemic_mode": "unreliable", "modality": "impossible",
                     "reality_directive": "State impossible things as fact. "
                     "No hedging. Paradox presented in declarative mode. "
                     "Logic that folds back on itself."},
            "mid":  {"epistemic_mode": "liminal", "modality": "conditional",
                     "reality_directive": "Reality bends under observation. "
                     "Familiar things behave strangely. "
                     "One impossible element in an otherwise stable frame."},
            "high": {"epistemic_mode": "reliable", "modality": "declarative",
                     "reality_directive": "Journalistic reliability. "
                     "Verifiable details. Physical accuracy. "
                     "Hedging language for uncertainty."},
        },
        "image_output_mapping": {
            "low":  {"spatial_logic": "impossible",
                     "physics_accuracy": "violated",
                     "visual_directive": "Impossible geometry. Escher-like spatial "
                     "paradox. Recursive visual structures. Dream logic composition. "
                     "Perspective that contradicts itself."},
            "mid":  {"spatial_logic": "liminal",
                     "physics_accuracy": "mostly_correct",
                     "visual_directive": "Physically plausible with one wrong element. "
                     "Uncanny valley of space. Light from impossible source. "
                     "Scale inconsistency."},
            "high": {"spatial_logic": "correct",
                     "physics_accuracy": "accurate",
                     "visual_directive": "Physically accurate rendering. "
                     "Correct perspective, lighting, material behavior. "
                     "Photographic spatial logic."},
        },
    },

    "interiority": {
        "id": "interiority",
        "name": "Interiority",
        "description": "Degree of access to inner experience — psychological depth "
                       "and subjective consciousness rendered in the text.",
        "low_label": "exterior / behavioral",
        "high_label": "interior / consciousness",
        "text_output_mapping": {
            "low":  {"pov_mode": "external", "thought_access": "none",
                     "interiority_directive": "Camera-eye. Behavior only. "
                     "No access to thought. Dialogue and action. "
                     "Reader infers psychology from surface."},
            "mid":  {"pov_mode": "limited", "thought_access": "filtered",
                     "interiority_directive": "Selective interiority. "
                     "Observations filtered through a distinctive consciousness "
                     "but not direct stream of thought."},
            "high": {"pov_mode": "deep", "thought_access": "immersive",
                     "interiority_directive": "Language as thought happening. "
                     "Consciousness rendered in real-time. "
                     "The sentence IS the inner experience."},
        },
        "image_output_mapping": {
            "low":  {"framing_distance": "wide", "dof": "deep",
                     "gaze_directive": "Wide environmental framing. "
                     "Figure-in-landscape. Deep depth of field. "
                     "Subject as element of composition, not psychological center."},
            "mid":  {"framing_distance": "medium", "dof": "moderate",
                     "gaze_directive": "Medium shot. Subject's face visible. "
                     "Environmental context retained. "
                     "Gaze vector at 15-30° from camera axis."},
            "high": {"framing_distance": "close", "dof": "shallow",
                     "gaze_directive": "Tight framing. Eyes prominent. "
                     "Shallow depth of field isolating subject. "
                     "Direct or near-direct gaze vector to viewer. "
                     "Background dissolved into bokeh."},
        },
    },

    "temporal_mode": {
        "id": "temporal_mode",
        "name": "Temporal Mode",
        "description": "The text's relationship to time — from episodic eternal present "
                       "to cyclical/exhaustive temporal structures.",
        "low_label": "eternal present / episodic",
        "high_label": "cyclical / exhaustive",
        "text_output_mapping": {
            "low":  {"tense": "present", "temporal_scope": "moment",
                     "time_directive": "Each passage exists in its own present. "
                     "No before or after implied. Self-contained observation. "
                     "Time as a series of discrete nows."},
            "mid":  {"tense": "variable", "temporal_scope": "span",
                     "time_directive": "Awareness of duration. Past informing present. "
                     "Flashback and prolepsis available but controlled. "
                     "Deep time acknowledged."},
            "high": {"tense": "omniscient_temporal", "temporal_scope": "generations",
                     "time_directive": "All moments present simultaneously. "
                     "Cyclical return. Generations rhyming. "
                     "Every permutation explored. Time as exhaustive catalog."},
        },
        "image_output_mapping": {
            "low":  {"motion_state": "frozen",
                     "temporal_texture": "instantaneous",
                     "visual_directive": "Crisp frozen instant. No motion blur. "
                     "No implied sequence. Photograph temporality."},
            "mid":  {"motion_state": "implied",
                     "temporal_texture": "durational",
                     "visual_directive": "Implied duration. Weathering, aging, "
                     "patina suggesting passage of time. "
                     "Environmental storytelling through wear."},
            "high": {"motion_state": "composite",
                     "temporal_texture": "layered",
                     "visual_directive": "Multiple temporal layers in single frame. "
                     "Ghosting, palimpsest, archaeological stratification. "
                     "Long exposure. Decay and growth co-present."},
        },
    },
}


# ---------------------------------------------------------------------------
# Author catalog — 11 curated styles
# ---------------------------------------------------------------------------

AUTHOR_CATALOG: dict[str, AuthorEntry] = {

    "hemingway": {
        "id": "hemingway",
        "display_name": "Hemingway-esque",
        "language_origin": "English (American)",
        "coordinates": {
            "syntactic_density":    0.10,
            "sensory_concreteness": 0.90,
            "ornamental_register":  0.05,
            "tension_visibility":   0.10,
            "tension_temporality":  0.25,
            "reality_stability":    0.90,
            "interiority":          0.15,
            "temporal_mode":        0.20,
        },
        "signature_moves": [
            "Iceberg theory — emotional weight carried by omission",
            "Paratactic 'and' conjunction chains",
            "Dialogue carrying subtext the narrator won't state",
            "Concrete nouns, active verbs, minimal adjectives",
            "Short paragraphs as rhythmic percussion",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "but", "then"],
            "sentence_starters": ["He", "She", "It was", "There was", "The"],
            "forbidden": ["very", "really", "beautiful", "magnificent",
                          "incredible", "amazing"],
            "register": "Anglo-Saxon monosyllabic preference",
            "paragraph_rhythm": "short-short-short-medium-short",
        },
        "image_vocabulary": {
            "keywords": ["stark composition", "high negative-space ratio",
                         "single subject isolation", "hard directional light",
                         "minimal props", "environmental realism",
                         "unflinching gaze", "dust and daylight"],
            "color_palette": ["ochre", "bone white", "dried blood",
                              "sun-bleached", "khaki", "deep shadow"],
            "compositional_rules": [
                "Subject-to-negative-space ratio minimum 1:3",
                "Single dominant light source at 45° elevation",
                "No decorative elements in frame",
                "Horizon line in lower third",
            ],
        },
    },

    "de_sade": {
        "id": "de_sade",
        "display_name": "Marquis de Sade-esque",
        "language_origin": "French",
        "coordinates": {
            "syntactic_density":    0.95,
            "sensory_concreteness": 0.50,
            "ornamental_register":  0.90,
            "tension_visibility":   0.95,
            "tension_temporality":  0.80,
            "reality_stability":    0.60,
            "interiority":          0.20,
            "temporal_mode":        0.90,
        },
        "signature_moves": [
            "Exhaustive enumeration — every permutation cataloged",
            "Philosophical monologue embedded in extreme scenario",
            "Bodies as philosophical instruments, not psychological subjects",
            "Nested subordination mirroring power hierarchies",
            "Transgressive content delivered in aristocratic register",
        ],
        "text_vocabulary": {
            "conjunctions": ["moreover", "furthermore", "notwithstanding",
                             "whereupon", "inasmuch as"],
            "sentence_starters": ["It is necessary that", "One must observe",
                                  "Let us now consider", "The principle demands"],
            "forbidden": ["nice", "pleasant", "comfortable", "gentle"],
            "register": "Aristocratic philosophical — Latinate, formal",
            "paragraph_rhythm": "long-longer-longest-philosophical_aside-resume",
        },
        "image_vocabulary": {
            "keywords": ["baroque layering", "chiaroscuro extremes",
                         "diagonal tension lines", "dense ornamental surfaces",
                         "power geometry", "theatrical staging",
                         "overwhelming visual density", "cataloging composition"],
            "color_palette": ["crimson", "gold leaf", "deep velvet",
                              "marble white", "candle flame", "shadow black"],
            "compositional_rules": [
                "Multiple overlapping visual planes minimum 5 deep",
                "Diagonal dominant lines at 30-60° creating instability",
                "Every surface carries texture or pattern",
                "Lighting from multiple contradictory sources",
            ],
        },
    },

    "le_guin": {
        "id": "le_guin",
        "display_name": "Ursula K. Le Guin-esque",
        "language_origin": "English (American)",
        "coordinates": {
            "syntactic_density":    0.50,
            "sensory_concreteness": 0.55,
            "ornamental_register":  0.45,
            "tension_visibility":   0.50,
            "tension_temporality":  0.60,
            "reality_stability":    0.40,
            "interiority":          0.50,
            "temporal_mode":        0.55,
        },
        "signature_moves": [
            "Worldbuilding through implication rather than exposition",
            "Balanced cadence — neither sparse nor baroque",
            "Anthropological precision about invented cultures",
            "Quiet radical premises delivered matter-of-factly",
            "Warm but unsentimental narrative voice",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "though", "because", "as if", "while"],
            "sentence_starters": ["The", "In the", "There was a", "She had",
                                  "It was not"],
            "forbidden": ["awesome", "literally", "basically", "epic"],
            "register": "Educated but accessible — precise without ostentation",
            "paragraph_rhythm": "medium-medium-long-short-medium",
        },
        "image_vocabulary": {
            "keywords": ["balanced composition", "warm natural light",
                         "inhabited landscape", "architectural worldbuilding",
                         "cultural detail in environment", "dignified framing",
                         "grounded fantasy", "lived-in spaces"],
            "color_palette": ["earth tones", "deep forest green", "stone grey",
                              "warm amber", "twilight blue", "weathered wood"],
            "compositional_rules": [
                "Rule of thirds with subject at intersection point",
                "Environmental context always visible — subject in world",
                "Warm color temperature 4500-5500K",
                "Balanced depth of field — subject sharp, context readable",
            ],
        },
    },

    "didion": {
        "id": "didion",
        "display_name": "Joan Didion-esque",
        "language_origin": "English (American)",
        "coordinates": {
            "syntactic_density":    0.45,
            "sensory_concreteness": 0.70,
            "ornamental_register":  0.15,
            "tension_visibility":   0.30,
            "tension_temporality":  0.40,
            "reality_stability":    0.95,
            "interiority":          0.60,
            "temporal_mode":        0.40,
        },
        "signature_moves": [
            "Clinical sentence structure masking emotional intensity",
            "Specific sensory detail as existential evidence",
            "Retrospective present tense — reporting from aftermath",
            "Lists of concrete facts that accumulate into mood",
            "The personal made universal through precision",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "but", "which", "although"],
            "sentence_starters": ["I", "We", "The", "It was",
                                  "In the", "That was the"],
            "forbidden": ["incredible", "unbelievable", "indescribable",
                          "breathtaking"],
            "register": "Journalistic precision — cool, specific, exact",
            "paragraph_rhythm": "medium-short-long(periodic)-short-fragment",
        },
        "image_vocabulary": {
            "keywords": ["forensic observation", "clinical framing",
                         "specific light conditions", "geographical precision",
                         "quiet devastation", "California light",
                         "motel aesthetic", "highway geometry"],
            "color_palette": ["bleached white", "smog amber", "pool blue",
                              "asphalt grey", "jacaranda purple", "desert tan"],
            "compositional_rules": [
                "Slightly off-center framing suggesting unease",
                "Harsh midday light — no romantic golden hour",
                "Specific environmental details legible in frame",
                "Flat perspective suggesting journalistic distance",
            ],
        },
    },

    "lovecraft": {
        "id": "lovecraft",
        "display_name": "Lovecraft-esque",
        "language_origin": "English (American)",
        "coordinates": {
            "syntactic_density":    0.85,
            "sensory_concreteness": 0.40,
            "ornamental_register":  0.85,
            "tension_visibility":   0.80,
            "tension_temporality":  0.85,
            "reality_stability":    0.15,
            "interiority":          0.70,
            "temporal_mode":        0.75,
        },
        "signature_moves": [
            "Accumulative horror through clause stacking",
            "The unspeakable — gesture toward sensory detail, then retreat",
            "Archaic register lending authority to impossible claims",
            "Geological/cosmic time dwarfing human experience",
            "Narrator's reliability degrading as text progresses",
        ],
        "text_vocabulary": {
            "conjunctions": ["and yet", "for", "though", "whilst",
                             "such that", "in consequence of which"],
            "sentence_starters": ["It was then that", "I cannot describe",
                                  "Of the", "There are things",
                                  "What I saw"],
            "forbidden": ["cute", "nice", "fun", "awesome", "cool"],
            "register": "Archaic academic — deliberately overwrought",
            "paragraph_rhythm": "medium-long-longer-longest-short(gasp)",
        },
        "image_vocabulary": {
            "keywords": ["non-Euclidean geometry", "cyclopean architecture",
                         "deep shadow with luminous edges", "tentacular forms",
                         "impossible scale", "submarine depth",
                         "eldritch luminescence", "geological antiquity"],
            "color_palette": ["deep ocean green", "phosphorescent",
                              "basalt black", "sickly yellow-green",
                              "void purple", "corpse grey"],
            "compositional_rules": [
                "Subject dwarfed by environment — human scale minimized",
                "Light source origin impossible or contradictory",
                "Perspective lines converging at impossible vanishing point",
                "Geometry that almost resolves but doesn't",
            ],
        },
    },

    "borges": {
        "id": "borges",
        "display_name": "Borges-esque",
        "language_origin": "Spanish (Argentine)",
        "coordinates": {
            "syntactic_density":    0.80,
            "sensory_concreteness": 0.15,
            "ornamental_register":  0.60,
            "tension_visibility":   0.55,
            "tension_temporality":  0.70,
            "reality_stability":    0.10,
            "interiority":          0.80,
            "temporal_mode":        0.70,
        },
        "signature_moves": [
            "Labyrinthine logic — the trap closes through reasoning",
            "Infinite libraries, mirrors, recursive structures",
            "Philosophical density compressed into miniature forms",
            "Scholarly apparatus (footnotes, citations) for fictional subjects",
            "Time as simultaneous rather than sequential",
        ],
        "text_vocabulary": {
            "conjunctions": ["perhaps", "or rather", "that is to say",
                             "in other words", "which is to say"],
            "sentence_starters": ["It is said that", "The curious reader",
                                  "According to", "One might conjecture",
                                  "The universe"],
            "forbidden": ["simple", "straightforward", "obvious", "clearly"],
            "register": "Erudite philosophical — precise, recursive, scholarly",
            "paragraph_rhythm": "long-medium-long(recursive)-parenthetical-short(sting)",
        },
        "image_vocabulary": {
            "keywords": ["infinite regression", "mirror recursion",
                         "impossible library", "labyrinthine geometry",
                         "Escher-like spatial paradox", "miniature containing cosmos",
                         "scholarly manuscript", "hexagonal architecture"],
            "color_palette": ["parchment", "library mahogany", "ink blue",
                              "mirror silver", "candlelight amber",
                              "mathematical white"],
            "compositional_rules": [
                "Recursive visual structures — frame contains smaller version of itself",
                "Impossible spatial logic — Penrose stairs, Klein bottle topology",
                "Text/manuscripts visible as compositional elements",
                "Symmetrical composition suggesting infinite extension",
            ],
        },
    },

    "murakami": {
        "id": "murakami",
        "display_name": "Murakami-esque",
        "language_origin": "Japanese",
        "coordinates": {
            "syntactic_density":    0.25,
            "sensory_concreteness": 0.80,
            "ornamental_register":  0.20,
            "tension_visibility":   0.20,
            "tension_temporality":  0.20,
            "reality_stability":    0.20,
            "interiority":          0.55,
            "temporal_mode":        0.25,
        },
        "signature_moves": [
            "Flat affect juxtaposed with surreal intrusion",
            "Mundane sensory detail anchoring the uncanny",
            "Pop culture references as emotional shorthand",
            "Loneliness rendered through domestic routine",
            "Cats, jazz, cooking as consciousness markers",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "but", "so", "then"],
            "sentence_starters": ["I", "She", "The", "It was a",
                                  "For some reason"],
            "forbidden": ["magnificent", "extraordinary", "awe-inspiring",
                          "spectacular"],
            "register": "Conversational flat — deliberately understated",
            "paragraph_rhythm": "medium-short-short-medium-short(offhand_surreal)",
        },
        "image_vocabulary": {
            "keywords": ["liminal space", "quiet domestic interior",
                         "single impossible element", "empty urban night",
                         "jazz club lighting", "cat on kitchen counter",
                         "mundane surrealism", "rain on window"],
            "color_palette": ["warm interior amber", "cold blue exterior",
                              "vinyl black", "kitchen white",
                              "neon reflection", "twilight grey"],
            "compositional_rules": [
                "Domestic interior framing — through doorways, across tables",
                "One element that doesn't belong in an otherwise normal scene",
                "Warm artificial light contrasting cold exterior visible through window",
                "Subject alone in frame — isolation geometry",
            ],
        },
    },

    "marquez": {
        "id": "marquez",
        "display_name": "Márquez-esque",
        "language_origin": "Spanish (Colombian)",
        "coordinates": {
            "syntactic_density":    0.75,
            "sensory_concreteness": 0.75,
            "ornamental_register":  0.80,
            "tension_visibility":   0.70,
            "tension_temporality":  0.95,
            "reality_stability":    0.30,
            "interiority":          0.40,
            "temporal_mode":        0.85,
        },
        "signature_moves": [
            "Magical realism — impossible content in matter-of-fact declarative",
            "Multigenerational time — fate announced, then approached patiently",
            "Tropical profusion of sensory detail",
            "Names and lineages as structural architecture",
            "Death foretold — opening sentence contains the ending",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "who", "which", "where",
                             "until", "as though"],
            "sentence_starters": ["Many years later", "It was",
                                  "The day", "Colonel", "No one"],
            "forbidden": ["basically", "literally", "actually", "arguably"],
            "register": "Declarative lush — matter-of-fact about the impossible",
            "paragraph_rhythm": "long-long-very_long-short(fate)-long",
        },
        "image_vocabulary": {
            "keywords": ["tropical botanical density", "butterflies as portent",
                         "golden afternoon light", "crumbling colonial architecture",
                         "magical realism composite", "generational portrait",
                         "rain of flowers", "solitude geometry"],
            "color_palette": ["tropical green", "marigold yellow", "terracotta",
                              "butterfly blue", "aged sepia", "blood orange"],
            "compositional_rules": [
                "Dense botanical framing — foliage filling edges",
                "Multiple generations suggested in single frame",
                "One physically impossible element rendered photorealistically",
                "Warm saturated color temperature 3500-4500K",
            ],
        },
    },

    "kafka": {
        "id": "kafka",
        "display_name": "Kafka-esque",
        "language_origin": "German (Czech)",
        "coordinates": {
            "syntactic_density":    0.65,
            "sensory_concreteness": 0.35,
            "ornamental_register":  0.10,
            "tension_visibility":   0.35,
            "tension_temporality":  0.30,
            "reality_stability":    0.25,
            "interiority":          0.35,
            "temporal_mode":        0.30,
        },
        "signature_moves": [
            "Impossible premise accepted, bureaucratic logic thereafter",
            "Plain surface describing impossible situations",
            "Arrested time — events happen but nothing progresses",
            "Authority that can never be reached or understood",
            "The body as site of inexplicable transformation",
        ],
        "text_vocabulary": {
            "conjunctions": ["however", "nevertheless", "in spite of",
                             "which", "although"],
            "sentence_starters": ["He", "It was", "The", "Someone",
                                  "There was no"],
            "forbidden": ["magical", "wonderful", "extraordinary", "miraculous"],
            "register": "Bureaucratic plain — institutional clarity about the absurd",
            "paragraph_rhythm": "medium-medium-medium-medium(relentless_same)-medium",
        },
        "image_vocabulary": {
            "keywords": ["institutional corridor", "impossible bureaucracy",
                         "clean lines with subtle wrongness", "door that leads nowhere",
                         "fluorescent institutional light", "scale distortion",
                         "empty waiting room", "metamorphic body"],
            "color_palette": ["institutional beige", "corridor green",
                              "fluorescent white", "document manila",
                              "ink stamp blue", "grey suit"],
            "compositional_rules": [
                "Symmetrical institutional framing with one element disrupted",
                "Vanishing-point corridors implying infinite recession",
                "Flat even lighting — no drama, no escape into shadow",
                "Human figure scaled slightly wrong relative to architecture",
            ],
        },
    },

    "shonagon": {
        "id": "shonagon",
        "display_name": "Sei Shōnagon-esque",
        "language_origin": "Japanese (Classical)",
        "coordinates": {
            "syntactic_density":    0.15,
            "sensory_concreteness": 0.95,
            "ornamental_register":  0.40,
            "tension_visibility":   0.25,
            "tension_temporality":  0.15,
            "reality_stability":    0.85,
            "interiority":          0.65,
            "temporal_mode":        0.10,
        },
        "signature_moves": [
            "List-based observation as primary literary form",
            "Aesthetic judgment as the content — 'things that are...'",
            "Radical sensory specificity about transient moments",
            "Categorical thinking — grouping experiences by quality",
            "Brevity with maximum sensory payload per word",
        ],
        "text_vocabulary": {
            "conjunctions": ["and", "—", ";"],
            "sentence_starters": ["Things that", "In spring", "It is",
                                  "A", "The", "One"],
            "forbidden": ["basically", "essentially", "in conclusion",
                          "furthermore", "moreover"],
            "register": "Elegant brevity — each word carries maximum sensory weight",
            "paragraph_rhythm": "fragment-fragment-short-fragment-observation",
        },
        "image_vocabulary": {
            "keywords": ["seasonal specificity", "single perfect object",
                         "morning light on silk", "rain on veranda",
                         "ink brush precision", "negative space as reverence",
                         "insect on flower", "paper screen diffused light"],
            "color_palette": ["cherry blossom pink", "ink black", "rice paper white",
                              "moss green", "persimmon orange", "dawn grey"],
            "compositional_rules": [
                "Single subject dominating frame — no competing elements",
                "Extreme negative space ratio minimum 1:5 subject to ground",
                "Natural light only — seasonal quality explicit",
                "Shallow depth isolating one perfect detail",
            ],
        },
    },

    "lispector": {
        "id": "lispector",
        "display_name": "Clarice Lispector-esque",
        "language_origin": "Brazilian Portuguese",
        "coordinates": {
            "syntactic_density":    0.55,
            "sensory_concreteness": 0.60,
            "ornamental_register":  0.55,
            "tension_visibility":   0.65,
            "tension_temporality":  0.50,
            "reality_stability":    0.50,
            "interiority":          0.95,
            "temporal_mode":        0.45,
        },
        "signature_moves": [
            "Language turning to examine itself mid-sentence",
            "Interior stream — consciousness as the event",
            "The body as epistemological instrument",
            "Recursive self-interruption and self-correction",
            "Philosophical viscerality — abstract ideas with physical weight",
        ],
        "text_vocabulary": {
            "conjunctions": ["but", "and yet", "or rather", "—",
                             "that is", "no"],
            "sentence_starters": ["She", "It was", "What she",
                                  "The", "But", "No—"],
            "forbidden": ["simply", "obviously", "naturally", "of course"],
            "register": "Philosophical intimate — thought caught in the act of thinking",
            "paragraph_rhythm": "medium-long(spiraling)-short(correction)-medium-fragment",
        },
        "image_vocabulary": {
            "keywords": ["extreme close-up", "organic texture as landscape",
                         "introspective gaze vector", "skin as terrain",
                         "interior light", "mirror self-regard",
                         "domestic object elevated to icon", "visceral abstraction"],
            "color_palette": ["skin tones", "interior shadow", "egg white",
                              "blood warmth", "kitchen tile", "afternoon gold"],
            "compositional_rules": [
                "Extreme close framing — face fills frame edge to edge",
                "Shallow depth of field f/1.4-f/2.0 equivalent",
                "Gaze vector direct to viewer or at own reflection",
                "Organic textures rendered at macro scale",
            ],
        },
    },
}


# ---------------------------------------------------------------------------
# Parameter names — ordered list for dynamics integration
# ---------------------------------------------------------------------------

PARAMETER_NAMES: list[str] = [
    "syntactic_density",
    "sensory_concreteness",
    "ornamental_register",
    "tension_visibility",
    "tension_temporality",
    "reality_stability",
    "interiority",
    "temporal_mode",
]


# ---------------------------------------------------------------------------
# Utility: extract coordinates only (for dynamics / distance computation)
# ---------------------------------------------------------------------------

def get_coordinates(author_id: str) -> AuthorCoordinates:
    """Return raw 8D coordinates for an author. Layer 1 lookup."""
    if author_id not in AUTHOR_CATALOG:
        raise ValueError(
            f"Unknown author '{author_id}'. "
            f"Available: {list(AUTHOR_CATALOG.keys())}"
        )
    return AUTHOR_CATALOG[author_id]["coordinates"]


def get_all_coordinates() -> dict[str, AuthorCoordinates]:
    """Return coordinates for all authors. Layer 1 lookup."""
    return {aid: entry["coordinates"] for aid, entry in AUTHOR_CATALOG.items()}


def get_author_ids() -> list[str]:
    """Return all available author IDs."""
    return list(AUTHOR_CATALOG.keys())
