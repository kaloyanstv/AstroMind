# AstroMind Simulator

AstroMind Simulator is an AI-driven space psychology simulation project that allows users to step into Mission Control. The application simulates crew interactions, problem-solving, and decision-making under space mission challenges. Users can input crew member names, select a common incident, and receive AI-generated conversation responses and solution validation via integrated Azure AI endpoints.

---

## Features

- **Crew Input & Incident Selection**  
  Collects real names for key crew roles (Commander, Engineer, Scientist, Pilot, Medic) and allows users to choose from a list of common spacecraft issues.

- **AI-Driven Conversation**  
  Generates a simulated conversation among team members based on the provided crew profiles and incident details.

- **Solution Proposal & Validation**  
  Users can propose a solution which is processed by the bot. Two functionalities are provided:
  - **Send to Chat:** Updates the team conversation with the AI's response.
  - **Validate Solution:** Provides analysis and feedback via a pop-up to help determine if the solution adequately addresses the incident.

- **Unified Beautiful Frontend**  
  Combines a visually appealing interface with advanced simulation functionality. The design features space-themed graphics, a modern layout, and a responsive design.

- **Backend Integration**  
  Uses a Flask backend integrated with the Azure AI Project Client to handle message processing, conversation updates, and solution validation.

---

## Architecture

### Frontend

- **HTML/CSS/JavaScript:**  
  A single-page application that combines mission crew input, incident selection, conversation display, and solution input within a unified form.

- **User Interface:**  
  Designed with a space-themed aesthetic using custom CSS and the Audiowide Google Font. The design is fully responsive and integrates all inputs and outputs within one seamless container.

- **Backend Connectivity:**  
  JavaScript `fetch` calls interact with Flask backend endpoints:
  - The `/genprofiles` endpoint processes crew and incident input, returning an initial conversation.
  - The `/answer` endpoint sends a user-proposed solution to update the conversation.
  - The `/validate_solution` endpoint validates the proposed solution and returns feedback.

### Backend

- **Flask Application:**  
  Serves HTML templates and static assets, and handles API endpoints for conversation and solution processing.

- **Azure AI Integration:**  
  Utilizes the Azure AI Project Client and associated agents to generate responses for team conversation and solution validation.

- **Session Management:**  
  Uses Flask sessions to store conversation history and other temporary data during user interactions.

---

## Setup & Installation

### Prerequisites

- Python 3.7 or higher
- Flask
- Azure AI Projects SDK
- Azure Identity (for authentication)
- An active Azure subscription with configured AI agents and connection strings

### Installation Steps

1. Clone the repository from GitHub.
2. Create a virtual environment (optional but recommended) and activate it.
3. Install the project dependencies using the requirements file.
4. Update your Flask application (for example, in `app.py`) with the correct Azure connection string and credentials. Replace any placeholder values (such as `"your_secret_key_here"`) with secure values and valid Azure configuration details.
5. Run the Flask application.
6. Open your web browser and navigate to the local server address (e.g., `http://127.0.0.1:5000`) to interact with AstroMind Simulator.

---

## Usage

1. **Enter Crew & Incident Details:**  
   Fill in the crew member names and select a common spacecraft issue from the dropdown on the beautiful frontend interface.

2. **Submit Problem:**  
   Click the **Submit Problem** button. Your input is sent to the backend via the `/genprofiles` endpoint, which processes the profiles and returns an initial AI-generated conversation.

3. **Propose a Solution:**  
   Once the conversation is displayed, type your solution into the solution input field.

4. **Send to Chat:**  
   Click **Send to Chat** to append your solution and the subsequent AI response to the conversation.

5. **Validate Solution:**  
   Click **Validate Solution** to receive a pop-up with feedback from the AI regarding whether your proposed solution adequately addresses the incident.

---

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask
- **AI Integration:** Azure AI Projects, Azure Identity
- **Deployment:** Local development server (Flask), extendable to cloud deployment

---

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with your improvements or bug fixes.

---

## Contact

For further information or support, please contact [Nikita Chernevskiy](mailto:nikita.chernevskiy@hotmail.com).

---

AstroMind Simulator is designed to help users explore the complex dynamics of space missions through AI-driven simulations. Enjoy exploring the cosmos with AstroMind!