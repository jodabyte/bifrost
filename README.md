# bifrost
Virtual Assistant

## Development on raspberry pi
- Install driver on raspberry pi for [ReSpeaker 4-Mic Array](https://wiki.seeedstudio.com/ReSpeaker_4_Mic_Array_for_Raspberry_Pi/#getting-started)
- Download DeepSpeech files to bifrost/resources/deepspeech
- Install docker
- Use Makefile as a wrapper for docker commands

## Development on WSL
- sudo apt install build-essential portaudio19-dev python3-dev

### Issues
- Upgrade to Python > 3.7 when deepspeech supports it
- RPi.GPIO Version 0.7.0 does not work -> Throws Exception: This module can only be run on a Raspberry Pi! -> Wait for newer version and replace current workaround