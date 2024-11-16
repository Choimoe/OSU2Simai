<div align="center">


# OSU2Simai

*_ OSU!maimai 谱面转换器 _*

使用 OSU2Simai，你可以轻松地将 osu!mania 谱面转换为 simai 语法 / nyageki 语法，并且可以在 [MajdataEdit](https://github.com/LingFeng-bbben/MajdataEdit) 、 [AstroDX](https://github.com/2394425147/astrodx) 、 [OngekiFumenEditor](https://github.com/NyagekiFumenProject/OngekiFumenEditor) 等软件上使用！

</div>

## 功能

1. 将 osu!mania 谱面提取出谱面信息、曲绘、音乐。

2. 将以时间戳为记录的谱面信息转化为以小节与音符记录的谱面，可实现不规则音的 96 分音近似。

   将 osu 谱面中的 timing 规整到 bpm 的调整与小节的调整。

3. 将以 osu 谱面格式的谱面信息转换为 [nyageki 格式](https://github.com/NyagekiFumenProject/OngekiFumenEditor) 音符记录的谱面。

## 使用

目前只支持命令行使用。下载 [最新发行版](https://github.com/Choimoe/OSU2Simai/releases/latest)，开箱即用：

在命令行输入（可能会在同目录下创建 `config.json`）：

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

若启用 `config.json` 中 `ONGEKI` 为 `true`，则会输出 NYAGEKI 谱面文件：

```
F:\OSU2SIMAI
| osu2simai.exe
| 889405 Sakuzyo - Fracture Ray.osz
└─889405 Sakuzyo - Fracture Ray
  | BG.jpg
  | out.nyageki
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

目前提供的参数（`config.json`）有：

- `KEYS`：定义 OSU!mania 谱面在 Simai 下的按键配置。
  - `[]` 表示没有配置。
  - `[5, 4]` 表示对于 2K 谱面，分别映射到 5 号键和 4 号键。
  - `[8, 7, 6, 5, 4, 3, 2, 1]` 表示对于 8K 谱面，从 8 号键映射一圈到 1 号键。

- `TEMP_DIR`：临时文件夹的路径，用于存储解压 `.osz` 的临时文件，默认路径为 `./tmp`。

- `AUTHOR`：作者信息，默认作者为 `OSU2Simai`。

- `LEVEL`：难度信息，默认难度信息为 `15`。

- `RANDOM`：开启随机安排键位，默认为 `0`，目前可选的值为 `0` 或 `2` 或 `4`。

- `SAME`：布尔值，表示是否允许超过双押，默认 `false` 表示不允许。

- `ONGEKI`：布尔值，启用或禁用 ONGEKI 模式。默认 `false` 表示禁用。

- `ONGEKI_KEYS`：在 ONGEKI 模式下，定义了按键的水平位置。默认为 `-16, -10, -4, 4, 10, 16`（会同步修改轨道线）。

## 搭建

直接 `clone` 本项目后直接可以运行 `osu2simai.py`。

核心代码在 `parser.py` 中 `OsuFileParser.convert_simai_header()` 方法中，实现较为复杂，后续会进行优化与改良。

--------------------

感谢观看，开发不易，希望能够点个 star~

欢迎提issue与pr！