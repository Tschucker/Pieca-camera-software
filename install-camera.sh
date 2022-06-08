# This script will install the camera, dng support, and any required prerequisites.
cd ~
echo -e ''
echo -e '\033[32mCamera [Installation Script] \033[0m'
echo -e '\033[32m-------------------------------------------------------------------------- \033[0m'
echo -e ''
echo -e '\033[93mUpdating package repositories... \033[0m'
sudo apt update

echo ''
echo -e '\033[93mInstalling prerequisites... \033[0m'
sudo apt install -y git python3 python3-pip python3-picamera python-tk libatlas-base-dev
sudo pip3 install keyboard PiDNG --force


echo ''
echo -e '\033[93mInstalling Camera... \033[0m'
cd ~
sudo rm -Rf ~/Pieca-camera-software
sudo git clone https://github.com/Tschucker/Pieca-camera-software
sudo chown -R $USER:$USER Pieca-camera-software
cd Pieca-camera-software
sudo chmod +x camera.py

echo ''
echo -e '\033[93mDownloading color profiles... \033[0m'
cd ~
sudo rm -Rf ~/Pieca-camera-software/profiles
mkdir ~/Pieca-camera-software/profiles
sudo chown -R $USER:$USER ~/Pieca-camera-software/profiles
wget -q https://github.com/davidplowman/Colour_Profiles/raw/master/imx477/PyDNG_profile.dcp -O ~/Pieca-camera-software/profiles/basic.dcp
wget -q https://github.com/davidplowman/Colour_Profiles/raw/master/imx477/Raspberry%20Pi%20High%20Quality%20Camera%20Lumariver%202860k-5960k%20Neutral%20Look.dcp -O ~/Pieca-camera-software/profiles/neutral.dcp
wget -q https://github.com/davidplowman/Colour_Profiles/raw/master/imx477/Raspberry%20Pi%20High%20Quality%20Camera%20Lumariver%202860k-5960k%20Skin%2BSky%20Look.dcp -O ~/Pieca-camera-software/profiles/skin-and-sky.dcp

cd ~
echo ''
echo -e '\033[93mSetting up alias... \033[0m'
sudo touch ~/.bash_aliases
sudo sed -i '/\b\(function camera\)\b/d' ~/.bash_aliases
sudo sed -i '$ a function camera { sudo python3 ~/Pieca-camera-software/camera.py "$@"; }' ~/.bash_aliases
echo -e 'You may use \e[1mcamera <options>\e[0m to launch the program.'

echo ''
echo -e '\033[32m-------------------------------------------------------------------------- \033[0m'
echo -e '\033[32mInstallation completed. \033[0m'
echo ''
sudo rm ~/install-camera.sh
bash
