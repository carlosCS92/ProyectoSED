//  AUTHOR: Miguel Andres Herrero, Carlos Congosto Sandoval

int LDRPin = A0;     //Pin de entrada de señal de la LDR
int LED = 13;        //Pin de señal de salida del LED
int consigna = 600;  //Valor de consigna, a partir del cual se apaga el LED
char new_c;
char c = '1';		//Valor que nos indica si el LED se enciende o se apaga
void setup()        //Configuracin IO de pines
{
  Serial.begin(9600);
  pinMode(LDRPin, INPUT);
  pinMode(LED, OUTPUT);
} 
 
void loop()
{
   
   int valor = analogRead(LDRPin); //almacena el valor que lee la LDR
   Serial.println(valor);
   delay(1000); //Esperamos 1 segundo
   new_c = Serial.read();//Leemos del puerto serie lo que recibimos de la raspy
   if(new_c == '1' || new_c == '0') //Comprobamos si el valor es 0 o 1
      c = new_c; //actualizamos el valor de c
   Serial.println(c);
   if (new_c=='1')
   {
      digitalWrite(LED, LOW);//Apagamos el LED
   }
   else if (new_c=='0')
      digitalWrite(LED, HIGH);//Encendemos el LED
}
