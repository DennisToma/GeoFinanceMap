from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from typing import Optional, List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        # Use text() for raw SQL queries
        tables_query = text("SELECT name FROM sqlite_master WHERE type='table'")
        tables = db.execute(tables_query).fetchall()
        
        if tables:
            first_table = tables[0][0]
            sample_query = text(f"SELECT * FROM {first_table} LIMIT 5")
            sample_data = db.execute(sample_query).fetchall()
            
            return {
                "status": "success",
                "tables": [table[0] for table in tables],
                "sample_data": [dict(row._mapping) for row in sample_data]  # Use _mapping to convert to dict
            }
        return {"status": "success", "message": "No tables found"}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
@app.get("/api/stocks")
def get_stocks(
    db: Session = Depends(get_db),
    sector: Optional[str] = None,
    limit: int = Query(default=50, le=100)
):
    try:
        query = "SELECT * FROM stocks"
        if sector:
            query += f" WHERE sector = :sector"
            result = db.execute(text(query), {"sector": sector}).fetchall()
        else:
            result = db.execute(text(query)).fetchall()
        
        return {
            "status": "success",
            "data": [dict(row._mapping) for row in result[:limit]]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/sectors")
def get_sectors(db: Session = Depends(get_db)):
    try:
        query = text("SELECT DISTINCT sector FROM stocks ORDER BY sector")
        result = db.execute(query).fetchall()
        return {
            "status": "success",
            "sectors": [row[0] for row in result]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/stock/{ticker}/data")
def get_stock_data(
    ticker: str,
    db: Session = Depends(get_db),
    limit: int = Query(default=100, le=1000)
):
    try:
        query = text("SELECT * FROM daily_data WHERE ticker = :ticker ORDER BY date DESC LIMIT :limit")
        result = db.execute(query, {"ticker": ticker, "limit": limit}).fetchall()
        return {
            "status": "success",
            "data": [dict(row._mapping) for row in result]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}