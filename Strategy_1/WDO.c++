#property  strict

input int period = 10;
input int target = 50;
input int stop = 10;
input double volume = 1.0;

double top, bottom;

void OnTick() {


   //top = iHigh(_Symbol, PERIOD_W1, iHighest(_Symbol, PERIOD_W1, MODE_HIGH, period, 1));
   //bottom = iLow(_Symbol, PERIOD_W1, iLowest(_Symbol, PERIOD_W1, MODE_LOW, period, 1));
   
   top = iHigh(_Symbol, _Period, iHighest(_Symbol, _Period, MODE_HIGH, period, 1));
   bottom = iLow(_Symbol, _Period, iLowest(_Symbol, _Period, MODE_LOW, period, 1));
   
   // se já tem posição aberta, não faz nada
   if (PositionSelect(_Symbol)) {
      deletePendingOrders();
      return;
   }
   
   // se não tem ordens pendentes, cria
   if (!hasOrders()) {
      placeOrders();
   }
   
   // verifica OCO (se uma ativou, cancela a outra)
   checkOCO();
}

void placeOrders() {
   MqlTradeRequest req;
   MqlTradeResult res;
   
   // BUY STOP
   ZeroMemory(req);
   req.action = TRADE_ACTION_PENDING;
   req.type = ORDER_TYPE_BUY_STOP;
   req.symbol = _Symbol;
   req.volume = volume;
   req.price = top;
   req.sl = top - stop * 500 * _Point;
   req.tp = top + target * 500 * _Point;
   req.type_filling = ORDER_FILLING_RETURN;
   req.type_time = ORDER_TIME_DAY;
   
   if (!OrderSend(req, res)) {
      Print("Erro ao enviar ordem de compra: ", GetLastError());
   } else {
      Print("Ordem de compra enviada. Retcode: ", res.retcode);
   }
   
   // SELL STOP
   ZeroMemory(req);
   req.action = TRADE_ACTION_PENDING;
   req.type = ORDER_TYPE_SELL_STOP;
   req.symbol = _Symbol;
   req.volume = volume;
   req.price = bottom;
   req.sl = bottom + (stop * 500) *_Point;
   req.tp = bottom - (target * 500) *_Point;
   req.type_filling = ORDER_FILLING_RETURN;
   req.type_time = ORDER_TIME_DAY;

   if (!OrderSend(req, res)) {
      Print("Erro ao enviar ordem de venda: ", GetLastError());
   } else {
      Print("Ordem de venda enviada. Retcode: ", res.retcode);
   }
}

void deletePendingOrders() {
   
   for(int i = OrdersTotal()-1; i >= 0; i--) {
      ulong ticket = OrderGetTicket(i);
      
      if(OrderSelect(ticket)) {
      
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
void checkOCO() {
   // se entrou em posição, remove pendentes
   if(PositionSelect(_Symbol)) {
      deletePendingOrders();
   }
}


bool hasOrders() {
   for (int i = 0; i < OrdersTotal(); i++) {
      ulong ticket = OrderGetTicket(i);
      
      if (OrderSelect(ticket)) {
         if (OrderGetString(ORDER_SYMBOL) == _Symbol) {
            return true;
            break;
         }
      }
   }
   return false;
}