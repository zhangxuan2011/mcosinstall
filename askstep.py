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
    :return:None，返回菜单
    """
    if step == "partdisk":
        execcmd("clear")
        execcmd("lsblk -f")
        partdisk = input("请问你要给哪个硬盘分区(磁盘名称示例:sda,nvme0n1p)(留空则返回上一级): ")
        if partdisk == None or partdisk == "":
            execcmd("clear")
            return
        if not fileexist(f"/dev/{partdisk}"):
            print("错误:无效的磁盘!!!!!")
            sleep(3)
            execcmd("clear")
            askstep("partdisk")
        execcmd(f"cfdisk /dev/{partdisk}")
        execcmd("clear")
        return
    elif step == "format":
        execcmd("clear")
        execcmd("fdisk -l")
        parformatdev = input("输入你要格式化的分区(例如:sda1)(留空则返回上一级): ")
        if parformatdev == None or parformatdev == "":
            return
        if not fileexist(f"/dev/{parformatdev}"):
            print("错误:无效的分区!!!!!")
            askstep("format")
        print("这些是你要格式化的文件系统:\n\t"
              "1. ext4(主分区用的) \n\t"
              "2. FAT32(EFI分区用的) \n")
        parformat = input("请选择(1,2)(留空返回菜单): ")
        if parformat == None or parformat == "":
            return
        if parformat == "1":
            execcmd(f"mkfs.ext4 /dev/{parformatdev}")
            print("命令执行完成!")
            sleep(3)
            execcmd("clear")
            askstep("format")
        elif parformat == "2":
            execcmd(f"mkfs.vfat /dev/{parformatdev}")
            print("命令执行完成!")
            sleep(3)
            execcmd("clear")
            askstep("format")
        else:
            print("输入的值有误!!!!!(输入1或者2) ")
            sleep(3)
            askstep("format")

    elif step == "setroot":
        execcmd("clear")
        execcmd("lsblk -f")
        global rootdev  # 这里global是为了方便,防止root分区被再次挂载
        rootdev = input("输入你要把系统安装到哪个分区(例如:sda1)(留空则返回菜单): ")
        if rootdev == None or rootdev == "":
            return
        if not fileexist(f"/dev/{rootdev}"):
            print("无效的分区!!!!!!")
            sleep(3)
            askstep("setroot")
        temp = input(f"这会把{rootdev}分区上的所有东西全部清除!!!!!\n你确定吗(输入Y为确定,不区分大小写,输入其他的则返回菜单): ")
        if not temp == "Y" or temp == "y":
            return
        # 这里开始安装
        os.chdir("/")
        execcmd(f"e2label /dev/{rootdev} MinecraftOS")  # 改标签
        execcmd(f"mount /dev/{rootdev} /squashfs-root") # 挂载主分区(注意:根目录要创建squashfs-root目录)
        execcmd("rm -rf /squashfs-root/*")
        execcmd(f"unsquashfs /usr/share/rootfs/rootfs.sfs")
        execcmd("genfstab -U /squashfs-root > /squashfs-root/etc/fstab")
        print("命令执行完成!")
        sleep(3)
        return

    elif step == "setmount":
        execcmd("clear")
        execcmd("lsblk -f")
        mountdisk = input("输入你要挂载的分区(例如:sda1)(留空则返回菜单): ")
        if mountdisk == None or mountdisk == "":
            return
        if mountdisk == rootdev:
            print("错误:这是你设置的root分区,不可再次被挂载!!!!!")
            sleep(3)
            askstep("setmount")
        mountpoint = input("这是你可以挂载分区的路径:\n\t"
                           "1./boot/efi(efi分区用)\n\t"
                           "2.custom(自定义)(由于技术原因暂不开放)\n"
                           "请输入选择,留空则返回菜单: ")
        if mountpoint == None or mountpoint == "":
            return
        if mountpoint == "1":
            execcmd(f"mount /dev/{mountdisk} /squashfs-root/boot/efi")
            print("命令执行完成!!!!!")
            sleep(3)
            askstep("setmount")
        elif mountpoint == "2":
            # 这里技术原因暂不开放
            print("错误:此选项暂不开放")
            sleep(3)
            askstep("setmount")
        else:
            print("错误:无效选项!!!!!")
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
            instdev = input("请问要将引导安装到哪个磁盘(如:sda): ")
            if not fileexist(f"/dev/{instdev}"):
                print("错误:磁盘不存在!!!!!!")
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
        print("命令执行完毕!!!")
        sleep(3)
        return

    elif step == "reboot":
        execcmd("clear")
        print("3秒后重启......")
        sleep(3)
        execcmd("reboot")

    elif step == "poweroff":
        execcmd("clear")
        print("3秒后关机......")
        sleep(3)
        execcmd("poweroff")

# EOF