#Written by Chris Keeler, on June 5th, 2015
#Converts ASCII text into Pokespeech through the use of their names.
#The number of utterable segments in their name defines in which base the ASCII value will be represented.
#The value at each index of the new-based integer will determine which segment is used.

#The resulting pokespeech will delimit the original ASCII characters and words

import os
import wave

class Pokemon():
	def __init__(self,_name,_utterances):
		self.name = _name
		self.utterances = _utterances
		self.sounds = dict()
	
	def loadSounds(self):
		for u in self.utterances:
			self.sounds[u] = SOUND_FILE_DIR+self.name+"\\"+u+".wav"

#Acquire the name of a Pokemon from the user, split into each utterable segment
#Return Value:
#	pokeName: A string, representing the name of a pokemon to use for the Pokespeech
#
def getPokemonName():
	print "Please enter the Pokemon's name, with each utterable section separated by spaces. (e.g. 'Pi ka chu')"
	pokeName = raw_input()
	return pokeName

#Defines the set of sounds usable for Pokespeech
#Arguments:
#	pokeName: A string, separating a pokemon's name sounds with spaces
#Return Value:
#	A list of sounds usable for Pokespeech
#
def changePokemon(pokeName):
	return pokeName.split()

#Changes a number from decimal to a different base
#Method retrieved from http://www.purplemath.com/modules/numbbase.htm
#Arguments:
#	convertable: A decimal integer, to be converted into an integer in desiredBase
#	desiredBase: A base into which we convert the previously supplied decimal integer
#Return Value:
#	baseXString: A string representing the number in a different base
#
def decimalToX(convertable,desiredBase):
	currentPosition = 0
	remainders = ""
	
	#The purple math method does not work so well for base 1.
	if desiredBase == 1:
		return "0"*convertable
	else:
		#Convert the decimal integer into the new base
		while convertable > 0:
			remainders += str(convertable%desiredBase)
			convertable = convertable / desiredBase
			
		#Since the remainders are found from smallest to largest, we reverse the string
		remainders = remainders[::-1]
		
		#Left-pad the new number with zeroes to the desired size of ascii, for ease of readability
		return remainders.zfill(ASCII_SIZE)

#Converts ASCII text into poke-speech.
#Arguments:
#	pokemon: A Pokemon object, to use in the speech conversion
#	inputText: A string, to be converted into Pokespeech
#Return value:
#	outputText: The same input string, represented in Pokespeech
#
def stringToPokeSpeech(pokemon,inputText):
	#The base we'll be using when converting the ASCII digits
	base = len(pokemon.utterances)
	outputText = ""
	for c in range(len(inputText)):
		tempText = ""
		#Convert char to decimal
		charIntVal = ord(inputText[c])
		
		#Convert decimal to some other base (in line with the number of sounds our current Pokemon can make)
		newBaseVal = decimalToX(charIntVal,base)
		
		#Convert each number in the new base to a pokemon sound
		if inputText[c] == ' ':
			#TODO: Change most recent CHAR_DELIMITER to a WORD_DELIMITER as is needed
			tempText+=WORD_DELIMITER+' '
		else:
			for i in range(len(newBaseVal)):
				tempText += pokemon.utterances[int(newBaseVal[i])]+' '
			tempText+=CHAR_DELIMITER+' '
		print inputText[c]+" was converted into '"+tempText+"'"
		outputText+=tempText
	
	return outputText

#Converts a file containing ASCII text into poke-speech (.txt format)
#Arguments:
#	pokemon: A Pokemon object, to use in the speech conversion
#	inFilePath: A string, to be used as the source of the ASCII text
#Return Value:
#	TODO
#
def asciiFileToPokeSpeech(pokemon,inFilePath):
	with open(inFilePath) as f:
		inputText = f.read()
	
	#Convert the ascii text into poke speech
	pokeSpeech = stringToPokeSpeech(pokemon,inputText)
	
	#Split the file name so that we know where to save the new file
	origFileName, origFileExtension = os.path.splitext(inFilePath)
	
	#Create the new file name
	pokeFilePath = origFileName+"_poke"+origFileExtension
	
	#Save the poke speech .txt file
	with open(pokeFilePath,'w') as f:
		f.write(pokeSpeech)

