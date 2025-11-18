from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import akshare as ak
from datetime import datetime

app = FastAPI(title="GFEX Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "GFEX Scraper API", "status": "running"}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "gfex-scraper"
    }

@app.get("/api/gfex/contracts")
def get_gfex_contracts():
    try:
        # Buscar dados de contratos de Lítio da GFEX usando akshare
        df = ak.futures_main_sina(symbol="LC", market="gfex")
        
        if df.empty:
            return {"success": False, "message": "Nenhum dado encontrado"}
        
        contracts = []
        for _, row in df.iterrows():
            contracts.append({
                "contract_code": row.get("symbol", ""),
                "opening_price": float(row.get("open", 0)),
                "highest_price": float(row.get("high", 0)),
                "lowest_price": float(row.get("low", 0)),
                "latest_price": float(row.get("trade", 0)),
                "up_down": float(row.get("change", 0)),
                "up_down_percentage": float(row.get("changepercent", 0)),
                "buying_price": float(row.get("buy", 0)),
                "selling_price": float(row.get("sell", 0)),
                "purchase_quantity": int(row.get("volume", 0)),
                "selling_quantity": int(row.get("amount", 0)),
                "turnover": int(row.get("amount", 0)),
                "position_volume": int(row.get("hold", 0)),
                "closing_price": "--",
                "settlement_price": float(row.get("settlement", 0)),
                "yesterday_closing": float(row.get("preclose", 0)),
                "yesterday_settlement": float(row.get("presettlement", 0))
            })
        
        aggregated = {
            "category": "Lithium Carbonate",
            "transactions": sum(c["turnover"] for c in contracts),
            "position": sum(c["position_volume"] for c in contracts)
        }
        
        return {
            "success": True,
            "contracts": contracts,
            "aggregated": aggregated
        
