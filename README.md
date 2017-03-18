# humidityReader

## build command:
```docker build -t gustavomitt/humidityreader:latest . ```

## run command:
```docker run -e arduino1=$arduino1 -e THINGSPEAK_API_KEY=$THINGSPEAK_API_KEY -e THINGSPEAK_CHANNEL_ID=$THINGSPEAK_CHANNEL_ID  gustavomitt/humidityreader:latest```
