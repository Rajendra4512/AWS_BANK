"""Synthetic banking operations with integer minor-unit ledger entries.

This module is intentionally local and educational. It never connects to a
real bank or authorizes irreversible financial activity.
"""
import hashlib
import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/banking", tags=["banking"])


def stamp():
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def connection():
    data = Path(os.getenv("AWS_BANK_DATA_DIR", "data"))
    data.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(data / "bank.sqlite3", timeout=15)
    c.row_factory = sqlite3.Row
    try:
        yield c
        c.commit()
    except Exception:
        c.rollback()
        raise
    finally:
        c.close()


def setup():
    with connection() as c:
        c.executescript(
            """
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_ref TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                owner_username TEXT UNIQUE,
                status TEXT NOT NULL DEFAULT 'active',
                created TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS accounts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL REFERENCES customers(id),
                account_number TEXT NOT NULL UNIQUE,
                kind TEXT NOT NULL CHECK(kind IN ('savings','current')),
                currency TEXT NOT NULL DEFAULT 'INR',
                balance_minor INTEGER NOT NULL DEFAULT 0 CHECK(balance_minor >= 0),
                status TEXT NOT NULL DEFAULT 'active',
                created TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS ledger_entries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_ref TEXT NOT NULL,
                account_id INTEGER NOT NULL REFERENCES accounts(id),
                direction TEXT NOT NULL CHECK(direction IN ('credit','debit')),
                amount_minor INTEGER NOT NULL CHECK(amount_minor > 0),
                balance_after_minor INTEGER NOT NULL CHECK(balance_after_minor >= 0),
                description TEXT NOT NULL,
                counterparty_account_id INTEGER,
                actor TEXT NOT NULL,
                created TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_ledger_account_created ON ledger_entries(account_id, created DESC);
            CREATE TABLE IF NOT EXISTS beneficiaries(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_username TEXT NOT NULL,
                nickname TEXT NOT NULL,
                destination_account_id INTEGER NOT NULL REFERENCES accounts(id),
                active INTEGER NOT NULL DEFAULT 1,
                created TEXT NOT NULL,
                UNIQUE(owner_username, destination_account_id)
            );
            CREATE TABLE IF NOT EXISTS service_requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                requester_username TEXT NOT NULL,
                kind TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS banking_idempotency(
                idempotency_key TEXT PRIMARY KEY,
                actor TEXT NOT NULL,
                response_json TEXT NOT NULL,
                created TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS banking_notifications(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                read INTEGER NOT NULL DEFAULT 0,
                created TEXT NOT NULL
            );
            """
        )
        if not c.execute("SELECT 1 FROM customers LIMIT 1").fetchone():
            _seed_customer(c, "SYN-CUST-001", "Asha Rao", "customer.asha", "SYN-100001", "savings", 125000)
            _seed_customer(c, "SYN-CUST-002", "Kabir Mehta", "customer.kabir", "SYN-100002", "current", 248000)
            _seed_customer(c, "SYN-CUST-003", "Mira Shah", "customer.mira", "SYN-100003", "savings", 91500)


def _seed_customer(c, ref, name, owner, account_number, kind, opening_minor):
    ts = stamp()
    c.execute(
        "INSERT INTO customers(customer_ref,display_name,owner_username,status,created) VALUES(?,?,?,?,?)",
        (ref, name, owner, "active", ts),
    )
    customer_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.execute(
        "INSERT INTO accounts(customer_id,account_number,kind,currency,balance_minor,status,created) VALUES(?,?,?,?,?,?,?)",
        (customer_id, account_number, kind, "INR", opening_minor, "active", ts),
    )
    account_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
    c.execute(
        "INSERT INTO ledger_entries(transaction_ref,account_id,direction,amount_minor,balance_after_minor,description,actor,created) VALUES(?,?,?,?,?,?,?,?)",
        (f"SEED-{ref}", account_id, "credit", opening_minor, opening_minor, "Synthetic opening balance", "system", ts),
    )


class Transfer(BaseModel):
    from_account_id: int = Field(gt=0)
    to_account_id: int = Field(gt=0)
    amount_minor: int = Field(gt=0, le=10_000_000)
    idempotency_key: str = Field(min_length=12, max_length=80, pattern=r"^[A-Za-z0-9_.:-]+$")
    description: str = Field(default="Internal transfer", min_length=3, max_length=160)


class Beneficiary(BaseModel):
    nickname: str = Field(min_length=2, max_length=80)
    destination_account_id: int = Field(gt=0)


class ServiceRequest(BaseModel):
    kind: str = Field(min_length=3, max_length=60)
    description: str = Field(min_length=8, max_length=1000)


