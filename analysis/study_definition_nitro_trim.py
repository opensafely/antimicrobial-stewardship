## Import code building blocks from cohort extractor package
from cohortextractor import StudyDefinition, patients

## Import codelists from codelist.py (which pulls them from the codelist folder)
from codelists import (
    trimethoprim_codes,
    nitrofurantoin_and_trimethoprim_codes,
    BRIT_trimethoprim,
    BRIT_nitrofurantoin_trimethoprim,
    BRIT_nitrofurantoin,
    jm_nitrofurantoin_trimethoprim,
    jm_nitrofurantoin,
    jm_trimethoprim
)

# DEFINE STUDY POPULATION ---

## Define study time variables
start_date = "2019-01-01"
end_date = "2019-12-31"

## Define study population and variables
study = StudyDefinition(
    # Configure the expectations framework
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.1,
    },
    # Set index date to start date
    index_date=start_date,
    # Define the study population
    population=patients.satisfying(
        """
        has_nitro_trim_prescription OR
        has_jm_nitro_trim_prescription
        """,
        has_nitro_trim_prescription = patients.with_these_medications(
            nitrofurantoin_and_trimethoprim_codes,
            between=[start_date,end_date],
            returning="binary_flag"
        ),
        has_jm_nitro_trim_prescription = patients.with_these_medications(
            jm_nitrofurantoin_trimethoprim,
            between=[start_date,end_date],
            returning="binary_flag"
        ),
        has_JM_nitro_trim_prescription = patients.with_these_medications(
            jm_nitrofurantoin_trimethoprim,
            between=[start_date,end_date],
            returning="binary_flag"
        ),
    ),
    
    ## Nitrofurantoin and trimethoprim
    nitrofurantoin_and_trimethoprim_prescriptions=patients.with_these_medications(
        nitrofurantoin_and_trimethoprim_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    ## Trimethoprim
    trimethoprim_prescriptions=patients.with_these_medications(
        trimethoprim_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),

    jm_nitrofurantoin_and_trimethoprim_prescriptions=patients.with_these_medications(
        jm_nitrofurantoin_trimethoprim,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    ## Trimethoprim
    jm_trimethoprim_prescriptions=patients.with_these_medications(
        jm_trimethoprim,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    jm_nitrofurantoin_prescriptions=patients.with_these_medications(
        jm_nitrofurantoin,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    BRIT_nitrofurantoin_and_trimethoprim_prescriptions=patients.with_these_medications(
        BRIT_nitrofurantoin_trimethoprim,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    ## Trimethoprim
    BRIT_trimethoprim_prescriptions=patients.with_these_medications(
        BRIT_trimethoprim,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    BRIT_nitrofurantoin_prescriptions=patients.with_these_medications(
        BRIT_nitrofurantoin,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
)