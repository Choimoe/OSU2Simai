<div align="center">


# OSU2Simai

*_ OSU!maimai 谱面转换器 _*

使用 OSU2Simai，你可以轻松地将 osu!mania 谱面转换为 simai 语法，并且可以在 [MajdataEdit](https://github.com/LingFeng-bbben/MajdataEdit) 或 [AstroDX](https://github.com/2394425147/astrodx) 等软件上使用！

</div>

## 功能

1. 将 osu!mania 谱面提取出谱面信息、曲绘、音乐。

2. 将以时间戳为记录的谱面信息转化为以小节与音符记录的谱面，可实现不规则音的 96 分音近似。

   将 osu 谱面中的 timing 规整到 bpm 的调整与小节的调整。

## 使用

目前只支持命令行使用。下载 [最新发行版](https://github.com/Choimoe/OSU2Simai/releases/latest)，开箱即用：

在命令行输入：

```cmd
osu2simai.exe osu_map.osz
```

选择需要的难度，执行完毕后会在 `osu2simai.exe` 同目录下生成与参数同名的文件夹，内容至少包含：`track.mp3`（或 `.ogg` 等）、`maidata.txt`。

下面以谱面 [889405 Sakuzyo - Fracture Ray](https://osu.ppy.sh/beatmapsets/889405#mania/1858949) 作为使用例：

```
F:\osu2simai>osu2simai.exe "889405 Sakuzyo - Fracture Ray.osz"
Found the following .osu files:
1: Sakuzyo - Fracture Ray (Kuo Kyoka) [CS' Forbidden Memories].osu
2: Sakuzyo - Fracture Ray (Kuo Kyoka) [CS' Present].osu
3: Sakuzyo - Fracture Ray (Kuo Kyoka) [Future].osu
4: Sakuzyo - Fracture Ray (Kuo Kyoka) [Past].osu
Select the .osu file to process (by number): 2
```

输入选项 `2`，会建立文件夹：

```
F:\OSU2SIMAI
| osu2simai.exe
| 889405 Sakuzyo - Fracture Ray.osz
└─889405 Sakuzyo - Fracture Ray
  | BG.jpg
  | maidata.txt
  └─track.mp3
```

`maidata.txt` 部分内容为：（其中 `&des` 与 `&lv_5` 写在了 `config.py`，可以自行修改）

```
&title=Fracture Ray
&artist=削除
&first=1.235
&des=OSU2Simai
&wholebpm=200
&lv_5=15
&inote_5=
(200)
{8},8,6,,2,4,,3,
{8},4,6,4,,7,5,7,
{8},2,4,,8,6,,7,
{8},8h[8:7],,6h[8:5],,4h[8:3],,,
{1}5h[2:1]/2,
```

使用 `MajDataEdit` 打开：

[![pkTvMM6.png](https://s21.ax1x.com/2024/07/21/pkTvMM6.png)](https://imgse.com/i/pkTvMM6)

## 参数设置

目前提供的参数（`config.py`）有：

```python
KEYS = [                      # 键位设置
    [],
    [],
    [5, 4],                   # 2K
    [],
    [6, 5, 4, 3],             # 4K
    [],
    [7, 6, 5, 4, 3, 2],       # 6K
    [8, 7, 6, 5, 4, 3, 2],    # 7K
    [8, 7, 6, 5, 4, 3, 2, 1]  # 8K
]
TEMP_DIR = './tmp'            # 临时文件目录
AUTHOR = 'OSU2Simai'          # 默认作者
LEVEL = 15                    # 默认等级
```

使用 `PyInstaller` 的时候也打包进去了，后续会进行优化（

## 搭建

直接 `clone` 本项目后直接可以运行 `osu2simai.py`。

核心代码在 `parser.py` 中 `OsuFileParser.convert_simai_header()` 方法中，实现较为复杂，后续会进行优化与改良。

--------------------

感谢观看，开发不易，希望能够点个 star~

欢迎提issue与pr！