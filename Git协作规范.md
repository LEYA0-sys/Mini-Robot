# 本项目git协作教程和要求

## git基本学习资料

1. 比较简单的，直接使用向：
   1. [Git基本使用教程（一）：入门及第一次基本完整操作_git的使用-CSDN博客](https://blog.csdn.net/qq_35206244/article/details/97698815)
   2. [Git基本使用教程（二）：获取更新与推送更新_git 查看库是否更新-CSDN博客](https://blog.csdn.net/qq_35206244/article/details/97772285)
2. 介绍原理，但是结构不是很清晰：
   1. [史上最全 Git 图文教程（非常详细）零基础入门到精通，收藏这一篇就够了-CSDN博客](https://blog.csdn.net/Javachichi/article/details/140660754)

假设你已经配置好了github的ssh密钥，加入到了本仓库。

## git协作流程案例

**克隆该仓库**

只有第一次开发，本地还没有仓库才需要这个步骤

```sh
git clone xxxx
```

**同步最新代码**

如果本地已经有了仓库，在创建自己的开发分支之前，需要确保同步了最新的代码

```sh
git checkout main					# 切换到main分支
git pull origin main				# 拉取最新的代码
```

**创建一个自己的分支**

分支名的命名无所谓，不要太离谱就好，比如叫develop，feat/sensor都行，这里以feat/sensor为例

```sh
git checkout -b feat/sensor
```

**在这个分支上提交自己的代码**

比如我在完善自己README.md的内容，你们可以创建一个自己名字的文件，随便写点内容，写完自己的代码之后，然后运行下面的命令，git commit的时候用中文描述自己的提交内容即可，注意引号是英文半角的引号哦

```sh
# 编辑代码后，依次执行
git add .
git commit -m "完成了在本地git协作的操作文档文档"
```

**将自己的分支推送到远程**

```sh
git push origin feat/sensor
```

![image-20250416014014480](./Git%E5%8D%8F%E4%BD%9C%E8%A7%84%E8%8C%83.assets/git.png)

---

接下来的操作需要在github仓库的网页完成

进入仓库主页，点分支按键，可以看到自己新建的分支和最新修改的代码
![image-20250416014310706](./Git%E5%8D%8F%E4%BD%9C%E8%A7%84%E8%8C%83.assets/web.png)

**发起 Pull Request / 合并请求**

在实际开发场景下，假设你的这个分支已经完成了某一个特性的开发，接下来可以先把这部分的代码合并到main分支上。进入Pull requests标签页，点击Compare & pull request，接下来确定是自己要合并的分支没有错，简单的写一下标题和本次合并的介绍就行了。确定无误之后点击Create pull request即可。之后的步骤将会交给仓库负责人审核，审核通过后由负责人合并到main主线上。分支被合并之后将会被删除，下一次开发时重复从**同步最新代码**开始即可。

![image-20250416015051792](./Git%E5%8D%8F%E4%BD%9C%E8%A7%84%E8%8C%83.assets/PR.png)

云端的分支在被合并之后可能会被删除（看管理者的操作），但是本地的不会，使用下面命令可以删除指定分支，将下面的分支名改成自己的即可

```sh
git checkout main          # 切换到主分支
git branch -d feat/sensor  # 删除本地分支
git remote prune origin    # 更新分支信息
git branch -a              # 查看远端分支信息
```
