######################################

# Some covariates used in the study are created from codelists of clinical conditions or 
# numerical values available on a patient's records.
# This script fetches all of the codelists identified in codelists.txt from OpenCodelists.

######################################


# --- IMPORT STATEMENTS ---

## Import code building blocks from cohort extractor package
from cohortextractor import (codelist, codelist_from_csv, combine_codelists)


# --- CODELISTS ---

## Delayed prescriptions for antibiotics
delayed_antibiotics_prescriptions_codes = codelist_from_csv(
  "codelists/user-MillieGreen-delayed-prescriptions-for-antibiotics.csv",
  system = "snomed",
  column = "code",
)

## Record of a coded infection clinical event on same day as an antibiotic
infection_codes = codelist_from_csv(
  "codelists/user-MillieGreen-infection-tmp.csv",
  system = "snomed",
  column = "code",
)

## Patients in long-stay nursing and residential care
carehome_primis_codes = codelist_from_csv(
  "codelists/primis-covid19-vacc-uptake-longres.csv",
  system = "snomed",
  column = "code",
)

### Learning disabilities
learning_disability_codes = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
  system = "snomed",
  column = "code",
)

### Serious Mental Illness
serious_mental_illness_codes = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-mh_cod.csv",
  system = "snomed",
  column = "code",
)

### Broad-spectrum antibiotics
broad_spectrum_antibiotics_codes = codelist_from_csv(
  "codelists/opensafely-co-amoxiclav-cephalosporins-and-quinolones.csv",
  system = "snomed",
  column = "dmd_id"
)

### Nitrofurantoin and trimethoprim
nitrofurantoin_and_trimethoprim_codes = codelist_from_csv(
  "codelists/opensafely-trimethoprim-and-nitrofurantoin.csv",
  system = "snomed",
  column = "dmd_id"
)

### Trimethoprim only
trimethoprim_codes= codelist_from_csv(
  "codelists/opensafely-trimethoprim.csv",
  system = "snomed",
  column = "dmd_id"
)