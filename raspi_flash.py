import RPi.GPIO as GPIO ## Import GPIO library
import time
import json
import hashlib
import subprocess
import sys
import pathlib
import commands
import urllib2


local_path = "/home/pi/cartlink_flash"

extract_andriod_loc = local_path + '/andriod_files'
extract_linaro_loc = local_path + '/linaro_files'
extract_link_linaro_loc = local_path + '/link_linaro_files'

andriod_loc = extract_andriod_loc + "/system_image-signed.zip"
tarloc = extract_linaro_loc + "/bootloaders.zip"
img_loc = extract_link_linaro_loc + "/linaro-vivid-alip-comark-eMMC-1p3p4.img"

andriod_file_name = 'system_image-signed.zip'
linaro_bl_name = "bootloaders.zip"
linaro_fb_name = "linaro-vivid-alip-comark-eMMC-1p3p4.img"

delete_andriod_loc = local_path + "/andriod_files"
delete_linaro_loc = local_path + "/linaro_files"
delete_link_linaro_loc = local_path + "/link_linaro"


def remove_files(file_path):
    delete_path = file_path+"/*"
    cmd = "sudo rm -rf " + delete_path
    result = commands.getoutput(cmd)
    print(result)
    print("files are deleted")


def erase_files():
    erase_logs = []
    cmd_1 = "fastboot flash partition /home/pi/cartlink_flash/linaro_files/bootloaders/gpt_both0.bin"
    cmd_2 = "sleep 10"
    erase_command = ["fastboot erase modem", "fastboot erase sbl1", "fastboot erase sbl2", "fastboot erase sbl3",
                     "fastboot erase rpm", "fastboot erase tz", "fastboot erase aboot"]
    print("Writing GPT partition...")
    result = commands.getoutput(cmd_1)
    erase_logs.append(result)
    print("GPT partition written, please wait **Don't poweroff**...")
    result_1 = commands.getoutput(cmd_2)
    erase_logs.append(result_1)
    print("erasing bootloaders...")
    for cmd in erase_command:
        result = commands.getoutput(cmd)
        print(result)
    return erase_logs


def flash_linaro_tar_image():
    linaro_logs_list = []
    linaro_logs_list.append(erase_files())
    print("flashing bootloaders...")
    cmd_1 = "fastboot flash modem /home/pi/cartlink_flash/linaro_files/bootloaders/NON-HLOS.bin"
    cmd_2 = "fastboot flash sbl1 /home/pi/cartlink_flash/linaro_files/bootloaders/sbl1.mbn"
    cmd_3 = "fastboot flash sbl2 /home/pi/cartlink_flash/linaro_files/bootloaders/sbl2.mbn"
    cmd_4 = "fastboot flash sbl3 /home/pi/cartlink_flash/linaro_files/bootloaders/sbl3.mbn"
    cmd_5 = "fastboot flash rpm /home/pi/cartlink_flash/linaro_files/bootloaders/rpm.mbn"
    cmd_6 = "fastboot flash tz /home/pi/cartlink_flash/linaro_files/bootloaders/tz.mbn"
    cmd_7 = "fastboot flash aboot /home/pi/cartlink_flash/linaro_files/bootloaders/emmc_appsboot.mbn"
    cmd_8 = "fastboot flash boot /home/pi/cartlink_flash/linaro_files/bootloaders/comark_boot.img"
    linaro_flash_image_list = [cmd_1, cmd_2, cmd_3, cmd_4, cmd_5, cmd_6, cmd_7, cmd_8]
    for cmd in linaro_flash_image_list:
        result = commands.getoutput(cmd)
        print(result)
        linaro_logs_list.append(result)
        print("{} flashing is done".format(cmd))
    return linaro_logs_list


def flash_linaro_image():
    linaro_image_file = "fastboot flash -S 700M userdata /home/pi/cartlink_flash/link_linaro_files" \
                        "/linaro-vivid-alip-comark-eMMC-1p3p4.img"
    result_linaro_image = commands.getoutput(linaro_image_file)
    print("{} flashing is done".format(linaro_image_file))
    print(result_linaro_image)
    return result_linaro_image


