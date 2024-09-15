from langchain_community.llms import OpenAI, Anthropic
from langchain_google_vertexai import VertexAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os


# Set your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google-credentials.json"
env = os.getenv('ENV', 'development')  # Default to 'development' if ENV is not set
dotenv_file = f'.env.{env}'
load_dotenv(dotenv_file)


class AIMentorPrototype:
    def __init__(self, model_name="vertex"):
        self.model_name = model_name
        self.llm = self._initialize_llm()
        self.memory = ConversationBufferMemory()
        self.conversation = ConversationChain(llm=self.llm, memory=self.memory)
        self.user_progress = {}
        self.db_connection = self._initialize_database()


    def _initialize_llm(self):
        if self.model_name.startswith("gpt"):
            return OpenAI(model_name=self.model_name)
        elif self.model_name.startswith("claude"):
            return Anthropic(model=self.model_name)
        elif self.model_name.startswith("vertex"):
            return VertexAI(
                model_name="text-bison@001",  # or any other available Vertex AI model
                max_output_tokens=1024,
                temperature=0.2,
                top_p=0.8,
                top_k=40
            )
        else:
            raise ValueError("Unsupported model")

    def _initialize_database(self):
        conn = psycopg2.connect(
            os.getenv('DB_URL')
        )
        return conn

    def identify_user_interest(self, user_input):
        prompt = PromptTemplate(
            input_variables=["user_input"],
            template="Identify the main interests and skills from the following user input: {user_input}"
        )
        return self.llm(prompt.format(user_input=user_input))

    def recommend_courses(self, interests):
        prompt = PromptTemplate(
            input_variables=["interests"],
            template="Recommend courses to enhance skills in: {interests}"
        )
        return self.llm(prompt.format(interests=interests))

    def track_progress(self, user_id, activity):
        if user_id not in self.user_progress:
            self.user_progress[user_id] = []
        self.user_progress[user_id].append(activity)

    def connect_to_mentor(self, user_interests):
        cursor = self.db_connection.cursor()
        query = sql.SQL("""
            SELECT name, expertise, experience
            FROM mentors
            WHERE expertise @> %s
            ORDER BY experience DESC
            LIMIT 1
        """)
        cursor.execute(query, (user_interests,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return f"Mentor: {result[0]}, Expertise: {result[1]}, Experience: {result[2]} years"
        else:
            return "No suitable mentor found"

    def process_mentor_feedback(self, feedback):
        prompt = PromptTemplate(
            input_variables=["feedback"],
            template="Analyze the following mentor feedback and provide recommendations: {feedback}"
        )
        return self.llm(prompt.format(feedback=feedback))

    def get_government_aids(self, industry):
        prompt = PromptTemplate(
            input_variables=["industry"],
            template="List government aids available for businesses in the {industry} industry"
        )
        return self.llm(prompt.format(industry=industry))

    def assist_msme_registration(self):
        return self.llm("Provide steps for registering a business as an MSME")

    def interact(self, user_input):
        response = self.conversation.predict(input=user_input)
        return response

    def close(self):
        self.db_connection.close()

# Usage example
ai_mentor = AIMentorPrototype(model_name="vertex")
user_input = "I'm interested in starting a sustainable fashion business but I'm not sure where to begin."
interests = ai_mentor.identify_user_interest(user_input)
courses = ai_mentor.recommend_courses(interests)
mentor = ai_mentor.connect_to_mentor(interests)
ai_mentor.track_progress("user123", "Identified interests and recommended courses")

print(f"Identified Interests: {interests}")
print(f"Recommended Courses: {courses}")
print(f"Suggested Mentor: {mentor}")

ai_mentor.close()