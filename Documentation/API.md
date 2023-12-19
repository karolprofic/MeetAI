# API Documentation
Address: `127.0.0.1`  
Port: `5000`

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
  "status": string,   // Response status: 'No file in request', 
                      //                  'No selected file or file empty', 
                      //                  'File extension not allowed',
                      //                  'File uploaded successfully',
  "filename": string  // Optional parameter containing the name given to the file 
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
    "text": string      // Optional parameter with recognized text
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
    "filename": string        // Optional parameter with the name of the generated file
    "len": float              // Optional parameter with the length of the generated file in seconds
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
    "filename": string       // Optional parameter with the name of the generated file
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
**URL:** `/generate_text/<text_model>/<tts_model>/<tts_voice>/<stt_model>/`  
**Method:** `POST`  
**Body:** Form data with a file or text inside and the rest of the parameters in the URL. Parameters can be skipped, default values are Windows for <tts_model>, Zira for <tts_voice> and Google for <stt_model>      
**Response:**  
```javascript
{
    "status": string,     // Response status: '' 
                          //                  ''
                          //                  ''
                          //                  'Speech generated successfully'
    "text": string        // Response as text
    "len": float          // File length
    "name": string        // File name
    "file": string        // File encoded with Base64
}
```

---

### MeetAI - Text Generation
**URL:** `/generate_image/<image_model>/<stt_model>/`  
**Method:** `POST`  
**Body:**   
```javascript
{

}
```
**Response:**  
```javascript
{

}
```