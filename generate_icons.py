"""生成贪吃蛇 PWA 图标 — 带蛇形图案的漂亮图标"""
import struct
import zlib
import math


def create_icon_pixels(size):
    """创建图标像素数据，返回 RGBA 字节"""
    pixels = []
    for y in range(size):
        row = []
        for x in range(size):
            u = x / max(size - 1, 1)
            v = y / max(size - 1, 1)
            row.append(get_pixel_color(u, v, size))
        pixels.append(row)
    return pixels


def get_pixel_color(u, v, size):
    """计算每个像素的颜色"""
    # 坐标转换到 -1..1
    x = u * 2 - 1
    y = v * 2 - 1
    dist = math.sqrt(x * x + y * y)

    # 圆角方形裁剪
    # 使用 superellipse 形状
    r = (abs(x) ** 4 + abs(y) ** 4) ** 0.25
    outer_r = 1.0
    inner_r = 0.92

    if r > outer_r:
        return (0, 0, 0, 0)  # 透明

    if r > inner_r:
        # 边框 — 渐变色
        t = (r - inner_r) / (outer_r - inner_r)
        rr = int(233 + (26 - 233) * t)
        gg = int(69 + (26 - 26) * t)
        bb = int(96 + (46 - 96) * t)
        return (rr, gg, bb, 255)

    # 背景
    bg_r, bg_g, bg_b = 26, 26, 46

    # 在中央区域画贪吃蛇图案
    # 缩放坐标到图标内部区域 (0.15-0.85 映射后的范围)
    sx = x / inner_r
    sy = y / inner_r

    color = draw_snake_pattern(sx, sy)
    if color:
        return color

    return (bg_r, bg_g, bg_b, 255)


def draw_snake_pattern(x, y):
    """在标准化坐标(-1..1)上绘制蛇形图案"""
    # 蛇身体的波浪线
    # 主蛇身: 从左下到右上的 S 形曲线
    t_range = 12  # 蛇身的长度分段
    snake_thickness = 0.06

    # 蛇身路径点 — 一个弯曲的蛇形
    # 使用贝塞尔曲线近似
    path = []
    for i in range(t_range + 1):
        t = i / t_range
        # S 形曲线
        px = -0.7 + t * 1.4  # 从左到右
        py = 0.35 * math.sin(t * math.pi * 2)  # S 形弯曲
        path.append((px, py))

    # 检查是否在蛇身上
    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        # 线段到点的距离
        dx = x2 - x1
        dy = y2 - y1
        length_sq = dx * dx + dy * dy
        if length_sq == 0:
            d = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        else:
            t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / length_sq))
            proj_x = x1 + t * dx
            proj_y = y1 + t * dy
            d = math.sqrt((x - proj_x) ** 2 + (y - proj_y) ** 2)

        if d < snake_thickness:
            # 根据位置渐变颜色（头绿尾浅绿）
            pos_ratio = i / (len(path) - 1)
            h = 160
            s = 80
            l = 30 + int(pos_ratio * 30)
            return hsl_to_rgb(h, s, l)

    # 蛇头（在路径末尾）
    head_x, head_y = path[-1]
    head_dist = math.sqrt((x - head_x) ** 2 + (y - head_y) ** 2)
    if head_dist < snake_thickness * 1.6:
        # 蛇头颜色 — 亮绿色
        return (0, 210, 140, 255)

    # 食物（红色圆点，在蛇头前方）
    food_x = head_x + 0.18
    food_y = head_y - 0.08
    food_dist = math.sqrt((x - food_x) ** 2 + (y - food_y) ** 2)
    if food_dist < 0.05:
        return (233, 69, 96, 255)
    elif food_dist < 0.08:
        # 食物光晕
        alpha = int(255 * (1 - (food_dist - 0.05) / 0.03))
        rr, gg, bb = 233, 69, 96
        bg_r, bg_g, bg_b = 26, 26, 46
        rr = int(rr * alpha / 255 + bg_r * (1 - alpha / 255))
        gg = int(gg * alpha / 255 + bg_g * (1 - alpha / 255))
        bb = int(bb * alpha / 255 + bg_b * (1 - alpha / 255))
        return (rr, gg, bb, 255)

    return None


def hsl_to_rgb(h, s, l):
    """HSL 转 RGB"""
    h = h % 360
    s = s / 100
    l = l / 100

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if h < 60:
        r1, g1, b1 = c, x, 0
    elif h < 120:
        r1, g1, b1 = x, c, 0
    elif h < 180:
        r1, g1, b1 = 0, c, x
    elif h < 240:
        r1, g1, b1 = 0, x, c
    elif h < 300:
        r1, g1, b1 = x, 0, c
    else:
        r1, g1, b1 = c, 0, x

    return (
        int((r1 + m) * 255),
        int((g1 + m) * 255),
        int((b1 + m) * 255),
        255,
    )


def write_png(filepath, width, height, pixels):
    """写入 PNG 文件"""
    raw_data = b""
    for row in pixels:
        raw_data += b"\x00"  # 无滤镜
        for r, g, b, a in row:
            raw_data += bytes([r, g, b, a])

    def chunk(chunk_type, data):
        c = chunk_type + data
        crc = struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
        return struct.pack(">I", len(data)) + c + crc

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b"IHDR", ihdr_data)
    compressed = zlib.compress(raw_data, 9)
    idat = chunk(b"IDAT", compressed)
    iend = chunk(b"IEND", b"")

    with open(filepath, "wb") as f:
        f.write(signature + ihdr + idat + iend)


for s in [192, 512]:
    px = create_icon_pixels(s)
    write_png(f"icons/icon-{s}.png", s, s, px)
    print(f"[OK] icons/icon-{s}.png ({s}x{s})")

print("\nIcons generated!")
