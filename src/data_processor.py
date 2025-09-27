import json
from datetime import datetime

class DataProcessor:

    def __init__(self, input_file="data/markets_raw.json", output_file="data/markets_cleaned.json"):
        self.input_file = input_file
        self.output_file = output_file



    def process_markets(self):
        with open(self.input_file) as f:
            market_full = json.load(f)
            markets = market_full.get("data", [])

        processed = []
        for m in markets:
            #an example data processor which collets all active markets that are not close yet
            if m.get("active") & m.get("closed") == False:
                processed.append({
                    "market_id": m.get("market_id"),
                    "condition_id": m.get("condition_id"),
                    "question": m.get("question"),
                    "end_date": self._parse_date(m.get("end_date_iso")),
                    "active": m.get("active"),
                    "closed": m.get("closed"),
                    "tokens": [
                        {
                            "token_id": t.get("token_id"),
                            "outcome": t.get("outcome"),
                            "price": t.get("price")
                        }
                        for t in m.get("tokens", [])
                    ]
                })

        with open(self.output_file, "w") as f:
            json.dump(processed, f, indent=4)

        print(f"[INFO] Processed {len(processed)} markets and saved to {self.output_file}")

    def _parse_date(self, date_str):
        if date_str:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).isoformat()
        return None
    
    

