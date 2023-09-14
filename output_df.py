def format_data(signal, hist):
    # Check if input dataframes have the same length
    if len(signal) != len(hist):
        raise ValueError("Input dataframes have different lengths.")

    # Check if input dataframes have a 'Signal' column
    if "Signal" not in signal.columns:
        raise ValueError(
            "Input dataframess must have 'Signal' and 'Date' columns."
        )

    records = []  # {signal, date, close}
    row_index = 0

    for index, row in signal.iterrows():
        signal = row["Signal"]
        # Format timestamps as in YYYY-MM-DD string format.
        date = index.strftime('%Y-%m-%d')
        close = hist.iloc[row_index, hist.columns.get_loc("Close")]

        if signal in [-1, 1]:
            record = [signal, date, close]
            records.append(record)

    row += 1

    return records


def calculate_result(records, capital=20000):
    results = []
    puchase_qty = 0

    for record in records:
        if int(record[0]) == 1:
            # Buy signals
            if (capital >= 10000):
                capital -= 10000
                purchase_qty += 10000 / record[2]
                print(purchase_qty)
            else:
                print(
                    f'Not enough capital to purchase at closing price {record[2]} on {record[1]}')
        elif int(record[0] == -1):
            # Sell signals
            if (purchase_qty > 0):
                capital += record[3] * purchase_qty
                purchase_qty = 0  # reset to 0
            else:
                print(
                    f"No stocks to sell at closing price {record[2]} on {record[1]}")

        result = [record[1], record[2], capital, purchase_qty]
        results.append(result)

    return results
