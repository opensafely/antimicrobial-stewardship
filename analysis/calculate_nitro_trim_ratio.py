import pandas as pd

df_input= pd.read_csv('output/input_nitro_trim.csv.gz')
nitrofurantoin_and_trimethoprim_prescriptions = df_input['nitrofurantoin_and_trimethoprim_prescriptions'].sum()
trimethoprim_prescriptions = df_input['trimethoprim_prescriptions'].sum()
trimethoprim_proportion = trimethoprim_prescriptions/nitrofurantoin_and_trimethoprim_prescriptions

BRIT_nitrofurantoin_and_trimethoprim_prescriptions = df_input['BRIT_nitrofurantoin_and_trimethoprim_prescriptions'].sum()
BRIT_trimethoprim_prescriptions = df_input['BRIT_trimethoprim_prescriptions'].sum()
BRIT_trimethoprim_proportion = BRIT_trimethoprim_prescriptions/BRIT_nitrofurantoin_and_trimethoprim_prescriptions
df_output = pd.DataFrame.from_dict(
    { 'codelists': ['OS','BRIT'],
    'nitrofurantoin_and_trimethoprim_prescriptions':[nitrofurantoin_and_trimethoprim_prescriptions,BRIT_nitrofurantoin_and_trimethoprim_prescriptions],
    'trimethoprim_prescriptions':[trimethoprim_prescriptions,BRIT_trimethoprim_prescriptions],
    'trimethoprim_proportion':[trimethoprim_proportion,BRIT_trimethoprim_proportion],
    })
df_output.to_csv('output/nitro_trim_ratio.csv',index=False)