## Import code building blocks from cohort extractor package
from cohortextractor import StudyDefinition, patients

## Import codelists from codelist.py (which pulls them from the codelist folder)
from codelists import (
    BRIT_broad_spectrum,
    BRIT_antibiotics,
    broad_spectrum_antibiotics_codes,
    antibacterials_codes
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
        has_brit_antibiotic OR
        has_os_antibiotic
        """,
        has_brit_antibiotic= patients.with_these_medications(
            BRIT_antibiotics,
            between=[start_date,end_date],
            returning="binary_flag"
        ),
        has_os_antibiotic= patients.with_these_medications(
            antibacterials_codes,
            between=[start_date,end_date],
            returning="binary_flag"
        ),
    ),
    
    ## OpenSAFELY
    OS_antibiotic_prescriptions=patients.with_these_medications(
        antibacterials_codes,
        between=[start_date,end_date],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    
    OS_broad_spectrum_prescriptions=patients.with_these_medications(
        broad_spectrum_antibiotics_codes,
        between=[start_date,end_date],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    ## BRIT
    BRIT_antibiotic_prescriptions=patients.with_these_medications(
        BRIT_antibiotics,
        between=[start_date,end_date],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    
    BRIT_broad_spectrum_prescriptions=patients.with_these_medications(
        BRIT_broad_spectrum,
        between=[start_date,end_date],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
)