def flash_tablet_image_files():
    tablet_logs_list = []
    cmd_1 = "fastboot flash -w system /home/pi/cartlink_flash/andriod_files/system.img"
    cmd_2 = "fastboot flash -w recovery /home/pi/cartlink_flash/andriod_files/recovery.img"
    cmd_3 = "fastboot flash -w boot /home/pi/cartlink_flash/andriod_files/boot.img"
    cmd_4 = "fastboot flash -w userdata /home/pi/cartlink_flash/andriod_files/userdata.img"
    cmd_5 = "fastboot flash -w cache /home/pi/cartlink_flash/andriod_files/cache.img"
    cmd_6 = "fastboot reboot"
    andriod_cmd_list = [cmd_1, cmd_2, cmd_3, cmd_4, cmd_5, cmd_6]
    for cmd in andriod_cmd_list:
        result = commands.getoutput(cmd)
        tablet_logs_list.append(result)
        print(result)
        print("{} flashing is done".format(cmd))
    return tablet_logs_list


def check_file_existance(path, file_name):
    file = pathlib.Path(path)
    if file.exists():
        existed_file_md5_value = commands.getoutput("md5sum {}".format(file_name))
        print(existed_file_md5_value)
        value = (existed_file_md5_value.split(' '))[0]
        print(value)
        return value
    else:
        return None


