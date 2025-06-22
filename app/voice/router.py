import os

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

from app.voice.VoiceRecognizer import VoiceRecognizer

router = APIRouter(prefix="/voice", tags=["voice"])


@router.get("/recorder.js", response_class=FileResponse)
def get_javascript():
    file_name = 'recorder.js'
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    return FileResponse(file_path)


@router.post('/process/')
async def process_voice(audiofile: UploadFile = File(...)):
    vr = VoiceRecognizer()
    audio_content = await audiofile.read()
    text = vr.process_voice(audio_content)
    text = vr.correct_translit(text)
    return {"text": text}
