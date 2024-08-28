"""

=====Translation Licence=====
Translate By zhangxuan, Based on Chinese Edition.
This translation may have some wrongs, please forgive that
and report it to "zx20110412@outlook.com"
Thank you!
=====Askstep.py usage=====
to do some options of installation.The main of mcosinstall.
=====Publish addr=====
https://github.com/zhangxuan2011/mcosinstall/tree/international
"""

from os import system as execcmd
from time import sleep
from os import path
import os


def fileexist(filename):
    try:
        f = open(filename, mode="r")
    except:
        return False
    else:
        f.close()
        return True
def askstep(step):
    """

    :param step:
    :return:None，Return to main menu
    """
    if step == "partdisk":
        execcmd("clear")
        execcmd("lsblk -f")
        partdisk = input("Which disk do you wanna part(Disk name example:sda,nvme0n1p)(Return if leave blank): ")
        if partdisk == None or partdisk == "":
            execcmd("clear")
            return
        if not fileexist(f"/dev/{partdisk}"):
            print("Error:Invaild disk!!!!!")
            sleep(3)
            execcmd("clear")
            askstep("partdisk")
        execcmd(f"cfdisk /dev/{partdisk}")
        execcmd("clear")
        return
    elif step == "format":
        execcmd("clear")
        execcmd("fdisk -l")
        parformatdev = input("Enter the partition you wanna format(example:sda1)(return if leave blank): ")
        if parformatdev == None or parformatdev == "":
            return
        if not fileexist(f"/dev/{parformatdev}"):
            print("Error:Invaild partition!!!!!")
            askstep("format")
        print("These partition you can choose to format:\n\t"
              "1. ext4(For Main Partition) \n\t"
              "2. FAT32(For EFI Partitions) \n")
        parformat = input("Please choose(1,2)(Leave blank to return): ")
        if parformat == None or parformat == "":
            return
        if parformat == "1":
            execcmd(f"mkfs.ext4 /dev/{parformatdev}")
            print("Command execute successfully!")
            sleep(3)
            execcmd("clear")
            askstep("format")
        elif parformat == "2":
            execcmd(f"mkfs.vfat /dev/{parformatdev}")
            print("Command execute Successfully")
            sleep(3)
            execcmd("clear")
            askstep("format")
        else:
            print("Invaild Value !!!!!(Enter 1 or 2) ")
            sleep(3)
            askstep("format")

    elif step == "setroot":
        execcmd("clear")
        execcmd("lsblk -f")
        global rootdev  # 这里global是为了方便,防止root分区被再次挂载
        rootdev = input("Enter partition where you wanna install MinecraftOS(Example:sda1)(Enter blank to return): ")
        if rootdev == None or rootdev == "":
            return
        if not fileexist(f"/dev/{rootdev}"):
            print("Invaild partition!!!!!!")
            sleep(3)
            askstep("setroot")
        temp = input(f"This will wipe all of the data of {rootdev}!!!!!\nAre you sure????(Enter Y to comfirm,return if enter the others): ")
        if not temp == "Y" or temp == "y":
            return
        # 这里开始安装
        os.chdir("/")
        execcmd(f"e2label /dev/{rootdev} MinecraftOS")  # change label
        execcmd(f"mount /dev/{rootdev} /squashfs-root") # Mount main part.(注意:根目录要创建squashfs-root目录)
        execcmd("rm -rf /squashfs-root/*")
        execcmd(f"unsquashfs /usr/share/rootfs/rootfs.sfs")
        execcmd("genfstab -U /squashfs-root > /squashfs-root/etc/fstab")
        print("Command execute Successfully")
        sleep(3)
        return

    elif step == "setmount":
        execcmd("clear")
        execcmd("lsblk -f")
        mountdisk = input("Enter partition u wanna mount(Example:sda1)(Leave blank to return): ")
        if mountdisk == None or mountdisk == "":
            return
        if mountdisk == rootdev:
            print("Error:This partition is root partition and it CAN'T be mount again!!!!!")
            sleep(3)
            askstep("setmount")
        mountpoint = input("These are the path u can mount the partition:\n\t"
                           "1./boot/efi(For efi partition)\n\t"
                           "2.custom(自定义)(No open cause of our Technology)\n"
                           "Enter choice, leave blank to return: ")
        if mountpoint == None or mountpoint == "":
            return
        if mountpoint == "1":
            execcmd(f"mount /dev/{mountdisk} /squashfs-root/boot/efi")
            print("Command execute Successfully!!!!")
            sleep(3)
            askstep("setmount")
        elif mountpoint == "2":
            # 这里技术原因暂不开放
            print("Error:This option is not open")
            sleep(3)
            askstep("setmount")
        else:
            print("Error:Invaild choice!!!!!")
            sleep(3)
            askstep("setmount")
    elif step == "grubinstall":
        execcmd("clear")
        # 检查启动方式
        if path.exists("/sys/firmware/efi/efivars"):
            bootmode = "efi"
            with open("/sys/firmware/efi/fw_platform_size", mode="r") as f:
                efisize = f.read()
            instdev = None
        else:
            bootmode = "legacy"
            efisize = None
            execcmd("lsblk -f")
            instdev = input("Install bootloader to which disk (such as:sda): ")
            if not fileexist(f"/dev/{instdev}"):
                print("Error:Disk Not exists!!!!!!")
                sleep(3)
                askstep("grubinstall")
        os.chdir("/usr/share/mcosinstall")
        execcmd("chmod 755 ./runchroot/main")
        execcmd("cp -r runchroot /squashfs-root")
        with open("/squashfs-root/runchroot/info.py", mode="w+") as f2:
            f2.write("class info:"
                     f"\n\tbootmode = \"{bootmode}\""
                     f"\n\tinstdev = \"{instdev}\""
                     f"\n\tefisize = {efisize}")
        execcmd("arch-chroot /squashfs-root /runchroot/main > mcosinstall.log")
        print("Command Execute successfully!!!")
        sleep(3)
        return

    elif step == "reboot":
        execcmd("clear")
        print("Reboot in 3s......")
        sleep(3)
        execcmd("reboot")

    elif step == "poweroff":
        execcmd("clear")
        print("Power off in 3s......")
        sleep(3)
        execcmd("poweroff")

# EOF
