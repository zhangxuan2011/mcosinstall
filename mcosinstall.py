from os import system as execcmd
from askstep import askstep
from time import sleep


def main_menu(guide_url=None):
    print("欢迎安装MinecraftOS!\n"
          f"如果您要正确地安装MinecraftOS,请阅读{guide_url}上的安装方式安装\n"
          f"否则,如果造成硬盘数据丢失，我们概不负责!!!!!!!\n\n"
          f"主菜单: \n\t"
          f"1.分区\n\t"
          f"2.格式化\n\t"
          f"3.设置安装位置并安装系统\n\t"
          f"4.设置挂载\n\t"
          f"5.安装引导\n\t"
          f"6.重启\n\t"
          f"7.关机\n\t")

def main():
    main_menu()
    choice = input('输入你的选择(1-6): ')
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