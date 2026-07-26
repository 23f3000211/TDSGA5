from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
 
app = FastAPI()
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 
def compute_charge(old_price, new_price, days_remaining, days_in_actual_month, spec):
    price_diff = new_price - old_price
    if spec == "v1":
        divisor = 30
    elif spec == "v2":
        divisor = days_in_actual_month
    else:
        raise ValueError(f"Unknown spec: {spec}")
    return price_diff * (days_remaining / divisor)
 
 
@app.post("/")
async def prorate(request: Request):
    body = await request.json()
 
    old_price = body["old_price"]
    new_price = body["new_price"]
    days_remaining = body["days_remaining"]
    days_in_actual_month = body["days_in_actual_month"]
    spec = body["spec"]
 
    charge = compute_charge(old_price, new_price, days_remaining, days_in_actual_month, spec)
 
    return JSONResponse({"charge": charge})
 
 
@app.get("/")
async def health():
    return {"status": "ok"}
