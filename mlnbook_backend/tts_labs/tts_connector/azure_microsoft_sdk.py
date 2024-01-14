import os
import azure.cognitiveservices.speech as speechsdk


def tts_generator(req_txt, req_type='txt'):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'),
                                           region=os.environ.get('SPEECH_REGION'))
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_language = "en-US"
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    if req_type == 'txt':
        # result = speech_synthesizer.speak_text_async("I'm excited to try text to speech").get()
        speech_synthesis_result = speech_synthesizer.speak_text_async(req_txt).get()
    else:
        # ssml_string = open("ssml.xml", "r").read()
        speech_synthesis_result = speech_synthesizer.speak_ssml_async(req_txt).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(req_txt))
        stream = speechsdk.AudioDataStream(speech_synthesis_result)
        stream.save_to_wav_file("path/to/write/file.wav")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