#Converts a file containing ASCII text into poke-speech (.wav format)
#Arguments:
#	pokemon: A Pokemon object, to use in the speech conversion
#	inFilePath: A string, to be used as the source of the ASCII text
#Return Value:
#	TODO
#
def asciiFileToPokeWav(pokemon,inFilePath):
	with open(inFilePath) as f:
		inputText = f.read()
	
	#Convert the ascii text into poke speech
	pokeSpeech = stringToPokeSpeech(pokemon,inputText)
	
	#Split the file name so that we know where to save the new file
	origFileName, origFileExtension = os.path.splitext(inFilePath)
	
	#Create the new file name
	pokeFilePath = origFileName+"_poke.wav"
	
	#Save the poke speech .wav file
	soundFileInputs = []
	for utterance in pokeSpeech.split():
		if utterance == CHAR_DELIMITER:
			soundFileInputs.append(CHAR_DELIMITER_FILE)
		elif utterance == WORD_DELIMITER:
			soundFileInputs.append(WORD_DELIMITER_FILE)
		else:
			soundFileInputs.append(pokemon.sounds[utterance])
	
	newAudioData = ""
	for s in soundFileInputs:
		#Open the .wav file and get header data
		currFile = wave.open(s,'r')
		fileParams = currFile.getparams()
		numChannels = currFile.getnchannels()
		numFrames = currFile.getnframes()
		#sampleWidth = currFile.getsampwidth()
		#sampleFrequency = currFile.getframerate()
		#compressionType = currFile.g
		
		#Read from the .wav file
		dataString = currFile.readframes(numFrames*numChannels)
		newAudioData += dataString
		
		currFile.close()
		
	#Open the file and set header data
	pokeWav = wave.open(pokeFilePath,'w')
	#pokeWav.setnchannels(numChannels)
	#pokeWav.setnframes(numFrames)
	#pokeWav.setsampwidth(sampleWidth)
	#pokeWav.setParams(numChannels,sampleWidth,sampleFrequency,numFrames,
	
	pokeWav.setparams(fileParams)
	
	#Write to the new .wav file
	pokeWav.writeframesraw(newAudioData)
	

#Collect an unknown pokemon name from a user, and turn their text input into pokespeech
def main():
	while True:
		tempName = getPokemonName()
		
		print "If you are you satisfied with: '"+tempName+"', then enter 'y'."
		confirm = raw_input().lower()
		
		if confirm == "y":
			pokeSounds = changePokemon(tempName)
			break
	
	print "Type some ASCII to get the Poke-speech equivalent of your text."
	print "Type 'exit' to leave."
	
	while True:
		convertable = raw_input()
		if convertable.lower() == "exit":
			break
		else:
			print stringToPokeSpeech(pokeSounds,convertable)
			break


source = os.getcwd()

ASCII_SIZE = 8
SOUND_FILE_DIR = source+"\sounds\\"
CHAR_DELIMITER = '.'
CHAR_DELIMITER_FILE = SOUND_FILE_DIR+"char_delimiter.wav"
WORD_DELIMITER = '_'
WORD_DELIMITER_FILE = SOUND_FILE_DIR+"word_delimiter.wav"

#Establish the dictionary of pokemon which can be used, and their sounds
knownPokemon = dict()
knownPokemon['pikachu'] = Pokemon('pikachu',['pi','ka','chu'])

for p in knownPokemon:
	knownPokemon[p].loadSounds()

#asciiFileToPokeSpeech(knownPokemon['pikachu'],source+"\exampleTexts\simple.txt")
asciiFileToPokeWav(knownPokemon['pikachu'],source+"\exampleTexts\simple.txt")