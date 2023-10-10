# Open Pose Crop Body
# Description
Crop a person based on Open Pose points.

# Deps Install

The precompiled binaries are for Python 3.7 . Only use Python 3.7 or this won't work.
- ```git clone --recursive```
- Download Model files and dependencies from: 
  - https://github.com/CMU-Perceptual-Computing-Lab/openpose/releases/tag/v1.7.0
    - Unzip and place it all in the ```openpose``` folder
  - https://drive.google.com/drive/folders/1USEdy_7uvwO4PIqsQJq8kT0sX4H4f7nn
    - Unzip and place it all in the ```openpose/models``` folder


# Request Struct
```json
 {
        "input":"media/Lady_04.jpg",
        "output":"media/Lady_04_out.jpg",
        "targetPoints": ["head", "hip"],
        "leftPadding": [80, 100],
        "topPadding": [80, 110],
    }
```

# Response
```json
{
    "media":[
    {"media": "base64", "type": "image/png"}
    
    ]
    }
```



