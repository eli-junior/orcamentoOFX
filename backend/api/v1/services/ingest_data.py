from ninja.files import UploadedFile
from ofxparse import OfxParser
import codecs


def ofx_reader(file: UploadedFile):

    try:
        file.open("rb")
        reader = codecs.getreader("latin-1")
        ofx = OfxParser.parse(reader(file))
    finally:
        file.close()

    transactions = []
    for transaction in ofx.account.statement.transactions:
        transactions.append(
            {
                "type": transaction.type,
                "date": transaction.date,
                "amount": transaction.amount,
                "memo": transaction.memo,
            }
        )

    return transactions
