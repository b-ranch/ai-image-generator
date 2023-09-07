import openai
import dotenv
import os
import requests
from PIL import Image
from fastapi import FastAPI, Form, Request
from fastapi.templating import Jinja2Templates

dotenv.load_dotenv()

openai.api_key = os.getenv('API_KEY')

app = FastAPI()

templates = Jinja2Templates(directory='templates')


@app.get('/')
async def root(request: Request):
    context = {'request': request, 'message': 'Hello, FastAPI with JinJa2!'}
    return templates.TemplateResponse('index.html', {'request': request, **context})


@app.post('/')
async def get_data(
    request: Request,
    text: str = Form(...),
):
    url1 = generate(text)
    response = requests.get(url1)
    with open('img.png', 'wb') as f:
        f.write(response.content)

    result = Image.open('/storage/img.png').convert('RGBA')
    result.save('/storage/img_rgba.png', 'PNG')
    context = {'request': request, 'message': 'Hello', 'url': url1}
    return templates.TemplateResponse('detail.html', {'request': request, **context})


def generate(text):
    res = openai.Image.create(
        # text describing the generated image
        # image=open('img_rgba.png', 'rb'),
        # mask=open('mask.png', 'rb'),
        prompt=text,
        # number of images to generate
        n=1,
        # size of each generated image
        size='256x256',
    )
    # returning the URL of one image as
    # we are generating only one image
    return res['data'][0]['url']


# Image.open(response.raw)
