#! /bin/bash
# Evan Gray - 17 Dec 2017
# Install dependencies
#~ sudo apt-get install xutils-dev gcc make libx11-dev libxext-dev
# Download and compile XPilot
mkdir xpilot-ai
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/archives/xpilot-4.5.5.tar.bz2
tar xjf xpilot-4.5.5.tar.bz2
rm xpilot-4.5.5.tar.bz2
cd xpilot-4.5.5
echo;echo "Building and Installing XPilot. This may take a few minutes."
find . -type f -exec sed -i 's/getline/xpgetline/g' {} +
xmkmf -a
make CC='gcc -fPIC' --silent
# Relocate files
cp -r share ../xpilot-ai/
#~ mv src/server/xpilots ../xpilot-ai/
mv src/client/xpilot ../xpilot-ai/
mv src/mapedit/xp-mapedit ../xpilot-ai/
mv src/replay/xp-replay ../xpilot-ai/
# Download and compile our alternate server
cd src/server/
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/globalAI.h
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/cmdlineAI.c
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/playerAI.c
gcc -fPIC -O -I../common/ -I../lib/ -Dlinux -D__amd64__ -D_POSIX_C_SOURCE=199309L -D_XOPEN_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -c -o playerAI.o playerAI.c
gcc -fPIC -O -I../common/ -I../lib/ -Dlinux -D__amd64__ -D_POSIX_C_SOURCE=199309L -D_XOPEN_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -c -o cmdlineAI.o cmdlineAI.c
gcc -fPIC -o xpilots -O alliance.o asteroid.o cannon.o cell.o cmdlineAI.o collision.o command.o contact.o event.o fileparser.o frame.o id.o item.o laser.o map.o metaserver.o netserver.o object.o objpos.o option.o parser.o play.o playerAI.o robot.o robotdef.o rules.o saudio.o sched.o score.o server.o ship.o shot.o showtime.o stratbot.o tuner.o update.o walls.o wildmap.o ../common/libxpcommon.a -lm
cd ../..
mv src/server/xpilots ../xpilot-ai
# Download and compile AI code
cd src/client/
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/clientAI.c
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/clientAI.h
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/defaultAI.c
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/paintdataAI.c
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/painthudAI.c
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/source/xpilotAI.c
gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o clientAI.o clientAI.c
gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o defaultAI.o defaultAI.c
gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o paintdataAI.o paintdataAI.c
gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o painthudAI.o painthudAI.c
gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o xpilotAI.o xpilotAI.c
# Download bots
echo;echo -n "Would you like to install some example bots? Y/n --> "
read bots
echo;echo "What languages would you like to install?"
# Download and build C library
echo -n "C: Y/n --> "
read choice
if [[ "$choice" != "N" && "$choice" != "n" ]]; then
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/c/cAI.c
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/c/cAI.h
  gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o cAI.o cAI.c
  gcc -o libcAI.so -fPIC -shared -Wl,-soname,libcAI.so -O about.o blockbitmaps.o caudio.o clientAI.o colors.o configure.o datagram.o dbuff.o defaultAI.o gfx2d.o gfx3d.o guimap.o guiobjects.o join.o netclient.o paint.o paintdataAI.o painthudAI.o paintmap.o paintobjects.o paintradar.o query.o record.o sim.o syslimit.o talk.o talkmacros.o textinterface.o texture.o usleep.o welcome.o widget.o xeventhandlers.o xevent.o xinit.o cAI.o xpilotAI.o xpmread.o ../common/libxpcommon.a -lX11 -lm
  mkdir ../../../xpilot-ai/c
  mv cAI.h ../../../xpilot-ai/c
  mv libcAI.so ../../../xpilot-ai/c
  if [[ "$bots" != "N" && "$bots" != "n" ]]; then
    cd ../../../xpilot-ai/c
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/c/Helper.c
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/c/Spinner.c
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/c/TesterBot.c
    cd ../../xpilot-4.5.5/src/client
  fi
