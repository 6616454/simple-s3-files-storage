from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Query

from src.db.repositories.holder import HolderRepository
from src.di import provide_current_user, provide_file_service, uow_provider
from src.schemas.file import OutputFile
from src.schemas.user import UserSchema
from src.services.file import FileService

router = APIRouter(
    prefix='/file',
    tags=['File']
)


@router.post('/upload', response_model=list[OutputFile])
async def uploading_files(
        dir: Optional[str] = Query(None),
        user: UserSchema = Depends(provide_current_user),
        files: list[UploadFile] = File(...),
        file_service: FileService = Depends(provide_file_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await file_service.upload_files(
        user_path=user.user_path,
        user_id=user.id,
        dir=dir,
        files=files,
        uow=uow
    )


@router.get('/list', response_model=list[OutputFile])
async def get_my_files(
        user: UserSchema = Depends(provide_current_user),
        file_service: FileService = Depends(provide_file_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await file_service.get_user_files(user.id, uow)


@router.get('/download/')
async def download_files(
        dir: Optional[str] = Query(None),
        file_id: Optional[int] = Query(None),
        compr_type: Optional[str] = Query(None),
        user: UserSchema = Depends(provide_current_user),
        file_service: FileService = Depends(provide_file_service),
        uow: HolderRepository = Depends(uow_provider)
):
    return await file_service.download_files(dir, file_id, user.id, user.user_path, compr_type, uow)
