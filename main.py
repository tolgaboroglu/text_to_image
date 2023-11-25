from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from typing import Optional
import uvicorn
import httpx
import json
import io
from PIL import Image
from utils.utils import Utils
from cache import variable_cache
import imgkit
from fastapi.responses import FileResponse 
import os 

app = FastAPI()


class ImageProcessRequest(BaseModel):
    key:str =""
    color: str
    prompt: str
    init_image: str
    width: int = 512
    height: int = 512
    samples: int = 1
    num_inference_steps: str = "30"
    safety_checker: str = "no"
    enhance_prompt: str = "yes"
    guidance_scale: float = 7.5
    strength: float = 0.7
    seed: Optional[None]
    webhook: Optional[None]
    track_id: Optional[None]

class HtmlTemplateModel(BaseModel):
    logo : str
    button_color: str
    punchline_color : str
    punchline: str
    button : str 

async def perform_image_processing(request_data: ImageProcessRequest):
    url = "https://stablediffusionapi.com/api/v3/img2img"

    headers = {
        'Content-Type': 'application/json'
    }

    
    # Convert request_data to a dictionary
    data = request_data.dict()

    # Manipulate the data
    data['prompt'] = data['prompt'] + ".Use anywhere the hex code color " + data['color']

    print(data["prompt"])
    data.pop('color')  # Remove the 'color' field from the dictionary

    check = Utils.is_url(data["init_image"])

    if not check :
        data["init_image"] = Utils.process_local_image(data["init_image"])

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            return response
        except httpx.ReadTimeout as e:
            raise HTTPException(status_code=504, detail="Request timeout: " + str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="HTTP request failed: " + str(e))


import requests

@app.post("/process_image/")
async def process_image(request: Request, image_process_request: ImageProcessRequest):
    response = await perform_image_processing(image_process_request)
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            print(response_json)
            image_url = response_json["output"][0]  # Extract the URL of the generated image
            
            image_response = requests.get(image_url)  # Fetch the image from the URL
            image_content = image_response.content
            variable_cache.gen_image = image_url 
            print(variable_cache.gen_image)
            # Save the image
            with open("output_image.png", "wb") as image_file:
                image_file.write(image_content)
            
            return Response(content=image_content, media_type="image/png",status_code=200) 

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

    raise HTTPException(status_code=response.status_code, detail="Image processing failed")


# Sample route to generate image from HTML content
@app.post("/generate-image/")
async def generate_image(request: Request,html_variable :HtmlTemplateModel):

    try:
        html_content = f"""
        <html>
        <head>
            <title>Dynamic Ad Template</title>
            <style>
                .container {{
                    text-align: center;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .logo {{
                    max-width: 200px;
                }}
                .image {{
                    max-width: 100%;
                    margin-top: 20px;
                }}
                .punchline {{
                    margin-top: 20px;
                    color: {html_variable.punchline_color};
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    margin-top: 20px;
                    border-radius: 5px;
                    text-decoration: none;
                    background-color: {html_variable.button_color};
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <img class="logo" src="{html_variable.logo}" alt="Logo">
                <img class="image" src="{variable_cache.gen_image}" alt="Product Image"> 
                <p class="punchline">Your Punchline Here</p>
                <a href="#" class="button">Learn More</a>
            </div>
        </body>
        </html>
        """

        options = {
            'format': 'png',
            'quality': 100, 
            'encoding': 'utf-8',
            'quiet': ''
        }

        
        # Diğer imgkit konfigürasyonları
        # Set execute permissions for the owner, group, and others
        wkhtmltoimage_path = "wkhtmltopdf/bin/wkhtmltoimage.exe"
        os.chmod(wkhtmltoimage_path, 0o755)
        config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)

        # Diğer işlemleri gerçekleştir
        img = imgkit.from_string(html_content, False, options=options, config=config)

        # Resmi Response olarak döndür
        return Response(content=img, media_type="image/png", status_code=200)

    except Exception as e:
        return str(e), 500


@app.post("/generate-and-process-image/")
async def generate_and_process_image(request: Request, html_variable: HtmlTemplateModel,
                                    image_process_request: ImageProcessRequest):
    try:
        # Generate image from HTML content
        img_response = await generate_image(request, html_variable)

        # Process the generated image
        response = await perform_image_processing(image_process_request)

        if response.status_code == 200:
            try:
                # Save the image
                with open("output_image.png", "wb") as image_file:
                    image_file.write(img_response.content)

                return Response(content=img_response.content, media_type="image/png", status_code=200)

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")

        raise HTTPException(status_code=response.status_code, detail="Image processing failed")

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
## <img class="logo" src="{html_variable.logo}" alt="Logo">
#  <img class="image" src="{variable_cache.gen_image}" alt="Product Image">