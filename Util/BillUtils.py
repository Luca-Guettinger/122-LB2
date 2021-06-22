from unicodedata import decimal

from model.Bill import Bill
from model.BillPosition import BillPosition


def sum_positions_totals(bill: Bill):
    result = 0
    for pos in bill.positions:
        result += float(pos.total)

    return result


def sum_mwst_totals(bill: Bill):
    result = 0.0
    for pos_a in bill.positions:
        pos: BillPosition
        pos = pos_a
        mwst_value = float(pos.mwst.split("_")[1].replace("%", ""))

        if mwst_value == 0:
            continue

        result += (mwst_value * float(pos.total) / 100)
    return result
