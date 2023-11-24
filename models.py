from pydantic import BaseModel


class ImageProcessResponse(BaseModel):
    # Define the fields you expect in the response
    result: str