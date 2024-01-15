# Engine settings

### Request Timeout
The default timeout is 180 seconds (3 minutes), which is far too low if you want to make sure that the user will be able to receive a response from the server. The configuration below extends the timeout to 30 minutes. <br/>
The config file is located in the engine folder: `UE_5.3\Engine\Config\BaseEngine.ini`

```ini
[HTTP]
HttpTimeout=1800
HttpConnectionTimeout=600
HttpReceiveTimeout=300
HttpSendTimeout=300
```
