/*************************************************************
  Smart Garden – ESP32 + Blynk + LCD (transistor-controlled)
  ------------------------------------------------------------
  • Starts watering when soil ≥ 2550 (dry)
  • Runs pump for 30 s max
  • Stops early if water ≤ 600 (empty tank)
  • LCD turns OFF during watering, restarts after
  • Displays live Soil/Water instantly after watering
  • Passive low-trigger buzzer sounds 20 s on motion
*************************************************************/

#define BLYNK_TEMPLATE_ID   "TMPL6yllapPQ4"
#define BLYNK_TEMPLATE_NAME "Smart Garden"
#define BLYNK_AUTH_TOKEN    "zHSjChF8DbMx6JGIT9rCqACRZWO3BlOS"

#define BLYNK_PRINT Serial

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ---- Wi-Fi ----
char ssid[] = "Wayne";
char pass[] = "Xieleven11";

// ---- LCD ----
LiquidCrystal_I2C lcd(0x27, 16, 2);

// ---- Pins ----
#define RELAY_PIN   26
#define SOIL_PIN    34
#define WATER_PIN   35
#define PIR_PIN     19
#define BUZZER_PIN  18   // low-trigger passive buzzer
#define SOIL_VCC    23
#define LCD_PWR     27   // transistor base pin (LCD GND control)

// ---- Variables ----
bool wateringActive = false;
bool lcdPowered = true;
unsigned long lastRead = 0;
unsigned long wateringStart = 0;
unsigned long lastLCDUpdate = 0;

const int soilThreshold = 2550;  // dry if ≥2550
const int waterLowLimit = 600;   // tank empty if ≤600
const unsigned long wateringDuration = 30000; // 30 s watering

int lastSoil = 0;
int lastWater = 0;

// ---- Blynk Virtual Pins ----
#define VP_SOIL   V4
#define VP_WATER  V5
#define VP_MOTOR  V6
#define VP_ALERT  V7

/********************** LCD Helpers *******************************/
static inline bool lcdReady() {
  Wire.beginTransmission(0x27);
  return (Wire.endTransmission() == 0);
}

static void lcdReinit() {
  for (int i = 0; i < 3; i++) {
    if (lcdReady()) break;
    delay(200);
  }
  lcd.init();
  lcd.backlight();
  delay(200);
}

/********************** Setup *******************************/
void setup() {
  Serial.begin(115200);
  delay(100);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  pinMode(RELAY_PIN, OUTPUT);
  pinMode(PIR_PIN, INPUT);
  pinMode(SOIL_VCC, OUTPUT);
  pinMode(LCD_PWR, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Default states
  digitalWrite(RELAY_PIN, HIGH);  // relay off
  digitalWrite(SOIL_VCC, LOW);
  digitalWrite(LCD_PWR, HIGH);
  digitalWrite(BUZZER_PIN, HIGH); // buzzer off (low trigger)

  lcdPowered = true;
  Wire.begin(21, 22);
  Wire.setClock(100000);

  lcdReinit();
  lcd.clear();
  lcd.print("Smart Garden");
  delay(1500);
  lcd.clear();

  // Initial soil/water reading
  digitalWrite(SOIL_VCC, HIGH);
  delay(200);
  lastSoil  = analogRead(SOIL_PIN);
  lastWater = analogRead(WATER_PIN);
  digitalWrite(SOIL_VCC, LOW);
  Blynk.virtualWrite(VP_SOIL, lastSoil);
  Blynk.virtualWrite(VP_WATER, lastWater);
  showOnLCD(lastSoil, lastWater);

  Serial.println("✅ Smart Garden Ready");
}

/********************** Loop *******************************/
void loop() {
  Blynk.run();

  // ---- Motion detection (20 s buzzer) ----
  if (digitalRead(PIR_PIN)) {
    Blynk.virtualWrite(VP_ALERT, "Motion Detected!");
    toneBuzzer(20000); // 20 s alarm
  }

  // ---- Stop watering after 30 s or if no water ----
  if (wateringActive) {
    if (millis() - wateringStart >= wateringDuration || lastWater <= waterLowLimit) {
      stopPump();
    }
  }

  // ---- Sensor read every 10 s ----
  if (millis() - lastRead >= 10000UL) {
    readSensors();
    lastRead = millis();
  }

  // ---- LCD refresh every 10 s (when idle) ----
  if (!wateringActive && millis() - lastLCDUpdate >= 10000UL) {
    showOnLCD(lastSoil, lastWater);
    lastLCDUpdate = millis();
  }
}

/********************** Read Sensors *******************************/
void readSensors() {
  digitalWrite(SOIL_VCC, HIGH);
  delay(200);
  int soil = analogRead(SOIL_PIN);
  int water = analogRead(WATER_PIN);
  digitalWrite(SOIL_VCC, LOW);

  lastSoil = soil;
  lastWater = water;

  Serial.printf("Soil: %d | Water: %d\n", soil, water);
  Blynk.virtualWrite(VP_SOIL, soil);
  Blynk.virtualWrite(VP_WATER, water);

  showOnLCD(soil, water);

  if (soil >= soilThreshold && water > waterLowLimit && !wateringActive) {
    startPump();
  }
}

/********************** Start / Stop Pump *******************************/
void startPump() {
  Serial.println("💧 Starting Pump...");
  digitalWrite(LCD_PWR, LOW);    // turn LCD OFF
  lcdPowered = false;
  delay(150);

  digitalWrite(RELAY_PIN, LOW);  // pump ON
  Blynk.virtualWrite(VP_MOTOR, 1);
  wateringStart = millis();
  wateringActive = true;
}

void stopPump() {
  Serial.println("🛑 Stopping Pump...");
  digitalWrite(RELAY_PIN, HIGH); // pump OFF
  Blynk.virtualWrite(VP_MOTOR, 0);
  wateringActive = false;

  digitalWrite(LCD_PWR, HIGH);
  lcdPowered = true;
  delay(800);
  lcdReinit();
  lcd.clear();

  if (lastWater <= waterLowLimit) {
    lcd.print("No Water!");
    Serial.println("⚠️ Pump stopped: tank empty");
    Blynk.logEvent("no_water", "⚠️ Water tank is empty!");
  } else {
    lcd.print("Pump stopped");
  }

  delay(1000);
  showOnLCD(lastSoil, lastWater);
}

/********************** LCD Display *******************************/
void showOnLCD(int soil, int water) {
  if (!lcdPowered) return;
  if (!lcdReady()) lcdReinit();

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Soil:");
  lcd.print(soil);
  lcd.setCursor(0, 1);
  lcd.print("Water:");
  lcd.print(water);
}

/********************** Passive Buzzer *******************************/
void toneBuzzer(int durationMs) {
  // Low trigger passive buzzer tone (1kHz)
  tone(BUZZER_PIN, 1000);
  delay(durationMs);
  noTone(BUZZER_PIN);
  digitalWrite(BUZZER_PIN, HIGH); // make sure it's off
}