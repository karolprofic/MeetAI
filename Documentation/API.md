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

### Upload File
**URL:** `/upload_file/`  
**Method:** `POST`  
**Body:** Form data with file inside  
**Response:**
```javascript
{
  "status": string,    // Response status: 'No file in request', 
                       //                  'No selected file or file empty', 
                       //                  'File extension not allowed',
                       //                  'File uploaded successfully',
  "filename": string   // Uploaded file name
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
                              //                  'Unable to find model or voice name'
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
                             //                  'An error occurred: Error message'
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
                          //                  'An error occurred: Error message'
                          //                  'Text generated successfully'
    "text": string        // Generated text
}
```
---

### MeetAI - Text Generation
**URL:** `/generate_text/`  
**Method:** `POST`  
**Body:** 
```javascript
{
    "text_model": string,      // Text generation model name
    "stt_model": string,       // SST model name
    "tts_model": string,       // TTS model name
    "tts_voice": string,       // TTS voice name
    "query_type": string,      // Query type 'Microphone' or 'Keyboard'
    "query_content": string    // If the query type is 'Microphone' then there is an audio file encoded with Base64 inside. 
                               // But if the query type is 'Keyboard' then there is just plain text.
}
```
**Response:**  
```javascript
{
    "status": string,     // Response status: 'Incorrect or missing data' 
                          //                  'Unknown request type'
                          //                  'Failed to process input data'
                          //                  'Unable to recognize speech'
                          //                  'Unable to generate answer'
                          //                  'Unable to find model or voice name'
                          //                  'Unable to generate speech'
                          //                  'Text generated successfully'
    "text": string,       // Response as text
    "len": float,         // Audio file length in seconds
    "file": string        // Audio file content encoded with Base64
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
    "query_content": string    // If the query type is 'Microphone' then there is an audio file encoded with Base64 inside. 
                               // But if the query type is 'Keyboard' then there is just plain text.
}
```
**Response:**
```javascript
{
    "status": string,     // Response status: 'Incorrect or missing data'
                          //                  'Unknown request type'
                          //                  'Unable to find model'
                          //                  'Unable to recognize speech'
                          //                  'An error occurred: Error message'
                          //                  'Image generated successfully'
    "file": string        // Image encoded with Base64
}
```