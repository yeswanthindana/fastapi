import uvicorn
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
import models, oauth2
import utils
from database import engine
import routers.user as user
import routers.role as role
import routers.organization as organization
import routers.authentication as authentication
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
app.include_router(user.router, dependencies=[Depends(utils.verify_unique_keys), Depends(oauth2.get_current_user)])
app.include_router(role.router, dependencies=[Depends(utils.verify_unique_keys), Depends(oauth2.get_current_user)])
app.include_router(organization.router, dependencies=[Depends(utils.verify_unique_keys), Depends(oauth2.get_current_user)])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)