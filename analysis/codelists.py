######################################

# Some covariates used in the study are created from codelists of clinical conditions or 
# numerical values available on a patient's records.
# This script fetches all of the codelists identified in codelists.txt from OpenCodelists.

######################################


# --- IMPORT STATEMENTS ---

## Import code building blocks from cohort extractor package
import code
from cohortextractor import (codelist_from_csv, combine_codelists)


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

### All antibacterials
antibacterials_codes= codelist_from_csv(
  "codelists/opensafely-antibacterials.csv",
  system = "snomed",
  column = "dmd_id"
)

## BRIT codelists
BRIT_nitrofurantoin = codelist_from_csv(
  "codelists/user-yayang-codes_ab_type_nitrofurantoincsv.csv",
  system = "snomed",
  column = "dmd_id"
)

BRIT_trimethoprim = codelist_from_csv(
  "codelists/user-yayang-codes_ab_type_trimethoprimcsv.csv",
  system = "snomed",
  column = "dmd_id"
)

BRIT_broad_spectrum = codelist_from_csv(
  "codelists/user-rriefu-broad-spectrum-antibiotics.csv",
  system = "snomed",
  column = "dmd_id"
)

BRIT_antibiotics = codelist_from_csv(
  "codelists/user-rriefu-antibiotics_dmd.csv",
  system = "snomed",
  column = "dmd_id"
)

Billy_broad_spectrum = codelist_from_csv(
  "codelists/user-BillyZhongUOM-broad_spec_op_codelist.csv",
  system = "snomed",
  column = "dmd"
)

BRIT_nitrofurantoin_trimethoprim = combine_codelists(BRIT_trimethoprim,BRIT_nitrofurantoin)

## JM reimplementations

jm_trimethoprim = codelist_from_csv(
  "codelists/user-jon_massey-trimethoprim-ingredient-based-drugs.csv",
  system = "snomed",
  column = "dmd_id"
)

jm_nitrofurantoin = codelist_from_csv(
  "codelists/user-jon_massey-nitrofurantoin-vtm-based-drugs.csv",
  system = "snomed",
  column = "id"
)

jm_nitrofurantoin_trimethoprim = combine_codelists(jm_trimethoprim,jm_nitrofurantoin)

jm_ktt9 = codelist_from_csv(
  "codelists/user-jon_massey-ktt9-replication-dmd.csv",
  system = "snomed",
  column = "dmd_id"
)