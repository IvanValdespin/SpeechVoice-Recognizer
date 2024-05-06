# Speech Recognition Micro-Service

## Requirements

### Whisper

Whisper is the primary component of this micro-service, and it can be found at [https://github.com/openai/whisper](https://github.com/openai/whisper).

**Installation Note:** It is not necessary to install setuptools-rust.

By default, the "medium" model is used. If you wish to change it, you can do so by modifying line 5 in the MainConfig.json file. Keep in mind that changing the model may affect efficiency and speed.

It's also possible to use a GPU if your system allows it. To enable GPU support, change line 6 to "cuda" in the MainConfig.json file and comment out lines 42 and 58 to 62 in the MainConfig.py file. If you are using a GPU, there's no need to install OpenVino.

### spaCy

spaCy is another required component, and you can find it at [https://spacy.io/usage](https://spacy.io/usage).

Either "en_core_web_md" or "en_core_web_lg" is needed to run the micro-service. These models are available at [https://spacy.io/models/en](https://spacy.io/models/en).

By default, "en_core_web_lg" is used. If you want to change the model, you can do so by modifying line 17 in the MainConfig.json file.

### OpenVino Toolkit

The OpenVino Toolkit is available at [https://pypi.org/project/openvino/](https://pypi.org/project/openvino/).

**Note:** OpenVino is only available if you are using an Intel OS or an Intel device, such as the Neural Stick 2.

To install the following libraries, you can use `pip3 install`:

- numpy
- pydub
- Flask
- SQLAlchemy

## Running the Micro-Service

To run the micro-service, ensure you are in the same location as EnglishApp.py and execute the following command:

```bash
flask --app EnglishApp.py run --host=0.0.0.0

## Using OIC Audio Files

If you are using the micro-service to obtain OIC audio files, please delete the "OIC" folder before sending requests to `/Audio`.

Once all audio files have been saved, you can retrieve the audio translations from the "TextFiles" folder by sending a GET request to `/OIC`.
