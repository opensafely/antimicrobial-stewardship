######################################

# This script provides the formal specification of the study data that will be extracted from
# the OpenSAFELY database.

######################################


# --- IMPORT STATEMENTS ---

## Import code building blocks from cohort extractor package
from cohortextractor import StudyDefinition, patients, Measure

## Import codelists from codelist.py (which pulls them from the codelist folder)
from codelists import (
    antibacterials_codes,
    infection_codes,
    learning_disability_codes,
    broad_spectrum_antibiotics_codes,
    carehome_primis_codes,
    trimethoprim_codes,
    nitrofurantoin_and_trimethoprim_codes,
    delayed_antibiotics_prescriptions_codes,
    serious_mental_illness_codes,
)

## Import measures config (also used in analysis scripts)
from measures import measures_kwargs

## Import pivot helper functions
from study_definition_functions import (
    pivot_clinical_event_dates,
    pivot_clinical_event_codes,
    pivot_medication_event_codes,
    pivot_medication_event_dates,
)

# DEFINE STUDY POPULATION ---

## Define study time variables
from datetime import datetime

start_date = "2019-01-01"
end_date = datetime.today().strftime("%Y-%m-%d")

## Pivoted infection variables
infection_date_variables = pivot_clinical_event_dates("infection", infection_codes, 5)
infection_code_variables = pivot_clinical_event_codes("infection",infection_codes,5)

## Pivoted antibiotics variables
antibiotics_date_variables = pivot_medication_event_dates("antibiotic",antibacterials_codes,5)
antibiotics_code_variables = pivot_medication_event_codes("antibiotic",antibacterials_codes,5)

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
        NOT has_died
        AND
        registered
        AND
        age
        AND
        has_follow_up_previous_year
        AND
        (sex = "M" OR sex = "F")
        """,
        has_died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
        ),
        registered=patients.satisfying(
            "registered_at_start",
            registered_at_start=patients.registered_as_of("index_date"),
        ),
        has_follow_up_previous_year=patients.registered_with_one_practice_between(
            start_date="index_date - 1 year",
            end_date="index_date",
            return_expectations={"incidence": 0.95},
        ),
    ),
    ## Measures
    ## All antibacterials
    antibiotics_prescriptions=patients.with_these_medications(
        antibacterials_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),
    ## Broad spectrum antibiotics
    broad_spectrum_antibiotics_prescriptions=patients.with_these_medications(
        broad_spectrum_antibiotics_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
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
    ## Delayed prescriptions for antibiotics
    delayed_antibiotics_prescriptions=patients.with_these_medications(
        delayed_antibiotics_prescriptions_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    delayed_antibiotics_prescriptions_event_code=patients.with_these_medications(
        delayed_antibiotics_prescriptions_codes,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        return_expectations={
            "category": {"ratios": {str(417576009): 0.9, str(699840007): 0.1}},
        },
    ),
    ## Consultations with GP result in a antibiotic
    ## Record of a coded infection clinical event on same day as an antibiotic
    infections = patients.with_these_clinical_events(infection_codes,
        between=["index_date", "last_day_of_month(index_date)"],
         returning="number_of_matches_in_period",
        return_expectations={
            "int": {"distribution": "normal", "mean": 3, "stddev": 1},
            "incidence": 0.5,
        },
    ),

    **infection_date_variables,
    **infection_code_variables,
    **antibiotics_date_variables,
    **antibiotics_code_variables,
    
    ## Course Duration (not currently possible)


    ## Demographic and clinical sub-groups
    ### Age
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
            "incidence": 0.001,
        },
    ),
    ### Age Band
    age_band=patients.categorised_as(
        {
            "0": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80+": """ age >=  80 AND age < 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.001,
                    "0-19": 0.124,
                    "20-29": 0.125,
                    "30-39": 0.125,
                    "40-49": 0.125,
                    "50-59": 0.125,
                    "60-69": 0.125,
                    "70-79": 0.125,
                    "80+": 0.125,
                }
            },
        },
    ),
    ### Care home
    care_home=patients.with_these_clinical_events(
        carehome_primis_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    ### Sex
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
        }
    ),
    ### Region - NHS England 9 regions
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.2,
                    "South West": 0.1,
                    "South East": 0.1,
                },
            },
        },
    ),
    ### Index of multiple deprivation
    imd=patients.categorised_as(
        {
            "0": "DEFAULT",
            "1": """index_of_multiple_deprivation >=1 AND index_of_multiple_deprivation < 32844*1/5""",
            "2": """index_of_multiple_deprivation >= 32844*1/5 AND index_of_multiple_deprivation < 32844*2/5""",
            "3": """index_of_multiple_deprivation >= 32844*2/5 AND index_of_multiple_deprivation < 32844*3/5""",
            "4": """index_of_multiple_deprivation >= 32844*3/5 AND index_of_multiple_deprivation < 32844*4/5""",
            "5": """index_of_multiple_deprivation >= 32844*4/5 """,
        },
        index_of_multiple_deprivation=patients.address_as_of(
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0": 0.01,
                    "1": 0.20,
                    "2": 0.20,
                    "3": 0.20,
                    "4": 0.20,
                    "5": 0.19,
                }
            },
        },
    ),
    ### Astma/COPD
    ### Serious Mental Illness
    serious_mental_illness=patients.with_these_clinical_events(
        serious_mental_illness_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    ### Learning disabilities
    learning_disability=patients.with_these_clinical_events(
        learning_disability_codes,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    ## Variables
    ### Practice
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
)


# --- DEFINE MEASURES ---
measures = [Measure(**kw) for kw in measures_kwargs]
