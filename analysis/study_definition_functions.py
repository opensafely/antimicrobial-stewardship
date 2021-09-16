from cohortextractor import patients
from cohortextractor.codelistlib import Codelist
from typing import Dict, List, Tuple


def pivot_event(
    name: str, codelist: Codelist, n: int, patient_function, returning: str, **kwargs
) -> Dict[str, Tuple]:

    between = [
        "index_date" if n == 1 else f"{name}_date_{n-1} + 1 day",
        "last_day_of_month(index_date)",
    ]

    return {
        f"{name}_{returning}_{n}": (
            patient_function(
                codelist=codelist,
                between=between,
                return_first_date_in_period=True,
                returning=returning,
                **kwargs,
            )
        )
    }


def pivot_event_date(
    name: str, codelist: Codelist, n: int, patient_function
) -> Dict[str, Tuple]:
    return pivot_event(
        name=name,
        codelist=codelist,
        n=n,
        patient_function=patient_function,
        returning="date",
        return_expectations={
            "date": {
                "earliest": "index_date",
                "latest": "last_day_of_month(index_date)",
            },
            "rate": "uniform",
            "incidence": 0.3,
        },
        date_format="YYYY-MM-DD"
    )


def pivot_clinical_event_dates(
    name: str, codelist: Codelist, n: int
) -> Dict[str, Tuple]:
    out_dict = {}
    for i in range(1, n + 1):
        out_dict.update(
            pivot_event_date(
                name=name,
                codelist=codelist,
                n=i,
                patient_function=patients.with_these_clinical_events,
            )
        )
    return out_dict


def pivot_medication_event_dates(
    name: str, codelist: Codelist, n: int
) -> Dict[str, Tuple]:
    out_dict = {}
    for i in range(1, n + 1):
        out_dict.update(
            pivot_event_date(
                name=name,
                codelist=codelist,
                n=i,
                patient_function=patients.with_these_medications,
            )
        )
    return out_dict


def pivot_clinical_event_codes(
    name: str, codelist: Codelist, n: int
) -> Dict[str, Tuple]:
    out_dict = {}
    for i in range(1, n + 1):
        out_dict.update(
            pivot_event(
                name=name,
                codelist=codelist,
                n=i,
                patient_function=patients.with_these_clinical_events,
                returning="code",
            )
        )
    return out_dict


def pivot_medication_event_codes(
    name: str, codelist: Codelist, n: int
) -> Dict[str, Tuple]:
    out_dict = {}
    for i in range(1, n + 1):
        out_dict.update(
            pivot_event(
                name=name,
                codelist=codelist,
                n=i,
                patient_function=patients.with_these_medications,
                returning="code",
            )
        )
    return out_dict
