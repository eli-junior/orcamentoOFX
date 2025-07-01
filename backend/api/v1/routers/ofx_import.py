from ninja import Router, File
from ninja.files import UploadedFile

from ..services.ingest_data import ofx_reader

router = Router()


@router.post("/ofx")
def import_ofx(request, file: UploadedFile = File(...)):
    transactions = ofx_reader(file)
    return transactions
