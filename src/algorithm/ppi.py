import math

RESOLUTION_4K_WIDTH = 3840
RESOLUTION_4K_HEIGHT = 2160
RESOLUTION_1080P_WIDTH = 1920
RESOLUTION_1080P_HEIGHT = 1080
RESOLUTION_SP6_WIDTH = 2736
RESOLUTION_SP6_HEIGHT = 1824

SCREEN_SIZE_SP6 = 12.3
SCREEN_SIZE_24 = 24
SCREEN_SIZE_27 = 27


def calculate_ppi(width_pixel_count, height_pixel_count, screen_size):
    """
    计算屏幕PPI

    :param width_pixel_count: 横向像素点数
    :param height_pixel_count: 纵向像素点数
    :param screen_size: 屏幕尺寸
    :return: PPI
    """
    return round(math.sqrt(width_pixel_count ** 2 + height_pixel_count ** 2) / screen_size, 1)


# surface pro 6的分辨率为2736 * 1824，屏幕尺寸12.3，PPI为267
print('SP6 = %s' % calculate_ppi(RESOLUTION_SP6_WIDTH, RESOLUTION_SP6_HEIGHT, SCREEN_SIZE_SP6))
# 4k 24寸
print('4k_24寸 = %s' % calculate_ppi(RESOLUTION_4K_WIDTH, RESOLUTION_4K_HEIGHT, SCREEN_SIZE_24))
# 4k 27寸
print('4k_27寸 = %s' % calculate_ppi(RESOLUTION_4K_WIDTH, RESOLUTION_4K_HEIGHT, SCREEN_SIZE_27))
# 经典1080p 24寸
print('1080p_24寸 = %s' % calculate_ppi(RESOLUTION_1080P_WIDTH, RESOLUTION_1080P_HEIGHT, SCREEN_SIZE_24))
