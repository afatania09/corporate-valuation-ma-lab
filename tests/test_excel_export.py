from io import BytesIO
from openpyxl import load_workbook
from valuation_lab.excel_export import lbo_workbook

def test_lbo_workbook():
    wb=load_workbook(BytesIO(lbo_workbook(26,20,3,12,12,6)))
    ws=wb["LBO"]
    assert ws["B2"].value==26
    assert ws["B8"].value=="=B2-B3"
    assert ws["B10"].value=="=MAX(0,B9-B6)"
    assert ws["B12"].value=="=B11^(1/B7)-1"
    assert "Notes" in wb.sheetnames
