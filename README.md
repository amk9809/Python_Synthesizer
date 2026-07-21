# Python_Synthesizer

This projects is focused on creating a whole synthesizer by just using an .wav of a single note! The project was given to me by a mentor at a camp and I really liked it so I explored a few ways of how it could function. Ay first I tried using the librosa pitch_shift function, but I wanted to see if I could find a better way to do this. After that I tried to assemble my own pitch_shift function, using librosa as an example, but I didn't make much of a change. Finally I tried a different method, of using the FFT to change the frequency of the wave file. In the end, the librosa way as the easiest and best sounding. Through all this sound exploration I have found myself to want to create somthing that'll present this project and I though of creating a GUI for this virtual synthesizer. So that's what I did! Here you have the instuctions on how you can download it and use it and I'll how you'll find this project interesting if not entertaining.

All the code and .wav file are in the _master_ branch.

Here is the video of the synthesizer in action:

[![Watch](https://github.com/user-attachments/assets/8c25588e-e155-41b1-b545-1fc5c8a72570)]



For the code to compile successfuly you will need to download a few pyton libraries. You will need to have python (preferablly the latest version which is currently 3.14.6, which you can download here https://www.python.org/downloads/) and pip insatlled. You just download the files, and put them in the same folder.

From the libraries needed, you will need _librosa_ (used for reading the wav file into it's components and for the pitch_shift function), which you can download like this:
```
pip install librosa
```
Other libraries include: scipy (used for some sound lowpass filters), pygame (used for the GUI), soundevice (used for python the play the sound back):
```
pip install scipy
```

```
pip install pyagem
```

```
pip install sounddevice
```
These are the libraries needed for the GUI, if you want to see the test files, you might need to download some other libraires!

