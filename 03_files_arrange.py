# -*- coding: utf-8 -*-

import os
import time
import shutil
import zipfile

# Нужно написать скрипт для упорядочивания фотографий (вообще любых файлов)
# Скрипт должен разложить файлы из одной папки по годам и месяцам в другую.
# Например, так:
#   исходная папка
#       icons/cat.jpg
#       icons/man.jpg
#       icons/new_year_01.jpg
#   результирующая папка
#       icons_by_year/2018/05/cat.jpg
#       icons_by_year/2018/05/man.jpg
#       icons_by_year/2017/12/new_year_01.jpg
#
# Входные параметры основной функции: папка для сканирования, целевая папка.
# Имена файлов в процессе работы скрипта не менять, год и месяц взять из времени создания файла.
# Обработчик файлов делать в обьектном стиле - на классах.
#
# Файлы для работы взять из архива icons.zip - раззиповать проводником в папку icons перед написанием кода.
# Имя целевой папки - icons_by_year (тогда она не попадет в коммит)
#

PATH = 'icons'
OUTPUT_FOLDER = 'icons_by_year'
FILE_NAME = 'icons.zip'


class CopyFiles:

    def __init__(self, path, output_folder):
        self.path = path
        self.output_folder = output_folder
        self.file_name = None

    def run(self):
        for dirpath, dirnames, filenames in os.walk(self.path):
            for file in filenames:
                full_file_path = os.path.join(dirpath, file)
                secs = os.path.getmtime(full_file_path)
                file_time = time.gmtime(secs)
                new_dir = self._create_new_dir(file_time)
                os.makedirs(new_dir, exist_ok=True)
                shutil.copy2(full_file_path, new_dir)

    def _create_new_dir(self, file_time):
        year = str(file_time[0])
        month = str(file_time[1])
        new_dir = os.path.join(os.path.dirname(self.path), self.output_folder, year, month)
        return new_dir


class ZipFiles(CopyFiles):

    def __init__(self, path, output_folder, file_name):
        super().__init__(path, output_folder)
        self.file_name = file_name

    def run(self):
        with zipfile.ZipFile(self.file_name, 'r') as zfile:
            # for file in zfile.namelist():
            #     if os.path.isfile(file):

            for info in zfile.infolist():
                if not info.is_dir():
                    file_name = info.filename
                    new_dir = self.create_folders(info)
                    self.write_files(file=file_name, new_dir=new_dir)

    def create_folders(self, info):
        file_time = info.date_time
        year = str(file_time[0])
        month = str(file_time[1])
        new_dir = os.path.join(year, month)
        return new_dir

    def write_files(self, file, new_dir):
        full_file_path = os.path.join(os.path.dirname(self.path), file)
        fname = os.path.basename(file) # для получения имени файла без пути к нему - os.path.basename(file)

        with zipfile.ZipFile(self.output_folder + '.zip', 'a') as newzip:
            newzip.write(full_file_path, os.path.join(new_dir, fname))


start_time = time.time()

# output = CopyFiles(path=PATH, output_folder=OUTPUT_FOLDER)
# output.run()

zipfile_create = ZipFiles(path=PATH, output_folder=OUTPUT_FOLDER, file_name=FILE_NAME)
zipfile_create.run()

print("Copy finished for {}".format(round(time.time() - start_time, 2)))
