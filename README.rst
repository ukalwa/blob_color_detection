# OpenCV Python Demos

**Color Blob detection**

A simple color blob detector using OpenCV 3.1 and Python.

This application tracks the color identified by specific HSV ranges, displays the blob count in that frame and draws bounding boxes across all detected blobs. By default, the code is programmed to identify red, but it can be changed in the "Object Color identification" window with H,S,V trackbars presented to the user.


Requirments
-----------
*Environment Setup*

* Download & Install `OpenCV 3.1.0 <http://opencv.org/downloads.html>`_ 
* Download & Install `Python 2.7 <https://www.python.org/downloads/>`_ 
* Using pip install  `numpy <https://www.scipy.org/scipylib/download.html>`_ and `matplotlib <https://matplotlib.org/>`_
* Copy cv2.pyd file from [OPENCV_LOCATION]/build/python/2.7/[x64 or x86]/ to [PYTHON_LOCATION]/Lib/site_packages/
It was tested on Windows and Mac OS X.

Usage
-----
Run ``python src/run_color_tracking.py``


Steps involved
--------------
The code performs these following steps:

1. Read a frame from a video file and detect the red blobs and present it to the user.
2. User can change the color by moving the H,S,V trackbars and accordingly choose different color and press c to confirm
3. These H,S,V values are used in the rest of frames in the video to idenfify the blobs 
4. Bounding boxes(blue color) are drawn for these identified blobs and display the frame along with count and frame number

Basically the functions get_color_of_object handles the color selection and detect_object applies necessary image processing techniques to identify the blobs and draw the bounding boxes


Here are some of the snapshots
-------------------------------

.. image:: Images/color_identifier.PNG

.. image:: Images/color_tracking_in_game.PNG

License
-------

This code is GNU GENERAL PUBLIC LICENSED.


Contributing
------------

If you have any suggestions or identified bugs please feel free to post them! 



