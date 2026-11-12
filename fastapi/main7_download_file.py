from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filname=uploaded_file.filename
    with open(filname, 'wb') as f:
        f.write(file.read())
