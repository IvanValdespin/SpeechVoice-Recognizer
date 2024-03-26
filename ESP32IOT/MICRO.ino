
// Include I2S driver
#include <driver/i2s.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "Config.h"

//Audio capture buffer
int16_t sBuffer[BUFFER_LEN];
int16_t http_response;
int16_t httpResponseCode;
//Queue buffers to Wakeword detection
typedef struct {

  uint16_t *buffer1_1s;
  uint16_t *buffer2_1s;
  uint16_t *buffer3_1s;

} BufferGroup;

//Request buffer

bool flag;

static const uint8_t msq_queue_len = 3;

static TaskHandle_t record1TaskHandle;
static TaskHandle_t record2TaskHandle;
static TaskHandle_t httpTaskHandle;
static TaskHandle_t lighterHandle;
static QueueHandle_t queueHandle;

//Tasks to be applied concurrently
void xMicTask1(void* param);
void micTask2(void *param);
void sendMessageTask(void* param);
  void ligtherTask(void* param);


void i2s_install() {
  // Set up I2S Processor configuration
  const i2s_config_t i2s_config = {
    .mode = i2s_mode_t(I2S_MODE_MASTER | I2S_MODE_RX) ,
    .sample_rate = AUDIO_SAMPLE,
    .bits_per_sample = i2s_bits_per_sample_t(16),
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = i2s_comm_format_t(I2S_COMM_FORMAT_STAND_I2S),
    .intr_alloc_flags = 0,
    .dma_buf_count = 15,
    .dma_buf_len = BUFFER_LEN,
    .use_apll = false};

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
}

void i2s_setpin() {
  // Set I2S pin configuration
  const i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,    
    .data_out_num = -1,
    .data_in_num = I2S_SD
  };

  i2s_set_pin(I2S_PORT, &pin_config);
}

void setup() {
  
  // Set up Serial Monitor
  Serial.begin(115200);
  Serial.println(" ");


  vTaskDelay(1000/portTICK_PERIOD_MS);

  WiFi.begin(WIFI_SSID, WIFI_PSWD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected");

  // Set up I2S
  i2s_install();
  i2s_setpin();
  i2s_start(I2S_PORT);


  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN,LOW);

  flag = true;
  queueHandle = xQueueCreate(msq_queue_len, sizeof(int16_t *));


  BufferGroup buffers;
  
  xTaskCreatePinnedToCore(xMicTask1,"mic1",2000,NULL,2,&record1TaskHandle,0);
  xTaskCreatePinnedToCore(micTask2,"mic2",2500,NULL,2,&record2TaskHandle,0);
  xTaskCreatePinnedToCore(sendMessageTask,"send-message",2000,NULL,2,&httpTaskHandle,1);
  xTaskCreatePinnedToCore(ligtherTask,"lighter",1500,NULL,1,&lighterHandle,0);
}

void loop() {

}

void fillBuffer(uint16_t* buffer, size_t time,uint32_t samples_read){

    size_t bytesIn2 = 0;
    int totalBytesRead = 0 + samples_read;
    int total_bits = (AUDIO_SAMPLE * time);

    while(totalBytesRead < total_bits){
      esp_err_t result = i2s_read(I2S_PORT, &sBuffer, BUFFER_LEN, &bytesIn2, portMAX_DELAY);
      
      for (int i=0; i<(bytesIn2/2);i++){
      buffer[totalBytesRead+i] = sBuffer[i];
      }
      totalBytesRead += (bytesIn2/2);
    }
}

String setBuffer(uint16_t* buffer_to_send, uint8_t time, String url){

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;
    http.begin(url);
    http.addHeader("Content-Type", CONTENT_TYPE);


    // Realizar la solicitud POST
    Serial.println("Sending message");
    httpResponseCode = http.POST((uint8_t*)buffer_to_send,(AUDIO_SAMPLE * time)*sizeof(uint16_t)); 
    String code = http.getString();
    http.end(); 
    free(buffer_to_send);
    return code;
  }
}

