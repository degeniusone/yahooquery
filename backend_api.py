from fastapi import FastAPI, Query as FastAPIQuery, Body
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Import TradingView Screener and yahooquery
try:
    from tradingview_screener import Query as ScreenerQuery, col as screener_col
except ImportError:
    ScreenerQuery = None
    screener_col = None

try:
    from yahooquery import Ticker
except ImportError:
    Ticker = None

app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TickerRequest(BaseModel):
    symbols: List[str]
    modules: Optional[List[str]] = None

@app.get("/api/ticker")
def ticker_data(
    symbols: List[str] = FastAPIQuery(..., description="Ticker symbols"),
    modules: Optional[List[str]] = FastAPIQuery(None, description="Optional modules to fetch")
):
    if Ticker is None:
        return {"error": "ticker package not installed"}
    try:
        ticker = Ticker(symbols)
        if modules:
            data = ticker.all_modules
            filtered = {sym: {mod: data[sym].get(mod) for mod in modules if mod in data[sym]} for sym in data}
            return filtered
        else:
            return ticker.summary_detail
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/screener")
def screener_data(
    fields: List[str] = FastAPIQuery(["name", "close", "volume"], description="Fields to select"),
    limit: int = 50
):
    if ScreenerQuery is None:
        return {"error": "screener package not installed"}
    try:
        q = ScreenerQuery().select(*fields).limit(limit)
        df = q.get_scanner_data()[1]  # (count, DataFrame)
        return df.head(limit).to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

# --- TradingView Screener Extended Endpoints ---
@app.get("/api/screener/columns")
def screener_columns():
    """List all available columns/fields for TradingView Screener."""
    if screener_col is None:
        return {"error": "screener package not installed"}
    try:
        # screener_col is a module with all columns as attributes
        cols = [c for c in dir(screener_col) if not c.startswith("_")]
        return {"columns": cols}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/screener/models")
def screener_models():
    """List available models (if any) for TradingView Screener."""
    try:
        from tradingview_screener import models as screener_models_mod
        models_list = [c for c in dir(screener_models_mod) if not c.startswith("_")]
        return {"models": models_list}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/screener/query")
def screener_advanced_query(query: dict = Body(...)):
    """Run an advanced TradingView Screener query using POST body."""
    if ScreenerQuery is None:
        return {"error": "screener package not installed"}
    try:
        q = ScreenerQuery()
        if 'select' in query:
            q = q.select(*query['select'])
        if 'where' in query:
            for cond in query['where']:
                q = q.where(getattr(screener_col, cond['column']), cond['op'], cond['value'])
        if 'order_by' in query:
            ob = query['order_by']
            q = q.order_by(getattr(screener_col, ob['column']), ascending=ob.get('ascending', False))
        if 'limit' in query:
            q = q.limit(query['limit'])
        if 'offset' in query:
            q = q.offset(query['offset'])
        df = q.get_scanner_data()[1]
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/screener/technical_rating")
def screener_technical_rating(rating: float = FastAPIQuery(..., description="Technical rating float (-1 to 1)")):
    """Format a technical rating value as a string (e.g., 'Strong Buy')."""
    try:
        from tradingview_screener.util import format_technical_rating
        return {"rating": format_technical_rating(rating)}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/screener/predefined")
def screener_predefined(screen_ids: Optional[List[str]] = FastAPIQuery(None, description="Predefined screeners (e.g. 'most_actives')"), count: int = 25):
    """Return results from predefined TradingView screeners."""
    if ScreenerQuery is None:
        return {"error": "screener package not installed"}
    try:
        # Example: screen_ids could be ['most_actives', 'day_gainers']
        results = {}
        for screen_id in (screen_ids or []):
            q = ScreenerQuery(screen_id).limit(count)
            df = q.get_scanner_data()[1]
            results[screen_id] = df.to_dict(orient="records")
        return results
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "Backend API for ticker and screener data"}
