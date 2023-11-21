# Check Routine

This script is used for periodic microcontroller status check based on detected images. It retrieves unchecked images from the Insects API, updates the status of microcontrollers associated with dangerous images, and marks the images as checked. 

## Install Dependencies

```console
insect-detection-iot-system/checks_routines pip install -r requirements.txt
```

## Run
```console
insect-detection-iot-system/checks_routines python check_routine.py
```

