import re
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class BaseParser:
    def parse(self, text: str) -> List[Dict]:
        raise NotImplementedError

class ActivoBankParser(BaseParser):
    """
    Parser for ActivoBank Portugal statements.
    Typically expects lines with Date (DD-MM-YYYY) and Amount.
    """
    def parse(self, text: str) -> List[Dict]:
        transactions = []
        lines = text.split('\n')
        
        # Regex for DD-MM-YYYY
        date_pattern = r"(\d{2}-\d{2}-\d{4})"
        
        for line in lines:
            # Skip header/footer noise
            if "Saldo" in line or "Movimento" in line:
                continue

            date_match = re.search(date_pattern, line)
            if date_match:
                date_str = date_match.group(1)
                try:
                    date_obj = datetime.strptime(date_str, "%d-%m-%Y")
                except ValueError:
                    continue

                parts = line.split()
                if len(parts) < 3:
                    continue
                
                try:
                    # ActivoBank specific: Amount often at end
                    amount_str = parts[-1].replace('.', '').replace(',', '.')
                    amount = float(amount_str)
                    description = " ".join(parts[1:-1])
                    
                    transactions.append({
                        "date": date_obj,
                        "description": description.strip(),
                        "amount": amount,
                        "type": "credit" if amount > 0 else "debit"
                    })
                except ValueError:
                    continue
                    
        return transactions

class RevolutParser(BaseParser):
    def parse(self, text: str) -> List[Dict]:
        transactions = []
        lines = text.split('\n')
        
        for line in lines:
            # Regex for "DD Mmm YYYY" or "DD Mmm"
            match = re.search(r"(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{4})?", line, re.IGNORECASE)
            
            if match:
                day, month, year = match.groups()
                if not year:
                    year = str(datetime.now().year) 
                
                date_str = f"{day} {month} {year}"
                try:
                    date_obj = datetime.strptime(date_str, "%d %b %Y")
                except ValueError:
                    continue

                words = line.split()
                amount = None
                
                for i in range(len(words) - 1, -1, -1):
                    word = words[i].replace(',', '').replace('$', '').replace('€', '')
                    try:
                        val = float(word)
                        if '.' in words[i] or abs(val) > 0: 
                            amount = val
                            break
                    except ValueError:
                        continue
                
                if amount is not None:
                    description = line[match.end():].split(str(amount))[0] 
                    transactions.append({
                        "date": date_obj,
                        "description": description.strip(),
                        "amount": amount,
                        "type": "credit" if amount > 0 else "debit"
                    })
                    
        return transactions

class TradeRepublicParser(BaseParser):
    def parse(self, text: str) -> List[Dict]:
        transactions = []
        lines = text.split('\n')
        date_pattern = r"(\d{4}-\d{2}-\d{2})"
        
        for line in lines:
            match = re.search(date_pattern, line)
            if match:
                date_str = match.group(1)
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    continue
                
                parts = line.split()
                try:
                    amount_str = parts[-1].replace('.', '').replace(',', '.')
                    amount = float(amount_str)
                    description = " ".join(parts[1:-1])
                    
                    transactions.append({
                        "date": date_obj,
                        "description": description.strip(),
                        "amount": amount,
                        "type": "credit" if amount > 0 else "debit"
                    })
                except ValueError:
                    continue

        return transactions

class ParserFactory:
    @staticmethod
    def get_parser(text: str) -> BaseParser:
        if "ActivoBank" in text or "Millennium" in text:
            return ActivoBankParser()
        elif "Revolut" in text:
            return RevolutParser()
        elif "Trade Republic" in text or "TRADE REPUBLIC" in text:
            return TradeRepublicParser()
        else:
            logger.warning("Could not detect bank format. Using generic parsing.")
            return RevolutParser()