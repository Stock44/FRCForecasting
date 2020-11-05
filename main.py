import re
import pandas as pd

def filter_qual_matches(match_list):
    qm_pattern = re.compile("\d{4}.*_qm(\d*)")
    is_of_type_series = pd.Series([], dtype=bool)

    match_numbers = pd.Series([], dtype=int)
    for event_match_key in match_list["event_and_match_key"]:
        match_key = qm_pattern.match(event_match_key)

        is_match_qm = match_key is not None
        is_of_type_series = is_of_type_series.append(pd.Series([is_match_qm]), ignore_index=True)

        if not is_match_qm: continue
        match_numbers = match_numbers.append(pd.Series([int(match_key.group(1))]), ignore_index=True)

    qualification_matches = match_list[is_of_type_series]
    match_numbers.index = qualification_matches.index
    qualification_matches.insert(0, "match_number", match_numbers)
    qualification_matches.set_index("match_number", inplace=True)

    return qualification_matches.sort_index()