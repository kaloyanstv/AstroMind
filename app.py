import json
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import MessageRole
from azure.identity import DefaultAzureCredential
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Replace with a secure secret

# Initialize the Azure AI Project client.
project_client = AIProjectClient.from_connection_string(
    credential=DefaultAzureCredential(),
    conn_str="eastus2.api.azureml.ms;d1ca9675-944b-4a77-b674-f4180d8122ef;agentsdk;project-demo-xnpv",
)
thread = project_client.agents.create_thread()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/genprofiles", methods=["POST"])
def genprofiles():
    # Collect names and incident from the form.
    names = {
        "commander": request.form.get("name_commander"),
        "engineer": request.form.get("name_engineer"),
        "scientist": request.form.get("name_scientist"),
        "pilot": request.form.get("name_pilot"),
        "medic": request.form.get("name_medic"),
    }
    incident = request.form.get("incident")
    
    # Build a prompt for ProfileAI.
    profile_prompt = (
        "Search the web and retrieve factual, publicly available biographies for the following individuals. "
        "For each, return a plain text summary preceded by the role label. But do not pay attention to the role while searching\n\n"
    )
    for role, name in names.items():
        profile_prompt += f"{role.capitalize()}: {name}\n"
    
    # Call ProfileAI.
    profile_agent = project_client.agents.get_agent("asst_IWOREmGaT0lkuj9nOI90rYc6")
    profile_thread = project_client.agents.create_thread()
    project_client.agents.create_message(
        thread_id=profile_thread.id, role="user", content=profile_prompt
    )
    project_client.agents.create_and_process_run(
        thread_id=profile_thread.id, agent_id=profile_agent.id
    )
    profile_response = project_client.agents.list_messages(
        thread_id=profile_thread.id
    ).get_last_message_by_role(MessageRole.AGENT)
    profiles_text = ""
    if profile_response:
        for msg in profile_response.text_messages:
            profiles_text += msg.text.value + "\n"
    
    # (Optionally, store profiles in session for debugging.)
    session["profiles"] = profiles_text
    
    # Build a prompt for ProblemAI.
    problem_prompt = (
        "Team profiles:\n"
        f"{profiles_text}\n\n"
        "Incident description below:\n"
        f"{incident}\n\n"
    )
    
    # Call ProblemAI.
    problem_agent = project_client.agents.get_agent("asst_bSX6frsDeNLnI5Kpdi7KdrIS")
    project_client.agents.create_message(
        thread_id=thread.id, role="user", content=problem_prompt
    )
    project_client.agents.create_and_process_run(
        thread_id=thread.id, agent_id=problem_agent.id
    )
    problem_response = project_client.agents.list_messages(
        thread_id=thread.id
    ).get_last_message_by_role(MessageRole.AGENT)
    conversation_text = ""
    if problem_response:
        for msg in problem_response.text_messages:
            conversation_text += msg.text.value + "\n"
    
    # Store the conversation text for later reference.
    session["conversation"] = conversation_text
    return jsonify({"conversation": conversation_text})

@app.route("/answer", methods=["POST"])
def answer():
    user_input = request.form.get("solution_input")
    # Send the solution message to ProblemAI.
    problem_agent = project_client.agents.get_agent("asst_bSX6frsDeNLnI5Kpdi7KdrIS")
    project_client.agents.create_message(
        thread_id=thread.id, role="user", content=user_input
    )
    project_client.agents.create_and_process_run(
        thread_id=thread.id, agent_id=problem_agent.id
    )
    problem_response = project_client.agents.list_messages(
        thread_id=thread.id
    ).get_last_message_by_role(MessageRole.AGENT)
    conversation_text = ""
    if problem_response:
        for msg in problem_response.text_messages:
            conversation_text += msg.text.value + "\n"
    session["conversation"] = conversation_text
    return jsonify({"conversation": conversation_text})

@app.route("/validate_solution", methods=["POST"])
def validate_solution():
    solution = request.form.get("solution_input")
    # Build a prompt for GodAI.
    god_prompt = (
        "Evaluate the following proposed solution to the incident described above. "
        "Do not suggest any new actions; simply analyze whether the solution addresses the failure adequately and explain why or why not.\n\n"
        f"Solution: {solution}"
    )
    god_agent = project_client.agents.get_agent("asst_RTmTW56uvhXgyBYeGW7cltW8")
    project_client.agents.create_message(
        thread_id=thread.id, role="user", content=god_prompt
    )
    project_client.agents.create_and_process_run(
        thread_id=thread.id, agent_id=god_agent.id
    )
    god_response = project_client.agents.list_messages(
        thread_id=thread.id
    ).get_last_message_by_role(MessageRole.AGENT)
    validation_text = ""
    if god_response:
        for msg in god_response.text_messages:
            validation_text += msg.text.value + "\n"
    # Return only the validation feedback.
    return jsonify({"validation": validation_text})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)