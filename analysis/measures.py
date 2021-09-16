# --- DEFINE MEASURES ---
groups = [
    "practice",
    "age_band",
    "sex",
    "care_home",
    "region",
    "imd",
    "serious_mental_illness",
    "learning_disability",
]
measures_kwargs = [
    {
        "id": "broad_spectrum_proportion",
        "numerator": "broad_spectrum_antibiotics_prescriptions",
        "denominator": "antibiotic_prescriptions",
        "group_by": groups,
    },
    {
        "id": "trimethoprim_prescription_proportion",
        "numerator": "trimethoprim_prescriptions",
        "denominator": "nitrofurantoin_and_trimethoprim_prescriptions",
        "group_by": groups,
    },
    {
        "id":"infection_match_proportion",
        "numerator":"infection_match_count",
        "denominator":"infections",
        "group_by": groups,
    },
    {
        "id":"antibiotic_match_proportion",
        "numerator":"antibiotic_prescription_match_count",
        "denominator":"antibiotic_prescriptions",
        "group_by": groups,
    },
]
