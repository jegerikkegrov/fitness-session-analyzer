from data_generator import generate_fitness_data


class ReferenceProfile:
    def __init__(self, baseline_heart_rate, baseline_skin_response, baseline_temperature):
        self.baseline_heart_rate = baseline_heart_rate
        self.baseline_skin_response = baseline_skin_response
        self.baseline_temperature = baseline_temperature

class Participant:
    def __init__(self, participant_id, reference_profile):
        self.participant_id = participant_id
        self.reference_profile = reference_profile


class Observation:
    def __init__(self, timestamp, heart_rate, skin_response, temperature, activity_level, signal_quality):
        self.timestamp = timestamp
        self.heart_rate = heart_rate
        self.skin_response = skin_response
        self.temperature = temperature
        self.activity_level = activity_level
        self.signal_quality = signal_quality


class FitnessSession:
    def __init__(self, participant):
        self.participant = participant
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)

def valid_heart_rate(heart_rate):
    if heart_rate is None:
        return False

    if heart_rate < 35 or heart_rate > 205:
        return False

    return True

def valid_temperature(temperature):
    if temperature is None:
        return False

    if temperature < 25 or temperature > 42:
        return False

    return True



profile, observations = generate_fitness_data(
    participant_id= "P001",
    scenario= "moderate_activity",
    seed= 42,
    number_of_windows= 12
)


reference_profile = ReferenceProfile(
    profile["baseline_heart_rate"],
    profile["baseline_skin_response"],
    profile["baseline_temperature"]
)

participant = Participant(
    profile["participant_id"],
    reference_profile
)

session = FitnessSession(participant)



for data in observations:
    observation = Observation(
        data["timestamp"],
        data["heart_rate"],
        data["skin_response"],
        data["temperature"],
        data["activity_level"],
        data["signal_quality"]
    )

    session.add_observation(observation)


print("Participants", session.participant.participant_id)
print("Number of observations:", len(session.observations))












