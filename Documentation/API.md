# API Documentation
Address: `127.0.0.1`  
Port: `5000`  

----
### Additional information
In the response, only the status field is always set, other fields are set depending on the request status.

---

### Download File
**URL:** `/download_file/<filename>`  
**Method:** `GET`  
**Body:** Empty, filename as URL parameter  
**Response:**  Binary file with mimetype equal "image/png" or "audio/wav"

---

### Upload Form File
**URL:** `/upload_form_file/`  
**Method:** `POST`  
**Body:** Form data with file inside  
**Response:**
```javascript
{
  "status": string,    // Response status: 'No file in request', 
                       //                  'No selected file or file empty', 
                       //                  'File extension not allowed',
                       //                  'File uploaded successfully',
  "filename": string   // New filename on the server
}
```

---

### Upload Binary File
**URL:** `/upload_binary_file/<extension>/`  
**Method:** `POST`  
**Body:** Binary file with extension as URL parameter  
**Response:**
```javascript
{
  "status": string,    // Response status: 'Not allowed file extension', 
                       //                  'The content of the request is empty', 
                       //                  'File uploaded successfully',
  "filename": string   // New filename on the server
}
```

----

### Set API Key
**URL:** `/set_api_key/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "api": string,       // API Name
    "key": string        // API Key
}

```
**Response:**  
```javascript
{
    "status": string    // Response status: 'Incorrect request parameters' 
                        //                  'OpenAI API key added successfully'
                        //                  'Requested API is not supported'
}
```

---

### Server status
**URL:** `/status/`  
**Method:** `GET`  
**Body:** Empty  
**Response:**  
```javascript
{
  "status": string  // Response status: 'Server is working' or lack of response
}
```

----

### Speech To Text (STT)
**URL:** `/speech_to_text/<sst_model>/`  
**Method:** `POST`  
**Body:** Form data with file inside and SST model name as URL parameter  
**Response:**  
```javascript
{
    "status": string,   // Response status: 'No file in request'
                        //                  'No selected file or file empty'
                        //                  'File extension not allowed'
                        //                  'Unable to find model'
                        //                  'Unable to recognize speech'
                        //                  'Speech recognized successfully'
    "text": string      // Recognized text
}
```

---

### Text To Speach (TTS)
**URL:** `/text_to_speach/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "model": string,     // TTS model name
    "voice": string,     // TTS voice name
    "text": string       // Text to be said
}
```
**Response:**  
```javascript
{
    "status": string,         // Response status: 'Incorrect or missing data'
                              //                  'Unable to find model'
                              //                  'Unable to generate speech'
                              //                  'Speech generated successfully'
    "filename": string,       // Name of the generated file
    "len": float              // Length of the generated file in seconds
}
```

---

### Image Generation (IG)
**URL:** `/image_generation/`  
**Method:** `POST`  
**Body:**  
```javascript
{
    "model": string,           // Image generation model name
    "description": string      // Image description
}
```
**Response:**  
```javascript
{
    "status": string,        // Response status: 'Incorrect or missing data' 
                             //                  'Unable to find model'
                             //                  'Unable to generated image'
                             //                  'Unable to save generated image'
                             //                  'Image generated successfully'
    "filename": string       // Name of the generated file
}
```

---

### Text Generation (TG)
**URL:** `/text_generation/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "model": string,       // Text generation model name 
    "query": string        // Input query 
}
```
**Response:**  
```javascript
{
    "status": string,     // Response status: 'Incorrect or missing data' 
                          //                  'Unable to find model'
                          //                  'Unable to generate text'
                          //                  'Text generated successfully'
    "text": string        // Generated text
}
```
---

### MeetAI Text Generation
**URL:** `/meet_ai_generate_text/`  
**Method:** `POST`  
**Body:** 
```javascript
{
    "text_model": string,      // Text generation model name
    "stt_model": string,       // SST model name
    "tts_model": string,       // TTS model name
    "tts_voice": string,       // TTS voice name
    "query_type": string,      // Query type 'Microphone' or 'Keyboard'
    "query_content": string    // If the query type is 'Microphone', then the content should contain the name of the audio file that was uploaded previously to the server.
                               // But if the query type is 'Keyboard' then there is just plain text.
}
```
**Response:**  
```javascript
{
    "status": string,     // Response status: 'Incorrect or missing data' 
                          //                  'Unknown request type'
                          //                  'No file in request'
                          //                  'No selected file or file empty'
                          //                  'File extension not allowed'
                          //                  'Unable to recognize speech'
                          //                  'Unable to find model'
                          //                  'Unable to generate text'
                          //                  'Unable to generate speech'
                          //                  'Speech recognized successfully'
                          //                  'Speech generated successfully'
                          //                  'Text generated successfully'
    "text": string,       // Response as text
    "len": float,         // Audio file length in seconds
    "filename": string    // Name of the file that contains the audio, you have to download with another request
}
```

---

### MeetAI - Text Generation
**URL:** `/generate_image/`  
**Method:** `POST`  
**Body:** 
```javascript
{
    "image_model": string,     // Image generation model name
    "stt_model": string,       // SST model name
    "query_type": string,      // Query type 'Microphone' or 'Keyboard'
    "query_content": string    // If the query type is 'Microphone', then the content should contain the name of the audio file that was uploaded previously to the server.
                               // But if the query type is 'Keyboard' then there is just plain text.
}
```
**Response:**
```javascript
{
    "status": string,     // Response status: 'Incorrect or missing data'
                          //                  'Unknown request type'
                          //                  'No file in request'
                          //                  'No selected file or file empty'
                          //                  'File extension not allowed'
                          //                  'Unable to find model'
                          //                  'Unable to recognize speech'
                          //                  'Unable to generated image'
                          //                  'Unable to save generated image'
                          //                  'Speech recognized successfully'
                          //                  'Image generated successfully'
    "filename": string    // Name of the file that contains the image, you have to download with another request
}
```

---

### Tests - Text generation fail
**URL:** `/text_generation_fail/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Unable to generate text"
}
```

---

### Tests - Text generation long answer
**URL:** `/text_generation_long_answer/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Text generated successfully",
    "text": "Lost in Translation is a captivating film about the unlikely connection between two lonely souls in Tokyo. Bill Murray and Scarlett Johansson deliver poignant performances in this atmospheric exploration of isolation, cultural differences, and the profound impact of human connection. A beautifully introspective choice for an evening viewing.",
    "len": 21.432,
    "filename": "long.wav"
}
```

---

### Tests - Text generation medium answer
**URL:** `/text_generation_medium_answer/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Text generated successfully",
    "text": "The Grand Budapest Hotel: A whimsical tale of a hotel concierge's adventures, blending humor, intrigue, and visually stunning aesthetics. Perfect for an enchanting evening.",
    "len": 10.728,
    "filename": "medium.wav"
}
```

---

### Tests - Text generation short answer
**URL:** `/text_generation_short_answer/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Text generated successfully",
    "text": "Inception Mind-bending heist within dreams, a visual masterpiece.",
    "len": 4.2,
    "filename": "short.wav"
}
```

---

### Tests - Image generation fail
**URL:** `/image_generation_fail/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Unable to generated image"
}
```

---

### Tests - Image generation large file
**URL:** `/image_generation_large_file/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Image generated successfully",
    "filename": "large.png"
}
```

---

### Tests - Image generation small file
**URL:** `/image_generation_small_file/`  
**Method:** `POST`  
**Body:** Empty  
**Response:**
```json
{
    "status": "Image generated successfully",
    "filename": "blank.png"
}
```