class CashOperation(BaseModel):
    account_id: int = Field(gt=0)
    amount_minor: int = Field(gt=0, le=10_000_000)
    idempotency_key: str = Field(min_length=12, max_length=80, pattern=r"^[A-Za-z0-9_.:-]+$")
    description: str = Field(default="Simulated cash operation", min_length=3, max_length=160)


class ProfileUpdate(BaseModel):
    display_name: str = Field(min_length=2, max_length=120)


class ServiceRequestStatus(BaseModel):
    status: str = Field(pattern=r"^(open|in_progress|resolved|rejected)$")


def principal(request: Request):
    token = request.cookies.get("aws_bank_session", "")
    with connection() as c:
        row = c.execute(
            "SELECT u.username,u.role FROM sessions s JOIN users u ON s.username=u.username WHERE s.token_hash=? AND s.expires>? AND u.active=1",
            (hashlib.sha256(token.encode()).hexdigest(), int(time.time())),
        ).fetchone()
    if row is None:
        raise HTTPException(401, "Sign in required")
    return dict(row)


def _admin(u):
    return u["role"] in ("admin", "bank_admin", "super_admin")


def _staff(u):
    return _admin(u) or u["role"] in ("bank_officer", "risk_analyst", "governance_officer")


def _audit(c, actor, action, detail):
    try:
        c.execute("INSERT INTO audit(ts,actor,action,detail) VALUES(?,?,?,?)", (stamp(), actor, action, json.dumps(detail)))
    except sqlite3.OperationalError as exc:
        if "no such table: audit" not in str(exc):
            raise


def _owns_account(c, account_id, u):
    row = c.execute(
        "SELECT a.*,c.owner_username,c.display_name FROM accounts a JOIN customers c ON c.id=a.customer_id WHERE a.id=? AND a.status='active'",
        (account_id,),
    ).fetchone()
    if row is None:
        raise HTTPException(404, "Account not found")
    if not _admin(u) and row["owner_username"] != u["username"]:
        raise HTTPException(403, "Account access denied")
    return row


@router.get("/summary")
def summary(u=Depends(principal)):
    with connection() as c:
        params = () if _admin(u) else (u["username"],)
        where = "" if _admin(u) else " WHERE c.owner_username=?"
        accounts = [dict(r) for r in c.execute("SELECT a.id,a.account_number,a.kind,a.currency,a.balance_minor,a.status,c.display_name,c.owner_username FROM accounts a JOIN customers c ON c.id=a.customer_id" + where + " ORDER BY a.id", params)]
        return {"currency": "INR", "accounts": accounts, "total_balance_minor": sum(a["balance_minor"] for a in accounts), "simulated": True}


@router.get("/accounts")
def accounts(u=Depends(principal)):
    return summary(u)


@router.get("/accounts/{account_id}/transactions")
def transactions(account_id: int, u=Depends(principal)):
    with connection() as c:
        _owns_account(c, account_id, u)
        return [dict(r) for r in c.execute("SELECT id,transaction_ref,direction,amount_minor,balance_after_minor,description,counterparty_account_id,created FROM ledger_entries WHERE account_id=? ORDER BY id DESC LIMIT 100", (account_id,))]


@router.get("/accounts/{account_id}/statement")
def statement(account_id: int, u=Depends(principal)):
    with connection() as c:
        account = _owns_account(c, account_id, u)
        entries = [dict(r) for r in c.execute("SELECT id,transaction_ref,direction,amount_minor,balance_after_minor,description,counterparty_account_id,created FROM ledger_entries WHERE account_id=? ORDER BY id ASC", (account_id,))]
        return {"account": dict(account), "entries": entries, "currency": account["currency"], "simulated": True}


@router.get("/profile")
def profile(u=Depends(principal)):
    with connection() as c:
        row = c.execute("SELECT customer_ref,display_name,owner_username,status,created FROM customers WHERE owner_username=?", (u["username"],)).fetchone()
        return {"identity": u, "customer": dict(row) if row else None, "simulated": True}


@router.put("/profile")
def update_profile(x: ProfileUpdate, u=Depends(principal)):
    with connection() as c:
        result = c.execute("UPDATE customers SET display_name=? WHERE owner_username=?", (x.display_name, u["username"]))
        if not result.rowcount:
            raise HTTPException(404, "Customer profile not found")
        _audit(c, u["username"], "banking.profile.update", {"display_name": x.display_name})
        return {"ok": True, "display_name": x.display_name}


