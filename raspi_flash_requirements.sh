#!/bin/bash
#This sript will check and install all requirements related to flashing cartlinks.

#check pip installed or not
if pip --version 2>&1 > /dev/null ; then
  echo "$(pip --version) is already installed"

else
  sudo apt-get install python-pip
fi

pip install -r $BUILDKITE_BUILD_CHECKOUT_PATH/requirements.txt

#check adb tools installed or not
if adb 2>&1 > /dev/null ; then
  echo "ADB Tools are already installed"
else
  echo "ADB Tools are not installed, installing now!"
  sudo apt-get update
  sudo apt-get install -y android-tools-adb android-tools-fastboot
fi

