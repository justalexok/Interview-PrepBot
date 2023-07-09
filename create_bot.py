import openai
import os
import create_bot
from dotenv import load_dotenv
import re
import tiktoken

load_dotenv()
openai.api_key = os.getenv('MyKey')

class CreateBot:

	def __init__(self,system_prompt):

		self.system = system_prompt
		self.messages = [
			{"role":"system","content": system_prompt},
			{"role":"user","content": "Let's begin our roleplay. Ask me a question"}
			]

	def chat(self):

		print('To end conversation, type "END".')

		answer = ''

		while answer != 'END':
			

			response = openai.ChatCompletion.create(
							model = "gpt-3.5-turbo",
							messages = self.messages
							)

			question = response['choices'][0]['message']['content']
			print('\n')
			print(question)
			print('\n')
			self.messages.append({'role':'assistant','content':question})

			answer = input("")
			print('\n')

			self.messages.append({'role':'user','content':answer})

			self.rate_answer(answer)


			filtered_msgs = []
			for msg in self.messages:
				if msg['role'] == 'user':
					continue
				filtered_msgs.append(msg)
			self.messages = filtered_msgs

			self.messages.append({'role':'user','content':"Next Question please."})

			full_text = self.get_full_text()
			num_tokens = self.num_tokens_from_string(full_text,'cl100k_base')
			print(f"Number of tokens: {num_tokens}")
			print(f"Length of messages: {len(self.messages)}")
			# for msg in self.messages:
			# 	print('\n')
			# 	print(msg)

	def get_question(self):

		self.messages.append({'role':'user','content':"Next Question please."})

		response = openai.ChatCompletion.create(
							model = "gpt-3.5-turbo",
							messages = self.messages
							)

		question = response['choices'][0]['message']['content']
		self.messages.append({'role':'assistant','content':question})

		return question

	def rate_answer(self,answer):

		self.messages.append({'role':'user','content':answer})

		self.messages.append({'role':'user','content':f"Now please rate my answer out of 5 in terms of {criteria}"})

		response = openai.ChatCompletion.create(
							model = "gpt-3.5-turbo",
							messages = self.messages
							)

		rating_description = response['choices'][0]['message']['content']
		rating = self.get_rating_int(rating_description)

		print(f"Rating as int: {rating}")

		return rating_description

	def get_rating_int(self,rating):

		match = re.search(r'\d+', rating)
		if match:
			return int(match.group())
		else:
			return None

	def num_tokens_from_string(self,string, encoding_name):
		encoding = tiktoken.get_encoding(encoding_name)
		num_tokens = len(encoding.encode(string))
		return num_tokens

	def get_full_text(self):
		full_text = ''
		for item in self.messages:
			full_text += item['content']
		return full_text
		

criteria = "how suitable does this answer suggest the candidate is for the role"

def get_prompt(role,company):

	job_interviewer_prompt = f"""
		You are interviewing me for a job. The Company is {company} and the role is {role}. 
		You're aim is to determine whether I am a good candidate for this role by asking relevant questions
		You could ask me questions relevant to the role, company and industry.
		You could also ask standard interview questions to determine if I am suitable for this role. 
		You could test my skillset with some practical quick tasks.
		Do not repeat any questions you've asked before.
	"""
	return job_interviewer_prompt

# interviewer = CreateBot(system_prompt = job_interviewer_prompt)

# interviewer.chat()



# spanish_girl_prompt = """
# You are a flirting tutor and we are engaging in conversational role play. You are playing the role of a young english-speaking spanish girl.
# The conversation should be in English.
# You should be able to rate my input in terms of how suitable a response it is for increasing romantic interest, given your age and nationality. 
# The highest rating should be for answers that illicit a romantic connection, are suitable for my age and nationality and fit with the flow of the conversation well. 
# The lowest rating might be inappropriate, dull, plain, unsuitable for my age or nationality or out of context for the flow of the conversation

# """

# spanish_girl = CreateBot(system_prompt = spanish_girl_prompt)

# criteria = "how suitable a response it is for increasing romantic interest, given your age and nationality."

# spanish_girl.chat()