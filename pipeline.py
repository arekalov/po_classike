from PIL import Image


def parse_tif(filePath):  # Разделение многостраничного .tiff на одностраничные .tif (Подготовка данных на задание №5)
    img = Image.open(filePath)
    img.load()
    pathes = []
    n_f = img.n_frames
    for i in range(n_f):
        img.seek(i)
        path = 'C:\\Users\Student\\PycharmProjects\\izh_it\\pipeline_photos\\Block_%s.tif' % (i,)
        pathes.append(path)
        img.save(path)
    return pathes


