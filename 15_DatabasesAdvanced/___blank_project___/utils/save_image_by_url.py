from typing import Any
from urllib.request import urlopen

import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from app_market.models import GoodImages


def save_image_by_url(model: GoodImages, url: str, file_name: str) -> Any:
    """
    Сохранение изображения по ссылке в базу с указанием имени
    :param model:
    :param url:
    :param file_name:
    :return:
    """
    r = requests.get(
        url,
        timeout=10
    )
    if not r.ok:
        return False
    
    img_temp = NamedTemporaryFile()
    # img_temp.write(r.content)
    img_temp.write(urlopen(url).read())
    img_temp.flush()
    
    is_save = model.image.save(file_name, File(img_temp), save=True)
    if is_save:
        return is_save
    return False
