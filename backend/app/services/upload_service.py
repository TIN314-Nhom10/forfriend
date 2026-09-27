import os
import uuid
from fastapi import HTTPException, UploadFile, status
from app.config import settings

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}

ALLOWED_PDF_EXTENSIONS = {".pdf"}
ALLOWED_PDF_TYPES = {"application/pdf"}


class UploadService:
    """Service phụ trách upload và lưu trữ file cục bộ (Zero Cloud / Zero S3)."""

    def __init__(self) -> None:
        self.base_dir = os.path.abspath(settings.UPLOAD_DIR)
        self.student_ids_dir = os.path.join(self.base_dir, "student-ids")
        self.cvs_dir = os.path.join(self.base_dir, "cvs")
        os.makedirs(self.student_ids_dir, exist_ok=True)
        os.makedirs(self.cvs_dir, exist_ok=True)

    async def upload_student_id(self, file: UploadFile) -> str:
        """
        Upload ảnh thẻ sinh viên:
        - Chỉ chấp nhận ảnh (JPG, PNG, WEBP)
        - Giới hạn tối đa 5MB
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên file không hợp lệ",
            )

        _, ext = os.path.splitext(file.filename.lower())
        if ext not in ALLOWED_IMAGE_EXTENSIONS or (
            file.content_type and file.content_type not in ALLOWED_IMAGE_TYPES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chỉ chấp nhận file ảnh định dạng JPG, PNG hoặc WEBP",
            )

        content = await file.read()
        if len(content) > settings.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dung lượng ảnh vượt quá giới hạn cho phép ({settings.MAX_IMAGE_SIZE // (1024 * 1024)}MB)",
            )

        filename = f"{uuid.uuid4().hex}{ext}"
        destination = os.path.join(self.student_ids_dir, filename)

        with open(destination, "wb") as f:
            f.write(content)

        return f"/uploads/student-ids/{filename}"

    async def upload_cv(self, file: UploadFile) -> str:
        """
        Upload file CV:
        - Chỉ chấp nhận định dạng PDF
        - Giới hạn tối đa 10MB
        """
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên file không hợp lệ",
            )

        _, ext = os.path.splitext(file.filename.lower())
        if ext not in ALLOWED_PDF_EXTENSIONS or (
            file.content_type and file.content_type not in ALLOWED_PDF_TYPES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Chỉ chấp nhận file tài liệu định dạng PDF",
            )

        content = await file.read()
        if len(content) > settings.MAX_CV_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dung lượng CV vượt quá giới hạn cho phép ({settings.MAX_CV_SIZE // (1024 * 1024)}MB)",
            )

        filename = f"{uuid.uuid4().hex}.pdf"
        destination = os.path.join(self.cvs_dir, filename)

        with open(destination, "wb") as f:
            f.write(content)

        return f"/uploads/cvs/{filename}"


upload_service = UploadService()
