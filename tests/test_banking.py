import os
import sqlite3
import tempfile
from concurrent.futures import ThreadPoolExecutor

from app import banking
from app.banking import CashOperation, Transfer


def test_seeded_transfer_is_atomic_and_idempotent(monkeypatch):
    with tempfile.TemporaryDirectory() as root:
        monkeypatch.setenv("AWS_BANK_DATA_DIR", root)
        banking.setup()
        user = {"username": "customer.asha", "role": "customer"}
        transfer = Transfer(
            from_account_id=1,
            to_account_id=2,
            amount_minor=1000,
            idempotency_key="test-transfer-0001",
            description="Synthetic test transfer",
        )

        first = banking.transfer(transfer, user)
        replay = banking.transfer(transfer, user)

        assert first["status"] == "posted"
        assert replay["transaction_ref"] == first["transaction_ref"]
        conn = sqlite3.connect(os.path.join(root, "bank.sqlite3"))
        try:
            balances = conn.execute(
                "SELECT balance_minor FROM accounts ORDER BY id"
            ).fetchall()
            ledger_count = conn.execute(
                "SELECT COUNT(*) FROM ledger_entries"
            ).fetchone()[0]
        finally:
            conn.close()
        assert balances[:2] == [(124000,), (249000,)]
        assert ledger_count == 5


def test_customer_cannot_transfer_from_another_customer(monkeypatch):
    with tempfile.TemporaryDirectory() as root:
        monkeypatch.setenv("AWS_BANK_DATA_DIR", root)
        banking.setup()
        transfer = Transfer(
            from_account_id=1,
            to_account_id=2,
            amount_minor=1000,
            idempotency_key="test-transfer-0002",
        )
        try:
            banking.transfer(transfer, {"username": "customer.kabir", "role": "customer"})
        except Exception as exc:
            assert getattr(exc, "status_code", None) == 403
        else:
            raise AssertionError("cross-customer transfer unexpectedly succeeded")


def test_transfer_rejects_self_transfer_and_insufficient_funds(monkeypatch):
    with tempfile.TemporaryDirectory() as root:
        monkeypatch.setenv("AWS_BANK_DATA_DIR", root)
        banking.setup()
        user = {"username": "customer.asha", "role": "customer"}
        for transfer, expected in [
            (Transfer(from_account_id=1, to_account_id=1, amount_minor=100, idempotency_key="test-self-0001"), 422),
            (Transfer(from_account_id=1, to_account_id=2, amount_minor=9999999, idempotency_key="test-funds-0001"), 409),
        ]:
            try:
                banking.transfer(transfer, user)
            except Exception as exc:
                assert getattr(exc, "status_code", None) == expected
            else:
                raise AssertionError("invalid transfer unexpectedly succeeded")


def test_simulated_cash_operations_are_idempotent_and_atomic(monkeypatch):
    with tempfile.TemporaryDirectory() as root:
        monkeypatch.setenv("AWS_BANK_DATA_DIR", root)
        banking.setup()
        user = {"username": "customer.asha", "role": "customer"}
        deposit = CashOperation(account_id=1, amount_minor=500, idempotency_key="deposit-test-0001", description="Synthetic deposit")
        first = banking.deposit(deposit, user)
        replay = banking.deposit(deposit, user)
        assert first["transaction_ref"] == replay["transaction_ref"]
        assert first["direction"] == "credit"
        withdrawal = CashOperation(account_id=1, amount_minor=250, idempotency_key="withdraw-test-0001", description="Synthetic withdrawal")
        result = banking.withdrawal(withdrawal, user)
        assert result["direction"] == "debit"
        conn = sqlite3.connect(os.path.join(root, "bank.sqlite3"))
        try:
            balance = conn.execute("SELECT balance_minor FROM accounts WHERE id=1").fetchone()[0]
        finally:
            conn.close()
        assert balance == 125250


def test_concurrent_withdrawals_cannot_overdraw_account(monkeypatch):
    with tempfile.TemporaryDirectory() as root:
        monkeypatch.setenv("AWS_BANK_DATA_DIR", root)
        banking.setup()
        user = {"username": "customer.asha", "role": "customer"}
        operations = [
            CashOperation(account_id=1, amount_minor=100000, idempotency_key="concurrent-withdraw-01"),
            CashOperation(account_id=1, amount_minor=100000, idempotency_key="concurrent-withdraw-02"),
        ]

        def run(operation):
            try:
                return ("posted", banking.withdrawal(operation, user))
            except Exception as exc:
                return ("failed", getattr(exc, "status_code", None))

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(run, operations))
        assert [r[0] for r in results].count("posted") == 1
        assert [r[1] for r in results].count(409) == 1
        conn = sqlite3.connect(os.path.join(root, "bank.sqlite3"))
        try:
            balance = conn.execute("SELECT balance_minor FROM accounts WHERE id=1").fetchone()[0]
        finally:
            conn.close()
        assert balance == 25000
