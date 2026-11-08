from valuation_lab.acquisition_model import AcquisitionInputs, model_acquisition
from valuation_lab.deal_sensitivity import deal_sensitivity
from valuation_lab.audit import audit_manifest

def sample():
    return AcquisitionInputs(100, .06, .24, .03, .05, .10, .25,
                             24, 8, 100, .08, 5, 4, 8, 5)

def test_audit_deterministic_and_sensitive_to_changes():
    a = sample()
    r = model_acquisition(a)
    one = audit_manifest("Acquisition", a, r)
    two = audit_manifest("Acquisition", a, r)
    assert one["sha256"] == two["sha256"]
    changed = audit_manifest("Acquisition", a, r, ["Different source"])
    assert one["sha256"] != changed["sha256"]

def test_entry_exit_sensitivity():
    cells = deal_sensitivity(sample(), [7, 8, 9], [7, 8, 9])
    assert len(cells) == 9
    assert cells[0]["entry_multiple"] == 7
    assert cells[-1]["exit_multiple"] == 9
    assert cells[0]["irr"] > cells[-1]["irr"] or cells[0]["moic"] != cells[-1]["moic"]
    base = model_acquisition(sample())
    center = next(c for c in cells if c["entry_multiple"] == 8 and c["exit_multiple"] == 8)
    assert abs(center["irr"] - base["irr"]) < 1e-12
