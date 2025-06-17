from ninja import Router
from typing import List, Dict, Any
from django.db import IntegrityError, transaction
from django.http import JsonResponse # For direct JsonResponse usage if needed outside Ninja's auto-conversion

from ..models import Lancamento
from ..schemas import LancamentoCreateSchema, MessageSchema, ErrorResponseSchema # Using ErrorResponseSchema for detailed errors

router = Router(tags=["Lançamentos"])

# This placeholder function for OFX parsing is not strictly needed here
# because Ninja will parse the incoming JSON payload directly into List[LancamentoCreateSchema].
# If the input were raw text or a file upload, then such a parsing function would be essential.
# def parse_simplified_ofx_data(data: List[Dict[str, Any]]) -> List[LancamentoCreateSchema]:
#     parsed_transactions = []
#     for item in data:
#         try:
#             parsed_transactions.append(LancamentoCreateSchema(**item))
#         except Exception as e:
#             print(f"Skipping item due to parsing/validation error: {item}, Error: {e}")
#     return parsed_transactions


@router.post(
    "/ofx-import",
    response={201: MessageSchema, 400: MessageSchema, 207: Dict[str, Any], 500: MessageSchema},
    summary="Importar Transações (Lista JSON)",
    description=(
        "Recebe uma lista de transações (simulando dados que seriam extraídos de um arquivo OFX) e as importa. "
        "Transações duplicadas (baseadas em data, valor, descrição original e tipo de transação, "
        "que formam um hash único) são ignoradas."
    )
)
def import_ofx_data(request, payload: List[LancamentoCreateSchema]):
    '''
    Endpoint para importar dados de transações a partir de uma lista JSON.
    Simula a importação de dados que seriam parseados de um arquivo OFX.
    Espera uma lista de objetos de transação conformes com LancamentoCreateSchema.

    Respostas:
    - 201: Todas as transações foram importadas com sucesso.
    - 207: Processamento parcial. Algumas transações foram importadas, outras foram ignoradas (duplicadas) ou causaram erros.
    - 400: Erro na requisição (e.g., payload malformado, tratado por Ninja antes de chegar aqui).
    - 500: Erro inesperado no servidor.
    '''
    imported_count = 0
    skipped_due_to_duplicate = 0
    skipped_due_to_error = 0
    error_details = []

    for tx_data in payload:
        try:
            # The hash is generated in Lancamento.save() automatically.
            # status_conciliacao defaults to 'pendente' in the model.
            # data_upload is set by auto_now_add=True in the model.
            lancamento = Lancamento(
                data_transacao=tx_data.data_transacao,
                valor=tx_data.valor,
                descricao_original=tx_data.descricao_original,
                tipo_transacao=tx_data.tipo_transacao
                # Outros campos como categoria_id, etc., são opcionais e podem vir no tx_data se LancamentoCreateSchema os incluir
            )
            # Attempt to save. The model's save() method calculates the hash.
            # IntegrityError will be raised if hash_transacao (unique=True) already exists.
            with transaction.atomic(): # Ensures save is atomic for IntegrityError handling
                lancamento.save()
            imported_count += 1
        except IntegrityError: # Catching if hash_transacao (unique=True) collision occurs
            skipped_due_to_duplicate += 1
        except Exception as e:
            # Log more detailed error on the server side here if possible
            error_details.append({"transaction_description": tx_data.descricao_original, "error": str(e)})
            skipped_due_to_error += 1

    total_processed = imported_count + skipped_due_to_duplicate + skipped_due_to_error

    if not payload: # Handle empty payload case
        return 400, {"message": "Nenhuma transação fornecida no payload."}

    if skipped_due_to_error > 0:
        # If there were processing errors beyond duplicates
        return 207, {
            "message": "Processamento concluído com erros.",
            "imported_count": imported_count,
            "skipped_duplicates_count": skipped_due_to_duplicate,
            "skipped_errors_count": skipped_due_to_error,
            "total_provided": len(payload),
            "errors": error_details
        }

    if skipped_due_to_duplicate > 0:
        # If only duplicates were skipped, but no other errors
         return 207, {
            "message": f"Importação concluída. {imported_count} transações novas importadas. {skipped_due_to_duplicate} transações duplicadas foram ignoradas.",
            "imported_count": imported_count,
            "skipped_duplicates_count": skipped_due_to_duplicate,
            "total_provided": len(payload)
        }

    if imported_count == 0 and skipped_due_to_duplicate == 0 and skipped_due_to_error == 0 and len(payload) > 0:
        # This case should ideally not be hit if payload is not empty, means something unexpected.
        # Or all items in payload were empty/invalid before even attempting to process.
        # For now, assume this means no *new* transactions were processed.
        return 200, {"message": "Nenhuma nova transação foi importada. Todas as transações fornecidas já existiam ou não puderam ser processadas."}


    return 201, {"message": f"Importação bem-sucedida. {imported_count} transações importadas."}
