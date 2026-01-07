# Apache Tika FastAPI Microservice (FREE)
# --------------------------------------
# Purpose: PDF / DOC / DOCX text extraction
# Used by: Master Job Engine (Accuracy Booster)

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import subprocess
import tempfile
import os

app = FastAPI(title="Apache Tika PDF Extractor")

TIKA_JAR = "tika-app.jar"

@app.get("/")
def health():
    return {"status": "ok", "service": "tika-fastapi"}

@app.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = subprocess.run(
            ["java", "-jar", TIKA_JAR, "-t", tmp_path],
            capture_output=True,
            text=True,
            timeout=60
        )

        os.remove(tmp_path)

        if result.returncode != 0:
            return JSONResponse(
                status_code=500,
                content={"error": "Tika extraction failed"}
            )

        return {
            "text": result.stdout,
            "length": len(result.stdout)
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
                      )