def _cash_operation(x: CashOperation, u, direction):
    with connection() as c:
        try:
            c.execute("BEGIN IMMEDIATE")
            prior = c.execute("SELECT response_json FROM banking_idempotency WHERE idempotency_key=? AND actor=?", (x.idempotency_key, u["username"])).fetchone()
            if prior:
                return json.loads(prior["response_json"])
            account = _owns_account(c, x.account_id, u)
            if direction == "debit" and account["balance_minor"] < x.amount_minor:
                raise HTTPException(409, "Insufficient funds")
            after = account["balance_minor"] + x.amount_minor if direction == "credit" else account["balance_minor"] - x.amount_minor
            ref = ("DP-" if direction == "credit" else "WD-") + uuid.uuid4().hex[:16].upper()
            ts = stamp()
            c.execute("UPDATE accounts SET balance_minor=? WHERE id=?", (after, x.account_id))
            c.execute("INSERT INTO ledger_entries(transaction_ref,account_id,direction,amount_minor,balance_after_minor,description,actor,created) VALUES(?,?,?,?,?,?,?,?)", (ref, x.account_id, direction, x.amount_minor, after, x.description, u["username"], ts))
            result = {"transaction_ref": ref, "status": "posted", "account_id": x.account_id, "amount_minor": x.amount_minor, "direction": direction, "currency": account["currency"], "simulated": True}
            c.execute("INSERT INTO banking_idempotency(idempotency_key,actor,response_json,created) VALUES(?,?,?,?)", (x.idempotency_key, u["username"], json.dumps(result), ts))
            c.execute("INSERT INTO banking_notifications(username,message,created) VALUES(?,?,?)", (account["owner_username"], f"{direction.title()} {ref} posted", ts))
            _audit(c, u["username"], "banking.cash_operation", {"transaction_ref": ref, "account_id": x.account_id, "direction": direction, "amount_minor": x.amount_minor})
            return result
        except HTTPException:
            c.rollback()
            raise
        except sqlite3.IntegrityError:
            c.rollback()
            raise HTTPException(409, "Cash operation could not be posted")


@router.post("/deposits")
def deposit(x: CashOperation, u=Depends(principal)):
    return _cash_operation(x, u, "credit")


@router.post("/withdrawals")
def withdrawal(x: CashOperation, u=Depends(principal)):
    return _cash_operation(x, u, "debit")


@router.post("/transfers")
def transfer(x: Transfer, u=Depends(principal)):
    if x.from_account_id == x.to_account_id:
        raise HTTPException(422, "Source and destination must differ")
    with connection() as c:
        try:
            c.execute("BEGIN IMMEDIATE")
            prior = c.execute("SELECT response_json FROM banking_idempotency WHERE idempotency_key=? AND actor=?", (x.idempotency_key, u["username"])).fetchone()
            if prior:
                return json.loads(prior["response_json"])
            source = _owns_account(c, x.from_account_id, u)
            destination = c.execute("SELECT * FROM accounts WHERE id=? AND status='active'", (x.to_account_id,)).fetchone()
            if destination is None:
                raise HTTPException(404, "Destination account not found")
            if source["currency"] != destination["currency"]:
                raise HTTPException(422, "Currency mismatch")
            if source["balance_minor"] < x.amount_minor:
                raise HTTPException(409, "Insufficient funds")
            ref = "TX-" + uuid.uuid4().hex[:16].upper()
            ts = stamp()
            source_after = source["balance_minor"] - x.amount_minor
            destination_after = destination["balance_minor"] + x.amount_minor
            c.execute("UPDATE accounts SET balance_minor=? WHERE id=?", (source_after, source["id"]))
            c.execute("UPDATE accounts SET balance_minor=? WHERE id=?", (destination_after, destination["id"]))
            c.execute("INSERT INTO ledger_entries(transaction_ref,account_id,direction,amount_minor,balance_after_minor,description,counterparty_account_id,actor,created) VALUES(?,?,?,?,?,?,?,?,?)", (ref, source["id"], "debit", x.amount_minor, source_after, x.description, destination["id"], u["username"], ts))
            c.execute("INSERT INTO ledger_entries(transaction_ref,account_id,direction,amount_minor,balance_after_minor,description,counterparty_account_id,actor,created) VALUES(?,?,?,?,?,?,?,?,?)", (ref, destination["id"], "credit", x.amount_minor, destination_after, x.description, source["id"], u["username"], ts))
            result = {"transaction_ref": ref, "status": "posted", "from_account_id": source["id"], "to_account_id": destination["id"], "amount_minor": x.amount_minor, "currency": source["currency"], "simulated": True}
            c.execute("INSERT INTO banking_idempotency(idempotency_key,actor,response_json,created) VALUES(?,?,?,?)", (x.idempotency_key, u["username"], json.dumps(result), ts))
            c.execute("INSERT INTO banking_notifications(username,message,created) VALUES(?,?,?)", (source["owner_username"], f"Transfer {ref} posted", ts))
            return result
        except HTTPException:
            c.rollback()
            raise
        except sqlite3.IntegrityError:
            c.rollback()
            raise HTTPException(409, "Transfer could not be posted")


