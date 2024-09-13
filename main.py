from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from rembg import remove
import io
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용, 필요에 따라 특정 도메인으로 변경 가능
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-background/")
async def remove_background(file: UploadFile = File(...)):
    # 업로드된 파일 읽기
    contents = await file.read()
    input_image = Image.open(io.BytesIO(contents))
    
    # 배경 제거
    output_image = remove(input_image)
    
    # 결과 이미지를 임시 파일로 저장
    output_path = "temp_output.png"
    output_image.save(output_path)
    
    # 파일 응답 반환
    return FileResponse(output_path, media_type="image/png", filename="output.png")

# 서버 종료 시 임시 파일 삭제
@app.on_event("shutdown")
def shutdown_event():
    if os.path.exists("temp_output.png"):
        os.remove("temp_output.png")

# uvicorn main:app --reload 명령어로 서버 실행
