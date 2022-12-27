from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File

from src.db.repositories.holder import HolderRepository
from src.di import provide_current_user, provide_file_service, uow_provider
from src.schemas.file import OutputFile
from src.schemas.user import UserSchema
from src.services.file import FileService

router = APIRouter(
    prefix='/file',
    tags=['File']
)


@router.post('/upload')
async def uploading_files(
        dir: Optional[str] = None,
        user: UserSchema = Depends(provide_current_user),
        files: list[UploadFile] = File(...),
        file_service: FileService = Depends(provide_file_service),
        uow: HolderRepository = Depends(uow_provider)
):
    await file_service.upload_files(
        user_path=user.user_path,
        dir=dir,
        files=files,
        uow=uow
    )
