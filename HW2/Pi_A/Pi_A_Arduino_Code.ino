// Chaitanya Pawar
// Date: 3/9/2022
// Description: Capture analogy digital values from a potentiometer and a light
// sensor. The captured data is catloged in various ranges, which will be used
// to compare both sensors values.

void setup() {
  Serial.begin(9600);  // initialize serial communication at 9600 bits per
                       // second
}

void loop() {
  // reads the inport analog pin A0 & A1
  int Poten_Value = analogRead(A0);  // read the input on analog pin 0
  int Light_Value = analogRead(A1);
  // reads the input on analog pin A0 (value between 0 and 1023)

  // Map the values to the range of 0 to 255
  Poten_Value = map(Poten_Value, 0, 691, 0, 255);
  Light_Value = map(Light_Value, 0, 1000, 0, 255);

  // Prints Analog values of the sensor to the serial monitor and provides a
  // range to compare both sensor's values to each other.
  Serial.print(Poten_Value);  // Measures and Sends Potentiometer's exact
                              // analog value in current position
  Serial.print(",");
  Serial.println(Light_Value);
  delay(100);
  /**
  delay(100);
  if (Poten_Value < 50) {                                               //Starts
  mapping values for the potentiometer Serial.println("  Potentiometer Analog
  Value Rage: 0-49"); delay(100); } else if (Poten_Value > 50) {
    Serial.println("  Potentiometer Analog Value Rage: 51-100");
    delay(100);
  }
  Serial.print(Light_Value); //Measures and Sends Light sensor's exact analog
  value in current lighting environment delay(100); if (Light_Value < 200) {
  //Starts mapping values for the light sensor Serial.println("  Light Sensor
  Analog Value Range : 0-200"); delay(100); } else if (Light_Value > 200) {
    Serial.println("  Light Sensor Analog Value Range : 200-600");
    delay(100);
  }
  **/
}