@router.get("/beneficiaries")
def beneficiaries(u=Depends(principal)):
    with connection() as c:
        where = "" if _admin(u) else " WHERE b.owner_username=?"
        params = () if _admin(u) else (u["username"],)
        return [dict(r) for r in c.execute("SELECT b.id,b.owner_username,b.nickname,b.destination_account_id,b.active,b.created,a.account_number,c.display_name FROM beneficiaries b JOIN accounts a ON a.id=b.destination_account_id JOIN customers c ON c.id=a.customer_id" + where + " ORDER BY b.id DESC", params)]


@router.post("/beneficiaries")
def add_beneficiary(x: Beneficiary, u=Depends(principal)):
    with connection() as c:
        destination = c.execute("SELECT id FROM accounts WHERE id=? AND status='active'", (x.destination_account_id,)).fetchone()
        if destination is None:
            raise HTTPException(404, "Destination account not found")
        try:
            c.execute("INSERT INTO beneficiaries(owner_username,nickname,destination_account_id,created) VALUES(?,?,?,?)", (u["username"], x.nickname, x.destination_account_id, stamp()))
        except sqlite3.IntegrityError:
            raise HTTPException(409, "Beneficiary already exists")
        return {"ok": True, "id": c.execute("SELECT last_insert_rowid()").fetchone()[0]}


@router.get("/service-requests")
def service_requests(u=Depends(principal)):
    with connection() as c:
        where = "" if _admin(u) else " WHERE requester_username=?"
        params = () if _admin(u) else (u["username"],)
        return [dict(r) for r in c.execute("SELECT * FROM service_requests" + where + " ORDER BY id DESC LIMIT 100", params)]


@router.post("/service-requests")
def create_service_request(x: ServiceRequest, u=Depends(principal)):
    ts = stamp()
    with connection() as c:
        c.execute("INSERT INTO service_requests(requester_username,kind,description,created,updated) VALUES(?,?,?,?,?)", (u["username"], x.kind, x.description, ts, ts))
        request_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
        return {"id": request_id, "status": "open"}


@router.put("/service-requests/{request_id}/status")
def update_service_request(request_id: int, x: ServiceRequestStatus, u=Depends(principal)):
    if not _staff(u):
        raise HTTPException(403, "Staff access required")
    with connection() as c:
        row = c.execute("SELECT * FROM service_requests WHERE id=?", (request_id,)).fetchone()
        if row is None:
            raise HTTPException(404, "Service request not found")
        c.execute("UPDATE service_requests SET status=?,updated=? WHERE id=?", (x.status, stamp(), request_id))
        c.execute("INSERT INTO banking_notifications(username,message,created) VALUES(?,?,?)", (row["requester_username"], f"Service request #{request_id} is {x.status}", stamp()))
        _audit(c, u["username"], "banking.service_request.status", {"request_id": request_id, "status": x.status})
        return {"id": request_id, "status": x.status}


@router.get("/staff/customers")
def staff_customers(u=Depends(principal)):
    if not _staff(u):
        raise HTTPException(403, "Staff access required")
    with connection() as c:
        return [dict(r) for r in c.execute("SELECT c.id,c.customer_ref,c.display_name,c.owner_username,c.status,a.id AS account_id,a.account_number,a.kind,a.currency,a.balance_minor FROM customers c LEFT JOIN accounts a ON a.customer_id=c.id ORDER BY c.id")]


@router.get("/staff/reconciliation")
def staff_reconciliation(u=Depends(principal)):
    if not _staff(u):
        raise HTTPException(403, "Staff access required")
    with connection() as c:
        rows=[]
        for account in c.execute("SELECT id,account_number,balance_minor,currency FROM accounts ORDER BY id"):
            ledger_net=c.execute("SELECT COALESCE(SUM(CASE WHEN direction='credit' THEN amount_minor ELSE -amount_minor END),0) AS net FROM ledger_entries WHERE account_id=?", (account["id"],)).fetchone()["net"]
            rows.append({"account_id":account["id"],"account_number":account["account_number"],"currency":account["currency"],"balance_minor":account["balance_minor"],"ledger_net_minor":ledger_net,"matched":account["balance_minor"]==ledger_net})
        return {"accounts":rows,"all_matched":all(row["matched"] for row in rows),"simulated":True}


@router.get("/notifications")
def notifications(u=Depends(principal)):
    with connection() as c:
        where = "" if _admin(u) else " WHERE username=?"
        params = () if _admin(u) else (u["username"],)
        return [dict(r) for r in c.execute("SELECT id,username,message,read,created FROM banking_notifications" + where + " ORDER BY id DESC LIMIT 50", params)]
