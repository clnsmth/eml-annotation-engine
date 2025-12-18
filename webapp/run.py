from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webapp.config import Config
from webapp.api import router
from webapp.core import ProposalRequest, TermDetails, SubmitterInfo, EMLMetadata, send_email_notification, recommend_for_attribute, recommend_for_geographic_coverage

# Instantiate the FastAPI app
app: FastAPI = FastAPI(title="Semantic EML Annotator Backend")

# Add CORS middleware to allow all origins and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(router)

__all__ = [
    "recommend_for_attribute",
    "recommend_for_geographic_coverage",
    "app",
]

if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)