import os
import ffmpeg

# Папка, где хранятся обрезанные видео
output_base_dir = "./gitignore/final-videos"  # Папка с нарезанными видео

# Папка, куда будет сохранено итоговое склеенное видео
final_output_dir = "./gitignore/final-videos-merged"  # Папка для итогового склеенного видео

# Функция для склеивания видео
def merge_videos(output_base_dir, final_output_dir):
    # Создаем папку для итогового видео, если она не существует
    os.makedirs(final_output_dir, exist_ok=True)

    # Список для хранения путей к видеофайлам
    video_files = []

    # Проходим по всем папкам в output_base_dir
    for folder in os.listdir(output_base_dir):
        folder_path = os.path.join(output_base_dir, folder)
        if os.path.isdir(folder_path):
            # Собираем все .avi файлы в текущей папке
            for file in os.listdir(folder_path):
                if file.endswith(".avi"):
                    video_files.append(os.path.join(folder_path, file))

    # Если найдено хотя бы одно видео, начинаем процесс склеивания
    if video_files:
        # Создаем временный текстовый файл для списка видео
        with open("file_list.txt", "w", encoding="utf-8") as file_list:
            for video_file in video_files:
                file_list.write(f"file '{video_file}'\n")

        # Путь к итоговому файлу
        output_file = os.path.join(final_output_dir, "merged_video.avi")

        # Склеиваем видео без перекодирования
        try:
            ffmpeg.input('file_list.txt', format='concat', safe=0).output(output_file, vcodec="copy", acodec="copy").run()
            print(f"Видео успешно склеено и сохранено как: {output_file}")
        except ffmpeg.Error as e:
            print(f"Ошибка при склеивании видео: {e}")

        # Удаляем временный файл списка
        os.remove("file_list.txt")
    else:
        print("Нет видео для склеивания!")

# Запуск склеивания видео
merge_videos(output_base_dir, final_output_dir)
