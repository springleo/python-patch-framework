#!/bin/bash

# Prepare a patch binary using makeself
#
# Arguments:
#          1: BUILD_FILE_NAME: the filename.bin that needs to be created, currently using "branch_name.bin"
#          2: 
#
BASE_DIR=$(dirname $(readlink -f $0))
TARGET_DIR=$BASE_DIR/target
TARGET_SRC=$TARGET_DIR/source
BUILD_FILE_NAME="$1"
MAKESELF_CMD=/root/ws/installer/install/binaryInstaller/makeself-master/makeself.sh
PWD=`pwd`
usage() {
  echo
  echo $0 "clean | bin_name"
  echo
  echo "eg: ./build.sh clean"
  echo "    ./build.sh patch_name.bin"
  echo
  exit 0
}

if [[ $# -eq 0 ]] ; then
   usage
fi

if [[ $1 = "clean" ]] ; then
   if [[ -d $TARGET_DIR ]] ; then
      echo "$TARGET_DIR found, deleting it ..." && rm -rf $TARGET_DIR
      exit $? 
   else
      echo "$TARGET_DIR not found, workspace already clean !"
      exit 0
   fi
fi

mkdir -p $TARGET_DIR/source

cd $TARGET_DIR

# Copy all required files to TARGET_DIR

cp -r $BASE_DIR/jars $TARGET_SRC
cp -r $BASE_DIR/misc $TARGET_SRC
cp -r $BASE_DIR/scripts $TARGET_SRC
cp -r $BASE_DIR/wars $TARGET_SRC
cp $BASE_DIR/*.py $TARGET_SRC
cp $BASE_DIR/README.txt $TARGET_SRC

find $TARGET_SRC -name ".gitkeep" -exec rm -f {} \;

$MAKESELF_CMD --sha256 --nomd5 --nocrc $TARGET_SRC $BUILD_FILE_NAME "AADS apostrophe patch Version 1.0" ./patch-class.py

if [[ -f $BUILD_FILE_NAME ]]; then
   sha256sum $BUILD_FILE_NAME > $BUILD_FILE_NAME.sha256sum.txt
fi

cd $PWD
