import os
import whisper
import ffmpeg

def get_floder_filenames(dpath="./multiplevideotest"):
    dirtyFiles = os.listdir(dpath)
    return [dpath + "/" + f for f in dirtyFiles if os.path.isfile(os.path.join(dpath, f))]

def transcribe_video(video_path, language="ru", model_size="small"):
    """
    Транскрибирует видеофайл в текст.

    :param video_path: Путь к видеофайлу.
    :param language: Язык транскрипции (например, "ru" для русского).
    :param model_size: Размер модели Whisper (tiny, base, small, medium, large).
    :return: Расшифрованный текст.
    """
    # Проверка существования файла
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Файл {video_path} не найден.")

    # Извлечение аудиодорожки
    audio_path = "audio_temp.wav"
    try:
        print("Извлечение аудио из видео...")
        ffmpeg.input(video_path).output(audio_path, ac=1, ar=16000).run(quiet=True, overwrite_output=True)

        # Загрузка модели Whisper
        print(f"Загрузка модели Whisper ({model_size})...")
        model = whisper.load_model(model_size)

        # Расшифровка аудио
        print("Начало транскрипции...")
        result = model.transcribe(audio_path, language=language)

        # Удаление временного аудиофайла
        os.remove(audio_path)

        print("Транскрипция завершена!")
        return result["text"]

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        raise

# Пример использования
if __name__ == "__main__":
    # video_path = input("Введите путь к папке с видеофайлами: ")
    video_path = './multiplevideotest'
    language = input("Введите язык (например, 'ru' для русского): ") or "ru"
    folder_prefix = input("Введите папку экспорта: ") or "multiplevideotestexport"
    if folder_prefix:
        folder_prefix = "./" + folder_prefix + "/"
        os.makedirs(folder_prefix, exist_ok=True)

    for k, video in enumerate(get_floder_filenames(video_path)):
        try:
            transcription = transcribe_video(video, language=language)
            print("\nТранскрибированный текст:\n")
            print(transcription)
            
            exportFilename = folder_prefix + "transcription.txt" + str(k)
            # Сохранение текста в файл
            with open(exportFilename, "w", encoding="utf-8") as f:
                f.write(transcription)
            f.close
            print("\nТранскрипция сохранена в файл: " + exportFilename)
        except Exception as e:
            print(f"Ошибка: {e}")

    fnames = get_floder_filenames(folder_prefix)
    with open(folder_prefix + "result.txt", "w", encoding="utf-8") as f:
        for file in fnames:
            with open(file, "r", encoding="utf-8") as infile:
                f.write(infile.read())
                f.write("\n")

    print("done")
        