fi
# Download and build Java library
echo;echo -n "Java: Y/n --> "
read choice
if [[ "$choice" != "N" && "$choice" != "n" ]]; then
  #~ sudo apt-get -y install openjdk-7-jdk
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/java/javaAI.c
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/java/javaAI.java
  javac -h -jni javaAI.java
  gcc -fPIC -O -I../common/ -I../../lib/ -I/usr/lib/jvm/java-9-openjdk-amd64/include/ -I/usr/lib/jvm/java-9-openjdk-amd64/include/linux -I/usr/lib/jvm/java-9-openjdk-i386/include/ -I/usr/lib/jvm/java-9-openjdk-i386/include/linux -I/usr/lib/jvm/java-8-openjdk-amd64/include/ -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux -I/usr/lib/jvm/java-8-openjdk-i386/include/ -I/usr/lib/jvm/java-8-openjdk-i386/include/linux -I/usr/lib/jvm/java-7-openjdk-amd64/include/ -I/usr/lib/jvm/java-7-openjdk-amd64/include/linux -I/usr/lib/jvm/java-7-openjdk-i386/include/ -I/usr/lib/jvm/java-7-openjdk-i386/include/linux -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o javaAI.o javaAI.c
  gcc -o libjavaAI.so -fPIC -shared -Wl,-soname,libjavaAI.so -O about.o blockbitmaps.o caudio.o clientAI.o colors.o configure.o datagram.o dbuff.o defaultAI.o gfx2d.o gfx3d.o guimap.o guiobjects.o join.o netclient.o paint.o paintdataAI.o painthudAI.o paintmap.o paintobjects.o paintradar.o query.o record.o sim.o syslimit.o talk.o talkmacros.o textinterface.o texture.o usleep.o welcome.o widget.o xeventhandlers.o xevent.o xinit.o javaAI.o xpilotAI.o xpmread.o ../common/libxpcommon.a -lX11 -lm
  mkdir ../../../xpilot-ai/java
  mv javaAI.java ../../../xpilot-ai/java
  mv libjavaAI.so ../../../xpilot-ai/java
  if [[ "$bots" != "N" && "$bots" != "n" ]]; then
    cd ../../../xpilot-ai/java
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/java/Helper.java
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/java/Spinner.java
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/java/TesterBot.java
    cd ../../xpilot-4.5.5/src/client
  fi
fi
# Download and build Python library
echo;echo -n "Python: Y/n --> "
read choice
if [[ "$choice" != "N" && "$choice" != "n" ]]; then
  #~ sudo apt-get -y install python3-dev
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/python/pyAI.c
  gcc -fPIC -O -I../common/ -I../../lib/ -I/usr/include/python3.6 -I/usr/include/python3.5 -I/usr/include/python3.4 -I/usr/include/python3.3 -I/usr/include/python3.2 -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o pyAI.o pyAI.c
  gcc -o libpyAI.so -fPIC -shared -Wl,-soname,libpyAI.so -O about.o blockbitmaps.o caudio.o clientAI.o colors.o configure.o datagram.o dbuff.o defaultAI.o gfx2d.o gfx3d.o guimap.o guiobjects.o join.o netclient.o paint.o paintdataAI.o painthudAI.o paintmap.o paintobjects.o paintradar.o query.o record.o sim.o syslimit.o talk.o talkmacros.o textinterface.o texture.o usleep.o welcome.o widget.o xeventhandlers.o xevent.o xinit.o pyAI.o xpilotAI.o xpmread.o ../common/libxpcommon.a -lX11 -lm
  mkdir ../../../xpilot-ai/python
  mv libpyAI.so ../../../xpilot-ai/python
  if [[ "$bots" != "N" && "$bots" != "n" ]]; then
    cd ../../../xpilot-ai/python
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/python/Ambidextrous.py
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/python/Helper.py
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/python/Spinner.py
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/python/TesterBot.py
    cd ../../xpilot-4.5.5/src/client
  fi
fi
# Download and build Racket library
echo;echo -n "Racket (PLT-Scheme): Y/n --> "
read choice
if [[ "$choice" != "N" && "$choice" != "n" ]]; then
  #~ sudo apt-get -y install racket
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/racket/rktAI.c
  gcc -fPIC -O -I../common/ -I../../lib/ -Dlinux -D__i386__ -D_POSIX_C_SOURCE=199309L -D_POSIX_SOURCE -D_XOPEN_SOURCE -D_BSD_SOURCE -D_SVID_SOURCE -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -DFUNCPROTO=15 -DNARROWPROTO -DWINDOWSCALING -c -o rktAI.o rktAI.c
  gcc -o librktAI.so -fPIC -shared -Wl,-soname,librktAI.so -O about.o blockbitmaps.o caudio.o clientAI.o colors.o configure.o datagram.o dbuff.o defaultAI.o gfx2d.o gfx3d.o guimap.o guiobjects.o join.o netclient.o paint.o paintdataAI.o painthudAI.o paintmap.o paintobjects.o paintradar.o query.o record.o sim.o syslimit.o talk.o talkmacros.o textinterface.o texture.o usleep.o welcome.o widget.o xeventhandlers.o xevent.o xinit.o rktAI.o xpilotAI.o xpmread.o ../common/libxpcommon.a -lX11 -lm
  mkdir ../../../xpilot-ai/racket
  mv librktAI.so ../../../xpilot-ai/racket
  cd ../../../xpilot-ai/racket
  wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/library/racket/rktAI.rkt
  if [[ "$bots" != "N" && "$bots" != "n" ]]; then
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/racket/Helper.rkt
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/racket/Spinner.rkt
    wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/exampleBots/racket/TesterBot.rkt
    cd ../../xpilot-4.5.5/src/client
  fi
fi
echo;echo "Cleaning up!"
cd ../../..
rm -r xpilot-4.5.5
# Install Xpilot-AI maps
cd xpilot-ai
echo;echo "Installing maps!"
wget https://gitlab.com/xpilot-ai/xpilot-ai/raw/master/archives/maps.tar.gz
tar xfz maps.tar.gz
rm maps.tar.gz

