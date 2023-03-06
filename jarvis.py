import os, datetime, pyttsx3, time, json, requests, geocoder, wikipedia, webbrowser, random
import speech_recognition as sr
import groupMe, other_funcs


if __name__ == "__main__":
    other_funcs.small_talks()
    while True:
        audio_input = other_funcs.command_prompt().lower()
        if 'location' in audio_input:
            other_funcs.get_loc()
        
        elif 'groupme' in audio_input:
            groupMe.login_to_groupMe()

        elif 'wikipedia' in audio_input:
            other_funcs.say_it("Searching Wiki")
            try:
                audio_input = audio_input.replace("wikipedia", "")
                results = wikipedia.summary(audio_input, sentences=3)
                speak(f'According to wikipedia...{results}')
            except wikipedia.exceptions.PageError: 
                other_funcs.say_it("Sorry! Couldn't find that. Can you search something else?")
        
        elif 'google' in audio_input:
            other_funcs.say_it("What should I search?")
            search_query = other_funcs.command_prompt().lower()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "youtube" in audio_input:
            webbrowser.open("https://www.youtube.com")

        
        elif "analyze" in audio_input:
            other_funcs.access_analysis()

        elif 'bye' in audio_input:
            other_funcs.say_it(f"Goodbye, have a nice one!")
            exit()
        
        elif 'thank' in audio_input:
            other_funcs.say_it("Pleasure is mine!")

        else:
            other_funcs.say_it("couldn't quite get that!")
