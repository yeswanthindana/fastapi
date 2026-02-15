
import uvicorn
from fastapi import FastAPI, Depends
from . import models, oauth2
from .utils import verify_unique_keys
from .database import engine
from .routers import user, role, organization, authentication
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(authentication.router)
app.include_router(user.router, dependencies=[Depends(verify_unique_keys), Depends(oauth2.get_current_user)])
app.include_router(role.router, dependencies=[Depends(verify_unique_keys), Depends(oauth2.get_current_user)])
app.include_router(organization.router, dependencies=[Depends(verify_unique_keys), Depends(oauth2.get_current_user)])


if __name__ == "__main__":
    uvicorn.run("web_api.main:app", host="0.0.0.0", port=8000, reload=True)