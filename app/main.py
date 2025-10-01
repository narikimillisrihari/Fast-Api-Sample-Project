from fastapi import FastAPI, Depends, BackgroundTasks, HTTPException
from app import schemas, scraper, crud, dependencies, utils

app = FastAPI(title="Quotes Scraper API")

@app.get("/quotes")
def read_quotes(page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    return crud.get_quotes(skip=skip, limit=page_size)

@app.get("/quotes/{quote_id}")
def read_quote(quote_id: int):
    quote = crud.get_quote(quote_id)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@app.post("/scrape")
def run_scrape(request: schemas.ScrapeRequest, background_tasks: BackgroundTasks,
               api_key: None = Depends(dependencies.verify_api_key)):
    sources = utils.load_sources()
    selected_sources = [s for s in sources if s["name"] == request.source] if request.source != "all" else sources
    if not selected_sources:
        raise HTTPException(status_code=404, detail="Source not found")

    results = []

    def scrape_task():
        for source in selected_sources:
            quotes = scraper.scrape_source(source, max_articles=request.max_articles)
            for q in quotes:
                _, status = crud.create_or_update_quote(q)
                results.append({"url": q.url, "status": status})

    background_tasks.add_task(scrape_task)
    return {"message": "Scrape started", "sources": [s["name"] for s in selected_sources]}
