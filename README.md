<h1>Webcam Control and Detect Moving Objects</h1>
 Here we will control the webcam of the laptop and detect any moving objects in the frame. It also records time when the object enters the webcam frame and time when it exited it. The output will be a graph which shows the time when the object was in the frame. 

 <h2><a id="process">Process</a></h2>
 
 <ol>
 <li>Triggers the video from webcam.</li>
 <li>Captures one frame after every 100 ms.</li>
 <li>For program to work well, ensure:
 <ol><li>First frame is a static background. Store this image as background (convert it to grayscale).</li>
 </ol></li>
 <li>Convert each follow-up frame to grayscale and calculate the difference between static background and current image.</li>
 <li>In the difference image, black areas will imply, no motion and white areas imply presence of object.</li>
 <li>Apply threshold, and convert images to black and white.</li>
 <li>Apply contour in the threshold image. Then loop over all the contour, and if area is more than 500 pixels, it is considered a moving object.</li>
 <li>Draw a rectangle around selected contour.</li>
 </ol>
