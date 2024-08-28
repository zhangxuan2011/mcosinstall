"""

=====Translation Licence=====
Translate By zhangxuan, Based on Chinese Edition.
This translation may have some wrongs, please forgive that
and report it to "zx20110412@outlook.com"
Thank you!
=====mcosinstall.py usage=====
To show main menu.Start with this
=====Publish addr=====
https://github.com/zhangxuan2011/mcosinstall/tree/international
"""

from os import system as execcmd
from askstep import askstep
from time import sleep


def main_menu(guide_url=None):
    execcmd("clear")
    print("Welcome to install MinecraftOS!\n"
          f"If you wanna insttall inecraftOS currectly ,Please read the installation method of {guide_url}\n"
          f"Otherwise if you lost all of the data of the disk,!!!!!!!\n"
          f"The user name of MinecraftOS: Minecraft\n"
          f"Password:123456(The same as root)\n\n"
          f"Main Menu: \n\t"
          f"1.Part disk\n\t"
          f"2.Format disk\n\t"
          f"3.Setup the install path and install OS \n\t"
          f"4.set mount \n\t"
          f"5.install bootloader\n\t"
          f"6.Reboot\n\t"
          f"7.Poweroff\n\t")

def main():
    main_menu()
    choice = input('Enter your choice (1-7): ')
    if choice == "1":
        askstep("partdisk")
        main()
    elif choice == "2":
        askstep("format")
        main()
    elif choice == "3":
        askstep("setroot")
        main()
    elif choice == "4":
        askstep("setmount")
        main()
    elif choice == "5":
        askstep("grubinstall")
        main()
    elif choice == "6":
        askstep("reboot")
    elif choice == "7":
        askstep("poweroff")
    else:
        print("错误:无效的选项!!!!!!")
        sleep(3)
        execcmd("clear")
        main()
if __name__ == '__main__':
    main()