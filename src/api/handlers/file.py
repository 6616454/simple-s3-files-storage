import time
from typing import Optional

from fastapi import APIRouter, Depends, UploadFile, File, Query
from starlette.responses import JSONResponse

from src.infrastructure.db.repositories.holder import HolderRepository
from src.api.di import provide_current_user, provide_file_service, uow_provider
from src.api.handlers.responses.file import OutputFile
from src.api.handlers.responses.user import UserSchema
from src.services.file import FileService

router = APIRouter(
    prefix='/file',
    tags=['File']
)


@router.get('/ping')
async def ping(
    uow: HolderRepository = Depends(uow_provider)
):
    start_db = time.time()
    await uow.user_repo.get_by_id(1)
    await uow.file_repo.get_file_by_user_and_id(1, 1)
    finish_db = time.time() - start_db

    start_redis = time.time()
    await uow.redis_repo.set(name='name', value='value')
    await uow.redis_repo.delete(name='name')
    finish_redis = time.time() - start_redis

    start_s3 = time.time()
    await uow.s3_repo.create_bucket('example')
    await uow.s3_repo.delete_bucket('example')
    finish_s3 = time.time() - start_s3

    return JSONResponse(
        status_code=200,
        content={
            'db': round(finish_db, 2),
            'cache': round(finish_redis, 2),
            's3': round(finish_s3, 2)
        }
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
        file_repo=uow.file_repo,
        s3_repo=uow.s3_repo,
        redis_repo=uow.redis_repo
    )


@router.get('/list', response_model=list[OutputFile])
async def get_my_files(
    user: UserSchema = Depends(provide_current_user),
    file_service: FileService = Depends(provide_file_service),
    uow: HolderRepository = Depends(uow_provider)
):
    return await file_service.get_user_files(
        user_id=user.id,
        file_repo=uow.file_repo,
        redis_repo=uow.redis_repo
    )


@router.get('/download/')
async def download_files(
    dir: Optional[str] = Query(None),
    file_id: Optional[int] = Query(None),
    compr_type: Optional[str] = Query(None),
    user: UserSchema = Depends(provide_current_user),
    file_service: FileService = Depends(provide_file_service),
    uow: HolderRepository = Depends(uow_provider)
):
    return await file_service.download_files(
        dir=dir,
        file_id=file_id,
        user_id=user.id,
        user_path=user.user_path,
        compr_type=compr_type,
        file_repo=uow.file_repo,
        s3_repo=uow.s3_repo
    )
