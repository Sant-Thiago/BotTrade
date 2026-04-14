//+------------------------------------------------------------------+
//| Breakout Pending Orders                                          |
//+------------------------------------------------------------------+
#property strict

input int period = 14;
input int target = 750;
input int stop = 250;
input double volume = 1.0;

double top, bottom;

//+------------------------------------------------------------------+
void OnTick() {

   double ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(_Symbol, SYMBOL_BID);
   
   // calcula topo e fundo (barra anterior)
   top = iHigh(_Symbol, PERIOD_D1, iHighest(_Symbol, PERIOD_D1, MODE_HIGH, period, 1));
   bottom = iLow(_Symbol, PERIOD_D1, iLowest(_Symbol, PERIOD_D1, MODE_LOW, period, 1));
      
   // se já tem posição aberta, não faz nada
   if(PositionSelect(_Symbol)) {
      deletePendingOrders();
      return;
   }

   // se não tem ordens pendentes, cria
   if (!hasBuyStop() && top > ask) {
      placeBuyStop();
   }
   
   if (!hasSellStop() && bottom < bid) {
      placeSellStop();
   }  

   // verifica OCO (se uma ativou, cancela a outra)
   checkOCO();
}


void placeBuyStop() {

   MqlTradeRequest req;
   MqlTradeResult res;

   // BUY STOP
   ZeroMemory(req);
   req.action = TRADE_ACTION_PENDING;
   req.type = ORDER_TYPE_BUY_STOP;
   req.symbol = _Symbol;
   req.volume = volume;
   req.price = top;
   req.sl = top - stop * _Point;
   req.tp = top + target * _Point;
   req.deviation = 10;
   
   // obrigatório em muitas corretoras
   req.type_filling = ORDER_FILLING_RETURN;
   req.type_time    = ORDER_TIME_DAY;
         
   if (!OrderSend(req, res))
   {
      Print("Erro ao enviar ordem de compra: ", GetLastError());
   } else 
   {
      Print("Ordem enviada. Retcode: ", res.retcode);
   }
   
}

void placeSellStop() {

   MqlTradeRequest req;
   MqlTradeResult res;

   // SELL STOP
   ZeroMemory(req);
   req.action = TRADE_ACTION_PENDING;
   req.type = ORDER_TYPE_SELL_STOP;
   req.symbol = _Symbol;
   req.volume = volume;
   req.price = bottom;
   req.sl = bottom + stop * _Point;
   req.tp = bottom - target * _Point;
   req.deviation = 10;
   
   // obrigatório em muitas corretoras
   req.type_filling = ORDER_FILLING_RETURN;
   req.type_time    = ORDER_TIME_DAY;
         
   if (!OrderSend(req, res)) {
      Print("Erro ao enviar ordem de venda: ", GetLastError());
   } else {
      Print("Ordem enviada. Retcode: ", res.retcode);
   }
   
}


//+------------------------------------------------------------------+
void deletePendingOrders()
{
   for(int i = OrdersTotal()-1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(OrderSelect(ticket))
      {
         if (OrderGetString(ORDER_SYMBOL) != _Symbol) continue;
         
         if(OrderGetInteger(ORDER_TYPE) == ORDER_TYPE_BUY_STOP ||
            OrderGetInteger(ORDER_TYPE) == ORDER_TYPE_SELL_STOP)
         {
            MqlTradeRequest req;
            MqlTradeResult res;

            ZeroMemory(req);
            req.action = TRADE_ACTION_REMOVE;
            req.order = ticket;

            OrderSend(req, res);
         }
      }
   }
}

//+------------------------------------------------------------------+
void checkOCO()
{
   // se entrou em posição, remove pendentes
   if(PositionSelect(_Symbol))
   {
      deletePendingOrders();
   }
}

bool hasBuyStop() {
   for(int i = 0; i < OrdersTotal(); i++) {
      ulong ticket = OrderGetTicket(i);
      
      if (OrderSelect(ticket)) {
         if (OrderGetString(ORDER_SYMBOL) == _Symbol &&
            OrderGetInteger(ORDER_TYPE) == ORDER_TYPE_BUY_STOP)
            return true;
      }
   }
   return false;
}

bool hasSellStop() {
   for (int i = 0; i < OrdersTotal(); i++) {
      ulong ticket = OrderGetTicket(i);
      
      if (OrderSelect(ticket)) {
         if (OrderGetString(ORDER_SYMBOL) == _Symbol &&
            OrderGetInteger(ORDER_TYPE) == ORDER_TYPE_SELL_STOP)
            return true;
      }
   }
   return false;
}