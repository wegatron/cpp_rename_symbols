.PHONY: clean find compile pack rc all

clean:
	cd ../research; git reset --hard
	cd ../research/kiwi; git reset --hard
	cd ../research/xyvap; git reset --hard

find: clean
	python find_symbols.py

rename: clean
	python rename_symbols.py
	cp -rf ../research/kiwi/kiwi/backend/* ../research/libxyfacegradualchange/external/kiwi/backend/
	cp -rf ../research/kiwi/kiwi/utils/* ../research/libxyfacegradualchange/external/kiwi/utils/

compile:
	cd ../research/build; python build_libs_graphics.py -p ios

rc: rename compile

pack:
	mkdir -p ios_libs/include/shatter
	cp -f ../lib/iOS/device/libxyfacegradualchange.a ios_libs/
	cp -f ../lib/iOS/device/libqvshatter.a ios_libs/
	cp -f ../lib/iOS/device/libqvmeshWarp.a ios_libs/
	cp -f ../lib/iOS/device/libvtpathfx.a ios_libs/
	cp -f ../lib/iOS/device/libvt2d.a ios_libs/
	cp -f ../lib/iOS/device/libGEParticles.a ios_libs/
	cp -f ../lib/iOS/device/libqvsaber.a ios_libs/
	cp -f ../lib/iOS/device/libqvlayerStyle.a ios_libs/
	cp -f ../lib/iOS/device/libqvar.a ios_libs/
	cp -f ../lib/iOS/device/liblsfacewarp.a ios_libs/
	cp -f ../lib/iOS/device/libatom3d_engine.a ios_libs/
	cp -f ../lib/iOS/device/libvap_frame_resolver.a ios_libs/
	cp -f ../lib/iOS/device/libkiwi_backend.a ios_libs/
	cp -f ../lib/iOS/device/libkiwi_utils.a ios_libs/
	cp -rf ../include/shatter/libqvshatter.h ios_libs/include/shatter/
	tar -cvf ios_libs.tar ios_libs

all: clean find rename compile pack