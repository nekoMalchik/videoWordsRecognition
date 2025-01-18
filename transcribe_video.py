import os
import time
import whisper
import json
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def get_folder_filenames(dpath="./multiplevideotest"):
    """Возвращает список файлов из папки."""
    dirty_files = os.listdir(dpath)
    return [os.path.join(dpath, f) for f in dirty_files if os.path.isfile(os.path.join(dpath, f))]

def transcribe_with_timestamps(video_path, language="ru", model_size="small"):
    """
    Распознает аудиодорожку и возвращает временные метки слов.

    :param video_path: Путь к видеофайлу.
    :param language: Язык транскрипции.
    :param model_size: Размер модели Whisper.
    :return: Расшифровка с временными метками.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Файл {video_path} не найден.")

    # Загрузка модели Whisper
    print(f"Загрузка модели Whisper ({model_size})...")
    model = whisper.load_model(model_size)

    # Расшифровка видео
    print(f"Начало транскрипции видео: {video_path}")
    result = model.transcribe(video_path, language=language, word_timestamps=True)
    print("Транскрипция завершена!")

    return result["segments"], result["text"]

def find_timestamps_with_phrases(segments, phrases):
    """
    Находит временные метки для заданной фразы.

    :param segments: Список сегментов с временными метками.
    :param phrases: Список фраз для поиска.
    :return: Словарь с временными интервалами, где встречается каждая фраза.
    """
    phrases_lower = [p.lower() for p in phrases]
    matching_intervals = {}

    for segment in segments:
        text = segment["text"].lower()
        for phrase in phrases_lower:
            if phrase in text:
                start = segment["start"]
                end = segment["end"]
                matching_intervals.setdefault(phrase, []).append({"start": format_time(start), "end": format_time(end)})

    return matching_intervals

def format_time(seconds):
    """Преобразует время в формате секунд в HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def process_video(video_path, phrases, export_folder):
    """
    Обрабатывает видео: выполняет транскрипцию, ищет фразы и сохраняет результаты.

    :param video_path: Путь к видеофайлу.
    :param phrases: Список фраз для поиска.
    :param export_folder: Папка для сохранения результатов.
    """
    print(f"Обработка файла: {video_path}")
    try:
        # Распознавание с временными метками
        segments, full_transcription = transcribe_with_timestamps(video_path)

        # Поиск временных интервалов с фразами
        intervals = find_timestamps_with_phrases(segments, phrases)

        if not intervals:
            print(f"Фразы {phrases} не найдены в {video_path}.")
            return

        # Сохранение результатов в JSON
        json_output_file = os.path.join(export_folder, os.path.splitext(os.path.basename(video_path))[0] + ".json")
        txt_output_file = os.path.join(export_folder, os.path.splitext(os.path.basename(video_path))[0] + ".txt")

        with open(json_output_file, "w", encoding="utf-8") as f:
            json.dump(intervals, f, indent=4, ensure_ascii=False)
        print(f"Временные метки сохранены в файл: {json_output_file}")

        # Сохранение полной транскрипции
        with open(txt_output_file, "w", encoding="utf-8") as f:
            f.write(full_transcription)
        print(f"Полная транскрипция сохранена в файл: {txt_output_file}")

    except Exception as e:
        print(f"Ошибка при обработке {video_path}: {e}")

# Главная логика программы
if __name__ == "__main__":
    video_folder = input("Введите путь к папке с видеофайлами: ") or "./gitignore/happy-together"
    export_folder = input("Введите папку для сохранения результатов: ") or "./gitignore/export"
    phrases = input("Введите фразы для поиска (через запятую): ") or "секс,секса,сексу,сексом,сексе,сексах"
    phrases = phrases.split(',')

    os.makedirs(export_folder, exist_ok=True)
    videos = get_folder_filenames(video_folder)

    # with ThreadPoolExecutor(max_workers=4) as executor:  # Устанавливаем 8 процессов
    #     for video_path in videos:
    #         start_time = time.time()
    #         print(f"Начало обработки файла: {video_path} в {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    #         executor.submit(process_video, video_path, phrases, export_folder)
    #         end_time = time.time()
    #         print(f"Завершение обработки файла: {video_path} в {time.strftime('%H:%M:%S', time.localtime(end_time))}")
    #         print(f"Время обработки: {end_time - start_time:.2f} секунд")

    for video_path in videos:
        start_time = time.time()
        print(f"Начало обработки файла: {video_path} в {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        
        process_video(video_path, phrases, export_folder)
        
        end_time = time.time()
        print(f"Завершение обработки файла: {video_path} в {time.strftime('%H:%M:%S', time.localtime(end_time))}")
        print(f"Время обработки: {end_time - start_time:.2f} секунд")

    print("Готово!")
