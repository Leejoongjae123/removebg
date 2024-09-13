from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import shutil
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)
# API 엔드포인트 URL
url = "http://43.201.253.111/remove-background/"

# CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 필요에 따라 특정 도메인으로 변경 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # 파일을 임시로 저장
    temp_file_path = f"/tmp/temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        shutil.copyfileobj(file.file, temp_file)

    # 파일을 읽어서 API에 요청
    with open(temp_file_path, "rb") as temp_file:
        files = {"file": temp_file}
        response = requests.post(url, files=files)

    # 응답 확인 및 결과 반환
    if response.status_code == 200:
        output_file_path = "/tmp/output.png"
        with open(output_file_path, "wb") as output_file:
            output_file.write(response.content)
        return FileResponse(output_file_path, media_type="image/png", filename="output.png")
    else:
        return {"error": f"요청 실패: {response.status_code}"}