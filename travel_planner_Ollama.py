import streamlit as st
import subprocess

# Helper class to use Ollama LLaMA 3 locally
class OllamaLlama3:
    def __init__(self, model="llama3"):
        self.model = model

    def run(self, prompt):
        try:
            result = subprocess.run(
                ["ollama", "run", self.model],
                input=prompt,
                text=True,
                capture_output=True,
                timeout=60
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            return "⚠️ Timeout: The model took too long to respond."


# Initialize model
llm = OllamaLlama3()

# Streamlit UI
st.set_page_config(page_title="Local AI Travel Planner", page_icon="🌍")
st.title("✈️ AI Travel Planner (Offline with LLaMA 3)")
st.caption("Powered by Ollama LLaMA 3 running fully local")

destination = st.text_input("📍 Where do you want to go?")
num_days = st.number_input("🗓️ Number of days", min_value=1, max_value=30, value=5)
budget= st.number_input("Budget", min_value= 1000, max_value= 10000)


if st.button("🧠 Generate Travel Plan") and destination:
    with st.spinner("🔍 Gathering activity ideas..."):
        mock_research = f"""
        Suggest top activities for a {num_days}-day trip to {destination}. 
        Include cultural spots, outdoor adventures, local foods, and offbeat places.
        Return only bullet points.
        """
        activities = llm.run(mock_research)
        st.success("Activities generated!")
        st.write("### 🎯 Top Things To Do")
        st.markdown(activities)

    with st.spinner("📅 Generating itinerary..."):
        itinerary_prompt = f"""
        Based on a {num_days}-day trip to {destination}, within the {budget} and activities like:
        {activities}

        Create a day-wise itinerary for a traveler visiting for {num_days} days.
        Format it with Day 1, Day 2... and include local tips if needed.
        """
        itinerary = llm.run(itinerary_prompt)
        st.success("Itinerary ready!")
        st.write("### 🗺️ Day-wise Itinerary")
        st.markdown(itinerary)

    with st.spinner("🏨 Finding accommodations..."):
        hotel_prompt = f"""
        Suggest 5 good places to stay in {destination} — Airbnbs, within the {budget} for {num_days}
        For each, include: Name, Type (Hotel/Airbnb), Price Range, and Why it's a good choice.
        """
        stays = llm.run(hotel_prompt)
        st.success("Stay options ready!")
        st.write("### 🛏️ Recommended Stays")
        st.markdown(stays)

    with st.spinner("🚗 Car rental options..."):
        car_prompt = f"""
        Suggest 3 car rental options for tourists in {destination}. 
        Include: Company Name, Car Types, Price Range, and why it's recommended.
        """
        cars = llm.run(car_prompt)
        st.success("Car rental suggestions ready!")
        st.write("### 🚗 Car Rental Options")
        st.markdown(cars)
