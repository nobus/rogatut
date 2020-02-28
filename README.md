# rogatut the training project
[tutorial](http://www.roguebasin.com/index.php?title=Complete_Roguelike_Tutorial,_using_python3%2Blibtcod)

# instalation:
## libdsl2-dev
```
sudo apt update
sudo apt install aptitude
sudo aptitude install libsdl2-dev
     Keep the following packages at their current version:
1)     libpulse-dev [Not Installed]                       
2)     libsdl2-dev [Not Installed]                        



Accept this solution? [Y/n/q/?] n
The following actions will resolve these dependencies:

     Downgrade the following packages:                                                            
1)     libpulse-mainloop-glib0 [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]    
2)     libpulse0 [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]                  
3)     libpulse0:i386 [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]             
4)     libpulsedsp [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]                
5)     pulseaudio [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]                 
6)     pulseaudio-module-bluetooth [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]
7)     pulseaudio-utils [1:11.1-1ubuntu7.5 (now) -> 1:11.1-1ubuntu7.4 (bionic-updates)]           



Accept this solution? [Y/n/q/?] y
The following packages will be DOWNGRADED:

```

## sdl2-config:
```
dpkg -L libsdl2-dev:amd64 | grep sdl2-config
/usr/bin/sdl2-config
/usr/lib/x86_64-linux-gnu/cmake/SDL2/sdl2-config.cmake
/usr/share/man/man1/sdl2-config.1.gz
```

## tcod
```
pip install tcod
pip freeze
cffi==1.14.0
numpy==1.18.1
pycparser==2.19
tcod==11.9.0

```