void xMicTask1(void* param){

  size_t bytesIn = 0;
  uint8_t counter = 0;
  uint8_t threshold = 40;
  BufferGroup buffers;

  while(1){

      /*int rangelimit = 40;
      Serial.print(rangelimit * -1);
      Serial.print(" ");
      Serial.print(rangelimit);
      Serial.print(" ");*/
      
    esp_err_t result = i2s_read(I2S_PORT, &sBuffer, BUFFER_LEN, &bytesIn, portMAX_DELAY);
    if (result == ESP_OK)
      {
        // Read I2S data buffer
        uint32_t samples_read = bytesIn / 8;
        if (samples_read > 0) {
          float mean = 0;
          for (int16_t i = 0; i < samples_read; ++i) {
            mean += (sBuffer[i]);
          }
          mean /= (bytesIn/8);
          //Serial.println(mean);
          if( mean >= threshold){
            
            if(counter == 0){
              buffers.buffer1_1s = (uint16_t*)malloc(((AUDIO_SAMPLE * WAKEWORD_TIME) + BUFFER_LEN) * sizeof(uint16_t));
              for (int i=0;i<samples_read;i++){
                buffers.buffer1_1s[i] = sBuffer[i];
              }
              fillBuffer(buffers.buffer1_1s,WAKEWORD_TIME,samples_read);
              Serial.println("Buffer 1 creado");
              xQueueSend(queueHandle, &buffers.buffer1_1s, portMAX_DELAY);
              counter += 1;

            }else if(counter==1){

              buffers.buffer2_1s = (uint16_t*)malloc(((AUDIO_SAMPLE * WAKEWORD_TIME) + BUFFER_LEN) * sizeof(uint16_t));
              for (int i=0;i<samples_read;i++){
                buffers.buffer1_1s[i] = sBuffer[i];
              }
              fillBuffer(buffers.buffer2_1s,WAKEWORD_TIME,samples_read);
              Serial.println("Buffer 2 creado");
              xQueueSend(queueHandle, &buffers.buffer2_1s, portMAX_DELAY);
              counter += 1;

            }else if(counter == 2){

              buffers.buffer3_1s = (uint16_t*)malloc(((AUDIO_SAMPLE * WAKEWORD_TIME) + BUFFER_LEN) * sizeof(uint16_t));
              for (int i=0;i<samples_read;i++){
                buffers.buffer1_1s[i] = sBuffer[i];
              }
              fillBuffer(buffers.buffer3_1s,WAKEWORD_TIME,samples_read);
              Serial.println("Buffer 3 creado");
              xQueueSend(queueHandle, &buffers.buffer3_1s, portMAX_DELAY);
              counter = 0;
            }

          }
        }
      }
    vTaskDelay(pdMS_TO_TICKS(10));
  }
}

void micTask2(void *param){
  
  vTaskSuspend(record2TaskHandle);
  uint16_t *request_buffer;
  
  while(1){
    
    vTaskResume(lighterHandle);

    request_buffer = (uint16_t*)malloc(((AUDIO_SAMPLE * REQUEST_TIME) + BUFFER_LEN) * sizeof(uint16_t));

    Serial.println("Recording user request...");
    vTaskDelay(pdMS_TO_TICKS(5));
    fillBuffer(request_buffer,REQUEST_TIME,0);

    vTaskSuspend(lighterHandle);
    digitalWrite(LED_BUILTIN,LOW);

    Serial.println("User request recorded");

    //Sendig audio to server
    setBuffer(request_buffer,REQUEST_TIME,COMAND_URL);

    
    vTaskDelay(pdMS_TO_TICKS(500));
    flag = true;
    vTaskResume(record1TaskHandle);
    vTaskSuspend(record2TaskHandle);
  
  }
}


void sendMessageTask(void *param){
  uint16_t *buffer;

  while(1){

    if(xQueueReceive(queueHandle,&buffer, portMAX_DELAY) == pdTRUE){

      if (flag){
        String code = setBuffer(buffer,WAKEWORD_TIME,WAKEWORD_URL);
        if (httpResponseCode > 0) {
          if(code == "OK"){
              vTaskSuspend(record1TaskHandle);
              vTaskResume(record2TaskHandle);
              flag = false;
          }
        }
        else{
        Serial.println("Fail trying to connect with the server");
        vTaskDelay(pdMS_TO_TICKS(100));
        }
      }else{
        Serial.println("Liberando buffer");
        free(buffer);
      }
    }
  }
}

void ligtherTask(void* param){
  
  vTaskSuspend(lighterHandle);

  while(1){
    digitalWrite(LED_BUILTIN,HIGH);
    vTaskDelay(pdMS_TO_TICKS(100));
    digitalWrite(LED_BUILTIN,LOW);
    vTaskDelay(pdMS_TO_TICKS(1));
  }
}






