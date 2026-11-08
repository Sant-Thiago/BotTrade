# WIN BOT — versão 0.1

Projeto inicial de pesquisa e execução simulada para mini-índice (WIN).

## Estado atual
- Estratégia híbrida explicável: estrutura de preço + rompimento + volume relativo.
- Motor de risco com stop, alvo, limite de perda diária e limite de operações.
- Executor `PaperExecutor`: **não envia ordens reais**.
- Leitura de candles OHLCV por CSV.
- Separação entre dados, estratégia, risco e execução.

## Requisitos
Python 3.11+

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux:
source .venv/bin/activate

pip install -r requirements.txt\npip install -e .
```

## Formato do CSV
Arquivo `data/win_1m.csv` com colunas:
`timestamp,open,high,low,close,volume`

O timestamp deve estar em horário de São Paulo, preferencialmente ISO 8601.
Exemplo: `2026-11-09T09:01:00-03:00`

## Executar
```bash
python -m winbot.main --csv data/win_1m.csv
```

## Regras iniciais da estratégia
A estratégia usa:
- EMA curta e longa como filtro de direção;
- rompimento da máxima/mínima de uma janela anterior;
- volume atual comparado à média de volume anterior;
- confirmação de candle direcional.

Os parâmetros são provisórios e **não representam uma estratégia validada**.
Não otimize parâmetros no mesmo período usado para avaliar o resultado.

## Segurança
A versão 0.1 opera apenas em simulação. Não conecte uma conta real.
Antes de qualquer execução real, será necessário:
1. escolher corretora e API compatíveis com WIN;
2. validar especificações do contrato, custos, slippage e horários;
3. implementar reconciliação de ordens/posições e proteção contra duplicidade;
4. testar em replay e conta simulada;
5. definir limites de risco aprovados pelo operador.

## Próximas etapas
1. Definir fonte de dados e corretora.
2. Criar backtest com custos e slippage.
3. Adicionar dados externos (DOL, IBOV, S&P 500).
4. Adicionar modelo estatístico/ML somente após baseline robusta.
5. Implementar adaptador da corretora, mantendo paper trading como padrão.
