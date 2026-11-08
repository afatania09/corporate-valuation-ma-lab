"""Entry and exit multiple sensitivity for a linked acquisition case."""
from dataclasses import replace
from .acquisition_model import model_acquisition

def deal_sensitivity(base, entry_multiples, exit_multiples):
    if not entry_multiples or not exit_multiples:
        raise ValueError("entry and exit multiple ranges required")
    output = []
    for entry in entry_multiples:
        for exit_ in exit_multiples:
            model = model_acquisition(replace(base, entry_multiple=entry,
                                             exit_multiple=exit_))
            output.append({"entry_multiple": entry, "exit_multiple": exit_,
                           "sponsor_equity": model["sponsor_equity"],
                           "exit_equity": model["exit_equity"],
                           "moic": model["moic"], "irr": model["irr"]})
    return output
