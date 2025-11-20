
from typing import List, Dict
from datetime import datetime, timedelta

class TransferDetector:
    def __init__(self, transactions: List[Dict]):
        self.transactions = transactions

    def detect_transfers(self) -> List[Dict]:
        """
        Detects transfers between accounts.
        """
        potential_transfers = {}
        for t in self.transactions:
            amount = abs(float(t.get('amount', 0)))
            if amount not in potential_transfers:
                potential_transfers[amount] = []
            potential_transfers[amount].append(t)

        transfers = []
        for amount, transactions in potential_transfers.items():
            if len(transactions) > 1:
                for i in range(len(transactions)):
                    for j in range(i + 1, len(transactions)):
                        t1 = transactions[i]
                        t2 = transactions[j]
                        date1 = datetime.fromisoformat(t1.get('transaction_date'))
                        date2 = datetime.fromisoformat(t2.get('transaction_date'))
                        if abs(date1 - date2) <= timedelta(days=3):
                            transfers.append(t1)
                            transfers.append(t2)
        return transfers
