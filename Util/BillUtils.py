from model.Bill import Bill


def sum_positions_totals(bill: Bill):
    result = 0
    for pos in bill.positions:
        result += float(pos.total)

    result = int(result * 100)
    return result
