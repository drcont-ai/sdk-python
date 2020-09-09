import starkbank
from datetime import datetime
from unittest import TestCase, main
from tests.utils.date import randomPastDate
from tests.utils.transaction import generateExampleTransactions
from tests.utils.user import exampleProject


starkbank.user = exampleProject


class TestTransactionPost(TestCase):

    def test_success(self):
        transactions = starkbank.transaction.create(generateExampleTransactions(n=5))
        self.assertEqual(len(transactions), 5)
        for transaction in transactions:
            print(transaction)


class TestTransactionGet(TestCase):

    def test_success(self):
        transactions = list(starkbank.transaction.query(limit=10))
        self.assertEqual(len(transactions), 10)
        print("Number of transactions:", len(transactions))

    def test_success_after_before(self):
        after = randomPastDate(days=10)
        before = datetime.today()
        transactions = list(starkbank.transaction.query(after=after.date(), before=before.date(), limit=10))
        self.assertLessEqual(len(transactions), 10)
        for transaction in transactions:
            print(transaction)


class TestTransactionInfoGet(TestCase):

    def test_success(self):
        transactions = starkbank.transaction.query()
        transaction_id = next(transactions).id
        transaction = starkbank.transaction.get(id=transaction_id)
        self.assertIsNotNone(transaction.id)
        self.assertEqual(transaction.id, transaction_id)

    def test_success_ids(self):
        transactions = starkbank.transaction.query(limit=5)
        transactions_ids_expected = [t.id for t in transactions]
        transactions_ids_result = [t.id for t in starkbank.transaction.query(ids=transactions_ids_expected)]
        transactions_ids_expected.sort()
        transactions_ids_result.sort()
        self.assertTrue(transactions_ids_result)
        self.assertEqual(transactions_ids_expected, transactions_ids_result)


if __name__ == '__main__':
    main()
