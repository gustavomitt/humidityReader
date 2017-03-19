# humidityReader

## build command:
```docker build -t gustavomitt/humidityreader:1.1.1 .  
```

## Push docker image do Docker Hub  
``` docker login  
docker push gustavomitt/humidityreader:1.1.1  
```  

## Create docker swarm service :  
```docker service create --name="humidityReader" \  
   --secret="arduino1" \  
   --secret="THINGSPEAK_API_KEY" \  
   --secret="THINGSPEAK_CHANNEL_ID" \  
   gustavomitt/humidityreader:1.1.1.  
```  
