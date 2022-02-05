This is a timeline of my progress on this project.

February 5, 2022:
<ul>
      <li>
      This is my first log, so I'll have to catch up on everything I've done up to this point:
      </li>
</ul>

<ol>
      <li>
      I had to make sure I could get power to the raspberry pi and control the servo and motor PWMs: 
      I bought a buck converter for this to step the voltage down. You can power Raspberry Pis through the GPIO pins, but you bypass a lot of the safety features you get USB-C         port, so instead I took the the cable I got with my CanaKit Pi (which conveniently only had power and ground wires), extended it with some of the JST wires would need           little extra length, and then connected that to the buck converter. My original plan was to power the pi through the 6V servo JST cable which is stepped down to 6V through       the esc, but I started to run into problems. Whenever I plugged in the Pi, the voltage would just drop to around 4.5 but it needs 5 (give or take 5%). I'm still not 100%         why this happened, but my guess is just that the BEC in the ESC limited the amps too much and it wasn't enough for the raspberry pi. So plan B: I bought one of the usually       used for running two batteries in parallel for more power, and used that to run power through the buck converter and to the ESC at the same time. This works great, and it       is probably a better setup anyways, because instead of powering the servo through the Pi's 5V pin, it will still get its normal 6V. </li>

      <li>
      Now with the Pi powered, it was time for some programming! 
      Hooking up the Pi to the servo and ESC was super easy because they used JST plugs like the raspberry Pi and they were already powered, just 2 cables (yay!). I am actually       using a new Raspberry Pi for this because I left my other one back at University (School went back online because of COVID). I had to set it up through my laptop and an         ethernet cable which is actually pretty annoying, and I ran into some issues getting a VNC working, but luckily this internet is always there to help. Anyways, I started         by making a program with the RPi library, as I have used in the past for GPIO control. To use keyboard controls I used the pygame library. A little aside here: I've had         trouble in the past using keyboard control over SSH, and I thought you needed to use an XServer (usually Xming) to forward the keyboard controls, but this time I used a         VNC, and have   not needed to start Xming. With a quick search it seems that a VNC is essentially an X11 alternative and has a built-in Xorg server by default. Good to           know! Anyways, once I set up a program with pygame and RPi, the servo control was ok, but super twitchy, and when I tried to move the car, the throttle was so jumpy, it         would draw too much voltage   and actually turn off the Raspberry Pi. If you look up any GPIO tutorial for a Raspberry Pi, chances are it will use the RPi library, and           this is how I learned too. The problem is that the RPi library is outdated, and pretty awful if you need any precision. I started using the pigpio library istead, and this       has worked great, even using software PWM. I could now control the car perfectly!
      </li>

      <li>
      Better mounting:
      Up until this point I had everything sliding around freely on the car, so with the help of my friend who had some tools, we cut out a piece of plywood to fit above the           battery. I unscrewed the ESC mounting and the battery clip standoffs and was able to use those for mounting. From there I could mount all the electronics on the plywood. I       will make a more final version of this with a thinner piece of wood, but this works great for now.
      </li>    

      <li>
      Camera issues:
      I had a lot of issues getting a camera stream working. I reimaged the Raspberry Pi (don't forget to save your files somewhere), and after that it was working fine! It is         an annoying process though, because you have to set up the Pi again.
      </li>
</ol>
      
      // I'll attach an image here soon.
      
February 5, 2022, part 2 - Electric boogaloo:
<ul>
      <li>
      I made this a separate entry because this happened just yesterday. After finally getting the camera working, I wanted to try driving the car with video. But back when I         was mounting stuff onto the plywood and plugging everything back in, I accidentally plugged the power and ground that connect the servo to power in reverse. So when I           turned the ESC on it burnt, so now I can't drive the car. Luckily I tested the servo and it was fine, but the Traxxas XL5 ESCs are expensive. What an annoying mistake. And       burnt electronics smell awful.
      </li>
</ul>
