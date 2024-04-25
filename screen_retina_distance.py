import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


ax_magnification_ratio = 1.05
ax_w_margin_ratio = 0.8
ax_h_margin_ratio = 0.2
ax_border_ratio = 0.01
margin = 0.2


def meters_2_inches(meters):
    return meters * 39.3701


def inches_2_meters(inches):
    return inches * 0.0254


# Draw Screen
def draw_axs_1(axs1, screen_width_meters, screen_height_meters, screen_size_inches):
    # 绘制屏幕长宽的矩形
    rect = patches.Rectangle((0, 0),
                             screen_width_meters, screen_height_meters,
                             fill=False, color='black', edgecolor='red', linewidth=2)
    axs1.add_patch(rect)

    # 绘制屏幕尺寸
    axs1.text(0.1, 0.1,
              "{screen_size_inches}″".format(screen_size_inches=screen_size_inches),
              fontname='Courier New', fontsize=14, weight='bold', ha='left', va='bottom')

    # 水平中线
    axs1.plot([0, screen_width_meters],
              [screen_height_meters / 2, screen_height_meters / 2],
              'r-', linewidth=2)

    # 垂直中线
    axs1.plot([screen_width_meters / 2, screen_width_meters / 2],
              [0, screen_height_meters],
              'b-', linewidth=2)

    # 注解长宽参数
    axs1.text(screen_width_meters / 2, screen_height_meters + margin,
              "{screen_width_meters:.2f}m".format(screen_width_meters=screen_width_meters),
              fontname='Courier New', weight='bold', ha='center', va='center',
              bbox=dict(boxstyle="round,pad=0.3", fc="lightgrey", ec='none'))

    axs1.text(screen_width_meters + margin, screen_height_meters / 2,
              "{screen_height_meters:.2f}m".format(screen_height_meters=screen_height_meters),
              fontname='Courier New', weight='bold', ha='left', va='center',
              bbox=dict(boxstyle="round,pad=0.3", fc="lightgrey", ec='none'))


