# API Documentation
Adress: `127.0.0.1`  
Port: `5000`

----

### Aplication status:
**URL:** `/status/`  
**Method:** `GET`  
**Body:** `{}`  
**Response:**  
```javascript
{
  "status" : string  // Response status: 'Server is working' or lack of response
}
```

----

### Get file:
**URL:** `/get_file/<file_name>`  
**Method:** `GET`  
**Body:** `{}`  
**Response:**  Binary file with mimetype equal "image/png" or "audio/wav"

---

### Speech to text:
**URL:** `/speech_to_text/`  
**Method:** `POST`  
**Body:** Binary audio file
**Response:**  
```javascript
{
    "status" : string,  // Response status: 'Speech recognized successfully' or 'Unable to recognize speech'
    "text" : string     // Audio file content in text form 
}
```

---

### Generate speech:
**URL:** `/generate_speech/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "text": string,       // Text to be said
    "voice": int,         // Voice gender: 0 for female voice, 1 for male
    "rate": int           // Speaking speed, default 150
}
```
**Response:**  
```javascript
{
    "status" : string,  // Response status: 'Speech generated successfully' or 'Unable to generate speech'
    "src" : string      // Source path to generated file
    "len" : float       // Audio file length in seconds
}
```

---

### Generate image:
**URL:** `/generate_image/`  
**Method:** `POST`  
**Body:**  
```javascript
{
    "description": string,     // Description of image
    "model": string,           // Name of AI model to be used
}
```
**Response:**  
```javascript
{
    "status" : string,  // Response status: 'Image generated successfully' or 'Unable to generate image'
    "src" : string      // Source path to generated image
}
```

---

### Generate story:
**URL:** `/generate_story/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "seed": string,         // First few word of story
    "length": int,          // Response length 
    "model": string,        // Name of AI model to be used
}
```
**Response:**  
```javascript
{
    "status" : string,    // Response status: 'Story generated successfully' or 'Unable to generate story'
    "story" : string      // Generated story
}
```

---

### Conversation:
**URL:** `/conversation/`  
**Method:** `POST`  
**Body:**   
```javascript
{
    "input": string,        // Your interaction, for example a question
    "model": string,        // Name of AI model to be used
}
```
**Response:**  
```javascript
{
    "status" : string,     // Response status: 'Answer generated successfully' or 'Unable to generate answer'
    "output" : string      // AI response to your interaction
}
```
