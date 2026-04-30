# models/repo_model.py
from pydantic import BaseModel, Field, HttpUrl

# 1. Handle Nested JSON first
# GitHub returns an "owner" object inside the main repository object
class Owner(BaseModel):
    login: str
    id: int
    type: str

# 2. The Main Repository Model
class RepositoryModel(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    html_url: HttpUrl # Validates that this is an actual, properly formatted URL
    description: str | None = None # Handles cases where description might be null
    owner: Owner # Nests the Owner model we created above