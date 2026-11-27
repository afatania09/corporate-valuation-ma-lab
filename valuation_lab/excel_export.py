"""Editable sponsor underwriting workbook; values in consistent monetary units."""
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

def lbo_workbook(entry_ev, entry_debt, exit_ebitda, exit_multiple, exit_debt, years):
    from examples.hilton_lbo_case import scenario
    scenario(entry_ev, entry_debt, exit_ebitda, exit_multiple, exit_debt, years)
    wb=Workbook()
    ws=wb.active
    ws.title="LBO"
    ws.append(["Sponsor underwriting","Value"])
    for label,value in zip(("Entry EV","Entry debt","Exit EBITDA","Exit multiple","Exit debt","Years"),(entry_ev,entry_debt,exit_ebitda,exit_multiple,exit_debt,years)):
        ws.append([label,value])
    for label,formula in [
        ("Entry equity","=B2-B3"),("Exit EV","=B4*B5"),
        ("Exit equity","=MAX(0,B9-B6)"),("MOIC","=B10/B8"),
        ("Annualised return","=B11^(1/B7)-1")]:
        ws.append([label,formula])
    ws["B12"].number_format="0.00%"
    ws["B11"].number_format='0.00"x"'
    for row in range(2,8):
        ws.cell(row,2).font=Font(color="0000FF")
    ws.column_dimensions["A"].width=30
    ws.column_dimensions["B"].width=22
    ws.freeze_panes="B2"
    for cell in ws[1]:
        cell.fill=PatternFill("solid",fgColor="17365D")
        cell.font=Font(color="FFFFFF",bold=True)
    notes=wb.create_sheet("Notes")
    notes.append(["Illustrative model; no interim distributions, fees or actual sponsor returns."])
    notes.append(["Blue inputs are editable. Excel recalculates formulas on opening."])
    notes.column_dimensions["A"].width=100
    out=BytesIO()
    wb.save(out)
    return out.getvalue()
