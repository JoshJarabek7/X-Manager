"""Module containing the ArchiveExtract class"""

import json
import shutil
import zipfile
from pathlib import Path
from fastapi import UploadFile, HTTPException


class ArchiveExtract:
    """Class containing methods for extracting data from the X archive file."""

    def extract_from_js(self, path: str):
        """Extracts JSON data from a JavaScript file"""
        with open(path, "r", encoding="utf-8") as f:
            js_content = f.read()

        json_start = js_content.find("[{")
        json_end = js_content.rfind("}]") + 2
        json_data = json.loads(js_content[json_start:json_end])

        return json_data

    def unzip_and_grab_data(self, zip_file: UploadFile):
        """Extract the data directory from the uploaded archive folder and add it to cwd"""
        try:
            with zipfile.ZipFile(zip_file.file) as zip_ref:
                temp_dir = Path("temp_unzip")
                temp_dir.mkdir(parents=True, exist_ok=True)
                zip_ref.extractall(temp_dir)

            extracted_data_dir = temp_dir / "data"
            if not extracted_data_dir.exists():
                raise FileNotFoundError("Data directory not found in the zip file")

            target_data_dir = Path.cwd() / "data"
            if target_data_dir.exists():
                shutil.rmtree(target_data_dir)

            shutil.move(str(extracted_data_dir), target_data_dir)

        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Invalid zip file")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)