# Draw vertical view
def draw_axs_2(axs2, screen_width_meters, screen_height_meters, distance_eye_screen, vertical_view_angle):
    # 垂直中线
    axs2.plot([0, 0],
              [screen_height_meters, 0],
              'b-', linewidth=2)

    # Draw d line
    axs2.plot([0, distance_eye_screen],
              [screen_height_meters / 2, screen_height_meters / 2],
              linestyle='-', color='green', linewidth=2)

    # Draw eye line
    axs2.plot([0, distance_eye_screen, 0],
              [0, screen_height_meters / 2, screen_height_meters],
              linestyle='-', color='gray', linewidth=2)

    # 标记 d
    axs2.text(distance_eye_screen / 2 - margin, screen_height_meters / 2,
              f'd = {distance_eye_screen:.2f}m'.format(distance_eye_screen=distance_eye_screen),
              fontname='Courier New', weight='bold', ha='center', va='center',
              bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", ec='none'))


def draw_axs_3(axs3, screen_width_meters, screen_height_meters, distance_eye_screen, horizontal_view_angle):
    # 水平中线
    axs3.plot([0, screen_width_meters],
              [distance_eye_screen, distance_eye_screen],
              'r-', linewidth=2)

    # Draw d line
    axs3.plot([screen_width_meters / 2, screen_width_meters / 2],
              [distance_eye_screen, 0],
              linestyle='-', color='green', linewidth=2)

    # Draw eye line
    axs3.plot([0, screen_width_meters / 2, screen_width_meters],
              [distance_eye_screen, 0, distance_eye_screen],
              linestyle='-', color='gray', linewidth=2)

    # 标记 d
    axs3.text(screen_width_meters / 2 + margin, distance_eye_screen / 2,
              f'd = {distance_eye_screen:.2f}m'.format(distance_eye_screen=distance_eye_screen),
              fontname='Courier New', weight='bold', ha='left', va='center',
              bbox=dict(boxstyle="round,pad=0.3", fc="lightgreen", ec='none'))


def draw_axs_4(axs4, screen_size_inches, distance_eye_screen, horizontal_view_angle, vertical_view_angle,
               screen_ppi, min_retina_d, min_retina_ppi, equivalent_ppi):
    thx_distance = inches_2_meters(meters_2_inches(distance_eye_screen) * 0.825)
    screen_size_meters = inches_2_meters(screen_size_inches)

    # 注释文本
    texts = [
        f'Screen PPI: {screen_ppi:.1f}',
        f'α_h: {horizontal_view_angle:.2f}°',
        f'α_v: {vertical_view_angle:.2f}°',
        '------------: ------------',
        f'THX Suggest d: {thx_distance:.2f}m',
        f'SMPTE Suggest d: {1.2 * screen_size_meters:.2f}m~{1.6 * screen_size_meters:.2f}m',
        f'Screen Min Retina d: {min_retina_d:.2f}m',
        f'Current d Min Retina PPI: {min_retina_ppi:.1f}',
        f'Equivalent 12″ PPI: {equivalent_ppi:.1f}',
        '------------: ------------',
        'iPhone4 12″ Retina PPI: 326',
    ]

    max_prefix_length = max(len(text.split(":")[0]) for text in texts)  # 计算最长的文本前缀

    # 对齐所有文本行，使冒号对齐
    aligned_texts = [text.split(":")[0].rjust(max_prefix_length) + ":" + text.split(":")[1] for text in texts]

    multi_line_text = "\n".join(aligned_texts)

    # 标注
    axs4.text(0, 0, multi_line_text, fontname='Courier New', va='bottom')


def visualize_screen_eye(screen_width_res, screen_height_res, screen_size_inches, distance_eye_screen):
    # 计算屏幕横向分辨率PPI
    screen_diagonal_res = math.sqrt(screen_width_res ** 2 + screen_height_res ** 2)
    screen_ppi = screen_diagonal_res / screen_size_inches

    # 计算屏幕宽度
    screen_aspect_ratio = screen_width_res / screen_height_res
    screen_width_inches = screen_size_inches / math.sqrt(1 + 1 / (screen_aspect_ratio ** 2))

    # 计算屏幕长宽 in meters
    screen_width_meters = inches_2_meters(screen_width_inches)
    screen_height_meters = screen_width_meters / screen_aspect_ratio

    # 达到 Retina 显示效果的最小 PPI 定为 326，计算达到 Retina 标准的最小观看距离
    retina_ppi = 326  # iPhone4 的 PPI 作为参考
    theta = 1 / 60 * (math.pi / 180)  # 弧度

    min_retina_d = 0.0254 / (retina_ppi * math.tan(theta / 2))

    # 计算能达到视网膜效果的最小 PPI
    min_retina_ppi = 0.0254 / (2 * distance_eye_screen * math.tan(theta / 2))

    # 等效 12 英寸距离 PPI
    equivalent_ppi = screen_ppi * (distance_eye_screen / inches_2_meters(12))

    ax_width = ax_magnification_ratio * max(distance_eye_screen, screen_width_meters)
    ax_height = ax_magnification_ratio * max(distance_eye_screen, screen_height_meters)

    # 计算水平&垂直视角
    horizontal_view_angle = math.degrees(2 * math.atan((screen_width_meters / 2) / distance_eye_screen))
    vertical_view_angle = math.degrees(2 * math.atan((screen_height_meters / 2) / distance_eye_screen))

    # 创建一个 2x2 的子图
    fig, axs = plt.subplots(nrows=2, ncols=2)

    axs1 = axs[0, 0]  # 左上子图（第一象限）
    axs2 = axs[0, 1]  # 右上子图（第二象限）
    axs3 = axs[1, 0]  # 左下子图（第三象限）
    axs4 = axs[1, 1]  # 右下子图（第四象限）

    draw_axs_1(axs1, screen_width_meters, screen_height_meters, screen_size_inches)
    draw_axs_2(axs2, screen_width_meters, screen_height_meters, distance_eye_screen, vertical_view_angle)
    draw_axs_3(axs3, screen_width_meters, screen_height_meters, distance_eye_screen, horizontal_view_angle)
    draw_axs_4(axs4, screen_size_inches, distance_eye_screen, horizontal_view_angle, vertical_view_angle,
               screen_ppi, min_retina_d, min_retina_ppi, equivalent_ppi)

    for ax_row in axs:
        for ax in ax_row:
            ax.axis('off')  # 去除坐标轴
            ax.set_aspect('equal', 'box')  # 保持长宽比
            ax.set_xlim([-ax_border_ratio * ax_width, ax_width])  # 保持缩放
            ax.set_ylim([-ax_border_ratio * ax_height, ax_height])

    # 调整子图之间的最小间隙
    plt.subplots_adjust(wspace=ax_width * ax_w_margin_ratio, hspace=ax_height * ax_h_margin_ratio)

    # 自动调整子图间的空隙
    plt.tight_layout()

    # 显示图表
    plt.show()


if __name__ == '__main__':
    visualize_screen_eye(screen_width_res=3840, screen_height_res=2160, screen_size_inches=85, distance_eye_screen=2.5)
