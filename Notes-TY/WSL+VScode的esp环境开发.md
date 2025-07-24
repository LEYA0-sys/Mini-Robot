# **WSL+VScode的esp环境开发**

https://blog.csdn.net/m0_67862631/article/details/148105239?fromshare=blogdetail&sharetype=blogdetail&sharerId=148105239&sharerefer=PC&sharesource=2302_80024781&sharefrom=from_link

https://blog.csdn.net/m0_67862631/article/details/148118009?fromshare=blogdetail&sharetype=blogdetail&sharerId=148118009&sharerefer=PC&sharesource=2302_80024781&sharefrom=from_link

具体步骤参考这两篇文章

操作完之后速度起飞，还能用**VScode图形化编译烧录**







下面这个可解决，但没啥必要，解决后一进入wsl就会进入root目录（应该是的），而不是home



![image-20250714141743608](./WSL+VScode%E7%9A%84esp%E7%8E%AF%E5%A2%83%E5%BC%80%E5%8F%91.assets/image-20250714141743608.png)

![image-20250714142413844](./WSL+VScode%E7%9A%84esp%E7%8E%AF%E5%A2%83%E5%BC%80%E5%8F%91.assets/image-20250714142413844.png)



**有这下面问题的主要原因应该是我使用了Windows的git bash**



再一次安装espIDF环境再次出现问题

```
liuli@liuli:~/esp32$ cd ~/esp32/esp-idf && ./install.sh esp32s3 
-bash: ./install.sh: Permission denied
```

1. 进入目录并赋予执行权限（如果需要）：

```bash
cd esp-idf
chmod +x install.sh
```



```
liuli@liuli:~/esp32/esp-idf$ ./install.sh esp32s3 
/usr/bin/env: ‘bash\r’: No such file or directory 
/usr/bin/env: use -[v]S to pass options in shebang lines
```


这个错误通常是由于脚本文件使用了 Windows 风格的换行符（CRLF），而 Linux 系统需要 Unix 风格的换行符（LF）导致的。可以按照以下步骤解决：

1. 首先安装`dos2unix`工具（如果尚未安装）：

```bash
sudo apt install dos2unix
```

2.转换`install.sh`文件的换行符格式：

```bash
dos2unix install.sh
```





liuli@liuli:~/esp32/esp-idf$ ./install.sh esp32s3 Detecting the Python interpreter /home/liuli/esp32/esp-idf/tools/detect_python.sh: line 9: $'\r': command not found


这个错误仍然是由于脚本文件中存在 Windows 风格的换行符（CRLF）导致的，这次是`detect_python.sh`文件出现了同样的问题。你需要对相关的脚本文件进行格式转换：

1. 先转换`detect_python.sh`文件：

```bash
dos2unix tools/detect_python.sh
```

1. 为了彻底解决问题，建议将整个项目中的所有 shell 脚本都转换为 Unix 格式：

```bash
find . -name "*.sh" -exec dos2unix {} \;
```

1. 之后再次尝试运行安装命令：

```bash
./install.sh esp32s3
```





因为使用esp-idf的工具，所以要设置环境变量，不然会提示没有idf.py的指令，也可以设置永久的环境变量，这里不建议这么去做，因为会影响到其他软件的使用，如果要设置永久，可以参考官方文档中的步骤

但解决这个问题，可以在VSCode中使用工具，在下一次文章中，我会讲

```
. $HOME/esp32/esp-idf/export.sh
```



