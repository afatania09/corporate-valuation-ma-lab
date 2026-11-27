"""Historical case, USD millions. Run python -m examples.microsoft_activision_case."""
import json

SOURCE = "https://www.sec.gov/Archives/edgar/data/789019/000095017025100235/msft-20250630.htm"
PRICE = 75408
GOODWILL = 51001
NET_ASSETS = {"cash":12976,"intangibles":21969,"other_assets":2503,
              "long_term_debt":-2799,"long_term_income_taxes":-1946,
              "deferred_income_taxes":-4676,"other_liabilities":-3620}

def analyse():
    net = sum(NET_ASSETS.values())
    goodwill = PRICE-net
    assert goodwill == GOODWILL
    # Illustrative perpetual incremental FCFF hurdle, not management guidance.
    # Price less acquired cash plus acquired long-term debt is an EV proxy.
    ev = PRICE-NET_ASSETS["cash"]-NET_ASSETS["long_term_debt"]
    return {"source":SOURCE,"currency":"USD millions","closed":"2023-10-13",
            "purchase_price":PRICE,"identifiable_net_assets":net,
            "reconstructed_goodwill":goodwill,"goodwill_pct":100*goodwill/PRICE,
            "ev_proxy":ev,
            "illustrative_fcff_hurdles":[
                {"wacc":w,"growth":g,"next_year_fcff":ev*(w-g)}
                for w in (.08,.10,.12) for g in (.02,.03,.04)],
            "warning":"Ex-post PPA; FCFF hurdles are hypothetical, not realised returns or a standalone synergy estimate."}

if __name__ == "__main__":
    print(json.dumps(analyse(),indent=2))
