import pandas as pd

df_input= pd.read_csv('output/input_broad_spec.csv.gz')
OS_antibiotic_prescriptions = df_input['OS_antibiotic_prescriptions'].sum()
OS_broad_spectrum_prescriptions = df_input['OS_broad_spectrum_prescriptions'].sum()
OS_broad_spec_proprtion = OS_broad_spectrum_prescriptions/OS_antibiotic_prescriptions

BRIT_antibiotic_prescriptions = df_input['BRIT_antibiotic_prescriptions'].sum()
BRIT_broad_spectrum_prescriptions = df_input['BRIT_broad_spectrum_prescriptions'].sum()
BRIT_broad_spec_proprtion = BRIT_broad_spectrum_prescriptions/BRIT_antibiotic_prescriptions

Billy_broad_spectrum_prescriptions = df_input['Billy_broad_spectrum_prescriptions'].sum()
Billy_broad_spectrum_proportion = Billy_broad_spectrum_prescriptions/OS_antibiotic_prescriptions

jm_broad_spectrum_prescriptions = df_input['jm_broad_spectrum_prescriptions'].sum()
jm_broad_spectrum_proportion = jm_broad_spectrum_prescriptions/OS_antibiotic_prescriptions

df_output = pd.DataFrame.from_dict(
    { 'codelists': ['OS','BRIT','Billy','JM'],
    'antibiotic_presciprions':[OS_antibiotic_prescriptions,BRIT_antibiotic_prescriptions,OS_antibiotic_prescriptions,OS_antibiotic_prescriptions],
    'broad_spectrum_prescriptions':[OS_broad_spectrum_prescriptions,BRIT_broad_spectrum_prescriptions,Billy_broad_spectrum_prescriptions,jm_broad_spectrum_prescriptions],
    'broad_spectrum_proportion':[OS_broad_spec_proprtion,BRIT_broad_spec_proprtion,Billy_broad_spectrum_proportion,jm_broad_spectrum_proportion],
    })
df_output.to_csv('output/broad_spec_ratio.csv',index=False)