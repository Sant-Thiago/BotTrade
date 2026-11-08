
import MetaTrader5 as mt5


def connect():
    print("MT5 | INICIANDO CONEXÃO")

    if not mt5.initialize():
        error = mt5.last_error()
        raise RuntimeError(f"Falha ao conectar ao MT5: {error}")

    terminal = mt5.terminal_info()

    if terminal is None:
        raise RuntimeError(
            f"Não foi possível obter informações do terminal: {mt5.last_error()}"
        )

    print("MT5 | CONECTADO")
    print(f"Terminal conectado: {terminal.connected}")
    print(f"Negociação permitida no terminal: {terminal.trade_allowed}")

    return terminal


def find_win_symbols():
    symbols = mt5.symbols_get()

    if symbols is None:
        raise RuntimeError(
            f"Falha ao consultar ativos: {mt5.last_error()}"
        )

    win_symbols = [
        symbol for symbol in symbols
        if "WIN" in symbol.name.upper()
    ]

    print("\nATIVOS ENCONTRADOS:")

    for symbol in win_symbols:
        mt5.symbol_select(symbol.name, True)

        tick = mt5.symbol_info_tick(symbol.name)

        print(f"\nAtivo: {symbol.name}")
        print(f"Descrição: {symbol.description}")

        if tick:
            print(f"Bid: {tick.bid}")
            print(f"Ask: {tick.ask}")
            print(f"Último preço: {tick.last}")

    return win_symbols


def main():
    try:
        connect()
        symbols = find_win_symbols()

        if not symbols:
            print("\nNenhum ativo com WIN encontrado.")

    except Exception as error:
        print(f"\nERRO: {error}")

    finally:
        mt5.shutdown()
        print("\nMT5 | CONEXÃO ENCERRADA")


if __name__ == "__main__":
    main()
