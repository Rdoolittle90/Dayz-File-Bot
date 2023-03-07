def divider_title(title="", width=50, symbol="-"):
    """
    Centers a given title within a divider made of a given symbol.
    :param title: (str) The title to center within the divider (default: "")
    :param width: (int) The width of the divider (default: 50)
    :param symbol: (str) The symbol to use for the divider (default: "-")
    :return: (str) The divider with the centered title
    """
    if len(title) > width:
        print(title[:width])

    left_pad = (width - len(title)) // 2
    right_pad = width - len(title) - left_pad

    print(symbol * left_pad + title + symbol * right_pad)