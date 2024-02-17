from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
import uvicorn
from google.cloud import storage
from controller import park
import os
from router import login_api, web_api, app_api

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

app.include_router(web_api.router)
app.include_router(app_api.router)
app.include_router(login_api.router)

def download_byte_range(
    bucket_name = "tsmchack2023-bsid-grp4-public-write-bucket", 
    source_blob_name='', 
    start_byte=0, 
    end_byte=99999999, 
    destination_file_name=''):

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    print(blob)
    blob.download_to_filename(destination_file_name, start=start_byte, end=end_byte)

    print(
        "Downloaded bytes {} to {} of object {} from bucket {} to local file {}.".format(
            start_byte, end_byte, source_blob_name, bucket_name, destination_file_name
        )
    )

async def get_img_path():
    return await park.get_all_PARK()
    

if __name__ == "__main__":

    data = park.get_all_PARK()

    SQL_file = []
    for i in range(len(data['response'])):
        SQL_file.append(data['response'][i]['PA_IMAGE'].split('/')[-1])

    server_file = os.listdir('./assets/img/Park_image/')

    for file in SQL_file:
        if file not in server_file:
            download_byte_range(source_blob_name = f'Park_image/{file}' ,destination_file_name = f'./assets/img/Park_image/{file}')

    # uvicorn.run(app)
    uvicorn.run(app, host='10.0.0.2', port=8080)
    # uvicorn.run(app, host='34.81.83.19', port=8080)
    

