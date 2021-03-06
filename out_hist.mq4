//+------------------------------------------------------------------+
//|                                                     out_hist.mq4 |
//|                      Copyright © 2007, MetaQuotes Software Corp. |
//|                                        http://www.metaquotes.net |
//+------------------------------------------------------------------+
#property copyright "Copyright © 2007, MetaQuotes Software Corp."
#property link      "http://www.metaquotes.net"

#property indicator_chart_window
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int init()
  {
  out_hist("EURUSD",5);  // This will produce daily history for GBPUSD
// Copy the above line of code for each currency pair and timeframe, and then press F5 to recompile (or restart MT4)
// First parameter must be a valid currency pair, e.g. GBPUSD
// Second parameter must be valid timeframe, i.e. one of 1, 5, 15, 30, 60 (=H1), 240 (=H4), 1440 (daily), 10080 (weekly), 43200 (monthly) 
// To use the currently displayed chart: out_hist(Symbol(),Period());

  return(0);
  }
//  
int out_hist(string ccy, int tf)
{
  string fname = ccy + "," + tf + ".csv";                         // Same folder for each TF (...\experts\files)
//string fname = "TF-" + tf + "\\" + ccy + "," + tf + ".csv";     // Different subfolder for each timeframe
  int handle = FileOpen(fname, FILE_CSV|FILE_WRITE, ",");         // "," means that output data will be separated by commas; change if necessary
  if(handle>0)
    {
     FileWrite(handle,"Date,Time,Open,Low,High,Close,Volume,RSI,AC,AD,ADX,Alligator,AO,ATR,BearsPower,Bands,BullsPower,CCI,DeMarker,Envelopes,Force,Fractals,Gator,Ichimoku,BWMFI,Momentum,MFI,MA,OsMA,MACD,OBV,SAR,RVI,StdDev,Stochastic,WPR,Vortex_minus,Vortex_positive,heis_sell,heis_buy,s");    // This writes the Header record to the file (change or remove to suit)
//   for(int i=0; i<iBars(ccy,tf); i++)                           // Use descending date sequence
     for(int i=iBars(ccy,tf)-1; i>=0; i--)                        // Use ascending date sequence
       {
       string date1 = TimeToStr(iTime(ccy,tf,i),TIME_DATE);
       //s1 = (iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1));
       int s2=0;
       if ((iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1))>0) s2 = 1;
       if ((iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1))<0) s2 = 2;
       //if ((iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1))=0) s2 = 0;
       string s1 = s2;
       //return(s1);
      // #define NEUTRAL 0
       //#define UP 1
       //#define DOWN 2

       //int direction=NEUTRAL;
       //if((iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1))>0) direction=UP;
       //if((iClose(ccy,tf,i+1)-iOpen(ccy,tf,i+1))<0) direction=DOWN;
       //return(direction);

       
       date1 = StringSubstr(date1,5,2) + "-" + StringSubstr(date1,8,2) + "-" + StringSubstr(date1,0,4);
// NOTE: StringSubstr(date1,5,2) is the MONTH
//       StringSubstr(date1,8,2) is the DAY
//       StringSubstr(date1,0,4) is the YEAR (4 digits)
//       "-" means the separator will be a hyphen
//       So if, for example, you want to change the output date format to DD/MM/YYYY, change the above line of code to:
//     date1 = StringSubstr(date1,8,2) + "/" + StringSubstr(date1,5,2) + "/" + StringSubstr(date1,0,4);

       string time1 = TimeToStr(iTime(ccy,tf,i),TIME_MINUTES);
       FileWrite(handle, date1, time1, iOpen(ccy,tf,i), iLow(ccy,tf,i), iHigh(ccy,tf,i), iClose(ccy,tf,i), iVolume(ccy,tf,i),iRSI(ccy,tf,14,PRICE_CLOSE,i), iAC(ccy,tf,i), iAD(ccy,tf,i),iADX(ccy,tf,14,PRICE_CLOSE,MODE_MAIN,i),iAlligator(ccy,tf,13,8,8,5,5,3,MODE_SMMA,PRICE_MEDIAN,MODE_GATORJAW,i), iAO(ccy,tf,i), iATR(ccy,tf,14,i), iBearsPower(ccy,tf,13,PRICE_CLOSE,i), iBands(ccy,tf,34,2,0,PRICE_CLOSE,MODE_LOWER,i), iBullsPower(ccy,tf,13,PRICE_CLOSE,i),iCCI(ccy,tf,14,PRICE_TYPICAL,i),iDeMarker(ccy,tf,14,i), iEnvelopes(ccy,tf,14,MODE_SMA,10,PRICE_CLOSE,0.10,MODE_UPPER,i),iForce(ccy,tf,13,MODE_SMA,PRICE_CLOSE,i),iFractals(ccy,tf,MODE_UPPER,i),iGator(ccy,tf,13,8,8,5,5,3,MODE_SMMA,PRICE_MEDIAN,MODE_UPPER,i),iIchimoku(ccy,tf,9,26,52,MODE_TENKANSEN,i),iBWMFI(ccy,tf,i),iMomentum(ccy,tf,14,PRICE_CLOSE,i), iMFI(ccy,tf,14,i), iMA(ccy,tf,13,8,MODE_SMMA,PRICE_MEDIAN,i), iOsMA(ccy,tf,12,26,9,PRICE_CLOSE,i), iMACD(ccy,tf,12,26,9,PRICE_CLOSE,MODE_MAIN,i),iOBV(ccy,tf,PRICE_CLOSE,i), iSAR(ccy,tf,0.02,0.2,i), iRVI(ccy,tf,10,MODE_MAIN,i), iStdDev(ccy,tf,10,0,MODE_EMA,PRICE_CLOSE,i), iStochastic(ccy,tf,5,3,3,MODE_SMA,0,MODE_MAIN,i), iWPR(ccy,tf,14,i), iCustom(ccy,tf,"Vortex_Indicator",14,1,i),iCustom(ccy,tf,"Vortex_Indicator",14,0,i),iCustom(ccy,tf,"Heisenberg_fixed",150,1000,0,i),iCustom(ccy,tf,"Heisenberg_fixed",150,1000,1,i), s1);
// The above line writes the data to the file in the order: date, time, open, low, high, close, volume. Change the order to suit, if necessary      
       }
     FileClose(handle);
     Comment("History output complete");     // Display a comment in the upper left corner of the chart to advise that process is complete
    }
//----
   return(0);
  }
//+------------------------------------------------------------------+
//| Custom indicator deinitialization function                       |
//+------------------------------------------------------------------+
int deinit()
  {
//----
   
//----
   return(0);
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int start()
  {
//----
   
//----
   return(0);
  }
//+------------------------------------------------------------------+