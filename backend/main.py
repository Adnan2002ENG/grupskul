from fastapi import FastAPI, HTTPException, Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from supabase_client import supabase
from auth_guard import verify_token

app = FastAPI()

# CORS (Frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Customize OpenAPI to enable Authorize 🔐 button
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="GrupSkul API",
        version="1.0.0",
        description="Backend for GrupSkul MVP",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "GrupSkul backend is working!"}

# ✅ Signup
@app.post("/signup")
def signup(email: str = Body(...), password: str = Body(...)):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user is None:
            raise HTTPException(status_code=400, detail=str(response))
        return {"message": "Signup successful", "user": response.user.email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Login
@app.post("/login")
def login(email: str = Body(...), password: str = Body(...)):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {
            "message": "Login successful",
            "user": response.user.email,
            "session": response.session.access_token
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Protected route with JWT
@app.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {"message": f"Hello, {user['email']} — you're authenticated!"}
