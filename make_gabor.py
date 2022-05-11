import numpy as np
from PIL import Image
import argparse
from matplotlib import colors


def deg2rad(deg):
    return (deg * np.pi) / 180


def save_gabor_patch_image(frequency, orientation, envelope, size, phase, bg_color, c1, c2, std=None):
    """
    Saves a gabor patch .PNG file with the given properties
    :param frequency: The frequency of the Gabor patch
    :param orientation: The orientation of the Gabor patch in degrees
    :param envelope: The envelope of the Gabor patch. Must be one of the following:
           * gaussian
           * linear
           * sine
           * circular
           * rectangular
    :param size: The size in pixels of the image
    :param phase: The phase of the Gabor patch
    :param bg_color: The background color of the image
    :param c1: The first color of the Gabor patch
    :param c2: The second color of the Gabor patch
    :param std: The STD of the gaussian envelope. Only relevant if envelope=="gaussian"
    :return:
    """
    amp, f = generate_gabor_patch(envelope, frequency, orientation, phase, size, std)
    c1 = np.array(colors.to_rgb(c1))
    c2 = np.array(colors.to_rgb(c2))
    bg_color = np.array(colors.to_rgb(bg_color))
    im_rgb_vals = (c1 * amp[:, :, None]) + (c2 * (1 - amp[:, :, None]))
    im_rgb_vals = (im_rgb_vals * f[:, :, None]) + (bg_color * (1 - f[:, :, None]))
    im = Image.fromarray((im_rgb_vals * 255).astype('uint8'), 'RGB')
    im.save(f"gabor_o{orientation:g}_env{envelope}_freq{frequency}.png")


def generate_gabor_patch(envelope, frequency, orientation, phase, size, std):
    im_range = np.arange(size)
    x, y = np.meshgrid(im_range, im_range)
    dx = x - size // 2
    dy = y - size // 2
    t = np.arctan2(dy, dx) - deg2rad(orientation)
    r = np.sqrt(dx ** 2 + dy ** 2)
    x = r * np.cos(t)
    y = r * np.sin(t)
    # The amplitude without envelope (from 0 to 1)
    amp = 0.5 + 0.5 * np.cos(2 * np.pi * (x * frequency + phase))
    if envelope == "gaussian":
        f = np.exp(-0.5 * (std / size) * ((x ** 2) + (y ** 2)))
    elif envelope == "linear":
        f = np.max(0, (size // 2 - r) / (size // 2))
    elif envelope == "sine":
        f = np.cos((np.pi * (r + size // 2)) / (size - 1) - np.pi / 2)
        f[r > size // 2] = 0
    elif envelope == "circle":
        f = np.ones_like(r)
        f[r > size // 2] = 0
    else:
        raise ValueError("Envelope type is incorrect!")
    return amp, f


def parse_args():
    parser = argparse.ArgumentParser(description='Process Gabor patch parameters')
    parser.add_argument('--frequency', '-f', type=float, help='The frequency of the Gabor patch', required=True)
    parser.add_argument('--orientation', '-o', metavar='N', nargs='+', type=float,
                        help='The orientation of the Gabor patch (in degrees)\nIf list, generates all orientations.\n'
                             'If you wish to generate X patches with uniform orientations between orientation o1 and orientation o2, enter o1 and o2 and specify --num_orientations=X',
                        required=True)
    parser.add_argument('--envelope', '-e', type=str,
                        help='The envelope of the Gabor patch. Must be one of the following:\n'
                             '\t* gaussian\t* linear\t* sine\t* circular\t* rectangular', default='sine')
    parser.add_argument('--size', '-s', type=int, help='The size of the Gabor patch image (in pixels)',
                        default=500)
    parser.add_argument('--phase', '-p', type=float, help='The phase of the Gabor patch', default=0)
    parser.add_argument('--background_color', '-bg', type=str, help='The background color of the Gabor patch',
                        default="gray")
    parser.add_argument('--color1', '-c1', type=str, help='The first color of the Gabor patch', default="black")
    parser.add_argument('--color2', '-c2', type=str, help='The second color of the Gabor patch', default="white")
    parser.add_argument('--std', type=float, help='The standard deviation of the Gabor patch image (in pixels)',
                        default=20)
    parser.add_argument('--num_orientations', type=int,
                        help='The number of orientations to create between the first and second orientations provided (inclusive)',
                        required=False, default=0)
    args = parser.parse_args()
    return list(vars(args).values())


if __name__ == '__main__':
    frequency, orientations, envelope, size, phase, bg_color, c1, c2, std, num_orientations = parse_args()
    if len(orientations) == 2 and num_orientations > 2:
        orientations = np.linspace(orientations[0], orientations[1], num_orientations)
    for orientation in orientations:
        save_gabor_patch_image(frequency, orientation, envelope, size, phase, bg_color, c1, c2, std)
