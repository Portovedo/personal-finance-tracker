import logging
from sqlalchemy.orm import Session
from app.models.statement import Statement
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.services.pdf_parser import PDFParser
from app.services.csv_parser import CSVParser
from app.services.bank_parsers import ParserFactory
from app.services.categorizer import MLCategorizer
from app.services.transfer_detector import TransferDetector

logger = logging.getLogger(__name__)

class StatementProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.ml_categorizer = MLCategorizer()
        self.transfer_detector = TransferDetector(db)

    def process(self, statement_id: int):
        statement = self.db.query(Statement).filter(Statement.id == statement_id).first()
        if not statement:
            logger.error(f"Statement {statement_id} not found")
            return

        try:
            if statement.file_type == 'pdf':
                raw_text = PDFParser.extract_text(statement.file_path)
                parser = ParserFactory.get_parser(raw_text)
                parsed_transactions = parser.parse(raw_text)
                
            elif statement.file_type == 'csv':
                parsed_transactions = CSVParser.parse(statement.file_path)
            else:
                raise ValueError("Unsupported file type")

            created_count = 0
            account = self.db.query(Account).filter(Account.id == statement.account_id).first()
            
            for pt in parsed_transactions:
                exists = self.db.query(Transaction).filter(
                    Transaction.account_id == account.id,
                    Transaction.transaction_date == pt['date'],
                    Transaction.amount == pt['amount'],
                    Transaction.description == pt['description']
                ).first()
                
                if exists:
                    continue

                category_id = self.ml_categorizer.categorize(pt['description'], self.db)
                
                if not category_id:
                    uncategorized = self.db.query(Category).filter(Category.name == "Uncategorized").first()
                    category_id = uncategorized.id if uncategorized else None

                transaction = Transaction(
                    account_id=account.id,
                    description=pt['description'],
                    amount=abs(pt['amount']),
                    type='credit' if pt['amount'] > 0 else 'debit',
                    transaction_date=pt['date'],
                    category_id=category_id,
                    status='pending'
                )
                self.db.add(transaction)
                created_count += 1

            statement.status = 'processed'
            self.db.commit()
            
            logger.info(f"Processed {created_count} transactions for statement {statement_id}")

        except Exception as e:
            logger.error(f"Error processing statement: {e}")
            statement.status = 'failed'
            statement.review_notes = str(e)
            self.db.commit()