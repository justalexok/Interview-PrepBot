from flask import Flask, render_template, request, jsonify, session
import create_bot


app = Flask(__name__)
app.secret_key = 'your-secret-key'

interviewer = create_bot.CreateBot(system_prompt = "blank")

@app.route("/")
@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/begin_interview", methods=['POST'])
def begin_interview():
	output = request.json  # Access the JSON data sent in the request body
	company = output.get("company")
	role = output.get("role")
	print(role, company)

	prompt = create_bot.get_prompt(role,company)
	interviewer = create_bot.CreateBot(system_prompt = prompt)

	print(interviewer.system)

	firstQ = interviewer.get_question()

	session['prompt'] = prompt
	session['messages'] = [{"role":"assistant","content": firstQ}]
	session.modified = True

	return jsonify(firstQ=firstQ)  # Return firstQ as a JSON response


@app.route("/rate_answer", methods=['POST'])
def rate_answer():
	output = request.json
	answer = output.get("answer")
	print(answer)

	prompt = session['prompt']
	messages = session['messages']

	interviewer = create_bot.CreateBot(system_prompt = prompt)
	for msg in messages:
		interviewer.messages.append(msg)

	print('Interviewer.messages inside rate_answer')
	for msg in interviewer.messages:
		print('\n')
		print('\t',msg)


	rating = interviewer.rate_answer(answer)
	print(rating)

	session['messages'].append({"role":"user","content": answer})
	session.modified = True

	return jsonify(rating=rating)

@app.route("/ask_question", methods=['POST'])
def ask_question():

	prompt = session['prompt']
	messages = session['messages']

	interviewer = create_bot.CreateBot(system_prompt = prompt)
	for msg in messages:
		interviewer.messages.append(msg)
	
	print('Interviewer.messages inside ask_question')
	for msg in interviewer.messages:
		print('\n')
		print('\t',msg)

	next_question = interviewer.get_question()
	session['messages'].append({"role":"assistant","content": next_question})
	session.modified = True

	return jsonify(next_question = next_question)


if __name__ == '__main__':
	app.run(debug=True,port=5001)