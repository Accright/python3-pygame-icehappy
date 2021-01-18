[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/tterb/atomic-design-ui/blob/master/LICENSEs)
[![Python Version](https://img.shields.io/github/pipenv/locked/python-version/metabolize/rq-dashboard-on-heroku)

## 项目名称
项目命名为：pyIceHappy 

一款利用Python3和Pygame开发的桌面端消消乐游戏，本项目使用分文件的构建方式，自主设计和编写了消除、交换、判断是否为可消除图等算法，并自行担任UI设计，实现了开心消消乐的选择关卡、金币、步数、消除、随机分配消除块等基本功能。

A desktop-side elimination game developed using Python3 and Pygame. This project uses a file-based construction method to independently design and write algorithms for elimination, exchange, and judgment whether it is an eliminateable graph, and take the role of UI design. The basic functions such as the selection of levels, gold coins, number of steps, elimination, random allocation of elimination blocks, etc. of Happy Match.

## 项目介绍

开心消消乐 是一款大家都十分熟知的游戏了。主要就是通过加载不同的小动物，然后玩家交换小动物的位置，和其他消除游戏机制类似，如果有三个或以上的小动物处于一个直线或T字形的位置，将会发生消除，并加载新的小动物。消除一定小动物的数量或达到一定的其他目标（例如冰块）则算作通关。

本项目利用Python3和Pygame开发的一款桌面端消消乐游戏，本项目使用分文件的构建方式，自主设计和编写了消除、交换、判断是否为可消除图等算法，并自行担任UI设计，通过搜集网络资源和自行设计，模拟并实现了开心消消乐的选择关卡、金币、步数、消除、随机分配消除块等基本功能，并做到高度还原手机端的效果。

### 文件分布

文件稍微有些杂乱，开发完之后一直没有整理。文件分布比较简单，main.py作为项目的入口，负责包的导入及鼠标键盘事件的监听，同时负责全局bgm的播放和关卡选择界面的绘制。manage.py作为所有逻辑的实现，其中类和函数的简单实现关系如下：

| 函数名/类名   | 简要介绍                    |
| ----- | --------------------          |
| SoundPlay    | 声音播放类，其中引用了Sound文件夹下的各种bgm           |
| Tree   | 关卡选择的树类，其中规定了关卡的果子出现的位置|
| ManagerTree  | 管理树类 ，用于树的绘制、文本加载、鼠标监听等 |
| Element| 元素类，元素类是小动物，冰块，选择光标等的合集，用于创建各类对象同时声明了move方法|
| Board | 剩余步数和下一关等的提示板，在关卡进行中或完成时弹出 |
| Manager | 该类是逻辑处理的主要类，包括坐标转换，元素重置，关卡绘制等多个函数，鼠标监听和交换后的判断逻辑也在此类中实现，具体实现方式可以阅读代码并参考注释 |

## 运行

安装Python3环境之后，安装Pyganme插件，直接运行main.py即可。

## 项目优点

1. 大量的原版配乐和图片素材 ；
2. 引入Pygame模块；
3. 分文件构建，使用数组展示小动物，替换鼠标 ；
4. 设计基础的交换消除和判断是否为有尽图算法；
5. 完善和高度还原的声音播放和图片加载；
6. 完善的关卡选择和积分及体力值系统 ； 

## 可能的问题

1. bug:有些有尽图可能无法做出判断 ；
2. 小动物的排列是完全随机的，关卡难度无法衡量；
3. 在部分高分辨率电脑上性能可能有点低 ；

## 注意

最近发现好多人拿这个项目去积分下载或做教程，本着开放的原则，不反对代码共享，但是请注明来源，遵循 [MIT](http://www.opensource.org/licenses/mit-license.php)协议。

## 项目截图：

![关卡选择](https://springboot-blog-1256194683.cos.ap-beijing.myqcloud.com/pic/py-1.jpg)

![游戏中](https://springboot-blog-1256194683.cos.ap-beijing.myqcloud.com/pic/py-2.jpg)
