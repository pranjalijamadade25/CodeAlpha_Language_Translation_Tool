
import streamlit as st
import argostranslate.translate

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.title("🌍 AI Language Translation Tool")
st.write("Translate text using locally installed AI language models.")
st.caption("Offline translation — no online translation API required.")

st.divider()

# Find installed languages and translation models
languages = argostranslate.translate.get_installed_languages()

language_names = {
    lang.code: lang.name for lang in languages
}

available_pairs = []

for lang in languages:
    for translation in lang.translations_from:
        available_pairs.append(
            (lang.code, translation.to_lang.code)
        )

# Stop safely if no model is installed
if not available_pairs:
    st.error(
        "No translation model is installed yet. "
        "Install a language model before translating."
    )
    st.code(
        'python -c "import argostranslate.translate as t; '
        'print([(l.code, [x.to_lang.code for x in l.translations]) '
        'for l in t.get_installed_languages()])"',
        language="bat"
    )
    st.stop()

# Source language selection
source_codes = sorted(set(source for source, target in available_pairs))

source_labels = {
    f"{language_names.get(code, code)} ({code})": code
    for code in source_codes
}

source_label = st.selectbox(
    "Translate from",
    list(source_labels.keys())
)
source_code = source_labels[source_label]

# Target languages supported by selected source
target_codes = sorted({
    target
    for source, target in available_pairs
    if source == source_code
})

if not target_codes:
    st.warning("No target language is available for this source.")
    st.stop()

target_labels = {
    f"{language_names.get(code, code)} ({code})": code
    for code in target_codes
}

target_label_list = list(target_labels.keys())

preferred_target = "hi" if source_code == "en" else target_codes[0]

default_index = next(
    (
        i for i, label in enumerate(target_label_list)
        if target_labels[label] == preferred_target
    ),
    0
)

target_label = st.selectbox(
    "Translate to",
    target_label_list,
    index=default_index
)
target_code = target_labels[target_label]

# Text input
text_input = st.text_area(
    "Enter your text",
    placeholder="Example: Hello, how are you?",
    height=150,
    max_chars=5000
)

if st.button("🌐 Translate Text", type="primary"):
    if not text_input.strip():
        st.warning("Please enter some text first.")
    else:
        try:
            with st.spinner("Translating with the local model..."):
                result = argostranslate.translate.translate(
                    text_input.strip(),
                    source_code,
                    target_code
                )

            if result:
                st.success("Translation completed!")
                st.text_area(
                    "Translated text",
                    value=result,
                    height=150
                )
                st.download_button(
                    "Download translation",
                    data=result,
                    file_name="translated_text.txt",
                    mime="text/plain"
                )
            else:
                st.warning("The model returned an empty translation.")

        except Exception as error:
            st.error("Local translation failed.")
            st.write("Technical details:", str(error))
            st.info(
                "Check that the selected language model is installed "
                "and that the source and target languages are supported."
            )

st.divider()
st.caption("CodeAlpha AI Internship | Project 1")