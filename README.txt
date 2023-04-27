Program usage:

py gpt_file_processor.py <arg> <filename/path>

arguments:
	-p : The processor will query openAI's chat gpt with the prompts in the file
	-w : The processor will request that openAI's chat gpt categorizes all the websites in the file with IAB categories

File formatting:
	Each individual prompt/file should be on its own new line. CSV files and .txt files are both valid. Other inputs are questionable.