def extract_files(url, open_loc):
    try:
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(open_loc, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print("Downloading: %s Bytes: %s" % (file_name, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8) * (len(status) + 1)
        return True
    except Exception as e:
        print("Downloading is failed due to : {}".format(e))
        return None


def extract_img_file(filename):
    return_result = extract_files(url=filename, open_loc=img_loc)
    if return_result:
        print("Image file is downloaded")
    else:
        print("Downloading is failed due to Error")


def extract_tar_files(filename):
    return_result = extract_files(url=filename, open_loc=tarloc)
    if return_result:
        print("linaro file is downloaded")
        print("extracting the file")
        tar_log_file = open('/home/pi/cartlink_flash/linaro_down_logs.txt', 'wb')
        result = commands.getoutput(
            'unzip /home/pi/cartlink_flash/linaro_files/bootloaders.zip -d /home/pi/cartlink_flash/linaro_files ')
        print(result)
        tar_log_file.write(str(result))
    else:
        print("unable to download and extract the file")


def extract_zip_file(file):
    return_result = extract_files(url=file, open_loc=andriod_loc)
    if return_result:
        print("andriod file is downloaded")
        print("extracting the file")
        zip_logs_file = open('/home/pi/cartlink_flash/android_download_logs.txt', 'w+')
        result = commands.getoutput(
            'unzip /home/pi/cartlink_flash/andriod_files/system_image-signed.zip -d /home/pi/cartlink_flash/andriod_files')
        print(result)
        zip_logs_file.write(result)
    else:
        print("unable to download and extract the file")


def open_json_file():
    with open("/home/pi/cartlink-latest.json") as json_file:
        latest_files_dict = json.load(json_file)
        return latest_files_dict


def steps_to_flash_device(component, latest_file_dict):
    tablet_s3_zip = (latest_file_dict['link_android'])
    tablet_andriod_md5 = (latest_file_dict['link_android_md5'])
    linaro_s3_tar = (latest_file_dict['link_linaro_BL'])
    linaro_s3_bl_md5 = latest_file_dict['link_linaro_BL_md5']
    linaro_fs_image = latest_file_dict['link_linaro_FS']
    linaro_fs_md5 = latest_file_dict['link_linaro_FS_md5']

    if component == 'tablet':
        tablet_log_file = open('/home/pi/cartlink_flash/andriod_flash_logs.txt', 'w+')
        result = check_file_existance(path=extract_andriod_loc, file_name=andriod_loc)
        print("tablet md5", result)
        print("existed file md5", tablet_andriod_md5)
        if result:
            if str(result) == str(tablet_andriod_md5):
                tablet_logs = flash_tablet_image_files()
                tablet_log_file.write(str(tablet_logs))
            else:
                remove_files(file_path=delete_andriod_loc)
                extract_zip_file(file=tablet_s3_zip)
                tablet_logs = flash_tablet_image_files()
                tablet_log_file.write(str(tablet_logs))
        else:
            extract_zip_file(file=tablet_s3_zip)
            tablet_logs = flash_tablet_image_files()
            tablet_log_file.write(str(tablet_logs))

    elif component == 'adl' or component == 'adr' or component == 'maint':

        result_tar = check_file_existance(path=extract_linaro_loc, file_name=tarloc)
        result_img = check_file_existance(path=extract_link_linaro_loc, file_name=img_loc)
        linaro_log_file = open("/home/pi/cartlink_flash/linaro_flash_logs.txt", 'w+')
        print("result of existed file", result_img)
        print("result of download image file",linaro_fs_md5)
        if result_tar:
            if str(result_tar) == str(linaro_s3_bl_md5):
                print("matched")
                result = flash_linaro_tar_image()
                linaro_log_file.write(str(result))
            else:
                remove_files(file_path=delete_linaro_loc)
                extract_tar_files(filename=linaro_s3_tar)
                result = flash_linaro_tar_image()
                linaro_log_file.write(str(result))
        else:
            print("file not existed", result_tar)
            extract_tar_files(filename=linaro_s3_tar)
            result = flash_linaro_tar_image()
            linaro_log_file.write(str(result))

        if result_img:
            if str(result_img) == str(linaro_fs_md5):
                result = flash_linaro_image()
                linaro_log_file.write(str(result))
            else:
                remove_files(file_path=delete_link_linaro_loc)
                extract_img_file(filename=linaro_fs_image)
                result = flash_linaro_image()
                linaro_log_file.write(str(result))
        else:
            print("file not existed", result_img)
            extract_img_file(filename=linaro_fs_image)
            result = flash_linaro_image()
            linaro_log_file.write(str(result))


def gpio_setup(unique_number):
    GPIO.setmode(GPIO.BCM)                          ## Use broadcom soc GPIO Number
    GPIO.setup(unique_number, GPIO.OUT)


def flash_raspi(sbc_name, relay_name, relay_state):
    flash_dict = {'adl': {'pwr': 21, 'fb': 20},
                  'adr': {'pwr': 16, 'fb': 12},
                  'maint': {'pwr': 23, 'fb': 18},
                  'tablet': {'pwr': 25, 'fb': 24}}

    operations = flash_dict[sbc_name]
    unique_number = operations[relay_name]
    gpio_setup(unique_number)

    if relay_name == 'pwr' and relay_state == 'off' or (relay_name == 'fb' and relay_state == 'on'):
        print("Turning {} {} {}".format(sbc_name, relay_name, relay_state))
        GPIO.output(unique_number, True)
    elif (relay_name == 'pwr' and relay_state == 'on') or (relay_name == 'fb' and relay_state == 'off'):
        print("Turning {} {} {}".format(sbc_name, relay_name, relay_state))
        GPIO.output(unique_number, False)



def check_fastboot_mode(component):
    fastboot_device = commands.getoutput("fastboot devices")
    print(fastboot_device)
    len_fastboot_devices = len(fastboot_device)
    for i in range(0, 6):
        if len_fastboot_devices > 0:
            return fastboot_device
        else:
            flash_raspi(component, 'fb', 'off')
            time.sleep(5)
            flash_raspi(component, 'pwr', 'off')
            time.sleep(5)
            flash_raspi(component, 'pwr', 'on')
            time.sleep(5)
            flash_raspi(component, 'fb', 'on')
            time.sleep(5)
            flash_raspi(component, 'pwr', 'off')
            time.sleep(5)
            flash_raspi(component, 'pwr', 'on')
	    time.sleep(5)
            fastboot_device = commands.getoutput("fastboot devices")
            len_fastboot_devices = len(fastboot_device)
    return None

def reboot_flash_device(component):
    flash_raspi(component, 'fb', 'on')
    time.sleep(5)
    flash_raspi(component, 'pwr', 'off')
    time.sleep(5)
    flash_raspi(component, 'pwr', 'on')
    time.sleep(5)
    fastboot_status = check_fastboot_mode(component)
    print(fastboot_status)
    if fastboot_status:
        latest_file_dic = open_json_file()
        steps_to_flash_device(component, latest_file_dic)
        time.sleep(5)
        flash_raspi(component, 'fb', 'off')
        time.sleep(5)
        flash_raspi(component, 'pwr', 'off')
        time.sleep(5)
        flash_raspi(component, 'pwr', 'on')
    else:
        print("system is unable to enter fastboot mode, check once")
        sys.exit()

def create_directories():
    cmd_1 = 'mkdir -p /home/pi/cartlink_flash/andriod_files'
    cmd_2 = 'mkdir -p /home/pi/cartlink_flash/linaro_files'
    cmd_3 = 'mkdir -p /home/pi/cartlink_flash/link_linaro_files'
    result = commands.getoutput(cmd_1)
    result = commands.getoutput(cmd_2)
    result = commands.getoutput(cmd_3)


def checking_process():
    cmd = "pgrep -c python"
    result = subprocess.check_output(cmd, shell=True)
    if int(result) > 1:
        print('Found Device is flashing, exiting.')
        sys.exit()
    print("Neither Device is in flashing process, process starting")


if len(sys.argv) > 1:
    for i in range(1, len(sys.argv)):
        checking_process()
        create_directories()
        reboot_flash_device(sys.argv[i])
else:
    checking_process()
    reboot_flash_device(sys.argv[1])
