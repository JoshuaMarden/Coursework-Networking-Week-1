def second_symbol(s: str, symbol: str) -> int:

    return s.find(symbol, (s.find(symbol)+1))


if __name__ == "__main__":
    print(second_symbol("Tes", "t"))
