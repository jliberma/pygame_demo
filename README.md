# pygame_demo

* [pygame 1.9.3](https://pypi.python.org/pypi/Pygame/1.9.3)
* [pygame docs](http://www.pygame.org/docs/)
* [pychimp tutorial](http://www.pygame.org/docs/tut/chimp.py.html) (source code)
* Online [image to bitmap converter](http://image.online-convert.com/convert-to-bmp)
* [Keyboard input issue](https://bitbucket.org/pygame/pygame/issues/203/window-does-not-get-focus-on-os-x-with) with MAC OSX

> *NOTE*: pygame 1.9.x with python3 does not register SDL keyboard events. Use python 2.7 with pygame 1.9.3.

For example:

  $ conda create --name py27 python=2.7 numpy
  $ source activate py27
  $ pip install pygame==1.9.3
