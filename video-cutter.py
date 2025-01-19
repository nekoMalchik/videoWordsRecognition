from datetime import datetime, timedelta
import os
import json
import ffmpeg

# Папки с данными
export_dir = "./gitignore/result-folder"
video_dir = "./gitignore/result-folder"
output_base_dir = "./gitignore/final-videos"

# Функция для корректировки времени
def adjust_time(time_str, offset):
    time = datetime.strptime(time_str, "%H:%M:%S") + timedelta(seconds=offset)
    return max(time, datetime.strptime("00:00:00", "%H:%M:%S")).strftime("%H:%M:%S")

# Функция для обрезки видео
def cut_video(input_file, timestamps, output_dir):
    for word, intervals in timestamps.items():
        if word != "секс":
            continue
        for i, interval in enumerate(intervals):
            start = adjust_time(interval["start"], -2)  # Вычесть 2 секунды
            end = adjust_time(interval["end"], 2)      # Добавить 2 секунды
            output_file = os.path.join(output_dir, f"{word}-{i+1}-cuted.avi")
            try:
                ffmpeg.input(input_file, ss=start, to=end).output(output_file, vcodec="copy", acodec="copy").run()
                print(f"Видео обрезано и сохранено: {output_file}")
            except ffmpeg.Error as e:
                print(f"Ошибка при обрезке видео {output_file}: {e}")

# Основная логика обработки файлов
def process_files(export_dir, video_dir, output_base_dir):
    for filename in os.listdir(export_dir):
        if not filename.endswith(".json"):
            continue
        base_name = os.path.splitext(filename)[0]
        json_path = os.path.join(export_dir, filename)
        video_file = os.path.join(video_dir, f"{base_name}.avi")

        if not os.path.exists(video_file):
            print(f"Видео файл не найден: {video_file}")
            continue

        with open(json_path, 'r', encoding='utf-8') as f:
            timestamps = json.load(f)

        output_dir = os.path.join(output_base_dir, f"{base_name}-cuted")
        os.makedirs(output_dir, exist_ok=True)
        cut_video(video_file, timestamps, output_dir)

# Запуск обработки
process_files(export_dir, video_dir, output_base_dir)
