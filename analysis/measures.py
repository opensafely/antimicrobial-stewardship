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
        "denominator": "antibacterial_prescriptions",
        "group_by": groups,
    },
    {
        "id": "trimethoprim_prescription_proportion",
        "numerator": "trimethoprim_prescriptions",
        "denominator": "nitrofurantoin_and_trimethoprim_prescriptions",
        "group_by": groups,
    },
]
