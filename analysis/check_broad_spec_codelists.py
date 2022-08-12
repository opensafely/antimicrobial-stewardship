from codelists import (
    BRIT_broad_spectrum,
    BRIT_antibiotics,
    broad_spectrum_antibiotics_codes,
    antibacterials_codes
)

BRIT_BS_count = len(BRIT_broad_spectrum)
BRIT_AB_count = len(BRIT_antibiotics)
OS_BS_count = len(broad_spectrum_antibiotics_codes)
OS_AB_count = len(antibacterials_codes)

BRIT_BS_not_in_AB = [b for b in BRIT_broad_spectrum if b not in BRIT_antibiotics]
OS_BS_not_in_AB = [o for o in broad_spectrum_antibiotics_codes if o not in antibacterials_codes]

with open('output/broad_spectrum_codelist_report.txt', 'w')  as f:
    f.write(f"BRIT antibiotics:{BRIT_AB_count}\n")
    f.write(f"BRIT broad spectrum:{BRIT_BS_count}\n")
    f.write(f"OpenSAFELY antibiotics:{OS_AB_count}\n")
    f.write(f"OpenSAFELY broad spectrum:{OS_BS_count}\n")
    if len(BRIT_BS_not_in_AB) >0:
        f.write(f"BRIT broad spectrum not in AB:{len(BRIT_BS_not_in_AB >0)}\n")
        for b in BRIT_BS_not_in_AB:
            f.write(f"{b}\n")
    if len(OS_BS_not_in_AB) >0:
        f.write(f"OpenSAFELY broad spectrum not in AB:{len(OS_BS_not_in_AB >0)}\n")
        for b in OS_BS_not_in_AB:
            f.write(f"{b}\n")