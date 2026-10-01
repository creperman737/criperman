import subprocess
import tempfile
from pathlib import Path


LANGUAGES = {
	"uz": "O'zbekcha",
	"en": "English",
	"ru": "Русский",
}


def load_dependencies():
	try:
		import speech_recognition as speech
		from deep_translator import GoogleTranslator
		from gtts import gTTS
	except ImportError as error:
		missing = error.name or "kerakli paket"
		print(f"Xatolik: {missing} topilmadi.")
		print("O'rnatish: python3 -m pip install -r requirements.txt")
		raise SystemExit(1)
	return speech, GoogleTranslator, gTTS


def choose_language():
	print("\nChiqish tilini tanlang:")
	for code, name in LANGUAGES.items():
		print(f"  {code} - {name}")

	while True:
		selected = input("Til kodi (q): ").strip().lower()
		if selected == "q":
			raise SystemExit(0)
		if selected in LANGUAGES:
			return selected
		print("Noto'g'ri til kodi.")


def recognize_speech(speech):
	recognizer = speech.Recognizer()
	with speech.Microphone() as microphone:
		print("Mikrofon sozlanmoqda...")
		recognizer.adjust_for_ambient_noise(microphone, duration=0.8)
		print("Gapiring...")
		audio = recognizer.listen(microphone, timeout=10, phrase_time_limit=30)

	try:
		text = recognizer.recognize_google(audio, language="uz-UZ")
	except speech.UnknownValueError:
		print("Ovoz tushunilmadi. Yana urinib ko'ring.")
		return ""
	except speech.RequestError as error:
		print(f"Nutqni tanish xatosi: {error}")
		return ""

	print(f"Siz aytdingiz: {text}")
	return text


def translate_text(text, target_language, translator_class):
	if target_language == "uz":
		return text
	return translator_class(source="uz", target=target_language).translate(text)


def speak(text, language, gtts_class):
	audio_file = Path(tempfile.gettempdir()) / "uzbek_tts_output.mp3"
	gtts_class(text=text, lang=language, slow=False).save(str(audio_file))

	try:
		subprocess.run(
			["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", str(audio_file)],
			check=True,
		)
	finally:
		audio_file.unlink(missing_ok=True)


def main():
	speech, translator_class, gtts_class = load_dependencies()
	print("O'zbekcha nutq tarjimoni. Chiqish uchun til tanlashda q ni bosing.")

	while True:
		target_language = choose_language()
		try:
			text = recognize_speech(speech)
		except speech.WaitTimeoutError:
			print("Ovoz kutilgan vaqtda kelmadi.")
			continue
		except OSError as error:
			print(f"Mikrofon xatosi: {error}")
			print("Linuxda mikrofon uchun PyAudio/PortAudio o'rnatilganini tekshiring.")
			return

		if not text:
			continue

		try:
			translated = translate_text(text, target_language, translator_class)
			print(f"{LANGUAGES[target_language]}: {translated}")
			speak(translated, target_language, gtts_class)
		except Exception as error:
			print(f"Tarjima yoki ovoz chiqarish xatosi: {error}")


if __name__ == "__main__":
	main()
