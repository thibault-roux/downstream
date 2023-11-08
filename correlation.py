from translate import Translator





if __name__ == '__main__':

    translator = Translator(from_lang="fr", to_lang="en")
    translation = translator.translate("Bonjour, comment ça va?")  # Replace this with your French text
    print(translation)