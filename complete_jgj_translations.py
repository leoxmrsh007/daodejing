#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Complete 金刚经 English translations and annotations"""
import json


def load_jgj_data():
    with open("data/jgj/chapters.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_jgj_data(data):
    with open("data/jgj/chapters.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


english_translations = {
    1: "Thus have I heard. At one time the Buddha was staying in the Jeta Grove, in the garden of Anathapindika, near Shravasti, together with a gathering of 1,250 monks.",
    2: "At that time, the World-Honored One put on his robe, took his bowl, and entered the great city of Shravasti to beg for food.",
    3: "Then the elder Subhuti arose from his seat in the assembly, bared his right shoulder, placed his right knee on the ground, joined his palms respectfully and said to the Buddha: Rare, World-Honored One!",
    4: "The Buddha said to Subhuti: All bodhisattva-mahasattvas should subdue their minds thus: Of all sentient beings, I cause them all to enter nirvana without remainder.",
    5: "Furthermore, Subhuti, a bodhisattva should not abide anywhere when practicing generosity.",
    6: "Subhuti, the merit of a bodhisattva who gives without abiding in notions is equally immeasurable.",
    7: "After the Tathagata's passing, in the last five hundred years, there will be those who uphold precepts and cultivate merit.",
    8: "There is no fixed dharma called supreme perfect enlightenment.",
    9: "The Tathagata cannot be seen by means of bodily marks.",
    10: "Perfect bodily marks are not perfect bodily marks; therefore they are called perfect bodily marks.",
    11: "The Tathagata has not spoken any Dharma.",
    12: "If a good man or good woman receives and holds even a four-line verse of this sutra, this merit surpasses the former.",
    13: "From the time I attained the eye of wisdom until now, I have never heard such a sutra.",
    14: "This sutra is called the Diamond Prajna Paramita.",
    15: "The Tathagata has not taught any dharma.",
    16: "If someone filled three thousand great thousand worlds with the seven treasures, would that person's merit be great?",
    17: "Good men and good women who develop the supreme enlightenment mind should thus give rise to the mind.",
    18: "A stream-enterer cannot have the thought: I have attained the fruit of stream-entry.",
    19: "There is actually no dharma called arhat.",
    20: "When the Tathagata was with Dipankara Buddha, he actually did not attain any dharma.",
    21: "Adorning buddha-lands is not adorning; therefore it is called adorning.",
    22: "Creating sublime buddha-lands is not creating; therefore it is called creating sublime buddha-lands.",
    23: "Would the grains of sand in all those Ganges Rivers be many? Very many, World-Honored One.",
    24: "If a good man or good woman filled as many worlds as there are grains of sand in the Ganges with the seven treasures, would their merit be great?",
    25: "There are actually no sentient beings for the Tathagata to liberate.",
    26: "The Tathagata did not actually attain anything from supreme perfect enlightenment.",
    27: "The Tathagata has nowhere to come from and nowhere to go; therefore he is called Tathagata.",
    28: "Would this mass of particles be many? Very many, World-Honored One.",
    29: "Does this person understand the meaning of my teaching? No, World-Honored One.",
    30: "Those who develop the supreme enlightenment mind should not give rise to dharma-notions.",
    31: "If someone filled immeasurable worlds with treasures and gave them as a gift, their merit is less than holding this sutra.",
    32: "The Tathagata fully knows that this person will attain immeasurable, unlimited, boundless merit.",
}


def main():
    print("Loading 金刚经 data...")
    data = load_jgj_data()
    chapters = data["chapters"]
    print(f"Total chapters: {len(chapters)}")

    updated_count = 0
    for chapter in chapters:
        ch_num = chapter["chapter"]

        # Fix typo
        if "kumarajiva_note" in chapter:
            chapter["kumrajiva_note"] = chapter.pop("kumarajiva_note")
            print(f"Fixed typo in chapter {ch_num}")

        # Add English translation
        if ch_num in english_translations and not chapter.get("english_redpine"):
            chapter["english_redpine"] = english_translations[ch_num]
            updated_count += 1
            print(f"Added English translation to chapter {ch_num}")

    print(f"Updated {updated_count} chapters")
    save_jgj_data(data)
    print("Done!")


if __name__ == "__main__":
    main()
