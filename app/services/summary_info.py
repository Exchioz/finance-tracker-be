from sqlalchemy import func, cast, Date, case
from sqlalchemy.orm import Session

from app.database.models import Transaction
from app.schemas.transactions import TransactionSummaryFilter

def build_period_expr(group_by: str):
    group_by = group_by.lower()
    if group_by == "day":
        return cast(Transaction.date, Date).label("period"), []
    elif group_by == "week":
        return func.concat(
            func.to_char(Transaction.date, "IYYY"),
            "-W",
            func.lpad(func.to_char(Transaction.date, "IW"), 2, "0")
        ).label("period"), []
    elif group_by == "month":
        return func.to_char(Transaction.date, "YYYY-MM").label("period"), []
    elif group_by == "year":
        return func.to_char(Transaction.date, "YYYY").label("period"), []
    elif group_by == "category":
        return None, [Transaction.category_id]
    elif group_by == "wallet":
        return None, [Transaction.wallet_id]
    elif group_by == "category_wallet":
        return None, [Transaction.category_id, Transaction.wallet_id]
    else:  # "all"
        return None, []

def query_transaction_summary(
    db: Session,
    user_id: int,
    flt: TransactionSummaryFilter
) -> list[dict]:
    group_by = (flt.group_by or "day").lower()
    period_expr, extra_group_fields = build_period_expr(group_by)

    base_query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if flt.start_date:
        base_query = base_query.filter(Transaction.date >= flt.start_date)
    if flt.end_date:
        base_query = base_query.filter(Transaction.date <= flt.end_date)
    if flt.category_id:
        base_query = base_query.filter(Transaction.category_id == flt.category_id)
    if flt.wallet_id:
        base_query = base_query.filter(Transaction.wallet_id == flt.wallet_id)

    # Jika group_by == "all", kita return satu-satunya aggregate total
    if group_by == "all":
        total = base_query.with_entities(
            func.sum(case((Transaction.type == "INCOME", Transaction.amount), else_=0)).label("total_income"),
            func.sum(case((Transaction.type == "EXPENSE", Transaction.amount), else_=0)).label("total_expense"),
            func.sum(case((Transaction.type == "INCOME", 1), else_=0)).label("income_count"),
            func.sum(case((Transaction.type == "EXPENSE", 1), else_=0)).label("expense_count"),
        ).first()

        ti = float(total.total_income or 0)
        te = float(total.total_expense or 0)
        ic = int(total.income_count or 0)
        ec = int(total.expense_count or 0)
        return [{
            "period": "all",
            "total_income": ti,
            "total_expense": te,
            "balance": ti - te,
            "income_count": ic,
            "expense_count": ec
        }]
    
    # Build select fields
    select_fields = []
    group_fields = []
    if period_expr is not None:
        select_fields.append(period_expr)
        group_fields.append(period_expr)
    for field in extra_group_fields:
        select_fields.append(field)
        group_fields.append(field)
    select_fields += [
        func.sum(case((Transaction.type == "INCOME", Transaction.amount), else_=0)).label("total_income"),
        func.sum(case((Transaction.type == "EXPENSE", Transaction.amount), else_=0)).label("total_expense"),
        func.sum(case((Transaction.type == "INCOME", 1), else_=0)).label("income_count"),
        func.sum(case((Transaction.type == "EXPENSE", 1), else_=0)).label("expense_count"),
    ]

    query_agg = base_query.with_entities(*select_fields).group_by(*group_fields)
    if period_expr is not None:
        query_agg = query_agg.order_by(period_expr)
    elif extra_group_fields:
        query_agg = query_agg.order_by(*extra_group_fields)

    results = query_agg.all()
    summary = []
    for row in results:
        row_dict = {}
        idx = 0
        if period_expr is not None:
            row_dict["period"] = str(row[idx])
            idx += 1
        if group_by == "category":
            row_dict["category_id"] = row[idx]
            idx += 1
        if group_by == "wallet":
            row_dict["wallet_id"] = row[idx]
            idx += 1
        if group_by == "category_wallet":
            row_dict["category_id"] = row[idx]
            idx += 1
            row_dict["wallet_id"] = row[idx]
            idx += 1
        row_dict["total_income"] = float(row[idx] or 0)
        row_dict["total_expense"] = float(row[idx+1] or 0)
        row_dict["balance"] = row_dict["total_income"] - row_dict["total_expense"]
        row_dict["income_count"] = int(row[idx+2] or 0)
        row_dict["expense_count"] = int(row[idx+3] or 0)
        summary.append(row_dict)
    return summary