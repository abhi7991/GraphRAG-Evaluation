import re

def getRelationship(question):
    # Create dictionaries mapping full language names and full years to their corresponding language codes and year values
    language_dict = {
        "English": "English",
        "Français": "French",
        "Español": "Spanish",
        "Deutsch": "German",
        "Pусский": "Russian",
        "Latin": "Latin",
        "Nederlands": "Dutch",
        "广州话 / 廣州話": "Cantonese",
        "普通话": "Mandarin",
        "Magyar": "Hungarian",
        "shqip": "Albanian",
        "Italiano": "Italian",
        "한국어/조선말": "Korean",
        "فارسی": "Persian",
        "Dansk": "Danish",
        "日本語": "Japanese",
        "العربية": "Arabic",
        "Hrvatski": "Croatian",
        "Bosanski": "Bosnian",
        "Română": "Romanian",
        "Bahasa indonesia": "Indonesian",
        "Bahasa melayu": "Malay",
        "svenska": "Swedish",
        "עִבְרִית": "Hebrew",
        "Český": "Czech",
        "Polski": "Polish",
        "Gaeilge": "Irish",
        "Norsk": "Norwegian",
        "Slovenčina": "Slovak",
        "Tiếng Việt": "Vietnamese",
        "Português": "Portuguese",
        "हिन्दी": "Hindi",
        "Català": "Catalan",
        "Íslenska": "Icelandic",
        "Afrikaans": "Afrikaans",
        "Srpski": "Serbian",
        "বাংলা": "Bengali",
        "Wolof": "Wolof",
        "Cymraeg": "Welsh",
        "ภาษาไทย": "Thai",
        "Latviešu": "Latvian",
        "Kiswahili": "Swahili",
        "български език": "Bulgarian",
        "ελληνικά": "Greek",
        "Türkçe": "Turkish",
        "suomi": "Finnish",
        "Esperanto": "Esperanto",
        "Український": "Ukrainian",
        "ქართული": "Georgian",
        "Bokmål": "Norwegian",
        "No Language": "No Language",
        "euskera": "Basque",
        "Azərbaycan": "Azerbaijani",
        "Malti": "Maltese",
        "اردو": "Urdu",
        "isiZulu": "Zulu",
        "Bamanankan": "Bambara",
        "پښتو": "Pashto",
        "Somali": "Somali",
        "ਪੰਜਾਬੀ": "Punjabi",
        "беларуская м": "Belarusian",
        "தமிழ்": "Tamil",
        "Galego": "Galician",
        "Kinyarwanda": "Kinyarwanda",
        "қазақ": "Kazakh",
        "Eesti": "Estonian",
        "Lietuvikai": "Lithuanian",
        "Slovenščina": "Slovenian",
        "తెలుగు": "Telugu",
        "Fulfulde": "Fulah",
        "ozbek": "Uzbek",
        "Hausa": "Hausa",
    }
    year_pattern = r'\b\d{4}\b'  # Regular expression pattern to match full years

    # Convert the question to lowercase for case-insensitive matching
    question_lower = question.lower()

    # Initialize variables to store language code and year value
    language_code = ""
    year_value = ""

    # Check if any language names are present in the question
    for lang_name, lang_code in language_dict.items():
        if lang_code.lower() in question_lower:
            language_code = lang_code
            break

    # Find all matches of the year pattern in the question
    year_matches = re.findall(year_pattern, question)
    if year_matches:
        year_value = float(year_matches[0])

    # Construct the relationship string based on the presence of language and year in the question
    relationship = ""
    if language_code and year_value:
        relationship += f" and (:SpokenLanguage{{name:'{language_code}'}})-[:LANGUAGE]->(movie) AND (:Year{{year:{year_value}}})-[:RELEASED]->(movie)"
    elif language_code:
        relationship += f" and (:SpokenLanguage{{name:'{language_code}'}})-[:LANGUAGE]->(movie)"
    elif year_value:
        relationship += f" and (:Year{{year:{year_value}}})-[:RELEASED]->(movie)"

    return relationship

    
