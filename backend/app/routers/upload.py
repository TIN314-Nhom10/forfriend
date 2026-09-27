from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.user import FileUploadResponse
from app.services.ai_verification_service import ai_verification_service
from app.services.upload_service import upload_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/api/v1/upload", tags=["Upload"])


@router.post(
    "/student-id",
    response_model=FileUploadResponse,
    summary="Tải lên ảnh thẻ sinh viên & xác thực AI Gemini",
)
async def upload_student_id(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tải lên ảnh thẻ sinh viên để xác thực danh tính qua Gemini Vision:
    - Chấp nhận JPG, PNG, WEBP (tối đa 5MB)
    - Trích xuất tên và trường đối chiếu với hồ sơ sinh viên
    - Gán huy hiệu Verified Student nếu khớp
    """
    content = await file.read()
    await file.seek(0)

    ai_result = await ai_verification_service.verify_student_id(
        image_bytes=content,
        mime_type=file.content_type or "image/jpeg",
        expected_name=current_user.name,
        expected_school=current_user.school,
    )

    url = await upload_service.upload_student_id(file)
    current_user.student_id_card_url = url
    await db.commit()

    return FileUploadResponse(
        url=url,
        message=ai_result.get("message", "Student ID verified"),
        verification=ai_result,
    )


@router.post(
    "/cv",
    response_model=FileUploadResponse,
    summary="Tải lên file CV sinh viên",
)
async def upload_cv(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Tải lên hồ sơ CV cá nhân:
    - Định dạng bắt buộc: PDF
    - Kích thước tối đa 10MB
    - Tự động liên kết URL CV vào hồ sơ của Hero
    """
    url = await upload_service.upload_cv(file)
    current_user.cv_url = url
    await db.commit()
    return FileUploadResponse(url=url)
